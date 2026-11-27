# F2P PROBE (M654/M655): model-free. test-only apply -> pytest (expect FAIL), then +gold -> pytest (expect PASS).
# HEADERS-RECONSTRUCTED (mechanical, context verified vs base tree)
# pid=scrapy_s3b base=45417e6b0364. No model calls. Ends: TEST-RESULT lines in log.
import os, subprocess, urllib.request, base64
def sh(cmd, timeout=300):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")
PID = "scrapy_s3b"
REPO = "scrapy/scrapy"
BASE = "45417e6b0364"
PYTEST = "scrapy/tests/test_utils_deprecate.py"
KEXPR = "test_issubclass or test_isinstance"
SRCFILE = "scrapy/utils/deprecate.py"
IMPORTPKG = "scrapy"
PIPPKGS = "scrapy pytest pytest-timeout"
TESTDIFF = base64.b64decode("LS0tIGEvc2NyYXB5L3Rlc3RzL3Rlc3RfdXRpbHNfZGVwcmVjYXRlLnB5CisrKyBiL3NjcmFweS90ZXN0cy90ZXN0X3V0aWxzX2RlcHJlY2F0ZS5weQpAQCAtMTQ1LDYgKzE0NSw5IEBAIGNsYXNzIFVwZGF0ZWRVc2VyQ2xhc3MxYShOZXdOYW1lKToKICAgICAgICAgICAgIGNsYXNzIE91dGRhdGVkVXNlckNsYXNzMShEZXByZWNhdGVkTmFtZSk6CiAgICAgICAgICAgICAgICAgcGFzcwogCisgICAgICAgICAgICBjbGFzcyBPdXRkYXRlZFVzZXJDbGFzczFhKERlcHJlY2F0ZWROYW1lKToKKyAgICAgICAgICAgICAgICBwYXNzCisKICAgICAgICAgICAgIGNsYXNzIFVucmVsYXRlZENsYXNzKG9iamVjdCk6CiAgICAgICAgICAgICAgICAgcGFzcwogCkBAIC0xNTksNiArMTYyLDggQEAgY2xhc3MgT2xkU3R5bGVDbGFzczoKICAgICAgICAgYXNzZXJ0IG5vdCBpc3N1YmNsYXNzKFVucmVsYXRlZENsYXNzLCBEZXByZWNhdGVkTmFtZSkKICAgICAgICAgYXNzZXJ0IG5vdCBpc3N1YmNsYXNzKE9sZFN0eWxlQ2xhc3MsIERlcHJlY2F0ZWROYW1lKQogICAgICAgICBhc3NlcnQgbm90IGlzc3ViY2xhc3MoT2xkU3R5bGVDbGFzcywgRGVwcmVjYXRlZE5hbWUpCisgICAgICAgIGFzc2VydCBub3QgaXNzdWJjbGFzcyhPdXRkYXRlZFVzZXJDbGFzczEsIE91dGRhdGVkVXNlckNsYXNzMWEpCisgICAgICAgIGFzc2VydCBub3QgaXNzdWJjbGFzcyhPdXRkYXRlZFVzZXJDbGFzczFhLCBPdXRkYXRlZFVzZXJDbGFzczEpCiAKICAgICAgICAgc2VsZi5hc3NlcnRSYWlzZXMoVHlwZUVycm9yLCBpc3N1YmNsYXNzLCBvYmplY3QoKSwgRGVwcmVjYXRlZE5hbWUpCiAKQEAgLTE3NSw2ICsxODAsOSBAQCBjbGFzcyBVcGRhdGVkVXNlckNsYXNzMmEoTmV3TmFtZSk6CiAgICAgICAgICAgICBjbGFzcyBPdXRkYXRlZFVzZXJDbGFzczIoRGVwcmVjYXRlZE5hbWUpOgogICAgICAgICAgICAgICAgIHBhc3MKIAorICAgICAgICAgICAgY2xhc3MgT3V0ZGF0ZWRVc2VyQ2xhc3MyYShEZXByZWNhdGVkTmFtZSk6CisgICAgICAgICAgICAgICAgcGFzcworCiAgICAgICAgICAgICBjbGFzcyBVbnJlbGF0ZWRDbGFzcyhvYmplY3QpOgogICAgICAgICAgICAgICAgIHBhc3MKIApAQCAtMTg2LDYgKzE5NCw5IEBAIGNsYXNzIE9sZFN0eWxlQ2xhc3M6CiAgICAgICAgIGFzc2VydCBpc2luc3RhbmNlKFVwZGF0ZWRVc2VyQ2xhc3MyKCksIERlcHJlY2F0ZWROYW1lKQogICAgICAgICBhc3NlcnQgaXNpbnN0YW5jZShVcGRhdGVkVXNlckNsYXNzMmEoKSwgRGVwcmVjYXRlZE5hbWUpCiAgICAgICAgIGFzc2VydCBpc2luc3RhbmNlKE91dGRhdGVkVXNlckNsYXNzMigpLCBEZXByZWNhdGVkTmFtZSkKKyAgICAgICAgYXNzZXJ0IGlzaW5zdGFuY2UoT3V0ZGF0ZWRVc2VyQ2xhc3MyYSgpLCBEZXByZWNhdGVkTmFtZSkKKyAgICAgICAgYXNzZXJ0IG5vdCBpc2luc3RhbmNlKE91dGRhdGVkVXNlckNsYXNzMmEoKSwgT3V0ZGF0ZWRVc2VyQ2xhc3MyKQorICAgICAgICBhc3NlcnQgbm90IGlzaW5zdGFuY2UoT3V0ZGF0ZWRVc2VyQ2xhc3MyKCksIE91dGRhdGVkVXNlckNsYXNzMmEpCiAgICAgICAgIGFzc2VydCBub3QgaXNpbnN0YW5jZShVbnJlbGF0ZWRDbGFzcygpLCBEZXByZWNhdGVkTmFtZSkKICAgICAgICAgYXNzZXJ0IG5vdCBpc2luc3RhbmNlKE9sZFN0eWxlQ2xhc3MoKSwgRGVwcmVjYXRlZE5hbWUpCiA=").decode()
FIXDIFF = base64.b64decode("LS0tIGEvc2NyYXB5L3V0aWxzL2RlcHJlY2F0ZS5weQorKysgYi9zY3JhcHkvdXRpbHMvZGVwcmVjYXRlLnB5CkBAIC03OSwxMiArNzksMTggQEAgZGVmIF9faW5zdGFuY2VjaGVja19fKGNscywgaW5zdCk6CiAgICAgICAgICAgICAgICAgICAgICAgIGZvciBjIGluIHt0eXBlKGluc3QpLCBpbnN0Ll9fY2xhc3NfX30pCiAKICAgICAgICAgZGVmIF9fc3ViY2xhc3NjaGVja19fKGNscywgc3ViKToKKyAgICAgICAgICAgIGlmIGNscyBpcyBub3QgRGVwcmVjYXRlZENsYXNzLmRlcHJlY2F0ZWRfY2xhc3M6CisgICAgICAgICAgICAgICAgIyB3ZSBzaG91bGQgZG8gdGhlIG1hZ2ljIG9ubHkgaWYgc2Vjb25kIGBpc3N1YmNsYXNzYCBhcmd1bWVudAorICAgICAgICAgICAgICAgICMgaXMgdGhlIGRlcHJlY2F0ZWQgY2xhc3MgaXRzZWxmIC0gc3ViY2xhc3NlcyBvZiB0aGUKKyAgICAgICAgICAgICAgICAjIGRlcHJlY2F0ZWQgY2xhc3Mgc2hvdWxkIG5vdCB1c2UgY3VzdG9tIGBfX3N1YmNsYXNzY2hlY2tfX2AKKyAgICAgICAgICAgICAgICAjIG1ldGhvZC4KKyAgICAgICAgICAgICAgICByZXR1cm4gc3VwZXIoRGVwcmVjYXRlZENsYXNzLCBjbHMpLl9fc3ViY2xhc3NjaGVja19fKHN1YikKKwogICAgICAgICAgICAgaWYgbm90IGluc3BlY3QuaXNjbGFzcyhzdWIpOgogICAgICAgICAgICAgICAgIHJhaXNlIFR5cGVFcnJvcigiaXNzdWJjbGFzcygpIGFyZyAxIG11c3QgYmUgYSBjbGFzcyIpCiAKICAgICAgICAgICAgIG1ybyA9IGdldGF0dHIoc3ViLCAnX19tcm9fXycsICgpKQotICAgICAgICAgICAgY2FuZGlkYXRlcyA9IHtjbHMsIG5ld19jbGFzc30KLSAgICAgICAgICAgIHJldHVybiBhbnkoYyBpbiBjYW5kaWRhdGVzIGZvciBjIGluIG1ybykKKyAgICAgICAgICAgIHJldHVybiBhbnkoYyBpbiB7Y2xzLCBuZXdfY2xhc3N9IGZvciBjIGluIG1ybykKIAogICAgICAgICBkZWYgX19jYWxsX18oY2xzLCAqYXJncywgKiprd2FyZ3MpOgogICAgICAgICAgICAgb2xkID0gRGVwcmVjYXRlZENsYXNzLmRlcHJlY2F0ZWRfY2xhc3M=").decode()
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
open(work + "/test_patch.diff", "w").write(TESTDIFF)
trc, tout = sh("cd " + work + " && git apply test_patch.diff 2>&1; echo TEST_APPLIED_RC=$?", timeout=60)
print("TEST-APPLY " + PID + " " + tout[-200:], flush=True)
assert "TEST_APPLIED_RC=0" in tout, "test-apply-fail"
brc, bout = sh("cd " + work + " && " + pyenv + " python -m pytest " + PYTEST + " -k \"" + KEXPR + "\" -q --tb=line -p no:cacheprovider > basefail_out.txt 2>&1; echo BASE_RC=$?; tail -8 basefail_out.txt", timeout=600)
print("BASE-FAIL-PROOF " + PID + " " + bout[-600:], flush=True)
open(work + "/fix.diff", "w").write(FIXDIFF)
frc, fout = sh("cd " + work + " && git apply fix.diff 2>&1; echo FIX_APPLIED_RC=$?", timeout=60)
print("FIX-APPLY " + PID + " " + fout[-200:], flush=True)
assert "FIX_APPLIED_RC=0" in fout, "fix-apply-fail"
crc, cout = sh("cd " + work + " && python -m py_compile " + SRCFILE + " 2>&1; echo COMPILE_RC=$?", timeout=60)
print("COMPILE " + PID + " " + cout[-200:], flush=True)
trc2, tout2 = sh("cd " + work + " && " + pyenv + " python -m pytest " + PYTEST + " -k \"" + KEXPR + "\" -v --tb=short -p no:cacheprovider > pytest_out.txt 2>&1; echo PYTEST_RC=$?; tail -12 pytest_out.txt", timeout=600)
print("TEST-RESULT " + PID + " " + tout2[-800:], flush=True)
print("PROBE-DONE " + PID, flush=True)
