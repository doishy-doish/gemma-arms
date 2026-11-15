# CPU brutal filter — doctrine (2026-11-15, user-ordered)

Why: anything that improves a 0.5B CPU agent's score is a standout improvement —
the hardest instrument we have. GPU wins can be sampler/shape luck (FI=2, 62.5%
base-vs-v8 agreement); CPU wins cannot hide.

What runs here (no secrets, no SFT, inference-only):
- cpu-smoke.yml: 0.5B Qwen via llama.cpp, 10 calls / 20-min wall, 1 task.
- Verdict ladder: L0 path works → L1 non-empty patch → L2 no regressions on the
  target test file → L3 hidden test flips. L0+L1 is a mechanics win; L2 is real;
  L3 on 0.5B would be a standout.
- Deliberately excluded: SFT/training (spiky on CPU), 28-call envelopes, graph
  tools (0/32 usage — D7), E2B weights (unresolved provenance).

Cost: runner minutes only (public repo = free), ~30-50 min/run. Wall the smoke
at one task until L1 is routine; only then expand the task list.
