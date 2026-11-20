# D2 gate — HARD-7 decimal, Tier 2 adoption bar (non-negotiable)

Run AFTER Saturday train, BEFORE any 58-task slot. Same kernel shape as DS-11 evals.

## Set: HARD-7 = 2 canaries + 5 hard targets
- Canaries (floor): 14786 (hold-check) + 9425 (cliff-check, 26->28 alarm).
- Hard: 7427 + 13920 + 7328 + 6589 + 14479 (convert queue order).
- Scored DECIMAL (post-hoc rubric H0.70/O0.15/G0.10/B0.05 from banked pulls),
  never binary-only; canary rule: canary-F + 0 converts = VOID re-fire, not kill.

## Pass bar (banked D2, decimal)
- RETAINED: canaries 1.00 AND graded mean >= 0.25 (floor trio 5077/9425/14786
  sticky wins must survive the adapter; any floor loss = serving regression, reject).
- CONVERTED: >=2 converts across the 5 hard AND mechanism compliance first:
  workspace-true __file__ on call <=5, HEAD-FAIL repro observed, clean-tree
  checkout on failed attempt 1, targeted pytest after every edit; score second.
- SERVING TRAPS (E-MISS): max |delta logit| > 0 (no all-zero lora_B no-op),
  no KV-cache hang on vLLM --lora-modules load, adapter dir < 3 GiB unpacked,
  single base model preserved.
- REPEAT (Path B Test 3): 1 confirmation repeat on HARD-7/k9; gain must survive
  repeat (draw-noise guard, not a full grid).

## Test budget (no more than 4 GPU tests to optimum)
- Test 1 (10 min): Gap-4 throughput (stock vs +adapter). Tax >15-20% -> STOP,
  lock lean stock Tier 1 (Path A, 1 test total).
- Test 2 (2-3h): train unified_r16 (dataset v2 + 50/50 real full-length) + D2 HARD-7.
- Test 3 (1h, only if Test 2 converts with no canary drop): confirmation repeat.
- Test 4 (1 slot): live submit vs 2,967B stock anchor.

## Verdicts
- PASS: Tier 2 (LEAN slashed prompt + unified_r16) becomes the 58-task submission.
- FAIL/NULL: Tier 2 dead. Fall back to Tier 1 (delete the `adapter:` line, ship stock
  3-4.5KB + 6-min cap) and take clean draws. Do not re-tune prompts to chase the adapter.
