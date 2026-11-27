# S3b-ORACLE calibration (M553) — S3b task + mechanism hint in ISSUES (prompt-only delta, no harness change).
# S3 PILOT scrapy_s3b (M546) — single-task de-oracled pilot, template from stagea-tornado_s6b.py (harness/ask/main identical).
# spec=scratch/roulette/spec-scrapy_s3b.json repo=scrapy/scrapy@45417e6b0364 fix=scrapy/utils/deprecate.py pytest=scrapy/tests/test_utils_deprecate.py -k "test_issubclass or test_isinstance"
"""Duck stage-A PERSONA (reasoning low + terse lock + ORACLES exactness): same-6 clean-room, one turn each, then public-proxy score.
Model: tinfoil/gemma4-31b via browser rail (pure chat API, no harness in Duck).
Harness (checkout/apply/pytest) lives HERE, not in the API.
"""

"""TESTING-ONLY BUNDLE (not submittable) — what stays here and why it cannot ship:
- THIS FILE (+ duckapi_duckai.py rail driver) is OUR measurement instrument on
  GitHub Actions. Official grading runs THEIR harness (HARNESS_README:
  Container A agent -> git diff -> Container B hermetic pytest) over
  submission.zip. Nothing here transfers; similarity is behavioral at best.
- ORACLES (exact import lines, recipes, forbid-lists): per-task answer keys for
  calibration. A submission must be a general agent (single-model rule,
  declarative-only: agent.yaml/prompts/skills/adapters — no Python
  orchestration, no hardcoded per-task answers). Shipping oracles = overfit to
  6 tasks, scores ~0 on the hidden set.
- PINNED 6 (TASKS/SLICES/PYTESTS at fixed base commits + test patches): our
  private slice. Official eval = full hidden task set; this bundle covers none
  of it.
- RETRY/T2/REVISE LOOPS, verbose tails, FAIL_TAILS, MODFILE/SHADOW-GUARD: our
  diagnostic scaffolding and draw budget. Official budgets (calls/wall/
  compaction) are enforced server-side by their harness; our loop counts
  against nothing there and cannot be submitted (no Python entrypoints allowed).
- Duck.ai CHAT RAIL: test transport only (official = vLLM tool-calling on 4xL4; chat tricks don't transfer).
- PARALLEL-FIRE RULE: serial-depends-on-last may still fire in parallel at HIGH confidence (prior GREEN same SHA / mechanical byte-proof); gate is confidence, not order (M232).
Rule: instrument freely here (faithfulness-only: never relax tests, never touch
test files); the submission path takes only what transfers de-oracled.
"""
import asyncio, os, sys, subprocess, tarfile, threading, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from duckapi_duckai import DuckAISession

