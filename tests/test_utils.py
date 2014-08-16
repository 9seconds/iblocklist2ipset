# -*- coding: utf-8 -*-


import os.path

# a hack for pytest to allow imports
if __package__ is None:
    import sys

    sys.path[0:0] = [
        os.path.dirname(                   # project_root
            os.path.dirname(               # tests
                os.path.abspath(__file__)  # this file
            )
        )
    ]

import posixpath
import StringIO

import pytest

from pyiblocklist.utils import try_if_empty, printable_path, \
    script_example_header


# noinspection PyUnresolvedReferences
class TestTryIfEmpty(object):

    @pytest.mark.parametrize("input_, expect_", (
        ([1, 2], 1),
        ([[], []], []),
        ([[], None], None),
        ([None, 1], 1)
    ))
    def test_ok(self, input_, expect_):
        inpt = list(reversed(input_))

        @try_if_empty(2)
        def fail_func():
            return inpt.pop()

        assert fail_func() == expect_

    # noinspection PyMethodMayBeStatic
    def test_exception_is_raised(self):
        @try_if_empty(10)
        def fail_func():
            raise Exception

        with pytest.raises(Exception):
            fail_func()


class TestPrintablePath(object):

    @pytest.mark.parametrize("input_, expect_", (
        ("/foo", "/foo"),
        ("/foo bar", r'"/foo bar"'),
        ('/foo "bar"', r'"/foo \"bar\""'),
        ("foo", os.path.abspath("foo")),
        ("foo bar", '"' + os.path.abspath("foo bar") + '"'),
        ('foo "bar"', '"' + os.path.abspath(r"foo \"bar\"") + '"')
    ))
    def test_ok(self, input_, expect_):
        assert printable_path(input_) == expect_


class TestScriptExampleHeader(object):

    @staticmethod
    def patch_io(patcher):
        io = StringIO.StringIO()
        patcher.setattr("sys.stdout", io)
        return io

    @staticmethod
    def run(io):
        @script_example_header
        def func():
            return 1
        func()

        return [line for line in io.getvalue().split("\n") if line]

    def test_wo_virtualenv(self, monkeypatch):
        io = self.patch_io(monkeypatch)
        monkeypatch.delenv("VIRTUAL_ENV", raising=False)

        output = self.run(io)

        assert output[0] == "#!/bin/bash"
        assert "set -e" in output

    def test_w_virtualenv(self, monkeypatch):
        io = self.patch_io(monkeypatch)
        virtualenv_path = posixpath.join("/", "virtualenv")
        monkeypatch.setenv("VIRTUAL_ENV", virtualenv_path)

        output = self.run(io)

        source_path = posixpath.join(virtualenv_path, "bin", "activate")
        assert "source {}".format(source_path) in output