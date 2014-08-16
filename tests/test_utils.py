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

import pytest

from pyiblocklist.utils import try_if_empty


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
