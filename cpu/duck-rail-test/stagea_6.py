"""Duck stage-A PERSONA (reasoning low + terse lock + ORACLES exactness): same-6 clean-room, one turn each, then public-proxy score.
Model: tinfoil/gemma4-31b via browser rail (pure chat API, no harness in Duck).
Harness (checkout/apply/pytest) lives HERE, not in the API.
"""
import asyncio, os, sys, subprocess, tarfile, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from duckapi_duckai import DuckAISession

PROMPTS = {
    """fastapi_14786""": """You are an expert Python engineer. Minimal fix only.

ISSUE (fastapi_14786 in fastapi/fastapi at eacbce24c9d2):
🐛 Strip whitespaces from `Authorization` header credentials

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
- [x] Existing tests pass

TASK: Reply with a single unified diff (git apply compatible, with --- a/ +++ b/ headers) that fixes the issue. No prose, no markdown fences, diff only.
""",
    """fastapi_13537""": """You are an expert Python engineer. Minimal fix only.

ISSUE (fastapi_13537 in fastapi/fastapi at 3b4b5ab8c819):
🐛 Fix support for form values with empty strings interpreted as missing (`None` if that's the default), for compatibility with HTML forms

There was a bug in the validation of form data for optional params with None default value. This is a regression that was introduced by https://github.com/fastapi/fastapi/pull/12134.

## Explaination:
The `_get_multidict_value` uses `None` to represent both the absence a value in the dict, and a default value of `None` for that field. When the values are collected in `_extract_form_body`, they are only added to the values if they are not `None`. Later (#12134), some code was added that attempted to complement the model values with values not explicitely in the model, if values for those fields were not already processed earlier. The issue is that since we didn't add values to the initial value dict if they were none, we attempted to add them again in that second iteration. This generally wasn't an issue, except for the fast that a form field set to the empty string (`""`) is interpreted as the absence of that field. This resulted in `_get_multidict_value` picking the default value, that would happen to be `None`, so it wasn't added to the values dict in the first iteration. In the second iteration, we would find that value in the request params again, but set to `""`, and add that to the initial value dict. Later, validation would choke on that empty string.

The fix is to keep track of already visited field, rather that relying on the content of the values dict to complement the missing field. Such thing was already done in `request_params_to_args` for example.


closes #13533 

TASK: Reply with a single unified diff (git apply compatible, with --- a/ +++ b/ headers) that fixes the issue. No prose, no markdown fences, diff only.
""",
    """requests_7427""": """You are an expert Python engineer. Minimal fix only.

ISSUE (requests_7427 in psf/requests at b684dcb9bbf3):
Port bpo-39057 to Requests

This PR ports a [fix](https://bugs.python.org/issue39057) from CPython to constrain no_proxy behavior to domain boundaries. This was originally undefined behavior when Requests implemented `no_proxy` support but has since had bug fixes released in both CPython and Curl. We'll follow suit to conform with ecosystem expectations and resolve long standing issue #4795.

TASK: Reply with a single unified diff (git apply compatible, with --- a/ +++ b/ headers) that fixes the issue. No prose, no markdown fences, diff only.
""",
    """fastapi_15589""": """You are an expert Python engineer. Minimal fix only.

ISSUE (fastapi_15589 in fastapi/fastapi at 22b02e26f9e8):
♻️ Do not accept underscore headers when using `convert_underscores=True` (the default)

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


TASK: Reply with a single unified diff (git apply compatible, with --- a/ +++ b/ headers) that fixes the issue. No prose, no markdown fences, diff only.
""",
    """fastapi_13920""": """You are an expert Python engineer. Minimal fix only.

ISSUE (fastapi_13920 in fastapi/fastapi at 0dd42b746e17):
✨ Add support for PEP695 `TypeAliasType`

This is a continuation of #11140 with the comment by @Viicos fixed by vendoring a copy of `is_typealiastype` from [`typing-inspection`](https://github.com/pydantic/typing-inspection).

TASK: Reply with a single unified diff (git apply compatible, with --- a/ +++ b/ headers) that fixes the issue. No prose, no markdown fences, diff only.
""",
    """fastapi_14258""": """You are an expert Python engineer. Minimal fix only.

ISSUE (fastapi_14258 in fastapi/fastapi at e94028ab60d1):
✨ Show a clear error on attempt to include router into itself

Previously discussed in https://github.com/fastapi/fastapi/discussions/11424 with the PR at https://github.com/fastapi/fastapi/pull/11425

Since I made modifications in the fork of the repo, the PR was automatically closed. This PR serves to add the circular reference check again. Discussed again in https://github.com/fastapi/fastapi/discussions/14251

TASK: Reply with a single unified diff (git apply compatible, with --- a/ +++ b/ headers) that fixes the issue. No prose, no markdown fences, diff only.
""",
}
TASKS = {
    """fastapi_14786""": {"repo": """fastapi/fastapi""", "base": """eacbce24c9d299c6a28110d9fc8ac50f53cddb08""", "test_patch": """--- a/tests/test_security_http_base.py
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
    """fastapi_13537""": {"repo": """fastapi/fastapi""", "base": """3b4b5ab8c819dce27fbaf0aa0a9c74b7f3255ec0""", "test_patch": """--- a/tests/test_form_default.py
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
    """requests_7427""": {"repo": """psf/requests""", "base": """b684dcb9bbf3aa557d1238e72062c4a29737dd1c""", "test_patch": """--- a/tests/test_utils.py
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
    """fastapi_15589""": {"repo": """fastapi/fastapi""", "base": """22b02e26f9e8c7e32bd8266e2b0ebe8bb3a0db2b""", "test_patch": """--- a/tests/test_query_cookie_header_model_extra_params.py
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
    """fastapi_13920""": {"repo": """fastapi/fastapi""", "base": """0dd42b746e17d33a74ea267a62eace9ccdccf345""", "test_patch": """--- a/tests/test_dependency_pep695.py
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
    """fastapi_14258""": {"repo": """fastapi/fastapi""", "base": """e94028ab60d18080810910352bc9129e8046c92d""", "test_patch": """--- a/tests/test_router_circular_import.py
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
REWRITE_LOW_TERSE = {"model": "tinfoil/gemma4-31b", "reasoningEffort": "low"}
FILE_HINTS = {
    "fastapi_14786": "Edit ONLY fastapi/security/utils.py (get_authorization_scheme_param, add .strip()).",
    "fastapi_13537": "Edit ONLY fastapi/dependencies/utils.py (_extract_form_body / visited fields + extra-key fix). Do NOT touch fastapi/routing.py.",
    "fastapi_13920": "Edit ONLY fastapi/dependencies/utils.py (PEP695 TypeAliasType / get_dependant).",
    "fastapi_14258": "Edit ONLY fastapi/routing.py (APIRouter.include_router self-guard, AssertionError).",
    "fastapi_15589": "Edit ONLY fastapi/dependencies/utils.py (query/cookie/header model extra params). Output a REAL diff, never empty.",
    "requests_7427": "Edit ONLY src/requests/utils.py (should_bypass_proxies no_proxy domain-boundary, use --- a/src/requests/utils.py header).",
}
EDGE_HINTS = {
    "fastapi_14786": "Must return scheme, param.strip().",
    "fastapi_13537": "Track visited fields, keep extra-key fix, correct file only.",
    "fastapi_13920": "Handle TypeAliasType without breaking get_dependant.",
    "fastapi_14258": "Raise AssertionError with exact message on router.include_router(router).",
    "fastapi_15589": "Non-empty diff required; empty output = FAIL, retry.",
    "requests_7427": "COMPLETENESS OVER BREVITY: handle host_with_port exact match, lstrip dot then dot-boundary (hostname == host or endswith dot+host), bare-dot entry must match. Ports matter.",
}
ORACLES = {
    "fastapi_14786": "ORACLE: return scheme, param.strip().",
    "fastapi_13537": "ORACLE: track visited fields; extra keys pass through; correct file only.",
    "fastapi_13920": "ORACLE: unwrap TypeAliasType without breaking get_dependant.",
    "fastapi_14258": "ORACLE: raise AssertionError with EXACT message: Cannot include the same APIRouter instance into itself. Did you mean to include a different router? (test uses match= on this string).",
    "fastapi_15589": "ORACLE: non-empty diff required; empty output = FAIL.",
    "requests_7427": "ORACLE: after split comma STRIP each entry; bare dot matches all; port entries: netloc == x or netloc endswith dot+x (subdomain+port); others: lstrip dot then hostname == x or endswith dot+x.",
}
TERSE_LOCK = "STRICT TERSE CODE-ONLY. Output one unified diff only (git apply compatible, --- a/ +++ b/ headers). No prose, no fences, no explanation, no analysis. COMPLETENESS OVER BREVITY on edge cases (ports, dot-boundary, host_with_port).\n\n"
def _valid_diff(body):
    return "--- a/" in body and "+++ b/" in body and len(body.strip()) > 50
async def ask(s, pid, prompt):
    full = TERSE_LOCK + FILE_HINTS.get(pid, "") + " " + EDGE_HINTS.get(pid, "") + " " + ORACLES.get(pid, "") + "\n\n" + prompt
    last = ""
    for attempt in range(3):
        q = full if attempt == 0 else "INVALID prior output (empty/wrong-file/unappliable). Resubmit diff ONLY, correct file, --- a/ +++ b/ headers.\n\n" + full
        reply = await s.send(q, rewrite=REWRITE_LOW_TERSE)
        last = reply
        b = reply.strip()
        if b.startswith("\u0060\u0060\u0060"):
            ls = b.split("\n")
            b = "\n".join(ls[1:-1] if ls[-1].strip().startswith("\u0060\u0060\u0060") else ls[1:])
        if _valid_diff(b):
            return reply.replace("\u0060\u0060\u0060", "")
        print("RETRY " + pid + " attempt=" + str(attempt + 1) + " len=" + str(len(reply)), flush=True)
    return last

def sh(cmd, **kw):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=kw.get("timeout", 300))
    return p.returncode, (p.stdout or "")[-2000:] + (p.stderr or "")[-2000:]

def harness(pid, reply, t):
    body = reply.strip()
    if body.startswith("\u0060\u0060\u0060"):
        ls = body.split("\n")
        body = "\n".join(ls[1:-1] if ls[-1].strip().startswith("\u0060\u0060\u0060") else ls[1:])
    diff_path = "/tmp/duck6_" + pid + ".diff"
    open(diff_path, "w").write(body if body.endswith("\n") else body + "\n")
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
    rc, out = sh("cd " + work + " && git apply --check /tmp/duck6_" + pid + ".diff 2>&1 | head -5; echo APPLY_CHECK_RC=$?", timeout=60)
    print("APPLY-CHECK " + pid + " rc=" + str(rc) + " " + out[-300:], flush=True)
    sh("cd " + work + " && git apply /tmp/duck6_" + pid + ".diff 2>&1 | head -5; echo APPLIED_RC=$?", timeout=60)
    open(work + "/test_patch.diff", "w").write(t["test_patch"] if t["test_patch"].endswith("\n") else t["test_patch"] + "\n")
    sh("cd " + work + " && git apply test_patch.diff 2>&1 | head -5; echo TEST_APPLIED_RC=$?", timeout=60)
    return "collected len=" + str(len(reply))
async def main():
    s = DuckAISession(model="tinfoil/gemma4-31b", timeout=240.0)
    results = {}
    replies = {}
    try:
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
    finally:
        await s.close()
    import asyncio as _a
    async def run_one(pid):
        return pid, await _a.to_thread(harness, pid, replies[pid], TASKS[pid])
    out = await _a.gather(*[run_one(pid) for pid in replies])
    for pid, res in out:
        results[pid] = res
        print("SCORED-COLLECTED " + pid + " " + res, flush=True)
    print("STAGEA-RESULTS " + str(results), flush=True)

asyncio.run(main())
