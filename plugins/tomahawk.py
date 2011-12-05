# -*- coding: utf-8 -*-
from btfly.task import BaseTask

class TomahawkHosts(BaseTask):
    def execute(self, context):
        values = self.get_values(context)
        return ','.join(values)

class TomahawkHostsFile(BaseTask):
    def execute(self, context):
        s = ''
        for value in self.get_values(context):
            s += value + '\n'
        return s.rstrip()

def register(manager):
    manager.register_task(TomahawkHosts('tomahawk_hosts', "output as tomahawk hosts. (comma separated)"))
    manager.register_task(TomahawkHostsFile('tomahawk_hosts_file', "output as tomahawk hosts file."))

