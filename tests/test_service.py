from testfm.decorators import capsule
from testfm.log import logger
from testfm.service import Service
from testfm.health import Health


@capsule
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
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0


@capsule
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
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0


def test_positive_automate_bz1624699(ansible_module):
    """Validate correct service restart on dynflowd stopped

    :id: 36f7ea87-12f3-4c12-817d-0031ce3ad241

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Stop dynflowd service
        2. Run foreman-maintain health check

    :expectedresults: service should restart correctly.

    :CaseImportance: Critical
    """
    setup = ansible_module.command(Service.service_stop({
        u'only': 'dynflowd'
    }))
    for result in setup.values():
        assert result['rc'] == 0
    contacted = ansible_module.command(Health.check(['-y']))
    for result in contacted.values():
        logger.info(result)
        assert result['rc'] == 0


@capsule
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
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0


@capsule
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
            logger.info(result['stdout'])
            assert "FAIL" not in result['stdout']
            assert result['rc'] == 0
    finally:
        teardown = ansible_module.command(Service.service_enable())
        for result in teardown.values():
            assert result['rc'] == 0


@capsule
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
            logger.info(result['stdout'])
            assert "FAIL" not in result['stdout']
            assert result['rc'] == 0
        contacted = ansible_module.command(Service.service_restart())
        for result in contacted.values():
            logger.info(result['stdout'])
            assert "FAIL" not in result['stdout']
            assert result['rc'] == 0
    finally:
        teardown = ansible_module.command(Service.service_start())
        for result in teardown.values():
            assert result['rc'] == 0


@capsule
def test_positive_service_status_clocale(ansible_module):
    """Foreman-maintain service on C locale

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
        assert result['rc'] == 0
