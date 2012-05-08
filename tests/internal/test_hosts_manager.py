# -*- coding: utf-8 -*-
import os
import pytest
import utils
utils.append_home_to_path(__file__)

from btfly.conf import load_conf, HostsManager
from btfly.utils import create_logger

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
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
    invalid_conf_file = os.path.join(TESTS_DIR, 'invalid_no_statuses.yaml')
    hosts_manager = create_invalid_hosts_manager(invalid_conf_file, valid_hosts_conf_file)
    errors = hosts_manager.validate(invalid_conf_file, valid_hosts_conf_file)
    e = errors[0]
    assert e.file == invalid_conf_file, "validate > statuses > file"
    assert e.message == "Attribute 'statuses' is required.", "validate > statuses > message"

    invalid_conf_file = os.path.join(TESTS_DIR, 'invalid_statuses_not_list.yaml')
    hosts_manager = create_invalid_hosts_manager(invalid_conf_file, valid_hosts_conf_file)
    errors = hosts_manager.validate(invalid_conf_file, valid_hosts_conf_file)
    e = errors[0]
    assert e.message == "Attribute 'statuses' must be a list.", "validate > statuses > message"
    assert e.line == 2, "validate > statuses > line"

    invalid_conf_file = os.path.join(TESTS_DIR, 'invalid_duplicated_statuses.yaml')
    hosts_manager = create_invalid_hosts_manager(invalid_conf_file, valid_hosts_conf_file)
    errors = hosts_manager.validate(invalid_conf_file, valid_hosts_conf_file)
    e = errors[0]
    assert e.message == "Duplicated status 'a'", "validate > statuses > message"
    assert e.line == 2, "validate > statuses > line"

def test_01_validate_environments():
    invalid_conf_file = os.path.join(TESTS_DIR, 'invalid_environments_not_list.yaml')
    hosts_manager = create_invalid_hosts_manager(invalid_conf_file, valid_hosts_conf_file)
    errors = hosts_manager.validate(invalid_conf_file, valid_hosts_conf_file)
    e = errors[0]
    assert e.message == "Attribute 'environments' must be a list.", "validate > environments > message"
    assert e.line == 5, "validate > environments > line"

    invalid_conf_file = os.path.join(TESTS_DIR, 'no_environments_conf.yaml')
    hosts_manager = create_invalid_hosts_manager(invalid_conf_file, valid_hosts_conf_file)
    errors = hosts_manager.validate(invalid_conf_file, valid_hosts_conf_file)
    log.debug("errors = %s" % errors)
    assert len(errors) == 0, "validate > environments > no environments"


def test_02_validate_tags():
    invalid_conf_file = os.path.join(TESTS_DIR, 'invalid_tags_not_list.yaml')
    hosts_manager = create_invalid_hosts_manager(
        invalid_conf_file,
        valid_hosts_conf_file
    )
    errors = hosts_manager.validate(invalid_conf_file, valid_hosts_conf_file)
    e = errors[0]
    assert e.message == "Attribute 'tags' must be a list.", "validate > tags > message"
    assert e.line == 7, "validate > tags > line"

    invalid_conf_file = os.path.join(TESTS_DIR, 'invalid_tags_entry_type.yaml')
    hosts_manager = create_invalid_hosts_manager(
        invalid_conf_file,
        valid_hosts_conf_file
    )
    errors = hosts_manager.validate(invalid_conf_file, valid_hosts_conf_file)
    e = errors[0]
    assert e.message == "A tag entry must be a hash.", "validate > tags > message"
    assert e.line == 6, "validate > tags > line"

    invalid_conf_file = os.path.join(TESTS_DIR, 'invalid_duplicated_tags.yaml')
    hosts_manager = create_invalid_hosts_manager(invalid_conf_file, valid_hosts_conf_file)
    errors = hosts_manager.validate(invalid_conf_file, valid_hosts_conf_file)
    e = errors[0]
    assert e.message == "Duplicated tag 'web'", "validate > statuses > message"
    assert e.line == 5, "validate > statuses > line"


def test_04_validate_hosts():
    invalid_hosts_conf_file = os.path.join(TESTS_DIR, 'invalid_no_hosts.yaml')
    hosts_manager = create_invalid_hosts_manager(valid_conf_file, invalid_hosts_conf_file)
    errors = hosts_manager.validate(valid_conf_file, invalid_hosts_conf_file)
    e = errors[0]
    assert e.message == "Attribute 'hosts' is required.", "validate > hosts > message"

    invalid_hosts_conf_file = os.path.join(TESTS_DIR, 'invalid_hosts_type.yaml')
    hosts_manager = create_invalid_hosts_manager(valid_conf_file, invalid_hosts_conf_file)
    errors = hosts_manager.validate(valid_conf_file, invalid_hosts_conf_file)
    e = errors[0]
    assert e.message == "Attribute 'hosts' must be a list.", "validate > hosts > message"
    assert e.line == 2, "validate > hosts > line"

    invalid_hosts_conf_file = os.path.join(TESTS_DIR, 'invalid_host_type.yaml')
    hosts_manager = create_invalid_hosts_manager(valid_conf_file, invalid_hosts_conf_file)
    errors = hosts_manager.validate(valid_conf_file, invalid_hosts_conf_file)
    e = errors[0]
    assert e.message == "'host' entry must be a hash.", "validate > host > message"
    assert len(errors) == 2, "validate > host > error count"

    invalid_hosts_conf_file = os.path.join(TESTS_DIR, 'invalid_duplicated_host_name.yaml')
    hosts_manager = create_invalid_hosts_manager(valid_conf_file, invalid_hosts_conf_file)
    errors = hosts_manager.validate(valid_conf_file, invalid_hosts_conf_file)
    e = errors[0]
    assert e.message == "Duplicated name for host 'web01'", \
        "validate > host > message"
    #assert e.line == 11, "validate > host > attribute > line"

