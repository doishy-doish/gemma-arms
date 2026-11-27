# F2P PROBE (M654/M655): model-free. test-only apply -> pytest (expect FAIL), then +gold -> pytest (expect PASS).
# pid=fastapi_14616 base=54f8aeeb9a15 v5 (+NL test+gold norm. No model calls. Ends: TEST-RESULT lines in log.
import os, subprocess, urllib.request, base64, sys
import sys as _sys
if _sys.version_info[0] < 3:
    import os as _os; _os.execvp("python3", ["python3"] + _sys.argv)
assert _sys.version_info >= (3, 10), "need python3.10+, got " + _sys.version
print("PY-VERSION " + sys.version.replace(chr(10)," "), flush=True)
def sh(cmd, timeout=300):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")
PID = "fastapi_14616"
REPO = "fastapi/fastapi"
BASE = "54f8aeeb9a15"
PYTEST = "tests/test_json_type.py"
KEXPR = "test_form_json_list or test_query_json_list or test_header_json_list or test_cookie_json_list"
SRCFILE = "fastapi/dependencies/utils.py"
IMPORTPKG = "fastapi"
PIPPKGS = "fastapi pytest pytest-timeout requests python-multipart annotated-doc starlette==0.37.2 httpx==0.27.2"
TESTDIFF = base64.b64decode("LS0tIGEvdGVzdHMvdGVzdF9qc29uX3R5cGUucHkKKysrIGIvdGVzdHMvdGVzdF9qc29uX3R5cGUucHkKQEAgLTAsMCArMSw2MyBAQAoraW1wb3J0IGpzb24KK2Zyb20gdHlwaW5nIGltcG9ydCBBbm5vdGF0ZWQKKworZnJvbSBmYXN0YXBpIGltcG9ydCBDb29raWUsIEZhc3RBUEksIEZvcm0sIEhlYWRlciwgUXVlcnkKK2Zyb20gZmFzdGFwaS50ZXN0Y2xpZW50IGltcG9ydCBUZXN0Q2xpZW50Citmcm9tIHB5ZGFudGljIGltcG9ydCBKc29uCisKK2FwcCA9IEZhc3RBUEkoKQorCisKK0BhcHAucG9zdCgiL2Zvcm0tanNvbi1saXN0IikKK2RlZiBmb3JtX2pzb25fbGlzdChpdGVtczogQW5ub3RhdGVkW0pzb25bbGlzdFtzdHJdXSwgRm9ybSgpXSkgLT4gbGlzdFtzdHJdOgorICAgIHJldHVybiBpdGVtcworCisKK0BhcHAuZ2V0KCIvcXVlcnktanNvbi1saXN0IikKK2RlZiBxdWVyeV9qc29uX2xpc3QoaXRlbXM6IEFubm90YXRlZFtKc29uW2xpc3Rbc3RyXV0sIFF1ZXJ5KCldKSAtPiBsaXN0W3N0cl06CisgICAgcmV0dXJuIGl0ZW1zCisKKworQGFwcC5nZXQoIi9oZWFkZXItanNvbi1saXN0IikKK2RlZiBoZWFkZXJfanNvbl9saXN0KHhfaXRlbXM6IEFubm90YXRlZFtKc29uW2xpc3Rbc3RyXV0sIEhlYWRlcigpXSkgLT4gbGlzdFtzdHJdOgorICAgIHJldHVybiB4X2l0ZW1zCisKKworQGFwcC5nZXQoIi9jb29raWUtanNvbi1saXN0IikKK2RlZiBjb29raWVfanNvbl9saXN0KGl0ZW1zOiBBbm5vdGF0ZWRbSnNvbltsaXN0W3N0cl1dLCBDb29raWUoKV0pIC0+IGxpc3Rbc3RyXToKKyAgICByZXR1cm4gaXRlbXMKKworCitjbGllbnQgPSBUZXN0Q2xpZW50KGFwcCkKKworCitkZWYgdGVzdF9mb3JtX2pzb25fbGlzdCgpOgorICAgIHJlc3BvbnNlID0gY2xpZW50LnBvc3QoCisgICAgICAgICIvZm9ybS1qc29uLWxpc3QiLCBkYXRhPXsiaXRlbXMiOiBqc29uLmR1bXBzKFsiYWJjIiwgImRlZiJdKX0KKyAgICApCisgICAgYXNzZXJ0IHJlc3BvbnNlLnN0YXR1c19jb2RlID09IDIwMCwgcmVzcG9uc2UudGV4dAorICAgIGFzc2VydCByZXNwb25zZS5qc29uKCkgPT0gWyJhYmMiLCAiZGVmIl0KKworCitkZWYgdGVzdF9xdWVyeV9qc29uX2xpc3QoKToKKyAgICByZXNwb25zZSA9IGNsaWVudC5nZXQoCisgICAgICAgICIvcXVlcnktanNvbi1saXN0IiwgcGFyYW1zPXsiaXRlbXMiOiBqc29uLmR1bXBzKFsiYWJjIiwgImRlZiJdKX0KKyAgICApCisgICAgYXNzZXJ0IHJlc3BvbnNlLnN0YXR1c19jb2RlID09IDIwMCwgcmVzcG9uc2UudGV4dAorICAgIGFzc2VydCByZXNwb25zZS5qc29uKCkgPT0gWyJhYmMiLCAiZGVmIl0KKworCitkZWYgdGVzdF9oZWFkZXJfanNvbl9saXN0KCk6CisgICAgcmVzcG9uc2UgPSBjbGllbnQuZ2V0KAorICAgICAgICAiL2hlYWRlci1qc29uLWxpc3QiLCBoZWFkZXJzPXsieC1pdGVtcyI6IGpzb24uZHVtcHMoWyJhYmMiLCAiZGVmIl0pfQorICAgICkKKyAgICBhc3NlcnQgcmVzcG9uc2Uuc3RhdHVzX2NvZGUgPT0gMjAwLCByZXNwb25zZS50ZXh0CisgICAgYXNzZXJ0IHJlc3BvbnNlLmpzb24oKSA9PSBbImFiYyIsICJkZWYiXQorCisKK2RlZiB0ZXN0X2Nvb2tpZV9qc29uX2xpc3QoKToKKyAgICBjbGllbnQuY29va2llcy5zZXQoIml0ZW1zIiwganNvbi5kdW1wcyhbImFiYyIsICJkZWYiXSkpCisgICAgcmVzcG9uc2UgPSBjbGllbnQuZ2V0KCIvY29va2llLWpzb24tbGlzdCIpCisgICAgYXNzZXJ0IHJlc3BvbnNlLnN0YXR1c19jb2RlID09IDIwMCwgcmVzcG9uc2UudGV4dAorICAgIGFzc2VydCByZXNwb25zZS5qc29uKCkgPT0gWyJhYmMiLCAiZGVmIl0KKyAgICBjbGllbnQuY29va2llcy5jbGVhcigp")
FIXDIFF = base64.b64decode("LS0tIGEvZmFzdGFwaS9kZXBlbmRlbmNpZXMvdXRpbHMucHkKKysrIGIvZmFzdGFwaS9kZXBlbmRlbmNpZXMvdXRpbHMucHkKQEAgLTUxLDcgKzUxLDcgQEAKIGZyb20gZmFzdGFwaS5zZWN1cml0eS5vYXV0aDIgaW1wb3J0IFNlY3VyaXR5U2NvcGVzCiBmcm9tIGZhc3RhcGkudHlwZXMgaW1wb3J0IERlcGVuZGVuY3lDYWNoZUtleQogZnJvbSBmYXN0YXBpLnV0aWxzIGltcG9ydCBjcmVhdGVfbW9kZWxfZmllbGQsIGdldF9wYXRoX3BhcmFtX25hbWVzCi1mcm9tIHB5ZGFudGljIGltcG9ydCBCYXNlTW9kZWwKK2Zyb20gcHlkYW50aWMgaW1wb3J0IEJhc2VNb2RlbCwgSnNvbgogZnJvbSBweWRhbnRpYy5maWVsZHMgaW1wb3J0IEZpZWxkSW5mbwogZnJvbSBzdGFybGV0dGUuYmFja2dyb3VuZCBpbXBvcnQgQmFja2dyb3VuZFRhc2tzIGFzIFN0YXJsZXR0ZUJhY2tncm91bmRUYXNrcwogZnJvbSBzdGFybGV0dGUuY29uY3VycmVuY3kgaW1wb3J0IHJ1bl9pbl90aHJlYWRwb29sCkBAIC03MjYsMTEgKzcyNiwxOSBAQCBkZWYgX3ZhbGlkYXRlX3ZhbHVlX3dpdGhfbW9kZWxfZmllbGQoCiAgICAgICAgIHJldHVybiB2XywgW10KIAogCitkZWYgX2lzX2pzb25fZmllbGQoZmllbGQ6IE1vZGVsRmllbGQpIC0+IGJvb2w6CisgICAgcmV0dXJuIGFueSh0eXBlKGl0ZW0pIGlzIEpzb24gZm9yIGl0ZW0gaW4gZmllbGQuZmllbGRfaW5mby5tZXRhZGF0YSkKKworCiBkZWYgX2dldF9tdWx0aWRpY3RfdmFsdWUoCiAgICAgZmllbGQ6IE1vZGVsRmllbGQsIHZhbHVlczogTWFwcGluZ1tzdHIsIEFueV0sIGFsaWFzOiBVbmlvbltzdHIsIE5vbmVdID0gTm9uZQogKSAtPiBBbnk6CiAgICAgYWxpYXMgPSBhbGlhcyBvciBnZXRfdmFsaWRhdGlvbl9hbGlhcyhmaWVsZCkKLSAgICBpZiBpc19zZXF1ZW5jZV9maWVsZChmaWVsZCkgYW5kIGlzaW5zdGFuY2UodmFsdWVzLCAoSW1tdXRhYmxlTXVsdGlEaWN0LCBIZWFkZXJzKSk6CisgICAgaWYgKAorICAgICAgICAobm90IF9pc19qc29uX2ZpZWxkKGZpZWxkKSkKKyAgICAgICAgYW5kIGlzX3NlcXVlbmNlX2ZpZWxkKGZpZWxkKQorICAgICAgICBhbmQgaXNpbnN0YW5jZSh2YWx1ZXMsIChJbW11dGFibGVNdWx0aURpY3QsIEhlYWRlcnMpKQorICAgICk6CiAgICAgICAgIHZhbHVlID0gdmFsdWVzLmdldGxpc3QoYWxpYXMpCiAgICAgZWxzZToKICAgICAgICAgdmFsdWUgPSB2YWx1ZXMuZ2V0KGFsaWFzLCBOb25lKQ==")
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
