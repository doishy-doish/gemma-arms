"""Build the unified M3+pass@2 turn-mode SFT dataset v2 (CPU-only, zero GPU).

Fixes the three flaws the Gap-3 audit caught in v1 (450 syn, mean 471ch):
  1. 0% multi-file fan-out -> ADD multifile_fanout rows (grep symbol from File 1,
     read File 2, edit BOTH sites, targeted pytest, submit). Field: 25/28 S3 share
     an identifier (89.3% reachable); cliff is at edit-all-sites (C1 6/11).
  2. 0 post-edit pytest -> EVERY edit behavior now ends with a targeted
     `pytest <single-file> -k ...` (timeout 100). Killer: 10/11 edited-gold fails
     had no_post_edit_pytest.
  3. 28.9% failing-repro-before-Edit-1 -> 75%+ : repro + retry + multifile + full
     all contain OBS FAIL on HEAD before Edit 1 (380/450 = 84.4% in default mix).
  4. 471ch mean -> premature-submission collapse risk: ADD fulllength rows
     (10-12 turns, CAP_FULL 8000) mixing import->repro->grep->read x2->edit x2->
     pytest->repro PASS->delete->diff->submit, so the LoRA sees full episodes,
     not just single-behavior snippets.

Competition Rule 2.4: NO competition data. Synthetic repos only (synpkg_*),
no task text, no snapshots, no gold patches, no tests. Shapes distilled from
banked trajectories (6589/7328 import trap, 7427/13920 thrash, C1 incomplete-
hunk, 14786/5077/9425 winner hygiene), re-voiced with fake symbols.

Usage (CPU now):
  python3 dataset/build_unified_dataset_v2.py --out dataset/unified-m3-pass2-v2.jsonl --n 450
Then:
  python3 dataset/fixture_validate_v2.py --in dataset/unified-m3-pass2-v2.jsonl
"""
import argparse, hashlib, json, random
from pathlib import Path

BEHAVIORS = ["workspace_true_import", "differential_repro", "clean_tree_retry",
             "post_compaction_submit", "multifile_fanout", "fulllength_episode"]
DEFAULT_MIX = {"workspace_true_import": 40, "differential_repro": 150,
               "clean_tree_retry": 80, "post_compaction_submit": 30,
               "multifile_fanout": 90, "fulllength_episode": 60}
CAP_CONCISE = 2500
CAP_FULL = 8000

PKGS = ["synpkg_alpha", "synpkg_beta", "synpkg_gamma", "synpkg_delta"]
MODS = ["utils", "sessions", "shared", "core", "helpers"]

def _turn(user, assistant):
    return [[user, assistant]]

def _mk_import(i, rng):
    pkg = rng.choice(PKGS); mod = rng.choice(MODS)
    user = "call 1: confirm workspace-true imports for %s.%s" % (pkg, mod)
    assistant = (
        "run_command: python3 -c \"import %s.%s; print(%s.%s.__file__)\"\n" % (pkg, mod, pkg, mod)
        + "OBS file=/workspace/src/%s/%s.py -> workspace-true, proceed.\n" % (pkg, mod)
        + "If OBS had shown dist-packages or site-packages, prefix every python command "
        + "with PYTHONPATH=src for src-layout repos or PYTHONPATH=. otherwise, then re-verify. "
        + "Never trust a repro until the import path is workspace-true. sample %d" % i)
    return {"id": "wt-%d" % i, "behavior": "workspace_true_import",
            "messages": _turn(user, assistant), "meta": {"source": "banked-6589-7328-shape"}}

