# VARIETY — all 11 tasks, gold vs agent, failure class each (2026-11-08)

Sources: gold diffs `case-*.diff` (all 11 PRs pulled) + agent timelines
`_timelines.txt` (from diag-bundle traces) + diag-table.json. 14356 detail in CASE-14356.md.

| task | gold file(s) | agent touched | calls | patch | conf | failure class |
|---|---|---|---|---|---|---|
| 14986 | applications.py setup + docs.py _html_safe_json | openapi/models.py (own validator!) + docs.py html | 14 | 896 | 0.95 | nearby-but-wrong + unrelated-test green |
| 14356 | dependencies/utils.py (7 lines) | params.py x5 edits | 22 | 0 | 0.95 | wrong file + 7 prose searches + empty submit |
| 3468 | console.py render_lines + error path | console.py print() try/except + 99KB write_file spray | 15 | 99543 | 0.95 | right file WRONG function + workspace spray |
| 3777 | console.py TTY detect + docs | progress.py | 11 | 271 | 1.00 | wrong file + WRONG tests green (test_progress) |
| 14360 | dependencies/utils.py alias (2 lines) | SAME file, wrong hunk | 15 | 672 | 0.95 | right file, wrong edit + weak verify |
| 3105 | _export_format.py ONE line | console.py dims; read _cell_widths @line 73000 | 16 | 567 | 1.00 | wrong file + unrelated green + absurd reads |
| 7309 | utils.py _parse_content_type_header | SAME file, subtly wrong | 9 | 687 | 1.00 | right file, wrong edit, targeted test still red |
| 13786 | security/* 401 + override + docs | api_key.py only, 13 churning edits | 23 | 3949 | 0.80 | edit-at-T3, churn, ran SOURCE file as pytest |
| 3180 | _wrap.py divide_line (gold file) | SAME file, wrong hunk | ~9 | 486 | 0.95 | right file, wrong edit, ZERO test runs (find only) |
| 7328 | sessions.py resolve_redirects (3 lines) | SAME file | 11 | 627 | 0.95 | right file; cited fake "PR #6295"; ran FULL suite |
| 3672 | ahttpx/_parsers.py + _pool.py | _server.py + _parsers.py partial | 6 | 1273 | 0.95 | premature submit, ZERO verification, cited spec list |

## Aggregate findings (this is what the summary table hides)

1. LOCALIZATION MOSTLY WORKED: gold file touched in 6/11
   (14360, 7309, 3180, 7328, 3468, 3672-partial). The game is NOT finding the
   file. "Routing is the game" (ARC slogan, BLUEPRINT §14) is WRONG for this lane.
2. REPAIR FAILED 11/11: wrong-hunk edits (14360, 7309, 3180), wrong-function
   (3468), wrong-file (14986, 14356, 3777, 3105), churn (13786), drive-by (3672).
3. VERIFICATION THEATER: 3777 + 3105 + 14986 cited GREEN but IRRELEVANT tests;
   3180 + 3672 ran NO tests; 7328 ran the FULL suite (banned everywhere);
   13786 ran a source file as pytest. Only 7309 ran the right test — and it
   stayed red, submitted anyway.
4. CONFIDENCE CONFABULATION: 0.95-1.00 claimed on ALL 11, including the empty
   submit. The UNC block elicited numbers with ZERO discrimination. Numbers
   without a verification anchor are decoration.
5. MISSING GUARDRAILS (winner has these as hard limits, we didn't): no cap on
   spray (3468's 99KB write_file), no full-suite ban (7328), no must-run-tests
   floor (3180, 3672). Added to ARM1 system.md as HARD BANS.
6. Analyzer sub-agent appeared in 14356/3468/7309 — all failed anyway. Delegated
   search doesn't fix broken repair. Supports single-agent + gates over
   multi-agent structure.
7. Prose `search_similar_code` (7x in 14356) returned nothing every time;
   dotted-symbol queries (7309, 7328, 3672) localized fine. Swap A stands,
   sharpened: symbols-or-grep, never prose.

## Consequence for ARM1 (applied)

- Gate B is the load-bearing wall, not gate A: repro must be issue-shaped
  (exact scenario from the issue text) and the SAME repro must go red->green
  after the edit. Kills wrong-hunk (14360/7309/3180), wrong-file
  (14986/14356/3777/3105), and no-verify submits (3180/3672) in one move.
- HARD BANS added: no bare/full-suite pytest; no whole-module write_file
  rewrites; no submit without running >=1 test command.
- Gate D sharpened: the cited test must be the repro or the issue-shaped test,
  never a passing-but-irrelevant file (3777/3105/14986 pattern).
- PENALTY LEDGER (swap P, negative-reward gate): `skills/penalty/` scores
  observable violations and BLOCKs submit until cleared — no repro artifact,
  no fail-then-pass chain in `/tmp/repro_runs.jsonl`, rerun red, compile
  fail, test/config touch, workspace scratch, spray. Submit only on
  `PENALTY=0 VERDICT=GO`. Punishment lands on the observable artifact, not
  on the model's self-report, so confabulated confidence can't pay.