SLICES = {
    """scrapy_s3b""": "    It can be used to rename a base class in a library. For example, if we\n    have\n\n        class OldName(SomeClass):\n            # ...\n\n    and we want to rename it to NewName, we can do the following::\n\n        class NewName(SomeClass):\n            # ...\n\n        OldName = create_deprecated_class('OldName', NewName)\n\n    Then, if user class inherits from OldName, warning is issued. Also, if\n    some code uses ``issubclass(sub, OldName)`` or ``isinstance(sub(), OldName)``\n    checks they'll still return True if sub is a subclass of NewName instead of\n    OldName.\n    \"\"\"\n\n    class DeprecatedClass(new_class.__class__):\n\n        deprecated_class = None\n        warned_on_subclass = False\n\n        def __new__(metacls, name, bases, clsdict_):\n            cls = super(DeprecatedClass, metacls).__new__(metacls, name, bases, clsdict_)\n            if metacls.deprecated_class is None:\n                metacls.deprecated_class = cls\n            return cls\n\n        def __init__(cls, name, bases, clsdict_):\n            meta = cls.__class__\n            old = meta.deprecated_class\n            if old in bases and not (warn_once and meta.warned_on_subclass):\n                meta.warned_on_subclass = True\n                msg = subclass_warn_message.format(cls=_clspath(cls),\n                                                   old=_clspath(old, old_class_path),\n                                                   new=_clspath(new_class, new_class_path))\n                if warn_once:\n                    msg += ' (warning only on first subclass, there may be others)'\n                warnings.warn(msg, warn_category, stacklevel=2)\n            super(DeprecatedClass, cls).__init__(name, bases, clsdict_)\n\n        # see http://www.python.org/dev/peps/pep-3119/#overloading-isinstance-and-issubclass\n        # and http://docs.python.org/2/reference/datamodel.html#customizing-instance-and-subclass-checks\n        # for implementation details\n        def __instancecheck__(cls, inst):\n            return any(cls.__subclasscheck__(c)\n                       for c in {type(inst), inst.__class__})\n\n        def __subclasscheck__(cls, sub):\n            if not inspect.isclass(sub):\n                raise TypeError(\"issubclass() arg 1 must be a class\")\n\n            mro = getattr(sub, '__mro__', ())\n            candidates = {cls, new_class}\n            return any(c in candidates for c in mro)\n\n        def __call__(cls, *args, **kwargs):\n            old = DeprecatedClass.deprecated_class\n            if cls is old:\n                msg = instance_warn_message.format(cls=_clspath(cls, old_class_path),\n                                                   new=_clspath(new_class, new_class_path))\n                warnings.warn(msg, warn_category, stacklevel=2)\n            return super(DeprecatedClass, cls).__call__(*args, **kwargs)\n\n    deprecated_cls = DeprecatedClass(name, (new_class,), clsdict or {})\n    frm = inspect.stack()[1]\n    parent_module = inspect.getmodule(frm[0])\n    if parent_module is not None:\n        deprecated_cls.__module__ = parent_module.__name__\n\n    return deprecated_cls\n\n\ndef _clspath(cls, forced=None):\n    if forced is not None:\n        return forced\n    return '{}.{}'.format(cls.__module__, cls.__name__)\n",
}
ISSUES = {
    """scrapy_s3b""": "[ISSUE]\n**Title:** Incorrect `issubclass` and `isinstance` Behavior with Subclasses of Deprecated Classes\n\n**Description:**\nWhen subclassing a deprecated class, the `issubclass` and `isinstance` functions behave unexpectedly by incorrectly identifying subclasses as related to each other, even when they shouldn't be.\n\n**Example Buggy Code:**\n```python\nDeprecatedName = create_deprecated_class('DeprecatedName', NewName)\n\nclass OutdatedUserClass1(DeprecatedName):\n    pass\n\nclass OutdatedUserClass1a(DeprecatedName):\n    pass\n\n# These checks incorrectly return True\nprint(issubclass(OutdatedUserClass1, OutdatedUserClass1a))  \nprint(isinstance(OutdatedUserClass1a(), OutdatedUserClass1))  \n```\n\n**Expected Behavior:**\n- `issubclass(OutdatedUserClass1, OutdatedUserClass1a)` should return `False` because `OutdatedUserClass1` and `OutdatedUserClass1a` are distinct subclasses of `DeprecatedName` and do not inherit from each other.\n- `isinstance(OutdatedUserClass1a(), OutdatedUserClass1)` should also return `False` since an instance of `OutdatedUserClass1a` is not an instance of `OutdatedUserClass1`.\n\n**Actual Behavior:**\nBoth `issubclass` and `isinstance` incorrectly return `True`, falsely indicating a relationship between `OutdatedUserClass1` and `OutdatedUserClass1a`. This inaccurate behavior disrupts type checking and can lead to logic errors in the application.\n[/ISSUE]\n\nHINT (calibration assist — mechanism only, not code): the custom __subclasscheck__ currently applies its mro-membership test for EVERY cls, including subclasses of the deprecated class. The fix restricts the custom magic to the case where cls IS the deprecated class itself, delegating all other cases to the normal type.__subclasscheck__. Only two small edits in scrapy/utils/deprecate.py.",
}
CONTRACT = """OUTPUT CONTRACT (follow exactly):
- Output edit blocks only: no prose, no fences, no explanation.
- Each block has exactly this shape:
FILE: <exact repo-relative path>
<<<<<< SEARCH
<exact verbatim lines copied from LOCALIZED CODE>
======
<replacement lines>
>>>>>>
- SEARCH must occur in the target file byte-for-byte exactly once. Keep SEARCH minimal but unique (include enough surrounding context).
- Multiple SEARCH/======/>>>>>> pairs allowed under one FILE: header (one pair per hunk); every pair is matched independently, all must match.
- Minimal fix only.
"""
ALLOW = {
    """scrapy_s3b""": ["scrapy/utils/deprecate.py"],
}
PROMPTS = {}
for _pid in ISSUES:
    PROMPTS[_pid] = "You are an expert Python engineer. Minimal fix only.\n\n" + ISSUES[_pid] + "\n\nLOCALIZED CODE (verbatim from the base commit; SEARCH blocks must be copied from here byte-for-byte):\n" + SLICES[_pid] + "\n" + CONTRACT
