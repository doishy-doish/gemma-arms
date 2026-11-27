# F2P PROBE (M654/M655): model-free. test-only apply -> pytest (expect FAIL), then +gold -> pytest (expect PASS).
# pid=fastapi_13207 v6 (+NL test+gold norm + inline-snapshot. No model calls. Ends: TEST-RESULT lines in log.
import os, subprocess, urllib.request, base64, sys
import sys as _sys
if _sys.version_info[0] < 3:
    import os as _os; _os.execvp("python3", ["python3"] + _sys.argv)
assert _sys.version_info >= (3, 10), "need python3.10+, got " + _sys.version
print("PY-VERSION " + sys.version.replace(chr(10)," "), flush=True)
def sh(cmd, timeout=300):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")
PID = "fastapi_13207"
REPO = "fastapi/fastapi"
BASE = "5126e099bdda"
PYTEST = "tests/test_computed_fields.py"
KEXPR = "test_get or test_openapi_schema"
SRCFILE = "fastapi/_compat/v2.py"
IMPORTPKG = "fastapi"
PIPPKGS = "fastapi pytest pytest-timeout requests python-multipart annotated-doc starlette==0.37.2 httpx==0.27.2 inline-snapshot"
TESTDIFF = base64.b64decode("LS0tIGEvdGVzdHMvdGVzdF9jb21wdXRlZF9maWVsZHMucHkKKysrIGIvdGVzdHMvdGVzdF9jb21wdXRlZF9maWVsZHMucHkKQEAgLTYsOCArNiw5IEBACiAKIAogQHB5dGVzdC5maXh0dXJlKG5hbWU9ImNsaWVudCIpCi1kZWYgZ2V0X2NsaWVudCgpOgotICAgIGFwcCA9IEZhc3RBUEkoKQorZGVmIGdldF9jbGllbnQocmVxdWVzdCk6CisgICAgc2VwYXJhdGVfaW5wdXRfb3V0cHV0X3NjaGVtYXMgPSByZXF1ZXN0LnBhcmFtCisgICAgYXBwID0gRmFzdEFQSShzZXBhcmF0ZV9pbnB1dF9vdXRwdXRfc2NoZW1hcz1zZXBhcmF0ZV9pbnB1dF9vdXRwdXRfc2NoZW1hcykKIAogICAgIGZyb20gcHlkYW50aWMgaW1wb3J0IEJhc2VNb2RlbCwgY29tcHV0ZWRfZmllbGQKIApAQCAtMzIsNiArMzMsNyBAQCBkZWYgcmVhZF9yZXNwb25zZXMoKSAtPiBSZWN0YW5nbGU6CiAgICAgcmV0dXJuIGNsaWVudAogCiAKK0BweXRlc3QubWFyay5wYXJhbWV0cml6ZSgiY2xpZW50IiwgW1RydWUsIEZhbHNlXSwgaW5kaXJlY3Q9VHJ1ZSkKIEBweXRlc3QubWFyay5wYXJhbWV0cml6ZSgicGF0aCIsIFsiLyIsICIvcmVzcG9uc2VzIl0pCiBAbmVlZHNfcHlkYW50aWN2MgogZGVmIHRlc3RfZ2V0KGNsaWVudDogVGVzdENsaWVudCwgcGF0aDogc3RyKToKQEAgLTQwLDYgKzQyLDcgQEAgZGVmIHRlc3RfZ2V0KGNsaWVudDogVGVzdENsaWVudCwgcGF0aDogc3RyKToKICAgICBhc3NlcnQgcmVzcG9uc2UuanNvbigpID09IHsid2lkdGgiOiAzLCAibGVuZ3RoIjogNCwgImFyZWEiOiAxMn0KIAogCitAcHl0ZXN0Lm1hcmsucGFyYW1ldHJpemUoImNsaWVudCIsIFtUcnVlLCBGYWxzZV0sIGluZGlyZWN0PVRydWUpCiBAbmVlZHNfcHlkYW50aWN2MgogZGVmIHRlc3Rfb3BlbmFwaV9zY2hlbWEoY2xpZW50OiBUZXN0Q2xpZW50KToKICAgICByZXNwb25zZSA9IGNsaWVudC5nZXQoIi9vcGVuYXBpLmpzb24iKQ==")
FIXDIFF = base64.b64decode("LS0tIGEvZmFzdGFwaS9fY29tcGF0L3YyLnB5CisrKyBiL2Zhc3RhcGkvX2NvbXBhdC92Mi5weQpAQCAtMTgwLDggKzE4MCwxMyBAQCBkZWYgZ2V0X3NjaGVtYV9mcm9tX21vZGVsX2ZpZWxkKAogICAgIF0sCiAgICAgc2VwYXJhdGVfaW5wdXRfb3V0cHV0X3NjaGVtYXM6IGJvb2wgPSBUcnVlLAogKSAtPiBEaWN0W3N0ciwgQW55XToKKyAgICBjb21wdXRlZF9maWVsZHMgPSBmaWVsZC5fdHlwZV9hZGFwdGVyLmNvcmVfc2NoZW1hLmdldCgic2NoZW1hIiwge30pLmdldCgKKyAgICAgICAgImNvbXB1dGVkX2ZpZWxkcyIsIFtdCisgICAgKQogICAgIG92ZXJyaWRlX21vZGU6IFVuaW9uW0xpdGVyYWxbInZhbGlkYXRpb24iXSwgTm9uZV0gPSAoCi0gICAgICAgIE5vbmUgaWYgc2VwYXJhdGVfaW5wdXRfb3V0cHV0X3NjaGVtYXMgZWxzZSAidmFsaWRhdGlvbiIKKyAgICAgICAgTm9uZQorICAgICAgICBpZiAoc2VwYXJhdGVfaW5wdXRfb3V0cHV0X3NjaGVtYXMgb3IgbGVuKGNvbXB1dGVkX2ZpZWxkcykgPiAwKQorICAgICAgICBlbHNlICJ2YWxpZGF0aW9uIgogICAgICkKICAgICAjIFRoaXMgZXhwZWN0cyB0aGF0IEdlbmVyYXRlSnNvblNjaGVtYSB3YXMgYWxyZWFkeSB1c2VkIHRvIGdlbmVyYXRlIHRoZSBkZWZpbml0aW9ucwogICAgIGpzb25fc2NoZW1hID0gZmllbGRfbWFwcGluZ1soZmllbGQsIG92ZXJyaWRlX21vZGUgb3IgZmllbGQubW9kZSldCkBAIC0yMDMsOSArMjA4LDE0IEBAIGRlZiBnZXRfZGVmaW5pdGlvbnMoCiAgICAgRGljdFtUdXBsZVtNb2RlbEZpZWxkLCBMaXRlcmFsWyJ2YWxpZGF0aW9uIiwgInNlcmlhbGl6YXRpb24iXV0sIEpzb25TY2hlbWFWYWx1ZV0sCiAgICAgRGljdFtzdHIsIERpY3Rbc3RyLCBBbnldXSwKIF06CisgICAgaGFzX2NvbXB1dGVkX2ZpZWxkczogYm9vbCA9IGFueSgKKyAgICAgICAgZmllbGQuX3R5cGVfYWRhcHRlci5jb3JlX3NjaGVtYS5nZXQoInNjaGVtYSIsIHt9KS5nZXQoImNvbXB1dGVkX2ZpZWxkcyIsIFtdKQorICAgICAgICBmb3IgZmllbGQgaW4gZmllbGRzCisgICAgKQorCiAgICAgc2NoZW1hX2dlbmVyYXRvciA9IEdlbmVyYXRlSnNvblNjaGVtYShyZWZfdGVtcGxhdGU9UkVGX1RFTVBMQVRFKQogICAgIG92ZXJyaWRlX21vZGU6IFVuaW9uW0xpdGVyYWxbInZhbGlkYXRpb24iXSwgTm9uZV0gPSAoCi0gICAgICAgIE5vbmUgaWYgc2VwYXJhdGVfaW5wdXRfb3V0cHV0X3NjaGVtYXMgZWxzZSAidmFsaWRhdGlvbiIKKyAgICAgICAgTm9uZSBpZiAoc2VwYXJhdGVfaW5wdXRfb3V0cHV0X3NjaGVtYXMgb3IgaGFzX2NvbXB1dGVkX2ZpZWxkcykgZWxzZSAidmFsaWRhdGlvbiIKICAgICApCiAgICAgdmFsaWRhdGlvbl9maWVsZHMgPSBbZmllbGQgZm9yIGZpZWxkIGluIGZpZWxkcyBpZiBmaWVsZC5tb2RlID09ICJ2YWxpZGF0aW9uIl0KICAgICBzZXJpYWxpemF0aW9uX2ZpZWxkcyA9IFtmaWVsZCBmb3IgZmllbGQgaW4gZmllbGRzIGlmIGZpZWxkLm1vZGUgPT0gInNlcmlhbGl6YXRpb24iXQ==")
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
