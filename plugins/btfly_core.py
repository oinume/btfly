# -*- coding: utf-8 -*-

from btfly.subcommand import Subcommand

class CSV(Subcommand):
    def execute(self, context):
        self.log.info("CSV subcommand execute()")
        hosts_conf = context.hosts_conf
        hosts = hosts_conf.get('hosts')
        values = []
        # HostsConf.names()
        # TODO: HostsConf.ips(roles=[ 'hoge' ])
        # HostsConf.names(statuses=[ 'active' ])
        # HostsConf.values
        # バグ取り
        # hosts.yaml作成
        # ディプロイスクリプト作成
        # maven repo登録スクリプト作成
        # Flashタグ切りスクリプト作成
        if context.field == 'name':
            for host in hosts:
                values.append(host.keys()[0])
        elif context.field == 'ip':
            for host in hosts:
                values.append(hosts.values()[0]['ip'])
        self.log.debug("values = %s" % values)
        return ','.join(values)

class ShEnv(Subcommand):
    def execute(self, context):
        return ''

def register(manager):
    manager.register_subcommand(CSV('csv', 'output as CSV.'))
    manager.register_subcommand(ShEnv('sh_env', 'output as sh environment.'))
