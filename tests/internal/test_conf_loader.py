# -*- coding: utf-8 -*-
import os
import pytest
import utils

utils.append_home_to_path(__file__)

from btfly.conf import load_conf, YAMLConfLoader, JSONConfLoader
from btfly.utils import create_logger

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
log = create_logger(True)

def test_01_load_yaml():
    loader = YAMLConfLoader()
    object = loader.load("""
statuses: [ 'active', 'troubled' ]
environments:
  - { production: [ 'production', 'prd' ] }
  - { development: [ 'development', 'dev' ] }
tags:
  - web: { description: 'web server' }
  - memcached: { description: 'memcached' }
""".strip())

    expected = {
        'statuses': [ 'active', 'troubled' ],
        'environments': [
            { 'production': [ 'production', 'prd' ] },
            { 'development': [ 'development', 'dev' ] },
        ],
        'tags': [
            { 'web': { 'description': 'web server' } },
            { 'memcached': { 'description': 'memcached' } },
        ]
    }
    assert expected == object, "YAMLConfLoader.load()"

def test_02_load_json():
    loader = JSONConfLoader()
    object = loader.load("""{
"statuses": [ "active", "troubled" ],
"environments": [
    { "production": [ "production", "prd" ] },
    { "development": [ "development", "dev" ] }
],
"tags": [
    { "web": { "description": "web server" } },
    { "memcached":  { "description": "memcached" } }
]
}""".strip())

    expected = {
        'statuses': [ 'active', 'troubled' ],
        'environments': [
            { 'production': [ 'production', 'prd' ] },
            { 'development': [ 'development', 'dev' ] },
        ],
        'tags': [
            { 'web': { 'description': 'web server' } },
            { 'memcached': { 'description': 'memcached' } },
        ]
    }
    assert expected == object, "JSONConfLoader.load()"

def test_03_load_conf():
    object = load_conf(os.path.join(TESTS_DIR, 'conf.yaml'))
    assert object['statuses'], "load_conf"

def test_04_load_conf_error():
    with pytest.raises(ValueError):
        load_conf(os.path.join(TESTS_DIR, 'conf.ini'))

def test_05_load_conf_error():
    with pytest.raises(ValueError):
        load_conf(None, None)
