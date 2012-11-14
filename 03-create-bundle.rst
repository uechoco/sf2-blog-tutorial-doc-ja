blogチュートリアル(3) バンドルの作成
====================================

.. note::

    この記事は、Symfony 2.0.7 で動作確認しています。

バンドルの作成
--------------

Symfony2には、 *バンドル(Bundle)* と呼ばれる重要な機構があります。
他のソフトウェアやフレームワークで言うところのプラグインの概念に近い存在です。
Symfony2では、コアフレームワークの機能からあなたが書こうとしているアプリケーションコードまで、すべてがバンドルで構成されています。
バンドルについて詳しく知りたい方は `Bundles`_ を参照してください。

.. note::

    symfony 1.x系を知っている方は、「frontendアプリケーションの中にblogモジュールを作成する」と言えば一連の流れがイメージできると思います。
    しかし、Symfony2では、frontendアプリケーションもblogモジュールもバンドルとして定義することが **できます** 。
    Symfony2ではバンドルをどの粒度で作成するのかが、アプリケーション設計上の重要なポイントになります。

このチュートリアルで作成するブログ機能もバンドルの中に作っていきます。コンソールコマンドでバンドルを作ってみましょう。

.. code-block:: console

    $ php app/console generate:bundle --namespace=My/BlogBundle --format=yml

.. note::

    ``app/console`` コマンドを実行する際のカレントディレクトリが、現在のSymfony2プロジェクトのルートディレクトリであることを確認して下さい。
    ``app`` ディレクトリ上で ``console`` と呼び出したり、他のカレントディレクトリから呼び出したりすると、正しい位置にバンドルが生成されない可能性があります。

.. note::

    ``generate:bundle`` コマンドを実行したときに以下のようなエラーが起きた場合は、\ ``app/cache`` ディレクトリ配下に適切な権限が設定されていない可能性があります。
    ``sudo chmod -R 777 app/cache`` などのコマンドで、権限の問題が解消できるかもしれません。

    .. code-block:: console

        [RuntimeException]
        Unable to write in the cache directory (/path-to-root/Symfony/app/cache/dev)

``generate:bundle`` コマンドの実行中には５〜６個の質問項目がありますが、すべての項目で何も入力せずにエンターを入力してください。
適切な初期値でコマンドを実行することができます。\ ``generate:bundle`` が成功すると、コンソールに以下のような出力がなされているでしょう。


.. code-block:: console

    $ php app/console generate:bundle --namespace=My/BlogBundle --format=yml
    
                                                
      Welcome to the Symfony2 bundle generator  
                                                
    
    
    Your application code must be written in bundles. This command helps
    you generate them easily.
    
    Each bundle is hosted under a namespace (like Acme/Bundle/BlogBundle).
    The namespace should begin with a "vendor" name like your company name, your
    project name, or your client name, followed by one or more optional category
    sub-namespaces, and it should end with the bundle name itself
    (which must have Bundle as a suffix).
    
    Use / instead of \ for the namespace delimiter to avoid any problem.
    
    Bundle namespace [My/BlogBundle]:     
    
    In your code, a bundle is often referenced by its name. It can be the
    concatenation of all namespace parts but it's really up to you to come
    up with a unique name (a good practice is to start with the vendor name).
    Based on the namespace, we suggest MyBlogBundle.
    
    Bundle name [MyBlogBundle]: 
    
    The bundle can be generated anywhere. The suggested default directory uses
    the standard conventions.
    
    Target directory [/path/to/Symfony/src]: 
    
    Determine the format to use for the generated configuration.
    
    Configuration format (yml, xml, php, or annotation) [yml]: 
    
    To help you getting started faster, the command can generate some
    code snippets for you.
    
    Do you want to generate the whole directory structure [no]? 
    
                                 
      Summary before generation  
                                 
    
    You are going to generate a "My\BlogBundle\MyBlogBundle" bundle
    in "/path/to/Symfony/src/" using the "yml" format.
    
    Do you confirm generation [yes]? 
    
                         
      Bundle generation  
                         
    
    Generating the bundle code: OK
    Checking that the bundle is autoloaded: OK
    Confirm automatic update of your Kernel [yes]? 
    Enabling the bundle inside the Kernel: OK
    Confirm automatic update of the Routing [yes]? 
    Importing the bundle routing resource: OK
    
                                                   
      You can now start using the generated code!  
                                                   
                                                   

自動生成されるファイル
----------------------

``genarate:bundle`` コマンドで作成したバンドルは、以下のようなファイルから成り立っています。

.. code-block:: text

    src/
        My/
            BlogBundle/
                Controller/
                    DefaultController.php
                DependencyInjection/
                    Configuration.php
                    MyBlogExtension.php
                Resources/
                    config/
                        routing.yml
                        services.yml
                    views/
                        Default/
                            index.html.twig
                Tests/
                    Controller/
                        DefaultControllerTest.php
                MyBlogBundle.php


バンドルの登録
--------------

さきほど作成したバンドルを使用するためには、\ *名前空間の登録*\ と *Kernel への登録* の2つの作業が必要です。
ところが、さきほどの ``generate:bundle`` コマンドが Kernel への登録も自動的に行なってくれています。
また、\ ``src`` ディレクトリに置かれたバンドルは名前空間の登録を行わなくても動くようなフォールバック機構が設定されているため、
名前空間の登録をしなくても動作します。

ここではこれらの作業がなぜ必要なのかを簡単に説明します。

名前空間の登録は、\ ``My`` という名前空間と物理的なパスを結びつけ、名前空間が使用されたときに自動読み込み(autoloading)されるように設定しています。名前空間を登録することで、\ ``include`` や ``require`` などを使用することを気にかけなくても Symfony2 がよきに計らってくれます。登録された名前空間の中に該当のクラスが見つからなかった場合は、\ ``src/`` ディレクトリの中も自動的に検索してくれます。

名前空間の登録は、\ ``app/autoload.php`` の ``registerNamespaces()`` メソッドに、以下の１行を追加します。

.. code-block:: php

    $loader->registerNamespaces(array(
        // ...
        'My' => __DIR__.'/../src',
    ));

次に、Kernel への登録は、\ ``My\BlogBundle`` 名前空間を Symfony2 に認識させ、使用可能な状態に設定するために行います。
Kernel への登録は、\ ``app/AppKernel.php`` の ``AppKernel::registerBundles()`` メソッドに、以下の１行を追加します(すでに登録されているはずです)。

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

    バンドルを作成する手順を復習したい場合は、ガイドブックの\ `Symfony2 でのページ作成`_\ を参照してください。


.. _`Bundles`: http://symfony.com/doc/current/book/bundles.html
.. _`Symfony2 でのページ作成`: http://docs.symfony.gr.jp/symfony2/book/page_creation.html
