# HOW THIS VEHICLE IS SUPPOSED TO BE WRITTEN (M724, durable just-in-case note).
# MISTAKES-IN-FILE: dataset-exact bytes + runtime _nl (M693/M695); b64 round-trip verified at build; KEXPR from +def tests; no-rail-code; readback full-match post-push (M626/M655).
# (1) Prompts reuse the proven CONTRACT constant VERBATIM (by reference, never paraphrased).
#     M723: a hand-assembled paraphrase dropped the machine-readable FILE:/SEARCH shape and
#     voided a full 6-slot rail (0/6 measured the prompt bug, not difficulty).
# (2) Any reply-parser change ships with a parse-smoke: golden sample (must score) +
#     adversarial prose (must void) through the SHIPPED parser path before push (M672/M723).
# (3) Dependencies are fleet-wide: a new pip/test package lands in the rail ensure_deps AND
#     every staged F2P PIPPKGS AND every staged rail copy, grep-verified same turn (M722:
#     per-vehicle patching let inline_snapshot/sqlalchemy kill slots after M709/M495 named them).
# (4) Evidence lines print the tool own rc (e.g. echo RC=$? right after the tool, before tail)
#     or a grep summary -- never the tail pipe own rc; asserts check FULL captured text (M666/M721e).
# (5) One variable per fire; pre-reg (predictions + kill rules) BEFORE staging (M632).
# Lineage: M717-M724. This header is comment-only and changes no behavior.
# F2P PROBE (M654/M655): model-free. test-only apply -> pytest (expect FAIL), then +gold -> pytest (expect PASS).
# pid=rich_2943 (M739: 14430-replacement shortlist, base 610fd75c433c). No model calls. Ends: TEST-RESULT lines in log.
import os, subprocess, urllib.request, base64, sys
import sys as _sys
if _sys.version_info[0] < 3:
    import os as _os; _os.execvp("python3", ["python3"] + _sys.argv)
