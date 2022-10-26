Pythonチュートリアル：テンプレートエンジン
=================

![](https://github.com/iisaka51/PythonOsaka/blob/main/data/images/Python_Logo.png)


## テンプレートエンジンについて
テンプレートエンジンは、テンプレートと呼ばれる雛形にデータを渡すとドキュメントを生成するものです。Python で利用されているテンプレートエンジンも多数あります。

 - [テンプレートエンジンを選定する](01_Choice_TemplateEngine.md)

テンプレートエンジンは、次のように大きく分類できます。

- Webアプリケーションの開発を意識したXML系テンプレートエンジン
- Web以外のドキュメントを生成することを意識した多用途テンプレートエンジン

ここでは、次の多用途テンプレートエンジンについて説明することにします。

- Jinja2：Django Template に触発されて開発。Ansibleなど多数のプロジェクトで採用
- Mako：高速で軽量なテンプレートエンジン
- Cheetah：多用途向けの高速なテンプレートエンジン

Jinja2 と Mako は、機能の多くに重複するものがあるため、初心者の場合、どちらを選択するかによって、テンプレート言語としてのフォーマットスタイルが決まることになります。
また、適用するプロジェクトがWebアプリケーションであれば、使用するフレームワークによって必然的に採用するテンプレートエンジンの選択肢が限定されることになります。


## Jinja2
Jinja2は、テンプレートをバイトコードにコンパイルし、HTMLエスケープ、サンドボックス化、テンプレート継承、テンプレートの一部をサンドボックス化する機能などの機能を備えています。 そのユーザーには、Mozilla、SourceForge、NPR、Instagramなどがあります。
ドキュメントも充実しています。
テンプレート内のロジックには独自の構文を使用します。

- [Jinja2を使ってみよう](02_Jinja2/)
- [jinja2-cliを使ってみよう](03_Jinja2_Cli.md)
- [kamidanaを使ってみよう](04_Kamidana.md)

## Mako
Pythonで実装されたオープンソースのテンプレートエンジンです。Jinja2がDjango Templateに触発されてその互換性を意識して設計されているのに対して、Makoは高速パフォーマンスを実現するように設計されています。
テンプレート内のロジックにはPythonコードをインラインで使用します。
データベースマイグレーションツール [alembic ](https://alembic.sqlalchemy.org/en/latest/) でもマイグレーションファイルの生成のために使用されています。


- [makoを使ってみよう](01_makoを使ってみよう.md)
- [mako:構文](02_mako:構文.md)
- [mako:タグ](03_mako:タグ.md)
- [mako:DefとBlock](04_mako:DefとBlock.md)
- [mako:フィルタ](05_mako:フィルタ.md)
- [mako:テンプレートの継承](06_mako:テンプレートの継承.md)
- [mako:キャッシュ](07_mako:キャッシュ.md)

## Cheetah
[Cheetah ](https://cheetahtemplate.org/)は、その名のとおり、高速で柔軟性があり、強力な、テンプレートエンジンおよびコード生成ツールです。 Cheetahは、Pythonからの利用に限定されているわけではなく、単独で使用することも、他のテクノロジーやスタックに組み込むこともできます。

Cheetahは、マークアップの生成とテンプレート化のためのドメイン固有言語を提供していて、既存のPythonコードとの完全な統合を可能にするだけでなく、従来のPython構文の拡張機能を提供してテキスト生成を容易にしてくれます。

- [Cheetahを使ってみよう](06_Cheetah/01_Cheetahを使ってみよう.md)
- [Cheetah:構文](06_Cheetah/02_Cheetah:構文.md)
- [Cheetah:ディレクティブ](06_Cheetah/03_Cheetah:ディレクティブ.md)
- [Cheetah:キャッシュとフィルター](06_Cheetah/04_Cheetah:キャッシュとフィルター.md)
- [Cheetah:テンプレートファイルのデバッグ](06_Cheetah/05_Cheetah:テンプレートファイ
ルのデバッグ.md)

## 参考
- [Jinja オフィシャルサイト http://jinja.pocoo.org/]
- [Cheetah オフィシャルサイト ](https://cheetahtemplate.org/)
- [Mako オフィシャルサイト ](https://www.makotemplates.org/)
