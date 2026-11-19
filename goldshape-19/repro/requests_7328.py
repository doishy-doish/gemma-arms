"""Gold-shape reproducer for requests#7328 (no httpbin needed).

Drives the REAL Session.resolve_redirects machinery through the `responses`
adapter mock: 3 redirects then 200. Mirrors gold test
test_redirect_history_no_self_reference assertions exactly:
no response may contain itself in its own history, and each history
must equal the prefix of the final history.
"""
import responses as responses_lib

import requests


@responses_lib.activate
def test_redirect_history_no_self_reference():
    responses_lib.add(
        responses_lib.GET, "http://example.com/a",
        status=302, headers={"Location": "http://example.com/b"},
    )
    responses_lib.add(
        responses_lib.GET, "http://example.com/b",
        status=302, headers={"Location": "http://example.com/c"},
    )
    responses_lib.add(
        responses_lib.GET, "http://example.com/c",
        status=302, headers={"Location": "http://example.com/d"},
    )
    responses_lib.add(responses_lib.GET, "http://example.com/d", status=200)

    r = requests.get("http://example.com/a")
    assert r.status_code == 200
    assert len(r.history) == 3
    for i, resp in enumerate(r.history):
        assert resp not in resp.history
        assert resp.history == r.history[:i]
