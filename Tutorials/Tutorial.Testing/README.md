Pythonチュートリアル：Python のテストフレームワーク
=================
![](https://gyazo.com/652059fd9995b17f0823497436d456a7.png)


# テストの重要性について
プログラム開発でテストをすることの理由付けには、次のようなことが挙げられます。

- **信頼性向上のため**：　少なくともいくつかのケースが動作するかどうかをチェックしておくと、他の人はそのプログラムの品質をより信頼することができ、開発者たちもより多くの信頼を得られることになります。
- **変更時のデグレードの把握**：　大きなプロジェクトでは、すべての部分を把握しておくことが難しい場合があります。テストを書くことで、何かを変更したときに、その影響で何かが壊れることがあるかを簡単に確認することができます。これは、コードを開発した人だけではなく、まだ開発途中にあるチームメンバーにも役立ちます。
- **コーディングスタイルの改善**：　テストを書かなければならないことがわかっていると、いくつかのものを少し違った形で書くようになります。これらのわずかな意識の違いは、通常、コーディングスタイルの改善されることになります。場合により、それが重要になることもあります。例えば、コードを徹底的にテストしなければならないとわかっていれば、より小さな単位でコードを書くようになります。
- **ドキュメントの作成**：　テストケースの中には、そのコードがどのように使用されるかを少しだけ示すものがあります。

これらの理由から、優秀な開発チーム（あるいは個人）であれば、設計段階でコードの実行を確認するために必要なテストの設計も行われ、本体のコードと同じレベルでテストコードが開発されていくこともあります。
アドホックなテストではなく、十分に設計されたテストは、不具合修正時やバージョンアップ時に設計の追加変更時にも新たなバグ混入を防ぐことができます。コードの品質を担保することになります。

テストフレームワークを利用すると、テスト作業およびテストコードの作成を効率よく行うことができます。


# Python の標準ライブラリによるテスト
Pythonの標準ライブラリには、doctest と unittest と呼ばれる、コードをテストするためのモジュールがあります。

## doctestによるテスト
doctestモジュールは、コードの中でPythonのインタラクティブなセッションに似たテキストを検索します。そして、それらのセッションを実行して、書かれている通りに動作するかどうかを検証します。

- [Pythonのテストツールdoctestを使ってみよう]


## unittest によるテスト
Pythonで利用できるテストフレームはたくさんあります。unitest は Python の標準ライブラリにあるものです。

- [Pythonのテストフレームワーク unittest を使ってみよう]
- [Pythonの関数をタイムアウトさせるときに便利なライブラリ]

## pytest によるテスト
pytest フレームワークは、Python テストの新しい標準を確立し、今日多くの開発者に人気があります。

- [Pythonのテストフレームワークpytestを使ってみよう]

## nose/nose2 によるテスト

- [Pythonのテストフレームワークnose2を使ってみよう]


# DjangoやFlaskなどのWebフレームワークでのテスト
Django や Flask のような人気のあるフレームワークを使ったWebアプリケーションのテストを書く場合、テストの書き方や実行方法にはいくつかの重要な違いがあります。

### 他のアプリケーションとの違い
Webアプリケーションでテストするコードを考えてみましょう。ルート(Route)、ビュー(View)、モデル(Model)のすべてで、多くのインポートされているモジュールと、使用しているフレームワークに関する知識が必要です。

これは、例えば車のテストをすることに似ています。ライトの点灯を確認するような簡単なテストを実行する前に、まず車載コンピュータを起動しなければなりません。

Django と Flask では unittest をベースにしたテストフレームワークを提供することで、これを容易にしています。unittestについて習得したチキ氏で方法でテストを書き続けることができますが、実行方法は少し異なります。

## Django テストランナーの使い方
Django の startapp テンプレートは、アプリケーションディレクトリ内に  `tests.py` ファイルを作成します。まだ存在していない場合は、以下の内容で作成します。

 tests.py
```
 from django.test import TestCase

 class MyTestCase(TestCase):
     # ここにテストコードを書く

```

unittestとの大きな違いは、 `unittest.TestCase` ではなく  `django.test.TestCase` を継承する必要があることです。これらのクラスは同じ API を持っていますが、 Django TestCase クラスはテストに必要な全ての状態を設定します。

テストスイートを実行するには、 unittest コマンドではなく、  `manage.py test` を使います。

 bash
```
 $ python manage.py test

```

複数のテストファイルを作りたい場合は、 `tests.py` を tests というフォルダに置き換え、その中に  `__init__.py` という空のファイルを入れて、  `test_*.py` ファイルを作ります。Django はこれらを読み込んで実行します。

より詳しい情報は  Django の[ドキュメント ](https://docs.djangoproject.com/ja/3.2/topics/testing/overview/#writing-tests) を参照してください。

## unittest と Flask の使い分け
Flask では、アプリをインポートしてからテストモードにする必要があります。テストクライアントをインスタンス化し、そのテストクライアントを使って、アプリケーション内の任意のルートにリクエストを行うことができます。

テストクライアントのインスタンス化はすべて、テストケースの `setUp()` メソッドで行います。次の例では、 `my_app` がアプリケーションの名前です。今の段階では　 `setUp()` が何をするのかわからなくても構いません。

テストファイル内のコードは次のようになります。


```
 import my_app
 import unittest


 class MyTestCase(unittest.TestCase):

     def setUp(self):
         my_app.app.testing = True
         self.app = my_app.app.test_client()

     def test_home(self):
         result = self.app.get('/')
         # アサーションを記述

```

その後、次のコマンドを使用してテストケースを実行することができます。

 bash
```
 $ python -m unittest discover

```

より詳しい情報は、Flaskの [ドキュメン ](https://flask.palletsprojects.com/en/2.0.x/testing/) を参照してください。


# より高度なテストシナリオ
アプリケーションのテストを作成する前に、すべてのテストには次の3つのステップがあることを理解しましょう。

  - 入力の作成
  - コードを実行し、出力を取得する
  - 予想される結果と出力を比較する

文字列や数値のような静的な値を入力するのは、いつも簡単というわけではありません。例えば、アプリケーションがクラスやコンテキストのインスタンスを必要とすることがあります。その時はどうするのでしょうか？

入力として作成したデータを**フィクスチャ(fixture)**と呼びます。フィクスチャを作成して再利用するのが一般的です。

同じテストを実行して、毎回異なる値を渡して、同じ結果を期待する場合、これは**パラメータ化(parameterization)** と呼ばれます。

# アプリケーションの動作の分離
前述しているようにテストに副作用があると、テストを実行するたびに違う結果になったり、さらに悪いことには、あるテストがアプリケーションの状態に影響を与え、別のテストが失敗する原因になったりするので、単体テスト（Unit Test)が難しくなります。

副作用の多いアプリケーションの一部をテストするために、いくつかの簡単なテクニックがあります。

- [単一責任原則（Single responsibility principle） ](https://en.wikipedia.org/wiki/Single_responsibility_principle) に従うようにコードをリファクタリングする。
- 副作用をなくすために、メソッドや関数の呼び出しをmockで処理する。
- アプリケーションの一部を単体テストではなく統合テストでテストする。

# 統合テストの作成
これまでのところ、おもに単体テストについて学んできました。単体テストは、予測可能で安定したコードを構築するための素晴らしい方法です。しかし、最終的には、アプリケーションが起動したときに動作する必要があります。

統合テスト(Integration Test) とは、アプリケーションの複数のコンポーネントをテストし、それらが一緒に動作することを確認することです。統合テストでは、アプリケーションの消費者やユーザーのように行動する必要があるかもしれません。

- HTTP REST APIの呼び出し
- Python APIの呼び出し
- Webサービスの呼び出し
- コマンドラインの実行

これらのタイプの統合テストは、単体テストと同じように、 入力、実行、アサートのパターンで書くことができます。最も大きな違いは、統合テストではより多くのコンポーネントを一度にチェックするため、単体テストよりも多くの副作用が発生することです。また、統合テストでは、データベース、ネットワークソケット、設定ファイルなど、より多くのフィクスチャが必要になります。

このような理由から、単体テストと統合テストを分離することは良い方法です。テスト用のデータベースやテストケースなど、統合に必要なフィクスチャの作成には単体テストよりもはるかに長い時間がかかることが多いので、統合テストはコミットのたびに実行するのではなく、本番環境にプッシュする前にのみ実行するようにしましょう。

単体テストと統合テストを分離する簡単な方法は、次のように、単にそれらを別のフォルダに入れることです。

 bash
```
 project/
 │
 ├── my_app/
 │   └── __init__.py
 │
 └── tests/
     |
     ├── unit/
     |   ├── __init__.py
     |   └── test_sum.py
     |
     └── integration/
         ├── __init__.py
         └── test_integration.py

```

選択したテストのグループだけを実行する方法はたくさんあります。ソース・ディレクトリ指定オプション `-s` は、テストを含むパスを指定してunittest discoverに追加することができます。

 bash
```
 $ python -m pytest discover -s tests/integration

```

unittest は、 `tests/integration` ディレクトリ内のすべてのテストの結果を表示します。

# データ駆動型アプリケーションのテスト
多くの統合テストでは、データベースのようなバックエンドのデータが特定の値で存在することを必要とします。たとえば、データベースに 100 人以上の顧客がいる場合にアプリケーションが正しく表示されるかどうかをチェックするテストや、商品名が日本語で表示されている場合に注文ページが動作するかどうかをチェックするテストなどがあります。

このようなタイプの統合テストは、再現性と予測可能性を確保するために、さまざまなテストフィクスチャに依存します。

良いテクニックとしては、統合テスト用のフォルダの中の  `fixtures` というディレクトリにテストデータを格納し、テストデータが含まれていることを示すことです。そうすれば、テストの中でデータをロードしてテストを実行することができます。

以下は、データがJSONファイルで構成されている場合の構造の例です。

 bash
```
 project/
 │
 ├── my_app/
 │   └── __init__.py
 │
 └── tests/
     |
     └── unit/
     |   ├── __init__.py
     |   └── test_sum.py
     |
     └── integration/
         |
         ├── fixtures/
         |   ├── test_basic.json
         |   └── test_complex.json
         |
         ├── __init__.py
         └── test_integration.py

```

テストケースの中では、 `.setUp()` メソッドを使って、既知のパスにあるフィクスチャファイルからテストデータを読み込み、そのテストデータに対して多くのテストを実行することができます。ひとつの Python ファイルに複数のテストケースを含めることができ、 unittest discovery はその両方を実行することになります。テストデータのセットごとに1つのテストケースを持つことができます。


```
 import unittest


 class TestBasic(unittest.TestCase):
     def setUp(self):
         # Load test data
         self.app = App(database='fixtures/test_basic.json')

     def test_customer_count(self):
         self.assertEqual(len(self.app.customers), 100)

     def test_existence_of_customer(self):
         customer = self.app.get_customer(id=10)
         self.assertEqual(customer.name, "Org XYZ")
         self.assertEqual(customer.address, "10 Red Road, Reading")


 class TestComplexData(unittest.TestCase):
     def setUp(self):
         # load test data
         self.app = App(database='fixtures/test_complex.json')

     def test_customer_count(self):
         self.assertEqual(len(self.app.customers), 10000)

     def test_existence_of_customer(self):
         customer = self.app.get_customer(id=9999)
         self.assertEqual(customer.name, u"バナナ")
         self.assertEqual(customer.address, "10 Red Road, Akihabara, Tokyo")

 if __name__ == '__main__':
     unittest.main()

```

アプリケーションがリモート API などの遠隔地のデータに依存している場合、テストの再現性を確保する必要があります。APIがオフラインであったり、接続に問題があったりしてテストが失敗すると、開発が滞ってしまいます。このような状況では、リモートフィクスチャをローカルに保存して、アプリケーションに呼び出して送信できるようにするのがベストです。

requests ライブラリには responses という無料のパッケージがあり、レスポンスフィクスチャを作成してテストフォルダに保存することができます。詳細はGitHubページをご覧ください。

# tox による複数の環境でのテスト
特定の依存関係のセットを持つ仮想環境を使用して、単一バージョンのPythonに対してテストすることは、それほど難しいものではありません。しかし、オープンソースとしてパッケージをリリースしているような場合では、複数のバージョンのPythonや複数のバージョンのパッケージで動作することを確認する必要でてきます。こうした場合に便利なパッケージが Toxです。
tox は、複数の環境でのテストを自動化するアプリケーションです。

### Toxのインストール
ToxはPyPIにpipでインストールできるパッケージとして公開されています。

 bash
```
 $ pip install tox

```

Toxのインストールが完了したら、次はToxを設定する必要があります。

### Toxの設定と依存関係
Toxの設定は、プロジェクトディレクトリにある設定ファイルで行います。Toxの設定ファイルには、以下の内容が含まれています。

- テストを実行するために実行するコマンド
- 実行する前に必要な追加パッケージ
- テストの対象となるPythonのバージョン

Tox の設定シンタックスを学ぶ代わりに、tox-quickstart アプリケーションを実行することで、先に始めることができます。

 bash
```
 $ tox-quickstart

```

Toxの設定ツールは、いくつかの質問をし回答することで、 `tox.ini` に以下のようなファイルを作成します。

 tox.ini
```
 [tox]
 envlist = py27, py36

 [testenv]
 deps =

 commands =
     python -m unittest discover
```

Toxを実行する前に、アプリケーションフォルダ内に、パッケージをインストールするための手順を記したsetup.pyファイルがあることが必要です。もし、 `setup.py` がない場合は、「[Packaging Python Projects ](https://packaging.python.org/tutorials/packaging-projects/#packaging-python-projects)」のガイドに従って  `setup.py` を作成してから実行してください。

また、あなたのプロジェクトがPyPIで配布されていない場合は、 `tox.ini` ファイルの  `[tox]` 見出しの下に以下の行を追加することで、この要件をスキップすることができます。

 抜粋　tox.ini
```
 [tox]
 envlist = py27, py36
 skipsdist=True

```

 `setup.py` を作成せず、アプリケーションに PyPI からの依存関係がある場合は、 `[testenv]` セクションの下のいくつかの行でそれらを指定する必要があります。例えば、Djangoであれば以下のものが必要です。

 抜粋 tox.ini
```
 [testenv]
 deps = django

```

この段階まで完了すると、テストを実行する準備が整います。

Toxを実行すると、Python 2.7用とPython 3.6用の2つの仮想環境が作成されます。Toxのディレクトリは、 `.tox/` と呼ばれます。 `.tox/` ディレクトリの中で、Toxは各仮想環境に対して  `python -m unittest discover` を実行します。

この処理を実行するには、コマンドラインでToxを呼び出します。

 bash
```
 $ tox

```

Toxは、各環境に対するテストの結果を出力します。初回の実行時には、仮想環境の作成に少し時間がかかりますが、一度作成してしまえば、2回目以降の実行はかなり速くなります。

### Toxの使用方法
Toxの出力は非常に簡単です。各バージョンの環境を作成し、依存ファイルをインストールして、テストコマンドを実行します。

覚えておくと便利な追加のコマンドラインオプションがいくつかあります。

Python 3.6のような単一の環境のみを実行します。

 bash
```
 $ tox -e py36

```

依存関係が変更されたり、site-packagesが破損している場合は、仮想環境を再構築してください。

 bash
```
 $ tox -r

```

tox の出力を少なくしたい場合は、次のように実行します。

 bash
```
 $ tox -q

```

逆に、より詳細な出力でToxを実行しいたい場合は、次のように実行します。

 bash
```
 $ tox -v

```

Toxに関する詳しい情報は、Toxの [ドキュメント ](https://tox.wiki/en/latest/) を参照してください。


# テスト実行の自動化
これまでは、コマンドを実行して手動でのテストを実行について説明してきました。しかし、変更を加えてGitなどのソースコントロールリポジトリにコミットすると、自動的にテストを実行してくれるツールもあります。
自動テストツールは、**CI（Continuous Integration）** / **CD（Continuous Deployment）** として知られています。CI/CDツールは、テストを実行し、アプリケーションをコンパイルして公開し、さらには本番環境にデプロイすることができます。

[Travis CI ](https://travis-ci.org/) は、多くのCI（継続的インテグレーション）サービスの一つです。

Travis CIはPythonと相性がよく、テストをすべて作成した後は、クラウド上でテストの実行を自動化することができます。Travis CIは、GitHubやGitLabで公開されているオープンソースのプロジェクトであれば無料で利用でき、プライベートなプロジェクトであれば有料で利用できます。

始めるには、ウェブサイトにログインし、GitHubまたはGitLabの認証情報で認証します。そして、 `.travis.yml` というファイルを以下の内容で作成します。

 .travis
```
 language: python

   - "2.7"
   - "3.7"
 install:
   - pip install -r requirements.txt
 script:
   - python -m unittest discover

```

この設定はTravis CIに次のことを指示します。

- Python 2.7と3.7でテストする（これらのバージョンを任意のものに置き換えることができます）。
- requirements.txtに記載されている全てのパッケージをインストールする(依存関係がない場合は、このセクションを削除してください)
-  `python -m unittest discover` を実行してテストを行います。

このファイルをコミットしてプッシュすると、Travis CI はリモート Git リポジトリにプッシュするたびにこれらのコマンドを実行します。その結果はウェブサイトで確認できます。


# まとめ
Python には、アプリケーションが設計通りに動作するかどうかを検証するために必要なコマンドやライブラリを組み込んたテストを効率よく簡単に実行できるテストフレームワークがあります。Python のコードを検証するための小さくて保守性の高いメソッドを書くことができます。

はじめは標準ライブラリの　unittest から初めて、テストについて学んでゆき、アプリケーションが成長したら、pytestのような他のテストフレームワークに切り替えて、より高度な機能を活用することもできます。

# 参考
- Python 公式ドキュメント
  - [doctest - 対話的な実行例をテストする  ](https://docs.python.org/ja/3/library/doctest.html#module-doctest)
  - [unittest - ユニットテストフレームワーク ](https://docs.python.org/ja/3/library/unittest.html)
- [テスト駆動開発](https://ja.wikipedia.org/wiki/%E3%83%86%E3%82%B9%E3%83%88%E9%A7%86%E5%8B%95%E9%96%8B%E7%99%BA#:~:text=%E3%83%86%E3%82%B9%E3%83%88%E9%A7%86%E5%8B%95%E9%96%8B%E7%99%BA%20(%E3%81%A6%E3%81%99%E3%81%A8%E3%81%8F%E3%81%A9%E3%81%86,%E6%B4%97%E7%B7%B4%E3%81%95%E3%81%9B%E3%82%8B%E3%80%81%E3%81%A8%E3%81%84%E3%81%86%E7%9F%AD%E3%81%84%E5%B7%A5%E7%A8%8B)
- [A simple example of Python OOP development (with TDD) - Part 1](https://www.thedigitalcatonline.com/blog/2015/05/13/python-oop-tdd-example-part1/)
- [A simple example of Python OOP development (with TDD) - Part 2 ](https://www.thedigitalcatonline.com/blog/2015/09/10/python-oop-tdd-example-part2/)
- [Packaging Python Projects ](https://packaging.python.org/tutorials/packaging-projects/#packaging-python-projects)
- [tox オフィシャルサイト  ](https://tox.wiki/en/latest/#)
- [Travis CI オフィシャルサイト ](https://travis-ci.org/)


