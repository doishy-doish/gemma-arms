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
# pid=fastapi_15763 (M739: 14430-replacement shortlist, base 9a9c4ad5d06f). No model calls. Ends: TEST-RESULT lines in log.
import os, subprocess, urllib.request, base64, sys
import sys as _sys
if _sys.version_info[0] < 3:
    import os as _os; _os.execvp("python3", ["python3"] + _sys.argv)
assert _sys.version_info >= (3, 10), "need python3.10+, got " + _sys.version
print("PY-VERSION " + sys.version.replace(chr(10)," "), flush=True)
def sh(cmd, timeout=300):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")
PID = "fastapi_15763"
REPO = "fastapi/fastapi"
BASE = "9a9c4ad5d06f5fe8ee6775a5aeaa2f83c854f263"
PYTEST = "tests/test_router_include_context.py"
KEXPR = "test_no_prefix_include_validation_sees_effective_api_route_path or test_no_prefix_include_validation_sees_effective_starlette_route_path or test_no_prefix_include_validation_rejects_empty_effective_api_route_path"
SRCFILE = "fastapi/routing.py"
IMPORTPKG = "fastapi"
PIPPKGS = "fastapi pytest pytest-timeout requests python-multipart annotated-doc starlette==0.37.2 httpx==0.27.2 inline-snapshot sqlalchemy orjson ujson"
TESTDIFF = base64.b64decode("LS0tIGEvdGVzdHMvdGVzdF9yb3V0ZXJfaW5jbHVkZV9jb250ZXh0LnB5CisrKyBiL3Rlc3RzL3Rlc3Rfcm91dGVyX2luY2x1ZGVfY29udGV4dC5weQpAQCAtMiw2ICsyLDcgQEAKIAogaW1wb3J0IHB5dGVzdAogZnJvbSBmYXN0YXBpIGltcG9ydCBBUElSb3V0ZXIsIEJvZHksIERlcGVuZHMsIEZhc3RBUEksIFJlcXVlc3QKK2Zyb20gZmFzdGFwaS5leGNlcHRpb25zIGltcG9ydCBGYXN0QVBJRXJyb3IKIGZyb20gZmFzdGFwaS5yZXNwb25zZXMgaW1wb3J0IEhUTUxSZXNwb25zZSwgSlNPTlJlc3BvbnNlLCBQbGFpblRleHRSZXNwb25zZQogZnJvbSBmYXN0YXBpLnJvdXRpbmcgaW1wb3J0ICgKICAgICBBUElSb3V0ZSwKQEAgLTgwNyw2ICs4MDgsNjAgQEAgZGVmIGVuZHBvaW50KHJlcXVlc3QpOiAgIyBwcmFnbWE6IG5vIGNvdmVyCiAgICAgYXNzZXJ0IGNhc3QoUm91dGUsIGNhbmRpZGF0ZXNbMF0pLnBhdGggPT0gIi9jaGlsZC9pdGVtcyIKIAogCitkZWYgdGVzdF9ub19wcmVmaXhfaW5jbHVkZV92YWxpZGF0aW9uX3NlZXNfZWZmZWN0aXZlX2FwaV9yb3V0ZV9wYXRoKCk6CisgICAgbGVhZl9yb3V0ZXIgPSBBUElSb3V0ZXIoKQorCisgICAgQGxlYWZfcm91dGVyLmdldCgiIikKKyAgICBkZWYgcmVhZF9pdGVtcygpOgorICAgICAgICByZXR1cm4gW10KKworICAgIHBhcmVudF9yb3V0ZXIgPSBBUElSb3V0ZXIoKQorICAgIHBhcmVudF9yb3V0ZXIuaW5jbHVkZV9yb3V0ZXIobGVhZl9yb3V0ZXIsIHByZWZpeD0iL2l0ZW1zIikKKworICAgICMgZm9yIGNvdmVyYWdlCisgICAgY2FuZGlkYXRlcyA9IGxpc3QoX2l0ZXJfaW5jbHVkZWRfcm91dGVfY2FuZGlkYXRlcyhwYXJlbnRfcm91dGVyLnJvdXRlcykpCisgICAgYXNzZXJ0IGNhc3QoQVBJUm91dGUsIGNhbmRpZGF0ZXNbMF0pLnBhdGggPT0gIiIKKworICAgIGFwcCA9IEZhc3RBUEkoKQorICAgIGFwcC5pbmNsdWRlX3JvdXRlcihwYXJlbnRfcm91dGVyKQorICAgIGNsaWVudCA9IFRlc3RDbGllbnQoYXBwKQorCisgICAgcmVzcG9uc2UgPSBjbGllbnQuZ2V0KCIvaXRlbXMiKQorCisgICAgYXNzZXJ0IHJlc3BvbnNlLnN0YXR1c19jb2RlID09IDIwMCwgcmVzcG9uc2UudGV4dAorICAgIGFzc2VydCByZXNwb25zZS5qc29uKCkgPT0gW10KKworCitkZWYgdGVzdF9ub19wcmVmaXhfaW5jbHVkZV92YWxpZGF0aW9uX3NlZXNfZWZmZWN0aXZlX3N0YXJsZXR0ZV9yb3V0ZV9wYXRoKCk6CisgICAgZGVmIGVuZHBvaW50KHJlcXVlc3QpOgorICAgICAgICByZXR1cm4gUGxhaW5UZXh0UmVzcG9uc2UoIm9rIikKKworICAgIGNoaWxkX3JvdXRlciA9IEFQSVJvdXRlcihyb3V0ZXM9W1JvdXRlKCIvaXRlbXMiLCBlbmRwb2ludCwgbmFtZT0icmVhZF9pdGVtcyIpXSkKKyAgICBwYXJlbnRfcm91dGVyID0gQVBJUm91dGVyKCkKKyAgICBwYXJlbnRfcm91dGVyLmluY2x1ZGVfcm91dGVyKGNoaWxkX3JvdXRlciwgcHJlZml4PSIvY2hpbGQiKQorCisgICAgYXBwID0gRmFzdEFQSSgpCisgICAgYXBwLmluY2x1ZGVfcm91dGVyKHBhcmVudF9yb3V0ZXIpCisgICAgY2xpZW50ID0gVGVzdENsaWVudChhcHApCisKKyAgICByZXNwb25zZSA9IGNsaWVudC5nZXQoIi9jaGlsZC9pdGVtcyIpCisKKyAgICBhc3NlcnQgcmVzcG9uc2Uuc3RhdHVzX2NvZGUgPT0gMjAwLCByZXNwb25zZS50ZXh0CisgICAgYXNzZXJ0IHJlc3BvbnNlLnRleHQgPT0gIm9rIgorCisKK2RlZiB0ZXN0X25vX3ByZWZpeF9pbmNsdWRlX3ZhbGlkYXRpb25fcmVqZWN0c19lbXB0eV9lZmZlY3RpdmVfYXBpX3JvdXRlX3BhdGgoKToKKyAgICByb3V0ZXIgPSBBUElSb3V0ZXIoKQorCisgICAgQHJvdXRlci5nZXQoIiIpCisgICAgZGVmIHJlYWRfaXRlbXMoKTogICMgcHJhZ21hOiBubyBjb3ZlcgorICAgICAgICByZXR1cm4gW10KKworICAgIGFwcCA9IEZhc3RBUEkoKQorICAgIHdpdGggcHl0ZXN0LnJhaXNlcyhGYXN0QVBJRXJyb3IpOgorICAgICAgICBhcHAuaW5jbHVkZV9yb3V0ZXIocm91dGVyKQorCisKIGRlZiB0ZXN0X2FwaXJvdXRlcl9tYXRjaGVzX2ZhbGxiYWNrX3dpdGhvdXRfaW5jbHVkZV9jb250ZXh0KCk6CiAgICAgcm91dGVyID0gQVBJUm91dGVyKCkKIA==")
FIXDIFF = base64.b64decode("LS0tIGEvZmFzdGFwaS9yb3V0aW5nLnB5CisrKyBiL2Zhc3RhcGkvcm91dGluZy5weQpAQCAtMjQzNSw5ICsyNDM1LDE2IEBAIGRlZiByZWFkX3VzZXJzKCk6CiAgICAgICAgICAgICAgICAgIkEgcGF0aCBwcmVmaXggbXVzdCBub3QgZW5kIHdpdGggJy8nLCBhcyB0aGUgcm91dGVzIHdpbGwgc3RhcnQgd2l0aCAnLyciCiAgICAgICAgICAgICApCiAgICAgICAgIGVsc2U6Ci0gICAgICAgICAgICBmb3IgciBpbiBfaXRlcl9pbmNsdWRlZF9yb3V0ZV9jYW5kaWRhdGVzKHJvdXRlci5yb3V0ZXMpOgotICAgICAgICAgICAgICAgIHBhdGggPSBnZXRhdHRyKHIsICJwYXRoIiwgTm9uZSkKLSAgICAgICAgICAgICAgICBuYW1lID0gZ2V0YXR0cihyLCAibmFtZSIsICJ1bmtub3duIikKKyAgICAgICAgICAgIGZvciByb3V0ZSwgcm91dGVfY29udGV4dCBpbiBfaXRlcl9yb3V0ZXNfd2l0aF9jb250ZXh0KHJvdXRlci5yb3V0ZXMpOgorICAgICAgICAgICAgICAgIGlmIHJvdXRlX2NvbnRleHQgaXMgTm9uZToKKyAgICAgICAgICAgICAgICAgICAgcGF0aCA9IGdldGF0dHIocm91dGUsICJwYXRoIiwgTm9uZSkKKyAgICAgICAgICAgICAgICAgICAgbmFtZSA9IGdldGF0dHIocm91dGUsICJuYW1lIiwgInVua25vd24iKQorICAgICAgICAgICAgICAgIGVsaWYgcm91dGVfY29udGV4dC5zdGFybGV0dGVfcm91dGUgaXMgbm90IE5vbmU6CisgICAgICAgICAgICAgICAgICAgIHBhdGggPSBnZXRhdHRyKHJvdXRlX2NvbnRleHQuc3RhcmxldHRlX3JvdXRlLCAicGF0aCIsIE5vbmUpCisgICAgICAgICAgICAgICAgICAgIG5hbWUgPSBnZXRhdHRyKHJvdXRlX2NvbnRleHQuc3RhcmxldHRlX3JvdXRlLCAibmFtZSIsICJ1bmtub3duIikKKyAgICAgICAgICAgICAgICBlbHNlOgorICAgICAgICAgICAgICAgICAgICBwYXRoID0gcm91dGVfY29udGV4dC5wYXRoCisgICAgICAgICAgICAgICAgICAgIG5hbWUgPSByb3V0ZV9jb250ZXh0Lm5hbWUKICAgICAgICAgICAgICAgICBpZiBwYXRoIGlzIG5vdCBOb25lIGFuZCBub3QgcGF0aDoKICAgICAgICAgICAgICAgICAgICAgcmFpc2UgRmFzdEFQSUVycm9yKAogICAgICAgICAgICAgICAgICAgICAgICAgZiJQcmVmaXggYW5kIHBhdGggY2Fubm90IGJlIGJvdGggZW1wdHkgKHBhdGggb3BlcmF0aW9uOiB7bmFtZX0pIg==")
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