TASKS = {
    """scrapy_s3b""": {"repo": "scrapy/scrapy", "base": "45417e6b0364", "test_patch": "@@ -145,6 +145,9 @@ class UpdatedUserClass1a(NewName):\n             class OutdatedUserClass1(DeprecatedName):\n                 pass\n \n+            class OutdatedUserClass1a(DeprecatedName):\n+                pass\n+\n             class UnrelatedClass(object):\n                 pass\n \n@@ -159,6 +162,8 @@ class OldStyleClass:\n         assert not issubclass(UnrelatedClass, DeprecatedName)\n         assert not issubclass(OldStyleClass, DeprecatedName)\n         assert not issubclass(OldStyleClass, DeprecatedName)\n+        assert not issubclass(OutdatedUserClass1, OutdatedUserClass1a)\n+        assert not issubclass(OutdatedUserClass1a, OutdatedUserClass1)\n \n         self.assertRaises(TypeError, issubclass, object(), DeprecatedName)\n \n@@ -175,6 +180,9 @@ class UpdatedUserClass2a(NewName):\n             class OutdatedUserClass2(DeprecatedName):\n                 pass\n \n+            class OutdatedUserClass2a(DeprecatedName):\n+                pass\n+\n             class UnrelatedClass(object):\n                 pass\n \n@@ -186,6 +194,9 @@ class OldStyleClass:\n         assert isinstance(UpdatedUserClass2(), DeprecatedName)\n         assert isinstance(UpdatedUserClass2a(), DeprecatedName)\n         assert isinstance(OutdatedUserClass2(), DeprecatedName)\n+        assert isinstance(OutdatedUserClass2a(), DeprecatedName)\n+        assert not isinstance(OutdatedUserClass2a(), OutdatedUserClass2)\n+        assert not isinstance(OutdatedUserClass2(), OutdatedUserClass2a)\n         assert not isinstance(UnrelatedClass(), DeprecatedName)\n         assert not isinstance(OldStyleClass(), DeprecatedName)\n "},
}
REWRITE_LOW_TERSE = {"model": "tinfoil/gemma4-31b", "reasoningEffort": "low"}
FILE_HINTS = {
    """scrapy_s3b""": "",
}
EDGE_HINTS = {
    """scrapy_s3b""": "",
}
ORACLES = {
    """scrapy_s3b""": "",
}
def _parse_blocks(body):
    # SLICE-2 delimiter tolerance: models wrap blocks in fences and vary
    # chevrons/spacing (<<<< SEARCH, <<<<<<< SEARCH). Flex ONLY delimiter
    # lines via regex; SEARCH/repl CONTENT bytes stay exact (fidelity gate
    # lives in harness). A trailing ``` fence line is ignored.
    import re as _rx
    _SEARCH_RE = _rx.compile(r"^\s*<{4,8}\s*SEARCH\s*$")
    _SEP_RE = _rx.compile(r"^\s*={4,8}\s*$")
    _END_RE = _rx.compile(r"^\s*>{4,8}\s*$")
    blocks = []
    parts = body.split("FILE:")
    if len(parts) < 2:
        return None
    for p in parts[1:]:
        nl = p.find("\n")
        if nl < 0:
            return None
        path = p[:nl].strip().strip("`").strip()
        if not path:
            return None
        lines = p[nl + 1:].split("\n")
        while lines and lines[-1].strip() in ("```",):
            lines.pop()
        # MULTI-PAIR (M518): successive SEARCH/======/>>>>>> triples under one
        # FILE: header all apply; a malformed triple voids the whole reply.
        triples = []
        i = 0
        n = len(lines)
        while True:
            while i < n and not lines[i].strip():
                i += 1
            if i >= n:
                break
            if not _SEARCH_RE.match(lines[i]):
                return None
            try:
                mi = next(j for j in range(i + 1, n) if _SEP_RE.match(lines[j]))
                ei = next(j for j in range(mi + 1, n) if _END_RE.match(lines[j]))
            except StopIteration:
                return None
            if mi <= i + 1 or ei <= mi + 1:
                return None
            search = "\n".join(lines[i + 1:mi])
            repl = "\n".join(lines[mi + 1:ei])
            if len(search.strip()) < 20:
                return None
            triples.append((search, repl))
            i = ei + 1
        if not triples:
            return None
        for (search, repl) in triples:
            blocks.append((path, search, repl))
    return blocks or None

