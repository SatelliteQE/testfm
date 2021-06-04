from distutils.version import StrictVersion as Version

import pytest
import unittest2

from testfm.helpers import product
from testfm.helpers import server


def stubbed(reason=None):
    """Skips test due to non-implentation or some other reason."""
    return unittest2.skip(reason)(pytest.mark.stubbed(reason))


def run_only_on(*server_version):
    """Decorator to skip tests based on server version.

    Usage:

    To skip a specific test::

        from TestFM.decorators import run_only_on

        @run_only_on("6.4")
        def test_health_check():
            # test code continues here

    :param str server_version: Enter "6.8", "6.7", "6.6", "6.5", "6.4" and "6.3"
    for specific version
    """
    prd_version = product()
    return pytest.mark.skipif(
        prd_version not in server_version,
        reason="Server version is '{}' and this test will run only "
        "on '{}' version".format(prd_version, server_version),
    )


def starts_in(version):
    """Decorator to select tests based on minimum Satellite version.

    Usage:

    To select a specific test based on minimum Satellite version.::

        from TestFM.decorators import starts_in

        @starts_in("6.6")
        def test_health_check():
            # test code continues here

    :param str version: Enter "6.10", "6.9", "6.8.4", and likewise
    for specific version
    """
    return pytest.mark.skipif(
        Version(product()) < Version(version),
        reason="Server version is '{}' and this test will run only "
        "on {} '{}' onward".format(product(), server(), version),
    )


def ends_in(version):
    """Decorator to select tests based on maximum Satellite version.

    Usage:

    To select a specific test based on maximum Satellite version.::

        from TestFM.decorators import ends_in

        @ends_in("6.6")
        def test_health_check():
            # test code continues here

    :param str version: Enter "6.10", "6.9", "6.8.4", and likewise
    for specific version
    """
    return pytest.mark.skipif(
        Version(product()) > Version(version),
        reason="Server version is '{}' and this test will run only "
        "on {} <= '{}'".format(product(), server(), version),
    )
