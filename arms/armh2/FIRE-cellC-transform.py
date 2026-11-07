# FIRE-ARMH2 cell C: transform + pins + manifest + self-checks (paste + run after F1..F6).
import re, hashlib, json
from pathlib import Path
AGENT_DIR = Path('/kaggle/working/armh2_submission')
MODEL_NAME = 'gemma-4-e4b-it-qat-w4a16-ct'
(AGENT_DIR / 'agent.yaml.orig').write_text((AGENT_DIR / 'agent.yaml').read_text(encoding='utf-8'), encoding='utf-8')
ref = (AGENT_DIR / 'prompts' / 'system.md').read_text(encoding='utf-8')
assert 'PHASE 1' in ref and 'CONFIDENCE <0.00-1.00> BECAUSE' in ref, 'system.md content wrong'
assert 'PENALTY=0' in ref, 'penalty gate missing from system.md'
assert 'SPEC PROLOGUE' in ref and 'NO STACKED EDITS' in ref, 'exotic upgrades missing from system.md'
assert 'THOUGHTS-OFF ANCHOR' in ref, 'H2 anchor rule missing from system.md'
for rel in ['skills/verify/SKILL.md', 'skills/verify/compile_check.py',
            'skills/repro/SKILL.md', 'skills/penalty/SKILL.md',
            'skills/penalty/penalty_ledger.py']:
    assert (AGENT_DIR / rel).is_file(), 'missing ' + rel
(AGENT_DIR / 'agent.yaml').write_text(
"""name: armh2_root
model: gemma-4-e4b-it-qat-w4a16-ct
description: ARMH2 thoughts-off hybrid — single root, phase gates locate/repro/edit/verify/submit, thought stripped from history, E4B base, diagnostic envelope.
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
  - load_skill
  - load_skill_resource
  - run_skill_script
skills:
  - skills/verify
  - skills/repro
  - skills/penalty
generate_content_config: !include configs/sampling.yaml
""", encoding='utf-8')
sp = AGENT_DIR / 'configs' / 'sampling.yaml'
samp = sp.read_text(encoding='utf-8') if sp.is_file() else ''
applied, missing = [], []
for k, v in {'temperature': '0.2', 'top_p': '0.95', 'top_k': '40', 'max_output_tokens': '8192', 'include_thoughts': 'false'}.items():
    pat = rf'^(\s*{k}\s*:).*$'
    if re.search(pat, samp, flags=re.MULTILINE):
        samp = re.sub(pat, rf'\g<1> {v}', samp, flags=re.MULTILINE); applied.append(k)
    else: missing.append(k)
if re.search(r'^(\s*(?:thinking_budget|thinking-budget|budget)\s*:).*$', samp, flags=re.MULTILINE):
    samp = re.sub(r'^(\s*(?:thinking_budget|thinking-budget|budget)\s*:).*$', r'\g<1> 4096', samp, flags=re.MULTILINE); applied.append('thinking->4096')
else: missing.append('thinking')
sp.write_text(samp, encoding='utf-8')
if 'include_thoughts' in missing:
    print('WARNING: sample sampling.yaml has no include_thoughts key — H2 thoughts-off NOT applied, tree is H1-equivalent. Do not read H2 results as thoughts-off.')
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
(WORKING_DIR / 'ARMH2_MANIFEST.json').write_text(json.dumps({'run_tag': 'armh2-thoughts-off', 'model': MODEL_NAME, 'files': files}, indent=1), encoding='utf-8')
roots = [n for n in ('agent.yaml', 'agent.yml', 'root_agent.yaml', 'root_agent.yml') if (AGENT_DIR / n).is_file()]
links = [str(p) for p in AGENT_DIR.rglob('*') if p.is_symlink()]
total = sum(p.stat().st_size for p in AGENT_DIR.rglob('*') if p.is_file())
ok = len(roots) == 1 and not links and total < 3 * 1024 ** 3
print('roots:', roots, '| symlinks:', links, '| total_bytes:', total)
print('sampling applied:', applied, '| missing:', missing)
print('files:', len(files), '| READY' if ok else '| CHECK FAILED (restore agent.yaml.orig, paste report back)')
