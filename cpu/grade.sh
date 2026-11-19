#!/bin/bash
# cpu/grade.sh — verdict ladder L0..L3 for one task. Needs: $WS repo at base,
# results/agent.patch, task json in $TASK_JSON. No secrets.
# Batch-9: emits results/ladder.json — machine-readable D16 meter:
#   tapply (agent patch git-applied), papply (test patch git-applied),
#   collected/failed/errors per phase, L2 (patched suite green, valid),
#   L3flip (per-test flip: graded-passed minus patched-passed), L3.
set -u
WS="${WS:-/tmp/ws}"; RES="${RES:-results}"
mkdir -p "$RES"
if [ -n "${TASK_JSON:-}" ]; then TPY="$(python3 -c "import json;t=json.load(open('$TASK_JSON'));print(' '.join(t.get('test_files') or [t.get('test_file','tests/test_style.py')]))")"; else TPY="${TPY:-tests/test_style.py}"; fi
echo "== L0 path check =="
test -f "$RES/agent.patch" && echo "L0 PASS: patch file exists ($(wc -c < "$RES/agent.patch") bytes)" || { echo "L0 FAIL"; exit 0; }
echo "== base tests =="
for _t in $TPY; do (cd "$WS" && python -m pytest "$_t" -q -W "ignore::DeprecationWarning" 2>&1 | tail -2); done | tee "$RES/pytest-base.log"
echo "== apply agent patch =="
git -C "$WS" reset -q && git -C "$WS" checkout -- . && git -C "$WS" clean -fdq || echo "RESET-WARN"
(cd "$WS" && git apply --check "$OLDPWD/$RES/agent.patch" 2>&1 && git apply "$OLDPWD/$RES/agent.patch" && echo APPLIED || echo "NOT-APPLIED-or-empty") | tee "$RES/apply-agent.txt"
git -C "$WS" status --porcelain=v1 | awk '{print $2}' > "$RES/agent-files.txt" || true
echo "== apply hidden test patch (grade phase only) =="
python - "$TASK_JSON" "$WS" <<'EOF'
import json,sys
t=json.load(open(sys.argv[1])); tp=t['test_patch']; open('/tmp/test_patch.diff','w').write(tp if tp.endswith('\n') else tp+'\n')
EOF
(cd "$WS" && git apply --check /tmp/test_patch.diff 2>&1 && git apply /tmp/test_patch.diff && echo TESTPATCH-APPLIED || echo TESTPATCH-FAIL) | tee "$RES/apply-test.txt"
echo "== patched + graded suites (per-test, D16 meter) =="
python3 - "$WS" "$RES" "$TPY" <<'EOF'
import json, os, re, subprocess, sys
ws, res, tpy = sys.argv[1], sys.argv[2], sys.argv[3].split()
def run(args):
    try:
        p = subprocess.run(['timeout', '280', 'python', '-m', 'pytest'] + args +
            ['-v', '--tb=no', '-p', 'no:cacheprovider', '-W', 'ignore::DeprecationWarning'],
            cwd=ws, capture_output=True, text=True, timeout=300)
        return (p.stdout or '') + '\n' + (p.stderr or '')
    except Exception as e:
        return 'HARNESS-ERR ' + str(e)[:200]
rx = re.compile(r'^(.*)\s(PASSED|FAILED|ERROR|SKIPPED|XFAIL|XPASS)\s*(\[.*\])?$')
def parse(out):
    passed, failed, errors, collected = set(), set(), set(), set()
    for line in out.split('\n'):
        m = rx.match(line.strip())
        if not m: continue
        nid, oc = m.group(1).strip(), m.group(2)
        if '::' not in nid: continue
        collected.add(nid)
        if oc == 'PASSED': passed.add(nid)
        elif oc == 'FAILED': failed.add(nid)
        elif oc == 'ERROR': errors.add(nid)
    return passed, failed, errors, collected, out.split('\n')
os.makedirs(res, exist_ok=True)
p_out = run(tpy)
pp, pf, pe, pc, _ = parse(p_out)
open(os.path.join(res, 'pytest-patched.log'), 'w').write('tail:\n' + '\n'.join(p_out.split('\n')[-15:]))
g_out = run(tpy)
gp, gf, ge, gc, _ = parse(g_out)
open(os.path.join(res, 'pytest-graded.log'), 'w').write('tail:\n' + '\n'.join(g_out.split('\n')[-20:]))
flip = sorted(gp - pp)
row = {
  'patched': {'collected': len(pc), 'failed': len(pf), 'errors': len(pe)},
  'graded': {'collected': len(gc), 'failed': len(gf), 'errors': len(ge)},
  'flip': flip[:50], 'n_flip': len(flip),
}
json.dump(row, open(os.path.join(res, 'ladder-suites.json'), 'w'), indent=1)
print('patched: collected=%d failed=%d errors=%d' % (len(pc), len(pf), len(pe)))
print('graded: collected=%d failed=%d errors=%d flip=%d' % (len(gc), len(gf), len(ge), len(flip)))
EOF
echo "== ladder (D16: valid only if tapply + collected>0 + clean tree-state.txt) =="
python3 - "$RES" <<'EOF'
import json, os, sys
res = sys.argv[1]
s = json.load(open(os.path.join(res, 'ladder-suites.json')))
aa = open(os.path.join(res, 'apply-agent.txt')).read()
at = open(os.path.join(res, 'apply-test.txt')).read()
af = open(os.path.join(res, 'agent-files.txt')).read().split() if os.path.exists(os.path.join(res, 'agent-files.txt')) else []
import re as _re
pol = [f for f in af if _re.search(r'(^|/)tests?/', f) or _re.search(r'(^|/)(test_.*|conftest\.py)$', f) or _re.search(r'\.(cfg|toml|ini|yaml|yml)$', f) or f == 'setup.py']
tapply = 'APPLIED' in aa and 'NOT-APPLIED' not in aa
papply = 'TESTPATCH-APPLIED' in at
lad = {
  'L0': os.path.exists(os.path.join(res, 'agent.patch')),
  'L1': tapply,
  'tapply': tapply,
  'papply': papply,
  'polluted': bool(pol),
  'polluted_files': pol[:10],
  'patched_collected': s['patched']['collected'],
  'patched_failed': s['patched']['failed'],
  'patched_errors': s['patched']['errors'],
  'graded_collected': s['graded']['collected'],
  'graded_failed': s['graded']['failed'],
  'graded_errors': s['graded']['errors'],
  'n_flip': s['n_flip'],
  'flip': s['flip'],
}
lad['L2'] = bool(tapply and not pol and lad['patched_collected'] > 0 and lad['patched_failed'] == 0 and lad['patched_errors'] == 0)
lad['L3'] = bool(tapply and papply and not pol and lad['graded_collected'] > 0 and lad['graded_failed'] == 0 and lad['graded_errors'] == 0 and lad['n_flip'] > 0)
json.dump(lad, open(os.path.join(res, 'ladder.json'), 'w'), indent=1)
print('tapply=%s papply=%s polluted=%s L0=%s L1=%s L2=%s L3=%s flip=%d' % (tapply, papply, bool(pol), lad['L0'], lad['L1'], lad['L2'], lad['L3'], lad['n_flip']))
EOF
