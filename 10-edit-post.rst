blogチュートリアル(10) 記事の編集
=================================

.. note::

    この記事は、Symfony 2.0.7 で動作確認しています。


最後に既存の記事を編集できるようにしてみましょう。
ここまで学習された方は、どのような手順で編集機能を実装するか、想像がついていることでしょう。

記事を編集するページのルーティングの作成
----------------------------------------

Symfonyでページを追加する際の作業パターンは

#. ルーティングを追加
#. アクションを追加
#. テンプレートを追加

です。記事を編集するページが増えますので、対応するルーティングを追加する必要があります。
``src/My/BlogBundle/Resources/config/routing.yml`` に ``blog_edit`` ルート(route)を追加してください。

.. code-block:: yaml

    # src/My/BlogBundle/Resources/config/routing.yml
    blog_edit:
        pattern:  /{id}/edit
        defaults: { _controller: MyBlogBundle:Default:edit }

編集アクションの作成
--------------------

続いて、\ ``Default`` コントローラに ``edit`` アクションを追加します。

.. code-block:: php

    // src/My/BlogBundle/Controller/DefaultController.php
    class DefaultController extends Controller
    {
        // ...
        public function editAction($id)
        {
            // DBから取得
            $em = $this->getDoctrine()->getEntityManager();
            $post = $em->find('MyBlogBundle:Post', $id);
            if (!$post) {
                throw new NotFoundHttpException('The post does not exist.');
            }
    
            // フォームのビルド
            $form = $this->createFormBuilder($post)
                ->add('title')
                ->add('body')
                ->getForm();
    
            // バリデーション
            $request = $this->getRequest();
            if ('POST' === $request->getMethod()) {
                $form->bindRequest($request);
                if ($form->isValid()) {
                    // 更新されたエンティティをデータベースに保存
                    $post = $form->getData();
                    $post->setUpdatedAt(new \DateTime());
                    $em->flush();
                    return $this->redirect($this->generateUrl('blog_index'));
                }
            }
    
            // 描画
            return $this->render('MyBlogBundle:Default:edit.html.twig', array(
                'post' => $post,
                'form' => $form->createView(),
            ));
        }
    }

前までのステップで作成した ``newAction`` と ``deleteAction`` の内容を合わせたようなアクションになっています。
最初に ``$id`` の記事をデータベースから取得し、そのオブジェクトを元にフォームをビルドし、
バリデーションを行い、バリデーションに成功した場合はデータベースに反映しています。

.. note::

    すでに永続化されているエンティティを ``EntityManager`` 経由で取得した場合、オブジェクトのプロパティを変更して ``EntityManager`` の ``flush()`` を実行するだけでデータベースに反映されることに注意してください。\ ``persist()`` は不要です。

編集用のテンプレートの作成
--------------------------

編集用のフォームを表示するためのテンプレートファイルを作成します。
記事の追加のためのフォームと大きく異なる点は、action 属性のURIだけでしょう。

.. code-block:: jinja

    {# src/My/BlogBundle/Resources/views/Default/edit.html.twig #}
    <h1>Edit Post</h1>
    <form action="{{ path('blog_edit', {'id':post.id}) }}" method="post" {{ form_enctype(form) }} novalidate>
        {{ form_widget(form) }}
        <input type="submit" value="Save Post" />
    </form>

また、記事の編集をするためのリンクを、記事一覧に追加します。

.. code-block:: jinja

    {# src/My/BlogBundle/Resources/views/Default/index.html.twig #}
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

ブラウザで確認
--------------

コードの入力が完了したら、ブラウザで http://localhost/Symfony/web/app_dev.php/blog/ にアクセスしてみてください。
各行にEditというリンクが表示されているので、押すと編集ページに遷移します。
内容を変更して「Save Post」をすれば、記事が保存されて一覧ページにリダイレクトされます。


