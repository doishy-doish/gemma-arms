# FIRE ORDER — ARM2 winner-shape + ARM3 31B (operator runs on Kaggle; no fire from here)

ARM1 (H1 v6) closed 0/10: decision line failed (RUN-LOG). Per the
WINNER-COMPARE fallback: ARM2 = winner-shape replication on E4B (prompt
variable isolated). ARM3 = the same prompt on the 31B base (model variable
isolated). Order: ARM2 first, ARM3 after its readout. Each needs its own
explicit `fire arm2` / `fire arm3` reply. MAIN set = REMAINING_10 (same 10
tasks; 14356 stays dev-only, never fires).

## Fire ARM2

- F0: notebook wheelhouse cell as usual. Do NOT run old cell 4 build.
- FA: paste+run `arm2/FIRE-cellA-build.py` (copies sample_submission, E4B
  swap + adapter strip, removes skills/).
- F1: `arm2/prompts/system.md` -> `(AGENT_DIR/'prompts'/'system.md').write_text(r'''...''')`
  (mkdir parents first; file verified free of triple-single-quotes and of
  every curly brace — ADK renders braces as session-state placeholders).
- FC: paste+run `arm2/FIRE-cellC-transform.py` (needles: HARD LIMITS, CALL
  PLAN, by call 12, CONFIDENCE, spray ban, SPEC step; skills/ must NOT
  exist; 9-tool registry assert; brace scan; real validate_directory gate;
  manifest ARM2_MANIFEST, run_tag arm2-winner). If CHECK FAILED: restore
  `WORKING_DIR/agent.yaml.pre-fc.bak`, paste the printed report back, stop.
- FD: starter validate cell on `arm2_submission`. Must pass.
- FE: rerun notebook cells 6 (vLLM), 8 (Evaluator) with
  `RUN_TAG='arm2-winner'`, `AGENT_DIR=WORKING_DIR/'arm2_submission'`,
  task filter REMAINING_10, then packaging cell.
- PKG-SIDECAR (fix 5): after packaging, paste+run the snippet below. It
  derives per-task step summaries from traces (independent of the harness
  Phase-1 log transcripts, which came back 0 bytes in diag-e4b) and fails
  loud if traces are missing.
- Paste back: FC report, per-task resolved/patch_chars/tool_calls,
  CONFIDENCE lines, sidecar report.

## Fire ARM3 (after ARM2 readout; needs `fire arm3`)

Same as ARM2 with `arm3/` files, `RUN_TAG='arm3-31b'`,
`AGENT_DIR=WORKING_DIR/'arm3_submission'`. Stock 31B adapters ship (cellA
asserts exactly one declared model + adapters present). If vLLM OOMs on
the L4, record it as the finding — do not improvise quantization changes
mid-fire.

## PKG-SIDECAR snippet (paste + run after the packaging cell)

```python
import json, re
from pathlib import Path
OUT = Path('/kaggle/working/arm2-fire')  # arm3-fire for the ARM3 run
tr = sorted((OUT / 'results' / 'traces').glob('trace_*.json'))
assert len(tr) == 10, 'trace count %d != 10' % len(tr)
lines = []
for p in tr:
    j = json.loads(p.read_text(encoding='utf-8'))
    seq, edits, conf, subs = [], {'ok': 0, 'fail': 0}, None, []
    for s in j.get('steps', []):
        for t in s.get('tool_calls', []) or []:
            seq.append(t.get('function_name'))
            if t.get('function_name') in ('edit_file', 'write_file'):
                if 'FileEditError' in json.dumps(s.get('observation') or ''):
                    edits['fail'] += 1
                else:
                    edits['ok'] += 1
            if t.get('function_name') == 'submit_patch':
                subs.append(json.dumps(s.get('observation'))[:120])
        m = re.search(r'CONFIDENCE.*', s.get('message') or '')
        if m:
            conf = m.group(0)[:200]
    lines.append('%s steps=%d edits=%s submits=%s conf=%s'
                 % (p.stem, len(j.get('steps', [])), edits, subs, conf))
(OUT / 'OUR-TRANSCRIPTS.txt').write_text('\n'.join(lines), encoding='utf-8')
logs = sorted((OUT / 'results' / 'logs').glob('*.log'))
empty = [p.name for p in logs if p.stat().st_size == 0]
print('traces=%d sidecar=OUR-TRANSCRIPTS.txt empty_harness_logs=%s'
      % (len(tr), empty))
```

## Reading the two arms

- ARM2 vs ARM0 (0/10, non-empty): pass bar >= +2 solves AND zero empty
  submits. Prompt isolation: does the winner schedule fix what gates
  could not?
- ARM3 vs ARM2 (paired, same 10): pass bar >= +2 over ARM2. Model
  isolation: is E4B the ceiling?
- If ARM2 wins and ARM3 does not: ship the prompt, model stays E4B. If
  ARM3 wins: the model is the lever; cost the 31B envelope next.
- H2/H3 (thoughts-off, lazy playbooks) stay pre-registered but move
  behind ARM2/ARM3; fire only after the ARM2 readout.
