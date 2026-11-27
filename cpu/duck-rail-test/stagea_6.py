# F2P PROBE (M654/M655): model-free. test-only apply -> pytest (expect FAIL), then +gold -> pytest (expect PASS).
# pid=fastapi_14873 base=cd31576d5704. No model calls. Ends: TEST-RESULT lines in log.
import os, subprocess, urllib.request, base64
def sh(cmd, timeout=300):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")
PID = "fastapi_14873"
REPO = "fastapi/fastapi"
BASE = "cd31576d5704"
PYTEST = "tests/test_router_events.py"
KEXPR = "test_startup_shutdown_handlers_as_parameters"
SRCFILE = "fastapi/routing.py"
IMPORTPKG = "fastapi"
PIPPKGS = "fastapi pytest pytest-timeout requests python-multipart annotated-doc starlette==0.37.2 httpx==0.27.2"
TESTDIFF = base64.b64decode("LS0tIGEvdGVzdHMvdGVzdF9yb3V0ZXJfZXZlbnRzLnB5CisrKyBiL3Rlc3RzL3Rlc3Rfcm91dGVyX2V2ZW50cy5weQpAQCAtMzE3LDMgKzMxNyw2MyBAQCBkZWYgbWFpbigpIC0+IGRpY3Rbc3RyLCBzdHJdOgogICAgICAgICBhc3NlcnQgcmVzcG9uc2UuanNvbigpID09IHsibWVzc2FnZSI6ICJIZWxsbyBXb3JsZCJ9CiAgICAgYXNzZXJ0IHN0YXRlLmFwcF9zdGFydHVwIGlzIFRydWUKICAgICBhc3NlcnQgc3RhdGUuYXBwX3NodXRkb3duIGlzIFRydWUKKworCitkZWYgdGVzdF9zdGFydHVwX3NodXRkb3duX2hhbmRsZXJzX2FzX3BhcmFtZXRlcnMoc3RhdGU6IFN0YXRlKSAtPiBOb25lOgorICAgICIiIlRlc3QgdGhhdCBzdGFydHVwL3NodXRkb3duIGhhbmRsZXJzIHBhc3NlZCBhcyBwYXJhbWV0ZXJzIHRvIEZhc3RBUEkgYXJlIGNhbGxlZCBjb3JyZWN0bHkuIiIiCisKKyAgICBkZWYgYXBwX3N0YXJ0dXAoKSAtPiBOb25lOgorICAgICAgICBzdGF0ZS5hcHBfc3RhcnR1cCA9IFRydWUKKworICAgIGRlZiBhcHBfc2h1dGRvd24oKSAtPiBOb25lOgorICAgICAgICBzdGF0ZS5hcHBfc2h1dGRvd24gPSBUcnVlCisKKyAgICBhcHAgPSBGYXN0QVBJKG9uX3N0YXJ0dXA9W2FwcF9zdGFydHVwXSwgb25fc2h1dGRvd249W2FwcF9zaHV0ZG93bl0pCisKKyAgICBAYXBwLmdldCgiLyIpCisgICAgZGVmIG1haW4oKSAtPiBkaWN0W3N0ciwgc3RyXToKKyAgICAgICAgcmV0dXJuIHsibWVzc2FnZSI6ICJIZWxsbyBXb3JsZCJ9CisKKyAgICBkZWYgcm91dGVyX3N0YXJ0dXAoKSAtPiBOb25lOgorICAgICAgICBzdGF0ZS5yb3V0ZXJfc3RhcnR1cCA9IFRydWUKKworICAgIGRlZiByb3V0ZXJfc2h1dGRvd24oKSAtPiBOb25lOgorICAgICAgICBzdGF0ZS5yb3V0ZXJfc2h1dGRvd24gPSBUcnVlCisKKyAgICByb3V0ZXIgPSBBUElSb3V0ZXIob25fc3RhcnR1cD1bcm91dGVyX3N0YXJ0dXBdLCBvbl9zaHV0ZG93bj1bcm91dGVyX3NodXRkb3duXSkKKworICAgIGRlZiBzdWJfcm91dGVyX3N0YXJ0dXAoKSAtPiBOb25lOgorICAgICAgICBzdGF0ZS5zdWJfcm91dGVyX3N0YXJ0dXAgPSBUcnVlCisKKyAgICBkZWYgc3ViX3JvdXRlcl9zaHV0ZG93bigpIC0+IE5vbmU6CisgICAgICAgIHN0YXRlLnN1Yl9yb3V0ZXJfc2h1dGRvd24gPSBUcnVlCisKKyAgICBzdWJfcm91dGVyID0gQVBJUm91dGVyKAorICAgICAgICBvbl9zdGFydHVwPVtzdWJfcm91dGVyX3N0YXJ0dXBdLCBvbl9zaHV0ZG93bj1bc3ViX3JvdXRlcl9zaHV0ZG93bl0KKyAgICApCisKKyAgICByb3V0ZXIuaW5jbHVkZV9yb3V0ZXIoc3ViX3JvdXRlcikKKyAgICBhcHAuaW5jbHVkZV9yb3V0ZXIocm91dGVyKQorCisgICAgYXNzZXJ0IHN0YXRlLmFwcF9zdGFydHVwIGlzIEZhbHNlCisgICAgYXNzZXJ0IHN0YXRlLnJvdXRlcl9zdGFydHVwIGlzIEZhbHNlCisgICAgYXNzZXJ0IHN0YXRlLnN1Yl9yb3V0ZXJfc3RhcnR1cCBpcyBGYWxzZQorICAgIGFzc2VydCBzdGF0ZS5hcHBfc2h1dGRvd24gaXMgRmFsc2UKKyAgICBhc3NlcnQgc3RhdGUucm91dGVyX3NodXRkb3duIGlzIEZhbHNlCisgICAgYXNzZXJ0IHN0YXRlLnN1Yl9yb3V0ZXJfc2h1dGRvd24gaXMgRmFsc2UKKyAgICB3aXRoIFRlc3RDbGllbnQoYXBwKSBhcyBjbGllbnQ6CisgICAgICAgIGFzc2VydCBzdGF0ZS5hcHBfc3RhcnR1cCBpcyBUcnVlCisgICAgICAgIGFzc2VydCBzdGF0ZS5yb3V0ZXJfc3RhcnR1cCBpcyBUcnVlCisgICAgICAgIGFzc2VydCBzdGF0ZS5zdWJfcm91dGVyX3N0YXJ0dXAgaXMgVHJ1ZQorICAgICAgICBhc3NlcnQgc3RhdGUuYXBwX3NodXRkb3duIGlzIEZhbHNlCisgICAgICAgIGFzc2VydCBzdGF0ZS5yb3V0ZXJfc2h1dGRvd24gaXMgRmFsc2UKKyAgICAgICAgYXNzZXJ0IHN0YXRlLnN1Yl9yb3V0ZXJfc2h1dGRvd24gaXMgRmFsc2UKKyAgICAgICAgcmVzcG9uc2UgPSBjbGllbnQuZ2V0KCIvIikKKyAgICAgICAgYXNzZXJ0IHJlc3BvbnNlLnN0YXR1c19jb2RlID09IDIwMCwgcmVzcG9uc2UudGV4dAorICAgICAgICBhc3NlcnQgcmVzcG9uc2UuanNvbigpID09IHsibWVzc2FnZSI6ICJIZWxsbyBXb3JsZCJ9CisgICAgYXNzZXJ0IHN0YXRlLmFwcF9zdGFydHVwIGlzIFRydWUKKyAgICBhc3NlcnQgc3RhdGUucm91dGVyX3N0YXJ0dXAgaXMgVHJ1ZQorICAgIGFzc2VydCBzdGF0ZS5zdWJfcm91dGVyX3N0YXJ0dXAgaXMgVHJ1ZQorICAgIGFzc2VydCBzdGF0ZS5hcHBfc2h1dGRvd24gaXMgVHJ1ZQorICAgIGFzc2VydCBzdGF0ZS5yb3V0ZXJfc2h1dGRvd24gaXMgVHJ1ZQorICAgIGFzc2VydCBzdGF0ZS5zdWJfcm91dGVyX3NodXRkb3duIGlzIFRydWUK").decode()
FIXDIFF = base64.b64decode("LS0tIGEvZmFzdGFwaS9yb3V0aW5nLnB5CisrKyBiL2Zhc3RhcGkvcm91dGluZy5weQpAQCAtOTUyLDE2ICs5NTIsNiBAQCBkZWYgX19pbml0X18oCiAgICAgICAgICAgICApLAogICAgICAgICBdID0gRGVmYXVsdChnZW5lcmF0ZV91bmlxdWVfaWQpLAogICAgICkgLT4gTm9uZToKLSAgICAgICAgIyBIYW5kbGUgb25fc3RhcnR1cC9vbl9zaHV0ZG93biBsb2NhbGx5IHNpbmNlIFN0YXJsZXR0ZSByZW1vdmVkIHN1cHBvcnQKLSAgICAgICAgIyBSZWY6IGh0dHBzOi8vZ2l0aHViLmNvbS9LbHVkZXgvc3RhcmxldHRlL3B1bGwvMzExNwotICAgICAgICAjIFRPRE86IGRlcHJlY2F0ZSB0aGlzIG9uY2UgdGhlIGxpZmVzcGFuIChvciBhbHRlcm5hdGl2ZSkgaW50ZXJmYWNlIGlzIGltcHJvdmVkCi0gICAgICAgIHNlbGYub25fc3RhcnR1cDogbGlzdFtDYWxsYWJsZVtbXSwgQW55XV0gPSAoCi0gICAgICAgICAgICBbXSBpZiBvbl9zdGFydHVwIGlzIE5vbmUgZWxzZSBsaXN0KG9uX3N0YXJ0dXApCi0gICAgICAgICkKLSAgICAgICAgc2VsZi5vbl9zaHV0ZG93bjogbGlzdFtDYWxsYWJsZVtbXSwgQW55XV0gPSAoCi0gICAgICAgICAgICBbXSBpZiBvbl9zaHV0ZG93biBpcyBOb25lIGVsc2UgbGlzdChvbl9zaHV0ZG93bikKLSAgICAgICAgKQotCiAgICAgICAgICMgRGV0ZXJtaW5lIHRoZSBsaWZlc3BhbiBjb250ZXh0IHRvIHVzZQogICAgICAgICBpZiBsaWZlc3BhbiBpcyBOb25lOgogICAgICAgICAgICAgIyBVc2UgdGhlIGRlZmF1bHQgbGlmZXNwYW4gdGhhdCBydW5zIG9uX3N0YXJ0dXAvb25fc2h1dGRvd24gaGFuZGxlcnMKQEAgLTk4NSw2ICs5NzUsMTcgQEAgZGVmIF9faW5pdF9fKAogICAgICAgICAgICAgYXNzZXJ0IG5vdCBwcmVmaXguZW5kc3dpdGgoIi8iKSwgKAogICAgICAgICAgICAgICAgICJBIHBhdGggcHJlZml4IG11c3Qgbm90IGVuZCB3aXRoICcvJywgYXMgdGhlIHJvdXRlcyB3aWxsIHN0YXJ0IHdpdGggJy8nIgogICAgICAgICAgICAgKQorCisgICAgICAgICMgSGFuZGxlIG9uX3N0YXJ0dXAvb25fc2h1dGRvd24gbG9jYWxseSBzaW5jZSBTdGFybGV0dGUgcmVtb3ZlZCBzdXBwb3J0CisgICAgICAgICMgUmVmOiBodHRwczovL2dpdGh1Yi5jb20vS2x1ZGV4L3N0YXJsZXR0ZS9wdWxsLzMxMTcKKyAgICAgICAgIyBUT0RPOiBkZXByZWNhdGUgdGhpcyBvbmNlIHRoZSBsaWZlc3BhbiAob3IgYWx0ZXJuYXRpdmUpIGludGVyZmFjZSBpcyBpbXByb3ZlZAorICAgICAgICBzZWxmLm9uX3N0YXJ0dXA6IGxpc3RbQ2FsbGFibGVbW10sIEFueV1dID0gKAorICAgICAgICAgICAgW10gaWYgb25fc3RhcnR1cCBpcyBOb25lIGVsc2UgbGlzdChvbl9zdGFydHVwKQorICAgICAgICApCisgICAgICAgIHNlbGYub25fc2h1dGRvd246IGxpc3RbQ2FsbGFibGVbW10sIEFueV1dID0gKAorICAgICAgICAgICAgW10gaWYgb25fc2h1dGRvd24gaXMgTm9uZSBlbHNlIGxpc3Qob25fc2h1dGRvd24pCisgICAgICAgICkKKwogICAgICAgICBzZWxmLnByZWZpeCA9IHByZWZpeAogICAgICAgICBzZWxmLnRhZ3M6IGxpc3RbVW5pb25bc3RyLCBFbnVtXV0gPSB0YWdzIG9yIFtdCiAgICAgICAgIHNlbGYuZGVwZW5kZW5jaWVzID0gbGlzdChkZXBlbmRlbmNpZXMgb3IgW10pCg==").decode()
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
brc, bout = sh("cd " + work + " && " + pyenv + " python -m pytest " + PYTEST + " -k \"" + KEXPR + "\" -q --tb=line -W ignore::PendingDeprecationWarning -W ignore::DeprecationWarning -p no:cacheprovider -p no:unraisableexception > basefail_out.txt 2>&1; echo BASE_RC=$?; tail -8 basefail_out.txt", timeout=600)
print("BASE-FAIL-PROOF " + PID + " " + bout[-600:], flush=True)
sbrc, sbout = sh("grep -aE \"passed|failed|error\" " + work + "/basefail_out.txt | tail -4; echo BASE_RC=" + str(brc), timeout=30)
print("BASE-SUMMARY " + PID + " " + sbout[-300:], flush=True)
open(work + "/fix.diff", "w").write(FIXDIFF)
frc, fout = sh("cd " + work + " && git apply fix.diff 2>&1; echo FIX_APPLIED_RC=$?", timeout=60)
print("FIX-APPLY " + PID + " " + fout[-200:], flush=True)
assert "FIX_APPLIED_RC=0" in fout, "fix-apply-fail"
crc, cout = sh("cd " + work + " && python -m py_compile " + SRCFILE + " 2>&1; echo COMPILE_RC=$?", timeout=60)
print("COMPILE " + PID + " " + cout[-200:], flush=True)
trc2, tout2 = sh("cd " + work + " && " + pyenv + " python -m pytest " + PYTEST + " -k \"" + KEXPR + "\" -v --tb=short -W ignore::PendingDeprecationWarning -W ignore::DeprecationWarning -p no:cacheprovider -p no:unraisableexception > pytest_out.txt 2>&1; echo PYTEST_RC=$?; tail -12 pytest_out.txt", timeout=600)
print("TEST-RESULT " + PID + " " + tout2[-800:], flush=True)
assert "PYTEST_RC=0" in tout2, "gold-does-not-pass"
print("PROBE-DONE " + PID, flush=True)
