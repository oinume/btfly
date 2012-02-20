How to install btfly
====================

必要なもの
------------

* python >= 2.5
* argparse
* PyYaml
* nose (ユニットテストを実行する際に必要)

インストール
------------

.. highlight:: bash

btflyのパッケージは `pypi <http://pypi.python.org/pypi/tomahawk/>`_ にあるので、最も簡単にインストールするには pip または easy_install を使う。

  $ sudo pip install btfly

または ::

  $ sudo easy_install btfly


もしくは昔ながらの方法でインストールすることもできる。 ::

  $ tar xvzf btfly-x.y.z.tar.gz
  $ cd btfly-x.y.z
  $ sudo python setup.py install

