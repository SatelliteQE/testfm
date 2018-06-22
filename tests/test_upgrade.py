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
    satellite_version = str(ansible_module.command(
        "rpm -q 'satellite' --queryformat='%{VERSION}'"
    ).values()[0]['stdout'])
    if satellite_version.startswith('6.4'):
        versions = ['6.4.z']
    elif satellite_version.startswith('6.3'):
        versions = ['6.3.z', '6.4']
    elif satellite_version.startswith('6.2'):
        versions = ['6.2.z', '6.3']
    else:
        versions = ['6.2']
    contacted = ansible_module.command(Upgrade.list_versions())
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        for ver in versions:
            assert ver in result['stdout']
