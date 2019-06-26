from testfm.decorators import run_only_on
from testfm.packages import Packages
from testfm.log import logger


def test_positive_foreman_maintain_packages_lock(setup_install_pkgs, ansible_module):
    """Verify whether satellite related packages get locked

    :id: d387d8be-10ad-4a62-aeff-3bc6a82e6bae

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain packages lock
        2. Run foreman-maintain packages status
        3. Run foreman-maintain packages is-locked
        4. check 'satellite' is mentioned
        in /etc/yum/pluginconf.d/versionlock.list
        5. Run foreman-maintain packages unlock
        6. Run foreman-maintain packages status
        7. Run foreman-maintain packages is-locked
        8. check 'satellite' is not mentioned
        in /etc/yum/pluginconf.d/versionlock.list

    :expectedresults: expected packages get locked and unlocked.

    :CaseImportance: Critical
    """
    sat_pkgs = 0
    contacted = ansible_module.command(Packages.lock())
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result["rc"] == 0
    contacted = ansible_module.command(Packages.status())
    for result in contacted.values():
        logger.info(result['stdout'])
        assert 'Packages are locked.' in result['stdout']
        assert "FAIL" not in result['stdout']
        assert result["rc"] == 0
    contacted = ansible_module.command(Packages.is_locked())
    for result in contacted.values():
        logger.info(result['stdout'])
        assert 'Foreman related packages are locked' in result['stdout']
        assert result["rc"] == 0
    contacted = ansible_module.command("grep 'satellite' /etc/yum/pluginconf.d/versionlock.list")
    for result in contacted.values():
        logger.info(result['stdout'])
        assert 'satellite' in result['stdout']
    contacted = ansible_module.shell("yum repolist")
    for result in contacted.values():
        logger.info(result['stdout'])
        sat_pkgs = int(contacted.values()[0]['stdout_lines'][-1][-3:])
    contacted = ansible_module.shell("yum versionlock list | wc -l")
    for result in contacted.values():
        logger.info(result['stdout'])
        assert int(result['stdout']) == sat_pkgs, 'number of packages locked is not ' \
                                                  'equal to packages provided by satellite repo'

    contacted = ansible_module.command(Packages.unlock())
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result["rc"] == 0
    contacted = ansible_module.command(Packages.status())
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert 'Packages are not locked.' in result['stdout']
        assert result["rc"] == 0
    contacted = ansible_module.command(Packages.is_locked())
    for result in contacted.values():
        logger.info(result['stdout'])
        assert 'Foreman related packages are not locked' in result['stdout']
        assert result["rc"] == 1
    contacted = ansible_module.command("grep 'satellite' /etc/yum/pluginconf.d/versionlock.list")
    for result in contacted.values():
        logger.info(result['stdout'])
        assert 'satellite' not in result['stdout']
    contacted = ansible_module.shell("yum versionlock list | wc -l")
    for result in contacted.values():
        logger.info(result['stdout'])
        assert int(result['stdout']) == 0, 'No package should be locked.'


@run_only_on('sat66')
def test_positive_lock_package_versions(setup_install_pkgs, ansible_module):
    """Verify whether satellite related packages get locked

    :id: 9218a718-038c-48bb-b4a4-d4cb74859ddb

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run satellite-installer --lock-package-versions
        2. Run foreman-maintain packages status
        3. Run foreman-maintain packages is-locked
        4. check 'satellite' is mentioned
        in /etc/yum/pluginconf.d/versionlock.list
        5. Run satellite-installer --no-lock-package-versions
        6. Run foreman-maintain packages status
        7. Run foreman-maintain packages is-locked
        8. check 'satellite' is not mentioned
        in /etc/yum/pluginconf.d/versionlock.list

    :expectedresults: expected packages get locked and unlocked.

    :CaseImportance: Critical
    """
    sat_pkgs = 0
    contacted = ansible_module.command('satellite-installer --lock-package-versions')
    for result in contacted.values():
        logger.info(result['stdout'])
        assert result["rc"] == 0
    contacted = ansible_module.command(Packages.status())
    for result in contacted.values():
        logger.info(result['stdout'])
        assert 'Packages are locked.' in result['stdout']
        assert "FAIL" not in result['stdout']
        assert result["rc"] == 0
    contacted = ansible_module.command(Packages.is_locked())
    for result in contacted.values():
        logger.info(result['stdout'])
        assert 'Foreman related packages are locked' in result['stdout']
        assert result["rc"] == 0
    contacted = ansible_module.command("grep 'satellite' /etc/yum/pluginconf.d/versionlock.list")
    for result in contacted.values():
        logger.info(result['stdout'])
        assert 'satellite' in result['stdout']
    contacted = ansible_module.shell("yum repolist")
    for result in contacted.values():
        logger.info(result['stdout'])
        sat_pkgs = int(contacted.values()[0]['stdout_lines'][-1][-3:])
    contacted = ansible_module.shell("yum versionlock list | wc -l")
    for result in contacted.values():
        logger.info(result['stdout'])
        assert int(result['stdout']) == sat_pkgs, 'number of packages locked is not ' \
                                                  'equal to packages provided by satellite repo'

    contacted = ansible_module.command('satellite-installer --no-lock-package-versions')
    for result in contacted.values():
        logger.info(result['stdout'])
        assert result["rc"] == 0
    contacted = ansible_module.command(Packages.status())
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert 'Packages are not locked.' in result['stdout']
        assert result["rc"] == 0
    contacted = ansible_module.command(Packages.is_locked())
    for result in contacted.values():
        logger.info(result['stdout'])
        assert 'Foreman related packages are not locked' in result['stdout']
        assert result["rc"] == 1
    contacted = ansible_module.command("grep 'satellite' /etc/yum/pluginconf.d/versionlock.list")
    for result in contacted.values():
        logger.info(result['stdout'])
        assert 'satellite' not in result['stdout']
    contacted = ansible_module.shell("yum versionlock list | wc -l")
    for result in contacted.values():
        logger.info(result['stdout'])
        assert int(result['stdout']) == 0, 'No package should be locked.'
