blogチュートリアル
==================

.. note::

    この記事は、Symfony 2.0.7 で動作確認しています。

はじめに
--------

このチュートリアルでは、CakePHPの `CakePHPブログチュートリアル`_ や 日本Symfonyユーザ会の `Symfony Blogチュートリアル`_ とほぼ同じ成果物（シンプルなブログアプリケーション）を、Symfony2で構築します。Symfony2をダウンロードしてインストールし、データベースの設定を行い、ブログの投稿記事の一覧表示、追加、編集、削除などのアプリケーションロジックを作成します。

このチュートリアルを学ぶと、Symfony2を使った初歩的な開発サイクルを学べると同時に、CakePHPやSymfony 1.x系との比較を行うこともできます。

準備しておく環境や知識
----------------------

#. 動作しているWebサーバ。Apacheを使用している前提で書いてありますので、Apacheの基本的な設定に関する知識が必要です。
#. 動作しているデータベースサーバ。MySQLを使用する前提で書いてあります。必要によってphpMyAdminなどのデータベース管理ツールなどを導入してください。
#. PHPやオブジェクト指向プログラミングの基本的な知識。Symfony2ではPHP 5.3から導入された\ *名前空間*\ や\ *クロージャ*\  、\ *静的遅延束縛*\ などの機能を活用しています。所々で解説をしますが、事前に学んでおくと非常に有利です。（参考：\ `PHP 5.3の新機能`_\ ）

それでは、はじめましょう！

.. toctree::
    :maxdepth: 1

    01-introduction
    02-create-database
    03-create-bundle
    04-schema
    05-list-page
    06-create-template
    07-create-form
    08-form-validation
    09-delete-post
    10-edit-post
    11-next-step
    customize/index

.. _`CakePHPブログチュートリアル`: http://book.cakephp.org/ja/view/219/Blog
.. _`Symfony Blogチュートリアル`: http://symfony.gr.jp/docs/for-beginners/blog-tutorial/
.. _`PHP 5.3の新機能`: http://jp.php.net/manual/ja/migration53.new-features.php
