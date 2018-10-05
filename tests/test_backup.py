from testfm.backup import Backup
from testfm.decorators import capsule, ansible_host_pattern, run_only_on
from testfm.log import logger
from testfm.service import Service
from fauxfactory import gen_string

BACKUP_DIR = '/tmp/'
NODIR_MSG = "ERROR: parameter 'BACKUP_DIR': no value provided"
NOPREV_MSG = ("ERROR: option '--incremental': Previous backup "
              "directory does not exist")

OFFLINE_CAPS_FILES = [
    'config_files.tar.gz',
    '.config.snar',
    'metadata.yml',
    'mongo_data.tar.gz',
    '.mongo.snar',
]

OFFLINE_SAT_FILES = [
    'pgsql_data.tar.gz',
    '.postgres.snar',
]

OFFLINE_BACKUP_FILES = OFFLINE_CAPS_FILES + OFFLINE_SAT_FILES

ONLINE_CAPS_FILES = [
    'config_files.tar.gz',
    '.config.snar',
    'metadata.yml',
    'mongo_dump',
]

ONLINE_SAT_FILES = [
    'candlepin.dump',
    'foreman.dump',
    'pg_globals.dump',
]

ONLINE_BACKUP_FILES = ONLINE_CAPS_FILES + ONLINE_SAT_FILES

CONTENT_FILES = [
    'pulp_data.tar',
    '.pulp.snar',
]

assert_msg = "All required backup files not found"


@capsule
def test_positive_backup_online(ansible_module):
    """Take online backup of server

    :id: 962d21de-04bc-43fd-9076-cdbfdb9d798e

    :setup:

        1. foreman-maintain should be installed.
    :steps:
        1. Run foreman-maintain backup online /backup_dir/

    :expectedresults: Backup should successful.

    :CaseImportance: Critical
    """
    subdir = "{0}backup-{1}".format(BACKUP_DIR, gen_string('alpha'))
    contacted = ansible_module.command(Backup.run_online_backup([
        '-y',
        subdir
    ]))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0

    # getting created files
    contacted = ansible_module.command('ls {}'.format(subdir))
    timestamped_dir = contacted.values()[0]['stdout_lines'][0]
    contacted = ansible_module.command(
                'ls -a {0}/{1}'.format(subdir, timestamped_dir))
    files_list = contacted.values()[0]['stdout_lines']
    expected_files = ONLINE_BACKUP_FILES

    # capsule-specific file list
    if ansible_host_pattern == 'capsule':
        expected_files = ONLINE_CAPS_FILES
    assert set(files_list).issuperset(
               expected_files + CONTENT_FILES), assert_msg


@capsule
def test_positive_backup_online_skip_pulp_content(ansible_module):
    """Take online backup skipping pulp content of server

    :id: 0a041aed-8578-40d9-8044-6a1db0daba59

    :setup:

        1. foreman-maintain should be installed.
    :steps:
        1. Run foreman-maintain backup online --skip-pulp-content /backup_dir/

    :expectedresults: Backup should successful.

    :CaseImportance: Critical
    """
    subdir = "{0}backup-{1}".format(BACKUP_DIR, gen_string('alpha'))
    contacted = ansible_module.command(Backup.run_online_backup([
        '-y',
        '--skip-pulp-content',
        subdir
    ]))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0

    # getting created files
    contacted = ansible_module.command('ls {}'.format(subdir))
    timestamped_dir = contacted.values()[0]['stdout_lines'][0]
    contacted = ansible_module.command(
                'ls -a {0}/{1}'.format(subdir, timestamped_dir))
    files_list = contacted.values()[0]['stdout_lines']
    expected_files = ONLINE_BACKUP_FILES

    # capsule-specific file list
    if ansible_host_pattern == 'capsule':
        expected_files = ONLINE_CAPS_FILES
    assert set(files_list).issuperset(
               expected_files), assert_msg
    assert CONTENT_FILES not in files_list, "content not skipped"


