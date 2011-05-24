blogチュートリアル(4) テーブルスキーマとエンティティクラス
==========================================================

.. note::

    この記事は、Symfony2 BETA2バージョンで動作確認しています。Symfony2がバージョンアップすると、動作しなくなる恐れがあります。

Postモデルの作成
----------------

お気づきかと思いますが、まだスキーマ（データベース上のテーブル）を作成していません。
このチュートリアルでは、モデルを定義してから自動的にスキーマを作成する手順を行いたいと思います。
スキーマはその過程で作成されますので、ご安心ください！

Doctrineでは、pure phpのクラスでモデルを定義します。おそらく\ ``src/My/BlogBundle``\ ディレクトリにはまだ\ ``Entity``\ ディレクトリは存在しないと思いますので、ディレクトリを作成し、その中に以下のような\ ``Post.php``\ を作成してください。

.. code-block:: php

    // src/My/BlogBundle/Entity/Post.php
    <?php
    
    namespace My\BlogBundle\Entity;
    
    use Doctrine\ORM\Mapping as ORM;
    
    /**
     * @ORM\Entity
     */
    class Post
    {
        /**
         * @ORM\Id
         * @ORM\Column(type="integer")
         * @ORM\GeneratedValue(strategy="AUTO")
         */
        protected $id;
        
        /**
         * @ORM\Column(type="string", length=255)
         */
        protected $title;
        
        /**
         * @ORM\Column(type="text")
         */
        protected $body;
        
        /**
         * @ORM\Column(type="datetime")
         */
        protected $createdAt;
        
        /**
         * @ORM\Column(type="datetime")
         */
        protected $updatedAt;
    }

.. note::

    Doctrineはphpオブジェクトのための永続的透過性を提供しているので、どんなphpクラスでモデルを定義しても動作します。

.. note::

    symfony 1.x系のDoctrineは\ ``ActiveRecord``\ デザインパターンを元に作られていました。
    モデルクラスがテーブルを表し、ここのインスタンスがテーブルの1つの行を表すような構成でした。
    Symfony2のDoctrine2では\ *ドメイン駆動設計*\ という新しい設計思想を導入したことにより、\ ``ActiveRecord``\ を廃止しました。
    代わりに採用されたのが\ ``Data Mapper``\ と\ ``Unit Of Work``\ パターンです。
    これらのデザインパターンは、マーチン・ファウラーの『エンタープライズ アプリケーションアーキテクチャパターン』に詳しく載っています。

.. note::

    このチュートリアルでは、ORMに限定してモデルを作成しています。
    ODMを考慮した、より抽象的な定義方法を学びたい場合は、
    `FriendsOfSymfony`_ がgithubで提供している `UserBundle`_ や `CommentBundle`_ などのソースコードが参考になります。

Postクラスを見てください。まず、本当はgetter/setterメソッドを書かなくてはいけませんが、省略しています。
代わりにアノテーション形式の設定が書かれていて、各カラムがどんなスキーマなのかを表しています。
Doctrineがこれらのメソッドを自動的に作成するコマンドを提供しているので、使ってみましょう！

.. code-block:: bash

    $ php app/console doctrine:generate:entities MyBlogBundle
    Generating entities for bundle "MyBlogBundle"
      > generating My\BlogBundle\Entity\Post

コマンドが成功すると、\ ``Post.php``\ が書き換えられていて、以下のようなメソッドが追加されています。

.. code-block:: php

    
        /**
         * Get id
         *
         * @return integer $id
         */
        public function getId()
        {
            return $this->id;
        }
        
        /**
         * Set title
         *
         * @param string $title
         */
        public function setTitle($title)
        {
            $this->title = $title;
        }
        
        /**
         * Get title
         *
         * @return string $title
         */
        public function getTitle()
        {
            return $this->title;
        }
        
        /**
         * Set body
         *
         * @param text $body
         */
        public function setBody($body)
        {
            $this->body = $body;
        }
        
        /**
         * Get body
         *
         * @return text $body
         */
        public function getBody()
        {
            return $this->body;
        }
        
        /**
         * Set createdAt
         *
         * @param datetime $createdAt
         */
        public function setCreatedAt($createdAt)
        {
            $this->createdAt = $createdAt;
        }
        
        /**
         * Get createdAt
         *
         * @return datetime $createdAt
         */
        public function getCreatedAt()
        {
            return $this->createdAt;
        }
        
        /**
         * Set updatedAt
         *
         * @param datetime $updatedAt
         */
        public function setUpdatedAt($updatedAt)
        {
            $this->updatedAt = $updatedAt;
        }
        
        /**
         * Get updatedAt
         *
         * @return datetime $updatedAt
         */
        public function getUpdatedAt()
        {
            return $this->updatedAt;
        }

.. note::

    さきほどのPostクラスを書くときに手を抜いてアノテーションのコメントブロックを書かなかった場合は、
    おそらくgetter/setterメソッドは自動生成されていないでしょう。
    ``doctrine:generate:entities``\ コマンドは、 *マッピング情報* がないと動きません。
    
    マッピング情報というのは先ほど書いたアノテーションの事で、YAMLやXMLでも記述することができます。
    例えばsymfony 1.x系に慣れている方は、こう行った情報は１つのファイルにまとめたいと考えるでしょう。
    その場合は、\ ``doctrine.orm.yml``\ という1つのファイルにすべてのマッピング情報を書くこともできます。
    
    マッピング情報の簡単な例が知りたい場合は、\ `Doctrine ORM`_\ を参照してください。


スキーマの作成
--------------

さきほど作成したエンティティを元に、スキーマを作成します。
スキーマの作成は\ ``doctrine:schema:create``\ コマンドで行います。

.. code-block:: bash

    $ php app/console doctrine:schema:create

コンソールには、以下のような出力がなされて、スキーマが作成されたと書かれているでしょう。

.. code-block:: bash

    ATTENTION: This operation should not be executed in an production enviroment.
    
    Creating database schema...
    Database schema created successfully!

phpMyAdminなどのデータベース管理ツールでblogsymfony2データベースを確認してみると、
Postテーブルが作られていて、その中にid、title、body、createdAt、updatedAtの5つのカラムが
作成されていることがわかります。


.. _`FriendsOfSymfony`: https://github.com/FriendsOfSymfony
.. _`UserBundle`: https://github.com/FriendsOfSymfony/UserBundle
.. _`CommentBundle`: https://github.com/FriendsOfSymfony/CommentBundle
.. _`Doctrine ORM`: http://symfony.com/doc/current/book/doctrine/orm.html
