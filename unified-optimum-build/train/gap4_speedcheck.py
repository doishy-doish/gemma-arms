"""Gap-4 speed check: stock 31B vs 31B + 233MB kit adapter on 4x L4 (10-min, 0 training).

Staged for 1-click fire when the 30h pool refreshes. NOT run now (quota over).

What it does (same kernel, back-to-back, no other load):
  1. Load stock gemma-4-31b-it-qat-w4a16-ct, generate 128 tokens x2 canary prompts,
     record wall + tok/s (3 reps, take median).
  2. Load same base + scottweeden/gemma-4-31b-swe-tool-use-lora (r16/a32, 233.6MiB,
     410 projections, export layout validated in KITTEST-CPU), repeat.
  3. Write JSON: {base_tps, ada_tps, tax_pct, base_wall, ada_wall}; decide
     train-or-lock: tax must leave 120 x mean_task_wall inside 720 min.
     Rule: projected = 120 x (252.5s x ada_wall/base_wall); PASS if <= 690 min
     (30 min safety under the 12h agent cap), else lock lean stock Tier 1.

Run (inside the competition 4x L4 kernel, ~10 min wall, ~20 min quota):
  python3 train/gap4_speedcheck.py --reps 3 --tokens 128 --out train/gap4-result.json

Then: PASS -> fire upgraded train (dataset v2); FAIL -> lock lean stock Tier 1.
Punica 27-45% stays QUARANTINED until this script's numbers land: the banked
timing-core 20.09->11.01 eff tok/s is episode throughput incl. tool/IO, NOT a
server decode rate, so it cannot settle Gap 4.
"""
import argparse, json, statistics, time
from pathlib import Path

CANARIES = [
    "canary-14786: workspace-true import check + 1-line diff (hold probe)",
    "canary-9425: cliff probe, 2-file fan-out sketch (28-call wobble probe)",
]

def _measure(generate_fn, prompt, tokens, reps):
    walls, tps = [], []
    for _ in range(reps):
        t0 = time.time()
        n = generate_fn(prompt, tokens)
        w = time.time() - t0
        walls.append(w); tps.append(n / max(w, 1e-6))
    return statistics.median(walls), statistics.median(tps)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--tokens", type=int, default=128)
    ap.add_argument("--out", default="train/gap4-result.json")
    ap.add_argument("--dry", action="store_true",
                    help="CPU structural check only: validate JSON shape, no torch/vLLM")
    a = ap.parse_args()
    if a.dry:
        fake = {"base_tps": 20.1, "ada_tps": 15.9, "tax_pct": 20.9,
                "base_wall": 6.4, "ada_wall": 8.1, "dry": True,
                "decision": "STAGED (dry shape ok, run on 4x L4 after refill)"}
        Path(a.out).write_text(json.dumps(fake, indent=1))
        print("DRY-OK -> %s (shape only, no GPU touched)" % a.out)
        return
    try:
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM
        from peft import PeftModel
    except Exception as e:
        print("FATAL: need competition kernel wheelhouse (torch/transformers/peft): %s" % e)
        raise SystemExit(2)
    base_id = "gemma-4-31b-it-qat-w4a16-ct"
    ada_id = "scottweeden/gemma-4-31b-swe-tool-use-lora"
    print("load base: %s" % base_id, flush=True)
    tok = AutoTokenizer.from_pretrained(base_id)
    base = AutoModelForCausalLM.from_pretrained(base_id, torch_dtype="auto")
    def gen_base(prompt, n):
        ids = tok(prompt, return_tensors="pt").input_ids
        t0 = time.time()
        with torch.no_grad():
            out = base.generate(ids, max_new_tokens=n, do_sample=False)
        return out.shape[1] - ids.shape[1]
    print("load adapter: %s" % ada_id, flush=True)
    ada = PeftModel.from_pretrained(base, ada_id)
    def gen_ada(prompt, n):
        ids = tok(prompt, return_tensors="pt").input_ids
        with torch.no_grad():
            out = ada.generate(ids, max_new_tokens=n, do_sample=False)
        return out.shape[1] - ids.shape[1]
    bw, bt = _measure(gen_base, CANARIES[0], a.tokens, a.reps)
    aw, at = _measure(gen_ada, CANARIES[0], a.tokens, a.reps)
    tax = 100.0 * (bt - at) / max(bt, 1e-9)
    proj = 120 * (252.5 * aw / max(bw, 1e-9)) / 60.0
    decision = "TRAIN" if proj <= 690 else "LOCK-LEAN-STOCK"
    res = {"base_tps": round(bt, 2), "ada_tps": round(at, 2), "tax_pct": round(tax, 1),
           "base_wall": round(bw, 2), "ada_wall": round(aw, 2),
           "projected_120min": round(proj, 1), "decision": decision,
           "reps": a.reps, "tokens": a.tokens}
    Path(a.out).write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))
    print("NEXT: %s" % ("fire upgraded train (dataset v2)" if decision == "TRAIN" else "lock lean stock Tier 1"))

if __name__ == "__main__":
    main()
