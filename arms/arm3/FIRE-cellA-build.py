# FIRE-ARM3 cell A: build tree (paste + run). 31B base: KEEP sample adapters
# (they are shaped for 31B); normalize every declared model line to 31B.
import re, shutil
from pathlib import Path
DATA_DIR = Path('/kaggle/input/competitions/gemma-4-developer-agent')
WORKING_DIR = Path('/kaggle/working'); WORKING_DIR.mkdir(parents=True, exist_ok=True)
MODEL_NAME = 'gemma-4-31b-it-qat-w4a16-ct'
SRC = DATA_DIR / 'sample_submission'; AGENT_DIR = WORKING_DIR / 'arm3_submission'
if AGENT_DIR.exists(): shutil.rmtree(AGENT_DIR)
shutil.copytree(SRC, AGENT_DIR)
models = set()
for yp in [AGENT_DIR / 'agent.yaml', *sorted((AGENT_DIR / 'sub_agents').glob('*.yaml'))]:
    if yp.is_file():
        t = yp.read_text(encoding='utf-8')
        t = re.sub(r'^(\s*model:\s*).*$', rf'\g<1>{MODEL_NAME}', t, flags=re.MULTILINE)
        yp.write_text(t, encoding='utf-8')
        models.update(re.findall(r'^\s*model:\s*(\S+)\s*$', t, flags=re.MULTILINE))
assert models == {MODEL_NAME}, 'declared-model drift: %s' % sorted(models)
assert (AGENT_DIR / 'adapters').is_dir(), '31B adapters missing from sample copy'
shutil.rmtree(AGENT_DIR / 'skills', ignore_errors=True)
print('tree ready:', AGENT_DIR, '| models:', sorted(models), '| adapters kept')
