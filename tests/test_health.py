import time

import pytest

from testfm.decorators import stubbed
from testfm.health import Health
from testfm.log import logger


@pytest.mark.capsule
def test_positive_foreman_maintain_health_list(ansible_module):
    """List health check in foreman-maintain

    :id: 976ef4cd-e028-4545-91bb-72433d40d7ee

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain health list

    :expectedresults: Health check list should work.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Health.list())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert result["rc"] == 0


@pytest.mark.capsule
def test_positive_foreman_maintain_health_list_tags(ansible_module):
    """List tags for health check in foreman-maintain

    :id: d0a6c8c1-8266-464a-bfdf-01d405dd9bd2

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain health list-tags

    :expectedresults: Tags for health checks should list.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Health.list_tags())
    for result in contacted.values():
        logger.info(result["stdout"])
        assert result["rc"] == 0


@pytest.mark.capsule
def test_positive_list_health_check_by_tags(ansible_module):
    """List health check in foreman-maintain by tags

    :id: 420d8e62-84d8-4496-8c24-037bd23febe9

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain health list --tags default

    :expectedresults: health checks according to tag should list.

    :CaseImportance: Critical
    """
    for tags in ["default", "pre-upgrade"]:
        contacted = ansible_module.command(Health.list({"tags": tags}))
        for result in contacted.values():
            logger.info(result["stdout"])
            assert result["rc"] == 0


@pytest.mark.capsule
def test_positive_foreman_maintain_health_check(ansible_module):
    """Verify foreman-maintain health check

    :id: bfff93dd-adde-4630-8411-1bb6b74daddd

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain health check

    :expectedresults: Health check should perform.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(
        Health.check(["-w", "puppet-check-no-empty-cert-requests,check-tftp-storage", "-y"])
    )
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]


@pytest.mark.capsule
def test_positive_foreman_maintain_health_check_by_tags(setup_install_pkgs, ansible_module):
    """Verify foreman-maintain health check by tags

        :id: 518e19af-2dd4-4fb0-8c90-208cbd354107

        :setup:
            1. foreman-maintain should be installed.

        :steps:
            1. Run foreman-maintain health check --tags tag_name

        :expectedresults: Health check should perform.

        :CaseImportance: Critical
        """
    contacted = ansible_module.command(Health.list_tags())
    for result in contacted.values():
        output = result["stdout"]
    output = [i.split("]\x1b[0m")[0] for i in output.split("\x1b[36m[") if i]
    for tag in output:
        contacted = ansible_module.command(Health.check(["--tags", tag, "--assumeyes"]))
        for result in contacted.values():
            logger.info(result["stdout"])
            assert "FAIL" not in result["stdout"]
            assert result["rc"] == 0


def test_positive_check_server_ping(ansible_module):
    """Verify server ping check

    :id: b1eec8cb-9f94-439a-b5e7-8621cb35501f

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain health check --label server-ping

    :expectedresults: Health check should perform.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Health.check({"label": "server-ping"}))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]


def test_negative_check_server_ping(setup_katello_service_stop, ansible_module):
    """Verify hammer ping check

    :id: ecdc5bfb-2adf-49f6-948d-995dae34bcd3

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run Katello-service stop
        2. Run foreman-maintain health check --label server-ping
        3. Run Katello-service start

    :expectedresults: Health check should perform.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Health.check({"label": "server-ping"}))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" in result["stdout"]


@pytest.mark.capsule
def test_positive_pre_upgrade_health_check(ansible_module):
    """Verify pre-upgrade health checks

    :id: f52bd43e-79cd-488b-adbb-3c9e5bac32cc

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain health check --tags pre-upgrade

    :expectedresults: Pre-upgrade health checks should perform.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Health.check({"tag": "pre-upgrade"}))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]


@pytest.mark.capsule
def test_positive_check_upstream_repository(setup_upstream_repository, ansible_module):
    """Verify upstream repository check

    :id: 349fcf33-2d25-4628-a6af-cff53e624b25

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain health check --label check-upstream-repository

    :expectedresults: Health check should perform.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(
        Health.check(["--label", "check-upstream-repository", "--assumeyes"])
    )
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" in result["stdout"]
        assert result["rc"] == 0


@pytest.mark.capsule
def test_positive_available_space(ansible_module):
    """Verify available-space check

    :id: 7d8798ca-3334-4dda-a9b0-dc3d7c0903e9

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain health check --label available-space

    :expectedresults: Health check should perform.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Health.check({"label": "available-space"}))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0


