## PLAYBOOK-HTTP (requests + httpx)

- Repro pattern: Session/Client level, not socket level — reproduce the
  observable behavior (redirect chain, headers, content decoding).
- requests: `sessions.py`, `adapters.py`, `models.py`. httpx: `_client.py`,
  `_transports/`, `_content.py`. Mirror across sync/async.
- Verify: `pytest tests/test_<area>*.py` for the touched module only.
