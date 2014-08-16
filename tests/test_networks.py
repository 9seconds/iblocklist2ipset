# -*- coding: utf-8 -*-

# a hack for pytest to allow imports
if __package__ is None:
    import sys
    import os.path

    sys.path[0:0] = [
        os.path.dirname(                   # project_root
            os.path.dirname(               # tests
                os.path.abspath(__file__)  # this file
            )
        )
    ]

import httmock
import pytest

from pyiblocklist.networks import extract_networks, fetch_networks, \
    convert_to_ipnetwork, ParseError


FAKE_NETWORKS = (
    '223.4.233.164/31',
    '223.4.241.230/31',
    '223.4.241.242/32'
)
FAKE_CONTENT = """
# Test stuff. If you see your ips and truly sure it is clean, please contact me
# It was actually copypasted from BlueTack level1 blocklist, so there.

SMSHoax FakeAV Fraud Trojan:223.4.233.164-223.4.233.165
SMSHoax FakeAV Fraud Trojan:223.4.241.230-223.4.241.231
SMSHoax FakeAV Fraud Trojan:223.4.241.242-223.4.241.242
""".strip()


def fake_response(content):
    # noinspection PyUnusedLocal
    @httmock.all_requests
    def make_response(url, request):
        headers = {
            "Content-Type": "text/plain"
        }
        return httmock.response(200, content, headers, elapsed=100, request=request)
    return make_response


# noinspection PyUnresolvedReferences
class TestConvertToIPNetwork(object):

    @pytest.mark.parametrize("input_", (
        "HELLO:123.123.123.123-123.123.123.255",
        "EVIL HACKER:150.250.250.250-150.251.250.250",
        ":150.250.250.250-150.251.250.250"
    ))
    def test_ok(self, input_):
        network = convert_to_ipnetwork(input_)
        assert network and len(network) > 0

    @pytest.mark.parametrize("input_", (
        "HELLO:223.123.123.123-123.123.123.255",
        "EVIL HACKER:150.250.250.250-",
        ":150.250.250.250-15",
        "::15.12"
    ))
    def test_nok(self, input_):
        with pytest.raises(ParseError):
            convert_to_ipnetwork(input_)

    @pytest.mark.parametrize("input_", (
        "",
        "#commentary"
        "#commented:127.0.0.1-127.0.0.12"
    ))
    def test_empty(self, input_):
        assert convert_to_ipnetwork(input_) == []


# noinspection PyUnresolvedReferences,PyMethodMayBeStatic
class TestFetchNetworks(object):

    def test_ok(self):
        with httmock.HTTMock(fake_response(FAKE_CONTENT)):
            networks = list(fetch_networks("http://fake.url"))

        assert set(networks) == set(FAKE_NETWORKS)

    @pytest.mark.parametrize("input_", (
        " ",
        "#commentary",
        """
        # commentary
        # another commentary
        """
    ))
    def test_empty(self, input_):
        with httmock.HTTMock(fake_response(input_)):
            assert list(fetch_networks("http://fake.url")) == []


# noinspection PyMethodMayBeStatic
class TestExtractNetworks(object):

    def test_no_repeats(self):
        urls = ["http://fake{}.url".format(idx) for idx in xrange(3)]
        with httmock.HTTMock(fake_response(FAKE_CONTENT)):
            networks = extract_networks(urls)

        assert set(networks) == set(FAKE_NETWORKS)
