import pytest
import yaml

from testfm.advanced import Advanced
from testfm.advanced_by_tag import AdvancedByTag
from testfm.constants import cap_beta_repo
from testfm.constants import cap_repos
from testfm.constants import sat_beta_repo
from testfm.constants import sat_repos
from testfm.decorators import stubbed
from testfm.helpers import server
from testfm.log import logger


def test_positive_foreman_maintain_service_restart(ansible_module):
    """Restart service using advanced procedure run

    :id: 64d3c78e-d602-43d6-bf77-f31135ed019e

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain advanced procedure run service-restart

    :expectedresults: Katello-service should restart.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Advanced.run_service_restart())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]


def test_positive_foreman_maintain_hammer_setup(setup_install_pexpect, ansible_module):
    """Hammer setup using advanced procedure

    :id: 236171c0-5185-465e-9eec-e15dfefb41c3

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Change password for user to any string
        2. Run advanced procedure run hammer-setup
        3. Change password to original password

    :expectedresults: Hammer setup should successful.

    :CaseImportance: Critical
    """
    try:
        setup = ansible_module.command(
            "hammer -u admin -p changeme"
            " user update"
            " --login admin "
            "--password 'JMNBzJ*a-4;XH!C~'"
        )
        for result in setup.values():
            logger.info(result)
            assert result["rc"] == 0
        output = ansible_module.expect(
            command=Advanced.run_hammer_setup(),
            responses={"Hammer admin password: ": "JMNBzJ*a-4;XH!C~"},
        )
        for result in output.values():
            logger.info(result)
            assert result["rc"] == 0
    finally:
        teardown = ansible_module.command(
            "hammer -u admin "
            "-p 'JMNBzJ*a-4;XH!C~'"
            " user update --login admin"
            " --password 'changeme'"
        )
        for result in teardown.values():
            logger.info(result)
            assert result["rc"] == 0


@stubbed
def test_positive_foreman_maintain_packages_update(ansible_module):
    """Packages update using advanced procedure run

    :id: d56523d7-7042-40e1-a96e-db8f33b960e5

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain advanced procedure run packages-update

    :expectedresults: packages should update.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Advanced.run_packages_update())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]


def test_positive_foreman_taks_delete_old(ansible_module):
    """Delete old foreman-tasks using advanced procedure run

    :id: c5deaf67-8fa9-43a6-bf62-1c0d6be63a85

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain advanced procedure run
        foreman-tasks-delete --state old

    :expectedresults: Old foreman tasks should delete.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Advanced.run_foreman_tasks_delete({u"state": "old"}))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]


def test_positive_foreman_taks_delete_planning(ansible_module):
    """Delete planning foreman-tasks using advanced procedure run

    :id: 447f5b05-b6a2-4f3a-8e89-8281995ca1cf

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain advanced procedure run
        foreman-tasks-delete --state planning

    :expectedresults: foreman tasks in planning state should delete.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Advanced.run_foreman_tasks_delete({u"state": "planning"}))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]


def test_positive_foreman_taks_delete_pending(ansible_module):
    """Delete pending foreman-tasks using advanced procedure run

    :id: 6bd3af66-9910-48c4-8cbb-69c3ddd18d6c

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain advanced procedure run
        foreman-tasks-delete --state pending

    :expectedresults: foreman tasks in pending state should delete.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Advanced.run_foreman_tasks_delete({u"state": "pending"}))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]


def test_positive_foreman_task_resume(ansible_module):
    """Resume paused foreman-tasks using advanced procedure run

    :id: e9afe55b-e3a4-425a-8bfd-a8df6674e516

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain advanced procedure run
        foreman-tasks-resume

    :expectedresults: foreman tasks in paused state should resume.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Advanced.run_foreman_tasks_resume())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]


def test_positive_foreman_tasks_ui_investigate(setup_install_pexpect, ansible_module):
    """Run foreman-tasks-ui-investigate using advanced procedure run

    :id: 3b4f69c6-c0a1-42e3-a099-8a6e26280d17

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain advanced procedure run
        foreman-tasks-ui-investigate

    :expectedresults: procedure foreman-tasks-ui-investigate should work.

    :CaseImportance: Critical
    """
    output = ansible_module.expect(
        command=Advanced.run_foreman_tasks_ui_investigate(),
        responses={"press ENTER after the tasks are resolved.": " "},
    )
    for result in output.values():
        logger.info(result)
        assert result["rc"] == 0


def test_positive_sync_plan_disable_enable(setup_sync_plan, ansible_module):
    """Run sync-plans-enable and sync-plans-disable
    using advanced procedure run.

    :id: 865df1e1-1189-437c-8451-22d772ff97d4

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain advanced procedure run
        sync-plans-disable
        2. Run foreman-maintain advanced procedure run
        sync-plans-enable

    :expectedresults: procedure sync-plans-enable should work.

    :CaseImportance: Critical
    """
    sync_ids, sat_hostname = setup_sync_plan()
    contacted = ansible_module.command(Advanced.run_sync_plans_disable())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert result["rc"] == 0
        assert "FAIL" not in result["stdout"]
    ansible_module.fetch(src="/var/lib/foreman-maintain/data.yml", dest="./")
    with open("./{}/var/lib/foreman-maintain/data.yml".format(sat_hostname)) as f:
        data_yml = yaml.safe_load(f)
    assert len(sync_ids) == len(data_yml[":default"][":sync_plans"][":disabled"])
    assert sorted(sync_ids) == sorted(data_yml[":default"][":sync_plans"][":disabled"])

    contacted = ansible_module.command(Advanced.run_sync_plans_enable())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert result["rc"] == 0
        assert "FAIL" not in result["stdout"]
    ansible_module.fetch(src="/var/lib/foreman-maintain/data.yml", dest="./")
    with open("./{}/var/lib/foreman-maintain/data.yml".format(sat_hostname)) as f:
        data_yml = yaml.safe_load(f)
    assert len(sync_ids) == len(data_yml[":default"][":sync_plans"][":enabled"])
    assert sorted(sync_ids) == sorted(data_yml[":default"][":sync_plans"][":enabled"])