assert _sys.version_info >= (3, 10), "need python3.10+, got " + _sys.version
print("PY-VERSION " + sys.version.replace(chr(10)," "), flush=True)
def sh(cmd, timeout=300):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")
PID = "rich_2943"
REPO = "Textualize/rich"
BASE = "610fd75c433c3dfcd9c296e8b91363979127b9fa"
PYTEST = "tests/test_style.py"
KEXPR = "test_clear_meta_and_links_clears_hash"
SRCFILE = "rich/style.py"
IMPORTPKG = "rich"
PIPPKGS = "fastapi pytest pytest-timeout requests python-multipart annotated-doc starlette==0.37.2 httpx==0.27.2 inline-snapshot sqlalchemy orjson ujson dirty_equals"
TESTDIFF = base64.b64decode("LS0tIGEvdGVzdHMvdGVzdF9zdHlsZS5weQorKysgYi90ZXN0cy90ZXN0X3N0eWxlLnB5CkBAIC0yNTEsMyArMjUxLDE3IEBAIGRlZiB0ZXN0X2NsZWFyX21ldGFfYW5kX2xpbmtzKCk6CiAgICAgYXNzZXJ0IGNsZWFyX3N0eWxlLmJnY29sb3IgPT0gQ29sb3IucGFyc2UoImJsYWNrIikKICAgICBhc3NlcnQgY2xlYXJfc3R5bGUuYm9sZAogICAgIGFzc2VydCBub3QgY2xlYXJfc3R5bGUuaXRhbGljCisKKworZGVmIHRlc3RfY2xlYXJfbWV0YV9hbmRfbGlua3NfY2xlYXJzX2hhc2goKToKKyAgICAiIiJSZWdyZXNzaW9uIHRlc3QgZm9yIGh0dHBzOi8vZ2l0aHViLmNvbS9UZXh0dWFsaXplL3JpY2gvaXNzdWVzLzI5NDIuIiIiCisKKyAgICBzdHlsZSA9IFN0eWxlLnBhcnNlKCJib2xkIHJlZCBvbiBibGFjayBsaW5rIGh0dHBzOi8vZXhhbXBsZS5vcmciKSArIFN0eWxlLm9uKAorICAgICAgICBjbGljaz0iQ0xJQ0siCisgICAgKQorICAgIGhhc2goc3R5bGUpICAjIEZvcmNlIGhhc2ggY2FjaGluZy4KKworICAgIGFzc2VydCBzdHlsZS5faGFzaCBpcyBub3QgTm9uZQorCisgICAgY2xlYXJfc3R5bGUgPSBzdHlsZS5jbGVhcl9tZXRhX2FuZF9saW5rcygpCisgICAgYXNzZXJ0IGNsZWFyX3N0eWxlLl9oYXNoIGlzIE5vbmU=")
FIXDIFF = base64.b64decode("LS0tIGEvcmljaC9zdHlsZS5weQorKysgYi9yaWNoL3N0eWxlLnB5CkBAIC02NjMsNyArNjYzLDcgQEAgZGVmIGNsZWFyX21ldGFfYW5kX2xpbmtzKHNlbGYpIC0+ICJTdHlsZSI6CiAgICAgICAgIHN0eWxlLl9zZXRfYXR0cmlidXRlcyA9IHNlbGYuX3NldF9hdHRyaWJ1dGVzCiAgICAgICAgIHN0eWxlLl9saW5rID0gTm9uZQogICAgICAgICBzdHlsZS5fbGlua19pZCA9ICIiCi0gICAgICAgIHN0eWxlLl9oYXNoID0gc2VsZi5faGFzaAorICAgICAgICBzdHlsZS5faGFzaCA9IE5vbmUKICAgICAgICAgc3R5bGUuX251bGwgPSBGYWxzZQogICAgICAgICBzdHlsZS5fbWV0YSA9IE5vbmUKICAgICAgICAgcmV0dXJuIHN0eWxl")
print("TYPES " + str(type(TESTDIFF)) + " " + str(type(FIXDIFF)) + " lens " + str(len(TESTDIFF)) + "/" + str(len(FIXDIFF)), flush=True)
if isinstance(TESTDIFF, str): TESTDIFF = TESTDIFF.encode("latin-1")
if isinstance(FIXDIFF, str): FIXDIFF = FIXDIFF.encode("latin-1")
if not TESTDIFF.endswith(b"\n"): TESTDIFF = TESTDIFF + b"\n"  # M693: git-2.56.1 NL rule (test patch)
if not FIXDIFF.endswith(b"\n"): FIXDIFF = FIXDIFF + b"\n"  # M695: same wall on gold (content byte-true; container NL only)
work = "/tmp/duck6_" + PID
sh("rm -rf " + work + " && mkdir -p " + work)
print("PIP-INSTALL " + PID, flush=True)
sh("pip install -q " + PIPPKGS + " 2>&1 | tail -1", timeout=600)
url = "https://github.com/" + REPO + "/archive/" + BASE + ".tar.gz"
urllib.request.urlretrieve(url, work + "/src.tgz")
sh("tar xzf " + work + "/src.tgz -C " + work + " --strip-components=1", timeout=120)
pyenv = "PYTHONPATH=" + work
mrc, mout = sh("cd " + work + " && " + pyenv + " python -c \"import " + IMPORTPKG + "; print(" + IMPORTPKG + ".__file__)\" 2>&1 | tail -2", timeout=60)
print("MODFILE check done", flush=True)
print("TEST-RESULT-MODFILE " + PID + " " + mout[-200:], flush=True)
assert (work + "/") in mout, "shadow-fail: " + mout[-200:]
open(work + "/test_patch.diff", "wb").write(TESTDIFF)
assert open(work + "/test_patch.diff","rb").read()==TESTDIFF, "test-write-readback"
trc, tout = sh("cd " + work + " && git apply test_patch.diff 2>&1; echo TEST_APPLIED_RC=$?", timeout=60)
print("TEST-APPLY " + PID + " " + tout[-200:], flush=True)
assert "TEST_APPLIED_RC=0" in tout, "test-apply-fail"
brc, bout = sh("cd " + work + " && " + pyenv + " python -m pytest " + PYTEST + " -k \"" + KEXPR + "\" -q --tb=line -W ignore::PendingDeprecationWarning -W ignore::DeprecationWarning -p no:cacheprovider -p no:unraisableexception > basefail_out.txt 2>&1; echo BASE_RC=$?; tail -8 basefail_out.txt", timeout=600)
print("BASE-FAIL-PROOF " + PID + " " + bout[-600:], flush=True)
sbrc, sbout = sh("grep -aE \"passed|failed|error\" " + work + "/basefail_out.txt | tail -4", timeout=30)
print("BASE-SUMMARY " + PID + " " + sbout[-300:], flush=True)
open(work + "/fix.diff", "wb").write(FIXDIFF)
assert open(work + "/fix.diff","rb").read()==FIXDIFF, "fix-write-readback"
frc, fout = sh("cd " + work + " && git apply fix.diff 2>&1; echo FIX_APPLIED_RC=$?", timeout=60)
print("FIX-APPLY " + PID + " " + fout[-200:], flush=True)
assert "FIX_APPLIED_RC=0" in fout, "fix-apply-fail"
crc, cout = sh("cd " + work + " && python -m py_compile " + SRCFILE + " 2>&1; echo COMPILE_RC=$?", timeout=60)
print("COMPILE " + PID + " " + cout[-200:], flush=True)
trc2, tout2 = sh("cd " + work + " && " + pyenv + " python -m pytest " + PYTEST + " -k \"" + KEXPR + "\" -v --tb=short -W ignore::PendingDeprecationWarning -W ignore::DeprecationWarning -p no:cacheprovider -p no:unraisableexception > pytest_out.txt 2>&1; echo PYTEST_RC=$?; tail -12 pytest_out.txt", timeout=600)
print("TEST-RESULT " + PID + " " + tout2[-800:], flush=True)
assert "PYTEST_RC=0" in tout2, "gold-does-not-pass"
print("PROBE-DONE " + PID, flush=True)
