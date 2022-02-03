"""
Usage:
    foreman-maintain maintenance-mode [OPTIONS] SUBCOMMAND [ARG] ...

Parameters:
    SUBCOMMAND                    subcommand
    [ARG] ...                     subcommand arguments

Subcommands:
    start                         Start maintenance-mode
    stop                          Stop maintenance-mode
    status                        Get maintenance-mode status
    is-enabled                    Get maintenance-mode status code

Options:
    -h, --help                    print help
"""
from testfm.base import Base


class MaintenanceMode(Base):
    """Manipulates Satellite-maintain's maintenance-mode command"""

    command_base = "maintenance-mode"

    @classmethod
    def start(cls, options=None):
        """foreman-maintain maintenance-mode start [OPTIONS]"""
        cls.command_sub = "start"

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def stop(cls, options=None):
        """foreman-maintain maintenance-mode stop [OPTIONS]"""
        cls.command_sub = "stop"

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def status(cls, options=None):
        """foreman-maintain maintenance-mode status [OPTIONS]"""
        cls.command_sub = "status"

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def is_enabled(cls, options=None):
        """foreman-maintain maintenance-mode is-enabled [OPTIONS]"""
        cls.command_sub = "is-enabled"

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result
