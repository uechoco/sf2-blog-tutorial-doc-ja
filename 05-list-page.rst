blogチュートリアル(5) ブログ閲覧ページの作成
============================================

.. note::

    この記事は、Symfony2 BETA2バージョンで動作確認しています。Symfony2がバージョンアップすると、動作しなくなる恐れがあります。

ページの作成
------------

Symfony2で新しくページを作成する場合、2つのステップが必要になります。（参考：\ `Creating Pages in Symfony2`_\ ）

- *ルーティング(route)の作成*\ : ルーティングはURIとコントローラを関連付ける役割があります。Symfony2はWebリクエストを元に、定義されたルーティングの中からマッチするものを見つけ出し、そのコントローラのアクションを実行します。
- *コントローラの作成*\ : コントローラはWebリクエストを受け取って何らかの処理をした後に、Symfony2の\ ``Response``\ オブジェクトを返す役割をになっています。

ルーティングの作成
------------------

デフォルトでは、ルーティングの設定ファイルは\ ``app/config/routing.yml``\ に配置されています。
ほかのSymfony2のアプリケーションと同様に、YAML、XML、PHPの形式で記述することができます。
Controllerに直にアノテーションを書いて定義する方法もあります。ここでは標準的なYAML形式で記述します。

.. code-block:: yaml

    # app/config/routing.yml
    blog:
        prefix: /blog
        resource: "@MyBlogBundle/Resources/config/routing.yml"

このルーティング定義は、「/blogから始まるURIは\ ``MyBlogBundle/Resources/config/routing.yml``\ で定義していて、
このルーティングルールをblogと呼ぶ」ことを表しています。
このようにSymfony2では、あるルーティング定義ファイルから別のルーティング定義ファイルを読み込むことができます。

つぎに、読み込まれる側のルーティング定義ファイルを記述します。

.. code-block:: yaml

    # src/My/BlogBundle/Resources/config/routing.yml
    blog_index:
        pattern:  /
        defaults: { _controller: MyBlogBundle:Default:index }
    
    blog_view:
        pattern:  /{id}
        defaults: { _controller: MyBlogBundle:Default:view }

1つのルーティングルールは、2つの要素で成り立っています。
1つ目の要素の\ ``pattern``\ は、どのようなURIがこのルート(route)にマッチするかを表しています。
もう1つの要素の\ ``defaults``\ は、どのコントローラが実行されるかを表しています。

さきほどのprefix定義を含めて考えると、\ ``/blog/``\ というURIでアクセスされたときに、
\ ``MyBlogBundle``\ の\ ``Default``\ コントローラの\ ``index``\ アクションを実行するように定義しています。
このルーティングルールに対して、blog_indexという名前をつけています。

他にもルーティングの定義では、プレースホルダー シンタックスなどを含む、柔軟で強力な機能がたくさんあります。
詳しくは、\ `Routing`_\ を参照してください。


コントローラの作成
------------------

さきほど作成したルーティングでは、\ ``/blog/``\ というURIでアクセスされると、
\ ``MyBlogBundle:Default:index``\ がフレームワークによって実行されるように定義しました。
ページの作成の2つ目のステップとして、コントローラを作成していきます。

\ ``init:bundle``\ コマンドでバンドルを作成しているので、\ ``MyBlogBundle``\ にはすでに\ ``DefaultController``\ が作られているでしょう。
ファイルの中を以下のように変更します。

.. code-block:: php

    // src/My/BlogBundle/Controller/DefaultController.php
    namespace My\BlogBundle\Controller;
    
    use Symfony\Bundle\FrameworkBundle\Controller\Controller;
    
    class DefaultController extends Controller
    {
        public function indexAction()
        {
            $em = $this->get('doctrine')->getEntityManager();
            $posts = $em->getRepository('MyBlogBundle:Post')->findAll();
            return $this->render('MyBlogBundle:Default:index.html.twig', array('posts' => $posts));
        }
    
        public function viewAction($id)
        {
            $em = $this->get('doctrine')->getEntityManager();
            $post = $em->find('MyBlogBundle:Post', $id);
            return $this->render('MyBlogBundle:Default:view.html.twig', array('post' => $post));
        }
    }

コントローラの各アクションは、メソッドの返り値として\ ``Response``\ オブジェクトを返す必要がありますが、
``render()``\ メソッドを使うと、テンプレートを描画してその\ ``Response``\ オブジェクトを返す一連の流れを
簡単に記述することができます。

``indexAction``\ アクションの中身を見てみましょう。

最初の行では、Doctrin2の\ ``EntityManager``\ オブジェクトを取得しています。
Doctrine2では、すべてのDB操作を\ ``EntityManager``\ を通じて行います。

2行目では、Postモデルの\ ``Repository``\ オブジェクトを取得し、\ ``findAll()``\ メソッドで全件取得しています。
Doctrine2の\ ``Repository``\ オブジェクトは、個々のモデルに対するクエリのカプセル化を行うことができます。
\ ``Repository``\ オブジェクトはモデルごとに独自のクラスとして定義して、独自のメソッドを定義することができます。
モデルごとに定義しなかった場合は、Doctrine2の標準の\ ``Repository``\ オブジェクトが採用されます。

3行目では、\ ``render()``\ メソッドを用いて、テンプレートファイルを描画し、\ ``Response``\ オブジェクトを返却しています。
テンプレートファイルの命名規則は、以下のようになっています。

*BundleName*:*ControllerName*:*TemplateName*

例えば\ ``MyBlogBundle:Default:index.html.twig``\ であれば、
\ ``MyBlogBundle``\ がバンドル名、\ ``Default``\ がコントローラ名、\ ``index.html.twig``\ がテンプレート名を指します。
この時、テンプレートファイルは\ ``src/My/BlogBundle/Resources/views/Default/index.html.twig``\ を参照します。

.. _`Creating Pages in Symfony2`: http://symfony.com/doc/current/book/page_creation.html
.. _`Routing`: http://symfony.com/doc/current/book/routing.html
