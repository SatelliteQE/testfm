from testfm.backup import Backup
from testfm.decorators import capsule
from testfm.log import logger
from testfm.restore import Restore
from fauxfactory import gen_string

NODIR_MSG = "ERROR: parameter 'BACKUP_DIR': no value provided"
BADDIR_MSG = ("The given directory does not contain the "
              "required files or has too many files")


@capsule
def test_positive_restore_online_backup(ansible_module):
    """Restore online backup of server

    :id: 3b83f757-2bf8-49ff-b237-bd466c5694bb

    :setup:

        1. foreman-maintain should be installed.
        2. Take online backup of server.
    :steps:
        1. Run foreman-maintain restore /backup_dir/

    :expectedresults: Restore successful.

    :CaseImportance: Critical
    """
    # preparing a target dir
    backup_dir = 'online_backup_restore'
    setup = ansible_module.command("rm -rf /tmp/{}".format(backup_dir))
    assert setup.values()[0]["rc"] == 0
    setup = ansible_module.file(
            path="/tmp/{}".format(backup_dir),
            state="directory",
            owner="postgres",
    )
    # saving backup to specified dir
    setup = ansible_module.command(Backup.run_online_backup([
        '-y', '--preserve-directory', '/tmp/{}'.format(backup_dir)]))
    for result in setup.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0
    # restore from previously saved backup
    contacted = ansible_module.command(Restore._construct_command(
        ['-y', '/tmp/{}'.format(backup_dir)]))
    for result in contacted.values():
        logger.info(result)
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0


@capsule
def test_positive_restore_offline_backup(ansible_module):
    """Restore offline backup of server

    :id: 1005c983-13d4-451b-8115-8fce504104ee

    :setup:

        1. foreman-maintain should be installed.
        2. Take offline backup of server.
    :steps:
        1. Run foreman-maintain restore /backup_dir/

    :expectedresults: Restore successful.

    :CaseImportance: Critical
    """
    # preparing a target dir
    backup_dir = 'offline_backup_restore'
    setup = ansible_module.command("rm -rf /tmp/{}".format(backup_dir))
    assert setup.values()[0]["rc"] == 0
    setup = ansible_module.file(
            path="/tmp/{}".format(backup_dir),
            state="directory",
            owner="postgres",
    )
    # saving backup to specified dir
    setup = ansible_module.command(Backup.run_offline_backup([
        '-y', '--preserve-directory', '/tmp/{}'.format(backup_dir)]))
    for result in setup.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0
    # restore from previously saved backup
    contacted = ansible_module.command(Restore._construct_command(
        ['-y', '/tmp/{}'.format(backup_dir)]))
    for result in contacted.values():
        logger.info(result)
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0


@capsule
def test_negative_restore_nodir(ansible_module):
    """Restore without specified source dir

    :id: c0eeb8fb-e6ca-40c7-8c25-b5a4e3cb7827

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain restore without providing
        directory

    :expectedresults: restore aborted, relevant message is
        returned

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Restore._construct_command(
        ['-y']))
    for result in contacted.values():
        logger.info(result)
        assert result['rc'] == 1
        assert NODIR_MSG in result['stderr']


@capsule
def test_negative_restore_baddir(ansible_module):
    """Restore with invalid source dir

    :id: 1ea94c42-6c33-4fd5-9fe5-c53036023418

    :setup:
        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain restore providing
        invalid directory

    :expectedresults: restore aborted, relevant message is
        returned

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Restore._construct_command([
        '-y', gen_string('alpha')
    ]))
    for result in contacted.values():
        logger.info(result['stderr'])
        assert result['rc'] == 1
        assert BADDIR_MSG in result['stdout']
