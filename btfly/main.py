#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
import yaml

config = {}
with open('config.yml') as f:
    content = '\n'.join(f.readlines())
    config = yaml.load(content)
print config

roles = []
with open('roles.yml') as f:
    content = '\n'.join(f.readlines())
    roles = yaml.load(content)
print roles

hosts = []
with open('hosts.yml') as f:
    content = '\n'.join(f.readlines())
    hosts = yaml.load(content)
    print hosts

# eval `BTFLY_ENV=production btfly --roles web --field ip env`
# --> btfly_hosts=(127.0.0.1 192.168.1.2)
# % btfly-foreach; do ssh $i uptime; done
#
# `BTFLY_ENV=production btfly --roles web --field ip csv`
# --> 127.0.0.1,192.168.1.2
# % tomahawk -h `BTFLY_ENV=production btfly --roles web --field ip csv` \
#  -p 4 -c -t 30 '/etc/init.d/httpd stop'
#
# btfly-rsync pigg_files /usr/local/pigg_files/
