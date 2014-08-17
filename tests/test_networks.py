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

from six import moves

from iblocklist2ipset.networks import extract_networks, fetch_networks, \
    convert_to_ipnetwork, ParseError
from tests import CommonTest


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
class TestFetchNetworks(CommonTest):

    def test_ok(self):
        with httmock.HTTMock(self.fake_response(self.FAKE_CONTENT)):
            networks = list(fetch_networks("http://fake.url"))

        assert set(networks) == set(self.FAKE_NETWORKS)

    @pytest.mark.parametrize("input_", (
        " ",
        "#commentary",
        """
        # commentary
        # another commentary
        """
    ))
    def test_empty(self, input_):
        with httmock.HTTMock(self.fake_response(input_)):
            assert list(fetch_networks("http://fake.url")) == []


# noinspection PyMethodMayBeStatic
class TestExtractNetworks(CommonTest):

    def test_no_repeats(self):
        urls = ["http://fake{0}.url".format(idx) for idx in moves.range(3)]
        with httmock.HTTMock(self.fake_response(self.FAKE_CONTENT)):
            networks = extract_networks(urls)

        assert set(networks) == set(self.FAKE_NETWORKS)
