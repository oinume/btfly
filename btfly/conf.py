# -*- coding: utf-8 -*-
from __future__ import with_statement

def load_conf(file, options=None):
    if not file and not options:
        raise ValueError("Cannot determine conf loader class.")
    
    if file:
        type = None
        for t, dict in type2loader.iteritems():
            for suffix in dict['file_suffixes']:
                if file.endswith(suffix):
                    type = t
                    break
            if type:
                break
        if type is None:
            raise ValueError("Unknown file type. File extension must be 'yaml', 'yml' or 'json'.")

        loader_class = type2loader[type]['loader_class']
        return loader_class().load_file(file)
    else:
        # TODO
        pass

class ConfLoader(object):
    def __init__(self):
        pass

    def load_file(self, file):
        if not file:
            raise ValueError("file path is empty.")
        f = open(file)
        try:
            return self.load('\n'.join(f.readlines()))
        finally:
            f.close()

    def load(self, string):
        pass

class YAMLConfLoader(ConfLoader):
    def __init__(self):
        super(YAMLConfLoader, self).__init__()
    
    def load(self, string):
        yaml = __import__('yaml')
        return yaml.load(string)

class JSONConfLoader(ConfLoader):
    def __init__(self):
        super(JSONConfLoader, self).__init__()
    
    def load(self, string):
        json = None
        try:
            json = __import__('json')
        except ImportError:
            json = __import__('simplejson')
        return json.loads(string)

type2loader = {
    'yaml': { 'file_suffixes': [ '.yml', '.yaml' ], 'loader_class': YAMLConfLoader, },
    'json': { 'file_suffixes': [ '.json' ], 'loader_class': JSONConfLoader },
}

class ConfValidator(object):
    def validate(conf, hosts_conf, conf_file=None, hosts_conf_file=None):
        # TODO: implement
        return ()
