blogチュートリアル(11) まとめと応用
===================================

.. note::

    この記事は、Symfony 2.0.7 で動作確認しています。

プログラムは無事に動きましたでしょうか？
このチュートリアルをマスターできたら、次はどうしますか？

チュートリアルのプログラムを改良してみる
----------------------------------------

このチュートリアルのアプリケーションは非常にシンプルなので、改良の余地がたくさんあります。
必要だと思う機能を追加したり、リファクタリングをしてより高度な機能を使ったりしてみてください。
例えば、以下のような例が考えられます(編注：いずれもチュートリアルの続きとして執筆したい)。

- Twig の継承を使って完全なHTMLを出力する(チュートリアルでは<html>タグがない!!)
- ルーティングで {$id} に数値以外が入らないように制限する
- フォームクラスを分離する
- Doctrine の拡張機能 Timestampable ビヘイビアを使って自動的に createdAt と updatedAt が保存されるようにする
- Repositry クラスを導入して、一覧表示のロジックを別クラスに分離する
- アノテーションで定義している Entity の設定を yaml で定義する
- 記事の追加・編集・削除をした後にflashメッセージを表示する
- 記事の追加・編集・削除アクションにはセキュリティをかける

.. note::

    :doc:`customize/index` にて、カスタマイズ例を紹介しています。

Symfony2 について、詳しく学んでみる
-----------------------------------

Symfony2 には非常にたくさんのドキュメントが揃っています。

- `ガイドブック`_ : Symfony2 のコアチームが作成した Symfony2 のバイブルです。基本的な機能が学べます。
- `クックブック`_ : Symfony2 の逆引き辞典です。
- `Reference Documents`_ : Symfony2 の様々な設定値をまとめたリファレンスです。
- `Glossary`_ : Symfony2 の基本的な用語が簡単に説明されている用語辞典です。
- `ORM Documentation 2.0`_ : Doctrine2 ORM の API 、 Reference 、 Cookbook があります。
- `DBAL Document 2.0`_ : Doctrine2 DBAL の API 、Reference があります。
- `FriendsOfSymfony - GitHub`_ : Symfony2 の精鋭たちがメンテナンスをしているgithubアカウントです。ベストプラクティスの詰まった Bundle が公開されています。

.. _`ガイドブック`: http://docs.symfony.gr.jp/symfony2/book/index.html
.. _`クックブック`: http://docs.symfony.gr.jp/symfony2/cookbook/index.html
.. _`Reference Documents`: http://symfony.com/doc/current/reference/index.html
.. _`Glossary`: http://symfony.com/doc/current/glossary/index.html
.. _`ORM Documentation 2.0`: http://www.doctrine-project.org/projects/orm/2.0/docs/en
.. _`DBAL Document 2.0`: http://www.doctrine-project.org/projects/dbal/2.0/docs/en
.. _`FriendsOfSymfony - GitHub`: https://github.com/FriendsOfSymfony/


