#!/usr/bin/env python3
"""GOLDSHAPE runner: base-vs-gold-vs-agent on gold-shape reproducers (CPU, no GPU).

Row = one DS-11 task. Patch set = none (base) | agent (banked P0 final) | gold.
Repro file is copied into the repo as an untracked helper and pytest runs ONLY
it - no test_patch application, no official harness. Validates the reproducer
(base FAIL + gold PASS) before the agent row counts as measurement.
"""
import json, subprocess, os, sys, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
def sh(cmd, **kw):
    try: return subprocess.run(cmd, capture_output=True, text=True, **kw)
    except subprocess.TimeoutExpired as e: return subprocess.CompletedProcess(cmd, 124, str(e.stdout or "")[-1000:], "TIMEOUT")
URLS = {"fastapi/fastapi":"https://github.com/fastapi/fastapi","psf/requests":"https://github.com/psf/requests"}
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--row",required=True); ap.add_argument("--patch-set",default="none")
    ap.add_argument("--workdir",default="/tmp/goldshape"); a = ap.parse_args()
    man = json.load(open(os.path.join(HERE,"manifest.json")))
    m = {r["id"]:r for r in man["rows"]}[a.row]
    patch = {"none":"", "agent":m["agent_patch"], "gold":m["gold_patch"]}[a.patch_set]
    repo = m["repo"]; base = m["base_commit"]
    wd = os.path.join(a.workdir, a.row+"-"+a.patch_set); os.makedirs(wd, exist_ok=True)
    rdir = os.path.join(wd,"repo")
    rec = {"id":a.row,"patch_set":a.patch_set,"base":base[:12],"patch_chars":len(patch)}
    if not os.path.exists(rdir): rec["clone"] = sh(["git","clone","--quiet",URLS[repo],rdir], timeout=300).returncode
    rec["fetch"] = sh(["git","fetch","--quiet","origin",base], cwd=rdir, timeout=300).returncode
    co = sh(["git","checkout","--quiet","-f",base], cwd=rdir, timeout=120); rec["checkout"] = co.returncode
    sh(["git","clean","-fdq"], cwd=rdir, timeout=120)
    if patch:
        p = os.path.join(wd,"cand.patch")
        if not patch.endswith("\n"): patch += "\n"
        open(p,"w",newline="").write(patch)
        pa = sh(["git","apply","--check","-v",p], cwd=rdir, timeout=60)
        rec["cand_apply_check"] = pa.returncode
        if pa.returncode == 0: sh(["git","apply",p], cwd=rdir, timeout=60)
    else:
        rec["cand_apply_check"] = -1
    repro_src = os.path.join(HERE,"repro",a.row+".py")
    repro_dst = os.path.join(rdir,"goldshape_repro_%s.py" % a.row)
    open(repro_dst,"w").write(open(repro_src).read())
    inst = sh(["pip","install","-q","-e",rdir], timeout=600); rec["install_rc"] = inst.returncode
    if repo == "fastapi/fastapi":
        dep = sh(["pip","install","-q","typing-inspection","httpx","pytest-asyncio","anyio"], timeout=600)
        rec["deps_rc"] = dep.returncode
    elif a.row == "requests_7328":
        dep = sh(["pip","install","-q","responses"], timeout=600)
        rec["deps_rc"] = dep.returncode
    pr = sh(["python","-m","pytest","-q",os.path.basename(repro_dst)], cwd=rdir, timeout=600)
    full = (pr.stdout or "")+(pr.stderr or "")
    rec.update({"pytest_rc":pr.returncode,
                "passed":("passed" in full and full.split("passed")[0].split("\n")[-1][-60:]),
                "tail":full[-2500:]})
    open(os.path.join(wd,"result.json"),"w").write(json.dumps(rec,indent=2))
    print(json.dumps(rec,indent=2))
if __name__=="__main__": main()
