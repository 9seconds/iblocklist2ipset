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

import httmock
import pytest

import iblocklist2ipset
from iblocklist2ipset import main, generate, example_update_ipset_job, \
    example_restore_ipset_job
from tests import CommonTest


class TestExampleUpdateIpsetJob(CommonTest):

    def test_ok(self, monkeypatch):
        io = self.patch_io(monkeypatch)
        args = self.default_args("example_update_ipset_job")

        code, _ = self.run_with_output(io, example_update_ipset_job,
                                       args)
        assert code is None or code == 0


class TestExampleRestoreIpsetJob(CommonTest):

    def test_ok(self, monkeypatch):
        io = self.patch_io(monkeypatch)
        args = self.default_args("example_restore_ipset_job")

        code, _ = self.run_with_output(io, example_restore_ipset_job,
                                       args)
        assert code is None or code == 0


class TestGenerate(CommonTest):

    def test_ok(self, monkeypatch):
        io = self.patch_io(monkeypatch)
        args = self.default_args("generate")

        with httmock.HTTMock(self.fake_response(self.FAKE_CONTENT)):
            code, _ = self.run_with_output(io, generate, args)
        assert code is None or code == 0

    @pytest.mark.parametrize("input_", (
        "HELLO:223.123.123.123-123.123.123.255",
        "EVIL HACKER:150.250.250.250-",
        ":150.250.250.250-15",
        "::15.12"
    ))
    def test_nok(self, input_, monkeypatch):
        monkeypatch.setattr("iblocklist2ipset.utils.TIME_TO_SLEEP", 0)

        io = self.patch_io(monkeypatch)
        args = self.default_args("generate")

        with httmock.HTTMock(self.fake_response(input_)):
            code, _ = self.run_with_output(io, generate, args)
        assert code is not None and code != 0


class TestMain(CommonTest):

    @classmethod
    def patch_docopt(cls, subcommand, patcher):
        fake_docopt = lambda *args, **kwargs: cls.default_args(subcommand)
        patcher.setattr("docopt.docopt", fake_docopt)

    @classmethod
    def patch_func(cls, func_name, patcher):
        sentinel = object()
        patcher.setattr(iblocklist2ipset, func_name,
                        lambda args: sentinel)
        return sentinel

    @pytest.mark.parametrize("input_", CommonTest.SUBCOMMANDS)
    def test_generate(self, input_, monkeypatch):
        self.patch_docopt(input_, monkeypatch)
        result = self.patch_func(input_, monkeypatch)

        assert main() is result

    def test_empty(self, monkeypatch):
        self.patch_docopt("FAKEFAKEFAKE", monkeypatch)

        result = main()
        assert result != 0 and result is not None
