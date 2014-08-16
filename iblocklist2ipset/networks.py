# -*- coding: utf-8 -*-


from __future__ import absolute_import

import itertools

import netaddr
import requests

from .settings import ATTEMPT_COUNT
from .utils import try_if_empty


class ParseError(ValueError):

    def __init__(self, line, msg):
        super(ParseError, self).__init__(
            u'Incorrect incoming line "{0}": {1}'.format(
                line, msg
            )
        )


@try_if_empty(ATTEMPT_COUNT)
def extract_networks(urls):
    networks = itertools.chain.from_iterable(
        fetch_networks(url) for url in urls
    )
    return frozenset(networks)


def fetch_networks(url):
    http_response = requests.get(url, stream=True)
    for item in http_response.iter_lines(decode_unicode=False):
        for network in convert_to_ipnetwork(item):
            yield str(network)


def convert_to_ipnetwork(blocklist_line):
    blocklist_line = blocklist_line.strip()
    # commentary or empty one
    if blocklist_line.startswith("#") or not blocklist_line:
        return []

    chunks = blocklist_line.split(":")

    try:
        start, finish = tuple(rng.strip() for rng in chunks[-1].split("-"))
    except ValueError as err:
        raise ParseError(blocklist_line, err)
    try:
        return netaddr.IPRange(start, finish).cidrs()
    except Exception as exc:
        raise ParseError(blocklist_line, exc)
