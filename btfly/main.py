#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import sys

from btfly.conf import load_conf, HostsManager
from btfly.utils import create_logger
from btfly.plugin_manager import PluginManager
from btfly.task import BaseTask

class Context(object):
    def __init__(self, home_dir, options, hosts_manager, field):
        self.home_dir = home_dir
        self.options = options
        self.hosts_manager = hosts_manager
        self.field = field

class Main(object):
    def __init__(self, file, home_dir, commandline_args=sys.argv[1:]):
        default_conf_dir = os.path.join(home_dir, 'conf')

        log = None
        env_debug = os.getenv('BTFLY_DEBUG') or '0'
        if env_debug == '1' or env_debug.lower() == 'true':
            log = create_logger(True)
        else:
            log = create_logger(False)
        self._log = log

        parser = argparse.ArgumentParser(
            prog = os.path.basename(file),
            description = "A micro host management program.",
            conflict_handler = 'resolve'
        )
        default_conf_path = os.path.join(default_conf_dir, 'conf.yaml')
        parser.add_argument(
            '-c', '--conf', default=default_conf_path,
            help='Configuration file path. (default: %s)' % (default_conf_path)
        )
        default_hosts_conf_path = self.default_hosts_conf_path(default_conf_dir)
        parser.add_argument(
            '-h', '--hosts-conf', default=default_hosts_conf_path,
            help='Hosts configuration file path. (default: %s)' % (default_hosts_conf_path)
        )
        parser.add_argument(
            '-s', '--statuses', help='Specify statues.'
        )
        parser.add_argument(
            '-r', '--roles', help='Specify roles.'
        )
        parser.add_argument(
            '-f', '--field', help='Specify a field.'
        )
        parser.add_argument(
            '-o', '--output-file', type=argparse.FileType('w'),
            help='Specify a file path to output. Default behavior is outputing to stdout.'
        )
        parser.add_argument(
            '-D', '--debug', action='store_true', default=False,
            help='Enable debug output.',
        )

        self._home_dir = home_dir
        self._file = file

        plugin_manager = PluginManager(log, parser)
        # load tasks
        plugin_manager.load_plugins(self.plugin_dirs(home_dir))
        log.debug("All plugins are loaded.")

        self._arg_parser = parser
        self._args = parser.parse_args(commandline_args)
        self._options = self._args.__dict__
        self._plugin_manager = plugin_manager

        # Load configuration
        conf = load_conf(self._options['conf'])
        hosts_conf = load_conf(self._options['hosts_conf'])
        self._hosts_manager = HostsManager(conf, hosts_conf, self._log)
        
        validation_errors = self._hosts_manager.validate(
            self._options['conf'], self._options['hosts_conf']
        )
        if validation_errors:
            for e in validation_errors:
                print >> sys.stderr, e.message
            raise RuntimeError("There are some errors in configuration files.")

        error = False
        if self._options.get('statuses'):
            # Check given --statuses are defined.
            conf_statuses = conf.get('statuses')
            statuses_list = [ s.strip() for s in self._options.get('statuses').split(',') ]
            for s in statuses_list:
                if s in conf_statuses:
                    statuses_list.append(s)
                else:
                    print >>sys.stderr, "status '%s' is not defined in configuration." % (s)
                    error = True
            self._options['statuses_list'] = statuses_list
        if error:
            raise ValueError("Option --statuses error")

        if self._options.get('roles'):
            # Check given --statuses are defined.
            conf_roles = conf.get('roles')
            roles_list = [ s.strip() for s in self._options.get('roles').split(',') ]
            for r in roles_list:
                if r in conf_roles:
                    roles_list.append(r)
                else:
                    print >>sys.stderr, "role '%s' is not defined in configuration." % (s)
                    error = True
            self._options['roles_list'] = roles_list
        if error:
            raise ValueError("Option --roles error")


    def run(self, out=None):
        # load tasks
        self._log.debug("options = %s" % (self._options))
        task = self._plugin_manager.task(self._options.get('task'))
        if not isinstance(task, BaseTask):
            raise ValueError("task '%s' is not instance of BaseTask." % task)

        field = self._options.get('field') or 'name'
        context = Context(
            self._home_dir,
            self._options,
            self._hosts_manager,
            field
        )
        output = self._args.func(context)
        should_close = False
        if out is None:
            out = self._options.get('output_file')
            if out is None:
                out = sys.stdout
            else:
                should_close = True
        try:
            print >>out, output
        finally:
            if should_close:
                try:
                    out.close()
                except IOError:
                    pass

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

    def default_hosts_conf_path(self, conf_dir):
        path = None
        if os.getenv('BTFLY_ENV'):
            # If BTFLY_ENV=production is defined, load 'hosts_production.yaml'
            path = os.path.join(conf_dir, 'hosts_%s.yaml' % os.getenv('BTFLY_ENV'))
            if not os.path.isfile(path):
                #self._log.warn("%s doesn't exist." % path)
                path = None
        if not path:
            path = os.path.join(conf_dir, 'hosts.yaml')
        return path

    def plugin_dirs(self, home_dir):
        plugin_dirs = []
        plugin_path = os.getenv('BTFLY_PLUGIN_PATH')
        if plugin_path:
            for path in plugin_path.split(os.pathsep):
                if os.path.isdir(path):
                    plugin_dirs.append(path)
                else:
                    self._log.warn("Plugin path '%s' not found. Ignored." % path)
        plugin_dirs.append(os.path.join(home_dir, 'plugins'))
        self._log.debug("plugin_dirs = %s" % plugin_dirs)
        return plugin_dirs

