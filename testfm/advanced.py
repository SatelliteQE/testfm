# -*- encoding: utf-8 -*-
"""
Usage:
    foreman-maintain advanced procedure run [OPTIONS] SUBCOMMAND [ARG] ...

Parameters:
    SUBCOMMAND                    subcommand
    [ARG] ...                     subcommand arguments

Subcommands:
    foreman-tasks-delete          Delete tasks
    foreman-tasks-fetch-tasks-status Fetch tasks status and wait till they
                                  finish
    foreman-tasks-resume          Resume paused tasks
    foreman-tasks-ui-investigate  Investigate the tasks via UI
    hammer-setup                  Setup hammer
    installer-upgrade             Procedures::Installer::Upgrade
    katello-service-restart       katello-service restart
    katello-service-start         katello-service start
    katello-service-stop          katello-service stop
    maintenance-mode-disable      Turn off maintenance mode
    maintenance-mode-enable       Turn on maintenance mode
    packages-install              Procedures::Packages::Install
    packages-update               Procedures::Packages::Update
    repositories-setup            Setup repositories
    sync-plans-disable            disable active sync plans
    sync-plans-enable             re-enable sync plans

Options:
    -h, --help                    print help
"""

from testfm.base import Base


class Advanced(Base):
    """Manipulates Foreman-maintain's advanced procedure run command"""

    command_base = 'advanced procedure run'

    @classmethod
    def run_service_restart(cls, options=None):
        """Build foreman-maintain advanced procedure run
         service-restart"""

        cls.command_sub = 'service-restart'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def run_katello_service_stop(cls, options=None):
        """Build foreman-maintain advanced procedure run
         service-stop"""

        cls.command_sub = 'service-stop'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def run_service_start(cls, options=None):
        """Build foreman-maintain advanced procedure run
         service-start"""

        cls.command_sub = 'service-start'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def run_packages_update(cls, options=None):
        """Build foreman-maintain advanced procedure run
         packages-update"""

        cls.command_sub = 'packages-update'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def run_disable_maintenance_mode(cls, options=None):
        """Build foreman-maintain advanced procedure run
         maintenance-mode-disable"""

        cls.command_sub = 'maintenance-mode-disable'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def run_enable_maintenance_mode(cls, options=None):
        """Build foreman-maintain advanced procedure run
         maintenance-mode-enable"""

        cls.command_sub = 'maintenance-mode-enable'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def run_foreman_tasks_delete(cls, options=None):
        """Build foreman-maintain advanced procedure run
         foreman-tasks-delete"""

        cls.command_sub = 'foreman-tasks-delete'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def run_foreman_tasks_resume(cls, options=None):
        """Build foreman-maintain advanced procedure run
         foreman-tasks-resume"""

        cls.command_sub = 'foreman-tasks-resume'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def run_sync_plans_enable(cls, options=None):
        """Build foreman-maintain advanced procedure run
         sync-plans-enable"""

        cls.command_sub = 'sync-plans-enable'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def run_sync_plans_disable(cls, options=None):
        """Build foreman-maintain advanced procedure run
         sync-plans-disable"""

        cls.command_sub = 'sync-plans-disable'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def run_foreman_tasks_ui_investigate(cls, options=None):
        """Build foreman-maintain advanced procedure run
         foreman-tasks-ui-investigate"""

        cls.command_sub = 'foreman-tasks-ui-investigate'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def run_hammer_setup(cls, options=None):
        """Build foreman-maintain advanced procedure run
         hammer-setup"""

        cls.command_sub = 'hammer-setup'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result
