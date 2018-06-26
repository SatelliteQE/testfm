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
