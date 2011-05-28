blogチュートリアル(2) データベースの設定
==========================================================

.. note::

    この記事は、Symfony2 BETA2およびBETA3バージョンで動作確認しています。Symfony2がバージョンアップすると、動作しなくなる恐れがあります。

MySQLにblogsymfony2データベースを作成
-------------------------------------

このチュートリアルで使用するデータベースの名前を **blogsymfony2** とします。まずはphpMyAdmin（またはコマンドラインなど、お好きなツール）を使って、MySQLに **blogsymfony2** という名前のデータベースを作成してください。以下にデータベースを作成するためのSQL文の例を載せておきます。

.. code-block:: sql

    CREATE DATABASE `blogsymfony2` DEFAULT CHARACTER SET 'utf8';


.. note::

    データベースの照合順序は「utf8_general_ci」または「utf8_bin」に設定してください。

データベースへの接続設定
------------------------

先ほどデータベース名をblogsymgony2としましたが、MySQLデータベースへ接続するユーザ名、パスワードも **blogsymfony2** に設定します。この設定はapp/config/parameters.iniファイルに記述します。エディタでこのファイルを開き、以下のように編集してください。

.. code-block:: ini

    [parameters]
        database_driver   = pdo_mysql
        database_host     = localhost
        database_name     = blogsymfony2
        database_user     = blogsymfony2
        database_password = blogsymfony2

また、以下にblogsymgony2データベースに対して権限を付与するSQL文の例を載せておきます。

.. code-block:: sql

    GRANT ALL ON `blogsymfony2`.* TO 'blogsymfony2'@localhost IDENTIFIED BY 'blogsymfony2';

.. note::

    Symfony2の主に使用される設定ファイルは、app/config/config.ymlです。Symfony2ではYAML形式の設定ファイルを標準で採用していますが、XMLやPHP、アノテーションなどの設定ファイル形式も使用することができます。これらの形式は互換性があり、どの設定形式でも記述できるように配慮されています。例外的にapp/config/parameters.iniだけがINI形式の設定ファイルですが、これは一番設定頻度が高い項目だけを簡単に設定できるように配慮されているためです。


