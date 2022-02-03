import pytest

from testfm.health import Health
from testfm.log import logger
from testfm.service import Service


@pytest.mark.capsule
def test_positive_foreman_maintain_service_restart(ansible_module):
    """Restart services using service restart

    :id: c5a38994-8c14-40c7-bc6a-1cfc68fc2d28

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain service restart

    :expectedresults: Katello-services should restart.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Service.service_restart())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0


@pytest.mark.capsule
def test_positive_foreman_maintain_service_start(ansible_module):
    """Start services using service start

    :id: fa3b02a9-b441-413b-b9d2-1a59d04f285c

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain service start

    :expectedresults: Katello-services should start.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Service.service_start())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0


def test_positive_foreman_service(ansible_module):
    """Validate httpd service should work as expected even stopping of the foreman service

    :id: 08a29ea2-2e49-11eb-a22b-d46d6dd3b5b2

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Stop foreman service
        2. Check the status for httpd should not have affect
        3. Run foreman-maintain health check

    :expectedresults: service should restart correctly.

    :CaseImportance: Critical
    """
    try:
        setup = ansible_module.command(Service.service_stop({"only": "foreman"}))
        for result in setup.values():
            assert result["rc"] == 0
            assert "FAIL" not in result["stdout"]
            assert "foreman" in result["stdout"]

        httpd_service = ansible_module.command(Service.service_status({"only": "httpd"}))
        for result in httpd_service.values():
            logger.info(result)
            assert result["rc"] == 0

        contacted = ansible_module.command(Health.check(["-y"]))
        for result in contacted.values():
            logger.info(result)
            assert result["rc"] == 0
            assert "foreman" in result["stdout"]

    finally:
        teardown = ansible_module.command(Service.service_start({"only": "foreman"}))
        for result in teardown.values():
            assert result["rc"] == 0


@pytest.mark.capsule
def test_positive_service_enable(ansible_module):
    """Enable services using foreman-maintain service

    :id: a0e0a052-0e21-465c-bb28-2e7613dbece6

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain service enable.

    :expectedresults: service should enable.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Service.service_enable())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0


@pytest.mark.capsule
def test_positive_service_disable(ansible_module):
    """Disable services using foreman-maintain service

    :id: e2c052e5-c2b6-4f0e-952b-3b0c22c66f22

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain service disable.

    :expectedresults: service should disable.

    :CaseImportance: Critical
    """
    try:
        contacted = ansible_module.command(Service.service_disable())
        for result in contacted.values():
            logger.info(result["stdout"])
            assert "FAIL" not in result["stdout"]
            assert result["rc"] == 0
    finally:
        teardown = ansible_module.command(Service.service_enable())
        for result in teardown.values():
            assert result["rc"] == 0


@pytest.mark.capsule
def test_positive_automate_bz1626651(ansible_module):
    """Disable services using foreman-maintain service

    :id: dc60e388-f012-4164-a496-b12d6230cdc2

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain service stop.
        2. Run foreman-maintain service restart

    :expectedresults: service should restart.

    :CaseImportance: Critical
    """
    try:
        contacted = ansible_module.command(Service.service_stop())
        for result in contacted.values():
            logger.info(result["stdout"])
            assert "FAIL" not in result["stdout"]
            assert result["rc"] == 0
        contacted = ansible_module.command(Service.service_restart())
        for result in contacted.values():
            logger.info(result["stdout"])
            assert "FAIL" not in result["stdout"]
            assert result["rc"] == 0
    finally:
        teardown = ansible_module.command(Service.service_start())
        for result in teardown.values():
            assert result["rc"] == 0


@pytest.mark.capsule
def test_positive_service_status_clocale(ansible_module):
    """Satellite-maintain service on C locale

    :id: 143dda54-5ab5-478a-b33e-af805bace2d7

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run LC_ALL=C foreman-maintain service stop.

    :expectedresults: service status should display.

    :CaseImportance: Critical
    """
    contacted = ansible_module.shell("LC_ALL=C " + Service.service_status())
    for result in contacted.values():
        logger.info(result)
        assert result["rc"] == 0


@pytest.mark.capsule
def test_positive_failed_service_status(ansible_module):
    """Verify foreman-maintain service status return error when service stopped

    :id: 74f6e276-1e54-4bf3-9538-19e87059f8b5

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain service stop.
        2. Run foreman-maintain service status.

    :expectedresults: service status should return error code.

    :CaseImportance: Critical
    """
    try:
        setup = ansible_module.command(Service.service_stop())
        for result in setup.values():
            logger.info(result["stdout"])
            assert result["rc"] == 0
        contacted = ansible_module.command(Service.service_status())
        for result in contacted.values():
            logger.info(result)
            assert result["rc"] != 0
    finally:
        teardown = ansible_module.command(Service.service_start())
        for result in teardown.values():
            assert result["rc"] == 0


def test_positive_fm_service_restart_bz_1696862(setup_bz_1696862, ansible_module):
    """Restart services using service restart

    :id: c7518650-d72a-47b1-8d38-42b862f474fc

    :setup:
        1. foreman-maintain should be installed.
        2. Run setup_bz_1696862 from conftest.py

    :steps:
        1. Run foreman-maintain service restart

    :expectedresults: Katello-services should restart even
     if hammer credentials are not available.

    :BZ: 1632768

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Service.service_restart())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0


def test_positive_foreman_maintain_service_list_sidekiq(ansible_module):
    """List sidekiq services with service list

    :id: 5acb68a9-c430-485d-bb45-b499adc90927

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain service list
        2. Run foreman-maintain service restart

    :expectedresults: Sidekiq-services should list and should restart.

    :CaseImportance: Medium
    """
    contacted = ansible_module.command(Service.service_list())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0
        assert "dynflow-sidekiq@.service" in result["stdout"]

    contacted = ansible_module.command(Service.service_restart())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0
        assert "dynflow-sidekiq@orchestrator" in result["stdout"]
        assert "dynflow-sidekiq@worker" in result["stdout"]
        assert "dynflow-sidekiq@worker-hosts-queue" in result["stdout"]


def test_positive_service_status_rpmsave(ansible_module, setup_rpmsave_file):
    """Verify foreman-maintain service status doesn't pick up any backup files like .rpmsave,
    or any file with .yml which don't exist as services.

    :id: dda696c9-7385-4450-8380-b694e4016661

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain service status.
        2. Verify foreman-maintain service status doesn't pick up any backup files like
           .rpmsave, or any file with .yml which don't exist as services.


    :expectedresults: foreman-maintain service status shouldn't pick
                      invalid services with extension .rpmsave

    :BZ: 1945916, 1962853

    :CaseImportance: High
    """
    contacted = ansible_module.command(Service.service_status(["-b"]))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "rpmsave" not in result["stdout"]
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0