def test_positive_available_space_candlepin(ansible_module):
    """Verify available-space-cp check

    :id: 382a2bf3-a3da-4e46-b370-a443450f93b7

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain health check --label available-space-cp

    :expectedresults: Health check should perform.

    :CaseImportance: Medium
    """
    contacted = ansible_module.command(Health.check({"label": "available-space-cp"}))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0


def test_positive_automate_bz1632768(setup_hammer_defaults, ansible_module):
    """Verify that health check is performed when
     hammer on system have defaults set.

    :id: 27a8b49b-8cb8-4004-ba41-36ed084c4740

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Setup hammer on system with defaults set

        2. Run foreman-maintain health check

    :expectedresults: Health check should perform.

    :BZ: 1632768

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Health.check(["--assumeyes"]))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0


@pytest.mark.capsule
def test_positive_puppet_check_no_empty_cert_requests(ansible_module):
    """Verify puppet-check-no-empty-cert-requests

    :id: aad69254-9978-41e7-83a9-122e342a8dc5

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain health check --label puppet-check-no-empty-cert-requests

    :expectedresults: Health check should perform.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(
        Health.check({"label": "puppet-check-no-empty-cert-requests"})
    )
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0


@pytest.mark.capsule
def test_positive_puppet_check_empty_cert_requests(setup_puppet_empty_cert, ansible_module):
    """Verify puppet-check-no-empty-cert-requests

    :id: d4b9f725-d764-475a-9fc0-8db4aa1cb6ce

    :setup:
        1. foreman-maintain should be installed.
        2. have some empty files in ${puppet-check-no-empty-cert-requests}

    :steps:
        1. Run foreman-maintain health check --label puppet-check-no-empty-cert-requests

    :expectedresults: Health check should perform.

    :CaseImportance: Critical
    """
    response = r".* \[Delete empty CA cert request files\].*] "
    contacted = ansible_module.expect(
        command=Health.check({"label": "puppet-check-no-empty-cert-requests"}),
        responses={response: "yes"},
    )
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" in result["stdout"]
        assert result["rc"] == 0
    puppet_ssldir_path = ansible_module.command("puppet config print ssldir").values()[0]["stdout"]
    contacted = ansible_module.find(
        paths="{}/ca/requests/".format(puppet_ssldir_path), file_type="file", size="0"
    )
    assert contacted.values()[0]["matched"] == 0


@pytest.mark.capsule
def test_positive_check_hotfix_installed(setup_hotfix_check, setup_install_pkgs, ansible_module):
    """Verify check-hotfix-installed check.

    :id: d9023293-4173-4223-bbf5-328b41cf87cd

    :setup:
        1. foreman-maintain should be installed.

        2. modify some files of satellite.

        3. Install hotfix-package, python-kitchen, yum-utils packages.

    :steps:
        1. Run foreman-maintain health check --label check-hotfix-installed

    :expectedresults: check-hotfix-installed check should detect modified file
        and installed hotfix.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(
        Health.check(
            {"label": "check-hotfix-installed", "whitelist": "check-non-redhat-repository"}
        )
    )
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "WARNING" in result["stdout"]
        assert "hotfix-package" in result["stdout"]
        assert setup_hotfix_check in result["stdout"]
        assert result["rc"] == 78


@pytest.mark.capsule
def test_positive_check_hotfix_installed_without_hotfix(setup_install_pkgs, ansible_module):
    """Verify check-hotfix-installed check.

    :id: 3b6fbf3a-5c78-4283-996e-ca8da88a5d1b

    :setup:
        1. foreman-maintain should be installed.

        2. Install python-kitchen, yum-utils packages.
    :steps:
        1. Run foreman-maintain health check --label check-hotfix-installed

    :expectedresults: Health check should perform.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(
        Health.check(
            {"label": "check-hotfix-installed", "whitelist": "check-non-redhat-repository"}
        )
    )
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "WARNING" not in result["stdout"]
        assert result["rc"] == 0


