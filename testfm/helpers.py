# helpers required for TestFM
import os

from fabric import Connection

from testfm.constants import SERVER_HOSTNAME


def product():
    """This helper provides Satellite/Capsule version."""

    server_version = os.popen(
        "ansible -i testfm/inventory server --user root -m shell "
        '-a "rpm -q satellite > /dev/null && rpm -q satellite --queryformat=%{VERSION}'
        ' || rpm -q satellite-capsule --queryformat=%{VERSION}" -o'
    ).read()
    return server_version.splitlines()[0].split(" ")[-1][:3]


def run(command):
    """ Use this helper to execute shell command on Satellite"""
    return Connection(SERVER_HOSTNAME, "root").run(command)


def server():
    """ Use this to find whether server on which tests are running is capsule or satellite."""
    contacted = run("rpm -q satellite > /dev/null; echo $?")
    if "0" in contacted.stdout:
        return "satellite"
    else:
        return "capsule"
