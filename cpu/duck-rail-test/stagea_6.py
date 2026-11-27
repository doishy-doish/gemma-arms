# F2P PROBE (M654/M655): model-free. test-only apply -> pytest (expect FAIL), then +gold -> pytest (expect PASS).
# pid=fastapi_15588 v6 (+NL test+gold norm + inline-snapshot. No model calls. Ends: TEST-RESULT lines in log.
import os, subprocess, urllib.request, base64, sys
import sys as _sys
if _sys.version_info[0] < 3:
    import os as _os; _os.execvp("python3", ["python3"] + _sys.argv)
assert _sys.version_info >= (3, 10), "need python3.10+, got " + _sys.version
print("PY-VERSION " + sys.version.replace(chr(10)," "), flush=True)
def sh(cmd, timeout=300):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")
PID = "fastapi_15588"
REPO = "fastapi/fastapi"
BASE = "cb83b83dcf78"
PYTEST = "tests/test_sse.py"
KEXPR = "test_server_sent_event_null_id_rejected or test_server_sent_event_single_line_fields_reject_newlines or test_server_sent_event_negative_retry_rejected"
SRCFILE = "fastapi/sse.py"
IMPORTPKG = "fastapi"
PIPPKGS = "fastapi pytest pytest-timeout requests python-multipart annotated-doc starlette==0.37.2 httpx==0.27.2 inline-snapshot"
TESTDIFF = base64.b64decode("LS0tIGEvdGVzdHMvdGVzdF9zc2UucHkKKysrIGIvdGVzdHMvdGVzdF9zc2UucHkKQEAgLTIyMSw2ICsyMjEsMTUgQEAgZGVmIHRlc3Rfc2VydmVyX3NlbnRfZXZlbnRfbnVsbF9pZF9yZWplY3RlZCgpOgogICAgICAgICBTZXJ2ZXJTZW50RXZlbnQoZGF0YT0idGVzdCIsIGlkPSJoYXNcMG51bGwiKQogCiAKK0BweXRlc3QubWFyay5wYXJhbWV0cml6ZSgiZmllbGRfbmFtZSIsIFsiZXZlbnQiLCAiaWQiXSkKK0BweXRlc3QubWFyay5wYXJhbWV0cml6ZSgidmFsdWUiLCBbImZpcnN0XG5zZWNvbmQiLCAiZmlyc3RccnNlY29uZCIsICJmaXJzdFxyXG5zZWNvbmQiXSkKK2RlZiB0ZXN0X3NlcnZlcl9zZW50X2V2ZW50X3NpbmdsZV9saW5lX2ZpZWxkc19yZWplY3RfbmV3bGluZXMoCisgICAgZmllbGRfbmFtZTogc3RyLCB2YWx1ZTogc3RyCispOgorICAgIHdpdGggcHl0ZXN0LnJhaXNlcyhWYWx1ZUVycm9yLCBtYXRjaD1mIlNTRSAne2ZpZWxkX25hbWV9JyBtdXN0IGJlIGEgc2luZ2xlIGxpbmUiKToKKyAgICAgICAgU2VydmVyU2VudEV2ZW50KGRhdGE9InRlc3QiLCAqKntmaWVsZF9uYW1lOiB2YWx1ZX0pCisKKwogZGVmIHRlc3Rfc2VydmVyX3NlbnRfZXZlbnRfbmVnYXRpdmVfcmV0cnlfcmVqZWN0ZWQoKToKICAgICB3aXRoIHB5dGVzdC5yYWlzZXMoVmFsdWVFcnJvcik6CiAgICAgICAgIFNlcnZlclNlbnRFdmVudChkYXRhPSJ0ZXN0IiwgcmV0cnk9LTEp")
FIXDIFF = base64.b64decode("LS0tIGEvZmFzdGFwaS9zc2UucHkKKysrIGIvZmFzdGFwaS9zc2UucHkKQEAgLTMzLDEwICszMywyMCBAQCBjbGFzcyBFdmVudFNvdXJjZVJlc3BvbnNlKFN0cmVhbWluZ1Jlc3BvbnNlKToKICAgICBtZWRpYV90eXBlID0gInRleHQvZXZlbnQtc3RyZWFtIgogCiAKLWRlZiBfY2hlY2tfaWRfbm9fbnVsbCh2OiBzdHIgfCBOb25lKSAtPiBzdHIgfCBOb25lOgorZGVmIF9jaGVja19zaW5nbGVfbGluZSh2OiBzdHIgfCBOb25lLCBmaWVsZF9uYW1lOiBzdHIpIC0+IHN0ciB8IE5vbmU6CisgICAgaWYgdiBpcyBub3QgTm9uZSBhbmQgKCJcciIgaW4gdiBvciAiXG4iIGluIHYpOgorICAgICAgICByYWlzZSBWYWx1ZUVycm9yKGYiU1NFICd7ZmllbGRfbmFtZX0nIG11c3QgYmUgYSBzaW5nbGUgbGluZSIpCisgICAgcmV0dXJuIHYKKworCitkZWYgX2NoZWNrX2V2ZW50X3NpbmdsZV9saW5lKHY6IHN0ciB8IE5vbmUpIC0+IHN0ciB8IE5vbmU6CisgICAgcmV0dXJuIF9jaGVja19zaW5nbGVfbGluZSh2LCAiZXZlbnQiKQorCisKK2RlZiBfY2hlY2tfaWRfdmFsaWQodjogc3RyIHwgTm9uZSkgLT4gc3RyIHwgTm9uZToKICAgICBpZiB2IGlzIG5vdCBOb25lIGFuZCAiXDAiIGluIHY6CiAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoIlNTRSAnaWQnIG11c3Qgbm90IGNvbnRhaW4gbnVsbCBjaGFyYWN0ZXJzIikKLSAgICByZXR1cm4gdgorICAgIHJldHVybiBfY2hlY2tfc2luZ2xlX2xpbmUodiwgImlkIikKIAogCiBjbGFzcyBTZXJ2ZXJTZW50RXZlbnQoQmFzZU1vZGVsKToKQEAgLTg2LDI0ICs5NiwyNyBAQCBjbGFzcyBTZXJ2ZXJTZW50RXZlbnQoQmFzZU1vZGVsKToKICAgICBdID0gTm9uZQogICAgIGV2ZW50OiBBbm5vdGF0ZWRbCiAgICAgICAgIHN0ciB8IE5vbmUsCisgICAgICAgIEFmdGVyVmFsaWRhdG9yKF9jaGVja19ldmVudF9zaW5nbGVfbGluZSksCiAgICAgICAgIERvYygKICAgICAgICAgICAgICIiIgogICAgICAgICAgICAgT3B0aW9uYWwgZXZlbnQgdHlwZSBuYW1lLgogCiAgICAgICAgICAgICBNYXBzIHRvIGBhZGRFdmVudExpc3RlbmVyKGV2ZW50LCAuLi4pYCBvbiB0aGUgYnJvd3Nlci4gV2hlbiBvbWl0dGVkLAotICAgICAgICAgICAgdGhlIGJyb3dzZXIgZGlzcGF0Y2hlcyBvbiB0aGUgZ2VuZXJpYyBgbWVzc2FnZWAgZXZlbnQuCisgICAgICAgICAgICB0aGUgYnJvd3NlciBkaXNwYXRjaGVzIG9uIHRoZSBnZW5lcmljIGBtZXNzYWdlYCBldmVudC4gTXVzdCBiZSBhCisgICAgICAgICAgICBzaW5nbGUgbGluZS4KICAgICAgICAgICAgICIiIgogICAgICAgICApLAogICAgIF0gPSBOb25lCiAgICAgaWQ6IEFubm90YXRlZFsKICAgICAgICAgc3RyIHwgTm9uZSwKLSAgICAgICAgQWZ0ZXJWYWxpZGF0b3IoX2NoZWNrX2lkX25vX251bGwpLAorICAgICAgICBBZnRlclZhbGlkYXRvcihfY2hlY2tfaWRfdmFsaWQpLAogICAgICAgICBEb2MoCiAgICAgICAgICAgICAiIiIKICAgICAgICAgICAgIE9wdGlvbmFsIGV2ZW50IElELgogCiAgICAgICAgICAgICBUaGUgYnJvd3NlciBzZW5kcyB0aGlzIHZhbHVlIGJhY2sgYXMgdGhlIGBMYXN0LUV2ZW50LUlEYCBoZWFkZXIgb24KLSAgICAgICAgICAgIGF1dG9tYXRpYyByZWNvbm5lY3Rpb24uICoqTXVzdCBub3QgY29udGFpbiBudWxsIChgXFwwYCkgY2hhcmFjdGVycy4qKgorICAgICAgICAgICAgYXV0b21hdGljIHJlY29ubmVjdGlvbi4gKipNdXN0IGJlIGEgc2luZ2xlIGxpbmUqKiBhbmQgbXVzdCBub3QgY29udGFpbgorICAgICAgICAgICAgbnVsbCAoYFxcMGApIGNoYXJhY3RlcnMuCiAgICAgICAgICAgICAiIiIKICAgICAgICAgKSwKICAgICBdID0gTm9uZQ==")
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
