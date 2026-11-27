# HOW THIS VEHICLE IS SUPPOSED TO BE WRITTEN (M724, durable just-in-case note).
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
# pid=fastapi_14360 (M739: 14430-replacement shortlist, base eead41bf4cf8). No model calls. Ends: TEST-RESULT lines in log.
import os, subprocess, urllib.request, base64, sys
import sys as _sys
if _sys.version_info[0] < 3:
    import os as _os; _os.execvp("python3", ["python3"] + _sys.argv)
assert _sys.version_info >= (3, 10), "need python3.10+, got " + _sys.version
print("PY-VERSION " + sys.version.replace(chr(10)," "), flush=True)
def sh(cmd, timeout=300):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")
PID = "fastapi_14360"
REPO = "fastapi/fastapi"
BASE = "eead41bf4cf8587b4d86091dd3eabbb85796e717"
PYTEST = "tests/test_request_param_model_by_alias.py"
KEXPR = "test_query_model_with_alias or test_header_model_with_alias or test_cookie_model_with_alias or test_query_model_with_alias_by_name or test_header_model_with_alias_by_name or test_cookie_model_with_alias_by_name"
SRCFILE = "fastapi/dependencies/utils.py"
IMPORTPKG = "fastapi"
PIPPKGS = "fastapi pytest pytest-timeout requests python-multipart annotated-doc starlette==0.37.2 httpx==0.27.2 inline-snapshot sqlalchemy orjson ujson dirty_equals"
TESTDIFF = base64.b64decode("LS0tIGEvdGVzdHMvdGVzdF9yZXF1ZXN0X3BhcmFtX21vZGVsX2J5X2FsaWFzLnB5CisrKyBiL3Rlc3RzL3Rlc3RfcmVxdWVzdF9wYXJhbV9tb2RlbF9ieV9hbGlhcy5weQpAQCAtMCwwICsxLDc2IEBACitmcm9tIGRpcnR5X2VxdWFscyBpbXBvcnQgSXNQYXJ0aWFsRGljdAorZnJvbSBmYXN0YXBpIGltcG9ydCBDb29raWUsIEZhc3RBUEksIEhlYWRlciwgUXVlcnkKK2Zyb20gZmFzdGFwaS5fY29tcGF0IGltcG9ydCBQWURBTlRJQ19WMgorZnJvbSBmYXN0YXBpLnRlc3RjbGllbnQgaW1wb3J0IFRlc3RDbGllbnQKK2Zyb20gcHlkYW50aWMgaW1wb3J0IEJhc2VNb2RlbCwgRmllbGQKKworYXBwID0gRmFzdEFQSSgpCisKKworY2xhc3MgTW9kZWwoQmFzZU1vZGVsKToKKyAgICBwYXJhbTogc3RyID0gRmllbGQoYWxpYXM9InBhcmFtX2FsaWFzIikKKworCitAYXBwLmdldCgiL3F1ZXJ5IikKK2FzeW5jIGRlZiBxdWVyeV9tb2RlbChkYXRhOiBNb2RlbCA9IFF1ZXJ5KCkpOgorICAgIHJldHVybiB7InBhcmFtIjogZGF0YS5wYXJhbX0KKworCitAYXBwLmdldCgiL2hlYWRlciIpCithc3luYyBkZWYgaGVhZGVyX21vZGVsKGRhdGE6IE1vZGVsID0gSGVhZGVyKCkpOgorICAgIHJldHVybiB7InBhcmFtIjogZGF0YS5wYXJhbX0KKworCitAYXBwLmdldCgiL2Nvb2tpZSIpCithc3luYyBkZWYgY29va2llX21vZGVsKGRhdGE6IE1vZGVsID0gQ29va2llKCkpOgorICAgIHJldHVybiB7InBhcmFtIjogZGF0YS5wYXJhbX0KKworCitkZWYgdGVzdF9xdWVyeV9tb2RlbF93aXRoX2FsaWFzKCk6CisgICAgY2xpZW50ID0gVGVzdENsaWVudChhcHApCisgICAgcmVzcG9uc2UgPSBjbGllbnQuZ2V0KCIvcXVlcnkiLCBwYXJhbXM9eyJwYXJhbV9hbGlhcyI6ICJ2YWx1ZSJ9KQorICAgIGFzc2VydCByZXNwb25zZS5zdGF0dXNfY29kZSA9PSAyMDAsIHJlc3BvbnNlLnRleHQKKyAgICBhc3NlcnQgcmVzcG9uc2UuanNvbigpID09IHsicGFyYW0iOiAidmFsdWUifQorCisKK2RlZiB0ZXN0X2hlYWRlcl9tb2RlbF93aXRoX2FsaWFzKCk6CisgICAgY2xpZW50ID0gVGVzdENsaWVudChhcHApCisgICAgcmVzcG9uc2UgPSBjbGllbnQuZ2V0KCIvaGVhZGVyIiwgaGVhZGVycz17InBhcmFtX2FsaWFzIjogInZhbHVlIn0pCisgICAgYXNzZXJ0IHJlc3BvbnNlLnN0YXR1c19jb2RlID09IDIwMCwgcmVzcG9uc2UudGV4dAorICAgIGFzc2VydCByZXNwb25zZS5qc29uKCkgPT0geyJwYXJhbSI6ICJ2YWx1ZSJ9CisKKworZGVmIHRlc3RfY29va2llX21vZGVsX3dpdGhfYWxpYXMoKToKKyAgICBjbGllbnQgPSBUZXN0Q2xpZW50KGFwcCkKKyAgICBjbGllbnQuY29va2llcy5zZXQoInBhcmFtX2FsaWFzIiwgInZhbHVlIikKKyAgICByZXNwb25zZSA9IGNsaWVudC5nZXQoIi9jb29raWUiKQorICAgIGFzc2VydCByZXNwb25zZS5zdGF0dXNfY29kZSA9PSAyMDAsIHJlc3BvbnNlLnRleHQKKyAgICBhc3NlcnQgcmVzcG9uc2UuanNvbigpID09IHsicGFyYW0iOiAidmFsdWUifQorCisKK2RlZiB0ZXN0X3F1ZXJ5X21vZGVsX3dpdGhfYWxpYXNfYnlfbmFtZSgpOgorICAgIGNsaWVudCA9IFRlc3RDbGllbnQoYXBwKQorICAgIHJlc3BvbnNlID0gY2xpZW50LmdldCgiL3F1ZXJ5IiwgcGFyYW1zPXsicGFyYW0iOiAidmFsdWUifSkKKyAgICBhc3NlcnQgcmVzcG9uc2Uuc3RhdHVzX2NvZGUgPT0gNDIyLCByZXNwb25zZS50ZXh0CisgICAgZGV0YWlscyA9IHJlc3BvbnNlLmpzb24oKQorICAgIGlmIFBZREFOVElDX1YyOgorICAgICAgICBhc3NlcnQgZGV0YWlsc1siZGV0YWlsIl1bMF1bImlucHV0Il0gPT0geyJwYXJhbSI6ICJ2YWx1ZSJ9CisKKworZGVmIHRlc3RfaGVhZGVyX21vZGVsX3dpdGhfYWxpYXNfYnlfbmFtZSgpOgorICAgIGNsaWVudCA9IFRlc3RDbGllbnQoYXBwKQorICAgIHJlc3BvbnNlID0gY2xpZW50LmdldCgiL2hlYWRlciIsIGhlYWRlcnM9eyJwYXJhbSI6ICJ2YWx1ZSJ9KQorICAgIGFzc2VydCByZXNwb25zZS5zdGF0dXNfY29kZSA9PSA0MjIsIHJlc3BvbnNlLnRleHQKKyAgICBkZXRhaWxzID0gcmVzcG9uc2UuanNvbigpCisgICAgaWYgUFlEQU5USUNfVjI6CisgICAgICAgIGFzc2VydCBkZXRhaWxzWyJkZXRhaWwiXVswXVsiaW5wdXQiXSA9PSBJc1BhcnRpYWxEaWN0KHsicGFyYW0iOiAidmFsdWUifSkKKworCitkZWYgdGVzdF9jb29raWVfbW9kZWxfd2l0aF9hbGlhc19ieV9uYW1lKCk6CisgICAgY2xpZW50ID0gVGVzdENsaWVudChhcHApCisgICAgY2xpZW50LmNvb2tpZXMuc2V0KCJwYXJhbSIsICJ2YWx1ZSIpCisgICAgcmVzcG9uc2UgPSBjbGllbnQuZ2V0KCIvY29va2llIikKKyAgICBhc3NlcnQgcmVzcG9uc2Uuc3RhdHVzX2NvZGUgPT0gNDIyLCByZXNwb25zZS50ZXh0CisgICAgZGV0YWlscyA9IHJlc3BvbnNlLmpzb24oKQorICAgIGlmIFBZREFOVElDX1YyOgorICAgICAgICBhc3NlcnQgZGV0YWlsc1siZGV0YWlsIl1bMF1bImlucHV0Il0gPT0geyJwYXJhbSI6ICJ2YWx1ZSJ9")
FIXDIFF = base64.b64decode("LS0tIGEvZmFzdGFwaS9kZXBlbmRlbmNpZXMvdXRpbHMucHkKKysrIGIvZmFzdGFwaS9kZXBlbmRlbmNpZXMvdXRpbHMucHkKQEAgLTc4Nyw5ICs3ODcsOCBAQCBkZWYgcmVxdWVzdF9wYXJhbXNfdG9fYXJncygKICAgICAgICAgICAgICAgICApCiAgICAgICAgIHZhbHVlID0gX2dldF9tdWx0aWRpY3RfdmFsdWUoZmllbGQsIHJlY2VpdmVkX3BhcmFtcywgYWxpYXM9YWxpYXMpCiAgICAgICAgIGlmIHZhbHVlIGlzIG5vdCBOb25lOgotICAgICAgICAgICAgcGFyYW1zX3RvX3Byb2Nlc3NbZmllbGQubmFtZV0gPSB2YWx1ZQorICAgICAgICAgICAgcGFyYW1zX3RvX3Byb2Nlc3NbZmllbGQuYWxpYXNdID0gdmFsdWUKICAgICAgICAgcHJvY2Vzc2VkX2tleXMuYWRkKGFsaWFzIG9yIGZpZWxkLmFsaWFzKQotICAgICAgICBwcm9jZXNzZWRfa2V5cy5hZGQoZmllbGQubmFtZSkKIAogICAgIGZvciBrZXkgaW4gcmVjZWl2ZWRfcGFyYW1zLmtleXMoKToKICAgICAgICAgaWYga2V5IG5vdCBpbiBwcm9jZXNzZWRfa2V5czo=")
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
