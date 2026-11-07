# FIRE ORDER — H2 + H3 hybrid arms (operator runs on Kaggle; no fire from here)

H1 (ARM1) fires FIRST — it is the only arm the logs fully prove. H2/H3 fire
after, each on the REMAINING 10 (or a 14986+3468 CAL pair first — cheaper).
Same E4B model, same 15/25/80 diagnostic envelope. Each arm needs its own
explicit `fire h2` / `fire h3` reply. Nothing below runs without it.

## Fire H2 (thoughts-off)

- F0: notebook cells 2 (wheelhouse) as usual. Do NOT run old cell 4 build.
- FA: paste+run `armh2/FIRE-cellA-build.py` (copies sample_submission, E4B swap).
- F1..F6: paste file contents into write cells (copy from workspace):
  - F1: `armh2/prompts/system.md` -> `(AGENT_DIR/'prompts'/'system.md').write_text(r'''...''')`
  - F2: `armh2/skills/verify/SKILL.md` -> `(AGENT_DIR/'skills'/'verify'/'SKILL.md').write_text(r'''...''')`
  - F3: `armh2/skills/verify/compile_check.py` -> `(AGENT_DIR/'skills'/'verify'/'compile_check.py').write_text(r'''...''')`
  - F4: `armh2/skills/repro/SKILL.md` -> `(AGENT_DIR/'skills'/'repro'/'SKILL.md').write_text(r'''...''')`
  - F5: `armh2/skills/penalty/SKILL.md` -> `(AGENT_DIR/'skills'/'penalty'/'SKILL.md').write_text(r'''...''')`
  - F6: `armh2/skills/penalty/penalty_ledger.py` -> `(AGENT_DIR/'skills'/'penalty'/'penalty_ledger.py').write_text(r'''...''')`
  (mkdir parents first; all six verified free of triple-single-quotes.)
- FC: paste+run `armh2/FIRE-cellC-transform.py` (agent.yaml replace w/ backup,
  sampling pins incl. include_thoughts=false, eval_config, manifest,
  self-checks incl. THOUGHTS-OFF ANCHOR). If the include_thoughts WARNING
  prints, the sample yaml lacks the key: results are H1-equivalent, do NOT
  read them as thoughts-off. If CHECK FAILED: restore `agent.yaml.orig`,
  paste the printed report back, stop.
- FD: starter validate cell on `armh2_submission`. Must pass.
- FE: rerun notebook cells 6 (vLLM), 8 (Evaluator) with `RUN_TAG='armh2'`,
  `AGENT_DIR=WORKING_DIR/'armh2_submission'`, same task filter, then 10, 12.
- Paste back: FC report, per-task resolved/patch_chars/tool_calls, CONFIDENCE lines.

## Fire H3 (lazy playbooks)

- F0: notebook cells 2 (wheelhouse) as usual. Do NOT run old cell 4 build.
- FA: paste+run `armh3/FIRE-cellA-build.py`.
- F1..F7: paste file contents into write cells (copy from workspace):
  - F1: `armh3/prompts/system.md` -> `(AGENT_DIR/'prompts'/'system.md').write_text(r'''...''')`
  - F2-F6: same five skill files as H2 but from `armh3/skills/...`
  - F7: `armh3/skills/playbooks/SKILL.md` + the three
    `armh3/skills/playbooks/resources/{fastapi,rich,http}.md`
    (four write cells, or one cell with four writes).
  (mkdir parents first; all verified free of triple-single-quotes.)
- FC: paste+run `armh3/FIRE-cellC-transform.py` (asserts lazy router present,
  playbooks NOT inline, all four playbook files exist). If CHECK FAILED:
  restore `agent.yaml.orig`, paste the printed report back, stop.
- PRE-FLIGHT (before FE): confirm whether skill-toolset calls
  (`load_skill`, `load_skill_resource`, `run_skill_script`) count against
  max_tool_calls — check the harness budget doc / one probe task. If they
  count, H3 pays 2 calls per task for ~5KB of ctx; note it in the readout
  and judge accordingly.
- FD/FE: as H2 but `RUN_TAG='armh3'`, `AGENT_DIR=WORKING_DIR/'armh3_submission'`.
- Paste back: FC report, per-task resolved/patch_chars/tool_calls, CONFIDENCE lines.

## Reading the three arms

- H1 vs ARM0 on REMAINING_10: pass bar +2 solves, more non-empty submits.
- H2 vs H1: isolates thoughts-off. Wins only if long-trajectory tasks
  (14356/13786 shapes) flip without new failure modes.
- H3 vs H1: isolates lazy playbooks. Wins only if equal-or-better with a
  smaller prompt — a ctx-efficiency win, not a repair win.
- If H1 fails its bar, H2/H3 still fire (cheap CAL pairs first): a failed
  H1 with a passing H2/H3 localizes the active ingredient by subtraction.
