# -*- encoding: utf-8 -*-
"""
Usage:
    foreman-maintain health [OPTIONS] SUBCOMMAND [ARG] ...

Parameters:
    SUBCOMMAND                    subcommand
    [ARG] ...                     subcommand arguments

Subcommands:
    list                          List the checks based on criteria
    list-tags                     List the tags to use for filtering checks
    check                         Run the health checks against the system

Options:
    -h, --help                    print help
"""

from testfm.base import Base


class Health(Base):
    """Manipulates Foreman-maintain's health command"""

    command_base = 'health'
