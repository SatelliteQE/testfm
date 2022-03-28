import pytest

from testfm.decorators import stubbed
from testfm.helpers import product
from testfm.helpers import server
from testfm.log import logger
from testfm.upgrade import Upgrade


@pytest.mark.capsule
def test_positive_satellite_maintain_upgrade_list(ansible_module):
    """List versions this system is upgradable to

    :id: 12efec41-4f09-4199-a20c-a4525e773b78

    :setup:

        1. satellite-maintain should be installed.
    :steps:
        1. Run satellite-maintain upgrade list-versions

    :expectedresults: Versions system is upgradable to are listed.

    :CaseImportance: Critical
    """
    if server() == "satellite":
        satellite_version = ansible_module.command(
            "rpm -q 'satellite' --queryformat='%{VERSION}'"
        ).values()[0]["stdout"]
        if satellite_version.startswith("6.11"):
            versions = ["6.11.z"]
        elif satellite_version.startswith("6.10"):
            versions = ["6.10.z", "6.11"]
        elif satellite_version.startswith("6.9"):
            versions = ["6.9.z", "6.10"]
        elif satellite_version.startswith("6.8"):
            versions = ["6.8.z", "6.9"]
        else:
            versions = ["unsupported satellite version"]
    else:
        capsule_version = ansible_module.command(
            "rpm -q 'satellite-capsule' --queryformat='%{VERSION}'"
        ).values()[0]["stdout"]
        if capsule_version.startswith("6.11"):
            versions = ["6.11.z"]
        elif capsule_version.startswith("6.10"):
            versions = ["6.10.z", "6.11"]
        elif capsule_version.startswith("6.9"):
            versions = ["6.9.z", "6.10"]
        elif capsule_version.startswith("6.8"):
            versions = ["6.8.z", "6.9"]
        else:
            versions = ["unsupported capsule version"]

    contacted = ansible_module.command(Upgrade.list_versions())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        for ver in versions:
            assert ver in result["stdout_lines"]


@pytest.mark.capsule
def test_positive_repositories_validate(ansible_module):
    """Test repositories-validate pre-upgrade check is
     skipped when system is subscribed using custom activationkey.

    :id: 811698c0-09da-4727-8886-077aebb2b5ed

    :setup:
        1. satellite-maintain should be installed.

    :steps:
        1. Run satellite-maintain upgrade check.

    :BZ: 1632111

    :expectedresults: repositories-validate check should be skipped.

    :CaseImportance: Critical
    """
    skip_message = "Your system is subscribed using custom activation key"
    export_command = "export EXTERNAL_SAT_ORG=Sat6-CI;export EXTERNAL_SAT_ACTIVATION_KEY=Ext_AK;"
    fm_command = Upgrade.check(
        [
            "--target-version",
            f"{product()}.z",
            "--whitelist",
            "check-non-redhat-repository",
            "--assumeyes",
        ]
    )
    contacted = ansible_module.shell(export_command + fm_command)
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "SKIPPED" in result["stdout"]
        assert "FAIL" not in result["stdout"]
        assert skip_message in result["stdout"]


@pytest.mark.capsule
@stubbed
def test_positive_self_update():
    """Test self-update satellite-maintain package feature.

    :id: 1c566768-fd73-4fe6-837b-26709a1ebed9

    :setup:
        1. satellite-maintain should be installed.
        2. satellite-maintain package version should be >= v0.6.x

    :steps:
        1. Run satellite-maintain upgrade check/run command.
        2. Run satellite-maintain upgrade check/run command with disable-self-upgrade option.

    :BZ: 1649329

    :expectedresults:
        1. Update satellite-maintain package to latest version and gives message to re-run command.
        2. If disable-self-upgrade option is used then it should skip self-upgrade step.

    :CaseImportance: Critical
    """


@pytest.mark.capsule
@stubbed
def test_positive_check_presence_satellite_or_satellite_capsule():
    """Check for presence of satellite or satellite-capsule packages feature.

    :id: 1011ff01-6dfb-422f-92c5-995d38bc163e

    :setup:
        1. satellite-maintain should be installed.
        2. satellite-maintain package version should be >= v0.6.x

    :steps:
        1. Run satellite-maintain upgrade list-versions/check/run command.
        2. Run satellite-maintain upgrade list-versions/check/run command,
            after removing satellite and satellite-capsule packages.

    :BZ: 1886031

    :expectedresults:
        1. If those packages are removed, then it should give error, like
            "Error: Important rpm package satellite/satellite-capsule is not installed!
             Install satellite/satellite-capsule rpm to ensure system consistency."

    :CaseImportance: Critical
    """
