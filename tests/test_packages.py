import pytest

from testfm.decorators import stubbed
from testfm.helpers import server
from testfm.log import logger
from testfm.packages import Packages


@pytest.mark.capsule
def test_positive_fm_packages_lock_unlock(ansible_module):
    """Verify whether packages get locked and unlocked for satellite and capsule
    using foreman_maintain

    :id: d387d8be-10ad-4a62-aeff-3bc6a82e6bae

    :setup:
        1. satellite-maintain should be installed.

    :steps:
        1. Run satellite-maintain packages lock
        2. Run satellite-maintain packages status
        3. Run satellite-maintain packages is-locked
        4. Run satellite-maintain packages unlock
        5. Run satellite-maintain packages status
        6. Run satellite-maintain packages is-locked

    :expectedresults: Packages get locked and unlocked using foreman_maintain

    :CaseImportance: Critical
    """
    # Packages locking in enabled in installer for satellite, and disabled for capsule by default
    installer_state = "disabled" if server() == "capsule" else "enabled"

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
        assert (
            f"Automatic locking of package versions is {installer_state} in installer."
            in result["stdout"]
        )
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
        assert (
            f"Automatic locking of package versions is {installer_state} in installer."
            in result["stdout"]
        )
        assert result["rc"] == 0
    contacted = ansible_module.command(Packages.is_locked())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "Packages are not locked" in result["stdout"]
        assert result["rc"] == 1

    # Teardown: lock packages of satellite, for capsule its unlocked by default
    if server() == "satellite":
        teardown = ansible_module.command(Packages.lock())
        for result in teardown.values():
            logger.info(result["stdout"])
            assert "FAIL" not in result["stdout"]
            assert result["rc"] == 0


@pytest.mark.capsule
def test_positive_lock_package_versions(request, ansible_module):
    """Verify whether packages get locked and unlocked for satellite and capsule
    using satellite-installer

    :id: 9218a718-038c-48bb-b4a4-d4cb74859ddb

    :setup:
        1. satellite-maintain should be installed.

    :steps:
        1. Run satellite-installer --lock-package-versions
        2. Run satellite-maintain packages status
        3. Run satellite-maintain packages is-locked
        4. Run satellite-installer --no-lock-package-versions
        5. Run satellite-maintain packages status
        6. Run satellite-maintain packages is-locked
        7. Teardown (Run satellite-installer --lock-package-versions)

    :expectedresults: Packages get locked and unlocked using satellite-installer

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
        assert "Automatic locking of package versions is disabled in installer." in result["stdout"]
        assert result["rc"] == 0
    contacted = ansible_module.command(Packages.is_locked())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "Packages are not locked" in result["stdout"]
        assert result["rc"] == 1

    # Teardown: lock packages of satellite, for capsule its unlocked by default
    if server() == "satellite":
        teardown = ansible_module.command("satellite-installer --lock-package-versions")
        for result in teardown.values():
            logger.info(result["stdout"])
            assert result["rc"] == 0


@pytest.mark.capsule
def test_positive_fm_packages_install(ansible_module, setup_packages_lock_tests):
    """Verify whether packages install/update work as expected.

    :id: 645a3d84-34cb-469c-8b79-105b889aac78

    :setup:
        1. satellite-maintain should be installed.

    :steps:
        1. Run satellite-installer --lock-package-versions
        2. Run satellite-maintain packages status
        3. Run satellite-maintain packages is-locked
        4. Try to install/update package using satellite-maintain packages install/update command.
        5. Run satellite-installer --no-lock-package-versions
        6. Run satellite-maintain packages status
        7. Run satellite-maintain packages is-locked
        8. Try to install package in unlocked state.
        9. Teardown (Run satellite-installer --lock-package-versions)

    :expectedresults: Packages get install/update,  unlocked.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command("yum install -y zsh")
    for result in contacted.values():
        assert result["rc"] == 1
        assert "Use foreman-maintain packages install/update <package>" in result["stdout"]
    # Test whether satellite-maintain packages install/ update command works as expected.
    contacted = ansible_module.command(Packages.install(["--assumeyes", "zsh"]))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert result["rc"] == 0
        assert "FAIL" not in result["stdout"]
        assert "Nothing to do" not in result["stdout"]
        assert "Packages are locked." in result["stdout"]
        assert "Automatic locking of package versions is enabled in installer." in result["stdout"]
    contacted = ansible_module.command(Packages.update(["--assumeyes", "zsh"]))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert result["rc"] == 0
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
        assert result["rc"] == 0
        assert "FAIL" not in result["stdout"]
        assert "Packages are not locked." in result["stdout"]
        assert "Automatic locking of package versions is disabled in installer." in result["stdout"]
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


@pytest.mark.capsule
def test_positive_fm_packages_update(ansible_module, setup_packages_update):
    """Verify whether packages check-update and update work as expected.

    :id: 354d9940-10f1-4244-9079-fdbd24be49b3

    :setup:
        1. satellite-maintain should be installed.

    :steps:
        1. Run satellite-maintain packages check-update
        2. Run satellite-maintain packages update to update the walrus package.
        3. Verify walrus package is updated.

    :BZ: 1803975

    :expectedresults: satellite-maintain packages check-update should list walrus package for update
                      and satellite-maintain packages update should update the walrus package.

    :CaseImportance: Critical
    """
    # Run satellite-maintain packages check update and verify walrus package is available for update
    contacted = ansible_module.command(Packages.check_update())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0
        assert "walrus" in result["stdout"]
    # Run satellite-maintain packages update
    contacted = ansible_module.command(Packages.update(["--assumeyes", "walrus"]))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0
    # Verify walrus package is updated.
    contacted = ansible_module.command("rpm -qa walrus")
    for result in contacted.values():
        logger.info(result["stdout"])
        assert result["rc"] == 0
        assert "walrus-5.21-1" in result["stdout"]


@stubbed
def test_positive_fm_packages_sat_installer(ansible_module):
    """Verify satellite-installer is not executed after install/update
    of rubygem-foreman_maintain package

    :id: d73971a1-68b4-4ab2-a87c-76cc5ff80a39

    :setup:
        1. satellite-maintain should be installed.

    :steps:
        1. Run satellite-maintain packages install/update rubygem-foreman_maintain
        2. Verify satellite-installer is not executed after install/update
           of rubygem-foreman_maintain package

    :BZ: 1825841

    :expectedresults: satellite-installer should not be executed after install/update
                      of rubygem-foreman_maintain package

    :CaseImportance: Critical
    """