def _mk_repro(i, rng):
    pkg = rng.choice(PKGS); mod = rng.choice(MODS)
    user = "write differential repro for issue behavior in %s.%s" % (pkg, mod)
    assistant = (
        "write_file repro.py: import from real repo path %s.%s, exact issue names, no alias.\n" % (pkg, mod)
        + "run_command: python3 repro.py -> OBS FAIL on unmodified HEAD as the issue describes.\n"
        + "edit_file %s/%s.py: one surgical hunk serving the ACCEPTANCE line.\n" % (pkg, mod)
        + "run_command: timeout 100 python3 -m pytest tests/test_%s.py -k issue -q -> OBS PASS (targeted only, never bare pytest).\n" % mod
        + "run_command: python3 repro.py -> OBS PASS after the fix. Suite green not required; "
        + "trust issue-shaped differential only. Delete repro.py immediately after it passes. sample %d" % i)
    return {"id": "dr-%d" % i, "behavior": "differential_repro",
            "messages": _turn(user, assistant), "meta": {"source": "banked-7328-7427-shape"}}

def _mk_retry(i, rng):
    pkg = rng.choice(PKGS); mod = rng.choice(MODS)
    user = "post-edit repro still red in %s.%s, attempt 1 landed" % (pkg, mod)
    assistant = (
        "run_command: git checkout -- . # clean-tree reset, drop the failed attempt-1 spray\n"
        + "run_command: python3 repro.py -> OBS FAIL on clean HEAD, confirmed.\n"
        + "edit_file %s/%s.py: one fresh hunk, no stacking on the dirty tree.\n" % (pkg, mod)
        + "run_command: timeout 100 python3 -m pytest tests/test_%s.py -k issue -q -> OBS PASS.\n" % mod
        + "run_command: python3 repro.py -> OBS PASS. One failed attempt plus one clean retry "
        + "is two independent passes inside 28 calls. sample %d" % i)
    return {"id": "ct-%d" % i, "behavior": "clean_tree_retry",
            "messages": _turn(user, assistant), "meta": {"source": "arm-A-7427-13920-shape"}}

def _mk_submit(i, rng):
    pkg = rng.choice(PKGS); mod = rng.choice(MODS)
    user = "issue-shaped repro green after compaction, calls remaining"
    assistant = (
        "STATE recovery: re-state TRIGGER/EXPECTED/ACCEPTANCE in one line from surviving diff.\n"
        + "run_command: python3 -m py_compile %s/%s.py -> OBS OK.\n" % (pkg, mod)
        + "run_command: git diff --stat -> only intended source files differ; scratch already deleted.\n"
        + "submit_patch now. Post-green editing is over; a green tree submitted beats a polished tree broken. sample %d" % i)
    return {"id": "ps-%d" % i, "behavior": "post_compaction_submit",
            "messages": _turn(user, assistant), "meta": {"source": "banked-winner-hygiene"}}

def _mk_multifile(i, rng):
    pkg = rng.choice(PKGS); m1 = rng.choice(MODS); m2 = rng.choice([m for m in MODS if m != m1])
    sym = "SYM_%d" % (1000 + (i * 37) % 9000)
    user = "issue spans two sites in %s (%s + %s), File 1 known" % (pkg, m1, m2)
    assistant = (
        "run_command: grep -rn %s %s/ -> OBS %s/%s.py + %s/%s.py share the symbol (M1 coupling).\n" % (sym, pkg, pkg, m1, pkg, m2)
        + "read_file %s/%s.py +-40 lines around %s; read_file %s/%s.py +-40 lines around %s.\n" % (pkg, m1, sym, pkg, m2, sym)
        + "write_file repro.py: FAIL on HEAD covering BOTH sites.\n"
        + "run_command: python3 repro.py -> OBS FAIL on unmodified HEAD.\n"
        + "edit_file %s/%s.py: hunk 1 serving ACCEPTANCE; edit_file %s/%s.py: hunk 2 (companion site, same symbol).\n" % (pkg, m1, pkg, m2)
        + "run_command: timeout 100 python3 -m pytest tests/test_%s.py -k issue -q -> OBS PASS.\n" % m1
        + "run_command: python3 repro.py -> OBS PASS on both sites. Delete repro.py. sample %d" % i)
    return {"id": "mf-%d" % i, "behavior": "multifile_fanout",
            "messages": _turn(user, assistant), "meta": {"source": "banked-C1-coupling-25of28"}}