@capsule
def test_positive_backup_online_preserve_directory(ansible_module):
    """Take online backup of server preserving directory

    :id: 343c79fd-5fd3-45a3-bb75-c807817f2970

    :setup:

        1. foreman-maintain should be installed.
    :steps:
        1. Run foreman-maintain backup online --preserve-directory /backup_dir/

    :expectedresults: Backup should successful.

    :CaseImportance: Critical
    """
    subdir = "{0}backup-{1}".format(BACKUP_DIR, gen_string('alpha'))
    ansible_module.file(
        path="{}".format(subdir),
        state="directory",
        owner="postgres",
    )
    contacted = ansible_module.command(Backup.run_online_backup([
        '-y',
        '--preserve-directory',
        subdir
    ]))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0

    contacted = ansible_module.command(
                'ls -a {0}'.format(subdir))
    files_list = contacted.values()[0]['stdout_lines']
    expected_files = ONLINE_BACKUP_FILES

    # capsule-specific file list
    if ansible_host_pattern == 'capsule':
        expected_files = ONLINE_CAPS_FILES
    assert set(files_list).issuperset(
               expected_files + CONTENT_FILES), assert_msg


@capsule
def test_positive_backup_online_split_pulp_tar(ansible_module):
    """Take online backup of server spliting pulp tar

    :id: f2c7173f-a955-4c0c-a232-60f6161fda81

    :setup:

        1. foreman-maintain should be installed.
    :steps:
        1. Run foreman-maintain backup online  --split-pulp-tar 1M /backup_dir/

    :expectedresults: Backup should successful.

    :CaseImportance: Critical
    """
    subdir = "{0}backup-{1}".format(BACKUP_DIR, gen_string('alpha'))
    contacted = ansible_module.command(Backup.run_online_backup([
        '-y',
        '--split-pulp-tar',
        '1M',
        subdir
    ]))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0

    contacted = ansible_module.command('ls {}'.format(subdir))
    timestamped_dir = contacted.values()[0]['stdout_lines'][0]
    contacted = ansible_module.command(
                'ls -a {0}/{1}'.format(subdir, timestamped_dir))
    files_list = contacted.values()[0]['stdout_lines']
    expected_files = ONLINE_BACKUP_FILES

    # capsule-specific file list
    if ansible_host_pattern == 'capsule':
        expected_files = ONLINE_CAPS_FILES
    assert set(files_list).issuperset(
               expected_files + CONTENT_FILES), assert_msg


@capsule
def test_positive_backup_online_incremental(ansible_module):
    """Take incremental online backup of server

    :id: e4af1804-8479-47c0-9f50-460b6edbe9e0

    :setup:

        1. foreman-maintain should be installed.
        2. Take backup of server.
    :steps:
        1. Run foreman-maintain backup online --incremental
         /previous_backup_dir/ /backup_dir/

    :expectedresults: Backup should successful.

    :CaseImportance: Critical
    """
    subdir = "{0}backup-{1}".format(BACKUP_DIR, gen_string('alpha'))
    dest_dir = "{0}backup-{1}".format(BACKUP_DIR, gen_string('alpha'))
    setup = ansible_module.command(Backup.run_online_backup([
        '-y',
        subdir
    ]))
    for result in setup.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0
    contacted = ansible_module.command('ls {}'.format(subdir))
    source_dir = contacted.values()[0]['stdout_lines'][0]
    contacted = ansible_module.command(Backup.run_online_backup([
        '-y',
        '--incremental',
        '{0}/{1}'.format(subdir, source_dir),
        dest_dir
    ]))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0

    contacted = ansible_module.stat(path=subdir)
    source_size = contacted.values()[0]['stat']['size']
    contacted = ansible_module.stat(path=dest_dir)
    dest_size = contacted.values()[0]['stat']['size']
    assert source_size >= dest_size


