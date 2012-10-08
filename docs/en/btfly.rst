btfly |release| documentation
=============================

What is btfly?
--------------

**btfly** is software to manager servers easier with YAML or JSON file. Once you put tags to servers in configuration file, you can get the information from **btfly** command.

Examples
--------

.. include:: ../_conf_yaml.all.rst
.. include:: ../_hosts_yaml.all.rst

.. highlight:: bash

First of all, put above conf.yaml and hosts.yaml into 'conf' directory, then run btfly command ::

  $ btfly out

This command output ::

  web01 db01 db02 db03

You can run ssh command to all servers by using this output like this. ::

  $ for host in `btfly out`; do ssh $host uptime; done

In short, it is able to do anything to your hosts (servers) like run a command with ssh by putting hosts information to hosts.yaml.

Additionally, you can do anything such as generating /etc/hosts by writing a plugin.

Narrow the hosts
^^^^^^^^^^^^^^^^

--tags ::

  $ btfly --tags=db out
  >>> db01 db02 db03

--tags option narrows hosts by tags. It's able to specify multiple tags with comma (,) like "--tags=db,web".

--statuses ::

  $ btfly --statuses=active
  >>> web01 db01 db02

--statuses option narrows hosts by statuses. It's able to specify multiple statuses with comma (,) like "--statuses=active,out". This option is used to exclude unreachable hosts.

Adding features with plugins
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pythonでプラグインを書くことで ::

  $ btfly --your-plugin-option your_plugin

のように呼び出すことができるので、例えば `Munin <http://munin-monitoring.org/>`_ の設定ファイルを生成するプラグインを作成することも可能である。

まとめ
^^^^^^

btflyを使ってサーバのステータスや役割の管理を行うようにすれば

* 特定のホストにだけコマンドを流す
* 特定のホストにファイルをリリースする

が可能になる。

Contents:
---------
.. toctree::
   :maxdepth: 2

   install
   tutorial
   btfly
   plugin

Indices and tables
==================
.. * :ref:`genindex`
.. * :ref:`modindex`
* :ref:`search`
