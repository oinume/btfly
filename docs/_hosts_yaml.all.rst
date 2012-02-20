hosts.yaml::

  hosts:
    - web01: { ip: '192.168.1.10', status: 'active', roles: [ 'web', 'memcached' ] }
    - db01:  { ip: '192.168.1.50', status: 'active', roles: [ 'master_db' ] }
    - db02:  { ip: '192.168.1.60', status: 'active', roles: [ 'slave_db' ] }
    - db03:  { ip: '192.168.1.61', status: 'out',    roles: [ 'slave_db' ] }
