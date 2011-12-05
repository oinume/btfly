# -*- coding: utf-8 -*-
from __future__ import with_statement
import copy
import re
from btfly.utils import create_logger

def load_conf(file, options=None):
    if not file and not options:
        raise ValueError("Cannot determine conf loader class.")
    
    if file:
        type = None
        for t, dict in TYPE2LOADER.iteritems():
            for suffix in dict['file_suffixes']:
                if file.endswith(suffix):
                    type = t
                    break
            if type:
                break
        if type is None:
            raise ValueError("Unknown file type. File extension must be 'yaml', 'yml' or 'json'.")

        loader_class = TYPE2LOADER[type]['loader_class']
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

TYPE2LOADER = {
    'yaml': { 'file_suffixes': [ '.yml', '.yaml' ], 'loader_class': YAMLConfLoader, },
    'json': { 'file_suffixes': [ '.json' ], 'loader_class': JSONConfLoader },
}

class ConfParseError(Exception):
    def __init__(self, message, file, line=None):
        super(ConfParseError, self).__init__(message)
        self._message = message
        self._file = file
        self._line = line

    @property
    def file(self): return self._file

    @property
    def line(self): return self._line

    def __str__(self):
        s = self._message
        if self._file is not None and self._line is not None:
            s += " (FILE: %s, LINE: %d)" % (self._file, self._line)
        elif self._file is not None:
            s += " (FILE: %s)" % (self._file)
        return "ConfParseError <" + s + ">"

    def __repr__(self):
        return self.__str__()

