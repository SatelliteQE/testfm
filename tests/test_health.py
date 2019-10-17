from testfm.decorators import capsule, stubbed
from testfm.health import Health
from testfm.log import logger


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
        logger.info(result['stdout'])
        assert result["rc"] == 0


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
        logger.info(result['stdout'])
        assert result["rc"] == 0


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
    for tags in ['default', 'pre-upgrade']:
        contacted = ansible_module.command(Health.list({
            'tags': tags
        }))
        for result in contacted.values():
            logger.info(result['stdout'])
            assert result["rc"] == 0


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
    contacted = ansible_module.command(Health.check([
        '-w', 'puppet-check-no-empty-cert-requests', '-y']))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']


def test_positive_foreman_maintain_health_check_by_tags(ansible_module):
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
        output = result['stdout']
    output = [i.split(']\x1b[0m')[0] for i in output.split('\x1b[36m[') if i]
    for tag in output:
        contacted = ansible_module.command(Health.check({
            'tags': tag,
            'whitelist': 'disk-performance, packages-install'
        }))
        for result in contacted.values():
            logger.info(result['stdout'])
            assert "FAIL" not in result['stdout']
            assert result['rc'] == 0


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
    contacted = ansible_module.command(Health.check({
        'label': 'server-ping'
    }))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']


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
    contacted = ansible_module.command(Health.check({
        'label': 'server-ping'
    }))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" in result['stdout']


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
    contacted = ansible_module.command(Health.check({
        'tag': 'pre-upgrade'
    }))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']


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
    contacted = ansible_module.command(Health.check([
            '--label', 'check-upstream-repository', '--assumeyes'
        ]))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" in result['stdout']
        assert result['rc'] == 0


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
    contacted = ansible_module.command(Health.check({
        'label': 'available-space'
    }))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0


def test_positive_automate_bz1632768(teardown_hammer_defaults, ansible_module):
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
    contacted = ansible_module.command(Health.check([
        '--assumeyes']))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0


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
    contacted = ansible_module.command(Health.check({
        'label': 'puppet-check-no-empty-cert-requests'}))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0


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
    response = '.* \[Delete empty CA cert request files\].*] '
    contacted = ansible_module.expect(
        command=Health.check({'label': 'puppet-check-no-empty-cert-requests'}),
        responses={response: "yes"})
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" in result['stdout']
        assert result['rc'] == 0
    puppet_ssldir_path = ansible_module.command(
        'puppet master --configprint ssldir').values()[0]['stdout']
    contacted = ansible_module.find(
        paths='{}/ca/requests/'.format(puppet_ssldir_path),
        file_type='file',
        size='0'
    )
    assert contacted.values()[0]['matched'] == 0


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
    contacted = ansible_module.command(Health.check({
        'label': 'check-hotfix-installed'
    }))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "WARNING" in result['stdout']
        assert "hotfix-package" in result['stdout']
        assert setup_hotfix_check in result['stdout']
        assert result['rc'] == 1


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
    contacted = ansible_module.command(Health.check({
        'label': 'check-hotfix-installed'
    }))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "WARNING" not in result['stdout']
        assert result['rc'] == 0


def test_positive_check_yum_exclude_list(setup_yum_exclude, ansible_module):
    """Verify check-yum-exclude-list

    :id: b50c8866-6175-4286-8106-561945726023

    :setup:
        1. foreman-maintain should be installed.
        2. configure yum exclude.

    :steps:
        1. configure yum exclude.
        2. Run foreman-maintain health check --label check-yum-exclude-list
        3. Assert that excluded packages are listed in output.
        4. remove yum exclude configured in step 1.

    :expectedresults: check-yum-exclude-list should work.

    :CaseImportance: Critical
    """
    yum_exclude = setup_yum_exclude(exclude='cat* bear*')
    contacted = ansible_module.command(Health.check({
        'label': 'check-yum-exclude-list'}))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert yum_exclude in result['stdout']
        assert result["rc"] == 1


def test_positive_check_yum_exclude_list_without_excludes(ansible_module):
    """Verify check-yum-exclude-list.

    :id: 12ed3d41-abc7-45bb-8234-6e3a45229254

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain health check --label check-yum-exclude-list
        2.Assert that no packages are listed in output.

    :expectedresults: check-yum-exclude-list should work.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Health.check({
        'label': 'check-yum-exclude-list'}))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result["rc"] == 0


@capsule
def test_positive_check_epel_repository(setup_epel_repository, ansible_module):
    """Verify check-epel-repository.

    :id: ce2d7278-d7b7-4f76-9923-79be831c0368

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Configure epel repository.
        2. Run foreman-maintain health check --label check-epel-repository.
        3. Assert that EPEL repos are enabled on system.

    :BZ: 1755755

    :expectedresults: check-epel-repository should work.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Health.check({
        'label': 'check-epel-repository'}))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "System is subscribed to EPEL repository" in result['stdout']
        assert "FAIL" in result['stdout']
        assert result["rc"] == 1


@stubbed
@capsule
def test_positive_check_epel_repository_with_invalid_repo(
        setup_epel_repository, setup_invalid_repository, ansible_module):
    """Verify check-epel-repository.

    :id: e41648f4-ada6-4e7e-9112-45146d308410

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Configure epel repository and a repository with invalid baseurl.
        2. Run foreman-maintain health check --label check-epel-repository.
        3. Assert that EPEL repos are enabled on system.

    :BZ: 1755755

    :expectedresults: check-epel-repository should work.

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Health.check({
        'label': 'check-epel-repository'}))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "System is subscribed to EPEL repository" in result['stdout']
        assert "FAIL" in result['stdout']
        assert result["rc"] == 1
