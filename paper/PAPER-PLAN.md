# PAPER PLAN — tick every box without risking the score (2026-11-08)

The bar is public (poncioponcho's artifact): pre-reg, controlled ablations,
decision lines, exact stats, frozen once-blind runs, asserting reproduction
notebook, freeze manifests, honesty notes, open code. Negative results
publish as findings.

| Box | Status | Where |
|---|---|---|
| Novel claim | DONE — discipline-as-model + punishment-as-loss; H1/H2/H3 bundle | HYBRID-ARMS.md |
| Pre-registration | DONE, frozen pre-fire | paper/PRE-REG.md |
| Decision lines | DONE (H1 pass bar, CAL keep rule, readout rule) | paper/PRE-REG.md |
| Stats frozen | DONE, math cross-checked (JS: w(0,10)=(0,.2775), m(7,0)=(.0078,.0156)) | paper/stats.py |
| Controlled ablations | READY — 3 arm trees validated, fire orders written | arm1/, armh2/, armh3/, FIRE-ORDER-*.md |
| Run-once discipline | RULED — each arm fires once on MAIN; re-run = new arm | PRE-REG.md, FIRE-ORDER-H23.md |
| Freeze manifests | AUTO — cellC writes *_MANIFEST.json with SHA-16 per file | FIRE-cellC files |
| Per-task CSVs | PENDING FIRE — paste back Evaluator output into paper/data/ | (at fire time) |
| Reproduction notebook | PENDING — skeleton after first fire; must assert every number | paper/ (at fire time) |
| Honesty notes | DONE — 14356 quarantine, no fresh held-out, upper-bound rule | paper/PRE-REG.md |
| Open code | OUR files are ours; attach Apache-2.0 LICENSE at packaging | (at packaging) |
| Main-track score | PENDING FIRE — H1 first, then CAL pairs, then H2/H3 | FIRE-ORDER-*.md |

Score/box tension, resolved: CAL pairs cost 2 tasks each and also serve the
paper (component isolation); MAIN fires once per arm (no score-chasing
re-runs, which would void the paper); H2/H3 full runs only if their CAL
pairs justify it. The paper never spends score budget, and the score run
never breaks pre-reg.

## CPU screening lane (engineering only — counts for NOTHING)
- `armc/` (E2B registry model, thinking 1024, system.md identical to H1) +
  draft workflow `ci/cpu-screen.yml` + `ci/models-cpu.yaml`
  (both DRAFT-UNVERIFIED).
- Purpose: mechanics checks only — do gates fire, does the ledger run, any
  crashes — at zero GPU quota. E2B is weaker and thinking is cut, so CPU
  outcomes never enter paper tables and never gate Kaggle fires alone.
- OPEN before use: (1) harness install source for Actions, (2) task-data
  source (public dataset URL or KAGGLE_KEY secret ferry).
- Smoke default: one model (E2B), one task (14986 — CAL member, gold known).
- CPU→GPU PROMOTION RULE (one-way, mechanics only). Promote to the GPU
  arm: crash fixes, skill-script bugs, instructions that caused tool-call
  errors, missing guardrails. NEVER promote: anything tuned to E2B's
  specific failures, thinking/output length changes, model-specific
  wording — the weak model doesn't get a vote on the strong model's
  prompt. CPU logs stay in CI artifacts, never in paper tables.
