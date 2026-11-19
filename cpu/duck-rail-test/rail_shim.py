"""Duck-rail OpenAI shim: /v1/models + /v1/chat/completions backed by duck.ai gemma4-31b.
Transport only: stdlib http.server, one DuckAISession per job, always responds (502 JSON
on rail error so the agent takes its retry path instead of hanging)."""
import asyncio
import json
import os
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from duckapi_duckai import DuckAISession

MODEL = "tinfoil/gemma4-31b"
SESSION = None
LOOP = asyncio.new_event_loop()

def get_session():
    global SESSION
    if SESSION is None:
        SESSION = DuckAISession(model=MODEL, timeout=540.0)
    return SESSION

def flatten(messages):
    parts = []
    for m in messages or []:
        role = m.get("role") or "user"
        text = m.get("content") or ""
        if isinstance(text, list):
            text = " ".join(p.get("text", "") for p in text if isinstance(p, dict))
        tag = {"system": "System Instruction", "user": "User", "assistant": "Assistant"}.get(role, str(role).capitalize())
        parts.append("[%s: %s]" % (tag, text) if role == "system" else "%s: %s" % (tag, text))
    out = "\n\n".join(parts)
    if "Assistant:" not in out.split("\n")[-1]:
        out += "\n\nAssistant:"
    return out

def ask(prompt):
    async def go():
        return await get_session().send(prompt, rewrite={"model": MODEL})
    fut = asyncio.run_coroutine_threadsafe(go(), LOOP)
    return fut.result(timeout=600)

class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass
    def _json(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        if self.path.startswith("/v1/models"):
            self._json(200, {"data": [{"id": MODEL, "object": "model"}]})
        else:
            self._json(404, {"error": "nope"})
    def do_POST(self):
        if not self.path.startswith("/v1/chat/completions"):
            return self._json(404, {"error": "nope"})
        try:
            n = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._json(400, {"error": "bad json"})
        try:
            reply = ask(flatten(payload.get("messages")))
            self._json(200, {"choices": [{"message": {"role": "assistant", "content": reply}, "finish_reason": "stop"}]})
        except Exception as e:
            self._json(502, {"error": str(e)[:300]})

if __name__ == "__main__":
    threading.Thread(target=LOOP.run_forever, daemon=True).start()
    ThreadingHTTPServer(("127.0.0.1", 8000)).serve_forever()
