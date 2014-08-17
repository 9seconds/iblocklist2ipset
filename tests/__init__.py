# -*- coding: utf-8 -*-


import os.path

from six import moves


class CommonTest(object):

    SUBCOMMANDS = (
        "generate",
        "example_restore_ipset_job",
        "example_update_ipset_job"
    )

    @staticmethod
    def patch_io(patcher):
        io = moves.cStringIO()
        patcher.setattr("sys.stdout", io)
        return io

    @classmethod
    def default_args(cls, subcommand):
        current_path = os.path.dirname(os.path.abspath(__file__))

        args = {
            "IPSET_PATH": os.path.join(current_path, "ipset"),
            "IPTABLES_NAME": "blocklist_iptables",
            "BLOCKLIST_URL": [
                "http://fake{0}.url".format(idx) for idx in moves.range(3)
            ],
            "--ipset": "blocklist_ipset",
        }
        for command in cls.SUBCOMMANDS:
            args[command] = subcommand in cls.SUBCOMMANDS

        return args

    @classmethod
    def run_with_output(cls, io, func, *args, **kwargs):
        result = func(*args, **kwargs)
        io_lines = [line for line in io.getvalue().split("\n") if line]

        return result, io_lines