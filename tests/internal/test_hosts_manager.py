# -*- coding: utf-8 -*-
import os
from nose.tools import eq_, ok_, raises

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
from btfly.conf import load_conf, HostsManager
from btfly.utils import create_logger

log = create_logger(True)

def create_valid_hosts_manager():
    conf = load_conf(os.path.join(TESTS_DIR, 'conf.yaml'))
    hosts_conf = load_conf(os.path.join(TESTS_DIR, 'hosts.yaml'))
    return HostsManager(conf, hosts_conf, log)

def create_invalid_hosts_manager(conf_file, hosts_conf_file):
    conf = load_conf(conf_file)
    hosts_conf = load_conf(hosts_conf_file)
    return HostsManager(conf, hosts_conf, log)

def test_00_validate_statuses():
    conf_file = os.path.join(TESTS_DIR, 'invalid_00_conf.yaml')
    hosts_conf_file = os.path.join(TESTS_DIR, 'hosts.yaml')
    hosts_manager = create_invalid_hosts_manager(conf_file, hosts_conf_file)
    errors = hosts_manager.validate(conf_file, hosts_conf_file)
    e = errors[0]
    eq_(e.file, conf_file, "validate > statuses > file")
    eq_(e.message, "Attribute 'statuses' is not found.", "validate > statuses > message")

def test_01_validate_statuses():
    conf_file = os.path.join(TESTS_DIR, 'invalid_01_conf.yaml')
    hosts_conf_file = os.path.join(TESTS_DIR, 'hosts.yaml')
    hosts_manager = create_invalid_hosts_manager(conf_file, hosts_conf_file)
    errors = hosts_manager.validate(conf_file, hosts_conf_file)
    e = errors[0]
    eq_(e.message, "Attribute 'statuses' is not list.", "validate > statuses > message")
    eq_(e.line, 2, "validate > statuses > line")

def test_02_validate_environments():
    conf_file = os.path.join(TESTS_DIR, 'invalid_02_conf.yaml')
    hosts_conf_file = os.path.join(TESTS_DIR, 'hosts.yaml')
    hosts_manager = create_invalid_hosts_manager(conf_file, hosts_conf_file)
    errors = hosts_manager.validate(conf_file, hosts_conf_file)
    e = errors[0]
    eq_(e.message, "Attribute 'environments' is not list.", "validate > environments > message")
    eq_(e.line, 5, "validate > environments > line")


def test_10_names():
    conf = load_conf(os.path.join(TESTS_DIR, 'conf.yaml'))
    hosts_conf = load_conf(os.path.join(TESTS_DIR, 'hosts.yaml'))
    hosts_manager = HostsManager(conf, hosts_conf, log)
    eq_(
        [ 'web01', 'web02', 'web03', 'mdb01', 'sdb01', 'sdb02', 'sdb03' ],
        hosts_manager.names(),
        "names > all"
    )
    eq_(
        [ 'web03' ],
        hosts_manager.names(roles=[ 'web', 'master_db' ], statuses=[ 'dead' ]),
        "names > roles, statuses"
    )
    #print hosts_manager.names(roles=[ 'web', 'master_db' ], statuses=[ 'dead' ])

def test_20_ip_addresses():
    conf = load_conf(os.path.join(TESTS_DIR, 'conf.yaml'))
    hosts_conf = load_conf(os.path.join(TESTS_DIR, 'hosts.yaml'))
    hosts_manager = HostsManager(conf, hosts_conf, log)
    eq_(
        [ '192.168.1.110', '192.168.1.111', '192.168.1.112' ],
        hosts_manager.ip_addresses(roles=[ 'slave_db' ]),
        "ip_addresses > roles"
    )
#    eq_(
#        [ 'web03' ],
#        hosts_manager.names(roles=[ 'web', 'master_db' ], statuses=[ 'dead' ]),
#        "names (roles, statuses)"
#    )
    #print hosts_manager.names(roles=[ 'web', 'master_db' ], statuses=[ 'dead' ])

