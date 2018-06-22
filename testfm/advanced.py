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
