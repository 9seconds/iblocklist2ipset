# -*- coding: utf-8 -*-
"""
Small utility to convert p2p format of IP Blocklists to IPSet format.

Usage:
  {program} generate [options] BLOCKLIST_PATH
  {program} example_ipset_job [options] IPTABLES_NAME IPSET_PATH
  {program} -h | --help
  {program} --version

Options:
  -h --help                         Shows this screen.
  --version                         Shows version and exits.
  -i IPSET_NAME --ipset=IPSET_NAME  The name of IPSet set [default: blocklist]

To get IP blocklists please visit https://www.iblocklist.com/
"""


from __future__ import print_function, absolute_import

import os.path
import sys

import docopt

from .common import PROGRAM_NAME, VERSION
from .ipset import generate_ipset
from .networks import extract_networks


def example_ipset_job(args):
    ipset_filename = os.path.abspath(args["IPSET_PATH"])
    iptables_name = args["IPTABLES_NAME"]

    print("#!/bin/sh", end="\n\n")
    print("ipset restore -f {}".format(ipset_filename), end="\n\n")
    print("iptables -F {}".format(iptables_name))
    for match_type in ("src", "dst"):
        print(" ".join(
            (
                "iptables",
                "-A {}".format(iptables_name),
                "-m state --state NEW",
                "-m set --match-set {} {}".format(args["--ipset"], match_type),
                "-j REJECT --reject-with icmp-host-unreachable"
            )
        ))


def generate(args):
    with open(args["BLOCKLIST_PATH"], "r") as resource:
        urls = [line.strip() for line in resource if line.startswith("http")]

    networks = extract_networks(urls)
    if not networks:
        return 1

    for line in generate_ipset(args["--ipset"], networks):
        print(line)


def main():
    arguments = docopt.docopt(__doc__.format(program=PROGRAM_NAME),
                              version=".".join(VERSION))

    if arguments["generate"]:
        return generate(arguments)
    elif arguments["example_ipset_job"]:
        return example_ipset_job(arguments)


if __name__ == "__main__":
    sys.exit(main())
