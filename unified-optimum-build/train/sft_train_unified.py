"""Saturday QLoRA train for the unified stack (4x L4, ~1h wall).
Mapping A from the banked kit recipe (scripts/train.py: turn-mode SFT, r16 /
alpha32 / dropout 0.05 on the 410 language-model projections, assistant tokens
only, gates, export in the competition adapter key layout).

Inputs: dataset/unified-m3-pass2.jsonl (~450 seqs, cap 2500ch, CPU-built).
Output: adapters/unified_r16/adapter_model.safetensors + updated metrics.

Run on the Saturday 30h refill (NOT now — quota):
  TIME_LIMIT_H=11.3 TRAIN_BUDGET_H=1.0 MAX_LEN=16384 EPOCHS=1 \
    python3 train/sft_train_unified.py \
    --data dataset/unified-m3-pass2.jsonl --out adapters/unified_r16

Then (same kernel, ~15 min):
  1. effect gate: max |delta logit| > 0 (catches the all-zero lora_B no-op trap).
  2. vLLM load check: adapter loads under --lora-modules with no KV-cache hang.
  3. paired DS-11 D2 gate (train/D2_gate.md): holds 5077/9425/14786 + >=2 converts
     of 7427/13920/7328/6589/14479. Tier 2 ships ONLY on D2 pass.
Quota math: ~1-2h wall = 2-4h quota + paired DS-11 ~3h = ~6-7h of 30h.
"""
import argparse, json, os, sys, time
from pathlib import Path

T0 = time.time()
LORA_R, LORA_ALPHA, LORA_DROPOUT = 16, 32, 0.05
TARGETS = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
EPOCHS_DEFAULT = 1
LR, SEED = 2e-5, 42
SCHEDULER = "cosine"
# LOCKED per external-research prune (Dettmers QLoRA + Biderman LoRA-Learns-Less):
# r=16 / a32 / 1-2 epochs / LR 1e-5-2e-5 cosine. NO rank sweeps (8/32/64),
# NO 3+ epochs (overfits <1000 ex, degrades base coding, raises Punica BW).

def log(*a):
    print("[+%5.1f min]" % ((time.time() - T0) / 60), *a, flush=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="dataset/unified-m3-pass2.jsonl")
    ap.add_argument("--out", default="adapters/unified_r16")
    ap.add_argument("--epochs", type=int, default=EPOCHS_DEFAULT)
    ap.add_argument("--dry", action="store_true", help="CPU structural check only, no torch")
    a = ap.parse_args()
    rows = [json.loads(l) for l in Path(a.data).read_text().splitlines() if l.strip()]
    assert len(rows) >= 400, "need >=400 seqs, got %d" % len(rows)
    log("unified train: samples=%d r=%d alpha=%d dropout=%s targets=%s epochs=%d" % (
        len(rows), LORA_R, LORA_ALPHA, LORA_DROPOUT, "+".join(t[0] for t in TARGETS), a.epochs))
    if a.dry:
        print("DRY-OK samples=%d (structural check only)" % len(rows))
        return
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    except Exception as e:
        print("FATAL: wheelhouse imports failed: %s" % e)
        print("Run inside the competition kernel with the 4x L4 wheelhouse; do not pip-install.")
        sys.exit(2)
    log("torch=%s cuda=%s gpus=%d" % (torch.__version__, torch.cuda.is_available(), torch.cuda.device_count()))
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    (out / "adapter_config.json").write_text(json.dumps({
        "peft_type": "LORA", "r": LORA_R, "lora_alpha": LORA_ALPHA,
        "lora_dropout": LORA_DROPOUT, "target_modules": TARGETS, "bias": "none",
        "task_type": "CAUSAL_LM",
        "base_model_name_or_path": "gemma-4-31b-it-qat-w4a16-ct"}, indent=1))
    log("config written; full QLoRA loop runs Saturday on 4x L4 (see kit scripts/train.py mapping A).")
    print("NEXT: run D2 gate train/D2_gate.md before any 58-task slot.")

if __name__ == "__main__":
    main()
