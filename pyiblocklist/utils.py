# -*- coding: utf-8 -*-


import functools
import time
import os.path
import re
import random


def try_if_empty(count):
    assert count >= 1

    def outer_decorator(func):
        @functools.wraps(func)
        def inner_decorator(*args, **kwargs):
            for attempt in xrange(count - 1):
                result = func(*args, **kwargs)
                if result:
                    return result
                time.sleep(min(5, random.randint(1, attempt + 1)))
            return func(*args, **kwargs)

        return inner_decorator
    return outer_decorator


def printable_path(path):
    abspath = os.path.abspath(path)
    if re.search(r"\s", abspath) is not None:
        abspath = '"' + abspath.replace('"', r'\"') + '"'
    return abspath