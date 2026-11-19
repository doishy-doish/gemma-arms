#!/usr/bin/env python3
"""Tiny CPU LoRA train for the 0.5B probe (rung 1: format-teaching).

Reads chat-format SFT JSONL (messages arrays), masks non-assistant tokens,
trains a rank-r LoRA on Qwen2.5-0.5B-Instruct in fp32 on CPU, saves a PEFT
adapter dir (adapter_model.safetensors + adapter_config.json).

Deliberately minimal: stdlib json + torch + transformers + peft only.
"""
import argparse
import json
import time

import torch
from torch.utils.data import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, get_linear_schedule_with_warmup
from peft import LoraConfig, get_peft_model


class ChatDS(Dataset):
    def __init__(self, rows, tok, max_seq):
        self.items = []
        for r in rows:
            msgs = r["messages"]
            # prefix = everything but the final assistant reply, with generation prompt
            pre_text = tok.apply_chat_template(msgs[:-1], tokenize=False, add_generation_prompt=True)
            full_text = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=False)
            pre_ids = tok(pre_text, add_special_tokens=False)["input_ids"]
            full = tok(full_text, truncation=True, max_length=max_seq, add_special_tokens=False)
            ids = full["input_ids"]
            attn = full["attention_mask"]
            labels = [-100] * min(len(pre_ids), len(ids)) + ids[min(len(pre_ids), len(ids)):]
            labels = labels[:len(ids)]
            self.items.append({"input_ids": torch.tensor(ids), "attention_mask": torch.tensor(attn),
                               "labels": torch.tensor(labels)})

    def __len__(self):
        return len(self.items)

    def __getitem__(self, i):
        return self.items[i]


def collate(batch):
    n = max(len(b["input_ids"]) for b in batch)
    out = {}
    for k in ("input_ids", "attention_mask", "labels"):
        pad = 0 if k != "labels" else -100
        out[k] = torch.stack([torch.nn.functional.pad(b[k], (0, n - len(b[k])), value=pad) for b in batch])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--epochs", type=int, default=1)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--rank", type=int, default=8)
    ap.add_argument("--batch", type=int, default=4)
    ap.add_argument("--max-seq", type=int, default=2048)
    args = ap.parse_args()

    rows = [json.loads(l) for l in open(args.data) if l.strip()]
    print(f"samples={len(rows)}", flush=True)
    tok = AutoTokenizer.from_pretrained(args.model, trust_remote_code=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    base = AutoModelForCausalLM.from_pretrained(args.model, torch_dtype=torch.float32,
                                               trust_remote_code=True)
    cfg = LoraConfig(r=args.rank, lora_alpha=args.rank * 2, lora_dropout=0.05,
                     target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                                     "gate_proj", "up_proj", "down_proj"],
                     task_type="CAUSAL_LM")
    model = get_peft_model(base, cfg)
    model.print_trainable_parameters()

    ds = ChatDS(rows, tok, args.max_seq)
    steps_per_epoch = (len(ds) + args.batch - 1) // args.batch
    total_steps = steps_per_epoch * args.epochs
    opt = torch.optim.AdamW(model.parameters(), lr=args.lr)
    sched = get_linear_schedule_with_warmup(opt, int(0.05 * total_steps), total_steps)
    model.train()
    t0 = time.time()
    step = 0
    for ep in range(args.epochs):
        order = torch.randperm(len(ds)).tolist()
        for i in range(0, len(ds), args.batch):
            b = collate([ds[j] for j in order[i:i + args.batch]])
            out = model(**b)
            out.loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step()
            sched.step()
            opt.zero_grad()
            step += 1
            el = time.time() - t0
            print(f"ep={ep} step={step}/{total_steps} loss={out.loss.item():.4f} elapsed_s={el:.0f}", flush=True)
    model.save_pretrained(args.out)
    print(f"saved adapter to {args.out} in {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
