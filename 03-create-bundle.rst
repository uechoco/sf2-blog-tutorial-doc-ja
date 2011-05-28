blogチュートリアル(3) バンドルの作成
==========================================================

.. note::

    この記事は、Symfony2 BETA2およびBETA3バージョンで動作確認しています。Symfony2がバージョンアップすると、動作しなくなる恐れがあります。

バンドルの作成
--------------

Symfony2には、 *バンドル(Bundle)* と呼ばれる重要な機構があります。
他のソフトウェアやフレームワークで言うところのプラグインの概念に近い存在です。
Symfony2では、コアフレームワークの機能からあなたが書こうとしているアプリケーションコードまで、すべてがバンドルで構成されています。
バンドルについて詳しくしりたい方は `Bundles` を参照してください。

.. note::

    symfony 1.x系を知っている方は、「frontendアプリケーションの中にblogモジュールを作成する」と言えば一連の流れがイメージできると思います。
    しかし、Symfony2では、frontendアプリケーションもblogモジュールもバンドルとして定義することが **できます** 。
    Symfony2ではバンドルをどの粒度で作成するのかが、アプリケーション設計上の重要なポイントになります。

このチュートリアルで作成するブログ機能もバンドルの中に作っていきます。コンソールコマンドでバンドルを作ってみましょう。

.. code-block:: bash

    $ php app/console init:bundle "My\BlogBundle" src

.. note::

    init:bundleコマンドを実行したときに以下のようなエラーが起きた場合は、app/cacheディレクトリの権限がない可能性があります。
    sudo chmod -R 777 app/cache/ などのコマンドで、権限の問題が解消できるかもしれません。

    [RuntimeException]
    Unable to write in the cache directory (/path-to-root/Symfony/app/cache/dev)


``init:bundle`` コマンドに成功すると、コンソールに以下のような出力がなされているでしょう。


.. code-block:: none

    $ php app/console init:bundle "My\BlogBundle" src
    Summary of actions
    - The bundle "MyBlogBundle" was created at "src/My/BlogBundle" and is using the namespace "My\BlogBundle".
    - The bundle contains a sample controller, a sample template and a sample routing file.

    Follow-up actions
    - Enable the bundle inside the AppKernel::registerBundles() method.
          Resource: http://symfony.com/doc/2.0/book/page_creation.html#create-the-bundle
    - Ensure that the namespace is registered with the autoloader.
          Resource: http://symfony.com/doc/2.0/book/page_creation.html#autoloading-introduction-sidebar
    - If using routing, import the bundle's routing resource.
          Resource: http://symfony.com/doc/2.0/book/routing.html#including-external-routing-resources
    - Starting building your bundle!
          Resource: http://symfony.com/doc/2.0/book/page_creation.html#the-hello-symfony-page


自動生成されるファイル
----------------------

``init:bundle`` コマンドで作成したバンドルは、以下のようなファイルから成り立っています。

.. code-block:: none

    src/
        My/
            BlogBundle/
                Controller/
                    DefaultController.php
                Resources/
                    config/
                        routing.yml
                    views/
                        Default/
                            index.html.twig
                MyBlogBundle.php


バンドルの登録
--------------

さきほど作成したバンドルと使用するためには、\ *名前空間の登録*\ と\ *Kernelへの登録* の2つの作業が必要です。

まず、名前空間の登録をします。この作業は My という名前空間と物理的なパスを結びつけ、名前空間が使用されたときに自動読み込み(autoloading)されるように設定しています。名前空間を登録することで、\ ``include`` や ``require`` などを使用することを気にかけなくてもSymfony2がよきに計らってくれます。

名前空間の登録は、\ ``app/autoload.php`` の ``registerNamespaces()`` メソッドに、以下の1行を追加します。

.. code-block:: php

    $loader->registerNamespaces(array(
        // ...
        'My' => __DIR__.'/../src',
    ));

次に、Kernelへの登録をします。この作業は、\ ``My\BlogBundle名前空間`` をSymfony2に認識させ、使用可能な状態に設定しています。

Kernelへの登録は、\ ``app/AppKernel.php`` の ``AppKernel::registerBundles()`` メソッドに、以下の1行を追加します。

.. code-block:: php

    public function registerBundles()
    {
        $bundles = array(
            // ...
            new My\BlogBundle\MyBlogBundle(),
        );

        // ...

        return $bundles;
    }

.. note::

    AppKernelには、アプリケーションで使用するすべてのバンドルのインスタンス生成文が並んでいます。
    こんなにたくさんのインスタンスを毎回生成するコストは大きいのではないかと不安になるかもしれませんが安心してください。
    この ``registerBundles()`` メソッドではDIコンテナから読み込まれるために必要な最低限の初期化処理しか行っていません。
    実際にバンドルの機能を読み込むわけではないので、大きな負荷にはなりません。
    ある程度のバンドル数までは気にしなくても大丈夫でしょう。

.. note::

    バンドルを作成する手順を復習したい場合は、\ `Creating Pages in Symfony2`_ を参照してください。


.. _`Bundles`: http://symfony.com/doc/current/book/bundles.html
.. _`Creating Pages in Symfony2`: http://symfony.com/doc/current/book/page_creation.html