@pytest.mark.capsule
def test_positive_check_validate_yum_config(ansible_module):
    """Verify validate-yum-config

    :id: b50c8866-6175-4286-8106-561945726023

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. configure yum exclude.
        2. Run foreman-maintain health check --label validate-yum-config
        3. Assert that excluded packages are listed in output.
        4. remove yum exclude configured in step 1.

    :expectedresults: validate-yum-config should work.

    :CaseImportance: Critical
    """
    file = "/etc/yum.conf"
    yum_exclude = "exclude='cat* bear*'"
    yum_clean_requirements = "clean_requirements_on_remove=1"
    failure_message = "Unset this configuration as it is risky while yum update or upgrade!"
    ansible_module.blockinfile(
        path=file, block=yum_exclude,
    )
    contacted = ansible_module.command(Health.check({"label": "validate-yum-config"}))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert yum_exclude in result["stdout"]
        assert failure_message in result["stdout"]
        assert result["rc"] == 1

    ansible_module.blockinfile(
        path=file, block=f"{yum_exclude} \n{yum_clean_requirements}",
    )

    contacted = ansible_module.command(Health.check({"label": "validate-yum-config"}))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert yum_exclude in result["stdout"]
        assert yum_clean_requirements in result["stdout"]
        assert failure_message in result["stdout"]
        assert result["rc"] == 1

    ansible_module.blockinfile(
        path=file, block=f"{yum_exclude} \n{yum_clean_requirements}", state="absent"
    )
    contacted = ansible_module.command(Health.check({"label": "validate-yum-config"}))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0


@pytest.mark.capsule
def test_positive_check_epel_repository(setup_epel_repository, ansible_module):
    """Verify check-non-redhat-repository.

    :id: ce2d7278-d7b7-4f76-9923-79be831c0368

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Configure epel repository.
        2. Run foreman-maintain health check --label check-non-redhat-repository.
        3. Assert that EPEL repos are enabled on system.

    :BZ: 1755755

    :expectedresults: check-non-redhat-repository should work.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Health.check({"label": "check-non-redhat-repository"}))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "System is subscribed to non Red Hat repositories" in result["stdout"]
        assert "FAIL" in result["stdout"]
        assert result["rc"] == 1


@stubbed
@pytest.mark.capsule
def test_positive_check_epel_repository_with_invalid_repo(
    setup_epel_repository, setup_invalid_repository, ansible_module
):
    """Verify check-non-redhat-repository.

    :id: e41648f4-ada6-4e7e-9112-45146d308410

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Configure epel repository and a repository with invalid baseurl.
        2. Run foreman-maintain health check --label check-non-redhat-repository.
        3. Assert that EPEL repos are enabled on system.

    :BZ: 1755755

    :expectedresults: check-non-redhat-repository should work.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Health.check({"label": "check-non-redhat-repository"}))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "System is subscribed to non Red Hat repositories" in result["stdout"]
        assert "FAIL" in result["stdout"]
        assert result["rc"] == 1


def test_positive_check_old_foreman_tasks(setup_old_foreman_tasks, ansible_module):
    """Verify check-old-foreman-tasks.

    :id: 156350c4-b55b-40b3-b8f2-202bd5ed9fb6

    :setup:
        1. foreman-maintain should be installed.
        2. Run setup_old_foreman_tasks from conftest.py

    :steps:
        1. Configure epel repository.
        2. Run foreman-maintain health check --label check-non-redhat-repository.
        3. Assert that old tasks are found on system.
        4. Assert that old tasks are deleted from system.

    :BZ: 1745489

    :expectedresults: check-old-foreman-tasks should work.

    :CaseImportance: Critical
    """
    error_message = "paused or stopped task(s) older than 30 days"
    delete_message = "Deleted old tasks:"
    contacted = ansible_module.command(
        Health.check(["--label", "check-old-foreman-tasks", "--assumeyes"])
    )
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" in result["stdout"]
        assert result["rc"] == 0
        assert error_message in result["stdout"]
        assert delete_message in result["stdout"]
    contacted = ansible_module.command(Health.check(["--label", "check-old-foreman-tasks"]))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0


@pytest.mark.capsule
def test_positive_check_tmout_variable(ansible_module):
    """Verify check-tmout-variable. Upstream issue #23430.

    :id: e0eea928-0ffb-4692-adb9-fc4bf041f301

    :setup:
        1. foreman-maintain should be installed.
        2. export TMOUT environment variable.

    :steps:
        1. Run foreman-maintain health check --label check-tmout-variable.
        2. Assert that check-tmout-variable pass.
        3. export TMOUT environment variable.
        4. Run foreman-maintain health check --label check-tmout-variable.
        5. Assert that check-tmout-variable fails.

    :expectedresults: check-tmout-variable should work.

    :CaseImportance: Critical
    """
    export = "export TMOUT=100;"
    error_message = (
        "The TMOUT environment variable is set with value 100. "
        "Run 'unset TMOUT' command to unset this variable."
    )
    # Run check without setting TMOUT environment variable.
    contacted = ansible_module.command(Health.check({"label": "check-tmout-variable"}))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0
    # Run check with TMOUT environment variable set.
    contacted = ansible_module.shell(export + Health.check({"label": "check-tmout-variable"}))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" in result["stdout"]
        assert error_message in result["stdout"]
        assert result["rc"] == 1


