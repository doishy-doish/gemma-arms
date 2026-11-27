# F2P PROBE (M654/M655): model-free. test-only apply -> pytest (expect FAIL), then +gold -> pytest (expect PASS).
# pid=fastapi_13920 base=0dd42b746e17 v5 (+NL test+gold norm. No model calls. Ends: TEST-RESULT lines in log.
import os, subprocess, urllib.request, base64, sys
import sys as _sys
if _sys.version_info[0] < 3:
    import os as _os; _os.execvp("python3", ["python3"] + _sys.argv)
assert _sys.version_info >= (3, 10), "need python3.10+, got " + _sys.version
print("PY-VERSION " + sys.version.replace(chr(10)," "), flush=True)
def sh(cmd, timeout=300):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")
PID = "fastapi_13920"
REPO = "fastapi/fastapi"
BASE = "0dd42b746e17"
PYTEST = "tests/test_dependency_pep695.py"
KEXPR = "test_pep695_type_dependencies"
SRCFILE = "fastapi/dependencies/utils.py"
IMPORTPKG = "fastapi"
PIPPKGS = "fastapi pytest pytest-timeout requests python-multipart annotated-doc starlette==0.37.2 httpx==0.27.2"
TESTDIFF = base64.b64decode("LS0tIGEvdGVzdHMvdGVzdF9kZXBlbmRlbmN5X3BlcDY5NS5weQorKysgYi90ZXN0cy90ZXN0X2RlcGVuZGVuY3lfcGVwNjk1LnB5CkBAIC0wLDAgKzEsMjcgQEAKK2Zyb20gdHlwaW5nIGltcG9ydCBBbm5vdGF0ZWQKKworZnJvbSBmYXN0YXBpIGltcG9ydCBEZXBlbmRzLCBGYXN0QVBJCitmcm9tIGZhc3RhcGkudGVzdGNsaWVudCBpbXBvcnQgVGVzdENsaWVudAorZnJvbSB0eXBpbmdfZXh0ZW5zaW9ucyBpbXBvcnQgVHlwZUFsaWFzVHlwZQorCisKK2FzeW5jIGRlZiBzb21lX3ZhbHVlKCkgLT4gaW50OgorICAgIHJldHVybiAxMjMKKworCitEZXBlbmRlZFZhbHVlID0gVHlwZUFsaWFzVHlwZSgKKyAgICAiRGVwZW5kZWRWYWx1ZSIsIEFubm90YXRlZFtpbnQsIERlcGVuZHMoc29tZV92YWx1ZSldLCB0eXBlX3BhcmFtcz0oKQorKQorCisKK2RlZiB0ZXN0X3BlcDY5NV90eXBlX2RlcGVuZGVuY2llcygpOgorICAgIGFwcCA9IEZhc3RBUEkoKQorCisgICAgQGFwcC5nZXQoIi8iKQorICAgIGFzeW5jIGRlZiBnZXRfd2l0aF9kZXAodmFsdWU6IERlcGVuZGVkVmFsdWUpIC0+IHN0cjogICMgbm9xYQorICAgICAgICByZXR1cm4gZiJ2YWx1ZToge3ZhbHVlfSIKKworICAgIGNsaWVudCA9IFRlc3RDbGllbnQoYXBwKQorICAgIHJlc3BvbnNlID0gY2xpZW50LmdldCgiLyIpCisgICAgYXNzZXJ0IHJlc3BvbnNlLnN0YXR1c19jb2RlID09IDIwMAorICAgIGFzc2VydCByZXNwb25zZS50ZXh0ID09ICcidmFsdWU6IDEyMyIn")
FIXDIFF = base64.b64decode("LS0tIGEvZmFzdGFwaS9kZXBlbmRlbmNpZXMvdXRpbHMucHkKKysrIGIvZmFzdGFwaS9kZXBlbmRlbmNpZXMvdXRpbHMucHkKQEAgLTY2LDYgKzY2LDcgQEAKIGZyb20gc3RhcmxldHRlLnJlc3BvbnNlcyBpbXBvcnQgUmVzcG9uc2UKIGZyb20gc3RhcmxldHRlLndlYnNvY2tldHMgaW1wb3J0IFdlYlNvY2tldAogZnJvbSB0eXBpbmdfZXh0ZW5zaW9ucyBpbXBvcnQgTGl0ZXJhbCwgZ2V0X2FyZ3MsIGdldF9vcmlnaW4KK2Zyb20gdHlwaW5nX2luc3BlY3Rpb24udHlwaW5nX29iamVjdHMgaW1wb3J0IGlzX3R5cGVhbGlhc3R5cGUKIAogbXVsdGlwYXJ0X25vdF9pbnN0YWxsZWRfZXJyb3IgPSAoCiAgICAgJ0Zvcm0gZGF0YSByZXF1aXJlcyAicHl0aG9uLW11bHRpcGFydCIgdG8gYmUgaW5zdGFsbGVkLiBcbicKQEAgLTM3MCw2ICszNzEsOSBAQCBkZWYgYW5hbHl6ZV9wYXJhbSgKICAgICBkZXBlbmRzID0gTm9uZQogICAgIHR5cGVfYW5ub3RhdGlvbjogQW55ID0gQW55CiAgICAgdXNlX2Fubm90YXRpb246IEFueSA9IEFueQorICAgIGlmIGlzX3R5cGVhbGlhc3R5cGUoYW5ub3RhdGlvbik6CisgICAgICAgICMgdW5wYWNrIGluIGNhc2UgUEVQIDY5NSB0eXBlIHN5bnRheCBpcyB1c2VkCisgICAgICAgIGFubm90YXRpb24gPSBhbm5vdGF0aW9uLl9fdmFsdWVfXwogICAgIGlmIGFubm90YXRpb24gaXMgbm90IGluc3BlY3QuU2lnbmF0dXJlLmVtcHR5OgogICAgICAgICB1c2VfYW5ub3RhdGlvbiA9IGFubm90YXRpb24KICAgICAgICAgdHlwZV9hbm5vdGF0aW9uID0gYW5ub3RhdGlvbg==")
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
sbrc, sbout = sh("grep -aE \"passed|failed|error\" " + work + "/basefail_out.txt | tail -4; echo BASE_RC=" + str(brc), timeout=30)
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
