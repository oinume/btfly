#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import imp
import os
import sys

from btfly.conf import load_conf, ConfValidator
from btfly.utils import create_logger

class Main(object):
    def __init__(self, file, home_dir):
        default_conf_dir = os.path.join(home_dir, 'conf')

        parser = argparse.ArgumentParser(
            prog = os.path.basename(file),
            description = "A micro host management program.",
            conflict_handler = 'resolve'
        )
        parser.add_argument(
            'command', metavar='command', nargs=1,
            help='An executing btfly command.',
        )

        default_conf_path = os.path.join(default_conf_dir, 'conf.yaml')
        parser.add_argument(
            '-c', '--conf', default=default_conf_path,
            help='Configuration file path. (default: %s)' % (default_conf_path)
        )
        default_hosts_conf_path = os.path.join(default_conf_dir, 'hosts.yaml')
        parser.add_argument(
            '-H', '--hosts-conf', default=default_hosts_conf_path,
            help='Hosts configuration file path. (default: %s)' % (default_hosts_conf_path)
        )
        parser.add_argument(
            '-r', '--roles', help='Specify roles.'
        )
        parser.add_argument(
            '-f', '--field', help='Specify a field.'
        )
        parser.add_argument(
            '-D', '--debug', action='store_true', default=False,
            help='Enable debug output.',
        )

        self.home_dir = home_dir
        self.file = file
        self.arg_parser = parser
        options = parser.parse_args()
        self.options = options.__dict__
        self.log = create_logger(self.options['debug'])

    def run(self):
        conf = load_conf(self.options['conf'])
        hosts_conf = load_conf(self.options['hosts_conf'])
        
        validator = ConfValidator()
        validation_errors = validator.validate(
            conf, hosts_conf,
            self.options['conf'], self.options['hosts_conf']
        )
        # TODO: validation
        if validation_errors:
            for e in validation_errors:
                print >> sys.stderr, e.message
        
        #target_field = self.options.get('field') or 'name'
        # load subcommands
        subcommand_plugins_dir = os.path.join(self.home_dir, 'plugins')
        # TODO: handle subcommand
        subcommand_plugins = self.load_subcommand_plugins(subcommand_plugins_dir)
        for plugin in subcommand_plugins:
            subcommands = plugin.define_subcommands()
            self.log.debug("subcommands = %s" % subcommands)

    def load_module(self, module_name,basepath):
        """ モジュールをロードして返す
        """
        f,n,d = imp.find_module(module_name,[basepath])
        return imp.load_module(module_name,f,n,d)

    def load_subcommand_plugins(self, base_dir):
        """ Pluginをロードしてリストにして返す
        """
        plugins = []
        for fdn in os.listdir(base_dir):
            try:
                if fdn.endswith(".py"):
                    m = self.load_module(fdn.replace(".py",""), base_dir)
                    plugins.append(m)
                elif os.path.isdir(fdn):
                    m = self.load_module(fdn)
                    plugins.append(m)
            except ImportError:
                pass
        return plugins
    

# eval `BTFLY_ENV=production btfly --roles web --field ip env`
# --> btfly_hosts=(127.0.0.1 192.168.1.2)
# % btfly-foreach; do ssh $i uptime; done
#
# `BTFLY_ENV=production btfly --roles web --field ip csv`
# --> 127.0.0.1,192.168.1.2
# % tomahawk -h `BTFLY_ENV=production btfly --roles web --field ip tomahawk_hosts` \
#  -p 4 -c -t 30 '/etc/init.d/httpd stop'
#
# btfly-rsync pigg_files /usr/local/pigg_files/

# plugin
# tomahawk.py
# def define_subcommands():
#     return [ { 'name': 'tomahawk_hosts', 'class': TomahawkHosts } ]
#c()
