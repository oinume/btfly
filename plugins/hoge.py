from btfly.subcommand import Subcommand

class Hoge(Subcommand):
    pass

def register(manager):
    manager.register_subcommand(Hoge('hoge', None))
