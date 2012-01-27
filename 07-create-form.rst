blogチュートリアル(7) 記事の追加
================================

.. note::

    この記事は、Symfony 2.0.7 で動作確認しています。


これまでのステップでデータベースに登録されている記事を表示できるようになりました。
次はいよいよ、フォームを作成してデータを追加・編集できるよにしてみましょう。

記事を追加するページのルーティングの作成
----------------------------------------

記事を追加するページが増えますので、対応するルーティングを追加する必要があります。
``src/My/BlogBundle/Resources/config/routing.yml`` に ``blog_new`` ルート(route)を追加してください。

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

.. note::

    ``{id}`` の条件として数値のみを受け付けるように制限することも可能です。この方法は\ `カスタマイズ編のルーティングのページ`_\ にて説明しています。

Postモデル用のフォームの作成
----------------------------

続いて、Default コントローラに記事追加用の ``new`` アクションを追加します。\ ``use`` 行を追加していることに注意してください。

.. code-block:: php

    // src/My/BlogBundle/Controller/DefaultController.php
    use My\BlogBundle\Entity\Post;
    // ...

    class DefaultController extends Controller
    {
        // ...

        public function newAction()
        {
            // フォームのビルド
            $form = $this->createFormBuilder(new Post())  // ここでPostクラスを使うため、ファイルの先頭あたりにuseを追加していることに注意
                ->add('title')
                ->add('body')
                ->getForm();
    
            // バリデーション
            $request = $this->getRequest();
            if ('POST' === $request->getMethod()) {
                $form->bindRequest($request);
                if ($form->isValid()) {
                    // エンティティを永続化
                    $post = $form->getData();
                    $post->setCreatedAt(new \DateTime());
                    $post->setUpdatedAt(new \DateTime());
                    $em = $this->getDoctrine()->getEntityManager();
                    $em->persist($post);
                    $em->flush();
                    return $this->redirect($this->generateUrl('blog_index'));
                }
            }
    
            // 描画
            return $this->render('MyBlogBundle:Default:new.html.twig', array(
                'form' => $form->createView(),
            ));
        }
    }

Symfony2では、\ ``FormBuilder`` を用いてコントローラのアクション内で簡単にフォームオブジェクトを作成することができます。
フォームオブジェクトを作成することで、バリデーションやDoctrineとの連携、フォームウィジェットのHTMLレンダリングなどを行うことができます。
このアクションでは、\ ``title`` と ``body`` の2つのフィールドを定義して、フォームを作成しています。

.. note::

    このステップではフォームをコントローラ内で動的に生成しましたが、別のクラスに分離することもできます。
    クラス化することで、アプリケーション内の別のアクションで再利用しやすくなります。

``new`` アクションでは、\ ``GET`` メソッドでアクセスした場合と、\ ``POST`` メソッドでアクセスした場合の両方を扱っています。
最初にブラウザで「/blog/new」というURLにアクセスした場合は ``GET`` メソッドになりますが、
フォームに内容を入力して送信ボタンを押した場合は ``POST`` メソッドになります。
``POST`` メソッドでアクションが実行された場合は、送信されたデータをフォームオブジェクトに\ **バインド**\ しています。
こうすることで、フォームオブジェクトに送信されたデータが統合されます。

.. note::

    CakePHPのチュートリアルでは、フォームの初回表示と投稿時でのアクション内の分岐を ``$this->data`` の有無で判断しています。
    symfony 1.x系やSymfony2では、REST(ful)の概念に基づき、このような判定をHTTPメソッドで行います。

フォームにデータをバインドすると、\ ``isValid()`` メソッドを実行してデータのバリデーション（検証）を実行できるようになります。
今のところ、バリデーションルールを追加していないので、あまり意味はありません。
バリデーションを通過した ``Post`` オブジェクトをフォームオブジェクトから取り出すには、\ ``getData()`` メソッドを使います。

フォームから取り出したオブジェクトをデータベースに登録するには、\ ``persist()`` メソッドで ``EntityManager`` に対して永続化指示を行った後、\ ``EntityManager`` の ``flush()`` メソッドを呼び出します。

.. note::

    ``Post`` オブジェクトを ``persist()`` するときに、\ ``createdAt`` と ``updatedAt`` の値を手動で代入しています。
    Doctrine2の ``Timestampable`` 拡張機能をインストールすると、この代入を自動で行うようにもできます。
    この方法は\ `カスタマイズ編の投稿日時・更新日時の自動挿入のページ`_\ で説明しています。

最後の数行は \ ``GET`` メソッドでアクセスされたときと、\ ``POST`` メソッドだがバリデーションに失敗した時に実行されます。
今まで見てきたアクションと同様に、入力フォーム用のテンプレートをレンダリングしています。
ここでは、フォームオブジェクトを描画可能な ``FormView`` オブジェクトに変換するために ``createView()`` メソッドを呼び出し、その結果をテンプレートにパラメータとして引き渡しています。

フォームを表示するテンプレートの作成
------------------------------------

最後に、表示用のテンプレートを作成します。

.. code-block:: jinja

    {# src/My/BlogBundle/Resources/views/Default/new.html.twig #}
    <h1>Add Post</h1>
    <form action="{{ path('blog_new') }}" method="post" {{ form_enctype(form) }} novalidate>
        {{ form_widget(form) }}
        <input type="submit" value="Save Post" />
    </form>

フォームタグのaction属性には、\ ``path()`` Twig関数でURIを生成しています。
``form_enctype()`` Twig関数は、ファイルアップロードフォームなどの時に ``enctype="multipart/form-data"`` を自動的に付加する関数です。
``form_widget()`` Twig関数は、HTMLウィジェットを描画する関数です。
フォームコレクション全体を与えることもできますし、個別のフォームフィールドを与えることもできます。

.. note::

    FORM タグに ``novalidate`` 属性をつけていることに注意してください。
    Symfony2 の Form コンポーネントを使うと、標準で `HTML5 のクライアントサイドフォームバリデーション`_ が有効になります。
    これはとても便利ですが、このチュートリアルではサーバーサイドのバリデーション等の実装の確認も行うため、\ ``novalidate`` 属性によりクライアントサイドバリデーションを無効化しています。
    
.. note::

    Twigで使用可能なフォーム関数を詳しく知りたい方は、\ `Twig Template Form Function Reference`_\ を参照してください。

また、記事の追加がしやすいように、ブログ一覧ページの末尾に追加ページへのリンクを追加しておきます。

.. code-block:: jinja

    {# src/My/BlogBundle/Resources/views/Default/index.html.twig #}
    {# ... #}
    <div>
    <a href="{{ path('blog_new') }}">add post</a>
    </div>

ブラウザで確認
--------------

コードの入力が完了したら、ブラウザで http://localhost/Symfony/web/app_dev.php/blog/new にアクセスしてみてください。
新規追加用のフォームが表示されたら、何かデータを入力して「Save Post」ボタンをクリックし、
データが正しく追加されるかどうか確認して下さい。

.. _`Twig Template Form Function Reference`: http://symfony.com/doc/2.0/reference/forms/twig_reference.html
.. _`カスタマイズ編のルーティングのページ`: customize/01-routing-requirements.html
.. _`カスタマイズ編の投稿日時・更新日時の自動挿入のページ`: customize/04-doctrine-timestampable.html
.. _`HTML5 のクライアントサイドフォームバリデーション`: http://www.w3.org/TR/html5/forms.html#client-side-form-validation
