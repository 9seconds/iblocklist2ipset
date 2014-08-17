# -*- coding: utf-8 -*-


import os.path

import httmock

from six import moves


class CommonTest(object):

    SUBCOMMANDS = (
        "generate",
        "example_restore_ipset_job",
        "example_update_ipset_job"
    )

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

    @staticmethod
    def fake_response(content):
        # noinspection PyUnusedLocal
        @httmock.all_requests
        def make_response(url, request):
            headers = {
                "Content-Type": "text/plain"
            }
            return httmock.response(200, content, headers, elapsed=100, request=request)
        return make_response

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
            args[command] = command == subcommand

        return args

    @classmethod
    def run_with_output(cls, io, func, *args, **kwargs):
        result = func(*args, **kwargs)
        io_lines = [line for line in io.getvalue().split("\n") if line]

        return result, io_lines