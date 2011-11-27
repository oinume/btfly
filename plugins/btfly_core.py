# -*- coding: utf-8 -*-

from btfly.task import BaseTask

class CSV(BaseTask):
    def execute(self, context):
        self.log.debug("CSV task execute()")
        hosts_conf = context.hosts_conf
        # TODO: context.hosts_managerにする
        hosts = hosts_conf.get('hosts')
        values = []
        if context.field == 'name':
            for host in hosts:
                values.append(host.keys()[0])
        elif context.field == 'ip':
            for host in hosts:
                values.append(hosts.values()[0]['ip'])
        self.log.debug("values = %s" % values)
        return ','.join(values)

class ShEnv(BaseTask):
    def execute(self, context):
        return ''

def register(manager):
    manager.register_task(CSV('csv', 'output as CSV.'))
    manager.register_task(ShEnv('sh_env', 'output as sh environment.'))