@capsule
def test_positive_backup_online_caspule_features(ansible_module):
    """Take online backup of server including capsule features dns, tftp, etc.

    :id: a36f8a53-a233-4bc8-bd0f-c4629e383cb9

    :setup:

        1. foreman-maintain should be installed.
    :steps:
        1. Run foreman-maintain backup online  --features dns,tftp /backup_dir/

    :expectedresults: Backup should successful.

    :CaseImportance: Critical
    """
    subdir = "{0}backup-{1}".format(BACKUP_DIR, gen_string('alpha'))
    contacted = ansible_module.command(Backup.run_online_backup([
        '-y',
        '--features',
        'dns,tftp,openscap,dhcp',
        subdir
    ]))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0

    # getting created files
    contacted = ansible_module.command('ls {}'.format(subdir))
    timestamped_dir = contacted.values()[0]['stdout_lines'][0]
    contacted = ansible_module.command(
                'ls -a {0}/{1}'.format(subdir, timestamped_dir))
    files_list = contacted.values()[0]['stdout_lines']
    expected_files = ONLINE_BACKUP_FILES

    # capsule-specific file list
    if ansible_host_pattern == 'capsule':
        expected_files = ONLINE_CAPS_FILES
    assert set(files_list).issuperset(
               expected_files + CONTENT_FILES), assert_msg


@capsule
def test_positive_backup_online_all(ansible_module):
    """Take online backup of server providing all options

    :id: 86a93e4f-61e3-4206-ae28-ce01136c5518

    :setup:

        1. foreman-maintain should be installed.
        2. Take backup of server.
    :steps:
        1. Run foreman-maintain backup online -y -f -s -p -t 10M -i
        /previous_backup/ --features dns,tftp /backup_dir/

    :expectedresults: Backup should successful.

    :CaseImportance: Critical
    """
    setup = ansible_module.command(Backup.run_online_backup([
        '-y',
        '/mnt/'
    ]))
    for result in setup.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0
    contacted = ansible_module.command(Backup.run_online_backup([
        '-y -f -s -p -t 10M -i',
        '/mnt/',
        '--features',
        'dns,tftp,openscap,dhcp',
        BACKUP_DIR
    ]))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0


@capsule
def test_positive_backup_offline(ansible_module):
    """Take offline backup of server

    :id: 2bbd15de-59f4-4ea0-8016-4cc951c6e4b9

    :setup:

        1. foreman-maintain should be installed.
    :steps:
        1. Run foreman-maintain backup offline /backup_dir/

    :expectedresults: Backup should successful.

    :CaseImportance: Critical
    """
    subdir = "{0}backup-{1}".format(BACKUP_DIR, gen_string('alpha'))
    contacted = ansible_module.command(Backup.run_offline_backup([
        '-y',
        subdir
    ]))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0

    # getting created files
    contacted = ansible_module.command('ls {}'.format(subdir))
    timestamped_dir = contacted.values()[0]['stdout_lines'][0]
    contacted = ansible_module.command(
                'ls -a {0}/{1}'.format(subdir, timestamped_dir))
    files_list = contacted.values()[0]['stdout_lines']
    expected_files = OFFLINE_BACKUP_FILES

    # capsule-specific file list
    if ansible_host_pattern == 'capsule':
        expected_files = OFFLINE_CAPS_FILES
    assert set(files_list).issuperset(
               expected_files + CONTENT_FILES), assert_msg


@capsule
def test_positive_backup_offline_skip_pulp_content(ansible_module):
    """Take offline backup of server skipping pulp content

    :id: 8c31620f-a1f1-4422-8609-3fd8e05d6056

    :setup:

        1. foreman-maintain should be installed.
    :steps:
        1. Run foreman-maintain backup offline --skip-pulp-content /backup_dir/

    :expectedresults: Backup should successful.

    :CaseImportance: Critical
    """
    subdir = "{0}backup-{1}".format(BACKUP_DIR, gen_string('alpha'))
    contacted = ansible_module.command(Backup.run_offline_backup([
        '-y',
        '--skip-pulp-content',
        subdir
    ]))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0

    # getting created files
    contacted = ansible_module.command('ls {}'.format(subdir))
    timestamped_dir = contacted.values()[0]['stdout_lines'][0]
    contacted = ansible_module.command(
                'ls -a {0}/{1}'.format(subdir, timestamped_dir))
    files_list = contacted.values()[0]['stdout_lines']
    expected_files = OFFLINE_BACKUP_FILES

    # capsule-specific file list
    if ansible_host_pattern == 'capsule':
        expected_files = OFFLINE_CAPS_FILES
    assert set(files_list).issuperset(
               expected_files), assert_msg
    assert CONTENT_FILES not in files_list, "content not skipped"


