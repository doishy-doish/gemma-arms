#!/usr/bin/env python3
"""VERIFY-19 runner v2 (repo-relative, CPU). Verbose diagnostics."""
import json, subprocess, os, sys, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
def sh(cmd, **kw):
    try: return subprocess.run(cmd, capture_output=True, text=True, **kw)
    except subprocess.TimeoutExpired as e: return subprocess.CompletedProcess(cmd, 124, str(e.stdout or "")[-1000:], "TIMEOUT")
URLS = {"fastapi/fastapi":"https://github.com/fastapi/fastapi","psf/requests":"https://github.com/psf/requests","Textualize/rich":"https://github.com/Textualize/rich"}
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--row",required=True); ap.add_argument("--patch-set",default="agent")
    ap.add_argument("--workdir",default="/tmp/verify19"); a = ap.parse_args()
    bundle = {r["id"]:r for r in json.load(open(os.path.join(HERE,"patches-19.json")))}
    m = bundle[a.row]
    patch = m["agent_patch"] if a.patch_set=="agent" else m["gold_patch"]
    test_patch = m["test_patch"]; repo = m["repo"]; base = m["base_commit"]
    wd = os.path.join(a.workdir, a.row+"-"+a.patch_set); os.makedirs(wd, exist_ok=True)
    rdir = os.path.join(wd,"repo")
    rec = {"id":a.row,"patch_set":a.patch_set,"y":m["y"],"patch_chars":len(patch or ""),"test_chars":len(test_patch or "")}
    if not os.path.exists(rdir): rec["clone"] = sh(["git","clone","--quiet",URLS.get(repo,repo),rdir], timeout=300).returncode
    rec["fetch"] = sh(["git","fetch","--quiet","origin",base], cwd=rdir, timeout=300).returncode
    co = sh(["git","checkout","--quiet","-f",base], cwd=rdir, timeout=120); rec["checkout"] = co.returncode; rec["checkout_err"] = (co.stderr or "")[-300:]
    rec["head"] = sh(["git","rev-parse","--short","HEAD"], cwd=rdir, timeout=30).stdout.strip()
    rec["inside"] = sh(["git","rev-parse","--is-inside-work-tree"], cwd=rdir, timeout=30).stdout.strip()
    sh(["git","clean","-fdq"], cwd=rdir, timeout=120)
    for nm, content in (("cand.patch",patch or ""),("test.patch",test_patch or "")):
        p = os.path.join(wd,nm)
        if content and not content.endswith("\n"): content += "\n"
        open(p,"w",newline="").write(content)
        raw = open(p,"rb").read()
        rec[nm+"_bytes"] = len(raw); rec[nm+"_crlf"] = raw.count(b"\r\n"); rec[nm+"_head3"] = "\n".join(content.split("\n")[:3])[:300]
    pa = sh(["git","apply","--check","-v",os.path.join(wd,"cand.patch")], cwd=rdir, timeout=60)
    pt = sh(["git","apply","--check","-v",os.path.join(wd,"test.patch")], cwd=rdir, timeout=60)
    st = sh(["git","apply","--stat",os.path.join(wd,"test.patch")], cwd=rdir, timeout=60)
    rec.update({"cand_apply_check":pa.returncode,"cand_out":((pa.stdout or "")+(pa.stderr or ""))[-800:],
                "test_apply_check":pt.returncode,"test_out":((pt.stdout or "")+(pt.stderr or ""))[-800:],
                "test_stat":((st.stdout or "")+(st.stderr or ""))[-400:]})
    if pa.returncode==0: sh(["git","apply",os.path.join(wd,"cand.patch")], cwd=rdir, timeout=60)
    if pt.returncode==0: sh(["git","apply",os.path.join(wd,"test.patch")], cwd=rdir, timeout=60)
    inst = sh(["pip","install","-q","-e",rdir], timeout=600); rec["install_rc"] = inst.returncode
    dep = sh(["pip","install","-q","httpx","pytest-asyncio","anyio","trio"], timeout=600); rec["deps_rc"] = dep.returncode
    import re
    names = sorted(set(re.findall(r"def (test_\w+)", test_patch or "")))[:12]
    sel = " or ".join(names) if names else ""
    cmd = ["python","-m","pytest","-q","-x","--continue-on-collection-errors","-W","ignore::pytest.PytestDeprecationWarning","-k",sel] if sel else ["python","-m","pytest","-q","-x","--continue-on-collection-errors","-W","ignore::pytest.PytestDeprecationWarning"]
    pr = sh(cmd, cwd=rdir, timeout=900)
    full = pr.stdout+pr.stderr
    rec.update({"pytest_rc":pr.returncode,"test_names":names,"failed_lines":[l[:200] for l in full.split("\n") if l.startswith("FAILED") or l.startswith("ERROR")][:20],"tail":full[-2000:]})
    open(os.path.join(wd,"result.json"),"w").write(json.dumps(rec,indent=2))
    print(json.dumps(rec,indent=2))
if __name__=="__main__": main()
