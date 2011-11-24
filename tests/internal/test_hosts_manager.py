# -*- coding: utf-8 -*-
import os
from nose.tools import eq_, ok_, raises

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
from btfly.conf import load_conf, HostsManager
from btfly.utils import create_logger

log = create_logger(True)

def test_01_names():
    conf = load_conf(os.path.join(TESTS_DIR, 'conf.yaml'))
    hosts_conf = load_conf(os.path.join(TESTS_DIR, 'hosts.yaml'))
    hosts_manager = HostsManager(conf, hosts_conf)
    eq_(
        [ 'web01', 'web02', 'web03', 'mdb01', 'sdb01', 'sdb02', 'sdb03' ],
        hosts_manager.names(),
        "names (all)"
    )
    eq_(
        [ 'web03' ],
        hosts_manager.names(roles=[ 'web', 'master_db' ], statuses=[ 'dead' ]),
        "names (roles, statuses)"
    )
    #print hosts_manager.names(roles=[ 'web', 'master_db' ], statuses=[ 'dead' ])

def test_02_ip_addresses():
    conf = load_conf(os.path.join(TESTS_DIR, 'conf.yaml'))
    hosts_conf = load_conf(os.path.join(TESTS_DIR, 'hosts.yaml'))
    hosts_manager = HostsManager(conf, hosts_conf)
    eq_(
        [ '192.168.1.110', '192.168.1.111', '192.168.1.112' ],
        hosts_manager.ip_addresses(roles=[ 'slave_db' ]),
        "ip_addresses (roles)"
    )
#    eq_(
#        [ 'web03' ],
#        hosts_manager.names(roles=[ 'web', 'master_db' ], statuses=[ 'dead' ]),
#        "names (roles, statuses)"
#    )
    #print hosts_manager.names(roles=[ 'web', 'master_db' ], statuses=[ 'dead' ])

