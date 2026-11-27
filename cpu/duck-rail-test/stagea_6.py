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
# pid=rich_2725 q9-A v1 (M735: Q9 direct variant-A, base 577def22dd83). No model calls. Ends: TEST-RESULT lines in log.
import os, subprocess, urllib.request, base64, sys
import sys as _sys
if _sys.version_info[0] < 3:
    import os as _os; _os.execvp("python3", ["python3"] + _sys.argv)
assert _sys.version_info >= (3, 10), "need python3.10+, got " + _sys.version
print("PY-VERSION " + sys.version.replace(chr(10)," "), flush=True)
def sh(cmd, timeout=300):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or "")
PID = "rich_2725"
REPO = "Textualize/rich"
BASE = "577def22dd83"
PYTEST = "tests/test_table.py"
KEXPR = "test_placement_table_box_elements"
SRCFILE = "rich/table.py"
IMPORTPKG = "rich"
PIPPKGS = "fastapi pytest pytest-timeout requests python-multipart annotated-doc starlette==0.37.2 httpx==0.27.2 inline-snapshot sqlalchemy orjson ujson"
TESTDIFF = base64.b64decode("LS0tIGEvdGVzdHMvdGVzdF90YWJsZS5weQorKysgYi90ZXN0cy90ZXN0X3RhYmxlLnB5CkBAIC0xLDYgKzEsNyBAQAogIyBlbmNvZGluZz11dGYtOAogCiBpbXBvcnQgaW8KK2Zyb20gdGV4dHdyYXAgaW1wb3J0IGRlZGVudAogCiBpbXBvcnQgcHl0ZXN0CiAKQEAgLTIzNCw2ICsyMzUsMTM0IEBAIGRlZiB0ZXN0X3NlY3Rpb24oKToKICAgICBhc3NlcnQgb3V0cHV0ID09IGV4cGVjdGVkCiAKIAorQHB5dGVzdC5tYXJrLnBhcmFtZXRyaXplKAorICAgICJzaG93X2hlYWRlcixzaG93X2Zvb3RlcixleHBlY3RlZCIsCisgICAgWworICAgICAgICAoCisgICAgICAgICAgICBGYWxzZSwKKyAgICAgICAgICAgIEZhbHNlLAorICAgICAgICAgICAgZGVkZW50KAorICAgICAgICAgICAgICAgICIiIgorICAgICAgICAgICAgICAgIGFiYmJiYmNiYmJiYmJiYmJjYmJiYmNiYmJiYmQKKyAgICAgICAgICAgICAgICAxRGVjICAyU2t5d2Fsa2VyMjI3NU0yMzc1TSAzCisgICAgICAgICAgICAgICAgNE1heSAgNVNvbG8gICAgIDUyNzVNNTM5M00gNgorICAgICAgICAgICAgICAgIGlqampqamtqampqampqamprampqamtqampqamwKKyAgICAgICAgICAgICAgICA3RGVjICA4TGFzdCBKZWRpODI2Mk04MTMzM005CisgICAgICAgICAgICAgICAgcXJycnJyc3JycnJycnJycnNycnJyc3JycnJydAorICAgICAgICAgICAgICAgICIiIgorICAgICAgICAgICAgKS5sc3RyaXAoKSwKKyAgICAgICAgKSwKKyAgICAgICAgKAorICAgICAgICAgICAgVHJ1ZSwKKyAgICAgICAgICAgIEZhbHNlLAorICAgICAgICAgICAgZGVkZW50KAorICAgICAgICAgICAgICAgICIiIgorICAgICAgICAgICAgICAgIGFiYmJiYmNiYmJiYmJiYmJjYmJiYmNiYmJiYmQKKyAgICAgICAgICAgICAgICAxTW9udGgyTmlja25hbWUgMkNvc3QyR3Jvc3MzCisgICAgICAgICAgICAgICAgZWZmZmZmZ2ZmZmZmZmZmZmdmZmZmZ2ZmZmZmaAorICAgICAgICAgICAgICAgIDREZWMgIDVTa3l3YWxrZXI1Mjc1TTUzNzVNIDYKKyAgICAgICAgICAgICAgICA0TWF5ICA1U29sbyAgICAgNTI3NU01MzkzTSA2CisgICAgICAgICAgICAgICAgaWpqampqa2pqampqampqamtqampqa2pqampqbAorICAgICAgICAgICAgICAgIDdEZWMgIDhMYXN0IEplZGk4MjYyTTgxMzMzTTkKKyAgICAgICAgICAgICAgICBxcnJycnJzcnJycnJycnJyc3JycnJzcnJycnJ0CisgICAgICAgICAgICAgICAgIiIiCisgICAgICAgICAgICApLmxzdHJpcCgpLAorICAgICAgICApLAorICAgICAgICAoCisgICAgICAgICAgICBGYWxzZSwKKyAgICAgICAgICAgIFRydWUsCisgICAgICAgICAgICBkZWRlbnQoCisgICAgICAgICAgICAgICAgIiIiCisgICAgICAgICAgICAgICAgYWJiYmJiY2JiYmJiYmJiYmNiYmJiY2JiYmJiZAorICAgICAgICAgICAgICAgIDFEZWMgIDJTa3l3YWxrZXIyMjc1TTIzNzVNIDMKKyAgICAgICAgICAgICAgICA0TWF5ICA1U29sbyAgICAgNTI3NU01MzkzTSA2CisgICAgICAgICAgICAgICAgaWpqampqa2pqampqampqamtqampqa2pqampqbAorICAgICAgICAgICAgICAgIDREZWMgIDVMYXN0IEplZGk1MjYyTTUxMzMzTTYKKyAgICAgICAgICAgICAgICBtbm5ubm5vbm5ubm5ubm5ub25ubm5vbm5ubm5wCisgICAgICAgICAgICAgICAgN01PTlRIOE5JQ0tOQU1FIDhDT1NUOEdST1NTOQorICAgICAgICAgICAgICAgIHFycnJycnNycnJycnJycnJzcnJycnNycnJycnQKKyAgICAgICAgICAgICAgICAiIiIKKyAgICAgICAgICAgICkubHN0cmlwKCksCisgICAgICAgICksCisgICAgICAgICgKKyAgICAgICAgICAgIFRydWUsCisgICAgICAgICAgICBUcnVlLAorICAgICAgICAgICAgZGVkZW50KAorICAgICAgICAgICAgICAgICIiIgorICAgICAgICAgICAgICAgIGFiYmJiYmNiYmJiYmJiYmJjYmJiYmNiYmJiYmQKKyAgICAgICAgICAgICAgICAxTW9udGgyTmlja25hbWUgMkNvc3QyR3Jvc3MzCisgICAgICAgICAgICAgICAgZWZmZmZmZ2ZmZmZmZmZmZmdmZmZmZ2ZmZmZmaAorICAgICAgICAgICAgICAgIDREZWMgIDVTa3l3YWxrZXI1Mjc1TTUzNzVNIDYKKyAgICAgICAgICAgICAgICA0TWF5ICA1U29sbyAgICAgNTI3NU01MzkzTSA2CisgICAgICAgICAgICAgICAgaWpqampqa2pqampqampqamtqampqa2pqampqbAorICAgICAgICAgICAgICAgIDREZWMgIDVMYXN0IEplZGk1MjYyTTUxMzMzTTYKKyAgICAgICAgICAgICAgICBtbm5ubm5vbm5ubm5ubm5ub25ubm5vbm5ubm5wCisgICAgICAgICAgICAgICAgN01PTlRIOE5JQ0tOQU1FIDhDT1NUOEdST1NTOQorICAgICAgICAgICAgICAgIHFycnJycnNycnJycnJycnJzcnJycnNycnJycnQKKyAgICAgICAgICAgICAgICAiIiIKKyAgICAgICAgICAgICkubHN0cmlwKCksCisgICAgICAgICksCisgICAgXSwKKykKK2RlZiB0ZXN0X3BsYWNlbWVudF90YWJsZV9ib3hfZWxlbWVudHMoc2hvd19oZWFkZXIsIHNob3dfZm9vdGVyLCBleHBlY3RlZCk6CisgICAgIiIiRW5zdXJlIGJveCBkcmF3aW5nIGNoYXJhY3RlcnMgY29ycmVjdGx5IHBvc2l0aW9uZWQuIiIiCisKKyAgICB0YWJsZSA9IFRhYmxlKAorICAgICAgICBib3g9Ym94LkFTQ0lJLCBzaG93X2hlYWRlcj1zaG93X2hlYWRlciwgc2hvd19mb290ZXI9c2hvd19mb290ZXIsIHBhZGRpbmc9MAorICAgICkKKworICAgICMgY29udGVudCByb3dzIGluZGljYXRlZCBieSBudW1lcmFscywgcHVyZSBkaXZpZGVycyBieSBsZXR0ZXJzCisgICAgdGFibGUuYm94Ll9fZGljdF9fLnVwZGF0ZSgKKyAgICAgICAgdG9wX2xlZnQ9ImEiLAorICAgICAgICB0b3A9ImIiLAorICAgICAgICB0b3BfZGl2aWRlcj0iYyIsCisgICAgICAgIHRvcF9yaWdodD0iZCIsCisgICAgICAgIGhlYWRfbGVmdD0iMSIsCisgICAgICAgIGhlYWRfdmVydGljYWw9IjIiLAorICAgICAgICBoZWFkX3JpZ2h0PSIzIiwKKyAgICAgICAgaGVhZF9yb3dfbGVmdD0iZSIsCisgICAgICAgIGhlYWRfcm93X2hvcml6b250YWw9ImYiLAorICAgICAgICBoZWFkX3Jvd19jcm9zcz0iZyIsCisgICAgICAgIGhlYWRfcm93X3JpZ2h0PSJoIiwKKyAgICAgICAgbWlkX2xlZnQ9IjQiLAorICAgICAgICBtaWRfdmVydGljYWw9IjUiLAorICAgICAgICBtaWRfcmlnaHQ9IjYiLAorICAgICAgICByb3dfbGVmdD0iaSIsCisgICAgICAgIHJvd19ob3Jpem9udGFsPSJqIiwKKyAgICAgICAgcm93X2Nyb3NzPSJrIiwKKyAgICAgICAgcm93X3JpZ2h0PSJsIiwKKyAgICAgICAgZm9vdF9sZWZ0PSI3IiwKKyAgICAgICAgZm9vdF92ZXJ0aWNhbD0iOCIsCisgICAgICAgIGZvb3RfcmlnaHQ9IjkiLAorICAgICAgICBmb290X3Jvd19sZWZ0PSJtIiwKKyAgICAgICAgZm9vdF9yb3dfaG9yaXpvbnRhbD0ibiIsCisgICAgICAgIGZvb3Rfcm93X2Nyb3NzPSJvIiwKKyAgICAgICAgZm9vdF9yb3dfcmlnaHQ9InAiLAorICAgICAgICBib3R0b21fbGVmdD0icSIsCisgICAgICAgIGJvdHRvbT0iciIsCisgICAgICAgIGJvdHRvbV9kaXZpZGVyPSJzIiwKKyAgICAgICAgYm90dG9tX3JpZ2h0PSJ0IiwKKyAgICApCisKKyAgICAjIGFkZCBjb250ZW50IC0gbm90ZSBoZWFkZXJzIHRpdGxlIGNhc2UsIGZvb3RlcnMgdXBwZXIgY2FzZQorICAgIHRhYmxlLmFkZF9jb2x1bW4oIk1vbnRoIiwgIk1PTlRIIiwgd2lkdGg9NSkKKyAgICB0YWJsZS5hZGRfY29sdW1uKCJOaWNrbmFtZSIsICJOSUNLTkFNRSIsIHdpZHRoPTkpCisgICAgdGFibGUuYWRkX2NvbHVtbigiQ29zdCIsICJDT1NUIiwgd2lkdGg9NCkKKyAgICB0YWJsZS5hZGRfY29sdW1uKCJHcm9zcyIsICJHUk9TUyIsIHdpZHRoPTUpCisKKyAgICB0YWJsZS5hZGRfcm93KCJEZWMiLCAiU2t5d2Fsa2VyIiwgIjI3NU0iLCAiMzc1TSIpCisgICAgdGFibGUuYWRkX3JvdygiTWF5IiwgIlNvbG8iLCAiMjc1TSIsICIzOTNNIikKKyAgICB0YWJsZS5hZGRfc2VjdGlvbigpCisgICAgdGFibGUuYWRkX3JvdygiRGVjIiwgIkxhc3QgSmVkaSIsICIyNjJNIiwgIjEzMzNNIikKKworICAgIGNvbnNvbGUgPSBDb25zb2xlKHJlY29yZD1UcnVlLCB3aWR0aD0yOCkKKyAgICBjb25zb2xlLnByaW50KHRhYmxlKQorICAgIG91dHB1dCA9IGNvbnNvbGUuZXhwb3J0X3RleHQoKQorICAgIHByaW50KHJlcHIob3V0cHV0KSkKKworICAgIGFzc2VydCBvdXRwdXQgPT0gZXhwZWN0ZWQKKworCiBpZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgogICAgIHJlbmRlciA9IHJlbmRlcl90YWJsZXMoKQogICAgIHByaW50KHJlbmRlcikK")
FIXDIFF = base64.b64decode("LS0tIGEvcmljaC90YWJsZS5weQorKysgYi9yaWNoL3RhYmxlLnB5CkBAIC03NzUsMTYgKzc3NSwxNiBAQAogICAgICAgICAgICAgICAgICAgICBfU2VnbWVudChfYm94LmhlYWRfcmlnaHQsIGJvcmRlcl9zdHlsZSksCiAgICAgICAgICAgICAgICAgICAgIF9TZWdtZW50KF9ib3guaGVhZF92ZXJ0aWNhbCwgYm9yZGVyX3N0eWxlKSwKICAgICAgICAgICAgICAgICApLAogICAgICAgICAgICAgICAgICgKKyAgICAgICAgICAgICAgICAgICAgX1NlZ21lbnQoX2JveC5taWRfbGVmdCwgYm9yZGVyX3N0eWxlKSwKKyAgICAgICAgICAgICAgICAgICAgX1NlZ21lbnQoX2JveC5taWRfcmlnaHQsIGJvcmRlcl9zdHlsZSksCisgICAgICAgICAgICAgICAgICAgIF9TZWdtZW50KF9ib3gubWlkX3ZlcnRpY2FsLCBib3JkZXJfc3R5bGUpLAorICAgICAgICAgICAgICAgICksCisgICAgICAgICAgICAgICAgKAogICAgICAgICAgICAgICAgICAgICBfU2VnbWVudChfYm94LmZvb3RfbGVmdCwgYm9yZGVyX3N0eWxlKSwKICAgICAgICAgICAgICAgICAgICAgX1NlZ21lbnQoX2JveC5mb290X3JpZ2h0LCBib3JkZXJfc3R5bGUpLAogICAgICAgICAgICAgICAgICAgICBfU2VnbWVudChfYm94LmZvb3RfdmVydGljYWwsIGJvcmRlcl9zdHlsZSksCiAgICAgICAgICAgICAgICAgKSwKLSAgICAgICAgICAgICAgICAoCi0gICAgICAgICAgICAgICAgICAgIF9TZWdtZW50KF9ib3gubWlkX2xlZnQsIGJvcmRlcl9zdHlsZSksCi0gICAgICAgICAgICAgICAgICAgIF9TZWdtZW50KF9ib3gubWlkX3JpZ2h0LCBib3JkZXJfc3R5bGUpLAotICAgICAgICAgICAgICAgICAgICBfU2VnbWVudChfYm94Lm1pZF92ZXJ0aWNhbCwgYm9yZGVyX3N0eWxlKSwKLSAgICAgICAgICAgICAgICApLAogICAgICAgICAgICAgXQogICAgICAgICAgICAgaWYgc2hvd19lZGdlOgogICAgICAgICAgICAgICAgIHlpZWxkIF9TZWdtZW50KF9ib3guZ2V0X3RvcCh3aWR0aHMpLCBib3JkZXJfc3R5bGUpCg==")
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
