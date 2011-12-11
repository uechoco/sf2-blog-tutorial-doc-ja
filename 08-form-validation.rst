blogチュートリアル(8) データのバリデーション
============================================

.. note::

    この記事は、Symfony 2.0.7 で動作確認しています。


今回は、このフォームにバリデーションルールを設定して、正しくデータが登録できるようにします。

バリデータの設定
----------------

フォームのバリデーションを有効にするには、YAMLやXMLで設定ファイルを記述するか、
アノテーションやPHPコードでモデルに直接記述します。
以前のステップでORMの設定をアノテーションで記述したので、
バリデーションもアノテーションで記述します。

``src/My/BlogBundle/Entity/Post.php`` を開いて、\ ``$title`` と ``$body`` の変数定義箇所を以下のように変更します（\ ``use`` 行を追加していることに注意してください）。

.. code-block:: php

    // src/My/BlogBundle/Entity/Post.php
    use Symfony\Component\Validator\Constraints as Assert;
    
    // ...
    
        /**
         * @ORM\Column(name="title", type="string", length=255)
         * @Assert\NotBlank()
         * @Assert\MinLength(2)
         * @Assert\MaxLength(50)
         */
        protected $title;
    
        /**
         * @ORM\Column(name="body", type="text")
         * @Assert\NotBlank()
         * @Assert\MinLength(10)
         */
        protected $body;
    
    // ...

``Symfony\Component\Validator\Constraints`` 名前空間を ``Assert`` という別名で読み込み、
各バリデーションルールを記述しています。\ ``NotBlank`` や ``MinLength`` など、
バリデーションの意味は文字通りです。
バリデーションに利用できる制約の一覧や詳細は、\ `制約リファレンス`_\ を参照してください。

ブラウザで確認
--------------

再び、記事の追加画面をブラウザで確認してみてください。
今度は、どちらのフォームにも1文字ずつ入れて送信すると、
英語のエラーメッセージが表示されるようになったはずです。

.. note::

    最近のブラウザを使っている人は、フォームタグの ``novalidate`` 属性を削除してみてください。
    データを追加するフォームのタイトルや本文に何も入力しないで送信しようとすると、
    警告がでてくるため、バリデーションが効いているものと思ったことでしょう。
    Formオブジェクトが自動的に HTML5 の ``required`` 属性を出力したためです。
    このようなクライアントサイドフォームバリデーションは便利ですが、Webブラウザが対応していなければ実行されませんので、
    必ずサーバーサイドでのバリデーションも実装するようにしてください。

.. _`制約リファレンス`: http://symfony.com/doc/current/reference/constraints.html