def test_09_validate_host_attributes():
    invalid_hosts_conf_file = os.path.join(TESTS_DIR, 'invalid_host_attributes_type.yaml')
    hosts_manager = create_invalid_hosts_manager(valid_conf_file, invalid_hosts_conf_file)
    errors = hosts_manager.validate(valid_conf_file, invalid_hosts_conf_file)
    e = errors[0]
    assert e.message == "Host 'localhost' must have a hash.", "validate > host > attribute > message"
    # TODO: bug
    #assert e.line == 11, "validate > host > line"

    invalid_hosts_conf_file = os.path.join(TESTS_DIR, 'invalid_host_attributes_required.yaml')
    hosts_manager = create_invalid_hosts_manager(valid_conf_file, invalid_hosts_conf_file)
    errors = hosts_manager.validate(valid_conf_file, invalid_hosts_conf_file)
    e = errors[0]
    assert e.message == "Attribute 'ip' is required for host 'localhost'", \
        "validate > host > attribute > message"
    #assert e.line == 11, "validate > host > attribute > line"

def test_11_validate_host_status_name():
    invalid_hosts_conf_file = os.path.join(TESTS_DIR, 'invalid_host_status_name.yaml')
    hosts_manager = create_invalid_hosts_manager(valid_conf_file, invalid_hosts_conf_file)
    errors = hosts_manager.validate(valid_conf_file, invalid_hosts_conf_file)
    e = errors[0]
    assert e.message == "Invalid status 'not_defined' for host 'web01'",\
        "validate > host > status > message"
    #assert e.line == 11, "validate > host > attribute > line"

def test_12_validate_host_tags_type():
    invalid_hosts_conf_file = os.path.join(TESTS_DIR, 'invalid_host_tags_type.yaml')
    hosts_manager = create_invalid_hosts_manager(valid_conf_file, invalid_hosts_conf_file)
    errors = hosts_manager.validate(valid_conf_file, invalid_hosts_conf_file)
    e = errors[0]
    assert e.message == "Invalid type of tags for host 'web01'",\
        "validate > host > tags > message"
    assert len(errors) == 2, "validate > host > tags > error count"
    #assert(e.line, 11, "validate > host > attribute > line")

def test_13_validate_host_tag_name():
    invalid_hosts_conf_file = os.path.join(TESTS_DIR, 'invalid_host_tag_name.yaml')
    hosts_manager = create_invalid_hosts_manager(valid_conf_file, invalid_hosts_conf_file)
    errors = hosts_manager.validate(valid_conf_file, invalid_hosts_conf_file)
    e = errors[0]
    assert e.message == "Invalid tag 'no_tag' for host 'web01'",\
        "validate > host > tags > message"
    #assert(e.line, 11, "validate > host > attribute > line")


def test_20_host_names():
    conf = load_conf(os.path.join(TESTS_DIR, 'conf.yaml'))
    hosts_conf = load_conf(os.path.join(TESTS_DIR, 'hosts.yaml'))
    hosts_manager = HostsManager(conf, hosts_conf, log)
    assert [ 'web01', 'web02', 'web03', 'mdb01', 'sdb01', 'sdb02', 'sdb03' ] == hosts_manager.host_names(),\
        "host_names > all"
    assert [ 'web03' ] == hosts_manager.host_names(tags=[ 'web', 'master_db' ], statuses=[ 'dead' ]),\
        "host_names > tags, statuses"

def test_30_ip_addresses():
    conf = load_conf(os.path.join(TESTS_DIR, 'conf.yaml'))
    hosts_conf = load_conf(os.path.join(TESTS_DIR, 'hosts.yaml'))
    hosts_manager = HostsManager(conf, hosts_conf, log)
    assert [ '192.168.1.110', '192.168.1.111', '192.168.1.112' ] \
        == hosts_manager.ip_addresses(tags=[ 'slave_db' ]),\
        "ip_addresses > tags"
#    assert(
#        [ 'web03' ],
#        hosts_manager.names(tags=[ 'web', 'master_db' ], statuses=[ 'dead' ]),
#        "names (tags, statuses)"
#    )
    #print hosts_manager.names(tags=[ 'web', 'master_db' ], statuses=[ 'dead' ])
