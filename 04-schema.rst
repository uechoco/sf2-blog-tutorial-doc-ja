blogチュートリアル(4) テーブルスキーマとエンティティクラス
==========================================================

.. note::

    この記事は、Symfony 2.0.0 で動作確認しています。Symfony2がバージョンアップすると、動作しなくなる恐れがあります。

Postモデルの作成
----------------

お気づきかと思いますが、まだスキーマ(データベース上のテーブル)を作成していません。
このチュートリアルでは、\ *エンティティ* と呼ばれるスキーマ定義ファイルを定義してから自動的にスキーマを作成する手順で行いたいと思います。

Doctrineでは、pure phpのクラスでスキーマを定義します。\ ``generate:doctrine:entity`` コマンドでエンティティファイルを自動生成します。
コマンドの実行中に４〜５個の質問項目がありますが、すべての項目でエンターを入力してください。

.. code-block:: bash 

    $ php app/console generate:doctrine:entity --entity=MyBlogBundle:Post --format=annotation --fields="title:string(255) body:text createdAt:datetime updatedAt:datetime"

次のようなコマンドの実行メッセージになります:

.. code-block:: none

                                                     
          Welcome to the Doctrine2 entity generator  
                                                     
        
        
        This command helps you generate Doctrine2 entities.
        
        First, you need to give the entity name you want to generate.
        You must use the shortcut notation like AcmeBlogBundle:Post.
        
        The Entity shortcut name [MyBlogBundle:Post]: 
        
        Determine the format to use for the mapping information.
        
        Configuration format (yml, xml, php, or annotation) [annotation]: 
        
        Instead of starting with a blank entity, you can add some fields now.
        Note that the primary key will be added automatically (named id).
        
        Available types: array, object, boolean, integer, smallint, 
        bigint, string, text, datetime, datetimetz, date, time, decimal, float.
        
        New field name (press <return> to stop adding fields): 
        
        Do you want to generate an empty repository class [no]? 
        
                                     
          Summary before generation  
                                     
        
        You are going to generate a "MyBlogBundle:Post" Doctrine2 entity
        using the "annotation" format.
        
        Do you confirm generation [yes]? 
        
                             
          Entity generation  
                             
        
        Generating the entity code: OK
        
                                                       
          You can now start using the generated code!  
                                                       

``generate:doctrine:entity`` コマンドによって、\ ``src/My/BlogBundle/Entity/`` ディレクトリが作成され、その中に次のような ``Post.php`` が生成されます:

.. code-block:: php

    <?php
    
    namespace My\BlogBundle\Entity;
    
    use Doctrine\ORM\Mapping as ORM;
    
    /**
     * My\BlogBundle\Entity\Post
     *
     * @ORM\Table()
     * @ORM\Entity
     */
    class Post
    {
        /**
         * @var integer $id
         *
         * @ORM\Column(name="id", type="integer")
         * @ORM\Id
         * @ORM\GeneratedValue(strategy="AUTO")
         */
        private $id;
    
        /**
         * @var string $title
         *
         * @ORM\Column(name="title", type="string", length=255)
         */
        private $title;
    
        /**
         * @var text $body
         *
         * @ORM\Column(name="body", type="text")
         */
        private $body;
    
        /**
         * @var datetime $createdAt
         *
         * @ORM\Column(name="createdAt", type="datetime")
         */
        private $createdAt;
    
        /**
         * @var datetime $updatedAt
         *
         * @ORM\Column(name="updatedAt", type="datetime")
         */
        private $updatedAt;
    
    
        /**
         * Get id
         *
         * @return integer 
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
         * @return string 
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
         * @return text 
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
         * @return datetime 
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
         * @return datetime 
         */
        public function getUpdatedAt()
        {
            return $this->updatedAt;
        }
    }

.. note::

    DoctrineはPHPオブジェクトのための透過的永続性を提供しているので、どんなPHPクラスでモデルを定義しても動作します。

.. note::

    symfony 1.x 系のDoctrine は ``ActiveRecord`` デザインパターンを元に作られていました。
    モデルクラスがテーブルを表し、ここのインスタンスがテーブルの1つの行を表すような構成でした。
    Symfony2 の Doctrine2 では\ *ドメイン駆動設計*\ という新しい設計思想を導入したことにより、\ ``ActiveRecord``\ を廃止しました。
    代わりに採用されたのが\ ``Data Mapper``\ と\ ``Unit Of Work``\ パターンです。
    これらのデザインパターンは、マーチン・ファウラーの『エンタープライズ アプリケーションアーキテクチャパターン』に詳しく載っています。

.. note::

    このチュートリアルでは、ORMに限定してモデルを作成しています。
    ODMを考慮した、より抽象的な定義方法を学びたい場合は、
    `FriendsOfSymfony`_ がgithubで提供している `UserBundle`_ や `CommentBundle`_ などのソースコードが参考になります。

Postクラスを見てください。コマンドで指定したカラムとその getter/setter メソッドが作成されています。


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

phpMyAdmin などのデータベース管理ツールで blogsymfony2 データベースを確認してみると、
Post テーブルが作られていて、その中にid、title、body、createdAt、updatedAtの5つのカラムが
作成されていることがわかります。


.. _`FriendsOfSymfony`: https://github.com/FriendsOfSymfony
.. _`UserBundle`: https://github.com/FriendsOfSymfony/UserBundle
.. _`CommentBundle`: https://github.com/FriendsOfSymfony/CommentBundle
.. _`Doctrine ORM`: http://symfony.com/doc/current/book/doctrine/orm.html