async def ask(s, pid, prompt):
    full = CONTRACT + " Emit exactly ONE FILE:/SEARCH/REPLACE triple; SEARCH must be a verbatim copy of source lines (full signature, no truncation) or the reply voids.\n\n" + prompt
    last = ""
    for attempt in range(3):
        q = full if attempt == 0 else "INVALID prior output (unparseable block, wrong FILE, or ambiguous SEARCH). Resubmit BLOCKS ONLY, correct FILE, SEARCH copied verbatim from LOCALIZED CODE.\n\n" + full
        reply = await s.send(q, rewrite=REWRITE_LOW_TERSE)
        last = reply
        b = reply.strip()
        if b.startswith("```"):
            ls = b.split("\n")
            b = "\n".join(ls[1:-1] if ls[-1].strip().startswith("```") else ls[1:])
        bl = _parse_blocks(b)
        if bl and all(p in ALLOW.get(pid, []) for (p, _s, _r) in bl):
            return reply.replace("```", "")
        print("RETRY " + pid + " attempt=" + str(attempt + 1) + " len=" + str(len(reply)), flush=True)
    return last

_DEPS_OK = False
_DEPS_LOCK = threading.Lock()
PYTESTS = {
    """scrapy_s3b""": "scrapy/tests/test_utils_deprecate.py -k \"test_issubclass or test_isinstance\"",
}
def ensure_deps():
    global _DEPS_OK
    with _DEPS_LOCK:
        if _DEPS_OK:
            return
        # DO NOT REMOVE annotated-doc (M495): fastapi runtime dep (`from annotated_doc import Doc`
        # in fastapi src). Agent never emits it; eval image has it baked. Without it every
        # pytest dies at collection (0/6 verified). Harness-only line (runners are online);
        # the submission bundle itself must still assume offline (M495a).
        sh("pip install -q fastapi pytest pytest-timeout requests python-multipart annotated-doc starlette==0.37.2 httpx==0.27.2 2>&1 | tail -1", timeout=300)
        sh("pip install -q scrapy 2>&1 | tail -1", timeout=300)
        _DEPS_OK = True


def sh(cmd, **kw):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=kw.get("timeout", 300))
    return p.returncode, (p.stdout or "")[-2000:] + (p.stderr or "")[-2000:]

