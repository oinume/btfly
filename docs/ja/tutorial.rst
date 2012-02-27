btfly チュートリアル
====================

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


conf.yaml
---------
.. include:: ../_conf_yaml.all.rst

* statuses - ホストに設定するステータスのリスト
* environments - 環境変数BTFLY_ENVで決定される環境のリスト。一般ユーザがこれを意識する必要はほぼない。
* tags - ホストに設定するタグのリスト。ここで定義されていないタグを hosts.yaml で指定しようとするとエラーになる。


hosts.yaml
----------
.. include:: ../_hosts_yaml.all.rst

* ip - IPアドレス
* status - ステータス
* tags - タグのリスト。複数指定可能


btflyの実行
-----------
下記のように btfly コマンドを実行してみる。 ::

  $ btfly out

これにより ::

  web01 db01 db02 db03

が出力される。この出力を利用することで、全てのサーバに ssh で uptime を実行することが可能になる。 ::

  $ for host in `btfly out`; do ssh $host uptime; done


条件をつける
^^^^^^^^^^^^

--tags ::

  $ btfly --tags=db out
  >>> db01 db02 db03

とすることで --tags で指定したタグのホストのみを抽出することもできる。

カンマ区切りで複数のタグを指定することも可能である。 ::

  $ btfly --tags=master_db,slave_db out
  >>> db01 db02 db03

--statuses ::

  $ btfly --statuses=active out
  >>> web01 db01 db02

とすれば status が active なホストだけを抽出できる。これにより「故障中のサーバは除外したい」ということも可能である。


プラグインによる拡張
--------------------

Pythonでプラグインを書くことが可能なので、btflyで管理しているホスト情報を利用して、特定のファイルのフォーマットを出力するプラグインを作成すれば、btflyをベースにしてMuninの設定ファイルなどを出力することが可能である。

詳細は :doc:`プラグイン <plugin>` を参照。


まとめ
------

btflyを使ってサーバのステータスや役割の管理を行うようにすれば

* 特定のホストにだけコマンドを流す
* 特定のホストにファイルをリリースする

が可能になる。プラグインを作ればどんな形式のファイルでも作れるので、様々な機能を追加することができる。
