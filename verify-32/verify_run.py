#!/usr/bin/env python3
"""VERIFY-19 runner v12 (=v11 + L3-critic + full-file double-run) (cand-only gate: test_patch applies AFTER gate) = v9 + pre-submit invariant gate (AST + allowlist + compile).
Gate runs after cand/test apply, before install. Records gate_* fields and
gate_block (1 = would-block submit). Pytest still runs to measure (data)."""
import json, subprocess, os, sys, argparse, ast
HERE = os.path.dirname(os.path.abspath(__file__))
def sh(cmd, **kw):
    try: return subprocess.run(cmd, capture_output=True, text=True, **kw)
    except subprocess.TimeoutExpired as e: return subprocess.CompletedProcess(cmd, 124, str(e.stdout or "")[-1000:], "TIMEOUT")
URLS = {"fastapi/fastapi":"https://github.com/fastapi/fastapi","psf/requests":"https://github.com/psf/requests","Textualize/rich":"https://github.com/Textualize/rich"}
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--row",required=True); ap.add_argument("--patch-set",default="agent")
    ap.add_argument("--workdir",default="/tmp/verify19"); a = ap.parse_args()
    bundle = {r["id"]:r for r in json.load(open(os.path.join(HERE,"patches-32.json")))}
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
    # GATE: allowlist + AST + compile on worktree diff (cand-side only: diff of cand.patch files)
    gate_block, gate_reasons = 0, []
    ch = [l for l in (sh(["git","diff","--name-only","HEAD","--","."], cwd=rdir, timeout=60).stdout or "").split("\n") if l]
    bad = [f for f in ch if f.startswith("tests/") or f.endswith((".cfg",".toml",".ini"))]
    rec["gate_allow"] = 0 if not bad else 1; rec["gate_changed"] = ch[:20]
    if bad: gate_block = 1; gate_reasons.append("allowlist:"+",".join(bad[:4]))
    pys = [f for f in ch if f.endswith(".py") and not f.startswith("tests/")]
    ast_ok, ast_err = 1, ""
    for f in pys:
        try: ast.parse(open(os.path.join(rdir,f)).read())
        except Exception as e: ast_ok = 0; ast_err = "%s (%s)" % (f, e); break
    rec["gate_ast"] = ast_ok; rec["gate_ast_err"] = ast_err[:200]
    if not ast_ok: gate_block = 1; gate_reasons.append("ast:"+ast_err[:100])
    if pys and ast_ok:
        cr = sh([sys.executable,"-m","py_compile"]+pys, cwd=rdir, timeout=120)
        rec["gate_compile"] = cr.returncode; rec["gate_compile_err"] = (cr.stderr or "")[-200:]
        if cr.returncode != 0: gate_block = 1; gate_reasons.append("compile")
    else: rec["gate_compile"] = -1; rec["gate_compile_err"] = "skipped"
    rec["gate_block"] = gate_block; rec["gate_reasons"] = gate_reasons
    if pt.returncode==0: sh(["git","apply",os.path.join(wd,"test.patch")], cwd=rdir, timeout=60)
    inst = sh(["pip","install","-q","-e",rdir], timeout=600); rec["install_rc"] = inst.returncode
    tr = os.path.join(rdir,"requirements-tests.txt")
    rec["testreq_rc"] = sh(["pip","install","-q","-r",tr], timeout=600).returncode if os.path.exists(tr) else -1
    vs = sh(["pip","show","starlette","fastapi","httpx","pytest","dirty_equals","inline_snapshot"], timeout=120)
    fz = sh(["pip", "freeze"], timeout=120)
    rec["freeze_grep"] = "\n".join([l for l in (fz.stdout or "").split("\n") if any(k in l.lower() for k in ["dirty", "inline", "snapshot", "starlette", "httpx"])])[:800]
    rec["pkg_versions"] = (vs.stdout or "")
    sm = sh(["python", "-c", "import dirty_equals; import inline_snapshot; print('smoke-ok')"], cwd=rdir, timeout=120)
    rec["import_smoke"] = ((sm.stdout or "") + (sm.stderr or ""))[-300:]
    dep = sh(["pip","install","-q","httpx","pytest-asyncio","anyio","trio","typer","pytest-timeout","pytest-httpbin"], timeout=600); rec["deps_rc"] = dep.returncode
    import re
    names = sorted(set(re.findall(r"def (test_\w+)", test_patch or "")))[:12]
    files = sorted(set(re.findall(r"^[+-]{3} [ab]/(\S+\.py)", test_patch or "", re.M)))
    sel = " or ".join(names) if names else ""
    base_cmd = ["python","-m","pytest","-q","-x","--continue-on-collection-errors","-W","ignore::pytest.PytestDeprecationWarning","-W","ignore::DeprecationWarning"]
    cmd = (base_cmd + files + (["-k",sel] if sel else [])) if files else (base_cmd + (["-k",sel] if sel else []))
    pr = sh(cmd, cwd=rdir, timeout=900)
    full = pr.stdout+pr.stderr
    rec.update({"pytest_rc":pr.returncode,"test_names":names,"test_files":files,"failed_lines":[l[:200] for l in full.split("\n") if l.startswith("FAILED") or l.startswith("ERROR")][:20],"tail":full[-4000:]})
    # DOUBLE-RUN (v12): same files WITHOUT -k (full-file view). Cost ~2x pytest, zero new infra.
    if files:
        fr = sh(base_cmd + files, cwd=rdir, timeout=900)
        ffull = fr.stdout+fr.stderr
        import re as _re
        _m = _re.search(r"(\d+) passed", ffull); _f = _re.search(r"(\d+) failed", ffull)
        rec.update({"full_rc":fr.returncode,"full_passed":int(_m.group(1)) if _m else -1,"full_failed":int(_f.group(1)) if _f else 0,
                    "full_failed_lines":[l[:200] for l in ffull.split("\n") if l.startswith("FAILED") or l.startswith("ERROR")][:5],
                    "full_tail":ffull[-1500:]})
    else:
        rec.update({"full_rc":-1,"full_passed":-1,"full_failed":0,"full_failed_lines":[],"full_tail":"skipped"})
    # L3-CRITIC (v12, deterministic/exact): hard-block ONLY empty; rest advisory flags.
    _ch = rec.get("gate_changed", []) or []
    _src = [f for f in _ch if not f.startswith("tests/")]
    _cflags = []
    _h3 = rec.get("cand.patch_head3","") or ""
    if (rec.get("patch_chars",0) or 0)==0: _cblock=1; _cflags=["empty"]
    else:
        _cblock=0
        if len(_src)==0 and len(_ch)>0: _cflags.append("testonly-diff")
        if len(_ch)==0:
            _cflags.append("unapplied-or-invisible" if rec.get("cand_apply_check",0)!=0 else "no-tracked-change")
        if "new file mode" in _h3 or "repro" in _h3: _cflags.append("pollution:new-file-or-repro")
        if len(_src)>3: _cflags.append("spray:%d-src-files" % len(_src))
    rec["critic_block"]=_cblock; rec["critic_flags"]=_cflags
    open(os.path.join(wd,"result.json"),"w").write(json.dumps(rec,indent=2))
    print(json.dumps(rec,indent=2))
if __name__=="__main__": main()
