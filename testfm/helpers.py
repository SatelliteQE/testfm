# helpers required for TestFM
import os


def product():
    """This helper provides Satellite/Capsule version"""
    server_version = os.popen(
        "ansible -i testfm/inventory server --user root -m shell "
        '-a "rpm -q satellite > /dev/null && rpm -q satellite --queryformat=%{VERSION}'
        ' || rpm -q satellite-capsule --queryformat=%{VERSION}" -o'
    ).read()
    return server_version.splitlines()[0].split(" ")[-1][:3]


def run(command):
    """Use this helper to execute shell command on Satellite"""
    return os.popen(f"ansible server -i testfm/inventory -u root -m command -a '{command}'").read()


def server():
    """Use this to find whether server on which tests are running is capsule or satellite."""
    result = run("rpm -q satellite")
    if "rc=0" in result:
        return "satellite"
    else:
        return "capsule"
