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

import re
import random

import pytest

from pyiblocklist.ipset import ipset_hashsize, generate_ipset


# noinspection PyUnresolvedReferences
class TestHashSize(object):

    @pytest.mark.parametrize("input_", (
        1, 14, 15, 16, 17, 18
    ))
    def test_ok(self, input_):
        result = ipset_hashsize(input_)

        assert result & (result - 1) == 0
        assert result <= input_

    @pytest.mark.parametrize("input_", (
        9, 10, 11, 12, 13, 14, 15
    ))
    def test_result_less_than(self, input_):
        assert ipset_hashsize(input_) == 8

    @pytest.mark.parametrize("input_", (
        1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192
    ))
    def test_result_the_same(self, input_):
        assert ipset_hashsize(input_) == input_


class TestGenerateIPSet(object):

    IPTABLES_NAME = "blocklist"
    DEFAULT_NETWORK_COUNT = 10

    @staticmethod
    def random_network():
        ipaddr = "{}.{}.{}.{}".format(
            random.randint(1, 254),
            random.randint(1, 254),
            random.randint(1, 254),
            random.randint(1, 254)
        )
        if random.random() > 0.1:
            ipaddr += "/{}".format(random.randint(1, 32))

        return ipaddr

    @classmethod
    def random_network_set(cls, count=0):
        networks = set()
        while len(networks) != count:
            networks.add(cls.random_network())
        return networks

    def test_header(self):
        networks = self.random_network_set(self.DEFAULT_NETWORK_COUNT)
        generator = generate_ipset(self.IPTABLES_NAME, networks)
        header = next(generator)

        # create blocklist0 hash:net family inet hashsize 32768 maxelem 65536
        matcher = re.match(r"""
            ^
            create\s+(?P<name>\w+)\s+
            hash:net\s+family\s+inet\s+
            hashsize\s+(?P<hashsize>\d+)\s+
            maxelem\s+(?P<maxelem>\d+)\s*
            $
            """, header, re.VERBOSE)
        assert matcher is not None, header

        elements = matcher.groupdict()
        for element in elements.itervalues():
            assert element is not None, elements
        elements["hashsize"] = int(elements["hashsize"])
        elements["maxelem"] = int(elements["maxelem"])

        assert elements["name"] == self.IPTABLES_NAME, elements
        assert elements["hashsize"] < elements["maxelem"], elements
        # noinspection PyTypeChecker
        assert elements["hashsize"] & (elements["hashsize"] - 1) == 0, elements
        assert elements["maxelem"] == self.DEFAULT_NETWORK_COUNT, elements

    def test_content(self):
        networks = self.random_network_set(self.DEFAULT_NETWORK_COUNT)
        generator = generate_ipset(self.IPTABLES_NAME, networks)
        next(generator)

        collected_networks = []
        for line in generator:
            matcher = re.match(r"add\s+(?P<name>\w+)\s+(?P<network>.*)\s*",
                               line)
            assert matcher is not None, line

            elements = matcher.groupdict()
            for element in elements.itervalues():
                assert element is not None, elements
            assert elements["name"] == self.IPTABLES_NAME, line
            assert elements["network"] in networks, line
            collected_networks.append(elements["network"])

        assert len(collected_networks) == len(networks), collected_networks
        assert len(set(collected_networks)) == len(collected_networks), collected_networks
