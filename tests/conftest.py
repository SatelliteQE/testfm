import datetime
from fauxfactory import gen_string
import pytest
from testfm.advanced import Advanced
from testfm.constants import (
    DOGFOOD_ACTIVATIONKEY,
    DOGFOOD_ORG,
    katello_ca_consumer,
    RHN_PASSWORD,
    RHN_USERNAME,
    RHN_POOLID,
    HOTFIX_URL,
    upstream_url,
)
from testfm.log import logger


@pytest.fixture(scope='function')
def setup_yum_exclude(request, ansible_module):
    """This fixture is used for adding and then removing yum excludes in /etc/yum.conf file.
    """
    file = '/etc/yum.conf'

    def yum_exclude(exclude):
        exclude = 'exclude=' + exclude
        ansible_module.lineinfile(
            dest=file,
            insertafter='EOF',
            line=exclude)
        request.addfinalizer(teardown_yum_exclude)
        return exclude

    def teardown_yum_exclude():
        ansible_module.lineinfile(
            dest=file,
            state='absent',
            regexp='^exclude=')
    return yum_exclude


@pytest.fixture(scope='function')
def setup_hotfix_check(request, ansible_module):
    """This fixture is used for installing hofix package and modifying foreman file.
    This fixture is used in test_positive_check_hotfix_installed_with_hotfix of test_health.py
    """
    file = ansible_module.find(
        paths='/opt/theforeman/tfm/root/usr/share/gems/gems/',
        patterns='fog-vsphere-*',
        file_type='directory')
    dpath = file.values()[0]['files'][0]['path']
    fpath = dpath + '/lib/fog/vsphere/requests/compute/list_clusters.rb'
    ansible_module.lineinfile(
        dest=fpath,
        insertafter='EOF',
        line="#modifying_file")

    ansible_module.yum_repository(
        name='hotfix_repo',
        description='hotfix_repo',
        file="hotfix_repo",
        baseurl=HOTFIX_URL,
        enabled="yes",
        gpgcheck="no"
    )
    setup = ansible_module.file(
        path='/etc/yum.repos.d/hotfix_repo.repo',
        state='present')
    assert setup.values()[0]["changed"] == 0
    setup = ansible_module.yum(
        name='hotfix-package',
        state='present')
    for result in setup.values():
        assert result['rc'] == 0

    def teardown_hotfix_check():
        teardown = ansible_module.command(
            'yum -y reinstall tfm-rubygem-fog-vsphere')
        for result in teardown.values():
            assert result['rc'] == 0
        teardown = ansible_module.file(
            path='/etc/yum.repos.d/hotfix_repo.repo',
            state='absent')
        assert teardown.values()[0]["changed"] == 1
        teardown = ansible_module.yum(
            name=['hotfix-package'],
            state='absent')
        for result in teardown.values():
            assert result['rc'] == 0
        ansible_module.command('yum clean all')
    request.addfinalizer(teardown_hotfix_check)
    return fpath


@pytest.fixture(scope='function')
def setup_install_pkgs(ansible_module):
    """This fixture installs necessary packages required by Testfm testcases to run properly.
    This fixture is used in test_positive_check_hotfix_installed_with_hotfix and
    test_positive_check_hotfix_installed_without_hotfix of test_health.py
    """
    setup = ansible_module.yum(
        name=['python-kitchen', 'yum-utils'],
        state='present')
    for result in setup.values():
        assert result['rc'] == 0


@pytest.fixture(scope='function')
def setup_for_hammer_defaults(request, ansible_module):
    """This fixture is used to add/delete hammer defaults value.
    It is used by test test_positive_sync_plan_with_hammer_defaults of test_advanced.py.
    """
    setup = ansible_module.command(
        "hammer defaults add --param-name organization_id --param-value 1")
    assert setup.values()[0]["rc"] == 0

    def teardown_for_hammer_defaults():
        teardown = ansible_module.command(
            "hammer defaults delete --param-name organization_id")
        assert teardown.values()[0]["rc"] == 0
    request.addfinalizer(teardown_for_hammer_defaults)


@pytest.fixture(scope='function')
def setup_katello_service_stop(request, ansible_module):
    """This fixture is used to stop/start katello services.
    It is used by test test_negative_check_hammer_ping of test_health.py.
    """
    setup = ansible_module.command(Advanced.run_katello_service_stop())
    for result in setup.values():
        assert result['rc'] == 0

    def teardown_katello_service_start():
        teardown = ansible_module.command(Advanced.run_service_start())
        for result in teardown.values():
            logger.info(result['stdout'])
            assert result['rc'] == 0
    request.addfinalizer(teardown_katello_service_start)


