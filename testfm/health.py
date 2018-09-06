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

    @classmethod
    def check(cls, options=None):
        """Build foreman-maintain health check
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
        cls.command_sub = 'check'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def list(cls, options=None):
        """Build foreman-maintain health list"""
        cls.command_sub = 'list'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def list_tags(cls, options=None):
        """Build foreman-maintain health list-tags"""
        cls.command_sub = 'list-tags'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result
