btfly のプラグイン機構
======================

btfly のプラグインはPythonで実装することができる。
btfly env などの標準で組み込まれているコマンドもこのプラグイン機構を使って実装されている。

必要なもの
----------

* python >= 2.5
* argparse
* PyYaml
* nose (ユニットテストを実行する際に必要)

実装方法
--------

custom_hosts.py

.. code-block:: python

    # custom_hosts.py
    class CustomHosts(BaseTask):
        def execute(self, context):
            hosts = context.hosts_manager.hosts(
                roles=context.options.get('roles'),
                statuses=context.options.get('statuses'),
            )
            
            s = "# Generated with btfly\n"
            for host in hosts:
                name = host.keys()[0] # TODO: host must be object
                attributes = host.values()[0]
                s += "%s %s\n" % (attributes.get('ip'), name)
            return s.rstrip()
    
    def register(manager):
        """
        This function is called when this plugin is loaded.
        """
        manager.register_task(CSV('csv', "output as CSV."))
        manager.register_task(Env('env', "output as sh environment."))
        manager.register_task(Hosts('hosts', "output as /etc/hosts format."))

