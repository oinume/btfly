# -*- coding: utf-8 -*-
import os
import pytest
import tempfile
from cStringIO import StringIO
import utils
utils.append_home_to_path(__file__)

from btfly.utils import create_logger
from btfly.main import Main

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
HOME_DIR = os.path.dirname(os.path.dirname(TESTS_DIR))
CONF_DIR = os.path.join(HOME_DIR, 'conf')

log = create_logger(True)

def test_01_run():
    out = StringIO()
    main = Main(__file__, CONF_DIR, "env".split())
    main.run(out)
    assert "BTFLY_HOSTS=(web01 db01 db02 db03)" == out.getvalue().rstrip(), "run"

def test_02_run_validation_errors():
    with pytest.raises(RuntimeError):
        out = StringIO()
        conf_path = os.path.join(TESTS_DIR, 'invalid_duplicated_statuses.yaml')
        main = Main(__file__, CONF_DIR, ("--conf=%s env" % (conf_path)).split())
        main.run(out)

def test_03_run_status_not_defined():
    with pytest.raises(ValueError):
        out = StringIO()
        main = Main(__file__, CONF_DIR, "--statuses=foobar env".split())
        main.run(out)

def test_04_run_tag_not_defined():
    with pytest.raises(ValueError):
        out = StringIO()
        main = Main(__file__, CONF_DIR, "--tags=foobar env".split())
        main.run(out)

def test_05_run_output_file():
    output_file = os.path.join(tempfile.gettempdir(), "out")
    main = Main(__file__, CONF_DIR, ("--output-file=%s env" % output_file).split())
    main.run()
    try:
        f = open(output_file)
        assert "BTFLY_HOSTS=(web01 db01 db02 db03)" == "".join(f.readlines()).rstrip(),\
            "run > --output-file"
    finally:
        f.close()
