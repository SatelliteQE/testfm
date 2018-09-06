# -*- encoding: utf-8 -*-
"""
Usage:
    foreman-maintain backup [OPTIONS] SUBCOMMAND [ARG] ...

Parameters:
    SUBCOMMAND                    subcommand
    [ARG] ...                     subcommand arguments

Subcommands:
    online                        Keep services online during backup
    offline                       Shut down services to preserve consistent
                                  backup
    snapshot                      Use snapshots of the databases to create
                                  backup

Options:
    -h, --help                    print help
"""

from testfm.base import Base


class Backup(Base):
    """Manipulates Foreman-maintain's backup command"""

    command_base = 'backup'

    @classmethod
    def run_online_backup(cls, options=None):
        """Build foreman-maintain backup online"""

        cls.command_sub = 'online'

        if options is None:
            options = {}

        result = cls._construct_command(options)
        return result

    @classmethod
    def run_offline_backup(cls, options=None):
        """Build foreman-maintain backup offline"""

        cls.command_sub = 'offline'

        if options is None:
            options = {}

        result = cls._construct_command(options)
        return result

    @classmethod
    def run_snapshot_backup(cls, options=None):
        """Build foreman-maintain backup snapshot"""

        cls.command_sub = 'snapshot'

        if options is None:
            options = {}

        result = cls._construct_command(options)
        return result
