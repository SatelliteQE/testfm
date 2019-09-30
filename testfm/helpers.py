# helpers required for TestFM
from fabric import Connection
from testfm.constants import SERVER_HOSTNAME
import os


def product():
    """This helper provides Satellite/Capsule version."""

    server_version = os.popen(
        'ansible -i testfm/inventory server --user root -m shell '
        '-a "rpm -q satellite > /dev/null && rpm -q satellite --queryformat=%{VERSION}'
        ' || rpm -q satellite-capsule --queryformat=%{VERSION}" -o').read()
    return server_version.splitlines()[0].split(' ')[-1][:3]


def run(command):
    """ Use this helper to execute shell command on Satellite"""
    return Connection(SERVER_HOSTNAME, 'root').run(command)
