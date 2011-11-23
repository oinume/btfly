#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys

from btfly.conf import load_conf, ConfValidator
from btfly.utils import create_logger
from btfly.plugin_manager import PluginManager
from btfly.subcommand import Subcommand

class Context(object):
    def __init__(self, home_dir, options, conf, hosts_conf, field):
        self.home_dir = home_dir
        self.options = options
        self.conf = conf
        self.hosts_conf = hosts_conf
        self.field = field

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
        
        
        # load subcommands
        plugin_manager = PluginManager(self.log)
        plugin_dirs = conf.get('plugin_dirs') or []
        if not plugin_dirs:
            # Add default plugin directory
            plugin_dirs.append(self.home_dir, 'plugins')
        plugin_manager.load_plugins(plugin_dirs)
        self.log.debug("options = %s" % (self.options))
        subcommand = plugin_manager.subcommand(self.options.get('command')[0])
        if not isinstance(subcommand, Subcommand):
            raise ValueError("subcommand '%s' is not instance of Subcommand" % subcommand)

        field = self.options.get('field') or 'name'
        context = Context(self.home_dir, self.options, conf, hosts_conf, field)
        output = subcommand.execute(context)
        print output
        
        # TODO: handle subcommand
        # TODO: PluginManager.register_subcommands()を呼ぶようにする


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
