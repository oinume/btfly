from btfly.task import Task

class Hoge(Task):
    pass

def register(manager):
    manager.register_task(Hoge('hoge', None))
