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


PROGRAM_NAME = "iblocklist2ipset"
VERSION = 0, 0, 1

ATTEMPT_COUNT = 16
TIME_TO_SLEEP = 1


RESTORE_IPSET_JOB_SCRIPT = r"""
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

UPDATE_IPSET_JOB_SCRIPT = r"""
{progpath} generate --ipset {ipset_name} {urls} > /tmp/{progname}.ipset
mv /tmp/{progname}.ipset {ipset_path}
""".strip()


def get_version():
    return ".".join(str(num) for num in VERSION)
