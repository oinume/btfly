# -*- coding: utf-8 -*-

import imp
import inspect
import os

class PluginManager(object):
    def __init__(self, log, arg_parser):
        self._log = log
        self._arg_parser = arg_parser
        self._arg_subparsers = arg_parser.add_subparsers(
            dest='task',
            help="task help"
        )
        self._tasks = {}
        self._tasks_list = []

    @property
    def tasks(self): return self._tasks

    def task(self, name):
        return self._tasks.get(name)

    def register_task(self, task):
        if task is None:
            raise ValueError("Argument task is None")
        elif self._tasks.has_key(task.name):
            raise ValueError("Argument task '%s' is already registered." % (task.name))
        
        self._log.debug("register task: '%s'" % (task.name))
        task.set_log(self._log)
        # Define task argument with help
        subparser = task.add_arguments(self._arg_subparsers)
        if subparser is None:
            raise RuntimeError("task.add_arguments() must be return parser object. (task = '%s')" % task.name)
        # Define task options
        task.add_options(subparser)
        # Set a callback method
        subparser.set_defaults(func=task.execute)

        self._tasks[task.name] = task
        self._tasks_list.append(task)

    def load_module(self, module_name,basepath):
        f,n,d = imp.find_module(module_name,[basepath])
        return imp.load_module(module_name,f,n,d)

    def load_plugins(self, base_dirs):
        plugins = []
        for base_dir in base_dirs:
            for fdn in os.listdir(base_dir):
                try:
                    m = None
                    if fdn.endswith('.py'):
                        m = self.load_module(fdn.replace('.py', ''), base_dir)
                    elif os.path.isdir(fdn):
                        m = self.load_module(fdn)
                    
                    if m is not None:
                        plugins.append(m)
                        for name, member in inspect.getmembers(m):
                            if inspect.isfunction(member) and name == 'register':
                                member(self)
                except ImportError:
                    pass
        
        return plugins
