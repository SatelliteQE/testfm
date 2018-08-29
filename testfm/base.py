

class Base(object):
    """
    @param command_base: base command of foreman-maintain.
    Output of recent `foreman-maintain --help`::

        Usage:
            foreman-maintain [OPTIONS] SUBCOMMAND [ARG] ...

        Parameters:
            SUBCOMMAND                    subcommand
            [ARG] ...                     subcommand arguments

        Subcommands:
            health                        Health related commands
            upgrade                       Upgrade related commands
            service                       Control applicable services
            backup                        Backup server
            restore                       Restore a backup
            advanced                      Advanced tools for server maintenance

        Options:
            -h, --help                    print help


    @since: 23.Jun.2018
    """
    command_base = None  # each inherited instance should define this
    command_sub = ''  # specific to instance, like: health, upgrade, etc

    @classmethod
    def _construct_command(cls, options=None):
        """Build a foreman-maintain command based on the options passed"""
        tail = u''
        if isinstance(options, list):
            for val in options:
                if val is None:
                    continue
                else:
                    tail += u' {0}'.format(val)
        else:
            for key, val in options.items():
                if val is None:
                    continue
                if val is True:
                    tail += u' --{0}'.format(key)
                elif val is not False:
                    if isinstance(val, list):
                        val = ','.join(str(el) for el in val)
                    tail += u' --{0}="{1}"'.format(key, val)

        cmd = u'foreman-maintain {0} {1} {2}'.format(
            cls.command_base,
            cls.command_sub,
            tail.strip()
        )
        return cmd

    @classmethod
    def check(cls, options=None):
        """Build foreman-maintain health check"""
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
        """Build foreman-maintain health list"""
        cls.command_sub = 'list-tags'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def list_versions(cls, options=None):
        """Build foreman-maintain upgrade list-versions"""
        cls.command_sub = 'list-versions'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

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
         katello-service-restart"""

        cls.command_sub = 'hammer-setup'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def run_online_backup(cls, options=None):
        """Build foreman-maintain backup online"""

        cls.command_sub = 'online'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def run_offline_backup(cls, options=None):
        """Build foreman-maintain backup offline"""

        cls.command_sub = 'offline'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def service_restart(cls, options=None):
        """Build foreman-maintain service"""

        cls.command_sub = 'restart'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result

    @classmethod
    def service_start(cls, options=None):
        """Build foreman-maintain service start"""

        cls.command_sub = 'start'

        if options is None:
            options = {}

        result = cls._construct_command(options)

        return result
