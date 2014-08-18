#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup, find_packages
from setuptools.command.test import test

from iblocklist2ipset import get_version


##############################################################################


REQUIREMENTS = (
    "netaddr==0.7.12",
    "requests==2.3.0",
    "docopt==0.6.2",
    "six==1.7.3"
)


with open("README.rst", "r") as resource:
    LONG_DESCRIPTION = resource.read()


##############################################################################


# copypasted from http://pytest.org/latest/goodpractises.html
class PyTest(test):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        test.initialize_options(self)
        self.pytest_args = None  # pylint: disable=W0201

    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = []  # pylint: disable=W0201
        self.test_suite = True  # pylint: disable=W0201

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        import sys
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

##############################################################################


setup(
    name="iblocklist2ipset",
    description="Converter between P2P lists from IBlocklist.com to IPSet",
    long_description=LONG_DESCRIPTION,
    version=get_version(),
    author="Sergey Arkhipov",
    license="MIT",
    author_email="serge@aerialsounds.org",
    maintainer="Sergey Arkhipov",
    maintainer_email="serge@aerialsounds.org",
    url="https://github.com/9seconds/iblocklist2ipset/",
    install_requires=REQUIREMENTS,
    tests_require=["pytest==2.6.1", "httmock==1.2.2"],
    packages=find_packages(exclude=["tests"]),
    entry_points={"console_scripts": [
        "iblocklist2ipset = iblocklist2ipset.cmd:main"
    ]},
    cmdclass={'test': PyTest},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking",
        "Topic :: System :: Networking :: Firewalls",
        "Topic :: Utilities"
    ],
    zip_safe=True
)
