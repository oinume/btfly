# -*- coding: utf-8 -*-

from btfly.subcommand import Subcommand

class CSV(Subcommand):
    def execute(self):
        # TODO: decorator
        self.log.info("CSV subcommand execute()")

class ShEnv(Subcommand):
    pass

def register(manager):
    manager.register_subcommand(CSV('csv', 'output as CSV.'))
    manager.register_subcommand(ShEnv('sh_env', 'output as sh environment.'))
