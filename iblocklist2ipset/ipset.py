# -*- coding: utf-8 -*-


import math

from six import u


def ipset_hashsize(element_count):
    assert element_count > 0

    power = math.floor(math.log(element_count) / math.log(2))
    return int(math.pow(2, power))


def generate_ipset(ipset_name, networks):
    # create blocklist0 hash:net family inet hashsize 32768 maxelem 65536
    header = u("create {0} hash:net family inet hashsize {1} maxelem {2}")
    yield header.format(
        ipset_name, ipset_hashsize(len(networks)), len(networks)
    )
    for network in networks:
        # add blocklist0 148.129.0.0/16
        yield u("add {0} {1}").format(ipset_name, network)
