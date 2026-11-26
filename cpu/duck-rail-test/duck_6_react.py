"""Duck stage-B: same-harness ReAct replay of the 6-task canary.
Same loop as the 31B bakes (OPERATING ORDER, same 4 tools, same budgets),
only the LLM is tinfoil/gemma4-31b via the browser rail (pure chat API).
Deltas vs Kaggle bake, honestly labeled: online (needs net), different serving
stack/decoding, no thinking-budget control, single-threaded turns, submit =
saved diff artifact (no hidden scorer on GH; proxy score = test_patch+pytest).
"""
import asyncio, os, sys, subprocess, json, urllib.request, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from duckapi_duckai import DuckAISession

TASKS = {
    """fastapi_14786""": {"repo": """fastapi/fastapi""", "base": """eacbce24c9d299c6a28110d9fc8ac50f53cddb08""", "problem": """🐛 Strip whitespaces from `Authorization` header credentials

## Description

Fixes whitespace handling in authorization header parameter extraction to comply with [RFC 6750](https://datatracker.ietf.org/doc/html/rfc6750#section-2.1).

## Problem

The current implementation preserves leading/trailing whitespace in the extracted credential parameter. While RFC 6750 allows one or more spaces (`1*SP`) between "Bearer" and the token, the token definition (`b64token`) doesn't include whitespace characters, meaning spaces should be treated as separators only.

This causes the extracted credentials to include extraneous whitespace, which can lead to authentication failures.

## Solution

Added `.strip()` to the parameter extraction to remove leading and trailing whitespace:
```python
return scheme, param.strip()
```

## Reproduction

### Before the fix:
```python
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

app = FastAPI()
security = HTTPBearer()

@app.get("/users/me")
def read_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
):
    return {"scheme": credentials.scheme, "credentials": credentials.credentials}
```

**Test case 1: Single space (correct)**
```bash
curl -X 'GET' \\
  'http://127.0.0.1:8000/users/me' \\
  -H 'Authorization: Bearer xxx'
```
Response: `{"scheme":"Bearer","credentials":"xxx"}` ✓

**Test case 2: Multiple spaces**
```bash
curl -X 'GET' \\
  'http://127.0.0.1:8000/users/me' \\
  -H 'Authorization: Bearer   xxx'
```
Response: `{"scheme":"Bearer","credentials":"  xxx"}` ✗

**Test case 3: Trailing whitespace**
```bash
curl -X 'GET' \\
  'http://127.0.0.1:8000/users/me' \\
  -H 'Authorization: Bearer xxx '
```
Response: `{"scheme":"Bearer","credentials":"xxx "}` ✗

### After the fix:

All three test cases now return: `{"scheme":"Bearer","credentials":"xxx"}` ✓

## Changes

- Modified `get_authorization_scheme_param()` in `fastapi/security/utils.py` to strip whitespace from the parameter
- Added test cases to verify the fix handles multiple spaces and trailing whitespace correctly

## Checklist

- [x] Tests added to cover the bug fix
- [x] Existing tests pass""""""", "hints": """""""""", "test_patch": """--- a/tests/test_security_http_base.py
+++ b/tests/test_security_http_base.py
@@ -21,6 +21,12 @@ def test_security_http_base():
     assert response.json() == {"scheme": "Other", "credentials": "foobar"}
 
 
+def test_security_http_base_with_whitespaces():
+    response = client.get("/users/me", headers={"Authorization": "Other  foobar "})
+    assert response.status_code == 200, response.text
+    assert response.json() == {"scheme": "Other", "credentials": "foobar"}
+
+
 def test_security_http_base_no_credentials():
     response = client.get("/users/me")
     assert response.status_code == 401, response.text
--- a/tests/test_security_oauth2_authorization_code_bearer.py
+++ b/tests/test_security_oauth2_authorization_code_bearer.py
@@ -37,6 +37,12 @@ def test_token():
     assert response.json() == {"token": "testtoken"}
 
 
+def test_token_with_whitespaces():
+    response = client.get("/items", headers={"Authorization": "Bearer  testtoken "})
+    assert response.status_code == 200, response.text
+    assert response.json() == {"token": "testtoken"}
+
+
 def test_openapi_schema():
     response = client.get("/openapi.json")
     assert response.status_code == 200, response.text"""},
    """fastapi_13537""": {"repo": """fastapi/fastapi""", "base": """3b4b5ab8c819dce27fbaf0aa0a9c74b7f3255ec0""", "problem": """🐛 Fix support for form values with empty strings interpreted as missing (`None` if that's the default), for compatibility with HTML forms

There was a bug in the validation of form data for optional params with None default value. This is a regression that was introduced by https://github.com/fastapi/fastapi/pull/12134.

## Explaination:
The `_get_multidict_value` uses `None` to represent both the absence a value in the dict, and a default value of `None` for that field. When the values are collected in `_extract_form_body`, they are only added to the values if they are not `None`. Later (#12134), some code was added that attempted to complement the model values with values not explicitely in the model, if values for those fields were not already processed earlier. The issue is that since we didn't add values to the initial value dict if they were none, we attempted to add them again in that second iteration. This generally wasn't an issue, except for the fast that a form field set to the empty string (`""`) is interpreted as the absence of that field. This resulted in `_get_multidict_value` picking the default value, that would happen to be `None`, so it wasn't added to the values dict in the first iteration. In the second iteration, we would find that value in the request params again, but set to `""`, and add that to the initial value dict. Later, validation would choke on that empty string.

The fix is to keep track of already visited field, rather that relying on the content of the values dict to complement the missing field. Such thing was already done in `request_params_to_args` for example.


closes #13533 """"""", "hints": """""""""", "test_patch": """--- a/tests/test_form_default.py
+++ b/tests/test_form_default.py
@@ -0,0 +1,35 @@
+from typing import Optional
+
+from fastapi import FastAPI, File, Form
+from starlette.testclient import TestClient
+from typing_extensions import Annotated
+
+app = FastAPI()
+
+
+@app.post("/urlencoded")
+async def post_url_encoded(age: Annotated[Optional[int], Form()] = None):
+    return age
+
+
+@app.post("/multipart")
+async def post_multi_part(
+    age: Annotated[Optional[int], Form()] = None,
+    file: Annotated[Optional[bytes], File()] = None,
+):
+    return {"file": file, "age": age}
+
+
+client = TestClient(app)
+
+
+def test_form_default_url_encoded():
+    response = client.post("/urlencoded", data={"age": ""})
+    assert response.status_code == 200
+    assert response.text == "null"
+
+
+def test_form_default_multi_part():
+    response = client.post("/multipart", data={"age": ""})
+    assert response.status_code == 200
+    assert response.json() == {"file": None, "age": None}"""},
    """requests_7427""": {"repo": """psf/requests""", "base": """b684dcb9bbf3aa557d1238e72062c4a29737dd1c""", "problem": """Port bpo-39057 to Requests

This PR ports a [fix](https://bugs.python.org/issue39057) from CPython to constrain no_proxy behavior to domain boundaries. This was originally undefined behavior when Requests implemented `no_proxy` support but has since had bug fixes released in both CPython and Curl. We'll follow suit to conform with ecosystem expectations and resolve long standing issue #4795.""""""", "hints": """""""""", "test_patch": """--- a/tests/test_utils.py
+++ b/tests/test_utils.py
@@ -844,6 +844,29 @@ def test_should_bypass_proxies_no_proxy(url, expected, monkeypatch):
     assert should_bypass_proxies(url, no_proxy=no_proxy) == expected
 
 
+@pytest.mark.parametrize(
+    "url, expected",
+    (
+        ("http://localhost/", True),
+        ("http://anotherdomain.com:8888/", True),
+        ("http://newdomain.com:1234/", True),
+        ("http://www.newdomain.com:1234/", True),
+        ("http://foo.d.o.t/", True),
+        ("http://d.o.t/", True),
+        ("http://prelocalhost/", False),
+        ("http://newdomain.com/", False),
+        ("http://newdomain.com:1235/", False),
+    ),
+)
+def test_should_bypass_proxies_no_proxy_domain_boundary(url, expected):
+    \"\"\"Ensure no_proxy matching respects domain boundaries and does not
+    greedily match domains that merely endswith the no_proxy entry.
+    See CPython bpo-39057.
+    \"\"\"
+    no_proxy = "localhost, anotherdomain.com, newdomain.com:1234, .d.o.t"
+    assert should_bypass_proxies(url, no_proxy=no_proxy) == expected
+
+
 @pytest.mark.skipif(os.name != "nt", reason="Test only on Windows")
 @pytest.mark.parametrize(
     "url, expected, override","""},
    """fastapi_15589""": {"repo": """fastapi/fastapi""", "base": """22b02e26f9e8c7e32bd8266e2b0ebe8bb3a0db2b""", "problem": """♻️ Do not accept underscore headers when using `convert_underscores=True` (the default)

## Pull Request

<!--
Please start with a GitHub Discussion.

Once a team member asks you to open a PR, create it and link the discussion here.

Obvious typo fixes can be made in a PR without starting a discussion.
-->

Discussion: <!-- Link to the GitHub Discussion -->

## Description

♻️ Do not accept underscore headers when using `convert_underscores=True` (the default)

This means it would only accept header names separated with hyphens by default, and to accept header names separated with underscores, an app would need to explicitly set `convert_underscores=False`.

<!-- Write the description of your PR here -->

## AI Disclaimer

<!-- If using AI, write here the prompt and model used -->

<details>
<summary>AI transcript</summary>

<!-- Paste here the entire AI transcript -->

</details>

## Checklist

- [ ] This PR is an obvious typo fix, or it links to a GitHub Discussion for the proposed code change.
- [ ] I added tests for the change.
- [ ] The new or updated tests fail on the main branch and pass on this PR.
- [ ] Coverage stays at 100%.
- [ ] The documentation explains the change if needed.
""""""", "hints": """""""""", "test_patch": """--- a/tests/test_query_cookie_header_model_extra_params.py
+++ b/tests/test_query_cookie_header_model_extra_params.py
@@ -11,6 +11,10 @@ class Model(BaseModel):
     model_config = {"extra": "allow"}
 
 
+class AuthHeaders(BaseModel):
+    x_user_id: str
+
+
 @app.get("/query")
 async def query_model_with_extra(data: Model = Query()):
     return data
@@ -26,6 +30,11 @@ async def cookies_model_with_extra(data: Model = Cookie()):
     return data
 
 
+@app.get("/header-requires-hyphen")
+async def header_model_requires_hyphen(data: AuthHeaders = Header()):
+    return data
+
+
 def test_query_pass_extra_list():
     client = TestClient(app)
     resp = client.get(
@@ -91,6 +100,32 @@ def test_header_pass_extra_single():
     assert resp_json["param2"] == "456"
 
 
+def test_header_model_prefers_hyphenated_header_with_convert_underscores():
+    client = TestClient(app)
+
+    resp = client.get(
+        "/header-requires-hyphen",
+        headers=[
+            ("x-user-id", "hyphenated-value"),
+            ("x_user_id", "underscore-value"),
+        ],
+    )
+
+    assert resp.status_code == 200
+    assert resp.json() == {"x_user_id": "hyphenated-value"}
+
+
+def test_header_model_rejects_underscore_header_with_convert_underscores():
+    client = TestClient(app)
+
+    resp = client.get(
+        "/header-requires-hyphen", headers={"x_user_id": "underscore-value"}
+    )
+
+    assert resp.status_code == 422
+    assert resp.json()["detail"][0]["loc"] == ["header", "x_user_id"]
+
+
 def test_cookie_pass_extra_list():
     client = TestClient(app)
     client.cookies = ["""},
    """fastapi_13920""": {"repo": """fastapi/fastapi""", "base": """0dd42b746e17d33a74ea267a62eace9ccdccf345""", "problem": """✨ Add support for PEP695 `TypeAliasType`

This is a continuation of #11140 with the comment by @Viicos fixed by vendoring a copy of `is_typealiastype` from [`typing-inspection`](https://github.com/pydantic/typing-inspection).""""""", "hints": """""""""", "test_patch": """--- a/tests/test_dependency_pep695.py
+++ b/tests/test_dependency_pep695.py
@@ -0,0 +1,27 @@
+from typing import Annotated
+
+from fastapi import Depends, FastAPI
+from fastapi.testclient import TestClient
+from typing_extensions import TypeAliasType
+
+
+async def some_value() -> int:
+    return 123
+
+
+DependedValue = TypeAliasType(
+    "DependedValue", Annotated[int, Depends(some_value)], type_params=()
+)
+
+
+def test_pep695_type_dependencies():
+    app = FastAPI()
+
+    @app.get("/")
+    async def get_with_dep(value: DependedValue) -> str:  # noqa
+        return f"value: {value}"
+
+    client = TestClient(app)
+    response = client.get("/")
+    assert response.status_code == 200
+    assert response.text == '"value: 123"'"""},
    """fastapi_14258""": {"repo": """fastapi/fastapi""", "base": """e94028ab60d18080810910352bc9129e8046c92d""", "problem": """✨ Show a clear error on attempt to include router into itself

Previously discussed in https://github.com/fastapi/fastapi/discussions/11424 with the PR at https://github.com/fastapi/fastapi/pull/11425

Since I made modifications in the fork of the repo, the PR was automatically closed. This PR serves to add the circular reference check again. Discussed again in https://github.com/fastapi/fastapi/discussions/14251""""""", "hints": """""""""", "test_patch": """--- a/tests/test_router_circular_import.py
+++ b/tests/test_router_circular_import.py
@@ -0,0 +1,12 @@
+import pytest
+from fastapi import APIRouter
+
+
+def test_router_circular_import():
+    router = APIRouter()
+
+    with pytest.raises(
+        AssertionError,
+        match="Cannot include the same APIRouter instance into itself. Did you mean to include a different router?",
+    ):
+        router.include_router(router)"""},
}
SYS = """You are an expert autonomous software engineer resolving a GitHub issue in a Python repo. Ship the smallest fix that makes hidden tests pass.
BUDGET 28 calls / 80 turns / 45s per command. get_status is FREE (never counts) -- call before >20s commands.
OPERATING ORDER -- LOCATE, EDIT by 15, VERIFY, SUBMIT EARLY AND OFTEN:
1. LOCATE 1-3: ONE sweep: git grep -n "<id1>|<id2>|<error-msg>" -- '*.py' | head -30. Phonebook: exact-match, caller, sibling, config -- read top 3-5 first, 40-90 line slices. Never ls -R / find . / cat whole files. Copy exception text -- assert vs raise fails hidden tests. No exploration after 30.
2. EDIT by 15: MUST have edited source by 15. Minimal diff, exact strings, no reformat. NEVER touch tests, pytest.ini, conftest.py (harness-committed). Fix cause, not symptom.
3. VERIFY (2 calls per cycle, max 2 cycles): call-1 ONE heredoc: python3 - <<'EOF' (assert __file__ inside work dir; py_compile edited files; run /tmp/repro_<id>.py edge asserts) EOF. call-2 ONLY if call-1 green: git diff --check; timeout 40 python -m pytest tests/test_target.py -k test_feature -q -x --tb=line; git diff --stat. 0 collected = RED, never submit on zero tests. Fallbacks: --noconftest -o addopts="" then direct asserts. Never bare pytest. PYTHONPATH=work dir always. Validity re-check: tree changed since LOCATE? re-confirm state before acting -- stale evidence fails, no extra calls.
4. SUBMIT (max 3 total): only after green call-2 -- unverified submit fails like no submit. After first green call-2, submit_patch. Never two submits in a row without an edit between. diff --stat must show source-only MODIFIED, patch_size>0 -- else edit+resubmit. Never end unsubmitted. K=3 ABORT: keep cleanest compilable diff and submit.
5. RESTART-40 (free 2nd pass): at 40 calls with no submit: write tried/failed/untried, restart untried-only, new plan.
Trail: LOC:<f:fn>|EDIT:done|VERIFY:<r>|SUBMIT:<sz> (<=15 tok).
TOOLS (reply with exactly one per turn):
<<<TOOL:{"tool":"read_file","filepath":"<path>","start_line":<n>,"end_line":<n>}>>>
<<<TOOL:{"tool":"edit_file","filepath":"<path>","old_string":"<exact>","new_string":"<exact>"}>>>
<<<TOOL:{"tool":"write_file","filepath":"<path>","content":"<full file text>"}>>>
<<<TOOL:{"tool":"run_command","command":"<shell, 45s max>"}>>>
<<<TOOL:{"tool":"get_status"}>>> (FREE -- calls used/left, turns, diff stat; use before long commands)
<<<TOOL:{"tool":"submit_patch"}>>> (only when verified; ends your run)
or plain-text reasoning ending with one of the above.
DUCK DELTAS (honest, vs Kaggle bake): online GH runner (needs net ok); different serving/decoding, no thinking-budget control and no temperature control (Kaggle temp 0.2 top_p 0.95 max 3072 thinking 768 N/A here); single-threaded turns; submit = saved diff artifact (no hidden scorer on GH; proxy score = test_patch+pytest); prompt clamp 12K chars head+tail on over-long sends; repo checked out at /tmp/duck6b_<id> (R11 says /workspace -- read as work dir). All paths relative to work dir.
"""

def sh(cmd, work, timeout=60):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout, cwd=work)
    out = ((p.stdout or "") + (p.stderr or ""))[-2500:]
    return p.returncode, out

def do_tool(tool, work):
    name = tool.get("tool")
    if name == "read_file":
        fp = tool.get("filepath",""); a = int(tool.get("start_line",1)); b = int(tool.get("end_line",a+90))
        try:
            lines = open(os.path.join(work,fp)).read().split("\n")
            return "OK\n" + "\n".join("%d:%s"%(i+1,lines[i]) for i in range(max(0,a-1), min(len(lines),b)))
        except Exception as e: return "ERR " + str(e)[:300]
    if name == "edit_file":
        fp = tool.get("filepath",""); old = tool.get("old_string",""); new = tool.get("new_string","")
        try:
            p = os.path.join(work,fp); s = open(p).read()
            if old not in s: return "ERR old_string not found"
            open(p,"w").write(s.replace(old,new,1)); return "OK edited " + fp
        except Exception as e: return "ERR " + str(e)[:300]
    if name == "run_command":
        try:
            rc, out = sh(tool.get("command","echo hi"), work, timeout=45)
            return ("OK rc=%d\n"%rc) + out[-2000:]
        except Exception as e: return "ERR " + str(e)[:300]
    if name == "write_file":
        fp = tool.get("filepath",""); content = tool.get("content","")
        try:
            p = os.path.join(work,fp); os.makedirs(os.path.dirname(p) or work, exist_ok=True)
            open(p,"w").write(content); return "OK wrote " + fp + " bytes=" + str(len(content))
        except Exception as e: return "ERR " + str(e)[:300]
    if name == "get_status":
        try:
            rc, out = sh("git diff --stat HEAD -- fastapi requests src 2>/dev/null | tail -5; echo ---; git status --short -- fastapi requests src 2>/dev/null | head -10", work)
            return ("STATUS calls=%d turns=%d\n" % (calls, turn)) + out[-800:]
        except Exception as e: return "ERR " + str(e)[:300]
    if name == "submit_patch":
        # M390 fix: base is COMMITTED at setup, so plain `git diff HEAD` scoped to
        # source dirs shows only agent modifications (the old `git add -N .` dumped
        # the whole tarball as new files = 19MB noise artifact). New .py files the
        # agent created via shell are appended as /dev/null hunks.
        rc, out = sh("git diff HEAD -- fastapi requests src > /tmpcv.diff; for f in $(git ls-files --others --exclude-standard -- fastapi requests src 2>/dev/null | grep -E '\\.py$'); do git diff --no-index -- /dev/null \"$f\" 2>/dev/null | tail -n +2 >> /tmpcv.diff; done; echo WROTE_RC=$?; wc -c /tmpcv.diff", work)
        return "SUBMITTED\n" + out[-500:]
    return "ERR unknown tool " + str(name)[:100]

TOOL_RE = re.compile(r"<<<TOOL:(\{.*?\})>>>", re.S)

async def run_task(s, pid):
    t = TASKS[pid]
    work = "/tmp/duck6b_" + pid
    sh("rm -rf " + work + " && mkdir -p " + work, "/tmp")
    urllib.request.urlretrieve("https://github.com/" + t["repo"] + "/archive/" + t["base"] + ".tar.gz", work + "/src.tgz")
    sh("tar xzf src.tgz -C " + work + " --strip-components=1 && rm src.tgz", work, timeout=120)
    sh("git init -q . 2>/dev/null; git add -A 2>/dev/null; git -c user.email=t@t -c user.name=t commit -qm base 2>/dev/null; echo ok", work)
    hist = SYS + "\nTASK " + pid + " (" + t["repo"] + "@" + t["base"][:12] + "):\n" + t["problem"] + ("\nHINTS:\n"+t["hints"] if t["hints"] else "")
    calls = 0
    submitted = 0
    edited_since_submit = True
    for turn in range(80):
        reply = await s.send(hist[-12000:], rewrite={"model": "tinfoil/gemma4-31b"})
        m = TOOL_RE.search(reply)
        if not m:
            hist += "\n[assistant text, no tool]\n" + reply[-1500:] + "\n[system: reply with exactly one <<<TOOL:{...}>>> per turn]"
            continue
        try: tool = json.loads(m.group(1))
        except Exception: hist += "\n[system: TOOL JSON unparseable, resend]"; continue
        if tool.get("tool") == "get_status":
            obs = do_tool(tool, work)
            hist += "\n[tool get_status ->]\n" + obs[-800:]
            continue
        if tool.get("tool") == "submit_patch" and calls >= 28:
            hist += "\n[system: call budget exhausted, submit refused]"; continue
        if tool.get("tool") != "submit_patch": calls += 1
        if calls > 28 and tool.get("tool") != "submit_patch":
            hist += "\n[system: 28-call budget spent; submit now or stop]"; continue
        obs = do_tool(tool, work)
        hist += "\n[tool " + tool.get("tool","?") + " ->]\n" + obs[-2000:]
        print(pid + " turn=%d calls=%d tool=%s obs=%.120s" % (turn, calls, tool.get("tool"), obs.replace("\n"," ")), flush=True)
        if obs.startswith("SUBMITTED"):
            sh("cp /tmpcv.diff /tmp/duck6b_" + pid + ".diff 2>/dev/null; echo ok", "/tmp")
            return "submitted calls=%d turns=%d" % (calls, turn)
    sh("git diff HEAD -- fastapi requests src > /tmp/duck6b_" + pid + ".diff 2>/dev/null; echo ok", work)
    return "budget-out calls=%d" % calls

async def main():
    only = os.environ.get("TASK_ID", "").strip()
    order = [only] if only in TASKS else ["fastapi_14786","fastapi_13537","requests_7427","fastapi_15589","fastapi_13920","fastapi_14258"]
    s = DuckAISession(model="tinfoil/gemma4-31b", timeout=240.0)
    res = {}
    try:
        for pid in order:
            print("=== TASK " + pid + " ===", flush=True)
            try: res[pid] = await run_task(s, pid)
            except Exception as e: res[pid] = "FAIL " + str(e)[:200]
            print("RESULT " + pid + " " + res[pid], flush=True)
    finally:
        await s.close()
    print("STAGEB-RESULTS " + json.dumps(res), flush=True)

asyncio.run(main())
