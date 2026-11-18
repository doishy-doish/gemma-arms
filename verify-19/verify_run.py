#!/usr/bin/env python3
"""VERIFY-19 runner (repo-relative, CPU). Reads patches-19.json next to itself."""
import json, subprocess, os, sys, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
def sh(cmd, **kw):
    try: return subprocess.run(cmd, capture_output=True, text=True, **kw)
    except subprocess.TimeoutExpired as e: return subprocess.CompletedProcess(cmd, 124, str(e.stdout or "")[-1000:], "TIMEOUT")
URLS = {"fastapi/fastapi":"https://github.com/fastapi/fastapi","psf/requests":"https://github.com/psf/requests","Textualize/rich":"https://github.com/Textualize/rich","encode/httpx":"https://github.com/encode/httpx"}
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--row",required=True); ap.add_argument("--patch-set",default="agent")
    ap.add_argument("--workdir",default="/tmp/verify19"); a = ap.parse_args()
    bundle = {r["id"]:r for r in json.load(open(os.path.join(HERE,"patches-19.json")))}
    m = bundle[a.row]; patch = m["agent_patch"] if a.patch_set=="agent" else m["gold_patch"]
    # test patch + base from bundle
    test_patch = m["test_patch"]; repo = m["repo"]; base = m["base_commit"]
    wd = os.path.join(a.workdir, a.row+"-"+a.patch_set); os.makedirs(wd, exist_ok=True)
    rdir = os.path.join(wd,"repo")
    if not os.path.exists(rdir): sh(["git","clone","--quiet",URLS.get(repo,repo),rdir], timeout=300)
    sh(["git","fetch","--quiet","origin",base], cwd=rdir, timeout=300)
    sh(["git","checkout","--quiet","-f",base], cwd=rdir, timeout=120)
    sh(["git","clean","-fdq"], cwd=rdir, timeout=120)
    open(os.path.join(wd,"cand.patch"),"w").write(patch or "")
    open(os.path.join(wd,"test.patch"),"w").write(test_patch or "")
    pa = sh(["git","apply","--check",os.path.join(wd,"cand.patch")], cwd=rdir, timeout=60)
    pt = sh(["git","apply","--check",os.path.join(wd,"test.patch")], cwd=rdir, timeout=60)
    rec = {"id":a.row,"patch_set":a.patch_set,"y":m["y"],"patch_chars":len(patch or ""),
           "cand_apply_check":pa.returncode,"test_apply_check":pt.returncode}
    if pa.returncode==0: sh(["git","apply",os.path.join(wd,"cand.patch")], cwd=rdir, timeout=60)
    if pt.returncode==0: sh(["git","apply",os.path.join(wd,"test.patch")], cwd=rdir, timeout=60)
    inst = sh(["pip","install","-q","-e",rdir], timeout=600)
    rec["install_rc"] = inst.returncode
    # test names: scrape def test_ from test patch
    import re
    names = sorted(set(re.findall(r"def (test_\w+)", test_patch or "")))[:12]
    sel = " or ".join(names) if names else ""
    cmd = ["python","-m","pytest","-q","-x","-k",sel] if sel else ["python","-m","pytest","-q","-x"]
    pr = sh(cmd, cwd=rdir, timeout=900)
    rec.update({"pytest_rc":pr.returncode,"test_names":names,"tail":(pr.stdout+pr.stderr)[-2000:]})
    open(os.path.join(wd,"result.json"),"w").write(json.dumps(rec,indent=2))
    print(json.dumps(rec,indent=2))
if __name__=="__main__": main()
