btfly tutorial
==============

.. highlight:: bash

インストール
----------------
:doc:`インストール <install>` を参照。


はじめに
--------
下記のコマンドを実行する。 ::

  $ mkdir btfly_tutorial
  $ cd btfly_tutorial
  $ btfly-quickstart
  
confディレクトリが作成され、その配下にconf.yaml, hosts.yamlが生成される。


conf.yamlの編集
---------------
.. include:: ../_conf_yaml.all.rst

* statuses - ステータスのリスト
* environments - 環境変数BTFLY_ENVで決定される環境のリスト。一般ユーザがこれを意識する必要はほぼない。
* roles - ホストのロール(役割)のリスト


hosts.yamlの編集
----------------
.. include:: ../_hosts_yaml.all.rst

* ip - IPアドレス
* status - ステータス
* roles - ロールのリスト。複数指定可能


btflyの実行
-----------
下記のように btfly コマンドを実行してみる。 ::

  $ btfly env

これにより ::

  BTFLY_HOSTS=(web01 db01 db02 db03)

が出力される。この出力をevalすることで、全てのサーバに ssh で uptime を実行することが可能になる。 ::

  $ eval `btfly env`
  $ for host in ${BTFLY_HOSTS[@]}; do ssh $host uptime; done

条件をつける
^^^^^^^^^^^^

--roles ::

  $ eval `btfly env --roles slave_db`
  $ echo $BTFLY_HOSTS
  >>> db02 db03

とすることで --roles で指定したロールを持つホストのみを抽出することもできる。

カンマ区切りで複数のロールを指定することも可能である。 ::

  $ eval `btfly env --roles master_db,slave_db`
  $ echo $BTFLY_HOSTS
  >>> db01 db02 db03

--statuses ::

  $ eval `btfly env --statuses active`
  $ echo $BTFLY_HOSTS
  >>> web01 db01 db02

とすれば status が active なホストだけを抽出できる。これにより「故障中のサーバは除外したい」ということも可能である。


プラグインによる拡張
^^^^^^^^^^^^^^^^^^^^

Pythonでプラグインを書くことが可能なので、btflyで管理しているホスト情報を利用して、特定のファイルのフォーマットを出力するプラグインを作成すれば、btflyをベースにしてMuninやNagiosなどの設定ファイルを出力することが可能である。

詳細は :doc:`plugin <plugin>` を読んでね。


最後に
^^^^^^

btflyを使ってサーバのステータスや役割の管理を行うようにすれば

* 特定のホストにだけコマンドを流す
* 特定のホストにファイルをリリースする

が可能になる。プラグインを作ればどんな形式のファイルでも作れるので、カスタマイズも自由自在である。
