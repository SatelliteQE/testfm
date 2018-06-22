# -*- encoding: utf-8 -*-
"""
Usage:
    foreman-maintain upgrade [OPTIONS] SUBCOMMAND [ARG] ...

Parameters:
    SUBCOMMAND                    subcommand
    [ARG] ...                     subcommand arguments

Subcommands:
    list-versions                 List versions this system is upgradable to
    check                         Run pre-upgrade checks before upgrading to
                                  specified version
    run                           Run full upgrade to a specified version

Options:
    -h, --help                    print help
"""

from testfm.base import Base


class Upgrade(Base):
    """Manipulates Foreman-maintain's health command"""

    command_base = 'upgrade'
