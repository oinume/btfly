# -*- coding: utf-8 -*-

from btfly.subcommand import Subcommand

class CSVSubcommand(Subcommand):
    pass

class ShEnvSubcommand(Subcommand):
    pass

def define_subcommands():
    return [
        { 'name': 'csv', 'class': CSVSubcommand, 'description': 'output as CSV format.' },
        { 'name': 'sh_env', 'class': ShEnvSubcommand, 'description': 'output as sh environment.' }
    ]
