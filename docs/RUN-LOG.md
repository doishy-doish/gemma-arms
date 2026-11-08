# RUN LOG — GPU quota: ~10 tests/week → 1 shot/day discipline

## H1 (ARM1, REMAINING_10) — FIRED 2026-11-08 ~late (operator ran on Kaggle)
- Envelope: E4B, 15/25/80, RUN_TAG='armh1... 'arm1-swap'. Pre-reg frozen pre-fire (paper/PRE-REG.md).
- Quota math: 1 full 10-task run ≈ 2.5–3.5h ≈ 1 day. CAL pair ≈ 30–45 min ≈ half a day.
- Awaiting paste-back: FC report, per-task resolved/patch_chars/tool_calls, CONFIDENCE lines.
- Results: 0/10, ARM1 FAILED (see H1 v6 READOUT below).

## Queue (superseded 2026-11-08 - kept for the record)
1. H1 readout → score + paper CSVs.
2. H2 CAL pair (14986+3468, ~35 min).
3. H3 CAL pair (~35 min).
4. Full H2/H3 only if pairs justify.

## H1 v6 READOUT (2026-11-08) - 0/10, ARM1 FAILED
- Kernel andralemisquitta/gemma-arm1-h1-fire-v6-brace-free-fix, lastRunTime 09:38:10Z.
- Per-task (resolved/patch/exit/calls): 14986 F/1714/1/25; 3468 F/1062/1/22; 3777 F/546/1/16; 14360 F/7351/2/21; 3105 F/102075/1/25; 7309 F/687/1/25; 13786 F/2142/2/16; 3180 F/7013/1/15; 7328 F/31730/1/24; 3672 F/1041/2/12. RESOLVED 0/10.
- Autopsy: graph mandate obeyed (first tool block 9/10); edit fail rate still ~30%; penalty-ledger verdict in 0/10 traces (scripts written but never engaged); CONF 0.90-0.99 everywhere, all wrong. Same failure modes as ARM0: spray submits 3105 (102KB) + 7328 (31KB), wrong package path 3672, wrong API 13786. Mechanism obeyed, outcome unchanged - points at model + verification-theater.
- Decision line (>=+2 AND more non-empty): FAILED. Per-protocol fallback: ARM2 (winner-shape, E4B) then ARM3 (same prompt, 31B). H2/H3 move behind ARM2/ARM3.
- Packaging note: diag harness logs came back 0-byte; fire orders now carry a PKG-SIDECAR step (trace-derived transcripts, fail loud on missing traces).

## Queue (revised 2026-11-08)
1. ARM2 fire -> readout (needs fire arm2).
2. ARM3 fire -> readout (needs fire arm3).
3. H2/H3 CAL pairs only if ARM2/ARM3 leave budget/questions open.
