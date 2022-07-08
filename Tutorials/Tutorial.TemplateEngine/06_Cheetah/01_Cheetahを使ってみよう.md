Cheetahを使ってみよう
=================
## Cheetahについて
[Cheetah](https://cheetahtemplate.org/])は、その名のとおり、高速で柔軟性があり、強力な、テンプレートエンジンおよびコード生成ツールです。 Cheetahは、Pythonからの利用に限定されているわけではなく、単独で使用することも、他のテクノロジーやスタックに組み込むこともできます。

Cheetahは、マークアップの生成とテンプレート化のためのドメイン固有言語を提供していて、既存のPythonコードとの完全な統合を可能にするだけでなく、従来のPython構文の拡張機能を提供してテキスト生成を容易にしてくれます。

Cheetah は Python2.x系で動作するもので、Cheetah3 はCheetah をフォークしてPython3.x向けに開発されています。ここでは、Cheetah3 を単に Cheetah と呼ぶことにします。

### Cheetah の利点
- すべての主要なPythonWebフレームワークでサポートされています
- 完全なドキュメント：アクティブなユーザーコミュニティによって保守されています
- 任意のテキストベースの形式を出力/生成できます
- テンプレートを最適化された、しかも読みやすいPythonコードにコンパイルできます
- Pythonのパワーと柔軟性を、シンプルなテンプレート言語と融合させています
  - プログラマー以外の人が理解が容易になります
- テンプレート内のPythonの全てに完全にアクセスできます
  - データ構造、モジュール、関数、オブジェクト、またはメソッド
  - 管理者が必要に応じてPythonへのアクセスを選択的に制限することもできます
- テンプレートの再利用が簡単
  - Pythonコードまたは他のCheetahテンプレートからアクセスできるテンプレートへのオブジェクト指向インターフェースを提供するすることで、コードの再利用を容易にしています
  - 1つのテンプレートで別のテンプレートをサブクラス化し、そのセクションを選択的に再実装できます。
  - Cheetahテンプレートは、任意のPythonクラスのサブクラスにすることができ、その逆も可能です
- シンプルでありながら強力なキャッシュメカニズムを提供します。
  - 動的なWebサイトのパフォーマンスを劇的に向上させることができます。
- 付属のコマンドラインツールを介して静的HTMLファイルを生成することができます。

Cheetahを利用すると、コンテンツ、グラフィックデザイン、およびプログラムコードを明確に分離することができます。これにより、高度にモジュール化され、柔軟性がある、再利用可能なサイトアーキテクチャ、開発時間の短縮、理解と保守が容易なHTMLおよびプログラムコードが実現します。特にチームでの作業に適しています。

## インストール
Cheetah のインストールは次のように行います。

```
 # Linux or Mac
 $ python -m pip install cheetah3

 # Windwos
 $ py -3 -m pip install cheetah3
```

## 利用方法
### コマンドラインツール
Cheetah はコマンドラインツール cheetah を利用することができます。

```
 % cheetah --help
          __  ____________  __
          \ \/            \/ /
           \/    *   *     \/    CHEETAH 3.2.6 Command-Line Tool
            \      |       /
             \  ==----==  /      by Tavis Rudd <tavis@damnsimple.com>
              \__________/       and Mike Orr <sluggoster@gmail.com>

 USAGE:
 ------
   cheetah compile [options] [FILES ...]     : Compile template definitions
   cheetah fill [options] [FILES ...]        : Fill template definitions
   cheetah help                              : Print this help message
   cheetah options                           : Print options help message
   cheetah test [options]                    : Run Cheetah's regression tests
                                             : (same as for unittest)
   cheetah version                           : Print Cheetah version number

 You may abbreviate the command to the first letter; e.g., 'h' == 'help'.
 If FILES is a single "-", read standard input and write standard output.
 Run "cheetah options" for the list of valid options.
```

cheetah コマンドを使うことで、python スクリプトを記述することなく単独でテンプレートファイルを作成、編集、デバッグを行うことができます。

次の例は、いくつかのCheetahコードの簡単な例です。

 cheetah_sample.py
```
 #from Cheetah.Template import Template
 #extends Template

 #set $people = [{'name' : 'Tom', 'mood' : 'Happy'}, {'name' : 'Dick',
                         'mood' : 'Sad'}, {'name' : 'Harry', 'mood' : 'Hairy'}]

 <strong>How are you feeling?</strong>
 <ul>
     #for $person in $people
         <li>
             $person['name'] is $person['mood']
         </li>
     #end for
 </ul>
```

Cheetah は実際にはPythonであることが理解できるはずです。Cheetahテンプレートがコンパイルされると、通常のPythonモジュールと同じように、メソッドをインポート、継承、および定義することができます。


このファイルを cheetah コマンドで処理してみましょう。

```
 % cheetah fill cheetah_sample.py
 Filling cheetah_sample.py -> cheetah_sample.py.html
```

生成されたファイル  `cheetah_sample.py.html` は次のようになります。

```
 <strong>How are you feeling?</strong>
 <ul>
         <li>
             Tom is Happy
         </li>
         <li>
             Dick is Sad
         </li>
         <li>
             Harry is Hairy
         </li>
 </ul>
```

## Cheetahタグ
Cheetahは、次の理由により、他のテンプレート言語のようにHTML / XMLスタイルのタグを使用しません。
- CheetahはHTMLに限定されない
- HTMLスタイルのタグは実際のHTMLタグと区別するのが難しい
HTMLスタイルのタグはレンダリングされたHTMLに表示されない何か問題が発生すると、HTMLスタイルのタグは無効なHTMLにつながることがよくあります。
例： `<img src="<template-directive>">`

Cheetahタグは、HTMLスタイルのタグやHTMLスタイルよりも冗長性が低く、理解しやすいものです。タグはほとんどのWYSIWYGエディターと互換性がありません

Cheetahは、はるかにコンパクトであることに加えて、ZopePageTemplate(ZPT)やPHPなどのHTMLタグ内に情報を配置する言語に比べていくつかの利点があります。
HTMLまたはXMLにバインドされた言語は他の言語ではうまく機能しませんが、ZPTのような構文はうまく機能します。ほとんどのWYSIWYG HTMLエディターでドキュメントの編集の結果をうまく表示することができません。理由は、テンプレートで記述されるロジックが、HTMLエディタが理解できないタグを伴っているためと、そのロジックを確認や変更するためには、ページを表示するだけで困難だからです。

## 言語構成一覧
#### コメントとドキュメント文字列
-  `{## １行のコメント}`
-  `{#* 複数行のコメント *#}`

#### 出力の生成、キャッシュ、フィルタリング
- プレーンテキスト
- 値を検索して置換： `{$placeholder}`
- 式を評価して置換： `{# 式}`
- 出力を破棄しま： `{# silent}`
- 1行での条件分岐： `{# if EXPR then EXPR else EXPR}`
- EOLまでの文字列を捨て去る： `{# slurp}`
- 解析されたファイルを読み込む： `{# include}`
- ファイルをそのまま読み込む： `{# includeraw}`
- Cheetahコードの逐語的な出力： `{# raw} ... {# endraw}`
- 変数のキャッシュ： `{$ *var}` 、`{$ *<interval> *var}`
- キャッシュされた領域： `{# cache} ... {# endcache}`
- 出力フィルターを設定します： `{# filter}`
- 制御出力インデント： `{# indent}` …（まだ実装されていません）
- Pythonモジュールとオブジェクトのインポート： `{# import}` 、 `{# from}`

#### 継承
- 継承する基本クラスを設定： `{# extends}`
- 実装するメインメソッドの名前を設定： `{# implements}`
- コンパイル時の宣言
- クラス属性を定義します： `{# attr}`
- クラスメソッドを定義： `{# def} ... {# enddef}`
 `{#block} ... {#endblock}` は、`{# def} ... {# enddef}`への簡略化されたインターフェイスを提供します

#### 実行時の割り当て
- ローカル変数： `{# set}`
- グローバル変数： `{# setglobal}`
- ローカル変数の削除： `{# del}`

#### フロー制御
-  `{# if} ... {# endif}`
-  `{# if} ... {# else} ... {# elseif} ... {# endif}`
-  `{# if} ... {# else} ... {# elif} ... {# endif}`
-  `{# unless} ... {# endunless}`
-  `{# for} ... {# endfor}`
-  `{# repeat} ... {# endrepeat}`
-  `{# while} ... {# endwhile}`
-  `{# break}`
-  `{# continue}`
-  `{# pass}`
-  `{# stop}`

#### エラー/例外処理
-  `{# assert}`
-  `{# raise}`
-  `{# try} ... {# except} ... {# else} ... {# endtry}`
-  `{# try} ... {# finally} ... {# endtry}`
-  `{# errorCatcher}`
-  `{# errorCatcher}` `$placeholder 呼び出しによって発生した例外のハンドラーを設定

#### パーサー/コンパイラーへの指示
-  `{# breakpoint}`
-  `{# compiler-settings} ... {# endcompiler-settings}`

#### 純粋なPythonコードへのエスケープ
- 式を評価した結果を出力します： `{<%=} ... {%>}`
- コードを実行して出力を破棄します： `{<%} ... {%>}`

#### Cheetahで生成されたPythonモジュールを細かく制御
- コンパイルされたテンプレートのエンコーディングを設定： `{# encoding}`
- コンパイルされたテンプレートモジュールのShBang行( `#!` )を設定：`{# shBang}`


