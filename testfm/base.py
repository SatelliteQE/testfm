

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
