カスタマイズ編(3) フラッシュメッセージの表示
============================================

.. note::

    この記事は、Symfony 2.0.7 で動作確認しています。

フラッシュメッセージを表示する
------------------------------

現在のblogアプリケーションでは、記事の追加・編集・削除をすると自動的に記事一覧にリダイレクトしますが、
何が起きて記事一覧が表示されたのかがよくわかりません。
一般的にはフラッシュメッセージと呼ばれる一時的なメッセージを表示してユーザに知らせることが多いでしょう
（例えば、記事追加直後の画面には「記事を追加しました」といったメッセージが表示されます）。
Symfony2にはセッション管理の一環としてフラッシュメッセージを簡単に扱うための機能があります。

フラッシュメッセージを登録するには、コントローラで以下のように書きます。
おそらく、POSTリクエストで来たフォームの値を処理して、リダイレクトする前に記述するでしょう。

.. code-block:: php

    $this->get('session')->setFlash('notice', '変更が保存されました！');

フラッシュメッセージを表示するには、Twigで以下のように書きます。

.. code-block:: jinja

    {% if app.session.hasFlash('notice') %}
        <div class="flash-notice">
            {{ app.session.flash('notice') }}
        </div>
    {% endif %}


修正する
--------

実際にblogアプリケーションを修正してみましょう。
まずは ``Default`` コントローラの ``newAction()``\ 、\ ``editAction()``\ 、\ ``deleteAction()`` のリダイレクト文の直前に、
フラッシュメッセージを登録する処理を追加します。

.. code-block:: php

    // src/My/BlogBundle/Controller/DefaultController.php
    
        public function newAction()
        {
            // ...
            $this->get('session')->setFlash('my_blog', '記事を追加しました');
            return $this->redirect($this->generateUrl('blog_index'));
            // ...
        }
    
        public function deleteAction($id)
        {
            // ...
            $this->get('session')->setFlash('my_blog', '記事を削除しました');
            return $this->redirect($this->generateUrl('blog_index'));
            // ...
        }
    
        public function editAction($id)
        {
            // ...
            $this->get('session')->setFlash('my_blog', '記事を編集しました');
            return $this->redirect($this->generateUrl('blog_index'));
            // ...
        }


次にテンプレートを修正して、フラッシュメッセージを表示させます。
<h1>タグの直前に埋め込みます。

.. code-block:: jinja

    {# src/My/BlogBundle/Resources/views/Default/index.html.twig #}
    {# ... #}
    {% if app.session.hasFlash('my_blog') %}
    <div style="background-color:yellow;color:red;font-weight:bold;">
        {{ app.session.flash('my_blog') }}
    </div>
    {% endif %}
    
    <h1>Blog posts</h1>
    {# ... #}


ブラウザで確認する
------------------

ブラウザで確認してみましょう。追加・編集・削除の操作の直後に記事一覧が表示されたとき、
ページ上部に黄色い背景の赤い大きな文字でフラッシュメッセージが表示されているでしょう。
記事一覧をリロードするとフラッシュメッセージは消えてしまいます。

