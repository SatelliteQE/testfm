# helpers required for TestFM
import os

from testfm import settings


def product():
    """Use this helper to fetch x.y version of Satellite/Capsule from x.y.z.v.w"""
    return ".".join(settings.server.version.release.split(".")[:2])


def run(command):
    """Use this helper to execute shell command on Satellite"""
    return os.popen(f"ansible server -i testfm/inventory -u root -m shell -a '{command}'").read()


def server():
    """Use this to find whether server on which tests are running is capsule or satellite."""
    return "satellite" if "rc=0" in run("rpm -q satellite") else "capsule"


def rhel7():
    """Use this helper to find if satellite RHEL version is 7"""
    return True if "rc=0" in run("rpm -qa rubygem-foreman_maintain | grep el7") else False
