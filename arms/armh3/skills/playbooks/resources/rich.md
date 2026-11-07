## PLAYBOOK-RICH

- Repro pattern: pin the terminal — `COLUMNS=80`, `TERM=xterm`, construct
  `Console(file=io.StringIO(), width=80, ...)` and capture exact output.
- Wrapping/measure/style logic lives in the module named by the symptom
  (`wrap.py`, `measure.py`, `style.py`, `segment.py`, `console.py`).
- Verify: `pytest tests/test_<area>*.py` for the touched module only.