@pytest.mark.capsule
def test_positive_procedure_by_tag_check_migrations(ansible_module):
    """Run pre-migrations and post-migrations using advanced
    procedure by-tag

    :id: 65cacca0-f142-4a63-a644-01f76120f16c

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain advanced procedure by-tag
        pre-migrations

        2. Run foreman-maintain advanced procedure by-tag
        post-migrations

    :expectedresults: procedures of pre-migrations tag and
     post-migrations tag should work.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(AdvancedByTag.pre_migrations())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
    check_iptables = ansible_module.command("iptables -L")
    for rules in check_iptables.values():
        logger.info(rules["stdout"])
        assert "FOREMAN_MAINTAIN" in rules["stdout"]
    teardown = ansible_module.command(AdvancedByTag.post_migrations())
    for result in teardown.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
    check_iptables = ansible_module.command("iptables -L")
    for rules in check_iptables.values():
        logger.info(rules["stdout"])
        assert "FOREMAN_MAINTAIN" not in rules["stdout"]


@pytest.mark.capsule
def test_positive_procedure_by_tag_restore_confirmation(ansible_module):
    """Run restore_confirmation using advanced procedure by-tag

    :id: f9e10352-04fb-49ba-8346-5b02e64fd028

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain advanced procedure by-tag
        restore

    :expectedresults: procedure restore_confirmation should work.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(AdvancedByTag.restore(["--assumeyes"]))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0


def test_positive_sync_plan_with_hammer_defaults(setup_for_hammer_defaults, ansible_module):
    """Verify that sync plan is disabled and enabled
    with hammer defaults set.

    :id: b25734c8-470f-4cad-bc56-5c0f75aa7499

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Setup hammer on system with defaults set

        2. Run foreman-maintain advanced procedure run sync-plans-enable

    :expectedresults: sync plans should get disabled and enabled.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Advanced.run_sync_plans_disable())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0
    contacted = ansible_module.command(Advanced.run_sync_plans_enable())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0


def test_positive_satellite_repositories_setup(setup_subscribe_to_cdn_dogfood, ansible_module):
    """Verify that all required repositories gets enabled.

    :id: e32fee2d-2a1f-40ed-9f94-515f75511c5a

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run 'foreman-maintain advanced procedure run repositories-setup --version 6.y

    :BZ: 1684730, 1869731

    :expectedresults: Required Satellite repositories should get enabled

    :CaseImportance: Critical
    """
    for ver in ["6.4", "6.5", "6.6", "6.7", "6.8"]:
        contacted = ansible_module.command(Advanced.run_repositories_setup({"version": ver}))
        for result in contacted.values():
            logger.info(result["stdout"])
            assert "FAIL" not in result["stdout"]
            assert result["rc"] == 0
        contacted = ansible_module.command("yum repolist")
        for result in contacted.values():
            logger.info(result["stdout"])
            for repo in sat_repos[ver]:
                assert repo in result["stdout"]
    # Verify that all required beta repositories gets enabled
    export_command = "export FOREMAN_MAINTAIN_USE_BETA=1;"
    contacted = ansible_module.shell(
        export_command + Advanced.run_repositories_setup({"version": "6.8"})
    )
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0
    contacted = ansible_module.command("yum repolist")
    for result in contacted.values():
        logger.info(result["stdout"])
        for repo in sat_beta_repo:
            assert repo in result["stdout"]


@pytest.mark.capsule
@pytest.mark.skipif(server() == "satellite", reason="Test intended to run only on Capsule servers")
def test_positive_capsule_repositories_setup(setup_subscribe_to_cdn_dogfood, ansible_module):
    """Verify that all required capsule repositories gets enabled.

    :id: 88558fb0-2268-469f-86ae-c4d18ccef782

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run 'foreman-maintain advanced procedure run repositories-setup --version 6.y

    :BZ: 1684730, 1869731

    :expectedresults: Required Capsule repositories should get enabled

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Advanced.run_repositories_setup({"version": "6.8"}))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0
    contacted = ansible_module.command("yum repolist")
    for result in contacted.values():
        logger.info(result["stdout"])
        for repo in cap_repos["6.8"]:
            assert repo in result["stdout"]
    # Verify that all required beta repositories gets enabled
    export_command = "export FOREMAN_MAINTAIN_USE_BETA=1;"
    contacted = ansible_module.shell(
        export_command + Advanced.run_repositories_setup({"version": "6.8"})
    )
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0
    contacted = ansible_module.command("yum repolist")
    for result in contacted.values():
        logger.info(result["stdout"])
        for repo in cap_beta_repo:
            assert repo in result["stdout"]
