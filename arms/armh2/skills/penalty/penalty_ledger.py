"""penalty_ledger.py - negative-reward gate. stdlib only.

Scores observable violations, reruns the repro against CURRENT code, and
prints itemized deductions plus one verdict line. Exit 0 on GO, 2 on BLOCK.
Run via run_skill_script before submit_patch. Submit ONLY on PENALTY=0 GO.
"""
import json
import py_compile
import subprocess
import sys
from pathlib import Path

root = Path("/workspace")
tmp = Path("/tmp")
hits = []  # (points, code, detail); every hit below BLOCKs submit


def git(*args):
    p = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    if p.returncode != 0:
        return []
    return [l for l in p.stdout.splitlines() if l]


def penalize(points, code, detail):
    hits.append((points, code, detail))


# 1. repro artifact must exist
repros = sorted(tmp.glob("repro_*.py"))
if not repros:
    penalize(50, "no-repro-artifact", "no /tmp/repro_*.py found")

# 2. fail-then-pass chain in the run log (order matters: fail BEFORE final pass)
chains = {}
log = tmp / "repro_runs.jsonl"
if log.is_file():
    for line in log.read_text().splitlines():
        try:
            e = json.loads(line)
        except Exception:
            continue
        if isinstance(e.get("exit"), int):
            chains.setdefault(e.get("file", "?"), []).append(e["exit"])
chained = [f for f, xs in chains.items() if xs and xs[-1] == 0 and any(x != 0 for x in xs[:-1])]
if repros and not chained:
    penalize(50, "no-red-evidence", "no fail-then-pass chain in /tmp/repro_runs.jsonl")

# 3. rerun the chained repro against current code (no logging: this is the check itself)
for f in chained:
    p = tmp / f
    if not p.is_file():
        penalize(50, "repro-missing", f + " logged but file gone")
        continue
    try:
        r = subprocess.run([sys.executable, str(p)], cwd=root,
                           capture_output=True, text=True, timeout=90)
        if r.returncode != 0:
            tail = (r.stdout + r.stderr)[-500:]
            penalize(50, "repro-red-after-edit", f + " exits " + str(r.returncode) + ": " + tail)
    except Exception as e:
        penalize(50, "repro-rerun-error", f + ": " + str(e)[:200])

# 4. byte-compile every changed .py (a syntax break never ships)
changed = set()
changed.update(git("diff", "--name-only"))
changed.update(git("diff", "--name-only", "--cached"))
for f in sorted(f for f in changed if f.endswith(".py")):
    p = root / f
    if not p.exists():
        continue
    try:
        py_compile.compile(str(p), doraise=True)
    except py_compile.PyCompileError as e:
        penalize(25, "compile-fail", f + ": " + str(e)[:200])

# 5. test/config edits are stripped at scoring: pure loss, always punished
PROTECTED_BASENAMES = {"conftest.py", "pytest.ini", ".pytest.ini", "pyproject.toml",
                       "tox.ini", "setup.cfg", "sitecustomize.py", "usercustomize.py",
                       "_swegemma_stubs.py"}
for f in sorted(changed):
    b = f.rsplit("/", 1)[-1]
    if (f.startswith(("tests/", "test/", "testing/")) or b.startswith("test_")
            or b.endswith("_test.py") or b in PROTECTED_BASENAMES or b.endswith(".pth")):
        penalize(20, "protected-touched", f)

# 6. workspace scratch would ship inside the patch via git add -N
EXCLUDED = ("__pycache__", ".pytest_cache", ".egg-info", "build/", "dist/", ".coverage")
scratch = [f for f in git("ls-files", "-o", "--exclude-standard")
           if not f.endswith(".pyc") and not any(x in f for x in EXCLUDED)]
if scratch:
    penalize(10, "workspace-scratch", "untracked under /workspace: " + ", ".join(scratch[:5]))

# 7. spray: size without proof is punished, not rewarded
stat = git("diff", "--stat")
files_n, lines_n = 0, 0
if stat:
    last = stat[-1]
    try:
        import re
        m = re.search(r"(\d+) files? changed", last)
        files_n = int(m.group(1)) if m else 0
        m2 = re.search(r"(\d+) insertions?", last)
        m3 = re.search(r"(\d+) deletions?", last)
        lines_n = (int(m2.group(1)) if m2 else 0) + (int(m3.group(1)) if m3 else 0)
    except Exception:
        pass
d = subprocess.run(["git", "diff", "--binary"], cwd=root, capture_output=True)
if files_n > 6 or lines_n > 2000 or len(d.stdout) > 60000:
    penalize(50, "spray", "diff: %d files, %d lines, %d bytes" % (files_n, lines_n, len(d.stdout)))

total = sum(p for p, _, _ in hits)
verdict = "BLOCK" if hits else "GO"
for p, code, detail in hits:
    print("[-] -%d %s: %s" % (p, code, detail))
print("PENALTY=%d VERDICT=%s" % (total, verdict))
sys.exit(2 if hits else 0)
