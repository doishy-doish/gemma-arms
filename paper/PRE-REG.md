# PRE-REGISTRATION — Gemma-4 arms H1/H2/H3 ( frozen 2026-11-08, before any fire)

## Arms
- ARM0 (recorded, diag-e4b 2026-11-07, 15/25/80): 0/11, all unresolved.
- H1 (ARM1 tree): single E4B agent, gates A-D, penalty ledger, exotics E1-E5.
- H2 (armh2/): H1 + thoughts-off (`include_thoughts: false`).
- H3 (armh3/): H1 + lazy playbooks.

## Task sets
- DEV (contamination quarantine): 14356 only — used for autopsy, never fired.
- CAL pair: 14986 + 3468 (full-budget reruns, isolates single components).
- MAIN set: REMAINING_10 (all except 14356). Each arm fires ONCE on MAIN.
  No re-fires to chase noise; any re-run is a new pre-registered arm.

## Decision lines (all paired, same tasks)
- H1 PASS: resolves ≥ ARM0+2 on MAIN **and** strictly more non-empty submits.
  (ARM0 non-empty: 10/10 excl. 14356? 14356 empty. MAIN excl 14356: ARM0
  non-empty 10/10 but 0 resolved — so the bar is +2 solves AND no empty submits.)
- CAL component KEEP: flipping ≥1 CAL-pair task from fail→pass with no
  pass→fail reversal on the pair.
- H2/H3 READOUT: McNemar exact two-sided p + Wilson 95% CIs reported
  regardless of outcome; negative results publish as-is (non-binding
  constraints are a finding, not a failure).

## Statistics (frozen in `paper/stats.py`)
- Resolution Wilson 95% interval, z=1.96.
- Same-task paired McNemar exact: conditional binomial on discordant pairs
  (b=H1-only solves, c=rival-only solves); standard one-sided + doubled
  two-sided must agree; report both.
- Failure-mode precedence: resolved → context overflow → budget truncation
  → session timeout → patch-failed-tests → abandoned/no-patch.

## Honesty notes (carried into the paper)
- 14356 inspected during development: all MAIN-set numbers are clean, but
  no fresh held-out split exists in this lane — state it, don't hide it.
- Base-commit validity: if any MAIN task passes tests with an empty patch,
  rates are upper bounds (probe: submit empty patch once per task? NO —
  wastes budget; instead report harness baselines if available).
- Every number in the paper must be re-computed by `reproduce_results.ipynb`
  from frozen per-task CSVs, with assertions. No hand-copied numbers.
