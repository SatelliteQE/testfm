# -*- encoding: utf-8 -*-
"""
Usage:
    foreman-maintain restore [OPTIONS] BACKUP_DIR

Parameters:
    BACKUP_DIR                    Path to backup directory to restore

Options:
    -y, --assumeyes               Automatically answer yes for all questions
    -w, --whitelist whitelist     Comma-separated list of labels of steps to
                                  be skipped
    -f, --force                   Force steps that would be skipped as they
                                  were already run
    -i, --incremental             Restore an incremental backup
    -h, --help                    print help
"""
from testfm.base import Base


class Restore(Base):
    """Manipulates Foreman-maintain's restore command"""

    command_base = 'restore'