# SLICE-2 Turn-2 feedback: harness records actionable failure tails here;
# main() sends at most ONE follow-up per pid in the same session.
FAIL_TAILS = {}
def harness(pid, reply, t):
    body = reply.strip()
    if body.startswith("```"):
        ls = body.split("\n")
        body = "\n".join(ls[1:-1] if ls[-1].strip().startswith("```") else ls[1:])
    blocks = _parse_blocks(body)
    if not blocks:
        print("EMPTY-DIFF " + pid + " len=" + str(len(body)), flush=True)
        FAIL_TAILS[pid] = "no parseable FILE:/SEARCH blocks in reply len=" + str(len(body)) + " — resubmit BLOCKS ONLY, SEARCH copied verbatim from LOCALIZED CODE slice"
        return "empty len=" + str(len(body))
    ok_paths = ALLOW.get(pid, [])
    for (path, _s, _r) in blocks:
        if path not in ok_paths:
            print("WRONG-FILE " + pid + " " + path, flush=True)
            FAIL_TAILS[pid] = "wrong FILE " + path + " — allowed: " + str(ok_paths); return "wrong-file " + path
    # SLICE-2 (M471): ALL collected outputs go to OUT_DIR only (blocks +
    # real unified diffs + replies + pytest tails). Work checkouts + tarballs
    # stay in /tmp/duck6_<pid> and are NEVER uploaded (prior /tmp/duck6_*
    # glob caught worktrees+tarballs = 146MB bloat; target <5MB).
    OUT_DIR = "/tmp/duck6_out"
    try:
        os.makedirs(OUT_DIR, exist_ok=True)
    except Exception:
        pass
    raw_path = OUT_DIR + "/" + pid + ".blocks"
    open(raw_path, "w").write(body if body.endswith("\n") else body + "\n")
    work = "/tmp/duck6_" + pid
    sh("rm -rf " + work + " && mkdir -p " + work)
    url = "https://github.com/" + t["repo"] + "/archive/" + t["base"] + ".tar.gz"
    print("FETCH " + pid + " " + url, flush=True)
    try:
        urllib.request.urlretrieve(url, work + "/src.tgz")
    except Exception as e:
        print("FETCH-FAIL " + pid + " " + str(e)[:200], flush=True)
        return "fetch-fail len=" + str(len(reply))
    sh("tar xzf " + work + "/src.tgz -C " + work + " --strip-components=1", timeout=120)
    ensure_deps()
    # SHADOW-GUARD (M518): src-layout repos (requests) are unimportable from the
    # tarball root via pytest path insertion, so tests would silently run against
    # site-packages instead of the patch. Force tarball-first via PYTHONPATH and
    # PROVE it by resolving the module file before pytest.
    mod = t["repo"].split("/")[1]
    pyenv = "PYTHONPATH=" + work + ":" + work + "/src"
    mrc, mout = sh("cd " + work + " && " + pyenv + " python -c \"import " + mod + "; print(" + mod + ".__file__)\" 2>&1 | tail -2", timeout=60)
    print("MODFILE " + pid + " " + mod + " " + mout[-160:], flush=True)
    if (work + "/") not in mout:
        FAIL_TAILS[pid] = "shadow import: " + mod + " resolves outside work dir (" + mout[-160:] + ") — tarball code would NOT run; fix PYTHONPATH/install before trusting pytest"
        return "shadow-fail " + mod
    applied = []
    origs = {}
    n_bl = len(blocks)
    for (path, search, repl) in blocks:
        fp = work + "/" + path
        try:
            content = open(fp).read()
        except Exception:
            print("READ-FAIL " + pid + " " + path, flush=True)
            return "read-fail " + path
        n = content.count(search)
        if n == 1:
            new_content = content.replace(search, repl, 1)
        elif n == 0:
            # SLICE-2 whitespace fallback: trailing-whitespace-insensitive
            # match, applied ONLY on a strictly unique line-range hit
            # (verified before replace). Still a miss otherwise.
            new_content = None
            olines = content.split("\n")
            norm = "\n".join(ln.rstrip() for ln in olines)
            nsearch = "\n".join(ln.rstrip() for ln in search.split("\n"))
            if nsearch.strip() and norm.count(nsearch) == 1:
                start = norm.find(nsearch)
                pre = norm[:start].count("\n")
                nlines = nsearch.count("\n") + 1
                if pre + nlines <= len(olines):
                    cand = "\n".join(olines[pre:pre + nlines])
                    if "\n".join(ln.rstrip() for ln in cand.split("\n")) == nsearch:
                        print("SEARCH-WSFALLBACK " + pid + " " + path + " lines=" + str(nlines), flush=True)
                        olines[pre:pre + nlines] = repl.split("\n")
                        new_content = "\n".join(olines)
            if new_content is None:
                print("SEARCH-MISS " + pid + " " + path + " n=0 block " + str(len(applied) + 1) + "/" + str(n_bl), flush=True)
                FAIL_TAILS[pid] = "SEARCH block " + str(len(applied) + 1) + "/" + str(n_bl) + " not found verbatim in " + path + " — copy exact lines from the LOCALIZED CODE slice (byte-for-byte, no rewording). NOTE: earlier blocks in this reply already applied to the file."
                return "search-miss " + path + " applied " + str(len(applied)) + "/" + str(n_bl)
        else:
            print("SEARCH-AMBIGUOUS " + pid + " " + path + " n=" + str(n) + " block " + str(len(applied) + 1) + "/" + str(n_bl), flush=True)
            FAIL_TAILS[pid] = "SEARCH block " + str(len(applied) + 1) + "/" + str(n_bl) + " matches " + str(n) + " places in " + path + " — extend SEARCH with more surrounding context lines until unique"
            return "search-ambiguous " + path + " applied " + str(len(applied)) + "/" + str(n_bl)
        origs[path] = content
        open(fp, "w").write(new_content)
        applied.append(path)
    # SLICE-2: real unified diffs into OUT_DIR (verdict evidence, not the
    # .blocks proposals — applied-file diff is what pytest actually ran).
    try:
        import difflib
        dl = []
        for path in applied:
            new = open(work + "/" + path).read()
            dl.extend(difflib.unified_diff(origs[path].splitlines(), new.splitlines(), "a/" + path, "b/" + path, lineterm=""))
        open(OUT_DIR + "/" + pid + ".diff", "w").write("\n".join(dl) + "\n" if dl else "")
    except Exception as e:
        print("DIFF-FAIL " + pid + " " + str(e)[:160], flush=True)
    rc, out = sh("cd " + work + " && python -m py_compile " + " ".join(sorted(set(applied))) + " 2>&1; echo COMPILE_RC=$?", timeout=60)
    print("COMPILE " + pid + " rc=" + str(rc) + " " + out[-200:], flush=True)
    open(work + "/test_patch.diff", "w").write(t["test_patch"] if t["test_patch"].endswith("\n") else t["test_patch"] + "\n")
    sh("cd " + work + " && git apply test_patch.diff 2>&1 | head -5; echo TEST_APPLIED_RC=$?", timeout=60)
    ensure_deps()
    tf = PYTESTS.get(pid, "")
    trc, tout = sh("cd " + work + " && " + pyenv + " python -m pytest " + tf + " -v --tb=short -W ignore::PendingDeprecationWarning -W ignore::DeprecationWarning -p no:cacheprovider > pytest_out.txt 2>&1; echo PYTEST_RC=$?; tail -15 pytest_out.txt", timeout=300)
    sh("cp " + work + "/pytest_out.txt " + OUT_DIR + "/" + pid + ".pytest.txt", timeout=30)
    import re as _re
    _m = _re.search(r"PYTEST_RC=(\d+)", tout)
    _ptr = _m.group(1) if _m else "?"
    print("TEST-RESULT " + pid + " rc=" + str(trc) + " pytest_rc=" + _ptr + " " + tout[-800:], flush=True)
    if str(_ptr) != "0":
        FAIL_TAILS[pid] = "pytest failed (pytest_rc=" + str(_ptr) + " blocks " + str(len(applied)) + "/" + str(n_bl) + "):\n" + tout[-1500:]
    print("APPLIED " + pid + " " + str(len(applied)) + "/" + str(n_bl) + " blocks", flush=True)
    return "collected len=" + str(len(reply)) + " testrc=" + _ptr + " blocks=" + str(len(applied)) + "/" + str(n_bl)

