# -*- coding: utf-8 -*-

from btfly.task import BaseTask

class CSV(BaseTask):
    def add_arguments(self, subparsers):
        p = subparsers.add_parser('csv', help="csv help")
        return p

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
    def add_arguments(self, subparsers):
        p = subparsers.add_parser('sh_env', help="sh_env help")
        return p

    def execute(self, context):
        return ''

def register(manager):
    manager.register_task(CSV('csv', 'output as CSV.'))
    manager.register_task(ShEnv('sh_env', 'output as sh environment.'))