@capsule
def test_positive_backup_offline_preserve_directory(ansible_module):
    """Take offline backup of server preserving directory

    :id: 99fc9319-d495-481a-b345-5f6ca12c4225

    :setup:

        1. foreman-maintain should be installed.
    :steps:
        1. Run foreman-maintain backup offline --preserve-directory
         /backup_dir/

    :expectedresults: Backup should successful.

    :CaseImportance: Critical
    """
    subdir = "{0}backup-{1}".format(BACKUP_DIR, gen_string('alpha'))
    ansible_module.file(
        path="{}".format(subdir),
        state="directory",
        owner="postgres",
    )
    contacted = ansible_module.command(Backup.run_offline_backup([
        '-y',
        '--preserve-directory',
        subdir
    ]))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0

    contacted = ansible_module.command(
                'ls -a {0}'.format(subdir))
    files_list = contacted.values()[0]['stdout_lines']
    expected_files = OFFLINE_BACKUP_FILES

    # capsule-specific file list
    if ansible_host_pattern == 'capsule':
        expected_files = OFFLINE_CAPS_FILES
    assert set(files_list).issuperset(
               expected_files + CONTENT_FILES), assert_msg


@capsule
def test_positive_backup_offline_split_pulp_tar(ansible_module):
    """Take offline backup of server splitting pulp tar

    :id: bdd19e11-89b6-471c-af65-359046686473

    :setup:

        1. foreman-maintain should be installed.
    :steps:
        1. Run foreman-maintain backup offline --split-pulp-tar 10M
         /backup_dir/

    :expectedresults: Backup should successful.

    :CaseImportance: Critical
    """
    subdir = "{0}backup-{1}".format(BACKUP_DIR, gen_string('alpha'))
    contacted = ansible_module.command(Backup.run_offline_backup([
        '-y',
        '--split-pulp-tar',
        '10M',
        subdir
    ]))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0

    contacted = ansible_module.command('ls {}'.format(subdir))
    timestamped_dir = contacted.values()[0]['stdout_lines'][0]
    contacted = ansible_module.command(
                'ls -a {0}/{1}'.format(subdir, timestamped_dir))
    files_list = contacted.values()[0]['stdout_lines']
    expected_files = OFFLINE_BACKUP_FILES

    # capsule-specific file list
    if ansible_host_pattern == 'capsule':
        expected_files = OFFLINE_CAPS_FILES
    assert set(files_list).issuperset(
               expected_files + CONTENT_FILES), assert_msg


@capsule
def test_positive_backup_offline_incremental(ansible_module):
    """Take offline incremental backup of server

    :id: 27df1544-0bc6-4922-a45c-3c7f3b805a1d

    :setup:

        1. foreman-maintain should be installed.
        2. Take offline backup of server
    :steps:
        1. Run foreman-maintain backup offline --incremental /previous_backup/
         /backup_dir/

    :expectedresults: Backup should successful.

    :CaseImportance: Critical
    """
    subdir = "{0}backup-{1}".format(BACKUP_DIR, gen_string('alpha'))
    dest_dir = "{0}backup-{1}".format(BACKUP_DIR, gen_string('alpha'))
    setup = ansible_module.command(Backup.run_offline_backup([
        '-y',
        subdir
    ]))
    for result in setup.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0
    contacted = ansible_module.command('ls {}'.format(subdir))
    source_dir = contacted.values()[0]['stdout_lines'][0]
    contacted = ansible_module.command(Backup.run_offline_backup([
        '-y',
        '--incremental',
        '{0}/{1}'.format(subdir, source_dir),
        dest_dir
    ]))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0

    contacted = ansible_module.stat(path=subdir)
    source_size = contacted.values()[0]['stat']['size']
    contacted = ansible_module.stat(path=dest_dir)
    dest_size = contacted.values()[0]['stat']['size']
    assert source_size >= dest_size