def _mk_full(i, rng):
    pkg = rng.choice(PKGS); m1 = rng.choice(MODS); m2 = rng.choice([m for m in MODS if m != m1])
    sym = "SYM_%d" % (2000 + (i * 53) % 8000)
    user = "full episode: import check through submit in %s (%s + %s)" % (pkg, m1, m2)
    t = []
    t.append(["call 1: workspace-true check",
              "run_command: python3 -c \"import %s.%s; print(%s.%s.__file__)\" -> OBS /workspace/src/%s/%s.py, proceed." % (pkg, m1, pkg, m1, pkg, m1)])
    t.append(["call 2-3: differential repro",
              "write_file repro.py (exact issue names, no alias).\nrun_command: python3 repro.py -> OBS FAIL on HEAD."])
    t.append(["call 4-5: fan-out",
              "run_command: grep -rn %s %s/ -> %s + %s share symbol.\nread_file %s/%s.py +-40; read_file %s/%s.py +-40." % (sym, pkg, m1, m2, pkg, m1, pkg, m2)])
    t.append(["call 6-8: edit both + targeted pytest",
              "edit_file %s/%s.py: hunk 1.\nedit_file %s/%s.py: hunk 2 (companion).\nrun_command: timeout 100 python3 -m pytest tests/test_%s.py -k issue -q -> OBS PASS." % (pkg, m1, pkg, m2, m1)])
    t.append(["call 9-10: repro PASS + hygiene",
              "run_command: python3 repro.py -> OBS PASS.\nrun_command: rm repro.py; git diff --stat -> only %s/%s.py + %s/%s.py differ." % (pkg, m1, pkg, m2)])
    t.append(["call 11: submit",
              "submit_patch now. sample %d (full episode, no post-green edits)." % i])
    return {"id": "fl-%d" % i, "behavior": "fulllength_episode",
            "messages": t, "meta": {"source": "banked-winner-full-episode"}}

MAKERS = {"workspace_true_import": _mk_import, "differential_repro": _mk_repro,
          "clean_tree_retry": _mk_retry, "post_compaction_submit": _mk_submit,
          "multifile_fanout": _mk_multifile, "fulllength_episode": _mk_full}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="dataset/unified-m3-pass2-v2.jsonl")
    ap.add_argument("--n", type=int, default=450)
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()
    rng = random.Random(a.seed)
    total = a.n
    mix = dict(DEFAULT_MIX)
    scale = total / float(sum(mix.values()))
    counts = {k: max(1, int(round(v * scale))) for k, v in mix.items()}
    while sum(counts.values()) > total:
        k = max(counts, key=counts.get); counts[k] -= 1
    rows = []
    for beh, c in counts.items():
        for i in range(c):
            r = MAKERS[beh](i, rng)
            blob = json.dumps(r["messages"])
            cap = CAP_FULL if beh == "fulllength_episode" else CAP_CONCISE
            assert len(blob) <= cap, "%s over cap %d>%d" % (r["id"], len(blob), cap)
            r["meta"].update({"chars": len(blob), "cap_ok": True,
                              "cap": cap, "has_fail_before_edit": beh in (
                                  "differential_repro", "clean_tree_retry",
                                  "multifile_fanout", "fulllength_episode")})
            rows.append(r)
    rng.shuffle(rows)
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    h = hashlib.sha256(out.read_bytes()).hexdigest()[:16]
    print("wrote %d samples -> %s sha=%s" % (len(rows), out, h))
    print("mix=" + json.dumps({b: sum(1 for r in rows if r["behavior"] == b) for b in BEHAVIORS}))
    nfail = sum(1 for r in rows if r["meta"]["has_fail_before_edit"])
    print("failing-repro-before-Edit1=%d/%d=%.1f%%" % (nfail, len(rows), 100.0 * nfail / len(rows)))

if __name__ == "__main__":
    main()
