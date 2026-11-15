#!/bin/bash
# cpu/grade.sh — verdict ladder L0..L3 for one smoke task. Needs: $WS repo at base,
# results/agent.patch, task json in $TASK_JSON. No secrets.
set -u
WS="${WS:-/tmp/ws}"; RES="${RES:-results}"
if [ -n "${TASK_JSON:-}" ]; then TPY="$(python3 -c "import json;t=json.load(open('$TASK_JSON'));print(' '.join(t.get('test_files') or [t.get('test_file','tests/test_style.py')]))")"; else TPY="${TPY:-tests/test_style.py}"; fi
echo "== L0 path check =="
test -f "$RES/agent.patch" && echo "L0 PASS: patch file exists ($(wc -c < "$RES/agent.patch") bytes)" || { echo "L0 FAIL"; exit 0; }
echo "== base tests =="
for _t in $TPY; do (cd "$WS" && python -m pytest "$_t" -q 2>&1 | tail -2); done | tee "$RES/pytest-base.log"
echo "== apply agent patch =="
(cd "$WS" && git apply --check "$OLDPWD/$RES/agent.patch" 2>&1 && git apply "$OLDPWD/$RES/agent.patch" && echo APPLIED || echo "NOT-APPLIED-or-empty")
for _t in $TPY; do (cd "$WS" && python -m pytest "$_t" -q 2>&1 | tail -2); done | tee "$RES/pytest-patched.log"
echo "== apply hidden test patch (grade phase only) =="
python - "$TASK_JSON" "$WS" <<'EOF'
import json,sys
t=json.load(open(sys.argv[1])); open('/tmp/test_patch.diff','w').write(t['test_patch'])
EOF
(cd "$WS" && git apply --check /tmp/test_patch.diff 2>&1 && git apply /tmp/test_patch.diff && echo TESTPATCH-APPLIED || echo TESTPATCH-FAIL)
for _t in $TPY; do (cd "$WS" && python -m pytest "$_t" -q 2>&1 | tail -5); done | tee "$RES/pytest-graded.log"
echo "== ladder =="
echo "L1 patch-nonempty: $(test -s "$RES/agent.patch" && echo PASS || echo FAIL)"
echo "L2/L3: read $RES/pytest-*.log (patched must keep base green = L2; graded target flip = L3)"
