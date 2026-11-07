# EXOTIC + HYBRID upgrades (2026-11-08)

Price rule stays: adopt what buys calls/ctx/time inside the envelope, CAL-test
the rest, reject what spends. "Exotic" here means unfamiliar-but-fitting, not
compute-heavy. Nothing below needs a new tool, a new model, or more budget.

## Adopted into ARM1 (cheap, evidence-backed)

- E1 SPEC PROLOGUE (winner step 1, 0 calls): TRIGGER / EXPECTED / ACCEPTANCE
  in thinking before Phase 1. Forces issue-shaped framing; kills
  wrong-function edits at the source. Costs ~3 thinking lines.
- E2 GRAPH LOCATE-ONLY: graph tools allowed in Phase 1 only; after the
  ranked list, traceback + grep. Delegated search appeared in 3 failed
  tasks (14356/3468/7309) and repaired none — the graph seeds, the
  traceback decides.
- E3 NO STACKED EDITS: never re-edit one hunk without a repro run between.
  13786 stacked 13 edits to 0. Second touch on a hunk = stop, rerun, decide.
- E4 QUOTED CONFIDENCE: BECAUSE must quote a tool-returned line (exit code,
  OK/FAIL, PASS count). Paraphrase = confabulation, the 0.95-on-empty pattern.
- E5 LEDGER→MICROSAMPLE POINTER: a BLOCK on repro-red-after-edit spends the
  conditional micro-sample budget there first (max 2 calls, repro referees).

## Novel hybrids (no one has these, to our knowledge)

- H1 THE BUNDLE ITSELF: winner-schedule (edit-by-12, freeze-by-20) +
  issue-shaped red->green gates + negative-reward ledger + conditional
  micro-sample + single E4B agent. Each part exists somewhere; the
  combination — discipline as the model, punishment as the loss — does not.
  ARM1 *is* H1. Fire it before theorizing further.
- H2 THOUGHTS-OFF (variant BUILT, staged for CAL): `include_thoughts: false`
  with thinking_budget 4096 — reasoning stays on, history strips thought,
  ctx spend drops on long trajectories. Variant tree `armh2/` built from
  ARM1 + one-line sampling change + thoughts-off anchor rule (restate repro
  path + ranked files + phase per turn), validated (yaml parses, all gate
  needles present, no triple-quotes). Fire-ready: own cellA/cellC in-tree
  (cellC pins include_thoughts=false, warns if the sample yaml lacks the
  key), full sequence in `FIRE-ORDER-H23.md`. Risk: cross-turn reasoning
  loss.
- H3 PLAYBOOK LAZY-LOAD (variant BUILT, staged behind H1/H2):
  `armh3/` extracts the three playbooks into `skills/playbooks/resources/`,
  system.md keeps every gate and loads one resource via the router.
  Validated (6008B, all needles, playbooks fully extracted). Fire-ready:
  own cellA/cellC in-tree (cellC asserts router present, playbooks NOT
  inline, all four playbook files exist), full sequence in
  `FIRE-ORDER-H23.md` incl. the skill-budget pre-flight check.

## Trace-back: what the DIAG11 logs say about each (parsed `_timelines.txt`)

- H1 gates fire on ALL 11: zero tasks ran an issue-shaped repro (no
  `/tmp/repro` anywhere in 11 trajectories) — gate B alone BLOCKs every
  submit we made. Per-task: 14986/3777/3105 irrelevant-green (gate D +
  ledger), 14360/7309/3180 wrong-hunk or red-stays-red (ledger rerun),
  3468 spray (ledger spray rule), 7328 full-suite (hard ban), 3180/3672
  no-verify (ledger), 13786 13 stacked edits (E3), 14356 9 prose searches
  + 22 calls of reading (symbols-or-grep + tripwires). H1 is proven
  against the logs before it ever fires live.
- H2 relevance is REAL but UNPROVEN: longest trajectories are 14356 (55
  steps), 13786 (51), 3468 (40), 3105 (37) — exactly where thought-history
  eats ctx. But NO task shows a MAX_TOKENS/token-limit nudge, so ctx never
  observably bound. H2 stays a CAL test (14986+3468), not a default.
- H3 saves ~5KB of static prompt (7087B -> ~2100B router) while trajectories
  carry 6-10 read_file outputs at up to 10K chars each — the read-discipline
  upgrade already in H1 attacks the actual hog. H3 fires only if H1 shows
  ctx binding, and only after confirming on Kaggle whether skill-toolset
  calls count against max_tool_calls (harness documents 9 budget-gated
  tools; skill tools' status is unverified).

## Rejected (spends more than it buys, per current evidence)

- Planner/router agents, analyzer delegation beyond Phase 1 (3 appearances,
  0 repairs), budget doubling, LoRA before ROI, temperature schedules,
  multi-sample rerank, fixed seed (key may not exist in the sample yaml —
  do not invent keys).
