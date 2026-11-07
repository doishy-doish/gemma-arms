## PLAYBOOK-FASTAPI

- Repro pattern: `fastapi.testclient.TestClient` against a minimal app, drive
  the exact failing request shape from the issue.
- Check `fastapi._compat` first when behavior differs by pydantic v1/v2.
- Dependency/param logic lives in `fastapi/dependencies/`; routing in
  `fastapi/routing/`, applications in `fastapi/applications.py`.
- Verify: `pytest tests/test_<area>*.py` for the touched area plus adjacent
  tutorial tests that encode the same behavior.