DEFAULT_ENVIRONMENTS = [
    { 'production' : [ 'production' ] },
    { 'staging'    : [ 'staging' ] },
    { 'development': [ 'development' ] },
]
class HostsManager(object):
    def __init__(self, conf, hosts_conf, log):
        self._conf = conf
        self._hosts_conf = hosts_conf
        self._log = log
        if log is None:
            self._log = create_logger()

    @property
    def conf(self): return self._conf

    @property
    def hosts_conf(self): return self._hosts_conf

    def validate(self, conf_file=None, hosts_conf_file=None):
        """
        validate self.conf and self.hosts_conf with original files.
        """

        errors = []

        ### statuses: required list->string
        statuses = self.conf.get('statuses')
        if statuses is None:
            errors.append(ConfParseError("Attribute 'statuses' is required.", conf_file, 0))
        elif type(statuses).__name__ != 'list':
            errors.append(self._attribute_must_be_list_error('statuses', conf_file))
        self._log.debug("statuses = %s" % (statuses))

        ### environments: optional list->dict->list
        environments = self.conf.get('environments')
        if environments:
            if type(environments).__name__ != 'list':
                errors.append(self._attribute_must_be_list_error('environments', conf_file))
        else:
            environments = copy.deepcopy(DEFAULT_ENVIRONMENTS)
            # Set default environments
            self.conf['environments'] = environments
        self._log.debug("environments = %s" % (environments))

        ### roles: optional list->dict
        roles = self.hosts_conf.get('roles') or [] # Contains role dict
        role_names = [] # Contains just role names
        if roles:
            if type(roles).__name__ == 'list':
                for role in roles:
                    if type(role).__name__ == 'dict':
                        role_names.append(role.keys()[0])
                    else:
                        errors.append(ConfParseError(
                            "A role entry must be a hash.",
                            hosts_conf_file,
                            self._error_line(re.compile(r'^roles\s*:'), hosts_conf_file)
                        ))
            else:
                errors.append(self._attribute_must_be_list_error('roles', hosts_conf_file))
        else:
            # Set default roles
            self.hosts_conf['roles'] = []
        self._log.debug("role_names = %s" % (role_names))

        ### hosts: required
        hosts = self.hosts_conf.get('hosts')
        if hosts is None:
            errors.append(ConfParseError("Attribute 'hosts' is required.", hosts_conf_file, 0))
        elif type(hosts).__name__ != 'list':
            errors.append(self._attribute_must_be_list_error('hosts', hosts_conf_file))
        
        if errors:
            # If any errors found at this point,
            # we cannot continue process, so return errors
            return errors

        host_names = [] # For checking a host name is unique.
        for host in hosts:
            ### host required dict
            if type(host).__name__ != 'dict':
                errors.append(ConfParseError(
                    "'host' entry must be a hash.",
                    hosts_conf_file,
                    None,
                ))
                # We cannot continue validation
                continue

            host_name = host.keys()[0]
            attrs = host.values()[0]
            host_name_regexp = re.compile(host_name) # TODO: cannot find line no bug.
            if type(attrs).__name__ != 'dict':
                errors.append(ConfParseError(
                    "Host '%s' must have a hash." % (host_name),
                    hosts_conf_file,
                    self._error_line(host_name_regexp, hosts_conf_file)
                ))
                continue
            
            if host_name in host_names:
                errors.append(ConfParseError(
                     "Duplicated name for host '%s'" % (host_name),
                     hosts_conf_file,
                     self._error_line(host_name_regexp, hosts_conf_file)
                ))
            host_names.append(host_name)

            # Check required attributes is defined.
            attribute_required_error = False
            for attribute in ('ip', 'status', 'roles'):
                if attrs.get(attribute) is None:
                    errors.append(ConfParseError(
                        "Attribute '%s' is required for host '%s'" % (attribute, host_name),
                        hosts_conf_file,
                        self._error_line(host_name_regexp, hosts_conf_file)
                    ))
                    attribute_required_error = True
            if attribute_required_error:
                continue
            
            host_status = attrs.get('status')
            ### host status: required string
            if not host_status in statuses:
                errors.append(ConfParseError(
                     "Invalid status '%s' for host '%s'" % (host_status, host_name),
                     hosts_conf_file,
                     self._error_line(host_name_regexp, hosts_conf_file)
                ))
            
            host_roles = attrs.get('roles')
            ### host roles: required list
            if type(host_roles).__name__ != 'list':
                errors.append(ConfParseError(
                    "Invalid type of roles for host '%s'" % (host_name),
                    hosts_conf_file,
                    self._error_line(host_name_regexp, hosts_conf_file)
                ))
                continue
            
            for host_role in host_roles:
                if not host_role in role_names:
                    errors.append(ConfParseError(
                        "Invalid role '%s' for host '%s'" % (host_role, host_name),
                        hosts_conf_file,
                        self._error_line(host_name_regexp, hosts_conf_file)
                    ))
            

        # Returns all found errors
        return errors

    def _error_line(self, regexp, conf_file):
        """
        Find a line number of error in `conf_file'
        """
        if conf_file is None:
            return 0
        self._log.debug("conf_file = %s" % (conf_file))
        f = open(conf_file)
        try:
            line_number = 1
            for line in f:
                if regexp.match(line):
                    return line_number
                line_number += 1
            return 0
        finally:
            f.close()

    def _attribute_must_be_list_error(self, attribute, file):
        return ConfParseError(
            "Attribute '%s' must be a list." % (attribute),
            file,
            self._error_line(re.compile(r'^' + attribute + r'\s*:'), file)
        )

    def host_names(self, **kwargs):
        # Return names
        return [ host.keys()[0] for host in self.hosts(**kwargs) ]

    def ip_addresses(self, **kwargs):
        # Return ips
        return [ host.values()[0].get('ip') for host in self.hosts(**kwargs) ]

    def hosts(self, **kwargs):
        hosts = self._hosts_conf.get('hosts')
        target_roles = kwargs.get('roles')
        target_statuses = kwargs.get('statuses')
        values, values_for_roles, values_for_statuses = [], [], []
        for host in hosts:
            name = host.keys()[0]
            attributes = host.values()[0]
            roles = attributes.get('roles')
            status = attributes.get('status')

            # collect host names with specified roles
            if target_roles:
                for target_role in target_roles:
                    if target_role in roles:
                        values_for_roles.append(name)
            # collect host names with specified statuses
            if target_statuses:
                if status in target_statuses:
                    values_for_statuses.append(name)
            # collect host names without any condition
            values.append(name)
        
        target_host_names = self.determine_values(
            target_roles, target_statuses,
            values, values_for_roles, values_for_statuses
        )
        target_hosts = []
        for host in hosts:
            if host.keys()[0] in target_host_names:
                target_hosts.append(host)
        return target_hosts

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
    
