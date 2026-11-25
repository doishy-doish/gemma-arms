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
    """fastapi_14786""": {"repo": """fastapi/fastapi""", "base": """eacbce24c9d299c6a28110d9fc8ac50f53cddb08""", "problem": """""", "hints": """""", "test_patch": """--- a/tests/test_security_http_base.py
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
    """fastapi_13537""": {"repo": """fastapi/fastapi""", "base": """3b4b5ab8c819dce27fbaf0aa0a9c74b7f3255ec0""", "problem": """""", "hints": """""", "test_patch": """--- a/tests/test_form_default.py
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
    """requests_7427""": {"repo": """psf/requests""", "base": """b684dcb9bbf3aa557d1238e72062c4a29737dd1c""", "problem": """""", "hints": """""", "test_patch": """--- a/tests/test_utils.py
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
    """fastapi_15589""": {"repo": """fastapi/fastapi""", "base": """22b02e26f9e8c7e32bd8266e2b0ebe8bb3a0db2b""", "problem": """""", "hints": """""", "test_patch": """--- a/tests/test_query_cookie_header_model_extra_params.py
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
    """fastapi_13920""": {"repo": """fastapi/fastapi""", "base": """0dd42b746e17d33a74ea267a62eace9ccdccf345""", "problem": """""", "hints": """""", "test_patch": """--- a/tests/test_dependency_pep695.py
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
    """fastapi_14258""": {"repo": """fastapi/fastapi""", "base": """e94028ab60d18080810910352bc9129e8046c92d""", "problem": """""", "hints": """""", "test_patch": """--- a/tests/test_router_circular_import.py
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
BUDGET 28 tool calls / 80 turns. TOOLS (reply with exactly one per turn):
<<<TOOL:{"tool":"read_file","filepath":"<path>","start_line":<n>,"end_line":<n>}>>>
<<<TOOL:{"tool":"edit_file","filepath":"<path>","old_string":"<exact>","new_string":"<exact>"}>>>
<<<TOOL:{"tool":"run_command","command":"<shell, 45s max>"}>>>
<<<TOOL:{"tool":"submit_patch"}>>> (only when verified; ends your run)
or plain-text reasoning ending with one of the above. OPERATING ORDER: LOCATE (calls 1-3: grep, read top files, 40-90 line slices), EDIT by 15, VERIFY (heredoc asserts + targeted pytest), SUBMIT max 3 total, never two submits in a row without an edit. NEVER touch tests/conftest. Minimal diff, exact strings. Trail each turn: LOC/EDIT/VERIFY/SUBMIT (<=15 tokens).
Workspace repo is checked out at /work. All paths relative to /work.
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
    if name == "submit_patch":
        rc, out = sh("git add -N . && git diff --stat && git diff > /tmpcv.diff; echo WROTE_RC=$?", work)
        return "SUBMITTED\n" + out[-500:]
    return "ERR unknown tool " + str(name)[:100]

TOOL_RE = re.compile(r"<<<TOOL:(\{.*?\})>>>", re.S)

async def run_task(s, pid):
    t = TASKS[pid]
    work = "/tmp/duck6b_" + pid
    sh("rm -rf " + work + " && mkdir -p " + work, "/tmp")
    urllib.request.urlretrieve("https://github.com/" + t["repo"] + "/archive/" + t["base"] + ".tar.gz", work + "/src.tgz")
    sh("tar xzf src.tgz -C " + work + " --strip-components=1 && rm src.tgz", work, timeout=120)
    sh("git init -q . 2>/dev/null; git add -N . 2>/dev/null; echo ok", work)
    hist = SYS + "\nTASK " + pid + " (" + t["repo"] + "@" + t["base"][:12] + "):\n" + t["problem"] + ("\nHINTS:\n"+t["hints"] if t["hints"] else "")
    calls = 0
    for turn in range(80):
        reply = await s.send(hist[-12000:], rewrite={"model": "tinfoil/gemma4-31b"})
        m = TOOL_RE.search(reply)
        if not m:
            hist += "\n[assistant text, no tool]\n" + reply[-1500:] + "\n[system: reply with exactly one <<<TOOL:{...}>>> per turn]"
            continue
        try: tool = json.loads(m.group(1))
        except Exception: hist += "\n[system: TOOL JSON unparseable, resend]"; continue
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
    sh("git diff > /tmp/duck6b_" + pid + ".diff 2>/dev/null; echo ok", work)
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
