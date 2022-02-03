"""
Usage:
    satellite-maintain content [OPTIONS] SUBCOMMAND [ARG] ...

Parameters:
    SUBCOMMAND                    subcommand
    [ARG] ...                     subcommand arguments

Subcommands:
    prepare                       Prepare content for Pulp 3
    prepare-abort                 Abort all running Pulp 2 to Pulp 3 migration tasks
    migration-stats               Retrieve Pulp 2 to Pulp 3 migration statistics
    migration-reset               Reset the Pulp 2 to Pulp 3 migration data (pre-switchover)
    remove-pulp2                  Remove pulp2 and mongodb packages and data

Options:
    -h, --help                    print help
"""
from testfm.base import Base


class Content(Base):
    """Manipulates Satellite-maintain's content command"""

    command_base = "content"

    @classmethod
    def prepare(cls, options=None):
        """Build foreman-maintain content prepare"""

        cls.command_sub = "prepare"

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def prepare_abort(cls, options=None):
        """Build foreman-maintain content prepare-abort"""

        cls.command_sub = "prepare-abort"

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def migration_stats(cls, options=None):
        """Build foreman-maintain content migration-stats"""

        cls.command_sub = "migration-stats"

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def migration_reset(cls, options=None):
        """Build foreman-maintain content migration-reset"""

        cls.command_sub = "migration-reset"

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def remove_pulp2(cls, options=None):
        """Build foreman-maintain content remove-pulp2"""

        cls.command_sub = "remove-pulp2"

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result
