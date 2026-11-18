#!/usr/bin/env python3
"""Pre-submit invariant gate (portable, ~30 lines). Run BEFORE submit_patch.
Usage: python pre_submit_gate.py <repo_dir>  -> exit 0 = shippable, 1 = blocked + reason.
Port: call via run_command in the agent bundle right before submit_patch."""
import ast, os, subprocess, sys

def changed(repo):
    p = subprocess.run(["git", "diff", "--name-only", "HEAD", "--", "."],
                       capture_output=True, text=True, cwd=repo)
    return [l for l in (p.stdout or "").split("\n") if l]

def main():
    repo = sys.argv[1] if len(sys.argv) > 1 else "."
    ch = changed(repo)
    bad = [f for f in ch if f.startswith("tests/") or f.endswith((".cfg", ".toml", ".ini"))]
    if bad:
        print("BLOCK allowlist: " + ",".join(bad[:8])); return 1
    pys = [f for f in ch if f.endswith(".py")]
    for f in pys:
        try: ast.parse(open(os.path.join(repo, f)).read())
        except Exception as e: print("BLOCK ast: %s (%s)" % (f, e)); return 1
    if pys:
        r = subprocess.run([sys.executable, "-m", "py_compile"] + pys,
                           capture_output=True, text=True, cwd=repo)
        if r.returncode != 0:
            print("BLOCK compile: " + (r.stderr or "")[-300:]); return 1
    print("GATE-OK %d files (%d py)" % (len(ch), len(pys))); return 0

if __name__ == "__main__": sys.exit(main())
