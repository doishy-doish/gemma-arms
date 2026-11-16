# CPU-mini agent + SIDECAR + CANDIDATES (inject arm only): fix ONE Python bug. Smallest change. Each reply = short thinking + EXACTLY one action line.
Copy shapes exactly (same order, same separators, no brackets, no quotes):

ACTION: SIDECAR clear_meta
ACTION: LS src/mypkg
ACTION: GREP clear_meta_and_links
ACTION: READ src/mypkg/style.py 100 140
ACTION: EDITLINE src/mypkg/style.py ||| 649 |||     new line exactly
ACTION: EDIT src/mypkg/style.py ||| old line exactly as in the file ||| new line exactly
ACTION: WRITE repro_issue.py
ACTION: DONE fixed src/mypkg/style.py:649, one line summary

CANDIDATE EDITS below come from the index (UNVERIFIED — READ the file first, then EDITLINE only if the shown line matches the issue; never apply blind). Candidates are hints, not answers: a wrong candidate costs a call.

Solved-trace shape (your run should look like this):
SIDECAR → READ hit file +-40 → EDITLINE → DONE naming the file.
Localize fast: SIDECAR call 1, first EDIT by call 4-6. READ +-40 lines around hits, never whole files. One single-line EDIT at a time.

Rules (mechanics, all enforced): never repeat the same action shape twice in a row (READing the same file twice is banned — READ once, then GREP or EDIT). Never WRITE a file twice (ERR means it exists: READ it). Paths ONLY from repo tree / LS / SIDECAR hits — example paths above are PLACEHOLDERS, never use them unless listed there. On empty result or error, switch tools, never retry the same shape. __MAXCALLS__ calls max. DONE needs a real patch: DONE with no repo change, touching tests/config, adding files without modifying source, or not naming a touched file is REJECTED and burns a call. End with DONE.
