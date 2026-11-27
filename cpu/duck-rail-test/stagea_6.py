# F2P PROBE (M654/M655): model-free. test-only apply -> pytest (expect FAIL), then +gold -> pytest (expect PASS).
# pid=fastapi_14266 base=2cf04ee30db9 v5 (+NL test+gold norm. No model calls. Ends: TEST-RESULT lines in log.
import os, subprocess, urllib.request, base64, sys
import sys as _sys
if _sys.version_info[0] < 3:
    import os as _os; _os.execvp("python3", ["python3"] + _sys.argv)
assert _sys.version_info >= (3, 10), "need python3.10+, got " + _sys.version
print("PY-VERSION " + sys.version.replace(chr(10)," "), flush=True)
def sh(cmd, timeout=300):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")
PID = "fastapi_14266"
REPO = "fastapi/fastapi"
BASE = "2cf04ee30db9"
PYTEST = "tests/test_top_level_security_scheme_in_openapi.py"
KEXPR = "test_get_root or test_get_root_no_token or test_openapi_schema"
SRCFILE = "fastapi/dependencies/utils.py"
IMPORTPKG = "fastapi"
PIPPKGS = "fastapi pytest pytest-timeout requests python-multipart annotated-doc starlette==0.37.2 httpx==0.27.2"
TESTDIFF = base64.b64decode("LS0tIGEvdGVzdHMvdGVzdF90b3BfbGV2ZWxfc2VjdXJpdHlfc2NoZW1lX2luX29wZW5hcGkucHkKKysrIGIvdGVzdHMvdGVzdF90b3BfbGV2ZWxfc2VjdXJpdHlfc2NoZW1lX2luX29wZW5hcGkucHkKQEAgLTAsMCArMSw2MCBAQAorIyBUZXN0IHNlY3VyaXR5IHNjaGVtZSBhdCB0aGUgdG9wIGxldmVsLCBpbmNsdWRpbmcgT3BlbkFQSQorIyBSZWY6IGh0dHBzOi8vZ2l0aHViLmNvbS9mYXN0YXBpL2Zhc3RhcGkvZGlzY3Vzc2lvbnMvMTQyNjMKKyMgUmVmOiBodHRwczovL2dpdGh1Yi5jb20vZmFzdGFwaS9mYXN0YXBpL2lzc3Vlcy8xNDI3MQorZnJvbSBmYXN0YXBpIGltcG9ydCBEZXBlbmRzLCBGYXN0QVBJCitmcm9tIGZhc3RhcGkuc2VjdXJpdHkgaW1wb3J0IEhUVFBCZWFyZXIKK2Zyb20gZmFzdGFwaS50ZXN0Y2xpZW50IGltcG9ydCBUZXN0Q2xpZW50Citmcm9tIGlubGluZV9zbmFwc2hvdCBpbXBvcnQgc25hcHNob3QKKworYXBwID0gRmFzdEFQSSgpCisKK2JlYXJlcl9zY2hlbWUgPSBIVFRQQmVhcmVyKCkKKworCitAYXBwLmdldCgiLyIsIGRlcGVuZGVuY2llcz1bRGVwZW5kcyhiZWFyZXJfc2NoZW1lKV0pCithc3luYyBkZWYgZ2V0X3Jvb3QoKToKKyAgICByZXR1cm4geyJtZXNzYWdlIjogIkhlbGxvLCBXb3JsZCEifQorCisKK2NsaWVudCA9IFRlc3RDbGllbnQoYXBwKQorCisKK2RlZiB0ZXN0X2dldF9yb290KCk6CisgICAgcmVzcG9uc2UgPSBjbGllbnQuZ2V0KCIvIiwgaGVhZGVycz17IkF1dGhvcml6YXRpb24iOiAiQmVhcmVyIHRva2VuIn0pCisgICAgYXNzZXJ0IHJlc3BvbnNlLnN0YXR1c19jb2RlID09IDIwMCwgcmVzcG9uc2UudGV4dAorICAgIGFzc2VydCByZXNwb25zZS5qc29uKCkgPT0geyJtZXNzYWdlIjogIkhlbGxvLCBXb3JsZCEifQorCisKK2RlZiB0ZXN0X2dldF9yb290X25vX3Rva2VuKCk6CisgICAgcmVzcG9uc2UgPSBjbGllbnQuZ2V0KCIvIikKKyAgICBhc3NlcnQgcmVzcG9uc2Uuc3RhdHVzX2NvZGUgPT0gNDAzLCByZXNwb25zZS50ZXh0CisgICAgYXNzZXJ0IHJlc3BvbnNlLmpzb24oKSA9PSB7ImRldGFpbCI6ICJOb3QgYXV0aGVudGljYXRlZCJ9CisKKworZGVmIHRlc3Rfb3BlbmFwaV9zY2hlbWEoKToKKyAgICByZXNwb25zZSA9IGNsaWVudC5nZXQoIi9vcGVuYXBpLmpzb24iKQorICAgIGFzc2VydCByZXNwb25zZS5zdGF0dXNfY29kZSA9PSAyMDAsIHJlc3BvbnNlLnRleHQKKyAgICBhc3NlcnQgcmVzcG9uc2UuanNvbigpID09IHNuYXBzaG90KAorICAgICAgICB7CisgICAgICAgICAgICAib3BlbmFwaSI6ICIzLjEuMCIsCisgICAgICAgICAgICAiaW5mbyI6IHsidGl0bGUiOiAiRmFzdEFQSSIsICJ2ZXJzaW9uIjogIjAuMS4wIn0sCisgICAgICAgICAgICAicGF0aHMiOiB7CisgICAgICAgICAgICAgICAgIi8iOiB7CisgICAgICAgICAgICAgICAgICAgICJnZXQiOiB7CisgICAgICAgICAgICAgICAgICAgICAgICAic3VtbWFyeSI6ICJHZXQgUm9vdCIsCisgICAgICAgICAgICAgICAgICAgICAgICAib3BlcmF0aW9uSWQiOiAiZ2V0X3Jvb3RfX2dldCIsCisgICAgICAgICAgICAgICAgICAgICAgICAicmVzcG9uc2VzIjogeworICAgICAgICAgICAgICAgICAgICAgICAgICAgICIyMDAiOiB7CisgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICJkZXNjcmlwdGlvbiI6ICJTdWNjZXNzZnVsIFJlc3BvbnNlIiwKKyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgImNvbnRlbnQiOiB7ImFwcGxpY2F0aW9uL2pzb24iOiB7InNjaGVtYSI6IHt9fX0sCisgICAgICAgICAgICAgICAgICAgICAgICAgICAgfQorICAgICAgICAgICAgICAgICAgICAgICAgfSwKKyAgICAgICAgICAgICAgICAgICAgICAgICJzZWN1cml0eSI6IFt7IkhUVFBCZWFyZXIiOiBbXX1dLAorICAgICAgICAgICAgICAgICAgICB9CisgICAgICAgICAgICAgICAgfQorICAgICAgICAgICAgfSwKKyAgICAgICAgICAgICJjb21wb25lbnRzIjogeworICAgICAgICAgICAgICAgICJzZWN1cml0eVNjaGVtZXMiOiB7IkhUVFBCZWFyZXIiOiB7InR5cGUiOiAiaHR0cCIsICJzY2hlbWUiOiAiYmVhcmVyIn19CisgICAgICAgICAgICB9LAorICAgICAgICB9CisgICAgKQ==")
FIXDIFF = base64.b64decode("LS0tIGEvZmFzdGFwaS9kZXBlbmRlbmNpZXMvdXRpbHMucHkKKysrIGIvZmFzdGFwaS9kZXBlbmRlbmNpZXMvdXRpbHMucHkKQEAgLTI0OCw2ICsyNDgsMTQgQEAgZGVmIGdldF9kZXBlbmRhbnQoCiAgICAgcGF0aF9wYXJhbV9uYW1lcyA9IGdldF9wYXRoX3BhcmFtX25hbWVzKHBhdGgpCiAgICAgZW5kcG9pbnRfc2lnbmF0dXJlID0gZ2V0X3R5cGVkX3NpZ25hdHVyZShjYWxsKQogICAgIHNpZ25hdHVyZV9wYXJhbXMgPSBlbmRwb2ludF9zaWduYXR1cmUucGFyYW1ldGVycworICAgIGlmIGlzaW5zdGFuY2UoY2FsbCwgU2VjdXJpdHlCYXNlKToKKyAgICAgICAgdXNlX3Njb3BlczogTGlzdFtzdHJdID0gW10KKyAgICAgICAgaWYgaXNpbnN0YW5jZShjYWxsLCAoT0F1dGgyLCBPcGVuSWRDb25uZWN0KSk6CisgICAgICAgICAgICB1c2Vfc2NvcGVzID0gc2VjdXJpdHlfc2NvcGVzCisgICAgICAgIHNlY3VyaXR5X3JlcXVpcmVtZW50ID0gU2VjdXJpdHlSZXF1aXJlbWVudCgKKyAgICAgICAgICAgIHNlY3VyaXR5X3NjaGVtZT1jYWxsLCBzY29wZXM9dXNlX3Njb3BlcworICAgICAgICApCisgICAgICAgIGRlcGVuZGFudC5zZWN1cml0eV9yZXF1aXJlbWVudHMuYXBwZW5kKHNlY3VyaXR5X3JlcXVpcmVtZW50KQogICAgIGZvciBwYXJhbV9uYW1lLCBwYXJhbSBpbiBzaWduYXR1cmVfcGFyYW1zLml0ZW1zKCk6CiAgICAgICAgIGlzX3BhdGhfcGFyYW0gPSBwYXJhbV9uYW1lIGluIHBhdGhfcGFyYW1fbmFtZXMKICAgICAgICAgcGFyYW1fZGV0YWlscyA9IGFuYWx5emVfcGFyYW0oCkBAIC0yNjksMTYgKzI3Nyw2IEBAIGRlZiBnZXRfZGVwZW5kYW50KAogICAgICAgICAgICAgICAgIHNlY3VyaXR5X3Njb3Blcz11c2Vfc2VjdXJpdHlfc2NvcGVzLAogICAgICAgICAgICAgICAgIHVzZV9jYWNoZT1wYXJhbV9kZXRhaWxzLmRlcGVuZHMudXNlX2NhY2hlLAogICAgICAgICAgICAgKQotICAgICAgICAgICAgaWYgaXNpbnN0YW5jZShwYXJhbV9kZXRhaWxzLmRlcGVuZHMuZGVwZW5kZW5jeSwgU2VjdXJpdHlCYXNlKToKLSAgICAgICAgICAgICAgICB1c2Vfc2NvcGVzOiBMaXN0W3N0cl0gPSBbXQotICAgICAgICAgICAgICAgIGlmIGlzaW5zdGFuY2UoCi0gICAgICAgICAgICAgICAgICAgIHBhcmFtX2RldGFpbHMuZGVwZW5kcy5kZXBlbmRlbmN5LCAoT0F1dGgyLCBPcGVuSWRDb25uZWN0KQotICAgICAgICAgICAgICAgICk6Ci0gICAgICAgICAgICAgICAgICAgIHVzZV9zY29wZXMgPSB1c2Vfc2VjdXJpdHlfc2NvcGVzCi0gICAgICAgICAgICAgICAgc2VjdXJpdHlfcmVxdWlyZW1lbnQgPSBTZWN1cml0eVJlcXVpcmVtZW50KAotICAgICAgICAgICAgICAgICAgICBzZWN1cml0eV9zY2hlbWU9cGFyYW1fZGV0YWlscy5kZXBlbmRzLmRlcGVuZGVuY3ksIHNjb3Blcz11c2Vfc2NvcGVzCi0gICAgICAgICAgICAgICAgKQotICAgICAgICAgICAgICAgIHN1Yl9kZXBlbmRhbnQuc2VjdXJpdHlfcmVxdWlyZW1lbnRzLmFwcGVuZChzZWN1cml0eV9yZXF1aXJlbWVudCkKICAgICAgICAgICAgIGRlcGVuZGFudC5kZXBlbmRlbmNpZXMuYXBwZW5kKHN1Yl9kZXBlbmRhbnQpCiAgICAgICAgICAgICBjb250aW51ZQogICAgICAgICBpZiBhZGRfbm9uX2ZpZWxkX3BhcmFtX3RvX2RlcGVuZGVuY3ko")
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