def test_positive_check_tftp_storage(ansible_module, setup_tftp_storage):
    """Verify check-tftp-storage

    :id: 9a900bc7-65ff-4280-bf8a-8974a7cb76c6

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Create test files in /var/lib/tftpboot/boot/
        2. Run foreman-maintain health check --label check-tftp-storage.
        3. Assert that check-tftp-storage fails.
        4. Assert that check deletes files older than token_duration setting.
        5. Delete all files from /var/lib/tftpboot/boot/
        6. Run foreman-maintain health check --label check-tftp-storage.
        7. Assert that check-tftp-storage pass.

    :expectedresults: check-tftp-storage should work.

    :CaseImportance: Critical
    """
    files = [
        "foreman-discovery-vmlinuz",
        "foreman-discovery-initrd.img",
        "do-not-delete.yml",
        "keep-discovery-initrd.img",
    ]
    # Create files for testing check-tftp-storage check.
    for file in files[:3]:
        setup = ansible_module.file(path=f"/var/lib/tftpboot/boot/{file}", state="touch")
        assert setup.values()[0]["changed"] == 1
    time.sleep(200)
    setup = ansible_module.file(path=f"/var/lib/tftpboot/boot/{files[-1]}", state="touch")
    assert setup.values()[0]["changed"] == 1
    # Run check-tftp-storage check.
    contacted = ansible_module.command(
        Health.check(["--label", "check-tftp-storage", "--assumeyes"])
    )
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "There are old initrd and vmlinuz files present in tftp" in result["stdout"]
        assert "Rerunning the check after fix procedure" in result["stdout"]
        assert "FAIL" in result["stdout"]
        assert result["rc"] == 0
    # check whether expected files are deleted
    for file in files[:2]:
        contacted = ansible_module.file(path=f"/var/lib/tftpboot/boot/{file}", state="absent")
        assert contacted.values()[0]["changed"] is False
    # check whether expected files are not deleted.
    for file in files[2:]:
        contacted = ansible_module.file(path=f"/var/lib/tftpboot/boot/{file}", state="present")
        assert contacted.values()[0]["changed"] is False
        ansible_module.file(path=f"/var/lib/tftpboot/boot/{file}", state="absent")
    # Re-run check with no files present in /var/lib/tftpboot/boot/
    contacted = ansible_module.command(Health.check(["--label", "check-tftp-storage"]))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0


def test_positive_check_postgresql_checkpoint_segments(ansible_module):
    """Verify check-postgresql-checkpoint-segments

    :id: 963a5b47-168a-4443-9fdf-bba59c9b0e97

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Add config_entries section in /etc/foreman-installer/custom-hiera.yaml
        2. Run foreman-maintain health check --label check-postgresql-checkpoint-segments.
        3. Assert that check-postgresql-checkpoint-segments fails.
        4. Add checkpoint_segments parameter in /etc/foreman-installer/custom-hiera.yaml
        5. Run foreman-maintain health check --label check-postgresql-checkpoint-segments.
        6. Assert that check-postgresql-checkpoint-segments fails.
        7. Remove config_entries section from /etc/foreman-installer/custom-hiera.yaml
        8. Run foreman-maintain health check --label check-postgresql-checkpoint-segments.
        9. Assert that check-postgresql-checkpoint-segments pass.

    :expectedresults: check-postgresql-checkpoint-segments should work.

    :CaseImportance: High
    """
    # Add config_entries section
    ansible_module.blockinfile(
        path="/etc/foreman-installer/custom-hiera.yaml",
        block="postgresql::server::config_entries:",
    )
    # Run check-postgresql-checkpoint-segments check.
    contacted = ansible_module.command(
        Health.check(["--label", "check-postgresql-checkpoint-segments"])
    )
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "ERROR: 'postgresql::server::config_entries' cannot be null." in result["stdout"]
        assert "Please remove it from following file and re-run the command." in result["stdout"]
        assert "FAIL" in result["stdout"]
        assert result["rc"] == 1
    # Add checkpoint_segments
    ansible_module.blockinfile(
        path="/etc/foreman-installer/custom-hiera.yaml",
        block="postgresql::server::config_entries: \n  checkpoint_segments: 32",
    )
    # Run check-postgresql-checkpoint-segments check.
    contacted = ansible_module.command(
        Health.check(["--label", "check-postgresql-checkpoint-segments"])
    )
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "ERROR: Tuning option 'checkpoint_segments' found." in result["stdout"]
        assert "Please remove it from following file and re-run the command." in result["stdout"]
        assert "FAIL" in result["stdout"]
        assert result["rc"] == 1
    # Remove config_entries section
    ansible_module.blockinfile(
        path="/etc/foreman-installer/custom-hiera.yaml",
        block="postgresql::server::config_entries: \n  checkpoint_segments: 32",
        state="absent",
    )
    # Run check-postgresql-checkpoint-segments check.
    contacted = ansible_module.command(
        Health.check(["--label", "check-postgresql-checkpoint-segments"])
    )
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0


