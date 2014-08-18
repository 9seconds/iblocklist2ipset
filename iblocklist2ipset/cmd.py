# -*- coding: utf-8 -*-


import sys
import docopt

from six import print_, u

from . import __doc__ as doc, get_version, \
    PROGRAM_NAME, RESTORE_IPSET_JOB_SCRIPT, UPDATE_IPSET_JOB_SCRIPT
from .ipset import generate_ipset
from .networks import extract_networks
from .utils import script_example_header, printable_path


@script_example_header
def example_restore_ipset_job(args):
    print_(u(RESTORE_IPSET_JOB_SCRIPT).format(
        ipset_filename=printable_path(args["IPSET_PATH"]),
        iptables_name=args["IPTABLES_NAME"],
        ipset_name=args["--ipset"]
    ))


@script_example_header
def example_update_ipset_job(args):
    print_(u(UPDATE_IPSET_JOB_SCRIPT).format(
        progpath=printable_path(sys.argv[0]),
        progname=PROGRAM_NAME,
        ipset_name=args["--ipset"],
        urls=" ".join('"{0}"'.format(url) for url in args["BLOCKLIST_URL"]),
        ipset_path=printable_path(args["IPSET_PATH"])
    ))


def generate(args):
    try:
        netwrks = extract_networks(args["BLOCKLIST_URL"])
    except Exception as err:  # pylint: disable=W0703
        print_(u("Cannot extract networks: {0}").format(err),
               file=sys.stderr)
        return 1

    for line in generate_ipset(args["--ipset"], netwrks):
        print_(line)


def main():
    arguments = docopt.docopt(doc.format(program=PROGRAM_NAME),
                              version=get_version())

    if arguments["generate"]:
        return generate(arguments)
    elif arguments["example_restore_ipset_job"]:
        return example_restore_ipset_job(arguments)
    elif arguments["example_update_ipset_job"]:
        return example_update_ipset_job(arguments)
    return 2
