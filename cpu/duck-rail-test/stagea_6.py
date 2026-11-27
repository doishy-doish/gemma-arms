# F2P PROBE (M654/M655): model-free. test-only apply -> pytest (expect FAIL), then +gold -> pytest (expect PASS).
# pid=fastapi_14430 v6 (+NL test+gold norm + inline-snapshot. No model calls. Ends: TEST-RESULT lines in log.
import os, subprocess, urllib.request, base64, sys
import sys as _sys
if _sys.version_info[0] < 3:
    import os as _os; _os.execvp("python3", ["python3"] + _sys.argv)
assert _sys.version_info >= (3, 10), "need python3.10+, got " + _sys.version
print("PY-VERSION " + sys.version.replace(chr(10)," "), flush=True)
def sh(cmd, timeout=300):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")
PID = "fastapi_14430"
REPO = "fastapi/fastapi"
BASE = "cff2236dacb7"
PYTEST = "tests/test_compat.py"
KEXPR = "test_serialize_sequence_value_with_optional_list or test_serialize_sequence_value_with_optional_list_pipe_union or test_serialize_sequence_value_with_none_first_in_union"
SRCFILE = "fastapi/_compat/v2.py"
IMPORTPKG = "fastapi"
PIPPKGS = "fastapi pytest pytest-timeout requests python-multipart annotated-doc starlette==0.37.2 httpx==0.27.2 inline-snapshot"
TESTDIFF = base64.b64decode("LS0tIGEvdGVzdHMvdGVzdF9jb21wYXQucHkKKysrIGIvdGVzdHMvdGVzdF9jb21wYXQucHkKQEAgLTE0LDcgKzE0LDcgQEAKIGZyb20gcHlkYW50aWMgaW1wb3J0IEJhc2VNb2RlbCwgQ29uZmlnRGljdAogZnJvbSBweWRhbnRpYy5maWVsZHMgaW1wb3J0IEZpZWxkSW5mbwogCi1mcm9tIC51dGlscyBpbXBvcnQgbmVlZHNfcHlfbHRfMzE0LCBuZWVkc19weWRhbnRpY3YyCitmcm9tIC51dGlscyBpbXBvcnQgbmVlZHNfcHkzMTAsIG5lZWRzX3B5X2x0XzMxNCwgbmVlZHNfcHlkYW50aWN2MgogCiAKIEBuZWVkc19weWRhbnRpY3YyCkBAIC0xNDgsNiArMTQ4LDE5IEBAIGRlZiB0ZXN0X3NlcmlhbGl6ZV9zZXF1ZW5jZV92YWx1ZV93aXRoX29wdGlvbmFsX2xpc3QoKToKICAgICBhc3NlcnQgaXNpbnN0YW5jZShyZXN1bHQsIGxpc3QpCiAKIAorQG5lZWRzX3B5ZGFudGljdjIKK0BuZWVkc19weTMxMAorZGVmIHRlc3Rfc2VyaWFsaXplX3NlcXVlbmNlX3ZhbHVlX3dpdGhfb3B0aW9uYWxfbGlzdF9waXBlX3VuaW9uKCk6CisgICAgIiIiVGVzdCB0aGF0IHNlcmlhbGl6ZV9zZXF1ZW5jZV92YWx1ZSBoYW5kbGVzIG9wdGlvbmFsIGxpc3RzIGNvcnJlY3RseSAod2l0aCBuZXcgc3ludGF4KS4iIiIKKyAgICBmcm9tIGZhc3RhcGkuX2NvbXBhdCBpbXBvcnQgdjIKKworICAgIGZpZWxkX2luZm8gPSBGaWVsZEluZm8oYW5ub3RhdGlvbj1saXN0W3N0cl0gfCBOb25lKQorICAgIGZpZWxkID0gdjIuTW9kZWxGaWVsZChuYW1lPSJpdGVtcyIsIGZpZWxkX2luZm89ZmllbGRfaW5mbykKKyAgICByZXN1bHQgPSB2Mi5zZXJpYWxpemVfc2VxdWVuY2VfdmFsdWUoZmllbGQ9ZmllbGQsIHZhbHVlPVsiYSIsICJiIiwgImMiXSkKKyAgICBhc3NlcnQgcmVzdWx0ID09IFsiYSIsICJiIiwgImMiXQorICAgIGFzc2VydCBpc2luc3RhbmNlKHJlc3VsdCwgbGlzdCkKKworCiBAbmVlZHNfcHlkYW50aWN2MgogZGVmIHRlc3Rfc2VyaWFsaXplX3NlcXVlbmNlX3ZhbHVlX3dpdGhfbm9uZV9maXJzdF9pbl91bmlvbigpOgogICAgICIiIlRlc3QgdGhhdCBzZXJpYWxpemVfc2VxdWVuY2VfdmFsdWUgaGFuZGxlcyBVbmlvbltOb25lLCBMaXN0Wy4uLl1dIGNvcnJlY3RseS4iIiI=")
FIXDIFF = base64.b64decode("LS0tIGEvZmFzdGFwaS9fY29tcGF0L3YyLnB5CisrKyBiL2Zhc3RhcGkvX2NvbXBhdC92Mi5weQpAQCAtMTcsNyArMTcsNyBAQAogCiBmcm9tIGZhc3RhcGkuX2NvbXBhdCBpbXBvcnQgbWF5X3YxLCBzaGFyZWQKIGZyb20gZmFzdGFwaS5vcGVuYXBpLmNvbnN0YW50cyBpbXBvcnQgUkVGX1RFTVBMQVRFCi1mcm9tIGZhc3RhcGkudHlwZXMgaW1wb3J0IEluY0V4LCBNb2RlbE5hbWVNYXAKK2Zyb20gZmFzdGFwaS50eXBlcyBpbXBvcnQgSW5jRXgsIE1vZGVsTmFtZU1hcCwgVW5pb25UeXBlCiBmcm9tIHB5ZGFudGljIGltcG9ydCBCYXNlTW9kZWwsIFR5cGVBZGFwdGVyLCBjcmVhdGVfbW9kZWwKIGZyb20gcHlkYW50aWMgaW1wb3J0IFB5ZGFudGljU2NoZW1hR2VuZXJhdGlvbkVycm9yIGFzIFB5ZGFudGljU2NoZW1hR2VuZXJhdGlvbkVycm9yCiBmcm9tIHB5ZGFudGljIGltcG9ydCBQeWRhbnRpY1VuZGVmaW5lZEFubm90YXRpb24gYXMgUHlkYW50aWNVbmRlZmluZWRBbm5vdGF0aW9uCkBAIC0zODEsNyArMzgxLDcgQEAgZGVmIGNvcHlfZmllbGRfaW5mbygqLCBmaWVsZF9pbmZvOiBGaWVsZEluZm8sIGFubm90YXRpb246IEFueSkgLT4gRmllbGRJbmZvOgogCiBkZWYgc2VyaWFsaXplX3NlcXVlbmNlX3ZhbHVlKCosIGZpZWxkOiBNb2RlbEZpZWxkLCB2YWx1ZTogQW55KSAtPiBTZXF1ZW5jZVtBbnldOgogICAgIG9yaWdpbl90eXBlID0gZ2V0X29yaWdpbihmaWVsZC5maWVsZF9pbmZvLmFubm90YXRpb24pIG9yIGZpZWxkLmZpZWxkX2luZm8uYW5ub3RhdGlvbgotICAgIGlmIG9yaWdpbl90eXBlIGlzIFVuaW9uOiAgIyBIYW5kbGUgb3B0aW9uYWwgc2VxdWVuY2VzCisgICAgaWYgb3JpZ2luX3R5cGUgaXMgVW5pb24gb3Igb3JpZ2luX3R5cGUgaXMgVW5pb25UeXBlOiAgIyBIYW5kbGUgb3B0aW9uYWwgc2VxdWVuY2VzCiAgICAgICAgIHVuaW9uX2FyZ3MgPSBnZXRfYXJncyhmaWVsZC5maWVsZF9pbmZvLmFubm90YXRpb24pCiAgICAgICAgIGZvciB1bmlvbl9hcmcgaW4gdW5pb25fYXJnczoKICAgICAgICAgICAgIGlmIHVuaW9uX2FyZyBpcyB0eXBlKE5vbmUpOg==")
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
