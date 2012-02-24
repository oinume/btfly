# -*- coding: utf-8 -*-
from btfly.task import BaseTask

class CSV(BaseTask):
    def execute(self, context):
        values = self.get_values(context)
        return ','.join(values)

class Env(BaseTask):
    def add_options(self, parser):
        parser.add_argument(
            '-E', '--env-name', default='BTFLY_HOSTS',
            help='Specify a name of environment variable to be output.'
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
        hosts = context.hosts_manager.hosts(
            roles=context.options.get('roles'),
            statuses=context.options.get('statuses'),
        )
        
        s = "# Generated with btfly\n" # TODO: line separator compatibility (set in conf.yaml ?)
        for host in hosts:
            s += "%s %s\n" % (host.ip, host.name)
        return s.rstrip()

def register(manager):
    """
    This function is called when this plugin is loaded.
    """
    manager.register_task(CSV('csv', "output as CSV."))
    manager.register_task(Env('env', "output as sh environment."))
    manager.register_task(Hosts('hosts', "output as /etc/hosts format."))
