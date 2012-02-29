.. code-block:: python
    
    # custom_localhost.py
    from btfly.task import BaseTask
    
    class CustomHosts(BaseTask):
        def execute(self, context):
            hosts = context.hosts_manager.hosts(
                tags=context.options.get('tags'),
                statuses=context.options.get('statuses'),
            )
            s = """
    # custom_hosts plugin for btfly
    127.0.0.1    localhost.localdomain localhost
    ::1          localhost.localdomain localhost
    """
            for host in hosts:
                s += "%s %s\n" % (host.ip, host.name)
            return s.strip()
    
    def register(manager):
        manager.register_task(CustomHosts('custom_hosts', "output as /etc/hosts format."))
