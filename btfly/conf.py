# -*- coding: utf-8 -*-
from __future__ import with_statement

class ConfLoader(object):
    def __init__(self):
        pass

    def load_file(self, file):
        if not file:
            raise ValueError("file path is empty.")

        type = None
        if file.endswith('.yaml') or file.endswith('.yml'):
            type = 'yaml'
        elif file.endswith('.json'):
            type = 'json'
        else:
            raise ValueError("Unknown file type. File extension must be 'yaml', 'yml' or 'json'.")

        f = open(file)
        try:
            return self.load('\n'.join(f.readlines()), type)
        finally:
            f.close()

    def load(self, string, type):
        object = {}
        if type == 'yaml':
            yaml = __import__('yaml')
            object = yaml.load(string)
        else:
            json = None
            try:
                json = __import__('json')
            except ImportError:
                json = __import__('simplejson')
            object = json.loads(string)
        return object

class ConfValidator(object):
    def validate(conf, hosts_conf, conf_file=None, hosts_conf_file=None):
        # TODO: implement
        return ()
