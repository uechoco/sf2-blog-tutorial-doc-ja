カスタマイズ編(4) 投稿日時・更新日時の自動挿入
==============================================

.. note::

    この記事は、Symfony 2.0.7 で動作確認しています。

ライフサイクル・コールバック
----------------------------

現在のblogアプリケーションでは、記事を追加したり編集したりするときに ``createdAt`` や ``updatedAt`` をコントローラで定義して更新しています。
毎回このような処理を書くのは面倒なので、エンティティクラス側で自動的に更新されると便利です。

Doctrine2には **ライフサイクル・コールバック** と呼ばれる機構があり、データの挿入・更新・削除の前後に特別な処理を定義することができます。

アノテーション記法でライフサイクル・コールバックを使用する場合は、エンティティクラスの冒頭で ``HasLifecycleCallbacks`` を明示的に宣言する必要があります。
YAMLやXMLで使用する場合はこの指定は必要ありません。

.. code-block:: php

    /**
     * @ORM\Entity()
     * @ORM\HasLifecycleCallbacks()
     */
    class Post
    {
        // ...
    }

ライフサイクル・コールバックが有効になったら、所定の書式でメソッドを登録するだけです。
例えば、最初に永続化(persist)される直前にだけコールバックされるメソッドは以下のように書きます。

.. code-block:: php

    /**
     * @ORM\PrePersist
     */
    public function setCreatedValue()
    {
        $this->created = new \DateTime();
    }

ライフサイクルのイベントの種類は、以下のようなものがあります。

- ``PreRemove``
- ``PostRemove``
- ``PrePersist``
- ``PostPersist``
- ``PreUpdate``
- ``PostUpdate``
- ``PostLoad``
- ``LoadClassMetadata``

修正する
--------

ライフサイクル・コールバックを使って、
blogアプリケーションの ``Post`` エンティティの投稿日時と更新日時が自動的に更新されるように修正しましょう。

まずは ``Post`` エンティティを修正して、ライフサイクル・コールバックを埋め込みます。
クラス定義のアノテーションで ``HasLifecycleCallbacks`` を宣言し、
``PrePersist`` と ``PreUpdate`` のライフサイクル・イベントに対するメソッドを書きます。

.. code-block:: php

    /**
     * @ORM\Entity
     * @ORM\HasLifecycleCallbacks
     */
    class Post
    {
        // ...
        
        /**
         * set values bedore persist
         *
         * @ORM\PrePersist
         */
        public function prePersist()
        {
            $this->createdAt = new \DateTime();
            $this->updatedAt = new \DateTime();
        }
    
        /**
         * set values bedore update
         *
         * @ORM\PreUpdate
         */
        public function preUpdate()
        {
            $this->updatedAt = new \DateTime();
        }
                
        // ...
    }

次に DefaultController.php の newAction() と editAction() の中でデータベースへの保存前にあった投稿日時と更新日時の設定を削除します。

.. code-block:: php

        public function newAction()
        {
            // ...
                // $post->setCreatedAt(new \DateTime());
                // $post->setUpdatedAt(new \DateTime());
            // ...
        }
        
        public function editAction($id)
        {
            // ...
                // $post->setUpdatedAt(new \DateTime());
        }

ブラウザで確認する
------------------

ブラウザで記事の投稿、編集を確認してみましょう。
以前と変わらない動作をしていますが、ライフサイクル・コールバックのおかげで投稿日時・更新日時がしっかり記録されています。

ライフサイクル・コールバックについてもっと詳しく知りたい方は、Doctrine のドキュメントの `Lifecycle Events documentation`_ を参照してください。

.. note::

    ライフサイクル・コールバックを使わずに、イベントリスナーを登録して同様の処理を行う方法もあります。
    詳しくはクックブックの `Registering Event Listeners and Subscribers`_ を参照してみてください。

.. note::

    今回扱った ``createdAt`` と ``updatedAt`` を自動更新する処理はDoctrineでは ``Timestampable`` と呼ばれています。
    Doctrineには他にも ``Sluggable`` や ``Translatable``\ 、\ ``Loggable`` などのビヘイビアがよく使われます。
    これらのビヘイビアを簡単に実装するための ``DoctrineExtensionsBundle`` というライブラリもあります。
    詳しくは `Doctrine Extensions: Timestampable: Sluggable, Translatable, etc.`_ を参照してみてください。

.. _`Lifecycle Events documentation`: http://www.doctrine-project.org/docs/orm/2.0/en/reference/events.html#lifecycle-events
.. _`Registering Event Listeners and Subscribers`: http://symfony.com/doc/current/cookbook/doctrine/event_listeners_subscribers.html
.. _`Doctrine Extensions: Timestampable: Sluggable, Translatable, etc.`: http://symfony.com/doc/current/cookbook/doctrine/common_extensions.html

