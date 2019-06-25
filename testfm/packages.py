# -*- encoding: utf-8 -*-
"""
Usage:
    foreman-maintain packages [OPTIONS] SUBCOMMAND [ARG] ...

Parameters:
    SUBCOMMAND                    subcommand
    [ARG] ...                     subcommand arguments

Subcommands:
    lock                          Prevent Foreman-related packages from automatic update

    unlock                        Enable Foreman-related packages for automatic update

    status                        Check if Foreman-related packages are protected against update

    is-locked                     Check if update of Foreman-related packages is allowed

Options:
    -h, --help                    print help
"""
from testfm.base import Base


class Packages(Base):
    """Manipulates Foreman-maintain's packages command"""

    command_base = 'packages'

    @classmethod
    def lock(cls, options=None):
        """
    Usage:
        foreman-maintain packages lock [OPTIONS]

    Options:
        -y, --assumeyes               Automatically answer yes for all questions

        -w, --whitelist whitelist     Comma-separated list of labels of steps to be skipped

        -f, --force                   Force steps that would be skipped as they were already run

        -h, --help                    print help
        """
        cls.command_sub = 'lock'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def unlock(cls, options=None):
        """
    Usage:
        foreman-maintain packages unlock [OPTIONS]

    Options:
        -y, --assumeyes               Automatically answer yes for all questions

        -w, --whitelist whitelist     Comma-separated list of labels of steps to be skipped

        -f, --force                   Force steps that would be skipped as they were already run

        -h, --help                    print help
        """
        cls.command_sub = 'unlock'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def status(cls, options=None):
        """
    Usage:
        foreman-maintain packages status [OPTIONS]

    Options:
        -y, --assumeyes               Automatically answer yes for all questions

        -w, --whitelist whitelist     Comma-separated list of labels of steps to be skipped

        -f, --force                   Force steps that would be skipped as they were already run

        -h, --help                    print help
        """
        cls.command_sub = 'status'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def is_locked(cls, options=None):
        """
    Usage:
        foreman-maintain packages is-locked [OPTIONS]

    Options:
        -y, --assumeyes               Automatically answer yes for all questions

        -w, --whitelist whitelist     Comma-separated list of labels of steps to be skipped

        -f, --force                   Force steps that would be skipped as they were already run

        -h, --help                    print help
        """
        cls.command_sub = 'is-locked'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result
