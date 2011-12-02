# -*- coding: utf-8 -*-

from btfly.task import BaseTask

class CSV(BaseTask):
    def execute(self, context):
        self.log.debug("CSV task execute()")
        hosts_manager = context.hosts_manager
        values = []
        if context.field == 'name':
            values = hosts_manager.names(
                roles=context.options.get('roles'),
                statuses=context.options.get('statuses')
            )
        elif context.field == 'ip':
            values = hosts_manager.ip_addresses(
                roles=context.options.get('roles'),
                statuses=context.options.get('statuses')
            )
        else:
            raise ValueError("Invalid context.field: '%s'" % (context.field))

        self.log.debug("values = %s" % values)
        return ','.join(values)

class ShEnv(BaseTask):
    def add_options(self, parser):
        parser.add_argument(
            '-E', '--env-name', default='BTFLY_HOSTS',
            help='Specify an environment name to output.'
        )

    def execute(self, context):
        hosts_manager = context.hosts_manager
        env_name = context.options.get('env_name') or 'BTFLY_HOSTS'
        if context.field == 'name':
            values = hosts_manager.names(
                roles=context.options.get('roles'),
                statuses=context.options.get('statuses')
            )
        elif context.field == 'ip':
            values = hosts_manager.ip_addresses(
                roles=context.options.get('roles'),
                statuses=context.options.get('statuses')
            )
        else:
            raise ValueError("Invalid context.field: '%s'" % (context.field))

        self.log.debug("values = %s" % values)
        return "%s=(%s)" % (env_name, ' '.join(values))
# eval `BTFLY_ENV=production btfly --roles web --field ip env`
# --> btfly_hosts=(127.0.0.1 192.168.1.2)
# % btfly-foreach; do ssh $i uptime; done


class Hosts(BaseTask):
    def execute(self, context):
        return ''

def register(manager):
    """
    This function is called when this plugin is loaded.
    """
    manager.register_task(CSV('csv', 'output as CSV.'))
    manager.register_task(ShEnv('sh_env', 'output as sh environment.'))
    manager.register_task(Hosts('hosts', 'output as /etc/hosts format.'))
