import pytest

from requests.utils import should_bypass_proxies


@pytest.mark.parametrize(
    "url, expected",
    (
        ("http://localhost/", True),
        ("http://anotherdomain.com:8888/", True),
        ("http://newdomain.com:1234/", True),
        ("http://www.newdomain.com:1234/", True),
        ("http://foo.d.o.t/", True),
        ("http://d.o.t/", True),
        ("http://prelocalhost/", False),
        ("http://newdomain.com/", False),
        ("http://newdomain.com:1235/", False),
    ),
)
def test_should_bypass_proxies_no_proxy_domain_boundary(url, expected):
    """Ensure no_proxy matching respects domain boundaries and does not
    greedily match domains that merely endswith the no_proxy entry.
    See CPython bpo-39057.
    """
    no_proxy = "localhost, anotherdomain.com, newdomain.com:1234, .d.o.t"
    assert should_bypass_proxies(url, no_proxy=no_proxy) == expected
