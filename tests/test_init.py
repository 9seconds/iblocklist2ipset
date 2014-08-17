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

import os.path

import pytest

from iblocklist2ipset import main, generate, example_update_ipset_job, \
    example_restore_ipset_job
from tests import CommonTest


class TestExampleUpdateIpsetJob(CommonTest):

    def test_ok(self, monkeypatch):
        io = self.patch_io(monkeypatch)
        args = self.default_args("example_update_ipset_job")

        code, output = self.run_with_output(io, example_update_ipset_job,
                                            args)
        assert code is None or code == 0


class TestExampleRestoreIpsetJob(CommonTest):

    def test_ok(self, monkeypatch):
        io = self.patch_io(monkeypatch)
        args = self.default_args("example_restore_ipset_job")

        code, output = self.run_with_output(io, example_restore_ipset_job,
                                            args)
        assert code is None or code == 0
