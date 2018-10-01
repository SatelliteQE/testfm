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

        @run_only_on('sat63')
        def test_health_check():
            # test code continues here

    :param str project: Enter 'sat63' , 'sat62' and 'sat61' for specific
     version
    """
    return pytest.mark.skipif(
        product() not in server,
        reason="Server version is '{0}' and this test will run only "
               "on '{1}' version".format(product(), server)
    )
