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
    def __init__(self, file, home_dir):
        default_conf_dir = os.path.join(home_dir, 'conf')

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

        self._home_dir = home_dir
        self._file = file

        log = None
        env_debug = os.getenv('BTFLY_DEBUG') or '0'
        if env_debug == '1' or env_debug.lower() == 'true':
            log = create_logger(True)
        else:
            log = create_logger(False)

        # TODO: プラグインをロードするタイミングとparse_args()を呼ぶ順番どうするか決める
        # plugin_dirsはconf.get()で決定される(confじゃなくて環境変数BTFLY_PLUGIN_PATHを定義するか？)
        # (os.pathsepつかう)
        plugin_manager = PluginManager(log, parser)
        plugin_dirs = [ os.path.join(home_dir, 'plugins') ]
        # load tasks
        plugin_manager.load_plugins(plugin_dirs)
        log.debug("All plugins are loaded.")

        self._arg_parser = parser
        self._args = parser.parse_args()
        self._options = self._args.__dict__
        self._log = log
        self._plugin_manager = plugin_manager

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

    def run(self, out=sys.stdout):
        # TODO:
        # validation tests
        # デフォルトのプラグイン作成(hosts生成)
        # バグ取り
        # hosts.yaml作成(Dev,Stg,Prd)
        # ディプロイスクリプト作成
        # maven repo登録スクリプト作成
        # Flashタグ切りスクリプト作成

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
        print >>out, output

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

