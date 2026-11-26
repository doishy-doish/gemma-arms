"""LoRA-on-CPU feasibility probe (Duck lane, public GH runner: 4vCPU/16GB/6h wall).
NOT a scoring adapter (wrong base) — answers: (a) does CPU LoRA fit/run, (b) wall-time per
step, (c) any delta signal on a gradeable proxy. KILL-or-PROVE: if step-time blows the 6h
envelope, the probe itself is the answer (CPU-LoRA infeasible, stop).
Design: Qwen2.5-Coder-1.5B-Instruct fp32 frozen + LoRA r16 (attn only), CPU AdamW,
micro-batch 1, ctx 1024, grad-checkpointing. Train on HumanEval-train canonical solutions,
eval pass@1 (execution, in-runner, no docker) on held-out split: BASE vs +LoRA delta.
Budget: <=100min train (hard wall-clock exit), ~20min per eval leg. Total < 3h.
M502. Public-repo safe: no keys, no private data, HF-only downloads.
"""
import json, os, sys, time, math, resource, traceback

RUN_H = float(os.environ.get("PROBE_HOURS", "2.5"))
T0 = time.time()
WALL = RUN_H * 3600
MAX_STEPS = int(os.environ.get("MAX_STEPS", "150"))
CTX = 1024
EVAL_TOKENS = 128

def log(msg):
    print(f"[lora-probe t={time.time()-T0:7.1f}s] {msg}", flush=True)

def mem_gb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6

def wall_left():
    return WALL - (time.time() - T0)

def main():
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from peft import LoraConfig, get_peft_model, TaskType
    from datasets import load_dataset

    BASE = "Qwen/Qwen2.5-Coder-1.5B-Instruct"
    log(f"torch={torch.__version__} threads={torch.get_num_threads()} mem={mem_gb():.2f}GB")
    torch.set_num_threads(4)

    log(f"loading {BASE} (fp32, CPU)...")
    tok = AutoTokenizer.from_pretrained(BASE, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    model = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype=torch.float32,
                                                 trust_remote_code=True)
    model.gradient_checkpointing_enable()
    model.train()
    log(f"base loaded mem={mem_gb():.2f}GB params={sum(p.numel() for p in model.parameters())/1e9:.2f}B")

    # ---- data: HumanEval, canonical solutions as SFT targets, 120 train / 44 held-out
    ds = load_dataset("openai_humaneval")["test"]
    items = [{"task_id": r["task_id"], "prompt": r["prompt"], "solution": r["canonical_solution"],
              "entry": r["entry_point"], "tests": r["test"]} for r in ds]
    train, held = items[:120], items[120:]
    log(f"train={len(train)} held={len(held)}")

    def fmt(it):
        return ("### Task\n" + it["prompt"] + "\n### Solution\n" + it["prompt"] + it["solution"])

    # ---- BASE eval first (greedy, execution-graded) so the delta is apples-to-apples
    base_score = evaluate(model, tok, held, tag="BASE")
    log(f"BASE held-out pass@1 = {base_score:.3f} wall_left={wall_left()/60:.0f}min")

    # ---- LoRA wrap (attention projections only = cheapest trainable surface)
    cfg = LoraConfig(task_type=TaskType.CAUSAL_LM, r=16, lora_alpha=32, lora_dropout=0.05,
                     target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])
    model = get_peft_model(model, cfg)
    model.print_trainable_parameters()
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=2e-4)

    # ---- train loop, micro-batch 1, accum 8, hard wall exit
    step, acc, losses, step_times = 0, 0, [], []
    model.train()
    idx = 0
    while step < MAX_STEPS and wall_left() > 20 * 60:
        it = train[idx % len(train)]; idx += 1
        s = time.time()
        try:
            enc = tok(fmt(it), return_tensors="pt", truncation=True, max_length=CTX)
            out = model(input_ids=enc["input_ids"], labels=enc["input_ids"])
            (out.loss / 8).backward()
            acc += 1
            if acc % 8 == 0:
                opt.step(); opt.zero_grad(); step += 1
                dt = time.time() - s
                step_times.append(dt); losses.append(out.loss.item())
                if step % 10 == 0:
                    log(f"step={step} loss={out.loss.item():.3f} step_s={dt:.1f} "
                        f"mean_step_s={sum(step_times)/len(step_times):.1f} mem={mem_gb():.2f}GB "
                        f"wall_left={wall_left()/60:.0f}min")
        except Exception as e:
            log(f"STEP-ERROR (continuing): {type(e).__name__}: {str(e)[:200]}")
            opt.zero_grad(); acc = 0
    log(f"train done steps={step} wall_left={wall_left()/60:.0f}min")
    proj = (sum(step_times) / max(len(step_times), 1)) * MAX_STEPS / 60 if step_times else -1
    log(f"measured mean_step_s={sum(step_times)/max(len(step_times),1):.1f} "
        f"projected_full_run_min={proj:.0f} (envelope=360min)")

    # ---- +LoRA eval on same held-out
    lora_score = evaluate(model, tok, held, tag="LORA")
    log(f"LORA held-out pass@1 = {lora_score:.3f} delta={lora_score-base_score:+.3f}")

    metrics = {"base_pass1": base_score, "lora_pass1": lora_score,
               "delta": lora_score - base_score, "steps": step,
               "mean_step_s": sum(step_times) / max(len(step_times), 1),
               "losses": losses, "wall_used_min": (time.time() - T0) / 60,
               "mem_gb": mem_gb()}
    os.makedirs("/tmp/lora_out", exist_ok=True)
    json.dump(metrics, open("/tmp/lora_out/metrics.json", "w"), indent=1)
    try:
        model.save_pretrained("/tmp/lora_out/adapter")
        log("adapter saved")
    except Exception as e:
        log(f"adapter-save failed (metrics still valid): {e}")
    print("METRICS " + json.dumps(metrics), flush=True)

def evaluate(model, tok, held, tag="EVAL"):
    """Greedy completion + exec() the HumanEval test. Returns pass@1."""
    import torch
    model.eval()
    wins, total = 0, 0
    for it in held:
        if wall_left() < 15 * 60:
            log(f"{tag}: wall guard, stopping early at {total}/{len(held)}")
            break
        try:
            enc = tok("### Task\n" + it["prompt"] + "\n### Solution\n" + it["prompt"],
                      return_tensors="pt", truncation=True, max_length=CTX)
            with torch.no_grad():
                gen = model.generate(enc["input_ids"], max_new_tokens=EVAL_TOKENS,
                                     do_sample=False, pad_token_id=tok.eos_token_id)
            code = tok.decode(gen[0][enc["input_ids"].shape[1]:], skip_special_tokens=True)
            full = it["prompt"] + code + "\n" + it["tests"] + f"\ncheck({it['entry']})"
            ns = {}
            exec(compile(full, "<gen>", "exec"), {"__builtins__": __builtins__}, ns)
            wins += 1
        except Exception:
            pass
        total += 1
    model.train()
    return wins / max(total, 1)

if __name__ == "__main__":
    try:
        main()
    except Exception:
        log("FATAL\n" + traceback.format_exc())
        sys.exit(3)
