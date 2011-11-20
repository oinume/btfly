#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import yaml

from btfly.conf import ConfLoader, ConfValidator
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

        self.file = file
        self.arg_parser = parser
        options = parser.parse_args()
        self.options = options.__dict__
        self.log = create_logger(self.options.debug)

    def run(self):
        loader = ConfLoader()
        conf = loader.load_file(self.options['conf'])
        hosts_conf = loader.load_file(self.options['hosts_conf'])
        
        validator = ConfValidator()
        validation_errors = validator.validate(
            conf, hosts_conf,
            self.options['conf'], self.options['hosts_conf']
        )
        # TODO: validation
        if validation_errors:
            for e in validation_errors:
                print >> sys.stderr, e.message
        
        target_field = self.options.get('field')
        if target_field is None:
            target_field = 'name'
        # TODO: handle subcommand

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
# tomahawk_hosts.py
# def define_plugins():
#     return [ { 'name': 'tomahawk_hosts', 'class': TomahawkHosts } ]
#c()
