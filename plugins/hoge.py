class MyClass(object):
    def __init__(self):
        pass

def define_subcommands():
    return [
        { 'name': 'hoge', 'subcommand_class': MyClass }
    ]
