.. highlight:: bash

プラグインによる機能追加
========================

btfly のプラグインはPythonで実装することができる。
btfly env などの標準で組み込まれているコマンドもこのプラグイン機構を使って実装されている。

実装方法
--------

ここでは、custom_hosts という名前のプラグインを作成する。
custom_hosts.py というファイル名で下記のコードをコピーして作成する。この custom_hosts.py は

* /etc/btfly/plugins
* $BTFLY_HOME/plugins
* 環境変数 BTFLY_PLUGIN_PATH で指定したディレクトリ

のいずれかに配置することで、プラグインとして認識される。

.. include:: ../_plugin_sample.all.rst

プラグインは下記のルールにのっとって実装されている必要がある。

#. btfly.task.BaseTask クラスを継承する
#. execute メソッドをオーバライドする
#. プラグインファイル内に regsiter 関数を作成し、manager.register_task を呼び出す。このメソッドの引数は以下。
  * btfly コマンドから呼び出すコマンド名
  * プラグインの説明


プラグインの実行
----------------
それでは、作成した custom_hosts プラグインを実行してみよう。 ::

  $ btfly custom_hosts

として実行し、 下記が出力されればプラグインはうまく動作している。 ::

  # custom_hosts plugin for btfly
  127.0.0.1    localhost.localdomain localhost
  ::1          localhost.localdomain localhost
  192.168.1.10 web01
  192.168.1.50 db01
  192.168.1.60 db02
  192.168.1.61 db03