async def main():
    s = DuckAISession(model="tinfoil/gemma4-31b", timeout=240.0)
    results = {}
    replies = {}
    if True:  # (was try/finally-close; close moved after TURN-2)
        for pid, prompt in PROMPTS.items():
            t = TASKS[pid]
            print("=== TASK " + pid + " (" + t["repo"] + "@" + t["base"][:12] + ") ===", flush=True)
            try:
                reply = await ask(s, pid, prompt)
            except Exception as e:
                print("CHAT-FAIL " + pid + " " + str(e)[:300], flush=True)
                results[pid] = "chat-fail"
                continue
            print("REPLY-OK " + pid + " len=" + str(len(reply)), flush=True)
            replies[pid] = reply
            # SLICE-2: save the FULL raw reply (13920/14258 diagnosis needs
            # the unmodified model text, not just parsed blocks).
            try:
                os.makedirs("/tmp/duck6_out", exist_ok=True)
                open("/tmp/duck6_out/" + pid + ".reply.txt", "w").write(reply)
            except Exception as e:
                print("REPLY-SAVE-FAIL " + pid + " " + str(e)[:120], flush=True)
    # (no close here — session stays open for TURN-2 below; closed after)
    import asyncio as _a
    async def run_one(pid):
        return pid, await _a.to_thread(harness, pid, replies[pid], TASKS[pid])
    out = await _a.gather(*[run_one(pid) for pid in replies])
    for pid, res in out:
        results[pid] = res
        print("SCORED-COLLECTED " + pid + " " + res, flush=True)
    # TURN-2 (SLICE-2): ONE follow-up in the SAME session for actionable
    # harness failures only: pytest_rc=1 (real test failures, e.g. 7427
    # prelocalhost tail), search-miss, empty. Env/collection failures
    # (pytest_rc 2/4/5) are NOT model faults — no retry, no variance burn.
    try:
        t2pids = []
        for pid, res in out:
            if res.startswith("search-miss") or res.startswith("empty") or res.startswith("wrong-file"):
                t2pids.append(pid)
            elif "testrc=1" in res:
                t2pids.append(pid)
        for pid in t2pids:
            tail = FAIL_TAILS.get(pid, "")[-1500:]
            fb = ("HARNESS FEEDBACK on your prior BLOCKS for " + pid + ":\n" + tail
                  + "\nResubmit BLOCKS ONLY (same contract: FILE:/SEARCH/======/>>>>>>, SEARCH copied verbatim from LOCALIZED CODE). Minimal fix only.\n\n" + PROMPTS[pid])
            try:
                reply2 = await s.send(fb, rewrite=REWRITE_LOW_TERSE)
            except Exception as e:
                print("TURN2-FAIL " + pid + " " + str(e)[:200], flush=True)
                continue
            print("REPLY2-OK " + pid + " len=" + str(len(reply2)), flush=True)
            try:
                open("/tmp/duck6_out/" + pid + ".reply2.txt", "w").write(reply2)
            except Exception:
                pass
            res2 = await _a.to_thread(harness, pid, reply2, TASKS[pid])
            results[pid] = res2 + " [turn2]"
            print("SCORED-COLLECTED-T2 " + pid + " " + results[pid], flush=True)
    finally:
        await s.close()
    print("STAGEA-RESULTS " + str(results), flush=True)

asyncio.run(main())
