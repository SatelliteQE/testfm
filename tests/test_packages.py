import pytest

from testfm.decorators import starts_in
from testfm.log import logger
from testfm.packages import Packages


@pytest.mark.capsule
def test_positive_fm_packages_lock(ansible_module):
    """Verify whether satellite related packages get locked

    :id: d387d8be-10ad-4a62-aeff-3bc6a82e6bae

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain packages lock
        2. Run foreman-maintain packages status
        3. Run foreman-maintain packages is-locked
        4. check 'satellite' is mentioned in /etc/yum/pluginconf.d/versionlock.list
        5. Run foreman-maintain packages unlock
        6. Run foreman-maintain packages status
        7. Run foreman-maintain packages is-locked
        8. check 'satellite' is not mentioned in /etc/yum/pluginconf.d/versionlock.list

    :expectedresults: expected packages get locked and unlocked.

    :CaseImportance: Critical
    """
    # Test Package lock command
    contacted = ansible_module.command(Packages.lock(["--assumeyes"]))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0
    contacted = ansible_module.command(Packages.status())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "Packages are locked." in result["stdout"]
        assert "Automatic locking of package versions is enabled in installer." in result["stdout"]
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0
    contacted = ansible_module.command(Packages.is_locked())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "Packages are locked" in result["stdout"]
        assert result["rc"] == 0
    # Test package unlock command
    contacted = ansible_module.command(Packages.unlock())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0
    contacted = ansible_module.command(Packages.status())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert "Packages are not locked." in result["stdout"]
        assert "Automatic locking of package versions is enabled in installer." in result["stdout"]
        assert result["rc"] == 0
    contacted = ansible_module.command(Packages.is_locked())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "Packages are not locked" in result["stdout"]
        assert result["rc"] == 1
    # lock packages
    teardown = ansible_module.command(Packages.lock())
    for result in teardown.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0


@pytest.mark.capsule
@starts_in("6.6")
def test_positive_lock_package_versions(ansible_module):
    """Verify whether satellite related packages get locked

    :id: 9218a718-038c-48bb-b4a4-d4cb74859ddb

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run satellite-installer --lock-package-versions
        2. Run foreman-maintain packages status
        3. Run foreman-maintain packages is-locked
        4. Run satellite-installer --no-lock-package-versions
        5. Run foreman-maintain packages status
        6. Run foreman-maintain packages is-locked
        7. Teardown (Run satellite-installer --lock-package-versions)

    :expectedresults: expected packages get locked and unlocked.

    :CaseImportance: Critical
    """
    # Test whether packages are locked or not
    contacted = ansible_module.command("satellite-installer --lock-package-versions")
    for result in contacted.values():
        logger.info(result["stdout"])
        assert result["rc"] == 0
    contacted = ansible_module.command(Packages.status())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "Packages are locked." in result["stdout"]
        assert "Automatic locking of package versions is enabled in installer." in result["stdout"]
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0
    contacted = ansible_module.command(Packages.is_locked())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "Packages are locked" in result["stdout"]
        assert result["rc"] == 0
    # Test whether packages are unlocked or not
    contacted = ansible_module.command("satellite-installer --no-lock-package-versions")
    for result in contacted.values():
        logger.info(result["stdout"])
        assert result["rc"] == 0
    contacted = ansible_module.command(Packages.status())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert "Packages are not locked." in result["stdout"]
        assert (
            "Automatic locking of package versions is disabled in installer." in result["stdout"]
        )
        assert result["rc"] == 0
    contacted = ansible_module.command(Packages.is_locked())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "Packages are not locked" in result["stdout"]
        assert result["rc"] == 1
    # lock packages
    teardown = ansible_module.command("satellite-installer --lock-package-versions")
    for result in teardown.values():
        logger.info(result["stdout"])
        assert result["rc"] == 0


@pytest.mark.capsule
def test_positive_fm_packages_install(ansible_module, setup_packages_lock_tests):
    """Verify whether packages install/update work as expected.

    :id: 645a3d84-34cb-469c-8b79-105b889aac78

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run satellite-installer --lock-package-versions
        2. Run foreman-maintain packages status
        3. Run foreman-maintain packages is-locked
        4. Try to install/update package using FM packages install/update command.
        5. Run satellite-installer --no-lock-package-versions
        6. Run foreman-maintain packages status
        7. Run foreman-maintain packages is-locked
        8. Try to install package in unlocked state.
        9. Teardown (Run satellite-installer --lock-package-versions)


    :expectedresults: expected packages get locked and unlocked.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command("yum install -y zsh")
    for result in contacted.values():
        assert result["rc"] == 1
        assert "Use foreman-maintain packages install/update <package>" in result["stdout"]
    # Test whether FM packages install/ update command works as expected.
    contacted = ansible_module.raw(
        Packages.install(["--assumeyes", "zsh-5.0.2-31.el7.x86_64 elinks"])
    )
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert "Nothing to do" not in result["stdout"]
        assert "Packages are locked." in result["stdout"]
        assert "Automatic locking of package versions is enabled in installer." in result["stdout"]
    contacted = ansible_module.raw(Packages.update(["--assumeyes", "zsh"]))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert "Nothing to do" not in result["stdout"]
        assert "Packages are locked." in result["stdout"]
        assert "Automatic locking of package versions is enabled in installer." in result["stdout"]
    # Test whether packages are unlocked or not
    contacted = ansible_module.command("satellite-installer --no-lock-package-versions")
    for result in contacted.values():
        logger.info(result["stdout"])
        assert result["rc"] == 0
    contacted = ansible_module.command(Packages.status())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert "Packages are not locked." in result["stdout"]
        assert (
            "Automatic locking of package versions is disabled in installer." in result["stdout"]
        )
        assert result["rc"] == 0
    contacted = ansible_module.command(Packages.is_locked())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "Packages are not locked" in result["stdout"]
        assert result["rc"] == 1
    contacted = ansible_module.yum(name="zsh", state="absent")
    for result in contacted.values():
        assert result["rc"] == 0
    contacted = ansible_module.command("yum install -y zsh")
    for result in contacted.values():
        assert result["rc"] == 0
        assert "Use foreman-maintain packages install/update <package>" not in result["stdout"]
