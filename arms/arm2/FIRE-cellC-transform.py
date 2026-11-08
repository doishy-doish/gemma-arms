# FIRE-ARM2 cell C: transform + pins + manifest + self-checks (paste + run after F1..F2).
import re, hashlib, json
from pathlib import Path
AGENT_DIR = Path('/kaggle/working/arm2_submission')
MODEL_NAME = 'gemma-4-e4b-it-qat-w4a16-ct'
(WORKING_DIR / 'agent.yaml.pre-fc.bak').write_text((AGENT_DIR / 'agent.yaml').read_text(encoding='utf-8'), encoding='utf-8')  # backup OUTSIDE submission dir: adk validate_directory rejects '.orig' inside it (H1 v2 -> 0/10 INVALID)
ref = (AGENT_DIR / 'prompts' / 'system.md').read_text(encoding='utf-8')
assert 'HARD LIMITS' in ref and 'CALL PLAN' in ref, 'winner-shape sections missing from system.md'
assert 'by call 12' in ref and 'CONFIDENCE' in ref, 'call-12 rule or evidence line missing'
assert 'rewrite a whole file' in ref and 'STEP 1' in ref, 'spray ban or SPEC step missing'
assert not (AGENT_DIR / 'skills').exists(), 'skills/ must not ship in ARM2 (winner-faithful single agent)'
(AGENT_DIR / 'agent.yaml').write_text(
"""name: arm2_root
model: gemma-4-e4b-it-qat-w4a16-ct
description: ARM2 winner-shape replication — SPEC + HARD LIMITS + CALL PLAN + targeted verify, E4B base, diagnostic envelope. DIAG11 test arm; procedure only, no task content.
instruction: !include prompts/system.md
tools:
  - run_command
  - read_file
  - edit_file
  - write_file
  - get_code_neighbors
  - search_similar_code
  - get_code_subgraph
  - get_status
  - submit_patch
generate_content_config: !include configs/sampling.yaml
""", encoding='utf-8')
sp = AGENT_DIR / 'configs' / 'sampling.yaml'
samp = sp.read_text(encoding='utf-8') if sp.is_file() else ''
applied, missing = [], []
for k, v in {'temperature': '0.2', 'top_p': '0.95', 'top_k': '40', 'max_output_tokens': '8192'}.items():
    pat = rf'^(\s*{k}\s*:).*$'
    if re.search(pat, samp, flags=re.MULTILINE):
        samp = re.sub(pat, rf'\g<1> {v}', samp, flags=re.MULTILINE); applied.append(k)
    else: missing.append(k)
stripped = []
for _pat in (r'^\s*thinking_budget\s*:.*$', r'^\s*thinking-budget\s*:.*$', r'^\s*include_thoughts\s*:.*$'):
    if re.search(_pat, samp, flags=re.MULTILINE):
        samp = re.sub(_pat + r'\n?', '', samp, flags=re.MULTILINE); stripped.append(_pat)
sp.write_text(samp, encoding='utf-8')
# ARM2 v2 lesson: the harness schema (SandboxedAgentConfig) REJECTS thinking_budget/
# include_thoughts under generate_content_config (0/10 INVALID, extra_forbidden).
# v3 fix: STRIP thinking keys if native carries them; never add/pin them. Fail loud.
assert 'thinking_budget' not in samp and 'include_thoughts' not in samp, 'thinking keys present in sampling.yaml (harness schema forbids them)'
(AGENT_DIR / 'eval_config.yaml').write_text(
"""evaluation:
  timeout_seconds: 300
  verification_timeout_seconds: 300
  max_tool_calls: 25
  max_time_minutes: 15
  max_turns: 80
""", encoding='utf-8')
files = []
for p in sorted(AGENT_DIR.rglob('*')):
    if p.is_file() and '.orig' not in p.name:
        files.append({'path': str(p.relative_to(AGENT_DIR)), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()[:16], 'bytes': p.stat().st_size})
for p in sorted(AGENT_DIR.rglob('*')):  # validator rejects backup/temp extensions inside submission dir (H1 v2 lesson)
    if p.is_file() and (p.suffix.lower() in ('.orig', '.bak', '.tmp', '.swp') or p.name.endswith('~')):
        p.unlink()
