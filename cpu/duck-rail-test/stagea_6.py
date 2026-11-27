# F2P PROBE (M654/M655): model-free. test-only apply -> pytest (expect FAIL), then +gold -> pytest (expect PASS).
# pid=fastapi_14463 base=f2687dc1bb01 v5 (+NL test+gold norm. No model calls. Ends: TEST-RESULT lines in log.
import os, subprocess, urllib.request, base64, sys
import sys as _sys
if _sys.version_info[0] < 3:
    import os as _os; _os.execvp("python3", ["python3"] + _sys.argv)
assert _sys.version_info >= (3, 10), "need python3.10+, got " + _sys.version
print("PY-VERSION " + sys.version.replace(chr(10)," "), flush=True)
def sh(cmd, timeout=300):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")
PID = "fastapi_14463"
REPO = "fastapi/fastapi"
BASE = "f2687dc1bb01"
PYTEST = "tests/test_additional_responses_union_duplicate_anyof.py"
KEXPR = "test_openapi_schema"
SRCFILE = "fastapi/openapi/utils.py"
IMPORTPKG = "fastapi"
PIPPKGS = "fastapi pytest pytest-timeout requests python-multipart annotated-doc starlette==0.37.2 httpx==0.27.2"
TESTDIFF = base64.b64decode("LS0tIGEvdGVzdHMvdGVzdF9hZGRpdGlvbmFsX3Jlc3BvbnNlc191bmlvbl9kdXBsaWNhdGVfYW55b2YucHkKKysrIGIvdGVzdHMvdGVzdF9hZGRpdGlvbmFsX3Jlc3BvbnNlc191bmlvbl9kdXBsaWNhdGVfYW55b2YucHkKQEAgLTAsMCArMSwxMjMgQEAKKyIiIgorUmVncmVzc2lvbiB0ZXN0OiBFbnN1cmUgYXBwLWxldmVsIHJlc3BvbnNlcyB3aXRoIFVuaW9uIG1vZGVscyBhbmQgY29udGVudC9leGFtcGxlcworZG9uJ3QgYWNjdW11bGF0ZSBkdXBsaWNhdGUgJHJlZiBlbnRyaWVzIGluIGFueU9mIGFycmF5cy4KK1NlZSBodHRwczovL2dpdGh1Yi5jb20vZmFzdGFwaS9mYXN0YXBpL3B1bGwvMTQ0NjMKKyIiIgorCitmcm9tIHR5cGluZyBpbXBvcnQgVW5pb24KKworZnJvbSBmYXN0YXBpIGltcG9ydCBGYXN0QVBJCitmcm9tIGZhc3RhcGkudGVzdGNsaWVudCBpbXBvcnQgVGVzdENsaWVudAorZnJvbSBweWRhbnRpYyBpbXBvcnQgQmFzZU1vZGVsCisKKworY2xhc3MgTW9kZWxBKEJhc2VNb2RlbCk6CisgICAgYTogc3RyCisKKworY2xhc3MgTW9kZWxCKEJhc2VNb2RlbCk6CisgICAgYjogc3RyCisKKworYXBwID0gRmFzdEFQSSgKKyAgICByZXNwb25zZXM9eworICAgICAgICA1MDA6IHsKKyAgICAgICAgICAgICJtb2RlbCI6IFVuaW9uW01vZGVsQSwgTW9kZWxCXSwKKyAgICAgICAgICAgICJjb250ZW50IjogeyJhcHBsaWNhdGlvbi9qc29uIjogeyJleGFtcGxlcyI6IHsiQ2FzZSBBIjogeyJ2YWx1ZSI6ICJhIn19fX0sCisgICAgICAgIH0KKyAgICB9CispCisKKworQGFwcC5nZXQoIi9yb3V0ZTEiKQorYXN5bmMgZGVmIHJvdXRlMSgpOgorICAgIHBhc3MgICMgcHJhZ21hOiBubyBjb3ZlcgorCisKK0BhcHAuZ2V0KCIvcm91dGUyIikKK2FzeW5jIGRlZiByb3V0ZTIoKToKKyAgICBwYXNzICAjIHByYWdtYTogbm8gY292ZXIKKworCitjbGllbnQgPSBUZXN0Q2xpZW50KGFwcCkKKworCitkZWYgdGVzdF9vcGVuYXBpX3NjaGVtYSgpOgorICAgIHJlc3BvbnNlID0gY2xpZW50LmdldCgiL29wZW5hcGkuanNvbiIpCisgICAgYXNzZXJ0IHJlc3BvbnNlLnN0YXR1c19jb2RlID09IDIwMCwgcmVzcG9uc2UudGV4dAorICAgIGFzc2VydCByZXNwb25zZS5qc29uKCkgPT0geworICAgICAgICAib3BlbmFwaSI6ICIzLjEuMCIsCisgICAgICAgICJpbmZvIjogeyJ0aXRsZSI6ICJGYXN0QVBJIiwgInZlcnNpb24iOiAiMC4xLjAifSwKKyAgICAgICAgInBhdGhzIjogeworICAgICAgICAgICAgIi9yb3V0ZTEiOiB7CisgICAgICAgICAgICAgICAgImdldCI6IHsKKyAgICAgICAgICAgICAgICAgICAgInN1bW1hcnkiOiAiUm91dGUxIiwKKyAgICAgICAgICAgICAgICAgICAgIm9wZXJhdGlvbklkIjogInJvdXRlMV9yb3V0ZTFfZ2V0IiwKKyAgICAgICAgICAgICAgICAgICAgInJlc3BvbnNlcyI6IHsKKyAgICAgICAgICAgICAgICAgICAgICAgICIyMDAiOiB7CisgICAgICAgICAgICAgICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIlN1Y2Nlc3NmdWwgUmVzcG9uc2UiLAorICAgICAgICAgICAgICAgICAgICAgICAgICAgICJjb250ZW50IjogeyJhcHBsaWNhdGlvbi9qc29uIjogeyJzY2hlbWEiOiB7fX19LAorICAgICAgICAgICAgICAgICAgICAgICAgfSwKKyAgICAgICAgICAgICAgICAgICAgICAgICI1MDAiOiB7CisgICAgICAgICAgICAgICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIkludGVybmFsIFNlcnZlciBFcnJvciIsCisgICAgICAgICAgICAgICAgICAgICAgICAgICAgImNvbnRlbnQiOiB7CisgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICJhcHBsaWNhdGlvbi9qc29uIjogeworICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgInNjaGVtYSI6IHsKKyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiYW55T2YiOiBbCisgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHsiJHJlZiI6ICIjL2NvbXBvbmVudHMvc2NoZW1hcy9Nb2RlbEEifSwKKyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyIkcmVmIjogIiMvY29tcG9uZW50cy9zY2hlbWFzL01vZGVsQiJ9LAorICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIF0sCisgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgInRpdGxlIjogIlJlc3BvbnNlIDUwMCBSb3V0ZTEgUm91dGUxIEdldCIsCisgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB9LAorICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgImV4YW1wbGVzIjogeyJDYXNlIEEiOiB7InZhbHVlIjogImEifX0sCisgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIH0KKyAgICAgICAgICAgICAgICAgICAgICAgICAgICB9LAorICAgICAgICAgICAgICAgICAgICAgICAgfSwKKyAgICAgICAgICAgICAgICAgICAgfSwKKyAgICAgICAgICAgICAgICB9CisgICAgICAgICAgICB9LAorICAgICAgICAgICAgIi9yb3V0ZTIiOiB7CisgICAgICAgICAgICAgICAgImdldCI6IHsKKyAgICAgICAgICAgICAgICAgICAgInN1bW1hcnkiOiAiUm91dGUyIiwKKyAgICAgICAgICAgICAgICAgICAgIm9wZXJhdGlvbklkIjogInJvdXRlMl9yb3V0ZTJfZ2V0IiwKKyAgICAgICAgICAgICAgICAgICAgInJlc3BvbnNlcyI6IHsKKyAgICAgICAgICAgICAgICAgICAgICAgICIyMDAiOiB7CisgICAgICAgICAgICAgICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIlN1Y2Nlc3NmdWwgUmVzcG9uc2UiLAorICAgICAgICAgICAgICAgICAgICAgICAgICAgICJjb250ZW50IjogeyJhcHBsaWNhdGlvbi9qc29uIjogeyJzY2hlbWEiOiB7fX19LAorICAgICAgICAgICAgICAgICAgICAgICAgfSwKKyAgICAgICAgICAgICAgICAgICAgICAgICI1MDAiOiB7CisgICAgICAgICAgICAgICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIkludGVybmFsIFNlcnZlciBFcnJvciIsCisgICAgICAgICAgICAgICAgICAgICAgICAgICAgImNvbnRlbnQiOiB7CisgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICJhcHBsaWNhdGlvbi9qc29uIjogeworICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgInNjaGVtYSI6IHsKKyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiYW55T2YiOiBbCisgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHsiJHJlZiI6ICIjL2NvbXBvbmVudHMvc2NoZW1hcy9Nb2RlbEEifSwKKyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgeyIkcmVmIjogIiMvY29tcG9uZW50cy9zY2hlbWFzL01vZGVsQiJ9LAorICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIF0sCisgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgInRpdGxlIjogIlJlc3BvbnNlIDUwMCBSb3V0ZTIgUm91dGUyIEdldCIsCisgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB9LAorICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgImV4YW1wbGVzIjogeyJDYXNlIEEiOiB7InZhbHVlIjogImEifX0sCisgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIH0KKyAgICAgICAgICAgICAgICAgICAgICAgICAgICB9LAorICAgICAgICAgICAgICAgICAgICAgICAgfSwKKyAgICAgICAgICAgICAgICAgICAgfSwKKyAgICAgICAgICAgICAgICB9CisgICAgICAgICAgICB9LAorICAgICAgICB9LAorICAgICAgICAiY29tcG9uZW50cyI6IHsKKyAgICAgICAgICAgICJzY2hlbWFzIjogeworICAgICAgICAgICAgICAgICJNb2RlbEEiOiB7CisgICAgICAgICAgICAgICAgICAgICJwcm9wZXJ0aWVzIjogeyJhIjogeyJ0eXBlIjogInN0cmluZyIsICJ0aXRsZSI6ICJBIn19LAorICAgICAgICAgICAgICAgICAgICAidHlwZSI6ICJvYmplY3QiLAorICAgICAgICAgICAgICAgICAgICAicmVxdWlyZWQiOiBbImEiXSwKKyAgICAgICAgICAgICAgICAgICAgInRpdGxlIjogIk1vZGVsQSIsCisgICAgICAgICAgICAgICAgfSwKKyAgICAgICAgICAgICAgICAiTW9kZWxCIjogeworICAgICAgICAgICAgICAgICAgICAicHJvcGVydGllcyI6IHsiYiI6IHsidHlwZSI6ICJzdHJpbmciLCAidGl0bGUiOiAiQiJ9fSwKKyAgICAgICAgICAgICAgICAgICAgInR5cGUiOiAib2JqZWN0IiwKKyAgICAgICAgICAgICAgICAgICAgInJlcXVpcmVkIjogWyJiIl0sCisgICAgICAgICAgICAgICAgICAgICJ0aXRsZSI6ICJNb2RlbEIiLAorICAgICAgICAgICAgICAgIH0sCisgICAgICAgICAgICB9CisgICAgICAgIH0sCisgICAgfQ==")
FIXDIFF = base64.b64decode("LS0tIGEvZmFzdGFwaS9vcGVuYXBpL3V0aWxzLnB5CisrKyBiL2Zhc3RhcGkvb3BlbmFwaS91dGlscy5weQpAQCAtMSwzICsxLDQgQEAKK2ltcG9ydCBjb3B5CiBpbXBvcnQgaHR0cC5jbGllbnQKIGltcG9ydCBpbnNwZWN0CiBpbXBvcnQgd2FybmluZ3MKQEAgLTM3Nyw3ICszNzgsNyBAQCBkZWYgZ2V0X29wZW5hcGlfcGF0aCgKICAgICAgICAgICAgICAgICAgICAgYWRkaXRpb25hbF9zdGF0dXNfY29kZSwKICAgICAgICAgICAgICAgICAgICAgYWRkaXRpb25hbF9yZXNwb25zZSwKICAgICAgICAgICAgICAgICApIGluIHJvdXRlLnJlc3BvbnNlcy5pdGVtcygpOgotICAgICAgICAgICAgICAgICAgICBwcm9jZXNzX3Jlc3BvbnNlID0gYWRkaXRpb25hbF9yZXNwb25zZS5jb3B5KCkKKyAgICAgICAgICAgICAgICAgICAgcHJvY2Vzc19yZXNwb25zZSA9IGNvcHkuZGVlcGNvcHkoYWRkaXRpb25hbF9yZXNwb25zZSkKICAgICAgICAgICAgICAgICAgICAgcHJvY2Vzc19yZXNwb25zZS5wb3AoIm1vZGVsIiwgTm9uZSkKICAgICAgICAgICAgICAgICAgICAgc3RhdHVzX2NvZGVfa2V5ID0gc3RyKGFkZGl0aW9uYWxfc3RhdHVzX2NvZGUpLnVwcGVyKCkKICAgICAgICAgICAgICAgICAgICAgaWYgc3RhdHVzX2NvZGVfa2V5ID09ICJERUZBVUxUIjo=")
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
