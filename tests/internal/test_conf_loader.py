# -*- coding: utf-8 -*-
import os
from nose.tools import eq_, ok_, raises

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
from btfly.conf import load_conf, YAMLConfLoader, JSONConfLoader
from btfly.utils import create_logger

log = create_logger(True)

def test_01_load_yaml():
    loader = YAMLConfLoader()
    object = loader.load("""
statuses: [ 'active', 'troubled' ]
environments:
  - { production: [ 'production', 'prd' ] }
  - { development: [ 'development', 'dev' ] }
""".strip())

    expected = {
        'statuses': [ 'active', 'troubled' ],
        'environments': [
            { 'production': [ 'production', 'prd' ] },
            { 'development': [ 'development', 'dev' ] },
        ]
    }
    eq_(expected, object, "YAMLConfLoader.load()")

def test_02_load_json():
    loader = JSONConfLoader()
    object = loader.load("""{
"statuses": [ "active", "troubled" ],
"environments": [
    { "production": [ "production", "prd" ] },
    { "development": [ "development", "dev" ] }
]
} """.strip())

    expected = {
        'statuses': [ 'active', 'troubled' ],
        'environments': [
            { 'production': [ 'production', 'prd' ] },
            { 'development': [ 'development', 'dev' ] },
        ]
    }
    eq_(expected, object, "JSONConfLoader.load()")

def test_03_load_conf():
    object = load_conf(os.path.join(TESTS_DIR, 'conf.yaml'))
    ok_(object['statuses'], "load_conf")

@raises(ValueError)
def test_04_load_conf_error():
    load_conf(os.path.join(TESTS_DIR, 'conf.ini'))

@raises(ValueError)
def test_05_load_conf_error():
    load_conf(None, None)