leftovers = [str(p.relative_to(AGENT_DIR)) for p in AGENT_DIR.rglob('*') if p.is_file() and (p.suffix.lower() in ('.orig', '.bak', '.tmp', '.swp') or p.name.endswith('~'))]
assert not leftovers, 'backup/temp files left in submission dir (validator rejects them): %s' % leftovers
KNOWN_TOOLS = {'edit_file', 'get_code_neighbors', 'get_code_subgraph', 'get_status', 'read_file', 'run_command', 'search_similar_code', 'submit_patch', 'write_file'}  # harness registry (H1 v3: load_skill* do NOT exist)
declared = {}
for _yf in [AGENT_DIR / 'agent.yaml', *sorted((AGENT_DIR / 'sub_agents').glob('*.yaml'))]:
    _txt = _yf.read_text(encoding='utf-8')
    assert 'load_skill' not in _txt, 'stale skill tool in %s (harness has no such tool)' % _yf.name
    _tools, _in_tools = [], False
    for _ln in _txt.splitlines():
        if _ln.strip() == 'tools:':
            _in_tools = True
            continue
        if _in_tools:
            if _ln.startswith('  - '):
                _tools.append(_ln[4:].strip())
            elif _ln.strip() and not _ln.startswith(' '):
                _in_tools = False
    declared[_yf.name] = _tools
_bad = {_f: [t for t in _ts if t not in KNOWN_TOOLS] for _f, _ts in declared.items()}
_bad = {_f: _ts for _f, _ts in _bad.items() if _ts}
assert not _bad, 'unknown tools declared (compile would fail): %s' % _bad
print('tools declared:', {_f: len(_ts) for _f, _ts in declared.items()}, '| all in registry')
for _yf in [AGENT_DIR / 'prompts' / 'system.md', *sorted((AGENT_DIR / 'prompts').glob('*.md')), *sorted((AGENT_DIR / 'sub_agents').glob('*.yaml'))]:
    _txt = _yf.read_text(encoding='utf-8')
    assert '{' not in _txt and '}' not in _txt, 'curly brace in %s (ADK renders {...} as session-state placeholder — H1 v5 lesson)' % _yf.name
print('brace scan: clean (no {...} placeholders in instructions)')
try:  # REAL validator gate (H1 v2 lesson): run adk's own validate_directory in-notebook, BEFORE any GPU work
    import inspect as _insp
    from adk_submission import discovery as _disc
    _fn = getattr(_disc, 'validate_directory', None)
    if _fn is None:
        print('real validator: validate_directory not found — local checks only')
    else:
        _nparams = len(_insp.signature(_fn).parameters)
        _fn(*([AGENT_DIR] + [None] * max(0, _nparams - 1)))
        print('real validator: PASS')
except ImportError as _e:
    print('real validator unavailable (%s) — local checks only' % _e)
except Exception as _e:
    if type(_e).__name__ == 'SubmissionValidationError':
        raise  # genuine submission defect: fail LOUD here, do not burn GPU
    print('real validator inconclusive (%s: %s) — local checks stand' % (type(_e).__name__, str(_e)[:200]))
(WORKING_DIR / 'ARM2_MANIFEST.json').write_text(json.dumps({'run_tag': 'arm2-winner', 'model': MODEL_NAME, 'files': files}, indent=1), encoding='utf-8')
roots = [n for n in ('agent.yaml', 'agent.yml', 'root_agent.yaml', 'root_agent.yml') if (AGENT_DIR / n).is_file()]
links = [str(p) for p in AGENT_DIR.rglob('*') if p.is_symlink()]
total = sum(p.stat().st_size for p in AGENT_DIR.rglob('*') if p.is_file())
ok = len(roots) == 1 and not links and total < 3 * 1024 ** 3
print('roots:', roots, '| symlinks:', links, '| total_bytes:', total)
print('sampling applied:', applied, '| missing:', missing, '| stripped:', stripped)
print('files:', len(files), '| READY' if ok else '| CHECK FAILED (restore WORKING_DIR/agent.yaml.pre-fc.bak, paste report back)')
