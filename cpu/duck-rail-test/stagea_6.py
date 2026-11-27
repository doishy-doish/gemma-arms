# F2P PROBE (M654/M655): model-free. test-only apply -> pytest (expect FAIL), then +gold -> pytest (expect PASS).
# pid=fastapi_14485 base=60699f306b67 v5 (+NL test+gold norm. No model calls. Ends: TEST-RESULT lines in log.
import os, subprocess, urllib.request, base64, sys
import sys as _sys
if _sys.version_info[0] < 3:
    import os as _os; _os.execvp("python3", ["python3"] + _sys.argv)
assert _sys.version_info >= (3, 10), "need python3.10+, got " + _sys.version
print("PY-VERSION " + sys.version.replace(chr(10)," "), flush=True)
def sh(cmd, timeout=300):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")
PID = "fastapi_14485"
REPO = "fastapi/fastapi"
BASE = "60699f306b67"
PYTEST = "tests/test_stringified_annotation_dependency.py"
KEXPR = "test_get or test_openapi_schema"
SRCFILE = "fastapi/dependencies/utils.py"
IMPORTPKG = "fastapi"
PIPPKGS = "fastapi pytest pytest-timeout requests python-multipart annotated-doc starlette==0.37.2 httpx==0.27.2"
TESTDIFF = base64.b64decode("LS0tIGEvdGVzdHMvdGVzdF9zdHJpbmdpZmllZF9hbm5vdGF0aW9uX2RlcGVuZGVuY3kucHkKKysrIGIvdGVzdHMvdGVzdF9zdHJpbmdpZmllZF9hbm5vdGF0aW9uX2RlcGVuZGVuY3kucHkKQEAgLTAsMCArMSw4MCBAQAorZnJvbSBfX2Z1dHVyZV9fIGltcG9ydCBhbm5vdGF0aW9ucworCitmcm9tIHR5cGluZyBpbXBvcnQgVFlQRV9DSEVDS0lORworCitpbXBvcnQgcHl0ZXN0Citmcm9tIGZhc3RhcGkgaW1wb3J0IERlcGVuZHMsIEZhc3RBUEkKK2Zyb20gZmFzdGFwaS50ZXN0Y2xpZW50IGltcG9ydCBUZXN0Q2xpZW50Citmcm9tIGlubGluZV9zbmFwc2hvdCBpbXBvcnQgc25hcHNob3QKK2Zyb20gdHlwaW5nX2V4dGVuc2lvbnMgaW1wb3J0IEFubm90YXRlZAorCitpZiBUWVBFX0NIRUNLSU5HOiAgIyBwcmFnbWE6IG5vIGNvdmVyCisgICAgZnJvbSBjb2xsZWN0aW9ucy5hYmMgaW1wb3J0IEFzeW5jR2VuZXJhdG9yCisKKworY2xhc3MgRHVtbXlDbGllbnQ6CisgICAgYXN5bmMgZGVmIGdldF9wZW9wbGUoc2VsZikgLT4gbGlzdDoKKyAgICAgICAgcmV0dXJuIFsiSm9obiBEb2UiLCAiSmFuZSBEb2UiXQorCisgICAgYXN5bmMgZGVmIGNsb3NlKHNlbGYpIC0+IE5vbmU6CisgICAgICAgIHBhc3MKKworCithc3luYyBkZWYgZ2V0X2NsaWVudCgpIC0+IEFzeW5jR2VuZXJhdG9yW0R1bW15Q2xpZW50LCBOb25lXToKKyAgICBjbGllbnQgPSBEdW1teUNsaWVudCgpCisgICAgeWllbGQgY2xpZW50CisgICAgYXdhaXQgY2xpZW50LmNsb3NlKCkKKworCitDbGllbnQgPSBBbm5vdGF0ZWRbRHVtbXlDbGllbnQsIERlcGVuZHMoZ2V0X2NsaWVudCldCisKKworQHB5dGVzdC5maXh0dXJlKG5hbWU9ImNsaWVudCIpCitkZWYgY2xpZW50X2ZpeHR1cmUoKSAtPiBUZXN0Q2xpZW50OgorICAgIGFwcCA9IEZhc3RBUEkoKQorCisgICAgQGFwcC5nZXQoIi8iKQorICAgIGFzeW5jIGRlZiBnZXRfcGVvcGxlKGNsaWVudDogQ2xpZW50KSAtPiBsaXN0OgorICAgICAgICByZXR1cm4gYXdhaXQgY2xpZW50LmdldF9wZW9wbGUoKQorCisgICAgY2xpZW50ID0gVGVzdENsaWVudChhcHApCisgICAgcmV0dXJuIGNsaWVudAorCisKK2RlZiB0ZXN0X2dldChjbGllbnQ6IFRlc3RDbGllbnQpOgorICAgIHJlc3BvbnNlID0gY2xpZW50LmdldCgiLyIpCisgICAgYXNzZXJ0IHJlc3BvbnNlLnN0YXR1c19jb2RlID09IDIwMCwgcmVzcG9uc2UudGV4dAorICAgIGFzc2VydCByZXNwb25zZS5qc29uKCkgPT0gWyJKb2huIERvZSIsICJKYW5lIERvZSJdCisKKworZGVmIHRlc3Rfb3BlbmFwaV9zY2hlbWEoY2xpZW50OiBUZXN0Q2xpZW50KToKKyAgICByZXNwb25zZSA9IGNsaWVudC5nZXQoIi9vcGVuYXBpLmpzb24iKQorICAgIGFzc2VydCByZXNwb25zZS5zdGF0dXNfY29kZSA9PSAyMDAsIHJlc3BvbnNlLnRleHQKKyAgICBhc3NlcnQgcmVzcG9uc2UuanNvbigpID09IHNuYXBzaG90KAorICAgICAgICB7CisgICAgICAgICAgICAib3BlbmFwaSI6ICIzLjEuMCIsCisgICAgICAgICAgICAiaW5mbyI6IHsidGl0bGUiOiAiRmFzdEFQSSIsICJ2ZXJzaW9uIjogIjAuMS4wIn0sCisgICAgICAgICAgICAicGF0aHMiOiB7CisgICAgICAgICAgICAgICAgIi8iOiB7CisgICAgICAgICAgICAgICAgICAgICJnZXQiOiB7CisgICAgICAgICAgICAgICAgICAgICAgICAic3VtbWFyeSI6ICJHZXQgUGVvcGxlIiwKKyAgICAgICAgICAgICAgICAgICAgICAgICJvcGVyYXRpb25JZCI6ICJnZXRfcGVvcGxlX19nZXQiLAorICAgICAgICAgICAgICAgICAgICAgICAgInJlc3BvbnNlcyI6IHsKKyAgICAgICAgICAgICAgICAgICAgICAgICAgICAiMjAwIjogeworICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAiZGVzY3JpcHRpb24iOiAiU3VjY2Vzc2Z1bCBSZXNwb25zZSIsCisgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICJjb250ZW50IjogeworICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgImFwcGxpY2F0aW9uL2pzb24iOiB7CisgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgInNjaGVtYSI6IHsKKyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIml0ZW1zIjoge30sCisgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICJ0eXBlIjogImFycmF5IiwKKyAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgInRpdGxlIjogIlJlc3BvbnNlIEdldCBQZW9wbGUgIEdldCIsCisgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgfQorICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgfQorICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB9LAorICAgICAgICAgICAgICAgICAgICAgICAgICAgIH0KKyAgICAgICAgICAgICAgICAgICAgICAgIH0sCisgICAgICAgICAgICAgICAgICAgIH0KKyAgICAgICAgICAgICAgICB9CisgICAgICAgICAgICB9LAorICAgICAgICB9CisgICAgKQ==")
FIXDIFF = base64.b64decode("LS0tIGEvZmFzdGFwaS9kZXBlbmRlbmNpZXMvdXRpbHMucHkKKysrIGIvZmFzdGFwaS9kZXBlbmRlbmNpZXMvdXRpbHMucHkKQEAgLTIwOSwxMSArMjA5LDIxIEBAIGRlZiBnZXRfZmxhdF9wYXJhbXMoZGVwZW5kYW50OiBEZXBlbmRhbnQpIC0+IExpc3RbTW9kZWxGaWVsZF06CiAgICAgcmV0dXJuIHBhdGhfcGFyYW1zICsgcXVlcnlfcGFyYW1zICsgaGVhZGVyX3BhcmFtcyArIGNvb2tpZV9wYXJhbXMKIAogCi1kZWYgZ2V0X3R5cGVkX3NpZ25hdHVyZShjYWxsOiBDYWxsYWJsZVsuLi4sIEFueV0pIC0+IGluc3BlY3QuU2lnbmF0dXJlOgorZGVmIF9nZXRfc2lnbmF0dXJlKGNhbGw6IENhbGxhYmxlWy4uLiwgQW55XSkgLT4gaW5zcGVjdC5TaWduYXR1cmU6CiAgICAgaWYgc3lzLnZlcnNpb25faW5mbyA+PSAoMywgMTApOgotICAgICAgICBzaWduYXR1cmUgPSBpbnNwZWN0LnNpZ25hdHVyZShjYWxsLCBldmFsX3N0cj1UcnVlKQorICAgICAgICB0cnk6CisgICAgICAgICAgICBzaWduYXR1cmUgPSBpbnNwZWN0LnNpZ25hdHVyZShjYWxsLCBldmFsX3N0cj1UcnVlKQorICAgICAgICBleGNlcHQgTmFtZUVycm9yOgorICAgICAgICAgICAgIyBIYW5kbGUgdHlwZSBhbm5vdGF0aW9ucyB3aXRoIGlmIFRZUEVfQ0hFQ0tJTkcsIG5vdCB1c2VkIGJ5IEZhc3RBUEkKKyAgICAgICAgICAgICMgZS5nLiBkZXBlbmRlbmN5IHJldHVybiB0eXBlcworICAgICAgICAgICAgc2lnbmF0dXJlID0gaW5zcGVjdC5zaWduYXR1cmUoY2FsbCkKICAgICBlbHNlOgogICAgICAgICBzaWduYXR1cmUgPSBpbnNwZWN0LnNpZ25hdHVyZShjYWxsKQorICAgIHJldHVybiBzaWduYXR1cmUKKworCitkZWYgZ2V0X3R5cGVkX3NpZ25hdHVyZShjYWxsOiBDYWxsYWJsZVsuLi4sIEFueV0pIC0+IGluc3BlY3QuU2lnbmF0dXJlOgorICAgIHNpZ25hdHVyZSA9IF9nZXRfc2lnbmF0dXJlKGNhbGwpCiAgICAgdW53cmFwcGVkID0gaW5zcGVjdC51bndyYXAoY2FsbCkKICAgICBnbG9iYWxucyA9IGdldGF0dHIodW53cmFwcGVkLCAiX19nbG9iYWxzX18iLCB7fSkKICAgICB0eXBlZF9wYXJhbXMgPSBbCkBAIC0yMzksMTAgKzI0OSw3IEBAIGRlZiBnZXRfdHlwZWRfYW5ub3RhdGlvbihhbm5vdGF0aW9uOiBBbnksIGdsb2JhbG5zOiBEaWN0W3N0ciwgQW55XSkgLT4gQW55OgogCiAKIGRlZiBnZXRfdHlwZWRfcmV0dXJuX2Fubm90YXRpb24oY2FsbDogQ2FsbGFibGVbLi4uLCBBbnldKSAtPiBBbnk6Ci0gICAgaWYgc3lzLnZlcnNpb25faW5mbyA+PSAoMywgMTApOgotICAgICAgICBzaWduYXR1cmUgPSBpbnNwZWN0LnNpZ25hdHVyZShjYWxsLCBldmFsX3N0cj1UcnVlKQotICAgIGVsc2U6Ci0gICAgICAgIHNpZ25hdHVyZSA9IGluc3BlY3Quc2lnbmF0dXJlKGNhbGwpCisgICAgc2lnbmF0dXJlID0gX2dldF9zaWduYXR1cmUoY2FsbCkKICAgICB1bndyYXBwZWQgPSBpbnNwZWN0LnVud3JhcChjYWxsKQogICAgIGFubm90YXRpb24gPSBzaWduYXR1cmUucmV0dXJuX2Fubm90YXRpb24KIA==")
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
