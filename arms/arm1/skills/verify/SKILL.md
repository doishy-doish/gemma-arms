# verify skill — pre-submit gate (swap D)

Run BEFORE `submit_patch`, after targeted pytest:

1. `run_skill_script` on `compile_check.py` with the workspace root. It byte-
   compiles every changed `.py` file (tracked modifications + untracked,
   tests excluded from FAIL but reported) and prints OK/FAIL per file.
2. If any source file FAILs, fix it and re-run. Never submit with a FAIL.
3. This catches syntax/indentation breakage from `edit_file` merges. It does
   NOT catch logic errors — targeted pytest is still mandatory (Phase 4.2).

Usage (Phase 4.1): call `run_skill_script` with script `compile_check.py`.
No arguments needed; it discovers changed files via git itself.
