blogチュートリアル(6) テンプレートの作成
========================================

.. note::

    この記事は、Symfony 2.0.0 で動作確認しています。Symfony2がバージョンアップすると、動作しなくなる恐れがあります。

テンプレートの作成
------------------

前のステップでコントローラにはアプリケーションロジックが定義されました。
今度は、作成したindexアクションとviewアクションのためのテンプレートを作成します。

Twigテンプレート
----------------

Symfony2では、標準で2つのテンプレート言語をサポートしています。
1つ目はクラシカルなPHPテンプレートで、もう1つは\ `Twig`_\ テンプレートです。
Twigはシンプルな文法ですが非常にパワフルなテンプレート言語です。

indexアクションのテンプレート
-----------------------------

まずはindexアクションのビューを作成します。

.. code-block:: jinja

    {# src/My/BlogBundle/Resources/views/Default/index.html.twig #}
    <h1>Blog posts</h1>
    <table>
        <tr>
            <td>Id</td>
            <td>Title</td>
            <td>CreatedAt</td>
        </tr>
        <!-- ここから、posts配列をループして、投稿記事の情報を表示 -->
        {% for post in posts %}
        <tr>
            <td>{{ post.id }}</td>
            <td><a href="{{ path('blog_view', {'id':post.id}) }}">{{ post.title }}</a></td>
            <td>{{ post.createdAt|date('Y/m/d H:i') }}</td>
        </tr>
        {% else %}
        <tr>
            <td colspan="3">No posts found</td>
        </tr>
        {% endfor %}
    </table>

Twigには、大きく分けて、3種類の特別な文法があります。

- ``{{ ... }}``: 値や式の結果をテンプレートに出力するための文法です。
- ``{% ... %}``: テンプレート内でロジックを制御するための文法で、\ **タグ**\ と呼ばれます。
- ``{# ... #}``: コメントを表すための文法です。複数行にわたって使用できます。

また、Twigには\ **フィルタ**\ という概念もあります。これは、描画する前にコンテンツに対して修飾を行う機能です。
``date``\ フィルタは、日付の出力形式を変換しています。

``path``\ はTwigの関数で、ルート(route)名を指定してURIを取得する機能です。

viewアクションのテンプレート
----------------------------

viewアクションのためのテンプレートも作成します。

.. code-block:: jinja

    {# src/My/BlogBundle/Resources/views/Default/view.html.twig #}
    <h1>{{ post.title }}</h1>
    <p><small>Created: {{ post.createdAt|date('Y/m/d H:i') }}</small></p>
    <p>{{ post.body|nl2br }}</p>

ここでは、新たに ``nl2br`` フィルタが出てきましたが、このフィルタは拡張機能として定義されていて、
標準では読み込まれません。\ ``nl2br`` フィルタを読み込むためには、
設定ファイルを修正して以下のブロックを追記してください:

.. code-block:: yaml

    # app/config/config.yml
    services:
        twig.extension.text:
            class: Twig_Extensions_Extension_Text
            tags:
                - { name: twig.extension }

Twigの設定の末尾に、2行追加しています。

ブラウザで確認
--------------

ここまでのステップを完了すると、ようやくブラウザで確認することができます。
ブラウザで http://localhost/Symfony/web/app_dev.php/blog/ にアクセスしてみてください。
この時点では、投稿記事がないのでリストには何も表示されませんが、
phpMyAdminなどでサンプルの投稿記事を入れてみると、その記事のタイトルがリストに表示されていると思います。

.. _`Twig`: http://www.twig-project.org/
