# -*- coding: utf-8 -*-
import os
from cStringIO import StringIO
from nose.tools import eq_, ok_, raises

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
from btfly.conf import load_conf, YAMLConfLoader, JSONConfLoader
from btfly.utils import create_logger
from btfly.main import Main

log = create_logger(True)

def test_01_run():
    out = StringIO()
    home_dir = os.path.dirname(os.path.dirname(TESTS_DIR))
    main = Main(__file__, home_dir, "env".split())
    main.run(out)
    print("out = %s" % out)



