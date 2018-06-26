# -*- encoding: utf-8 -*-
"""
Usage:
    foreman-maintain service [OPTIONS] SUBCOMMAND [ARG] ...

Parameters:
    SUBCOMMAND                    subcommand
    [ARG] ...                     subcommand arguments

Subcommands:
    start                         Start applicable services
    stop                          Stop applicable services
    restart                       Restart applicable services
    status                        Get statuses of applicable services
    list                          List applicable services
    enable                        Enable applicable services
    disable                       Disable applicable services

Options:
    -h, --help                    print help
"""

from testfm.base import Base


class Service(Base):
    """Manipulates Foreman-maintain's service command"""

    command_base = 'service'