@capsule
def test_positive_backup_offline_capsule_features(ansible_module):
    """Take offline backup of server including capsule features dns, tftp, etc.

    :id: 31f93423-affb-4f41-a666-993aa0a56e12

    :setup:

        1. foreman-maintain should be installed.
    :steps:
        1. Run foreman-maintain backup offline --features dns,tftp
         /backup_dir/

    :expectedresults: Backup should successful.

    :CaseImportance: Critical
    """
    subdir = "{0}backup-{1}".format(BACKUP_DIR, gen_string('alpha'))
    contacted = ansible_module.command(Backup.run_offline_backup([
        '-y',
        '--features',
        'dns,tftp,dhcp,openscap',
        subdir
    ]))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0

    contacted = ansible_module.command('ls {}'.format(subdir))
    timestamped_dir = contacted.values()[0]['stdout_lines'][0]
    contacted = ansible_module.command(
                'ls -a {0}/{1}'.format(subdir, timestamped_dir))
    files_list = contacted.values()[0]['stdout_lines']
    expected_files = OFFLINE_BACKUP_FILES

    # capsule-specific file list
    if ansible_host_pattern == 'capsule':
        expected_files = OFFLINE_CAPS_FILES
    assert set(files_list).issuperset(
               expected_files + CONTENT_FILES), assert_msg


@capsule
def test_positive_backup_offline_logical(ansible_module):
    """Take offline backup of server include-db-dumps

    :id: 26c9b3cb-f96a-44bb-828b-69865099af39

    :setup:

        1. foreman-maintain should be installed.
    :steps:
        1. Run foreman-maintain backup offline --include-db-dumps /backup_dir/

    :expectedresults: Backup should successful.

    :CaseImportance: Critical
    """
    subdir = "{0}backup-{1}".format(BACKUP_DIR, gen_string('alpha'))
    contacted = ansible_module.command(Backup.run_offline_backup([
        '-y',
        '--include-db-dumps',
        subdir
    ]))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0

    contacted = ansible_module.command('ls {}'.format(subdir))
    timestamped_dir = contacted.values()[0]['stdout_lines'][0]
    contacted = ansible_module.command(
                'ls -a {0}/{1}'.format(subdir, timestamped_dir))
    files_list = contacted.values()[0]['stdout_lines']
    expected_files = OFFLINE_BACKUP_FILES + ONLINE_BACKUP_FILES

    # capsule-specific file list
    if ansible_host_pattern == 'capsule':
        expected_files = OFFLINE_CAPS_FILES + ONLINE_CAPS_FILES
    assert set(files_list).issuperset(
               expected_files + CONTENT_FILES), assert_msg


@capsule
def test_positive_backup_offline_all(ansible_module):
    """Take offline backup of server providing all options

    :id: 2065e58a-4710-4315-af9e-e7049fabf323

    :setup:

        1. foreman-maintain should be installed.
        2. Take offline backup of server.
    :steps:
        1. Run foreman-maintain backup offline -y -f -s -p -t 10M -i
         /prevoius_backup/ --features dns,tfp --include-db-dumps /backup_dir/

    :expectedresults: Backup should successful.

    :CaseImportance: Critical
    """
    setup = ansible_module.command(Backup.run_offline_backup([
        '-y',
        '/mnt/'
    ]))
    for result in setup.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0
    contacted = ansible_module.command(Backup.run_offline_backup([
        '-y -f -s -p -t 10M -i',
        '/mnt/',
        '--features dns,tfp,dhcp,openscap',
        '--include-db-dumps',
        BACKUP_DIR
    ]))
    for result in contacted.values():
        logger.info(result['stdout'])
        assert "FAIL" not in result['stdout']
        assert result['rc'] == 0


@capsule
def test_negative_backup_online_nodir(ansible_module):
    """Take online backup of server with no destination

    :id: 298176a7-ba1d-4fcd-9718-d62c47900bb5

    :setup:

        1. foreman-maintain should be installed.
    :steps:
        1. Run foreman-maintain backup online without providing
        directory

    :expectedresults: backup aborted, relevant message is
        returned

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Backup.run_online_backup([
        '-y',
    ]))
    for result in contacted.values():
        logger.info(result['stderr'])
        assert result['rc'] == 1
        assert NODIR_MSG in result['stderr']


@capsule
def test_negative_backup_offline_nodir(ansible_module):
    """Take offline backup of server with no destination

    :id: 9377ebc6-663b-47d4-92e2-744398dba376

    :setup:

        1. foreman-maintain should be installed.
    :steps:
        1. Run foreman-maintain backup offline without providing
        directory

    :expectedresults: backup aborted, relevant message is
        returned

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Backup.run_offline_backup([
        '-y',
    ]))
    for result in contacted.values():
        logger.info(result['stderr'])
        assert result['rc'] == 1
        assert NODIR_MSG in result['stderr']


