# DIAG PROBE fastapi_13920 (M692): parse/transience/NL test. No model calls.
import os, subprocess, urllib.request, base64, sys
if sys.version_info[0] < 3:
    import os as _os; _os.execvp("python3", ["python3"] + sys.argv)
assert sys.version_info >= (3, 10), "need python3.10+"
print("PY-VERSION " + sys.version.replace(chr(10)," "), flush=True)
def sh(cmd, timeout=300):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")
PID = "fastapi_13920"
REPO = "fastapi/fastapi"
BASE = "0dd42b746e17"
PYTEST = "tests/test_dependency_pep695.py"
KEXPR = "test_pep695_type_dependencies"
PIPPKGS = "fastapi pytest pytest-timeout requests python-multipart annotated-doc starlette==0.37.2 httpx==0.27.2"
TESTDIFF = base64.b64decode("LS0tIGEvdGVzdHMvdGVzdF9kZXBlbmRlbmN5X3BlcDY5NS5weQorKysgYi90ZXN0cy90ZXN0X2RlcGVuZGVuY3lfcGVwNjk1LnB5CkBAIC0wLDAgKzEsMjcgQEAKK2Zyb20gdHlwaW5nIGltcG9ydCBBbm5vdGF0ZWQKKworZnJvbSBmYXN0YXBpIGltcG9ydCBEZXBlbmRzLCBGYXN0QVBJCitmcm9tIGZhc3RhcGkudGVzdGNsaWVudCBpbXBvcnQgVGVzdENsaWVudAorZnJvbSB0eXBpbmdfZXh0ZW5zaW9ucyBpbXBvcnQgVHlwZUFsaWFzVHlwZQorCisKK2FzeW5jIGRlZiBzb21lX3ZhbHVlKCkgLT4gaW50OgorICAgIHJldHVybiAxMjMKKworCitEZXBlbmRlZFZhbHVlID0gVHlwZUFsaWFzVHlwZSgKKyAgICAiRGVwZW5kZWRWYWx1ZSIsIEFubm90YXRlZFtpbnQsIERlcGVuZHMoc29tZV92YWx1ZSldLCB0eXBlX3BhcmFtcz0oKQorKQorCisKK2RlZiB0ZXN0X3BlcDY5NV90eXBlX2RlcGVuZGVuY2llcygpOgorICAgIGFwcCA9IEZhc3RBUEkoKQorCisgICAgQGFwcC5nZXQoIi8iKQorICAgIGFzeW5jIGRlZiBnZXRfd2l0aF9kZXAodmFsdWU6IERlcGVuZGVkVmFsdWUpIC0+IHN0cjogICMgbm9xYQorICAgICAgICByZXR1cm4gZiJ2YWx1ZToge3ZhbHVlfSIKKworICAgIGNsaWVudCA9IFRlc3RDbGllbnQoYXBwKQorICAgIHJlc3BvbnNlID0gY2xpZW50LmdldCgiLyIpCisgICAgYXNzZXJ0IHJlc3BvbnNlLnN0YXR1c19jb2RlID09IDIwMAorICAgIGFzc2VydCByZXNwb25zZS50ZXh0ID09ICcidmFsdWU6IDEyMyIn")
print("TYPES " + str(type(TESTDIFF)) + " len " + str(len(TESTDIFF)), flush=True)
if isinstance(TESTDIFF, str): TESTDIFF = TESTDIFF.encode("latin-1")
work = "/tmp/duck6_" + PID
sh("rm -rf " + work + " && mkdir -p " + work)
print("PIP-INSTALL " + PID, flush=True)
sh("pip install -q " + PIPPKGS + " 2>&1 | tail -1", timeout=600)
url = "https://github.com/" + REPO + "/archive/" + BASE + ".tar.gz"
urllib.request.urlretrieve(url, work + "/src.tgz")
sh("tar xzf " + work + "/src.tgz -C " + work + " --strip-components=1", timeout=120)
pyenv = "PYTHONPATH=" + work
mrc, mout = sh("cd " + work + " && " + pyenv + " python -c \"import fastapi; print(fastapi.__file__)\" 2>&1 | tail -2", timeout=60)
print("MODFILE check done", flush=True)
print("TEST-RESULT-MODFILE " + PID + " " + mout[-200:], flush=True)
assert (work + "/") in mout, "shadow-fail: " + mout[-200:]
open(work + "/test_patch.diff", "wb").write(TESTDIFF)
assert open(work + "/test_patch.diff","rb").read()==TESTDIFF, "test-write-readback"
print("DIAG-LEN " + str(len(TESTDIFF)) + " tail=" + repr(TESTDIFF[-60:]), flush=True)
g1c, g1o = sh("git --version 2>&1", timeout=60)
print("GIT-VERSION " + g1o.strip().splitlines()[0], flush=True)
c0, o0 = sh("cd " + work + " && git apply --check test_patch.diff 2>&1; echo CHECK_ASIS_RC=$?", timeout=60)
print("CHECK-ASIS rc-line=" + repr(o0.strip().splitlines()[-2:]), flush=True)
a0, ao0 = sh("cd " + work + " && git apply test_patch.diff 2>&1; echo APPLY_ASIS_RC=$?", timeout=60)
print("APPLY-ASIS rc-line=" + repr(ao0.strip().splitlines()[-2:]), flush=True)
sh("cd " + work + " && git checkout -- . 2>&1; git clean -fdq 2>&1; echo CLEANED=$?", timeout=60)
open(work + "/test_patch_nl.diff","wb").write(TESTDIFF + b"\n")
c1, o1 = sh("cd " + work + " && git apply --check test_patch_nl.diff 2>&1; echo CHECK_NL_RC=$?", timeout=60)
print("CHECK-NL rc-line=" + repr(o1.strip().splitlines()[-2:]), flush=True)
a1, ao1 = sh("cd " + work + " && git apply test_patch_nl.diff 2>&1; echo APPLY_NL_RC=$?", timeout=60)
print("APPLY-NL rc-line=" + repr(ao1.strip().splitlines()[-2:]), flush=True)
b0, bo0 = sh("cd " + work + " && " + pyenv + " python -m pytest " + PYTEST + " -k \"" + KEXPR + "\" -q --tb=line -W ignore::PendingDeprecationWarning -W ignore::DeprecationWarning -p no:cacheprovider -p no:unraisableexception 2>&1 | tail -4; echo BASE_RC=$?", timeout=600)
print("BASE-AFTER-APPLIES " + bo0[-500:], flush=True)
print("PROBE-DONE " + PID, flush=True)
