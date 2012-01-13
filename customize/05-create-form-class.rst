カスタマイズ編(5) フォームクラスの作成
======================================

.. note::

    この記事は、Symfony 2.0.7 で動作確認しています。

フォームクラス
--------------

``Default`` コントローラの ``newAction()`` や ``editAction()`` のフォーム作成部を見てみると、
フォームがコントローラ内で直接生成されていることがわかります。
しかしながら、より良い実装方法はフォーム生成部分を独立したPHPクラスに分離することです。
フォーム生成部を分離することで、アプリケーション内で再利用することができます。

フォーム生成部分を独立したPHPクラスに分離するには、\ ``Symfony\Component\Form\AbstractType`` を継承したクラスを作成し、
``buildForm()`` メソッドと ``getName()`` メソッドを実装します。
例えば商品名と商品価格を表すフォームクラスを作ると以下のようになります。

.. code-block:: php

    <?php
    // src/Acme/StoreBundle/Form/ProductType.php
    namespace Acme\StoreBundle\Form;
    
    use Symfony\Component\Form\AbstractType;
    use Symfony\Component\Form\FormBuilder;
    
    class ProductType extends AbstractType
    {
        public function buildForm(FormBuilder $builder, array $options)
        {
            $builder
                ->add('name')
                ->add('price', 'money', array('currency' => 'USD'))
            ;
        }

        public function getName()
        {
            return 'product';
        }
    }

追加した個々のフォーム要素は、それぞれ ``FormType`` クラスの要素（フォームタイプ）として扱われます。
フォームタイプには、\ ``TextType`` や ``FileType``\ 、\ ``MoneyType`` などの多くの種類があります。
Formコンポーネントでは、フォームの要素がどんなフォームタイプに近しいかを推測する ``FormTypeGuesser`` クラスが存在します。
``FormTypeGuesser`` は、DoctrineやValidatorのマッピング情報から動的にフォームタイプを判別しています。

分離したフォームをコントローラで使うには、コントローラの便利関数である ``createForm()`` メソッドを使います。

.. code-block:: php

    // src/Acme/StoreBundle/Controller/DefaultController.php
    
    // add this new use statement at the top of the class
    use Acme\StoreBundle\Form\ProductType;
    
    public function indexAction()
    {
        $product = // ...
        $form = $this->createForm(new ProductType(), $product);
    
        // ...
    }

``createForm()`` メソッドは、以下のように書き直すこともできます。

.. code-block:: php

    $form = $this->createForm(new ProductType());
    $form->setData($product);

``setData()`` メソッドを使う場合、フォームタイプの推測を活用するために、
フォームクラス側に以下のメソッドを追加することが望ましいです。

.. code-block:: php

    public function getDefaultOptions(array $options)
    {
        return array(
            'data_class' => 'Acme\StoreBundle\Entity\Product',
        );
    }

修正する
--------

blogアプリケーションのフォームもクラスを分離して再利用してみましょう。
まずは、\ ``Post`` エンティティに対応する ``PostType`` フォームクラスを作成します。

.. code-block:: php

    // src/My/BlogBundle/Form/PostType.php
    namespace My\BlogBundle\Form;
    
    use Symfony\Component\Form\AbstractType;
    use Symfony\Component\Form\FormBuilder;
    
    class PostType extends AbstractType
    {
        public function buildForm(FormBuilder $builder, array $options)
        {
            $builder
                ->add('title')
                ->add('body')
            ;
        }
        
        public function getDefaultOptions(array $options)
        {
            return array(
                'data_class' => 'My\BlogBundle\Entity\Post',
            );
        }
        
        public function getName()
        {
            return 'post';
        }
    }

次に、\ ``Default`` コントローラの ``addAction()`` と ``editAction()`` で直接フォーム生成している部分をフォームクラス経由に変更します。

.. code-block:: php

    use My\BlogBundle\Form\PostType;
    
    class DefaultController extends Controller
    {
        // ...

        public function newAction()
        {
            // フォームのビルド
    //        $form = $this->createFormBuilder(new Post())
    //            ->add('title')
    //            ->add('body')
    //            ->getForm();
            $form = $this->createForm(new PostType(), new Post());
            
            // ...
        }
        // ...
        public function editAction($id)
        {
            // ...
            
            // フォームのビルド
    //        $form = $this->createFormBuilder($post)
    //            ->add('title')
    //            ->add('body')
    //            ->getForm();
            $form = $this->createForm(new PostType(), $post);
            
            // ...
        }
        // ...
    }

コントローラのソースコードが少しすっきりしました。

ブラウザで確認する
------------------

ブラウザで前と同じ動作をしているか、確認しましょう。

