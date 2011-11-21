# -*- coding: utf-8 -*-

import imp
import inspect
import os

class PluginManager(object):
    def __init__(self, log):
        self._log = log
        self._subcommands = {}
        self._subcommands_list = []
        
    def register_subcommand(self, subcommand):
        if subcommand is None:
            raise ValueError("Argument subcommand is None")
        
        self._log.debug("register subcommand: '%s'" % (subcommand.name))
        subcommand.set_log(self._log)
        self._subcommands[subcommand.name] = subcommand
        self._subcommands_list.append(subcommand)

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
                        for name, object in inspect.getmembers(m):
                            if inspect.isfunction(object) and name == 'register':
                                object(self)
                except ImportError:
                    pass
        
        return plugins
