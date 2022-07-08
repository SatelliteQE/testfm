import yaml

from testfm.log import logger
from testfm.maintenance_mode import MaintenanceMode


def test_positive_maintenance_mode(setup_sync_plan, ansible_module):
    """Test satellite-maintain maintenance-mode subcommand

    :id: 51d76219-d3cc-43c0-9894-7bcb75c163c3

    :setup:
        1. satellite-maintain should be installed.
        2. active sync-plans
        3. set :manage_crond: true in /etc/foreman-maintain/foreman_maintain.yml'

    :steps:
        1. Verify that maintenance-mode is Off.
        2. Start maintenance-mode.
        3. Verify that active sync-plans got disabled or not.
        4. Verify that FOREMAN_MAINTAIN is mentioned in nftables list.
        5. Verify that crond.service is stopped.
        6. Validate maintenance-mode status command's output.
        7. Validate maintenance-mode is-enabled command's output.
        8. Stop maintenance-mode.
        9. Verify that disabled sync-plans got re-enabled or not.
        10. Verify that FOREMAN_MAINTAIN is not mentioned in nftables list.
        11. Verify that crond.service is running.
        12. Validate maintenance-mode status command's output.
        13. Validate maintenance-mode is-enabled command's output.

    :expectedresults: satellite-maintain maintenance-mode start/stop able
        to disable/enable sync-plan, stop/start crond.service and is able to add
        FOREMAN_MAINTAIN chain rule in nftables.

    :CaseImportance: Critical
    """
    sync_ids, sat_hostname = setup_sync_plan()
    maintenance_mode_off = [
        "Status of maintenance-mode: Off",
        "Nftables table: absent",
        "sync plans: enabled",
        "cron jobs: running",
    ]
    maintenance_mode_on = [
        "Status of maintenance-mode: On",
        "Nftables table: present",
        "sync plans: disabled",
        "cron jobs: not running",
    ]

    # Verify maintenance-mode status
    setup = ansible_module.command(MaintenanceMode.status())
    for result in setup.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert "OK" in result["stdout"]
        assert result["rc"] == 0
    # Verify maintenance-mode is-enabled
    setup = ansible_module.command(MaintenanceMode.is_enabled())
    for result in setup.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert "OK" in result["stdout"]
        assert result["rc"] == 1
        assert "Maintenance mode is Off" in result["stdout"]

    # Verify maintenance-mode start
    contacted = ansible_module.command(MaintenanceMode.start())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0
        assert f"Total {len(sync_ids)} sync plans are now disabled." in result["stdout"]
    ansible_module.fetch(src="/var/lib/foreman-maintain/data.yml", dest="./")
    with open(f"./{sat_hostname}/var/lib/foreman-maintain/data.yml") as f:
        data_yml = yaml.safe_load(f)
    assert len(sync_ids) == len(data_yml[":default"][":sync_plans"][":disabled"])
    assert sorted(sync_ids) == sorted(data_yml[":default"][":sync_plans"][":disabled"])
    for rules in ansible_module.command("nft list tables").values():
        logger.info(rules["stdout"])
        # Assert FOREMAN_MAINTAIN is listed in nftables
        assert "FOREMAN_MAINTAIN" in rules["stdout"]
    # Assert crond.service is stopped
    contacted = ansible_module.service_facts()
    state = contacted.values()[0]["ansible_facts"]["services"]["crond.service"]["state"]
    assert "stopped" in state
    # Verify maintenance-mode status
    contacted = ansible_module.command(MaintenanceMode.status())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert "OK" in result["stdout"]
        assert result["rc"] == 0
        for i in maintenance_mode_on:
            assert i in result["stdout"]
    # Verify maintenance-mode is-enabled
    contacted = ansible_module.command(MaintenanceMode.is_enabled())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert "OK" in result["stdout"]
        assert result["rc"] == 0
        assert "Maintenance mode is On" in result["stdout"]

    # Verify maintenance-mode stop
    contacted = ansible_module.command(MaintenanceMode.stop())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert result["rc"] == 0
        assert "FAIL" not in result["stdout"]
        assert f"Total {len(sync_ids)} sync plans are now enabled." in result["stdout"]
    ansible_module.fetch(src="/var/lib/foreman-maintain/data.yml", dest="./")
    with open(f"./{sat_hostname}/var/lib/foreman-maintain/data.yml") as f:
        data_yml = yaml.safe_load(f)
    assert len(sync_ids) == len(data_yml[":default"][":sync_plans"][":enabled"])
    assert sorted(sync_ids) == sorted(data_yml[":default"][":sync_plans"][":enabled"])
    for rules in ansible_module.command("nft list tables").values():
        logger.info(rules["stdout"])
        # Assert FOREMAN_MAINTAIN not listed in nftables
        assert "FOREMAN_MAINTAIN" not in rules["stdout"]
    # Assert crond.service is running
    contacted = ansible_module.service_facts()
    state = contacted.values()[0]["ansible_facts"]["services"]["crond.service"]["state"]
    assert "running" in state
    # Verify maintenance-mode status
    contacted = ansible_module.command(MaintenanceMode.status())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert "OK" in result["stdout"]
        assert result["rc"] == 0
        for i in maintenance_mode_off:
            assert i in result["stdout"]
    # Verify maintenance-mode is-enabled
    contacted = ansible_module.command(MaintenanceMode.is_enabled())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert "OK" in result["stdout"]
        assert result["rc"] == 1
        assert "Maintenance mode is Off" in result["stdout"]