@pytest.fixture(scope='function')
def setup_install_pexpect(ansible_module):
    """This fixture is used to install pexpect on host.
    It is used by test test_positive_foreman_maintain_hammer_setup,
    test_positive_foreman_tasks_ui_investigate of test_advanced.py and in
    fixture setup_puppet_empty_cert.
    """
    ansible_module.get_url(
        url='https://bootstrap.pypa.io/get-pip.py',
        dest='/root'
    )
    setup = ansible_module.command("python /root/get-pip.py")
    for result in setup.values():
        assert result["rc"] == 0
    setup = ansible_module.command("pip install pexpect")
    for result in setup.values():
        assert result["rc"] == 0


@pytest.fixture(scope='function')
def setup_sync_plan(request, ansible_module):
    """This fixture is used to create/delete sync-plan.
    It is used by test test_positive_sync_plan_disable_enable of test_advanced.py.
    """
    sync_plan_name = gen_string('alpha')
    sync_date = datetime.datetime.today().strftime('%Y-%m-%d')
    setup = ansible_module.command(
        'hammer sync-plan create --name {0} --enabled true \
        --interval "weekly" --sync-date {1} --organization-id 1'.format(
            sync_plan_name, sync_date))
    for result in setup.values():
        assert result["rc"] == 0
    setup = ansible_module.command(
        'hammer --output csv sync-plan info --name {0} --organization-id 1'.format(
            sync_plan_name))
    sync_id = setup.values()[0]['stdout_lines'][1].split(',')[0]

    def teardown_sync_plan():
        teardown = ansible_module.command(
            'hammer sync-plan delete --name {0} --organization-id 1'.format(
                sync_plan_name))
        for result in teardown.values():
            assert result["rc"] == 0
    request.addfinalizer(teardown_sync_plan)
    return int(sync_id)


@pytest.fixture(scope='function')
def setup_puppet_empty_cert(setup_install_pexpect, ansible_module):
    """This fixture is used to create empty puppet cert and also uses
    setup_install_pexpect fixture to install pexpect.
    It is used by test test_positive_puppet_check_empty_cert_requests of test_health.py.
    """
    fname = gen_string('alpha')
    puppet_ssldir_path = ansible_module.command(
        'puppet master --configprint ssldir').values()[0]['stdout']
    setup = ansible_module.file(
        path='{0}/ca/requests/{1}'.format(puppet_ssldir_path, fname),
        state='touch')
    assert setup.values()[0]["changed"] == 1


@pytest.fixture(scope='function')
def setup_upstream_repository(request, ansible_module):
    """This fixture is used to create/delete upstream repositories.
    It is used by test test_positive_check_upstream_repository of test_health.py.
    """
    for name, url in upstream_url.items():
        ansible_module.yum_repository(
            name=name,
            description=name,
            file="upstream_repo",
            baseurl=url,
            enabled="yes",
            gpgcheck="no"
            )
    setup = ansible_module.file(
        path='/etc/yum.repos.d/upstream_repo.repo',
        state='present')
    assert setup.values()[0]["changed"] == 0

    def teardown_upstream_repository():
        teardown = ansible_module.file(
            path='/etc/yum.repos.d/upstream_repo.repo',
            state='absent')
        assert teardown.values()[0]["changed"] == 1
        ansible_module.command('yum clean all')
    request.addfinalizer(teardown_upstream_repository)


@pytest.fixture(scope='function')
def setup_subscribe_to_cdn_dogfood(request, ansible_module):
    """This fixture is used to subscribe host to CDN if it's subscribed to dogfood
    and unsubscribe from CDN after test finishes and subscribe back to doogfood.
    It is used by test test_positive_repositories_setup of test_health.py.
    """
    subscribed_to = str(ansible_module.command(
        'subscription-manager identity').values()[0]['stdout'])
    if "Quality Assurance" in subscribed_to:
        subscribed_to_cdn = True
    else:
            subscribed_to_cdn = False
    if subscribed_to_cdn is False:
        ansible_module.command('subscription-manager unregister')
        ansible_module.command('subscription-manager clean')
        ca_consumer = ansible_module.command(
            'yum list katello-ca-consumer*').values()[0]['stdout']
        if 'katello-ca-consumer' in ca_consumer:
            pkg_name = [t for t in ca_consumer.split() if t.startswith('katello-ca-consumer')][0]
            ansible_module.yum(name=pkg_name,
                               state='absent')
        ansible_module.command(
            'subscription-manager register --force --user="{0}" --password="{1}"'.format(
                RHN_USERNAME, RHN_PASSWORD))
        for pool_id in RHN_POOLID.split():
            ansible_module.command(
                'subscription-manager subscribe --pool={0}'.format(pool_id))

    def teardown_subscribe_to_cdn_dogfood():
        if subscribed_to_cdn is False:
            ansible_module.command('subscription-manager unregister')
            ansible_module.command('subscription-manager clean')
            ansible_module.command(
                'yum -y localinstall {0}'.format(katello_ca_consumer))
            ansible_module.command(
                'subscription-manager register --force --org="{0}" --activationkey="{1}"'.format(
                    DOGFOOD_ORG, DOGFOOD_ACTIVATIONKEY))

    request.addfinalizer(teardown_subscribe_to_cdn_dogfood)