@capsule
def test_negative_backup_online_incremental_nodir(ansible_module):
    """Take online backup of server with no destination

    :id: cfb68cdf-9d27-4a38-bc16-900fc9488ac6

    :setup:

        1. foreman-maintain should be installed.
    :steps:
        1. Run foreman-maintain backup offline with nonexistent
        directory

    :expectedresults: backup aborted, relevant message is
        returned

    :CaseImportance: Critical
    """
    contacted = ansible_module.command(Backup.run_online_backup([
        '-y',
        '--incremental',
        gen_string('alpha'),
    ]))
    for result in contacted.values():
        logger.info(result['stderr'])
        assert result['rc'] == 1
        assert NOPREV_MSG in result['stderr']


@run_only_on('sat64')
def test_positive_backup_stopped_dynflowd(ansible_module):
    """Take online backup of server when dynflowd is not running

    :id: 321b5f16-337c-4370-87b6-cfe1c78c9139

    :setup:

        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain service stop --only dynflowd
        2. Run foreman-maintain backup online /backup_dir/

    :expectedresults: Backup should successful.

    :CaseImportance: Critical
    """
    subdir = "{0}backup-{1}".format(BACKUP_DIR, gen_string('alpha'))
    try:
        setup = ansible_module.command(Service.service_stop({
            u'only': 'dynflowd'
        }))
        for result in setup.values():
            logger.info(result)
            assert result['rc'] == 0
        contacted = ansible_module.command(Backup.run_online_backup([
            '-y',
            subdir
        ]))
        for result in contacted.values():
            logger.info(result['stdout'])
            assert "FAIL" not in result['stdout']
            assert result['rc'] == 0

        # getting created files
        contacted = ansible_module.command('ls {}'.format(subdir))
        timestamped_dir = contacted.values()[0]['stdout_lines'][0]
        contacted = ansible_module.command(
            'ls -a {0}/{1}'.format(subdir, timestamped_dir))
        files_list = contacted.values()[0]['stdout_lines']
        expected_files = ONLINE_BACKUP_FILES

        # capsule-specific file list
        if ansible_host_pattern == 'capsule':
            expected_files = ONLINE_CAPS_FILES
        assert set(files_list).issuperset(
            expected_files + CONTENT_FILES), assert_msg
    finally:
        teardown = ansible_module.command(Service.service_start())
        for result in teardown.values():
            assert result['rc'] == 0


@run_only_on('sat63')
def test_positive_backup_stopped_foreman_tasks(ansible_module):
    """Take online backup of server when foreman-tasks is not running

    :id: 3def9d00-f9be-4817-adf0-acd7cf68460b

    :setup:

        1. foreman-maintain should be installed.

    :steps:
        1. Run foreman-maintain service stop --only foreman-tasks
        2. Run foreman-maintain backup online /backup_dir/

    :expectedresults: Backup should successful.

    :CaseImportance: Critical
    """
    subdir = "{0}backup-{1}".format(BACKUP_DIR, gen_string('alpha'))
    try:
        setup = ansible_module.command(Service.service_stop({
            u'only': 'foreman-tasks'
        }))
        for result in setup.values():
            logger.info(result)
            assert result['rc'] == 0
        contacted = ansible_module.command(Backup.run_online_backup([
            '-y',
            subdir
        ]))
        for result in contacted.values():
            logger.info(result['stdout'])
            assert "FAIL" not in result['stdout']
            assert result['rc'] == 0
    finally:
        teardown = ansible_module.command(Service.service_start())
        for result in teardown.values():
            assert result['rc'] == 0
