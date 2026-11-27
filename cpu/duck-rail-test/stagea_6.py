# RICH HARNESS-FIT PROBE (M575): model-free. Gold-apply + targeted pytest for B1/B2.
# No rail, no secrets, no model calls. Deterministic: same tarball + same diffs = same result.
# Ends: TEST-RESULT per task + {pid}.pytest.txt + {pid}.applied.txt in OUT_DIR (/tmp/duck6_out).
# B3 owed: rich_2725 has base but no gold/tree; rich_3296 has tree+gold but no base SHA. Probe B1+B2 now.
import os, subprocess, urllib.request, base64
OUT_DIR = "/tmp/duck6_out"
os.makedirs(OUT_DIR, exist_ok=True)
TASKS = {
 "rich_3905": {
  "repo": "Textualize/rich",
  "base": "96dd4b60e3a7",
  "pytest": "tests/test_progress.py",
  "k": "test_no_output_if_progress_is_disabled_non_interactive",
  "fixB64": "ZGlmZiAtLWdpdCBhL3JpY2gvcHJvZ3Jlc3MucHkgYi9yaWNoL3Byb2dyZXNzLnB5CmluZGV4IDQyMWUxNDExOWQuLmY1NWI5ODFlNDAgMTAwNjQ0Ci0tLSBhL3JpY2gvcHJvZ3Jlc3MucHkKKysrIGIvcmljaC9wcm9ncmVzcy5weQpAQCAtMTE3Miw5ICsxMTcyLDEwIEBAIGRlZiBzdGFydChzZWxmKSAtPiBOb25lOgogCiAgICAgZGVmIHN0b3Aoc2VsZikgLT4gTm9uZToKICAgICAgICAgIiIiU3RvcCB0aGUgcHJvZ3Jlc3MgZGlzcGxheS4iIiIKLSAgICAgICAgc2VsZi5saXZlLnN0b3AoKQotICAgICAgICBpZiBub3Qgc2VsZi5jb25zb2xlLmlzX2ludGVyYWN0aXZlIGFuZCBub3Qgc2VsZi5jb25zb2xlLmlzX2p1cHl0ZXI6Ci0gICAgICAgICAgICBzZWxmLmNvbnNvbGUucHJpbnQoKQorICAgICAgICBpZiBub3Qgc2VsZi5kaXNhYmxlOgorICAgICAgICAgICAgc2VsZi5saXZlLnN0b3AoKQorICAgICAgICAgICAgaWYgbm90IHNlbGYuY29uc29sZS5pc19pbnRlcmFjdGl2ZSBhbmQgbm90IHNlbGYuY29uc29sZS5pc19qdXB5dGVyOgorICAgICAgICAgICAgICAgIHNlbGYuY29uc29sZS5wcmludCgpCiAKICAgICBkZWYgX19lbnRlcl9fKHNlbGYpIC0+IFNlbGY6CiAgICAgICAgIHNlbGYuc3RhcnQoKQo=",
  "testB64": "ZGlmZiAtLWdpdCBhL3Rlc3RzL3Rlc3RfcHJvZ3Jlc3MucHkgYi90ZXN0cy90ZXN0X3Byb2dyZXNzLnB5CmluZGV4IDBiZTY4M2MzZWEuLjIwZjQyNmE0Y2QgMTAwNjQ0Ci0tLSBhL3Rlc3RzL3Rlc3RfcHJvZ3Jlc3MucHkKKysrIGIvdGVzdHMvdGVzdF9wcm9ncmVzcy5weQpAQCAtNTY1LDYgKzU2NSwzMCBAQCBkZWYgdGVzdF9ub19vdXRwdXRfaWZfcHJvZ3Jlc3NfaXNfZGlzYWJsZWQoKSAtPiBOb25lOgogICAgIGFzc2VydCByZXN1bHQgPT0gZXhwZWN0ZWQKIAogCitkZWYgdGVzdF9ub19vdXRwdXRfaWZfcHJvZ3Jlc3NfaXNfZGlzYWJsZWRfbm9uX2ludGVyYWN0aXZlKCkgLT4gTm9uZToKKyAgICBjb25zb2xlID0gQ29uc29sZSgKKyAgICAgICAgZmlsZT1pby5TdHJpbmdJTygpLAorICAgICAgICBmb3JjZV9pbnRlcmFjdGl2ZT1GYWxzZSwKKyAgICAgICAgd2lkdGg9NjAsCisgICAgICAgIGNvbG9yX3N5c3RlbT0idHJ1ZWNvbG9yIiwKKyAgICAgICAgbGVnYWN5X3dpbmRvd3M9RmFsc2UsCisgICAgICAgIF9lbnZpcm9uPXt9LAorICAgICkKKyAgICBwcm9ncmVzcyA9IFByb2dyZXNzKAorICAgICAgICBjb25zb2xlPWNvbnNvbGUsCisgICAgICAgIGRpc2FibGU9VHJ1ZSwKKyAgICApCisgICAgdGVzdCA9IFsiZm9vIiwgImJhciIsICJiYXoiXQorICAgIGV4cGVjdGVkX3ZhbHVlcyA9IGl0ZXIodGVzdCkKKyAgICB3aXRoIHByb2dyZXNzOgorICAgICAgICBmb3IgdmFsdWUgaW4gcHJvZ3Jlc3MudHJhY2sodGVzdCwgZGVzY3JpcHRpb249InRlc3QiKToKKyAgICAgICAgICAgIGFzc2VydCB2YWx1ZSA9PSBuZXh0KGV4cGVjdGVkX3ZhbHVlcykKKyAgICByZXN1bHQgPSBjb25zb2xlLmZpbGUuZ2V0dmFsdWUoKQorICAgIHByaW50KHJlcHIocmVzdWx0KSkKKyAgICBleHBlY3RlZCA9ICIiCisgICAgYXNzZXJ0IHJlc3VsdCA9PSBleHBlY3RlZAorCisKIGRlZiB0ZXN0X29wZW4oKSAtPiBOb25lOgogICAgIGNvbnNvbGUgPSBDb25zb2xlKAogICAgICAgICBmaWxlPWlvLlN0cmluZ0lPKCksCg=="
 },
 "rich_3894": {
  "repo": "Textualize/rich",
  "base": "4d6d631a3d2d",
  "pytest": "tests/test_inspect.py",
  "k": "test_qualname_in_slots",
  "fixB64": "ZGlmZiAtLWdpdCBhL3JpY2gvX2luc3BlY3QucHkgYi9yaWNoL19pbnNwZWN0LnB5CmluZGV4IDI3ZDY1Y2VjOTMuLjA1ZDVlZWNjMTUgMTAwNjQ0Ci0tLSBhL3JpY2gvX2luc3BlY3QucHkKKysrIGIvcmljaC9faW5zcGVjdC5weQpAQCAtMTAxLDYgKzEwMSwxMCBAQCBkZWYgX2dldF9zaWduYXR1cmUoc2VsZiwgbmFtZTogc3RyLCBvYmo6IEFueSkgLT4gT3B0aW9uYWxbVGV4dF06CiAgICAgICAgIHNpZ25hdHVyZV90ZXh0ID0gc2VsZi5oaWdobGlnaHRlcihfc2lnbmF0dXJlKQogCiAgICAgICAgIHF1YWxuYW1lID0gbmFtZSBvciBnZXRhdHRyKG9iaiwgIl9fcXVhbG5hbWVfXyIsIG5hbWUpCisgICAgICAgIGlmIG5vdCBpc2luc3RhbmNlKHF1YWxuYW1lLCBzdHIpOgorICAgICAgICAgICAgcXVhbG5hbWUgPSBnZXRhdHRyKG9iaiwgIl9fbmFtZV9fIiwgbmFtZSkKKyAgICAgICAgICAgIGlmIG5vdCBpc2luc3RhbmNlKHF1YWxuYW1lLCBzdHIpOgorICAgICAgICAgICAgICAgIHF1YWxuYW1lID0gbmFtZQogCiAgICAgICAgICMgSWYgb2JqIGlzIGEgbW9kdWxlLCB0aGVyZSBtYXkgYmUgY2xhc3NlcyAod2hpY2ggYXJlIGNhbGxhYmxlKSB0byBkaXNwbGF5CiAgICAgICAgIGlmIGluc3BlY3QuaXNjbGFzcyhvYmopOgo=",
  "testB64": "ZGlmZiAtLWdpdCBhL3Rlc3RzL3Rlc3RfaW5zcGVjdC5weSBiL3Rlc3RzL3Rlc3RfaW5zcGVjdC5weQppbmRleCAzZjZlNWI5ZmU4Li5kNjk3MmZiNWVkIDEwMDY0NAotLS0gYS90ZXN0cy90ZXN0X2luc3BlY3QucHkKKysrIGIvdGVzdHMvdGVzdF9pbnNwZWN0LnB5CkBAIC00MDQsNiArNDA0LDE5IEBAIGNsYXNzIFRoaW5nOgogICAgIGFzc2VydCByZW5kZXIobW9kdWxlLCBtZXRob2RzPVRydWUpID09IGV4cGVjdGVkCiAKIAorZGVmIHRlc3RfcXVhbG5hbWVfaW5fc2xvdHMoKToKKyAgICBmcm9tIGZ1bmN0b29scyBpbXBvcnQgbHJ1X2NhY2hlCisKKyAgICBAbHJ1X2NhY2hlCisgICAgY2xhc3MgS2xhc3M6CisgICAgICAgIF9fc2xvdHNfXyA9ICgiX19xdWFsbmFtZV9fIiwpCisKKyAgICB0cnk6CisgICAgICAgIGluc3BlY3QoS2xhc3MpCisgICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgorICAgICAgICBhc3NlcnQgRmFsc2UsIGYiQ2xhc3Mgd2l0aCBfX3F1YWxuYW1lX18gaW4gX19zbG90c19fIHNob3VsZG4ndCByYWlzZSB7ZX0iCisKKwogQHB5dGVzdC5tYXJrLnBhcmFtZXRyaXplKAogICAgICJzcGVjaWFsX2NoYXJhY3RlcixleHBlY3RlZF9yZXBsYWNlbWVudCIsCiAgICAgKAo="
 }
}
def sh(cmd, timeout=300):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return p.returncode, ((p.stdout or "")[-2000:] + (p.stderr or "")[-2000:])
sh("pip install -q pytest pytest-timeout pygments typing-extensions 2>&1 | tail -1", timeout=300)
for pid, t in TASKS.items():
    work = "/tmp/duck6_" + pid
    sh("rm -rf " + work + " && mkdir -p " + work)
    url = "https://github.com/" + t["repo"] + "/archive/" + t["base"] + ".tar.gz"
    print("FETCH " + pid + " " + url, flush=True)
    try:
        urllib.request.urlretrieve(url, work + "/src.tgz")
    except Exception as e:
        print("TEST-RESULT " + pid + " fetch-fail " + str(e)[:160], flush=True)
        continue
    sh("tar xzf " + work + "/src.tgz -C " + work + " --strip-components=1", timeout=120)
    pyenv = "PYTHONPATH=" + work
    mrc, mout = sh("cd " + work + " && " + pyenv + " python -c \"import rich; print(rich.__file__)\" 2>&1 | tail -2", timeout=60)
    print("MODFILE " + pid + " rich " + mout[-160:], flush=True)
    if (work + "/") not in mout:
        print("TEST-RESULT " + pid + " shadow-fail " + mout[-160:], flush=True)
        continue
    open(work + "/fix.diff", "w").write(base64.b64decode(t["fixB64"]).decode())
    frc, fout = sh("cd " + work + " && git apply fix.diff 2>&1; echo FIX_APPLIED_RC=$?", timeout=60)
    print("FIX-APPLY " + pid + " " + fout[-200:], flush=True)
    if "FIX_APPLIED_RC=0" not in fout:
        print("TEST-RESULT " + pid + " fix-apply-fail", flush=True)
        continue
    open(work + "/test_patch.diff", "w").write(base64.b64decode(t["testB64"]).decode())
    trc2, tout2 = sh("cd " + work + " && git apply test_patch.diff 2>&1; echo TEST_APPLIED_RC=$?", timeout=60)
    print("TEST-APPLY " + pid + " " + tout2[-200:], flush=True)
    if "TEST_APPLIED_RC=0" not in tout2:
        print("TEST-RESULT " + pid + " test-apply-fail", flush=True)
        continue
    crc, cout = sh("cd " + work + " && python -m py_compile rich/progress.py rich/_inspect.py 2>&1; echo COMPILE_RC=$?", timeout=60)
    print("COMPILE " + pid + " " + cout[-200:], flush=True)
    trc, tout = sh("cd " + work + " && " + pyenv + " python -m pytest " + t["pytest"] + " -k " + t["k"] + " -v --tb=short -p no:cacheprovider > pytest_out.txt 2>&1; echo PYTEST_RC=$?; tail -15 pytest_out.txt", timeout=300)
    sh("cp " + work + "/pytest_out.txt " + OUT_DIR + "/" + pid + ".pytest.txt", timeout=30)
    open(OUT_DIR + "/" + pid + ".applied.txt", "w").write("fix_rc=0 test_rc=0 pytest_out_tail:\n" + tout[-1500:])
    import re as _re
    _m = _re.search(r"PYTEST_RC=(\d+)", tout)
    _ptr = _m.group(1) if _m else "?"
    print("TEST-RESULT " + pid + " rc=" + str(trc) + " pytest_rc=" + _ptr + " " + tout[-800:], flush=True)
print("PROBE-DONE", flush=True)
