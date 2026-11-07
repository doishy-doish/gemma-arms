"""compile_check.py — byte-compile every changed .py file. stdlib only.

Discovers changed files via git (tracked modifications + untracked,
excluding deleted). Prints OK/FAIL per file. Exit 0 iff all compile.
Test files are compiled too but reported separately (they never score).
"""
import py_compile
import subprocess
import sys
from pathlib import Path

root = Path("/workspace")


def git(*args):
    p = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    if p.returncode != 0:
        return []
    return [l for l in p.stdout.splitlines() if l]


changed = set()
changed.update(git("diff", "--name-only"))
changed.update(git("diff", "--name-only", "--cached"))
changed.update(git("ls-files", "-o", "--exclude-standard"))

pyfiles = sorted(f for f in changed if f.endswith(".py"))
if not pyfiles:
    print("compile_check: no changed .py files")
    sys.exit(0)

failed = 0
for f in pyfiles:
    p = root / f
    tag = "test" if ("test" in f or "conftest" in f) else "src "
    if not p.exists():
        print(f"SKIP [{tag}] {f} (deleted)")
        continue
    try:
        py_compile.compile(str(p), doraise=True)
        print(f"OK   [{tag}] {f}")
    except py_compile.PyCompileError as e:
        failed += 1
        print(f"FAIL [{tag}] {f}: {e}")
print(f"compile_check: {len(pyfiles)} files, {failed} failures")
sys.exit(1 if failed else 0)
