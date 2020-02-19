# -*- encoding: utf-8 -*-
"""
Usage:
    foreman-maintain advanced procedure by-tag [OPTIONS] SUBCOMMAND [ARG] ...

Parameters:
    SUBCOMMAND                    subcommand
    [ARG] ...                     subcommand arguments

Subcommands:
    post-migrations               Run procedures tagged #post_migrations:
                                  maintenance_mode_disable, sync_plans_enable
    pre-migrations                Run procedures tagged #pre_migrations:
                                  maintenance_mode_enable, sync_plans_disable
    restore                       Run procedures tagged #restore:
                                  restore_confirmation

Options:
    -h, --help                    print help
"""
from testfm.base import Base


class AdvancedByTag(Base):
    """Manipulates Foreman-maintain's advanced procedure by-tag command"""

    command_base = "advanced procedure by-tag"

    @classmethod
    def post_migrations(cls, options=None):
        """Build foreman-maintain advanced procedure by-tag
         post-migrations"""

        cls.command_sub = "post-migrations"

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def pre_migrations(cls, options=None):
        """Build foreman-maintain advanced procedure by-tag
         pre-migrations"""

        cls.command_sub = "pre-migrations"

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def restore(cls, options=None):
        """Build foreman-maintain advanced procedure by-tag
         backup"""

        cls.command_sub = "restore"

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result
