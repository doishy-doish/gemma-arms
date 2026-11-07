# penalty skill — negative-reward gate (swap P)

Punishment, not advice. Run `penalty_ledger.py` via `run_skill_script`
BEFORE `submit_patch`. It reruns your repro against current code,
byte-compiles touched files, and scans the diff for spray, workspace
scratch, and test/config edits. Submit ONLY on `PENALTY=0 VERDICT=GO`.
Any BLOCK item must be fixed and the ledger rerun. No evidence, no submit.

## What it deducts (all BLOCK until cleared)
- No `/tmp/repro_*.py` artifact: -50.
- No fail-then-pass chain for one repro in `/tmp/repro_runs.jsonl`: -50
  (red->green unproven — return to Phase 1, do not edit blind).
- Ledger's own rerun of the repro fails now: -50.
- Changed `.py` file fails byte-compile: -25 per file.
- Test/config file touched (`tests/`, `test_*`, conftest, pytest.ini,
  packaging): -20 each (stripped at scoring anyway — pure loss).
- Scratch left under `/workspace` (untracked, non-excluded): -10 until
  cleaned (it would ship inside your patch via `git add -N`).
- Spray: diff over 6 files, 2000 changed lines, or 60000 bytes: -50
  (a 99KB spray scored 0 — size without proof is punished, not rewarded).

## Logging runs (required, costs no extra calls)
Run the repro through this wrapper so every run is evidence:
`python3 /tmp/repro_<taskid>.py > /tmp/repro_<taskid>.log 2>&1; code=$?; tail -5 /tmp/repro_<taskid>.log; echo "{\"file\": \"repro_<taskid>.py\", \"exit\": $code}" >> /tmp/repro_runs.jsonl; exit $code`
Pre-edit the exit must be nonzero; post-edit zero. The ledger checks the
chain order in `repro_runs.jsonl`: at least one fail BEFORE the final pass
for the same file.
If BLOCK code is repro-red-after-edit and calls used <18, your next 2
calls are the micro-sample budget: ONE alternative hunk for the same site,
repro referees.
