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
    """tornado_s6b""": """
            if hasattr(self, "stream"):
                # TODO: this may cause a StreamClosedError to be raised
                # by the connection's Future.  Should we cancel the
                # connection more gracefully?
                self.stream.close()
            return True
        else:
            # If our callback has already been called, we are probably
            # catching an exception that is not caused by us but rather
            # some child of our callback. Rather than drop it on the floor,
            # pass it along, unless it's just the stream being closed.
            return isinstance(value, StreamClosedError)

    def on_connection_close(self) -> None:
        if self.final_callback is not None:
            message = "Connection closed"
            if self.stream.error:
                raise self.stream.error
            try:
                raise HTTPStreamClosedError(message)
            except HTTPStreamClosedError:
                self._handle_exception(*sys.exc_info())

    async def headers_received(
        self,
        first_line: Union[httputil.ResponseStartLine, httputil.RequestStartLine],
        headers: httputil.HTTPHeaders,
    ) -> None:
        assert isinstance(first_line, httputil.ResponseStartLine)
        if self.request.expect_100_continue and first_line.code == 100:
            await self._write_body(False)
            return
        self.code = first_line.code
        self.reason = first_line.reason
        self.headers = headers

        if self._should_follow_redirect():
            return

        if self.request.header_callback is not None:
            # Reassemble the start line.
            self.request.header_callback("%s %s %s\\r\\n" % first_line)
            for k, v in self.headers.get_all():
                self.request.header_callback("%s: %s\\r\\n" % (k, v))
            self.request.header_callback("\\r\\n")

    def _should_follow_redirect(self) -> bool:
        if self.request.follow_redirects:
            assert self.request.max_redirects is not None
            return (
                self.code in (301, 302, 303, 307, 308)
                and self.request.max_redirects > 0
            )
        return False

    def finish(self) -> None:
        assert self.code is not None
        data = b"".join(self.chunks)
        self._remove_timeout()
        original_request = getattr(self.request, "original_request", self.request)
        if self._should_follow_redirect():
            assert isinstance(self.request, _RequestProxy)
            new_request = copy.copy(self.request.request)
            new_request.url = urllib.parse.urljoin(
                self.request.url, self.headers["Location"]
            )
            new_request.max_redirects = self.request.max_redirects - 1
            del new_request.headers["Host"]
            # http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.4
            # Client SHOULD make a GET request after a 303.
            # According to the spec, 302 should be followed by the same
            # method as the original request, but in practice browsers
            # treat 302 the same as 303, and many servers use 302 for
            # compatibility with pre-HTTP/1.1 user agents which don't
            # understand the 303 status.
            if self.code in (302, 303):
                new_request.method = "GET"
                new_request.body = None
                for h in [
                    "Content-Length",
                    "Content-Type",
                    "Content-Encoding",
                    "Transfer-Encoding",
                ]:
                    try:
                        del self.request.headers[h]
                    except KeyError:
                        pass
            new_request.original_request = original_request
            final_callback = self.final_callback
            self.final_callback = None
            self._release()
            fut = self.client.fetch(new_request, raise_error=False)
            fut.add_done_callback(lambda f: final_callback(f.result()))
            self._on_end_request()
            return
        if self.request.streaming_callback:
            buffer = BytesIO()
        else:
            buffer = BytesIO(data)  # TODO: don't require one big string?
        response = HTTPResponse(
            original_request,
            self.code,
            reason=getattr(self, "reason", None),
            headers=self.headers,
""",
}
ISSUES = {
    """tornado_s6b""": """[ISSUE]
**Title:** HTTP client raises KeyError when handling redirect without 'Location' header

**Description**
When the HTTP client receives a redirect response (e.g., status code 301) without a 'Location' header, it raises a `KeyError`. This unexpected error disrupts the redirect handling process and prevents the client from gracefully managing such responses.

**Example Code**
```python
response = client.fetch("/redirect_without_location", follow_redirects=True)
```

**Expected Behavior**
The client should detect the absence of the 'Location' header in a redirect response and return the response as-is without attempting to follow the redirect. This avoids raising errors and allows the application to handle the situation appropriately.

**Actual Behavior**
A `KeyError: 'Location'` is raised when the client tries to access the missing 'Location' header, causing the request to fail unexpectedly.

[/ISSUE]
""",
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
    """tornado_s6b""": ["""tornado/simple_httpclient.py"""],
}
PROMPTS = {}
for _pid in ISSUES:
    PROMPTS[_pid] = "You are an expert Python engineer. Minimal fix only.\n\n" + ISSUES[_pid] + "\n\nLOCALIZED CODE (verbatim from the base commit; SEARCH blocks must be copied from here byte-for-byte):\n" + SLICES[_pid] + "\n" + CONTRACT
TASKS = {
    """tornado_s6b""": {"repo": """tornadoweb/tornado""", "base": """b399a9d19c45951e4561e6e580d7e8cf396ef9ff""", "test_patch": """--- a/tornado/test/httpclient_test.py
+++ b/tornado/test/httpclient_test.py
@@ -62,6 +62,13 @@ class RedirectHandler(RequestHandler):
         )
 
 
+class RedirectWithoutLocationHandler(RequestHandler):
+    def prepare(self):
+        # For testing error handling of a redirect with no location header.
+        self.set_status(301)
+        self.finish()
+
+
 class ChunkHandler(RequestHandler):
     @gen.coroutine
     def get(self):
@@ -143,6 +150,7 @@ class HTTPClientCommonTestCase(AsyncHTTPTestCase):
                 url("/post", PostHandler),
                 url("/put", PutHandler),
                 url("/redirect", RedirectHandler),
+                url("/redirect_without_location", RedirectWithoutLocationHandler),
                 url("/chunk", ChunkHandler),
                 url("/auth", AuthHandler),
                 url("/countdown/([0-9]+)", CountdownHandler, name="countdown"),
@@ -291,6 +299,14 @@ Transfer-Encoding: chunked
         self.assertTrue(response.effective_url.endswith("/countdown/0"))
         self.assertEqual(b"Zero", response.body)
 
+    def test_redirect_without_location(self):
+        response = self.fetch("/redirect_without_location", follow_redirects=True)
+        # If there is no location header, the redirect response should
+        # just be returned as-is. (This should arguably raise an
+        # error, but libcurl doesn't treat this as an error, so we
+        # don't either).
+        self.assertEqual(301, response.code)
+
     def test_credentials_in_url(self):
         url = self.get_url("/auth").replace("http://", "http://me:secret@")
         response = self.fetch(url)
 
"""},
}
REWRITE_LOW_TERSE = {"model": "tinfoil/gemma4-31b", "reasoningEffort": "low"}
FILE_HINTS = {
    """tornado_s6b""": "",
}
EDGE_HINTS = {
    """tornado_s6b""": "",
}
ORACLES = {
    """tornado_s6b""": "",
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
    """tornado_s6b""": """undefined -k 'test_redirect_without_location'""",
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
        sh("pip install -q tornado 2>&1 | tail -1", timeout=300)
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
