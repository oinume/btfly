# -*- coding: utf-8 -*-
import os
from nose.tools import eq_, ok_, raises

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
from btfly.conf import load_conf, HostsManager
from btfly.utils import create_logger

log = create_logger(True)

def test_01_names():
    conf = load_conf(os.path.join(TESTS_DIR, 'conf_for_loader.yaml'))
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

