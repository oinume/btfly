# -*- coding: utf-8 -*-
from __future__ import with_statement
from btfly.utils import create_logger

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

class ConfParseError(Exception):
    def __init__(self, message, file, line=None):
        super(ConfParseError, self).__init__(message)
        self._message = message
        self._file = file
        self._line = line

    def __str__(self):
        s = self._message
        if self._file is not None and self._line is not None:
            s += " (FILE: %s, LINE: %d)" % (self._file, self._line)
        elif self._file is not None:
            s += " (FILE: %s)" % (self._file)
        return "ConfParseError <" + s + ">"

    def __repr__(self):
        return self.__str__()

class HostsManager(object):
    def __init__(self, conf, hosts_conf, log):
        self._conf = conf
        self._hosts_conf = hosts_conf
        self._log = log
        if log is None:
            self._log = create_logger()

    @property
    def conf(self):
        return self._conf

    @property
    def hosts_conf(self):
        return self._hosts_conf

    def validate(self, conf_file=None, hosts_conf_file=None):
        errors = []
        # statuses
        statuses = self.conf.get('statuses')
        if statuses is None:
            errors.append(ConfParseError("Attribute 'statuses' is not found.", conf_file, 0))
        elif type(self.conf.statuses).__name__ != 'list':
            errors.append(ConfParseError("Attribute 'statuses' is not list.", conf_file, 0))

        # TODO: regexp check

        # environments
        #environments = self.conf.get('environments')
        
        return errors

    def names(self, **kwargs):
        hosts = self._hosts_conf.get('hosts')
        target_roles = kwargs.get('roles') or []
        target_statuses = kwargs.get('statuses') or []
        values, values_for_roles, values_for_statuses = [], [], []
        for host in hosts:
            name = host.keys()[0]
            attributes = host.values()[0]
            roles = attributes.get('roles') or [] # TODO: normalize
            status = attributes.get('status') or '' # TODO: ありえない

            # collect host names with specified roles
            self._append_if_roles_matched(values_for_roles, target_roles, roles, name)
            # collect host names with specified statuses
            self._append_if_statuses_matched(values_for_statuses, target_statuses, status, name)
            # collect host names without any condition
            values.append(name)
        return self.determine_values(
            target_roles, target_statuses,
            values, values_for_roles, values_for_statuses
        )

    def ip_addresses(self, **kwargs):
        hosts = self._hosts_conf.get('hosts')
        target_roles = kwargs.get('roles') or []
        target_statuses = kwargs.get('statuses') or []
        values, values_for_roles, values_for_statuses = [], [], []
        for host in hosts:
            attributes = host.values()[0]
            ip = attributes.get('ip') or '' # TODO: ありえない
            roles = attributes.get('roles') or [] # TODO: normalize
            status = attributes.get('status') or '' # TODO: ありえない

            # collect host names with specified roles
            self._append_if_roles_matched(values_for_roles, target_roles, roles, ip)
            # collect host names with specified statuses
            self._append_if_statuses_matched(values_for_statuses, target_statuses, status, ip)
            # collect host names without any condition
            values.append(ip)
        return self.determine_values(
            target_roles, target_statuses,
            values, values_for_roles, values_for_statuses
        )

    def values(self):
        pass

    def _append_if_roles_matched(self, list, target_roles, roles, value):
        # collect host names with specified roles
        for target_role in target_roles:
            for role in roles:
                if role == target_role:
                    list.append(value)

    def _append_if_statuses_matched(self, list, target_statuses, status, value):
        for target_status in target_statuses:
            if status == target_status:
                list.append(value)

    def determine_values(self, target_roles, target_statuses,
                         values, values_for_roles, values_for_statuses):
        if target_roles and target_statuses:
            return list(set(values_for_roles) & set(values_for_statuses))
        elif target_roles and not target_statuses:
            return values_for_roles
        elif not target_roles and target_statuses:
            return values_for_statuses
        else:
            return values
    
