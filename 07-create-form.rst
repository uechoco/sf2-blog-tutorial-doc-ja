blogチュートリアル(7) 記事の追加
================================

.. note::

    この記事は、Symfony 2.0.0 で動作確認しています。Symfony2がバージョンアップすると、動作しなくなる恐れがあります。


これまでのステップでデータベースに登録されている記事を表示できるようになりました。
次はいよいよ、フォームを作成してデータを追加・編集できるよにしてみましょう。

記事を追加するページのルーティングの作成
----------------------------------------

記事を追加するページが増えますので、対応するルーティングを追加する必要があります。
\ ``src/My/BlogBundle/Resources/config/routing.yml``\ に blog_add ルート(route)を追加してください。

.. code-block:: yaml

    # src/My/BlogBundle/Resources/config/routing.yml
    blog_index:
        pattern:  /
        defaults: { _controller: MyBlogBundle:Default:index }
    
    blog_add:
        pattern:  /add
        defaults: { _controller: MyBlogBundle:Default:add }
    
    blog_view:
        pattern:  /{id}
        defaults: { _controller: MyBlogBundle:Default:view }

.. note::

    blog_add ルート(route)は、 blog_view ルート(route)よりも前に定義してください。
    blog_view ルートは、 {id} と思わしきあらゆる文字列とマッチしてしまうため、最後に定義しておく必要があります。
    間違いを未然に防ぐために、 {id} の条件として数値のみを受け付けるように制限することも可能です。

Postモデル用のフォームの作成
----------------------------

続いて、Defaultコントローラにアクションを追加します。

.. code-block:: php

    // src/My/BlogBundle/Controller/DefaultController.php
    use My\BlogBundle\Entity\Post;

    class DefaultController extends Controller
    {
        // ...

        public function addAction()
        {
            // フォームのビルド
            $form = $this->get('form.factory')
                ->createBuilder('form', new Post())
                ->add('title', 'text')
                ->add('body','textarea')
                ->getForm();
    
            // バリデーション
            $request = $this->get('request');
            if ($request->getMethod() == 'POST') {
                $form->bindRequest($request);
                if ($form->isValid()) {
                    // データベースに追加
                    $post = $form->getData();
                    $now = new \DateTime('now');
                    $post->setCreatedAt($now);
                    $post->setUpdatedAt($now);
                    $em = $this->get('doctrine')->getEntityManager();
                    $em->persist($post);
                    $em->flush();
                    return $this->redirect($this->generateUrl('blog_index'));
                }
            }
    
            // 描画
            return $this->render('MyBlogBundle:Default:add.html.twig', array(
                'form' => $form->createView(),
            ));
        }
    }

Symfony2では、\ ``FormFactory``\ を用いてコントローラのアクション内で簡単にフォームオブジェクトを作成することができます。
フォームオブジェクトを作成することで、バリデーションやDoctrineとの連携、HTMLレンダリングなどを行うことができます。
このアクションでは、\ ``title``\ と\ ``body``\ の2つのフィールを定義して、フォームを作成しています。

.. note::

    このステップではフォームをコントローラ内で動的に生成しましたが、別のクラスに分離することもできます。
    クラス化することで、アプリケーション内で再利用することができます。

このアクションでは、\ ``GET``\ メソッドでアクセスした場合と、\ ``POST``\ メソッドでアクセスした場合の両方を扱っています。
最初にブラウザで「/blog/add」というURLにアクセスした場合は\ ``GET``\ メソッドになりますが、
フォームに内容を入力して送信ボタンを押した場合は\ ``POST``\ メソッドになります。
\ ``POST``\ メソッドの場合は、送信されたデータをフォームオブジェクトに\ **バインド**\ し、
フォームに関連付けられているオブジェクト、すなわち\ ``Post``\ モデルのレコードとして、扱えるようになります。

.. note::

    CakePHPのチュートリアルでは、フォームの初回表示と投稿時でのアクション内の分岐を、
    \ ``$this->data``\ の有無で判断しています。
    symfony 1.x系やSymfony2では、REST(ful)の概念に基づき、このような判定をHTTPメソッドで行います。

バインドしたデータは、 ``isValid()`` メソッドでバリデーションができます。
今のところ、バリデーションルールを追加していないので、あまり意味はありません。
バリデーションを通過した\ ``Post``\ オブジェクトを安全に取り出すには、
``getData()`` メソッドを使います。

フォームから取り出したオブジェクトをデータベースに登録するには、 ``persist()`` メソッドを使った後、
``flush()`` メソッドを呼び出します。

.. note::

    ``Post`` オブジェクトを ``persist()`` するときに、 ``createdAt`` と ``updatedAt`` の値を手動で代入しています。
    Doctrine2には\ ``Timestampable``\ というBehaviorがあり、この代入操作を自動的に行ってくれる仕組みがあります。

最後の数行で、\ ``GET``\ メソッドでアクセスされたときにテンプレートの描画を行っています。
フォームオブジェクトを描画可能な ``FormView`` オブジェクトに変換するために、
``createView()`` メソッドを呼び出しています。

フォームを表示するビューの作成
------------------------------

最後に、表示用のビューを作成します。

.. code-block:: jinja

    {# src/My/BlogBundle/Resources/views/Default/add.html.twig #}
    <h1>Add Post</h1>
    <form action="{{ path('blog_add') }}" method="post" {{ form_enctype(form) }}>
        {{ form_widget(form) }}
        <input type="submit" value="Save Post" />
    </form>

フォームタグのaction属性には、 path() Twig関数でURIを生成しています。
form_enctype() Twig関数は、ファイルアップロードフォームなどの時に ``enctype="multipart/form-data"`` を自動的に付加する関数です。
form_widget() Twig関数は、HTMLウィジェットを描画する関数です。
フォームコレクション全体を与えることもできますし、個別のフォームフィールドを与えることもできます。

.. note::

    Twigで使用可能なフォーム関数を詳しく知りたい方は、\ `Twig Template Form Function Reference`_\ を参照してください。

また、記事の追加がしやすいように、ブログ一覧にリンクを追加しておきます。

.. code-block:: jinja

    {# src/My/BlogBundle/Resources/views/Default/index.html.twig #}
    {# ... #}
    <div>
    <a href="{{ path('blog_add') }}">add post</a>
    </div>

ブラウザで確認
--------------

コードの入力が完了したら、ブラウザで http://localhost/Symfony/web/app_dev.php/blog/add にアクセスしてみてください。
新規追加用のフォームが表示されたら、何かデータを入力して「Save Post」ボタンをクリックし、
データが正しく追加されるかどうか確認して下さい。

.. _`Twig Template Form Function Reference`: http://symfony.com/doc/2.0/reference/forms/twig_reference.html

