from testfm.health import Health
from testfm.upgrade import Upgrade
from testfm.advanced import Advanced


def check_health():
    """
    Usage:
    foreman-maintain health check [OPTIONS]

    Options:
        --label label                 Limit only for a specific label.
                                      (Use "list" command to see available
                                       labels)
        --tags tags                   Limit only for specific set of labels.
                                      (Use list-tags command to see available
                                      tags) (comma-separated list)
        -y, --assumeyes               Automatically answer yes for all
                                      questions
        -w, --whitelist whitelist     Comma-separated list of labels of steps
                                      to be ignored
        -f, --force                   Force steps that would be skipped as they
                                      were already run
        -h, --help                    print help
    """

    return Health.check()


def list_versions():
    """
    Usage:
    foreman-maintain upgrade list-versions [OPTIONS]

    Options:
        -h, --help                    print help
    """

    return Upgrade.list_versions()


def advanced_procedure_run_service_restart():
    """
    Usage:
    foreman-maintain advanced procedure run katello-service-restart [OPTIONS]

    Options:
        --only ONLY                   A comma-separated list of services to
                                      include (comma-separated list)
        --exclude EXCLUDE             A comma-separated list of services to
                                      skip (comma-separated list)
        -y, --assumeyes               Automatically answer yes for all
                                      questions
        -w, --whitelist whitelist     Comma-separated list of labels of steps
                                      to be ignored
        -f, --force                   Force steps that would be skipped as they
                                      were already run
        -h, --help                    print help
    """

    return Advanced.run_katello_service_restart()
