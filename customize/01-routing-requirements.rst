カスタマイズ編(1) ルーティングのURLパラメータの必須条件の指定
=============================================================

.. note::

    この記事は、Symfony 2.0.7 で動作確認しています。

ルーティングのURLパラメータの受け入れられる値
---------------------------------------------

現在のblogアプリケーションには、以下のURLのパターンが存在します。

- ``/blog/``
- ``/blog/new``
- ``/blog/{id}/show``
- ``/blog/{id}/delete``
- ``/blog/{id}/edit``

``{id}`` には、データベースの ``Post`` テーブルのプライマリキー、すなわち整数値を期待しています。
しかしながら、\ ``{id}`` に適当な文字列を入力しても有効なURLとして受け入れられてしまっています。
例えば ``/blog/hoge/show`` や ``/blog/foo/edit`` などのURLは有効とみなされてしまい、アクションが実行されてしまいます。
``{id}`` には整数値しか受け入れないように制限する方が望ましいです。

別の例として以下のようなURLパターンを想定してみます。

- ``/blog/{id}/show``
- ``/blog/{slug}/show``

``{id}`` には、やはり ``Post`` テーブルのプライマリキー、すなわち整数値を期待しています。
一方 ``{slug}`` には、整数値以外のすべての文字列を期待しています。
しかしながら、\ ``{id}`` はあらゆる文字列を受け入れてしまうため、\ ``/blog/{slug}/show`` は実行されません。
やはりこの場合も、\ ``{id}`` には整数値しか受け入れないように制限する必要があります。

URLパラメータに必須条件を指定する
---------------------------------

``routing.yml`` の設定で、URLパラメータに対する必須条件を正規表現で指定することができます。
blogアプリケーションの ``routing.yml`` を修正して、\ ``{id}`` に整数値以外が入らないようにします。

.. code-block:: yaml

    # src/My/BlogBundle/Resources/config/routing.yml
    blog_index:
        pattern:  /
        defaults: { _controller: MyBlogBundle:Default:index }
    
    blog_new:
        pattern:  /new
        defaults: { _controller: MyBlogBundle:Default:new }
    
    blog_show:
        pattern:  /{id}/show
        defaults: { _controller: MyBlogBundle:Default:show }
        requirements:
            id:  \d+
    
    blog_delete:
        pattern:  /{id}/delete
        defaults: { _controller: MyBlogBundle:Default:delete }
        requirements:
            id:  \d+
    
    blog_edit:
        pattern:  /{id}/edit
        defaults: { _controller: MyBlogBundle:Default:edit }
        requirements:
            id:  \d+

このように修正することで、\ ``{id}`` に整数値以外が入った場合はマッチするURLが存在しないので、
どのアクションも実行されずに 404 エラーが発生するようになります。


もっとルーティングについて知りたい場合は、ガイドブックの\ `ルーティング`_\ を参照してください。

.. _`ルーティング`: http://docs.symfony.gr.jp/symfony2/book/routing.html

