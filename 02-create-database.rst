blogチュートリアル(2) データベースの設定
========================================

.. note::

    この記事は、Symfony 2.0.7 で動作確認しています。

MySQLにblogsymfony2データベースを作成
-------------------------------------

このチュートリアルで使用するデータベースの名前を **blogsymfony2** とします。まずはphpMyAdmin（またはコマンドラインなど、お好きなツール）を使って、MySQLに **blogsymfony2** という名前のデータベースを作成してください。以下にデータベースを作成するためのSQL文の例を載せておきます。

.. code-block:: sql

    CREATE DATABASE `blogsymfony2` DEFAULT CHARACTER SET 'utf8';


.. note::

    データベースの照合順序は「utf8_general_ci」または「utf8_bin」に設定してください。

データベースへの接続設定
------------------------

次に、Symfony側でMySQLに作成したデータベースへ接続する設定を行います。ここではデータベースへ接続するユーザ名、パスワードも **blogsymfony2** であると想定しています（お使いの環境に合わせて変更してください）。エディタで ``app/config/parameters.ini`` ファイルを開き、以下のように編集してください。

.. code-block:: ini

    [parameters]
        database_driver   = pdo_mysql
        database_host     = localhost
        database_port     =
        database_name     = blogsymfony2
        database_user     = blogsymfony2
        database_password = blogsymfony2

また、以下にblogsymgony2データベースに対して権限を付与するSQL文の例を載せておきます。

.. code-block:: sql

    GRANT ALL ON `blogsymfony2`.* TO 'blogsymfony2'@localhost IDENTIFIED BY 'blogsymfony2';

.. note::

    Symfony2 Standard Editionのメインの設定ファイルは、\ ``app/config/config.yml`` です。
    Symfony2ではYAML形式の設定ファイルを標準で採用していますが、XMLやPHP、アノテーションなどの設定ファイル形式も使用することができます。
    これらの形式は互換性があり、どの設定形式でも記述できるように配慮されています。

