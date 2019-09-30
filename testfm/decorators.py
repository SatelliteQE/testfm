from testfm.helpers import product

import pytest
import unittest2

# Run for capsule
capsule = pytest.mark.capsule
ansible_host_pattern = pytest.config.getoption("--ansible-host-pattern")


def stubbed(reason=None):
    """Skips test due to non-implentation or some other reason."""
    return unittest2.skip(reason)(pytest.mark.stubbed(reason))


def run_only_on(*server):
    """Decorator to skip tests based on server version.

    Usage:

    To skip a specific test::

        from TestFM.decorators import run_only_on

        @run_only_on('6.4')
        def test_health_check():
            # test code continues here

    :param str project: Enter '6.7', '6.6' , '6.5' , '6.4' , '6.3' and '6.2'
    for specific version
    """
    return pytest.mark.skipif(
        product() not in server,
        reason="Server version is '{0}' and this test will run only "
               "on '{1}' version".format(product(), server)
    )


def starts_in(version):
    """Decorator to select tests based on minimum Satellite version.

    Usage:

    To select a specific test based on minimum Satellite version.::

        from TestFM.decorators import starts_in

        @starts_in(6.6)
        def test_health_check():
            # test code continues here

    :param float version: Enter 6.7, 6.6, 6.5 , 6.4 , 6.3 , 6.2 and 6.1
    for specific version
    """
    return pytest.mark.skipif(
        float(product()) < version,
        reason="Server version is '{0}' and this test will run only "
               "on {1} '{2}' onward".format(product(), ansible_host_pattern, version))


def ends_in(version):
    """Decorator to select tests based on maximum Satellite version.

    Usage:

    To select a specific test based on maximum Satellite version.::

        from TestFM.decorators import ends_in

        @ends_in(6.6)
        def test_health_check():
            # test code continues here

    :param float version: Enter 6.7, 6.6, 6.5 , 6.4 , 6.3 , 6.2 and 6.1
    for specific version
    """
    return pytest.mark.skipif(
        float(product()) > version,
        reason="Server version is '{0}' and this test will run only "
               "on {1} <= '{2}'".format(product(), ansible_host_pattern, version))
