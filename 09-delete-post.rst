blogチュートリアル(9) 記事の削除
================================

.. note::

    この記事は、Symfony 2.0.7 で動作確認しています。


次は、ユーザーが既存の記事を削除できるようにしてみましょう。

記事を削除するURIのルーティングの作成
-------------------------------------

記事を削除するURI (※ここではページではない) が増えますので、対応するルーティングを追加する必要があります。
``src/My/BlogBundle/Resources/config/routing.yml`` に ``blog_delete`` ルート(route)を追加してください。

.. code-block:: yaml

    # src/My/BlogBundle/Resources/config/routing.yml
    blog_delete:
        pattern:  /{id}/delete
        defaults: { _controller: MyBlogBundle:Default:delete }

削除アクションの作成
--------------------

続いて、\ ``Default`` コントローラに ``delete`` アクションを追加します。

.. code-block:: php

    // src/My/BlogBundle/Controller/DefaultController.php
    use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

    class DefaultController extends Controller
    {
        // ...
        public function deleteAction($id)
        {
            $em = $this->getDoctrine()->getEntityManager();
            $post = $em->find('MyBlogBundle:Post', $id);
            if (!$post) {
                throw new NotFoundHttpException('The post does not exist.');
            }
            $em->remove($post);
            $em->flush();
            return $this->redirect($this->generateUrl('blog_index'));
        }
    }

このコードでは、与えられた ``{id}`` を元に、該当記事のレコードに対応するエンティティを取得しています。
エンティティが見つからなかった場合は、\ ``NotFoundHttpException`` 例外をスローして処理を中断します。
エンティティが見つかった場合は、\ ``EntityManager`` の ``remove()`` メソッドで削除指示を出して、\ ``flush()`` します。
削除後は記事一覧にリダイレクトします。

また、記事の削除をするためのリンクを、記事一覧に追加します。

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
            <td><a href="{{ path('blog_delete', {'id':post.id}) }}">Delete</a></td>
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
各行にDeleteというリンクが出ているので、押すと記事が消えるでしょう。

