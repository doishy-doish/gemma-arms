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
# pid=rich_3944 (M739: 14430-replacement shortlist, base 36fe3f7ca9be). No model calls. Ends: TEST-RESULT lines in log.
import os, subprocess, urllib.request, base64, sys
import sys as _sys
if _sys.version_info[0] < 3:
    import os as _os; _os.execvp("python3", ["python3"] + _sys.argv)
assert _sys.version_info >= (3, 10), "need python3.10+, got " + _sys.version
print("PY-VERSION " + sys.version.replace(chr(10)," "), flush=True)
def sh(cmd, timeout=300):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")
PID = "rich_3944"
REPO = "Textualize/rich"
BASE = "36fe3f7ca9becca4777861d5e6e625f5a4a37545"
PYTEST = "tests/test_cells.py"
KEXPR = "test_nerd_font"
SRCFILE = "rich/cells.py"
IMPORTPKG = "rich"
PIPPKGS = "fastapi pytest pytest-timeout requests python-multipart annotated-doc starlette==0.37.2 httpx==0.27.2 inline-snapshot sqlalchemy orjson ujson dirty_equals"
TESTDIFF = base64.b64decode("LS0tIGEvdGVzdHMvdGVzdF9jZWxscy5weQorKysgYi90ZXN0cy90ZXN0X2NlbGxzLnB5CkBAIC0xODEsMyArMTgxLDkgQEAgZGVmIHRlc3Rfc3BsaXRfZ3JhcGhlbWVzKAogICAgIGFzc2VydCBjZWxsX2xlbih0ZXh0KSA9PSBleHBlY3RlZF9jZWxsX2xlbmd0aAogICAgIGFzc2VydCBzcGFucyA9PSBleHBlY3RlZF9zcGFucwogICAgIGFzc2VydCBjZWxsX2xlbmd0aCA9PSBleHBlY3RlZF9jZWxsX2xlbmd0aAorCisKK2RlZiB0ZXN0X25lcmRfZm9udCgpOgorICAgICIiIlJlZ3Jlc3Npb24gdGVzdCBmb3IgaHR0cHM6Ly9naXRodWIuY29tL1RleHR1YWxpemUvcmljaC9pc3N1ZXMvMzk0MyIiIgorICAgICMgTm90IGFsbG9jYXRlZCBieSB1bmljb2RlLCBidXQgdXNlZCBieSBuZXJkIGZvbnRzCisgICAgYXNzZXJ0IGNlbGxfbGVuKCJcVTAwMGYwMjRkIikgPT0gMQ==")
FIXDIFF = base64.b64decode("LS0tIGEvcmljaC9jZWxscy5weQorKysgYi9yaWNoL2NlbGxzLnB5CkBAIC01Nyw3ICs1Nyw3IEBAIGRlZiBnZXRfY2hhcmFjdGVyX2NlbGxfc2l6ZShjaGFyYWN0ZXI6IHN0ciwgdW5pY29kZV92ZXJzaW9uOiBzdHIgPSAiYXV0byIpIC0+IGluCiAgICAgY29kZXBvaW50ID0gb3JkKGNoYXJhY3RlcikKICAgICB0YWJsZSA9IGxvYWRfY2VsbF90YWJsZSh1bmljb2RlX3ZlcnNpb24pLndpZHRocwogICAgIGlmIGNvZGVwb2ludCA+IHRhYmxlWy0xXVsxXToKLSAgICAgICAgcmV0dXJuIDAKKyAgICAgICAgcmV0dXJuIDEKICAgICBsb3dlcl9ib3VuZCA9IDAKICAgICB1cHBlcl9ib3VuZCA9IGxlbih0YWJsZSkgLSAxCiAgICAgaW5kZXggPSAobG93ZXJfYm91bmQgKyB1cHBlcl9ib3VuZCkgLy8gMg==")
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
