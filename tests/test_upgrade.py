from testfm.helpers import product
from testfm.log import logger
from testfm.upgrade import Upgrade


def test_positive_foreman_maintain_upgrade_list(ansible_module):
    """List versions this system is upgradable to

    :id: 12efec41-4f09-4199-a20c-a4525e773b78

    :setup:

        1. foreman-maintain should be installed.
    :steps:
        1. Run foreman-maintain upgrade list-versions

    :expectedresults: Versions system is upgradable to are listed.

    :CaseImportance: Critical
    """
    satellite_version = ansible_module.command(
        "rpm -q 'satellite' --queryformat='%{VERSION}'"
    ).values()[0]["stdout"]
    if satellite_version.startswith("6.8"):
        versions = ["6.8.z"]
    elif satellite_version.startswith("6.7"):
        versions = ["6.7.z", "6.8"]
    elif satellite_version.startswith("6.6"):
        versions = ["6.6.z", "6.7"]
    elif satellite_version.startswith("6.5"):
        versions = ["6.5.z", "6.6"]
    elif satellite_version.startswith("6.4"):
        versions = ["6.4.z", "6.5"]
    elif satellite_version.startswith("6.3"):
        versions = ["6.3.z", "6.4"]
    elif satellite_version.startswith("6.2"):
        versions = ["6.2.z", "6.3"]
    else:
        versions = ["6.2"]
    contacted = ansible_module.command(Upgrade.list_versions())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        for ver in versions:
            assert ver in result["stdout_lines"]


def test_positive_repositories_validate(setup_install_pkgs, ansible_module):
    """ Test repositories-validate pre-upgrade check is
     skipped when system is subscribed using custom activationkey.

    :id: 811698c0-09da-4727-8886-077aebb2b5ed

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain upgrade check.

    :BZ: 1632111

    :expectedresults: repositories-validate check should be skipped.

    :CaseImportance: Critical
    """
    skip_message = "Your system is subscribed using custom activation key"
    export_command = "export EXTERNAL_SAT_ORG=Sat6-CI;export EXTERNAL_SAT_ACTIVATION_KEY=Ext_AK;"
    fm_command = Upgrade.check(
        [
            "--target-version",
            "{}.z".format(product()),
            "--whitelist",
            '"disk-performance,check-epel-repository,check-hotfix-installed,'
            'check-upstream-repository"',
            "--assumeyes",
        ]
    )
    contacted = ansible_module.shell(export_command + fm_command)
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "SKIPPED" in result["stdout"]
        assert "FAIL" not in result["stdout"]
        assert skip_message in result["stdout"]
