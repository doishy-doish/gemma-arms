# F2P PROBE (M654/M655): model-free. test-only apply -> pytest (expect FAIL), then +gold -> pytest (expect PASS).
# pid=fastapi_5077 base=930b27e5fa32 v3. No model calls. Ends: TEST-RESULT lines in log.
import os, subprocess, urllib.request, base64, sys
import sys as _sys
if _sys.version_info[0] < 3:
    import os as _os; _os.execvp("python3", ["python3"] + _sys.argv)
assert _sys.version_info >= (3, 10), "need python3.10+, got " + _sys.version
print("PY-VERSION " + sys.version.replace(chr(10)," "), flush=True)
def sh(cmd, timeout=300):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")
PID = "fastapi_5077"
REPO = "fastapi/fastapi"
BASE = "930b27e5fa32"
PYTEST = "tests/test_wrapped_method_forward_reference.py"
KEXPR = "test_wrapped_method_type_inference"
SRCFILE = "fastapi/dependencies/utils.py"
IMPORTPKG = "fastapi"
PIPPKGS = "fastapi pytest pytest-timeout requests python-multipart annotated-doc starlette==0.37.2 httpx==0.27.2"
TESTDIFF = base64.b64decode("LS0tIGEvdGVzdHMvZm9yd2FyZF9yZWZlcmVuY2VfdHlwZS5weQorKysgYi90ZXN0cy9mb3J3YXJkX3JlZmVyZW5jZV90eXBlLnB5CkBAIC0wLDAgKzEsOSBAQAorZnJvbSBweWRhbnRpYyBpbXBvcnQgQmFzZU1vZGVsCisKKworZGVmIGZvcndhcmRyZWZfbWV0aG9kKGlucHV0OiAiRm9yd2FyZFJlZk1vZGVsIikgLT4gIkZvcndhcmRSZWZNb2RlbCI6CisgICAgcmV0dXJuIEZvcndhcmRSZWZNb2RlbCh4PWlucHV0LnggKyAxKQorCisKK2NsYXNzIEZvcndhcmRSZWZNb2RlbChCYXNlTW9kZWwpOgorICAgIHg6IGludCA9IDAKLS0tIGEvdGVzdHMvdGVzdF93cmFwcGVkX21ldGhvZF9mb3J3YXJkX3JlZmVyZW5jZS5weQorKysgYi90ZXN0cy90ZXN0X3dyYXBwZWRfbWV0aG9kX2ZvcndhcmRfcmVmZXJlbmNlLnB5CkBAIC0wLDAgKzEsMzEgQEAKK2ltcG9ydCBmdW5jdG9vbHMKKworZnJvbSBmYXN0YXBpIGltcG9ydCBGYXN0QVBJCitmcm9tIGZhc3RhcGkudGVzdGNsaWVudCBpbXBvcnQgVGVzdENsaWVudAorCitmcm9tIC5mb3J3YXJkX3JlZmVyZW5jZV90eXBlIGltcG9ydCBmb3J3YXJkcmVmX21ldGhvZAorCisKK2RlZiBwYXNzdGhyb3VnaChmKToKKyAgICBAZnVuY3Rvb2xzLndyYXBzKGYpCisgICAgZGVmIG1ldGhvZCgqYXJncywgKiprd2FyZ3MpOgorICAgICAgICByZXR1cm4gZigqYXJncywgKiprd2FyZ3MpCisKKyAgICByZXR1cm4gbWV0aG9kCisKKworZGVmIHRlc3Rfd3JhcHBlZF9tZXRob2RfdHlwZV9pbmZlcmVuY2UoKToKKyAgICAiIiIKKyAgICBSZWdyZXNzaW9uIHRlc3QgZW5zdXJpbmcgdGhhdCB3aGVuIGEgbWV0aG9kIGltcG9ydGVkIGZyb20gYW5vdGhlciBtb2R1bGUKKyAgICBpcyBkZWNvcmF0ZWQgd2l0aCBzb21ldGhpbmcgdGhhdCBzZXRzIHRoZSBfX3dyYXBwZWRfXyBhdHRyaWJ1dGUgKGZ1bmN0b29scy53cmFwcyksCisgICAgdGhlbiB0aGUgdHlwZXMgYXJlIHN0aWxsIHByb2Nlc3NlZCBjb3JyZWN0bHksIGluY2x1ZGluZyBkZXJlZmVyZW5jaW5nIG9mIGZvcndhcmQKKyAgICByZWZlcmVuY2VzLgorICAgICIiIgorICAgIGFwcCA9IEZhc3RBUEkoKQorICAgIGNsaWVudCA9IFRlc3RDbGllbnQoYXBwKQorICAgIGFwcC5wb3N0KCIvZW5kcG9pbnQiKShwYXNzdGhyb3VnaChmb3J3YXJkcmVmX21ldGhvZCkpCisgICAgYXBwLnBvc3QoIi9lbmRwb2ludDIiKShwYXNzdGhyb3VnaChwYXNzdGhyb3VnaChmb3J3YXJkcmVmX21ldGhvZCkpKQorICAgIHdpdGggY2xpZW50OgorICAgICAgICByZXNwb25zZSA9IGNsaWVudC5wb3N0KCIvZW5kcG9pbnQiLCBqc29uPXsiaW5wdXQiOiB7IngiOiAwfX0pCisgICAgICAgIHJlc3BvbnNlMiA9IGNsaWVudC5wb3N0KCIvZW5kcG9pbnQyIiwganNvbj17ImlucHV0IjogeyJ4IjogMH19KQorICAgIGFzc2VydCByZXNwb25zZS5qc29uKCkgPT0gcmVzcG9uc2UyLmpzb24oKSA9PSB7IngiOiAxfQ==")
FIXDIFF = base64.b64decode("LS0tIGEvZmFzdGFwaS9kZXBlbmRlbmNpZXMvdXRpbHMucHkKKysrIGIvZmFzdGFwaS9kZXBlbmRlbmNpZXMvdXRpbHMucHkKQEAgLTE5Miw3ICsxOTIsOCBAQCBkZWYgZ2V0X2ZsYXRfcGFyYW1zKGRlcGVuZGFudDogRGVwZW5kYW50KSAtPiBMaXN0W01vZGVsRmllbGRdOgogCiBkZWYgZ2V0X3R5cGVkX3NpZ25hdHVyZShjYWxsOiBDYWxsYWJsZVsuLi4sIEFueV0pIC0+IGluc3BlY3QuU2lnbmF0dXJlOgogICAgIHNpZ25hdHVyZSA9IGluc3BlY3Quc2lnbmF0dXJlKGNhbGwpCi0gICAgZ2xvYmFsbnMgPSBnZXRhdHRyKGNhbGwsICJfX2dsb2JhbHNfXyIsIHt9KQorICAgIHVud3JhcHBlZCA9IGluc3BlY3QudW53cmFwKGNhbGwpCisgICAgZ2xvYmFsbnMgPSBnZXRhdHRyKHVud3JhcHBlZCwgIl9fZ2xvYmFsc19fIiwge30pCiAgICAgdHlwZWRfcGFyYW1zID0gWwogICAgICAgICBpbnNwZWN0LlBhcmFtZXRlcigKICAgICAgICAgICAgIG5hbWU9cGFyYW0ubmFtZSwKQEAgLTIxNywxMiArMjE4LDEzIEBAIGRlZiBnZXRfdHlwZWRfYW5ub3RhdGlvbihhbm5vdGF0aW9uOiBBbnksIGdsb2JhbG5zOiBEaWN0W3N0ciwgQW55XSkgLT4gQW55OgogCiBkZWYgZ2V0X3R5cGVkX3JldHVybl9hbm5vdGF0aW9uKGNhbGw6IENhbGxhYmxlWy4uLiwgQW55XSkgLT4gQW55OgogICAgIHNpZ25hdHVyZSA9IGluc3BlY3Quc2lnbmF0dXJlKGNhbGwpCisgICAgdW53cmFwcGVkID0gaW5zcGVjdC51bndyYXAoY2FsbCkKICAgICBhbm5vdGF0aW9uID0gc2lnbmF0dXJlLnJldHVybl9hbm5vdGF0aW9uCiAKICAgICBpZiBhbm5vdGF0aW9uIGlzIGluc3BlY3QuU2lnbmF0dXJlLmVtcHR5OgogICAgICAgICByZXR1cm4gTm9uZQogCi0gICAgZ2xvYmFsbnMgPSBnZXRhdHRyKGNhbGwsICJfX2dsb2JhbHNfXyIsIHt9KQorICAgIGdsb2JhbG5zID0gZ2V0YXR0cih1bndyYXBwZWQsICJfX2dsb2JhbHNfXyIsIHt9KQogICAgIHJldHVybiBnZXRfdHlwZWRfYW5ub3RhdGlvbihhbm5vdGF0aW9uLCBnbG9iYWxucykKIAog")
print("TYPES " + str(type(TESTDIFF)) + " " + str(type(FIXDIFF)) + " lens " + str(len(TESTDIFF)) + "/" + str(len(FIXDIFF)), flush=True)
if isinstance(TESTDIFF, str): TESTDIFF = TESTDIFF.encode("latin-1")
if isinstance(FIXDIFF, str): FIXDIFF = FIXDIFF.encode("latin-1")
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
