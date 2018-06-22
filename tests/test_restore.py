from testfm.backup import Backup
from testfm.decorators import capsule
from testfm.log import logger
from testfm.restore import Restore


@capsule
def test_positive_restore_online_backup(ansible_module):
    """Restore online backup of server

    :id: 3b83f757-2bf8-49ff-b237-bd466c5694bb

    :setup:

        1. foreman-maintain should be installed.
        2. Take online backup of server.
    :steps:
        1. Run foreman-maintain restore /backup_dir/

    :expectedresults: Restore should successful.

    :CaseImportance: Critical
    """
    setup = ansible_module.command(Backup.run_online_backup([
        '-y', '/tmp/online_backup_restore/']))
    for result in setup.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
    contacted = ansible_module.command(Restore._construct_command(
        ['-y', '/tmp/online_backup_restore/']))
    for result in contacted.values():
        logger.info(result)
        assert "FAIL" not in result['stdout']
