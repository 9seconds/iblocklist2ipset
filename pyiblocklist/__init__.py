# -*- coding: utf-8 -*-
"""
Small utility to convert p2p format of IP Blocklists to IPSet format.

Usage:
  {program} generate [options] BLOCKLIST_URL...
  {program} example_restore_ipset_job [options] IPTABLES_NAME IPSET_PATH
  {program} example_update_ipset_job [options] IPSET_PATH BLOCKLIST_URL...
  {program} -h | --help
  {program} --version

Options:
  -h --help                         Shows this screen.
  --version                         Shows version and exits.
  -i IPSET_NAME --ipset=IPSET_NAME  The name of IPSet set [default: blocklist]

To get IP blocklists please visit https://www.iblocklist.com/
"""


from __future__ import print_function, absolute_import

import sys

import docopt

from .ipset import generate_ipset
from .networks import extract_networks
from .settings import PROGRAM_NAME, VERSION
from .utils import printable_path


RESTORE_IPSET_JOB_SCRIPT = ur"""
#!/bin/bash
set -e

ipset restore -f {ipset_filename}

iptables -F {iptables_name}
iptables -A {iptables_name} \
    -m state --state NEW \
    -m set --match-set {ipset_name} src \
    -j REJECT --reject-with icmp-host-unreachable
iptables -A {iptables_name} \
    -m state --state NEW \
    -m set --match-set {ipset_name} dst \
    -j REJECT --reject-with icmp-host-unreachable
""".strip()

UPDATE_IPSET_JOB_SCRIPT = ur"""
#!/bin/bash
set -e

{progpath} generate --ipset {ipset_name} {urls} > /tmp/{progname}.ipset
mv /tmp/{progpath}.ipset {ipset_path}
""".strip()


def example_restore_ipset_job(args):
    print(RESTORE_IPSET_JOB_SCRIPT.format(
        ipset_filename=printable_path(args["IPSET_PATH"]),
        iptables_name=args["IPTABLES_NAME"],
        ipset_name=args["--ipset"]
    ))


def example_update_ipset_job(args):
    print(UPDATE_IPSET_JOB_SCRIPT.format(
        progpath=printable_path(sys.argv[0]),
        progname=PROGRAM_NAME,
        ipset_name=args["--ipset"],
        urls=" ".join('"{}"'.format(url) for url in args["BLOCKLIST_URL"]),
        ipset_path=printable_path(args["IPSET_PATH"])
    ))


def generate(args):
    try:
        netwrks = extract_networks(args["BLOCKLIST_URL"])
    except Exception as err:  # pylint: disable=W0703
        print(u"Cannot extract networks: {}".format(err), file=sys.stderr)
        return 1

    for line in generate_ipset(args["--ipset"], netwrks):
        print(line)


def main():
    arguments = docopt.docopt(__doc__.format(program=PROGRAM_NAME),
                              version=".".join(str(part) for part in VERSION))

    if arguments["generate"]:
        return generate(arguments)
    elif arguments["example_restore_ipset_job"]:
        return example_restore_ipset_job(arguments)
    elif arguments["example_update_ipset_job"]:
        return example_update_ipset_job(arguments)


if __name__ == "__main__":
    sys.exit(main())
