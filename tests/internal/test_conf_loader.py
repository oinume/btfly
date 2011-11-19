# -*- coding: utf-8 -*-
import os
from nose.tools import eq_, ok_

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
from btfly.conf import ConfLoader
from btfly.utils import create_logger

log = create_logger(True)
loader = ConfLoader()

def test_01_load_yaml():
    object = loader.load("""
statuses: [ 'active', 'troubled' ]
environments:
  - { production: [ 'production', 'prd' ] }
  - { development: [ 'development', 'dev' ] }
""".strip(), 'yaml')

    expected = {
        'statuses': [ 'active', 'troubled' ],
        'environments': [
            { 'production': [ 'production', 'prd' ] },
            { 'development': [ 'development', 'dev' ] },
        ]
    }
    eq_(expected, object, "load (yaml)")

def test_01_load_json():
    object = loader.load("""{
"statuses": [ "active", "troubled" ],
"environments": [
    { "production": [ "production", "prd" ] },
    { "development": [ "development", "dev" ] }
]
} """.strip(), 'json')

    expected = {
        'statuses': [ 'active', 'troubled' ],
        'environments': [
            { 'production': [ 'production', 'prd' ] },
            { 'development': [ 'development', 'dev' ] },
        ]
    }
    eq_(expected, object, "load (json)")

