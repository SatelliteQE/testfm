from testfm import settings
from testfm.helpers import rhel7

RHN_USERNAME = settings.subscription.rhn_username
RHN_PASSWORD = settings.subscription.rhn_password
FM_RHN_POOLID = settings.subscription.fm_rhn_poolid
DOGFOOD_ORG = settings.subscription.dogfood_org
DOGFOOD_ACTIVATIONKEY = settings.subscription.dogfood_activationkey
CAPSULE_DOGFOOD_ACTIVATIONKEY = settings.subscription.capsule_dogfood_activationkey
DOGFOOD_URL = settings.subscription.dogfood_url
REPOS_HOSTING_URL = settings.robottelo.repos_hosting_url
HOTFIX_URL = f"{REPOS_HOSTING_URL}/hotfix_package/"
FAKE_YUM0_REPO = f"{REPOS_HOSTING_URL}/fake_yum0/"

katello_ca_consumer = DOGFOOD_URL + "/pub/katello-ca-consumer-latest.noarch.rpm"
upstream_url = {
    "candlepin_repo": (
        "https://fedorapeople.org/groups/katello/releases/yum/3.8/candlepin/el7/x86_64/"
    ),
    "client_repo": "https://fedorapeople.org/groups/katello/releases/yum/3.8/client/el7/x86_64/",
    "katello_repo": (
        "https://fedorapeople.org/groups/katello/releases/yum/latest/katello/el7/x86_64/"
    ),
    "plugins_repo": "https://yum.theforeman.org/plugins/latest/el7/x86_64/",
    "pulp_repo": "https://fedorapeople.org/groups/katello/releases/yum/3.5/pulp/el7/x86_64/",
    "puppet_repo": "http://yum.puppetlabs.com/el/6.4/x86_64/",
    "releases_repo": "https://yum.theforeman.org/releases/latest/el7/x86_64/",
}

# Common repositories for Satellite and Capsule
common_repos = (
    [
        "rhel-7-server-rpms",
        "rhel-server-rhscl-7-rpms",
        "rhel-7-server-ansible-2.9-rpms",
    ]
    if rhel7()
    else [
        "rhel-8-for-x86_64-baseos-rpms",
        "rhel-8-for-x86_64-appstream-rpms",
        "ansible-2.9-for-rhel-8-x86_64-rpms",
    ]
)

# Satellite repositories
sat_68_repos = [
    "rhel-7-server-satellite-6.8-rpms",
    "rhel-7-server-satellite-maintenance-6-rpms",
] + common_repos

sat_69_repos = [
    "rhel-7-server-satellite-6.9-rpms",
    "rhel-7-server-satellite-maintenance-6-rpms",
] + common_repos

sat_610_repos = [
    "rhel-7-server-satellite-6.10-rpms",
    "rhel-7-server-satellite-maintenance-6-rpms",
] + common_repos

sat_70_repos = (
    [
        "rhel-7-server-satellite-7.0-rpms",
        "rhel-7-server-satellite-maintenance-7.0-rpms",
    ]
    if rhel7()
    else [
        "satellite-7.0-for-rhel-8-x86_64-rpms",
        "satellite-maintenance-7.0-for-rhel-8-x86_64-rpms",
    ]
) + common_repos

# Satellite Beta repositories
sat_beta_repo = [
    "rhel-server-7-satellite-6-beta-rpms",
    "rhel-7-server-satellite-maintenance-6-beta-rpms",
] + common_repos

# Capsule repositories
cap_68_repos = [
    "rhel-7-server-satellite-capsule-6.8-rpms",
    "rhel-7-server-satellite-maintenance-6-rpms",
] + common_repos

cap_69_repos = [
    "rhel-7-server-satellite-capsule-6.9-rpms",
    "rhel-7-server-satellite-maintenance-6-rpms",
] + common_repos

cap_610_repos = [
    "rhel-7-server-satellite-capsule-6.10-rpms",
    "rhel-7-server-satellite-maintenance-6-rpms",
] + common_repos

cap_70_repos = (
    [
        "rhel-7-server-satellite-capsule-7.0-rpms",
        "rhel-7-server-satellite-maintenance-7.0-rpms",
    ]
    if rhel7()
    else [
        "satellite-capsule-7.0-for-rhel-8-x86_64-rpms",
        "satellite-maintenance-7.0-for-rhel-8-x86_64-rpms",
    ]
) + common_repos

# Capsule Beta repositories
cap_beta_repo = [
    "rhel-server-7-satellite-capsule-6-beta-rpms",
    "rhel-7-server-satellite-maintenance-6-beta-rpms",
] + common_repos

sat_repos = {
    "6.8": sat_68_repos,
    "6.9": sat_69_repos,
    "6.10": sat_610_repos,
    "7.0": sat_70_repos,
}
cap_repos = {
    "6.8": cap_68_repos,
    "6.9": cap_69_repos,
    "6.10": cap_610_repos,
    "7.0": cap_70_repos,
}
satellite_maintain_yml = "/etc/foreman-maintain/foreman_maintain.yml"
epel_repo = "https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm"
satellite_answer_file = "/etc/foreman-installer/scenarios.d/satellite-answers.yaml"
fm_hammer_yml = "/etc/foreman-maintain/foreman-maintain-hammer.yml"
gems_path = f"""{f"{'/opt/theforeman/tfm/root' if rhel7() else ''}" + '/usr/share/gems/gems/'}"""
