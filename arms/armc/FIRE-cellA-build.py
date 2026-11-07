# FIRE-ARM1 cell A: build tree (paste + run). Files land in F1/F2/F3 first.
import re, shutil
from pathlib import Path
DATA_DIR = Path('/kaggle/input/competitions/gemma-4-developer-agent')
WORKING_DIR = Path('/kaggle/working'); WORKING_DIR.mkdir(parents=True, exist_ok=True)
MODEL_NAME = 'gemma-4-e4b-it-qat-w4a16-ct'
SRC = DATA_DIR / 'sample_submission'; AGENT_DIR = WORKING_DIR / 'arm1_submission'
if AGENT_DIR.exists(): shutil.rmtree(AGENT_DIR)
shutil.copytree(SRC, AGENT_DIR)
for yp in [AGENT_DIR / 'agent.yaml', *sorted((AGENT_DIR / 'sub_agents').glob('*.yaml'))]:
    if yp.is_file():
        t = yp.read_text(encoding='utf-8')
        t = re.sub(r'^(\s*model:\s*).*$', rf'\g<1>{MODEL_NAME}', t, flags=re.MULTILINE)
        t = re.sub(r'^\s*adapter:\s*.*\n?', '', t, flags=re.MULTILINE)
        yp.write_text(t, encoding='utf-8')
shutil.rmtree(AGENT_DIR / 'adapters', ignore_errors=True)
print('tree ready:', AGENT_DIR, '| agent.yaml exists:', (AGENT_DIR / 'agent.yaml').is_file())
