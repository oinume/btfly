# -*- coding: utf-8 -*-

from btfly.task import BaseTask

class CSV(BaseTask):
    def execute(self, context):
        self.log.debug("CSV task execute()")
        hosts_manager = context.hosts_manager
        values = self.get_values(context)
        return ','.join(values)

class ShEnv(BaseTask):
    def add_options(self, parser):
        parser.add_argument(
            '-E', '--env-name', default='BTFLY_HOSTS',
            help='Specify an environment name to output.'
        )

    def execute(self, context):
        values = self.get_values(context)
        env_name = context.options.get('env_name') or 'BTFLY_HOSTS'
        return "%s=(%s)" % (env_name, ' '.join(values))
# eval `BTFLY_ENV=production btfly --roles web --field ip env`
# --> BTFLY_HOSTS=(127.0.0.1 192.168.1.2)
# % btfly_foreach; do ssh $i uptime; done

class Hosts(BaseTask):
    def execute(self, context):
        hosts_manager = context.hosts_manager
        hosts = context.hosts_manager.hosts(
            roles=context.options.get('roles'),
            statuses=context.options.get('statuses'),
        )
        
        s = "# Generated with btfly\n"
        for host in hosts:
            name = host.keys()[0] # TODO: host must be object
            attributes = host.values()[0]
            s += "%s %s\n" % (attributes.get('ip'), name)
        return s.rstrip()

def register(manager):
    """
    This function is called when this plugin is loaded.
    """
    manager.register_task(CSV('csv', 'output as CSV.'))
    manager.register_task(ShEnv('sh_env', 'output as sh environment.'))
    manager.register_task(Hosts('hosts', 'output as /etc/hosts format.'))
