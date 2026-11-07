# FIRE ORDER — ARM1 causal test (operator runs on Kaggle; no fire from here)

Goal: baseline prompt (recorded 0/10 excl 14356) vs full swap A+B+C+D on the
REMAINING 10, same E4B model, same 15/25/80 diagnostic envelope.

Budget: 10 tasks x <=15 min + boot ~8 min + harness ≈ 2.5-3h inside one 12h window.
Needs explicit `fire` reply. Nothing below runs without it.

## ARM0 (recorded, no rerun needed — diag-e4b 2026-11-07, same caps)

All unresolved. patch_chars: 14986:896, 14356:(held out, empty), 3468:99543
(unfocused mega-diff), 3777:271, 14360:672, 3105:567, 7309:687, 13786:3949,
3180:486, 7328:627, 3672:1273. Note 3468's 99KB spray: non-empty but scoreless.

## Fire cells (in diag-e4b-v2.ipynb session, Kaggle)

- F0: run notebook cells 2 (wheelhouse) as usual. Do NOT run old cell 4 build.
- FA: paste+run `arm1/FIRE-cellA-build.py` (copies sample_submission, E4B swap).
- F1..F6: paste file contents into write cells (copy from workspace):
  - F1: `arm1/prompts/system.md` -> `(AGENT_DIR/'prompts'/'system.md').write_text(r'''...''')`
  - F2: `arm1/skills/verify/SKILL.md` -> `(AGENT_DIR/'skills'/'verify'/'SKILL.md').write_text(r'''...''')`
  - F3: `arm1/skills/verify/compile_check.py` -> `(AGENT_DIR/'skills'/'verify'/'compile_check.py').write_text(r'''...''')`
  - F4: `arm1/skills/repro/SKILL.md` -> `(AGENT_DIR/'skills'/'repro'/'SKILL.md').write_text(r'''...''')`
  - F5: `arm1/skills/penalty/SKILL.md` -> `(AGENT_DIR/'skills'/'penalty'/'SKILL.md').write_text(r'''...''')`
  - F6: `arm1/skills/penalty/penalty_ledger.py` -> `(AGENT_DIR/'skills'/'penalty'/'penalty_ledger.py').write_text(r'''...''')`
  (mkdir parents first; all six verified free of triple-single-quotes.)
- FC: paste+run `arm1/FIRE-cellC-transform.py` (agent.yaml replace w/ backup
  `agent.yaml.orig`, sampling pins replace-if-present + report, eval_config,
  manifest, self-checks). If CHECK FAILED: restore `agent.yaml.orig`,
  paste the printed report back, stop.
- FD: starter validate cell (validate_directory) on `arm1_submission`. Must pass.
- FE: rerun notebook cells 6 (vLLM start), 8 (Evaluator) with
  `RUN_TAG='arm1-swap'`, `AGENT_DIR=WORKING_DIR/'arm1_submission'`,
  task filter `REMAINING_10` (in FIRE cellA), then 10 (package), 12 (calibration).
- Paste back: FC report, per-task resolved/patch_chars/tool_calls, CONFIDENCE lines.

## Decision rule (CASE-14356 §3)

ARM1 must beat ARM0 by >=2 solves AND raise non-empty submits, else kill the
swap. If signal: CAL ablates A/B/C/D individually on 14986+3468 full-budget
reruns to isolate the active ingredient. Fallback if ARM1 loses: ARM2 =
winner-prompt replication (Flexonafft HARD LIMITS + CALL PLAN + PROCEDURE
shape, our envelope) — fully specified in WINNER-COMPARE.md. Contamination guard: 14356 stays dev-only;
playbooks describe procedure, never fixes. Field tension on record: winners ran
single-agent without graph tools — this test settles it causally instead of by vote.
