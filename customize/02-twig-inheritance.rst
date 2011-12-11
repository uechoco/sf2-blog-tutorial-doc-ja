カスタマイズ編(2) Twigのテンプレート継承
========================================

.. note::

    この記事は、Symfony 2.0.7 で動作確認しています。

HTMLタグが出力されていない
--------------------------

現在のblogアプリケーションをブラウザで表示してHTMLソースを見てみると、\ ``<html>`` タグが正しく出力されていないことに気づきます。
各テンプレートファイルに直接 ``<html>`` や ``<body>`` タグを記述しても良いのですが、
Twigの **継承** 機能を使えば、すべてのテンプレートファイルの結果に対して簡単に ``<html>`` タグを追加することができます。

テンプレートの継承
------------------

多くの場合、アプリケーションのテンプレートには、ヘッダやフッタ、サイドバーなどの共通要素が含まれています。
一般的なテンプレートエンジンでは、それらの共通要素を別ファイルに小分けにして ``include`` するような機構が用意されています。
Twigにも別ファイルのテンプレートを ``include`` する仕組みはありますが、
Twigではテンプレートの継承という別の方法で解決することが多いでしょう。
テンプレートの継承を使うと、あるテンプレートを別のテンプレートで装飾していくことができるようになります。

テンプレートの継承の例を挙げてみます。まずはベース・レイアウトのテンプレートを用意します。
ベース・レイアウトのテンプレートには先に挙げたような共通要素が多く含まれていますが、
それらの要素を **block** というTwigのタグで囲い、名前をつけます。
例えば ``<title>`` タグに関する ``block`` は以下のように定義できるでしょう。

.. code-block:: jinja

    <title>{% block title %}Welcome!{% endblock %}</title>

このように、ベース・レイアウトのテンプレートにいくつもの ``block`` を定義していきます。

次に、子となるテンプレートファイルを用意し、ベース・レイアウトのテンプレートを継承します。
以下のような構文で継承することができます。

.. code-block:: jinja

    {% extends '::base.html.twig' %}

子となるテンプレートでは、継承した親のテンプレートの ``block`` を上書きすることができます。
``title block`` を上書きしてみましょう。

.. code-block:: jinja

    {% block title %}Child Template{% endblock %}

このように、\ ``block`` 単位で上書きしていくことで、HTMLを形作っていきます。
なお、テンプレートは複数回継承することができます。

.. note::

    継承という言葉から連想されるように、テンプレートの継承はPHPのクラスの継承とよく似ています。
    ``block`` の定義は、PHP のクラスでは ベースクラスのメソッドに当たります。
    テンプレートを継承することは、PHP のクラスで extends することに当たります。
    そして、block の中身を上書きすることは、メソッドのオーバーライドに当たります。


ベース・レイアウト・テンプレート
--------------------------------

Symfony2には、テンプレートの継承のためのベース・レイアウト・テンプレートが最初から用意されています。
そのファイルを見てみましょう。

.. code-block:: jinja

    {# app/Resources/views/base.html.twig #}
    <!DOCTYPE html>
    <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <title>{% block title %}Welcome!{% endblock %}</title>
            {% block stylesheets %}{% endblock %}
            <link rel="shortcut icon" href="{{ asset('favicon.ico') }}" />
        </head>
        <body>
            {% block body %}{% endblock %}
            {% block javascripts %}{% endblock %}
        </body>
    </html>

このファイルはアプリケーションフォルダにあるので、アプリケーション全体で共通に使うことを想定しています。
このファイルをそのまま継承するのも可能ですが、一般的にはバンドルやコントローラごとに
中間のテンプレートファイルを設けて、多段階に継承していきます。

テンプレートの修正
------------------

実際にblogアプリケーションのテンプレートを修正してベース・レイアウト・テンプレートを継承していきます。

すでにベース・レイアウト・テンプレートは用意されているので、
まずはblogアプリケーション用の中間テンプレートを作成します。

.. code-block:: jinja

    {# src/My/BlogBundle/Resources/views/layout.html.twig #}
    {% extends '::base.html.twig' %}
    {% block title %}ブログアプリケーション{% endblock %}

ここでは、ベース・レイアウト・テンプレートを継承して、タイトルだけを上書きしています。
次に各ページのテンプレートファイルを修正していきます。
extends 構文を記述し、今まで書いてあったコンテンツを body block でくくるだけです。

.. code-block:: jinja

    {# src/My/BlogBundle/Resources/views/Default/index.html.twig #}
    {% extends 'MyBlogBundle::layout.html.twig' %}
    
    {% block body %}
    <h1>Blog posts</h1>
    <table>
        <tr>
            <td>Id</td>
            <td>Title</td>
            <td>CreatedAt</td>
            <td>Operation</td>
        </tr>
        {# ここから、posts配列をループして、投稿記事の情報を表示 #}
        {% for post in posts %}
        <tr>
            <td>{{ post.id }}</td>
            <td><a href="{{ path('blog_show', {'id':post.id}) }}">{{ post.title }}</a></td>
            <td>{{ post.createdAt|date('Y/m/d H:i') }}</td>
            <td><a href="{{ path('blog_edit', {'id':post.id}) }}">Edit</a> <a href="{{ path('blog_delete', {'id':post.id}) }}">Delete</a></td>
        </tr>
        {% else %}
        <tr>
            <td colspan="4">No posts found</td>
        </tr>
        {% endfor %}
    </table>
    
    <div>
    <a href="{{ path('blog_new') }}">add post</a>
    </div>
    {% endblock %}

.. code-block:: jinja

    {# src/My/BlogBundle/Resources/views/Default/show.html.twig #}
    {% extends 'MyBlogBundle::layout.html.twig' %}
    
    {% block body %}
    <h1>{{ post.title }}</h1>
    <p><small>Created: {{ post.createdAt|date('Y/m/d H:i') }}</small></p>
    <p>{{ post.body|nl2br }}</p>
    {% endblock %}

.. code-block:: jinja

    {# src/My/BlogBundle/Resources/views/Default/new.html.twig #}
    {% extends 'MyBlogBundle::layout.html.twig' %}
    
    {% block body %}
    <h1>Add Post</h1>
    <form action="{{ path('blog_new') }}" method="post" {{ form_enctype(form) }} novalidate>
        {{ form_widget(form) }}
        <input type="submit" value="Save Post" />
    </form>
    {% endblock %}

.. code-block:: jinja

    {# src/My/BlogBundle/Resources/views/Default/edit.html.twig #}
    {% extends 'MyBlogBundle::layout.html.twig' %}
    
    {% block body %}
    <h1>Edit Post</h1>
    <form action="{{ path('blog_edit', {'id':post.id}) }}" method="post" {{ form_enctype(form) }} novalidate>
        {{ form_widget(form) }}
        <input type="submit" value="Save Post" />
    </form>
    {% endblock %}

ブラウザで確認する
------------------

修正したテンプレートの結果をブラウザで確認してみましょう。
HTMLソースを見てみると、\ ``<html>`` タグが出力されていることが確認できます。
もう1つ大きく違うのは、ページ下部にWebProfilerのツールバーが表示されていることです。

.. note::

    このWebProfilerのツールバーはapp_dev.phpでアクセスしているときにしか表示されません。
    ``</body>`` 閉じタグの直前に埋め込まれる仕組みになっています。
    ``</body>`` 閉じタグが見つからない場合は表示されません。


もっとテンプレートについて知りたい場合は、ガイドブックの\ `テンプレートの基本`_\ を参照してください。

.. _`テンプレートの基本`: http://docs.symfony.gr.jp/symfony2/book/templating.html

