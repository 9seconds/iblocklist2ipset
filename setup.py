#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

from iblocklist2ipset.settings import VERSION


##############################################################################


REQUIREMENTS = (
    "netaddr==0.7.12",
    "requests==2.3.0",
    "docopt==0.6.2"
)


##############################################################################


# copypasted from http://pytest.org/latest/goodpractises.html
class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        import sys
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

##############################################################################


setup(
    name="iblocklist2ipset",
    description="Converter between P2P lists from IBlocklist.com to IPSet",
    long_description="TTT",
    version=".".join(str(part) for part in VERSION),
    author="Sergey Arkhipov",
    license="MIT",
    author_email="serge@aerialsounds.org",
    maintainer="Sergey Arkhipov",
    maintainer_email="serge@aerialsounds.org",
    url="https://github.com/9seconds/iblocklist2ipset/",
    install_requires=REQUIREMENTS,
    tests_require=["pytest==2.6.1", "httmock==1.2.2"],
    packages=find_packages(exclude=["tests"]),
    entry_points=dict(console_scripts=["iblocklist2ipset = iblocklist2ipset:main"]),
    cmdclass={'test': PyTest},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking",
        "Topic :: Utilities"
    ],
    zip_safe=True
)
