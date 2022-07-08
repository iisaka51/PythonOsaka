kamidanaを使ってみよう
=================
## kamidana について
[kamidana ](https://github.com/podhmo/kamidana) は Jinja2 のCLIツールです。

次のような機能があります。
- jinja2ファイルをテンプレートファイルとして使用
- さまざまな入力形式のサポート（json、yaml、tomlなど）
- 親テンプレートパスに関連したルックアップテンプレートの方法が変更された
- 穏やかなエラーメッセージ
- スピードアップのためのバッチ実行（kamidana-batch経由）
- 個々のフィルターを使用したレンダリング（オプション `--additionals` を使用）
- 便利な追加モジュール（例：kamidana.additionals.naming ...）

プロジェクトにテンプレートエンジンを利用するときに、テンプレートファイル単独で作成やテストができると、工程の依存関係が小さくなり作業効率がよくなります。
そうしたときに、CLIツールがあると便利になるわけです。

開発者のpodhmo氏がブログで[コメント ](https://pod.hatenablog.com/entry/2017/05/13/195233)していますが、Jinja2 のCLIツールには j2cli ほか多數の変種があります。
> podhmo氏のブログからの引用
>何でj2cliを使わないのかというと、以下の様な理由。
>	j2cliのforkがいっぱいあってカオス
>	(一番star数が多いforkは)python3.xに対応していない
>	おもったよりも機能が多くない
>	(正直そんなに良いコードに見えない)
>	(init.pyで import pkg_resources とかつらい)
>そんなわけで自分用の物を作り始めた。

### インストール
kamidana は次のようにインストールすることができます。
 bash
```
 $ pip install kanidana
```

## 使用方法
 bash
```
 $ kamidana --help
 usage: kamidana [-h] [--driver DRIVER] [--loader LOADER] [-d DATA]
                 [--logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}]
                 [-a ADDITIONALS] [-e EXTENSION]
                 [-i {yaml,json,toml,csv,tsv,raw,env,md,markdown,spreadsheet}]
                 [-o OUTPUT_FORMAT] [--dump-context] [--list-info] [--debug]
                 [--quiet] [--dst DST]
                 [template]
 
 positional arguments:
   template
 
 optional arguments:
   -h, --help            show this help message and exit
   --driver DRIVER       default: kamidana.driver:Driver
   --loader LOADER       default: kamidana.loader:TemplateLoader
   -d DATA, --data DATA  support yaml, json, toml
   --logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}
   -a ADDITIONALS, --additionals ADDITIONALS
   -e EXTENSION, --extension EXTENSION
   -i {yaml,json,toml,csv,tsv,raw,env,md,markdown,spreadsheet}, --input-format {yaml,json,toml,csv,tsv,raw,env,md,markdown,spreadsheet}
   -o OUTPUT_FORMAT, --output-format OUTPUT_FORMAT
   --dump-context        dumping loading data (used by jinja2 template)
                   [-o OUTPUT_FORMAT] [--dump-context] [--list-info] [--debug]
                   [--quiet] [--dst DST]
                   [template]
   
   positional arguments:
     template
   
   optional arguments:
     -h, --help            show this help message and exit
     --driver DRIVER       default: kamidana.driver:Driver
     --loader LOADER       default: kamidana.loader:TemplateLoader
     -d DATA, --data DATA  support yaml, json, toml
     --logging {CRITICAL,FATAL,ERROR,WARN,WARNING,INFO,DEBUG,NOTSET}
     -a ADDITIONALS, --additionals ADDITIONALS
     -e EXTENSION, --extension EXTENSION
     -i {yaml,json,toml,csv,tsv,raw,env,md,markdown,spreadsheet}, --input-format {yaml,json,toml,csv,tsv,raw,env,md,markdown,spreadsheet}
     -o OUTPUT_FORMAT, --output-format OUTPUT_FORMAT
     --dump-context        dumping loading data (used by jinja2 template)
     --list-info           listting information (for available extensions and
                           additional modules)
     --debug
     --quiet
     --dst DST
```




