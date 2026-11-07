# RULES CHECK — submission compliance, verified 2026-11-08 (before any fire)

Checked all three arm trees + fire cells against the harness contract
(HARNESS_README §2/§7) and the official inference notebook pattern
(starter-blob.json). Re-check at fire time via cellC self-checks.

## Pass
- One root config: `agent.yaml` only; `configs/sampling.yaml` +
  `eval_config.yaml` are non-root names. cellC asserts `roots == 1`.
- Tools: all 13 names appear in the harness registry (9 budgeted +
  `load_skill`, `load_skill_resource`, `run_skill_script` per §5.3).
- `.py` in submissions ONLY as skill scripts under `skills/` 
  (`compile_check.py`, `penalty_ledger.py`). FIRE-*.py stay local —
  fire orders paste only the listed files, never the build cells.
- Extensions: only .yaml/.yml/.md/.py(+skill scripts). Manifests write to
  WORKING_DIR, never into the submission tree.
- `!include`: relative, no traversal, depth 1. No symlinks (cellC asserts).
  Sizes: KBs vs 3 GiB cap, instruction ~7KB vs 1M cap.
- eval_config keys: official notebook `.get`s exactly
  `timeout_seconds / verification_timeout_seconds / max_tool_calls /
  max_time_minutes / max_turns` with defaults — unknown keys ignored, and
  ours are all read keys. Budgets inside envelope.
- Single model E4B, no `adapter` key, cellA strips `adapters/`.
  Sampling pins only rewrite keys already present (indent-agnostic, so flat
  or nested both match) and REPORT applied/missing — no invented keys.
- sub_agents: left exactly as the sample ships (mirrors the official
  notebook). Our agent.yaml references none, so they are inert.

## Fixed during this check
- cellC sampling-pin regexes carried doubled backslashes (`\\s`) in all
  three arms — pins would silently never match. Fixed to `\s`; verified 0
  doubles remain and official notebook uses the same single-backslash form.
- Manifests moved out of the submission tree into WORKING_DIR.

## Fire-time gates (already in cellC)
- Roots/symlinks/size check, needle asserts per arm, sampling applied /
  missing report, H2 include_thoughts WARNING, validate_directory cell.

## Standing rule (from the backslash miss, 2026-11-08)
- Presence checks are not validation. Every regex and every piece of logic
  in a fire cell must be SEMANTICALLY simulated before fire (JS-equiv run
  against flat + nested shapes, asserting the rewrite actually lands).
- Silent-by-design fallbacks (like the applied/missing report) are where
  bugs hide: a miss disguised as "key absent in sample" is still a miss.
