"""Compressed-task CPU probe: 0.5B vs 4B on skeleton twin-enumeration (lean55 base + 172B addition). CPU-only, no GPU."""
import os, json, sys, urllib.request

TOY = {
  "fastapi/routing.py": 'def openapi(prefix=""):\n  return prefix\ndef other():\n  pass\n',
  "fastapi/openapi/utils.py": 'def openapi(prefix=""):\n  return prefix+"/open"\n',
  "fastapi/main.py": 'def unrelated():\n  pass\n',
}
GOLD = sorted(["fastapi/routing.py", "fastapi/openapi/utils.py"])

def skeletonize(repo):
    out = {}
    for p, txt in repo.items():
        lines = txt.split("\n")
        sk = [f"# {p} ({len(lines)} lines)"]
        for i, ln in enumerate(lines):
            import re
            m = re.match(r"^\s*(def|class)\s+([A-Za-z_0-9]+)", ln)
            if m: sk.append(f"{m.group(1)} {m.group(2)} # L{i+1}")
        out[p] = "\n".join(sk)
    return out

SYS_ADD = "Context is skeleton-first (paths+signatures+L#s); full bodies on read_file only.\nFrom TRIGGER grep one shared symbol, enumerate ALL twin files before any edit."

def prompt_for(skel):
    ctx = "\n\n".join(skel.values())
    return f"""Mission: Make the smallest correct change. {SYS_ADD}
TRIGGER: bug in openapi() prefix handling.
SKELETON CONTEXT:
{ctx}
List ALL files that define 'openapi' (exact paths, one per line):"""

def heuristic(symbol="openapi"):
    skel = skeletonize(TOY)
    return sorted([p for p, sk in skel.items() if symbol in sk])

def try_llama(model_path, prompt, n_ctx=2048):
    try:
        from llama_cpp import Llama
        llm = Llama(model_path=model_path, n_ctx=n_ctx, verbose=False)
        out = llm(prompt, max_tokens=128, temperature=0.0)
        txt = out["choices"][0]["text"]
        return txt
    except Exception as e:
        return f"LOAD-INFER-FAIL: {str(e)[:300]}"

def score(txt):
    hits = [g for g in GOLD if g in txt]
    return {"hits": hits, "recall": len(hits)/len(GOLD), "full": len(hits)==len(GOLD)}

if __name__ == "__main__":
    skel = skeletonize(TOY)
    prompt = prompt_for(skel)
    print("=== prompt ===")
    print(prompt[:1200])
    print("=== heuristic (CPU baseline, no model) ===")
    h = heuristic()
    print(h, score(" ".join(h)))
    res = {"heuristic": {"hits": h, **score(" ".join(h))}, "models": {}}
    for tag, path in [("qwen05", os.environ.get("GGUF_05B","")), ("qwen4b", os.environ.get("GGUF_4B",""))]:
        if path and os.path.exists(path):
            print(f"=== {tag}: {path} ===")
            txt = try_llama(path, prompt)
            print(txt[:800])
            s = score(txt)
            print(tag, s)
            res["models"][tag] = {"output": txt[:1000], **s}
        else:
            print(f"=== {tag}: missing file, skipped ===")
            res["models"][tag] = {"skipped": True}
    open(os.environ.get("OUT","compressed-05b-4b-result.json"),"w").write(json.dumps(res, indent=2))
    print("wrote", os.environ.get("OUT","compressed-05b-4b-result.json"))
