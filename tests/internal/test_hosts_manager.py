# -*- coding: utf-8 -*-
import os
from nose.tools import eq_, ok_, raises

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
from btfly.conf import load_conf, HostsManager
from btfly.utils import create_logger

log = create_logger(True)
valid_conf_file = os.path.join(TESTS_DIR, 'conf.yaml')
valid_hosts_conf_file = os.path.join(TESTS_DIR, 'hosts.yaml')

def create_valid_hosts_manager():
    return HostsManager(
        load_conf(valid_conf_file),
        load_conf(valid_hosts_conf_file),
        log
    )

def create_invalid_hosts_manager(conf_file, hosts_conf_file):
    return HostsManager(
        load_conf(conf_file),
        load_conf(hosts_conf_file),
        log
    )

def test_00_validate_statuses():
    conf_file = os.path.join(TESTS_DIR, 'invalid_no_statuses.yaml')
    hosts_manager = create_invalid_hosts_manager(conf_file, valid_hosts_conf_file)
    errors = hosts_manager.validate(conf_file, valid_hosts_conf_file)
    e = errors[0]
    eq_(e.file, conf_file, "validate > statuses > file")
    eq_(e.message, "Attribute 'statuses' is required.", "validate > statuses > message")

def test_01_validate_statuses():
    conf_file = os.path.join(TESTS_DIR, 'invalid_statuses_not_list.yaml')
    hosts_manager = create_invalid_hosts_manager(conf_file, valid_hosts_conf_file)
    errors = hosts_manager.validate(conf_file, valid_hosts_conf_file)
    e = errors[0]
    eq_(e.message, "Attribute 'statuses' must be a list.", "validate > statuses > message")
    eq_(e.line, 2, "validate > statuses > line")

def test_02_validate_environments():
    conf_file = os.path.join(TESTS_DIR, 'invalid_environments_not_list.yaml')
    hosts_manager = create_invalid_hosts_manager(conf_file, valid_hosts_conf_file)
    errors = hosts_manager.validate(conf_file, valid_hosts_conf_file)
    e = errors[0]
    eq_(e.message, "Attribute 'environments' must be a list.", "validate > environments > message")
    eq_(e.line, 5, "validate > environments > line")

def test_03_validate_no_environments():
    conf_file = os.path.join(TESTS_DIR, 'no_environments_conf.yaml')
    hosts_manager = create_invalid_hosts_manager(conf_file, valid_hosts_conf_file)
    errors = hosts_manager.validate(conf_file, valid_hosts_conf_file)
    eq_(len(errors), 0, "validate > environments > no environments")

def test_03_validate_hosts():
    invalid_hosts_conf_file = os.path.join(TESTS_DIR, 'invalid_no_hosts.yaml')
    hosts_manager = create_invalid_hosts_manager(valid_conf_file, invalid_hosts_conf_file)
    errors = hosts_manager.validate(valid_conf_file, invalid_hosts_conf_file)
    e = errors[0]
    eq_(e.message, "Attribute 'hosts' is required.", "validate > hosts > message")

def test_04_validate_roles_and_hosts():
    invalid_hosts_conf_file = os.path.join(TESTS_DIR, 'invalid_hosts_roles_type.yaml')
    hosts_manager = create_invalid_hosts_manager(valid_conf_file, invalid_hosts_conf_file)
    errors = hosts_manager.validate(valid_conf_file, invalid_hosts_conf_file)
    e = errors[0]
    eq_(e.message, "Attribute 'roles' must be a list.", "validate > roles > message")
    eq_(e.line, 2, "validate > roles > line")
    e = errors[1]
    eq_(e.message, "Attribute 'hosts' must be a list.", "validate > hosts > message")
    eq_(e.line, 4, "validate > hosts > line")

# TODO: more tests (roles defined , status defined ...)

def test_10_host_names():
    conf = load_conf(os.path.join(TESTS_DIR, 'conf.yaml'))
    hosts_conf = load_conf(os.path.join(TESTS_DIR, 'hosts.yaml'))
    hosts_manager = HostsManager(conf, hosts_conf, log)
    eq_(
        [ 'web01', 'web02', 'web03', 'mdb01', 'sdb01', 'sdb02', 'sdb03' ],
        hosts_manager.host_names(),
        "host_names > all"
    )
    eq_(
        [ 'web03' ],
        hosts_manager.host_names(roles=[ 'web', 'master_db' ], statuses=[ 'dead' ]),
        "host_names > roles, statuses"
    )

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