@pytest.mark.capsule
def test_positive_check_env_proxy(ansible_module):
    """Verify env-proxy.

    :id: f8c44b40-3ce5-4179-8d6b-1156c0032450

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. export HTTP_PROXY environment variable.
        2. Run foreman-maintain health check --label env-proxy.
        3. Assert that check env-proxy fail.
        4. Run foreman-maintain health check --label env-proxy.
        5. Assert that check env-proxy pass.

    :expectedresults: check env-proxy should work.

    :CaseImportance: Medium
    """
    export = "export  HTTP_PROXY=https://proxy.example.com:5442;"
    error_message = "Global HTTP(S) proxy in environment (env) is set. Please unset first!"
    # Run check with HTTP_PROXY environment variable set.
    contacted = ansible_module.shell(export + Health.check({"label": "env-proxy"}))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" in result["stdout"]
        assert error_message in result["stdout"]
        assert result["rc"] == 1

    # Run check without setting HTTP_PROXY environment variable.
    contacted = ansible_module.command(Health.check({"label": "env-proxy"}))
    for result in contacted.values():
        logger.info(result["stdout"])
        assert "FAIL" not in result["stdout"]
        assert result["rc"] == 0


@stubbed
def test_positive_check_foreman_proxy_verify_dhcp_config_syntax(ansible_module):
    """Verify foreman-proxy-verify-dhcp-config-syntax

    :id: 43ca5cc7-9888-490d-b1ba-f3298e737039

    :setup:
        1. foreman-maintain should be installed.
        2. Satellite instance configured with external DHCP like Infoblox,
           which has `:use_provider: dhcp_infoblox` set in /etc/foreman-proxy/settings.d/dhcp.yml
        3. Satellite instance which is DHCP enabled and has `:use_provider: dhcp_isc`
           set in /etc/foreman-proxy/settings.d/dhcp.yml

    :steps:
        1. foreman-maintain health list | grep foreman-proxy-verify-dhcp-config-syntax
        2. foreman-maintain health check --label foreman-proxy-verify-dhcp-config-syntax

    :BZ: 1847889

    :expectedresults: Check is not available on the satellite instances where `:use_provider:`
                      is set other than `dhcp_isc`, and also not on DHCP disabled Satellite.


    :CaseImportance: Medium
    """


def test_positive_remove_job_file(setup_subscribe_to_cdn_dogfood, ansible_module):
    """Verify file /var/lib/pulp/job1.0.0 is not present after the following command.

    :id: eed224f9-a2ec-4d15-9047-cede0b823866

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain health list --tags pre-upgrade
        2. Run foreman-maintain health check --label disk-performance

    :expectedresults: `disk-performance` shouldn't exist under pre-upgrade tag and
            /var/lib/pulp/job1.0.0 file should not exist after check execution

    :CaseImportance: Medium

    :BZ: 1827219, 1762302
    """
    # Verify pre-upgrade checks don't include disk-performance check
    contacted = ansible_module.command(Health.list({"tags": "pre-upgrade"}))
    for result in contacted.values():
        assert "disk-performance" not in result["stdout"]

    # Verify job1.0.0 file not exist after check completion
    contacted = ansible_module.command(
        Health.check(["--label", "disk-performance", "--assumeyes"])
    )
    contacted = ansible_module.find(paths="/var/lib/pulp", file_type="file")
    for file in contacted.values()[0]["files"]:
        assert "job" not in file["path"]
