"""Fixture validation for the unified dataset v2 (CPU-only, zero GPU).
Checks: JSONL parse, schema behaviors, caps (2500 concise / 8000 full),
mix present, zero-contamination, failing-repro>=75%, multifile>=60,
pytest present in every edit behavior, full-episode multi-turn shape.
Exit 0 PASS, exit 1 FAIL.
"""
import argparse, json, re, sys
from pathlib import Path

BEHAVIORS = {"workspace_true_import", "differential_repro", "clean_tree_retry",
             "post_compaction_submit", "multifile_fanout", "fulllength_episode"}
CAP_CONCISE = 2500
CAP_FULL = 8000
EDIT_BEHAVIORS = {"differential_repro", "clean_tree_retry", "multifile_fanout", "fulllength_episode"}
BANNED_TASKIDS = ["6589", "7328", "7427", "7433", "7205", "13920", "14258", "14479", "14786", "5077", "9425"]
BANNED_PATHS = ["src/requests/", "src/fastapi", "fastapi/_compat", "requests/sessions.py"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", default="dataset/unified-m3-pass2-v2.jsonl")
    a = ap.parse_args()
    p = Path(a.inp)
    if not p.exists():
        print("FAIL: missing %s (run build_unified_dataset_v2.py first)" % p); sys.exit(1)
    rows = [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
    fails = []
    if len(rows) < 400:
        fails.append("count %d < 400 floor" % len(rows))
    seen = {}
    nfail = 0
    for r in rows:
        b = r.get("behavior")
        if b not in BEHAVIORS:
            fails.append("bad behavior %r id=%s" % (b, r.get("id"))); continue
        seen[b] = seen.get(b, 0) + 1
        msgs = r.get("messages", [])
        if not msgs or not all(isinstance(m, list) and len(m) == 2 for m in msgs):
            fails.append("bad message shape id=%s" % r.get("id")); continue
        blob = json.dumps(msgs)
        cap = CAP_FULL if b == "fulllength_episode" else CAP_CONCISE
        if len(blob) > cap:
            fails.append("over cap id=%s chars=%d cap=%d" % (r.get("id"), len(blob), cap))
        low = blob.lower()
        if b in EDIT_BEHAVIORS and "pytest" not in low:
            fails.append("missing pytest in edit behavior id=%s" % r.get("id"))
        if b in ("differential_repro", "clean_tree_retry", "multifile_fanout", "fulllength_episode"):
            if "obs fail" not in low:
                fails.append("missing FAIL-before-edit id=%s" % r.get("id"))
            else:
                nfail += 1
        for t in BANNED_TASKIDS:
            if re.search(r"\b%s\b" % t, blob):
                fails.append("contamination task-id %s in %s" % (t, r.get("id")))
        for bp in BANNED_PATHS:
            if bp in blob:
                fails.append("contamination real-path %s in %s" % (bp, r.get("id")))
    for b in BEHAVIORS:
        if seen.get(b, 0) < 30:
            fails.append("behavior %s thin: %d (<30)" % (b, seen.get(b, 0)))
    if seen.get("multifile_fanout", 0) < 60:
        fails.append("multifile_fanout thin: %d (<60)" % seen.get("multifile_fanout", 0))
    pct = 100.0 * nfail / max(1, len(rows))
    print("samples=%d mix=%s failing-repro=%d (%.1f%%)" % (len(rows), json.dumps(seen, sort_keys=True), nfail, pct))
    if pct < 75.0:
        fails.append("failing-repro %.1f%% < 75%% floor" % pct)
    fl = [r for r in rows if r.get("behavior") == "fulllength_episode"]
    if fl:
        mean_turns = sum(len(r.get("messages", [])) for r in fl) / len(fl)
        print("fulllength: n=%d mean_turns=%.1f" % (len(fl), mean_turns))
        if mean_turns < 5:
            fails.append("fulllength too short: mean_turns=%.1f" % mean_turns)
    if fails:
        print("FAIL %d reasons:" % len(fails))
        for f in fails[:20]:
            print(" - " + f)
        sys.exit(1)
    print("PASS unified dataset v2 fixtures green")

if __name__ == "__main__":
    main()
