# repro skill — issue-shaped reproduction in 1-2 calls

Write the family pattern to `/tmp/repro_<taskid>.py` via ONE `run_command`
heredoc, then run it through the logging wrapper (same call runs it AND
records evidence — no extra calls):
`python3 /tmp/repro_<taskid>.py > /tmp/repro_<taskid>.log 2>&1; code=$?; tail -5 /tmp/repro_<taskid>.log; echo "{\"file\": \"repro_<taskid>.py\", \"exit\": $code}" >> /tmp/repro_runs.jsonl; exit $code`
It MUST fail pre-fix (nonzero exit logged). After the Phase-3 edit, rerun
the SAME file through the SAME wrapper: it MUST pass. The penalty ledger
reads the chain in `/tmp/repro_runs.jsonl`: fail BEFORE final pass, or it
BLOCKs submit. An edit this file can't confirm is a guess.

## fastapi
```python
from fastapi.testclient import TestClient
# FILL from the issue: from <app_module> import app
# FILL: client = TestClient(app)
# FILL: resp = client.get(...)  (exact request shape from the issue)
print(resp.status_code); print(resp.json())
# FILL: assert <the issue's expected behavior>
```

## rich
```python
import io, os
os.environ["COLUMNS"] = "80"  # FILL width from issue if given
os.environ["TERM"] = "xterm"
from rich.console import Console
# FILL: buf = io.StringIO(); console = Console(file=buf, width=80)
# FILL: console.print(...)  (exact scenario from the issue)
out = buf.getvalue(); print(repr(out))
# FILL: assert <expected output>
```

## http (requests + httpx)
```python
# FILL: Session/Client-level repro, no mocks — drive the OBSERVABLE behavior
# (redirect chain, headers, content) exactly as the issue describes.
# FILL: print + assert expected.
```
