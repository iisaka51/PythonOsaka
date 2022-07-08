タスクランナーdoitを使ってみよう
=================
![](https://gyazo.com/cbac6096bece30e62c3602266f0ca70f.png)

## doit について
doit は Python で実装された、タスクを簡単に定義することができ、プロジェクトに関連するすべてのタスクを、使いやすく、発見しやすい方法で統一して整理することができるツールです。

次のような’特徴があります。

- doitは、あらゆる種類のタスクを実行するビルドツールとして使うというアイデアから生まれました。doitは、アドホックなタスクを簡単に定義できるシンプルなタスクランナーとして使用することができ、プロジェクトに関連するすべてのタスクを使いやすく、発見しやすい方法で整理することができます。
- doitは、ビルドツールのような効率的な実行モデルでスケールアップします。doitは、有向非巡回グラフ(DAG: Direct Acyclic Graph)を作成し、タスクの結果をキャッシュすることができます。必要なタスクのみが正しい順序で実行されることを保証します。
- タスクの結果をキャッシュするためのチェックは、依存関係にあるファイルの変更に限定されません。また、「ターゲット」ファイルも必要ありません。そのため、従来のビルドツールでは対応できなかったワークフローの処理にも適しています。
- タスクの依存関係や作成は、実行中に動的に行うことができ、複雑なワークフローやパイプラインの駆動に適しています。
- doitは、拡張可能なコマンド、カスタム出力、ストレージバックエンド、「タスクローダー」を可能にするプラグインアーキテクチャで構築されています。また、ユーザーがdoitの機能をフレームワークのように活用して新しいアプリケーションやツールを作成できるAPIも提供しています。
- doitは、10年以上にわたって活発に開発されている成熟したプロジェクトです。並列実行、自動実行（ファイルの変更を監視）、シェルのタブコンプリート、DAGの視覚化、IPythonとの統合など、いくつかの機能があります。


## インストール

doit は pip コマンドで次のようにインストールできます。

 zsh
```
 $ pip install 
```

## doit の使用例
doitがタスクの自動化に役立つ使用例のいくつかをご紹介します。

### 煩雑なコマンドラインの呼び出しを簡素化
次のような入力が面倒で複雑なコマンドを繰り返し呼び出す必要があるとします。

 zsh
```
 % aws s3 sync _built/html s3://buck/et --exclude "*" --include "*.html"
```

このコマンド実行を  `dodo.py` として doit でラップします。
例示のためなので、echo コマンドとして記述しています。

 dodo.py
```
 def task_publish():
   """Publish to AWS S3"""
   return {
     "actions": [
         'echo aws s3 sync _built/html s3://buck/et --exclude "*" --include "*.html"'
     ]
   }
```

以降は、単に次のように実行するだけになります。

 bvsh
```
 $ doit publish
```

これにより、doit は カレントディレクトリにある  `dodo.py` （このファイル名がデフォルト)を読み込んで、コマンドライン引数で’与えた  `publish` から  `task_publish()` 関数を探して実行します。

 `doit list` と実行すると、タスク一覧を表示します。

 zsh
```
 % doit list
 publish   Publish to AWS S3
```

複数のアクションを1つのタスクにまとめたり、複数のタスクを使用することも簡単です。

### プロジェクトに関連する典型的なアクションの自動化
コードのリント、テストスイートの実行、カバレッジの評価、スペルを含むドキュメントの作成などが必要になる場合が多いはずです。

やらなければならないタスクを dodo.py に追加で定義するようにしましょう。

### 統一された方法の共有
例えば、リポジトリにコードの変更をコミットするときに、同僚が自分と同じ手順を踏んでくれるでしょうか？　その手順が複雑すぎると言われたら、どうしますか？

そうした場合は、手順を実行する  `dodo.py` ファイルを提供しましょう。簡単なことであれば、使ってもらえる可能性が高くなります。

dodo.pyは、ベスト・プラクティスの使いやすい処方箋となるでしょう。

### すでに実行済みの作業をスキップして処理時間を最適化する
例えば、データベースをダンプした出力から、データをCSVに変換するとします。ダンプに数分程度かかりますが、多くの場合内容は以前と同じです。すでに終わっていることを、なぜ待つのでしょうか？

変換を doit タスクに組み込むと、doit は自動的に入力と出力が同期していることを検知し、可能な限り1秒以内に完了します。

### 複雑なタスクの管理
コーディングしたシステムでは、相互に依存する多くの小さなアクションを行わなければならないとします。
それを小さなタスクに分割し、ファイルの依存関係を定義し、何を最初に処理し、何を次に処理するかの計画をdoitに任せます。
この方法は、クリーンで小さなタスクを組み合わせたものになるでしょう。

### タスクの並列実行による高速化
すでにたくさんのタスクが定義されていて、結果は正しく、時間だけがかかっています。しかし、マルチコア・マシンがあるではありませんか。こうしたときは、doit に並列処理をさせましょう。
例えば４並列で処理させたいときは次のようにコマンドを実行します。

 zsh
```
 % doit -n 4
```

doitがタスク実行の計画を立てて、並列処理を行ってくれます。
処理を書き直す必要はありません。適切に宣言されたタスクを用意するだけです。

### doitの機能でプロジェクトを拡張
あなたのPythonプロジェクトにはdoitの機能が必要ですが、ユーザーにコマンドラインでdoitを呼んでもらうことはできないかもしれません。そうしたときは、自分のコマンドラインツールにdoitの機能を統合することができます。誰も doit の存在を気づかないでしょう。

### クロスプラットフォームの処理ツールを作る
チームメンバーがMS Windowsで作業していたり、Linuxで作業していたりすることはよくあります。
シェル・スクリプトは素晴らしいものですが、BashやZsh などシェルの違いや、同じシェルでもバージョン間の小さな差異が単一の再利用可能なソリューションを妨げていることも多いものです。

dodo.py と python を使えば、クロスプラットフォームな方法で処理を記述できる可能性が高くなります。pathlib.Pathとshutilsの機能を使って、ディレクトリの作成、ファイルの移動、コピーなどを行うことができます。


## doit の実行方法

### dodo.py を実行する
dodo ファイルが　dodo.py としてカレントディレクトリに存在しているときは、単純に doit を実行するだけです。
doitがパラメータなしで実行されると、カレントフォルダー内のdodo.pyというファイルの中からタスクを探し、そのタスクを実行します。

 zsh
```
 % ls dodo.py
 dodo.py
 % doit list
 publish   Publish to AWS S3
 
```

### dodo.py 以外のファイルを実行
もし、 `dodo.py` 以外のファイル名を使用したい場合は、次のように doit を実行します。

 zsh
```
 % mv dodo.py 01_aws_sync.py
 % doit -f 01_aws_sync.py list
 publish   Publish to AWS S3
 
```


### python から実行

doit コマンドを起動するのではなく、python からdoit モジュールをロードしても実行することができます。
zsh
```
 % python -m doit -f 01_aws_sync.py list
 publish   Publish to AWS S3
 
```

### dodoファイルから実行
Linux系プラットフォームでは、dodo ファイルを次のように記述することで、dodo ファイルを直接実行して doit を呼び出すことができます。

 01_aws_sync_cmd.py
```
 #!/usr/bin/env doit -f
 
 def task_publish():
   """Publish to AWS S3"""
   return {
     "actions": [
         'echo aws s3 sync _built/html s3://buck/et --exclude "*" --include "*.html"'
     ]
   }
   
```

 zsh
```
 % chmod u+x 01_aws_sync_cmd.py
 % ./01_aws_sync_cmd.py list
 publish   Publish to AWS S3
```

### APIから起動

 01_aws_sync_api.py
```
 def task_publish():
   """Publish to AWS S3"""
   return {
     "actions": [
         'echo aws s3 sync _built/html s3://buck/et --exclude "*" --include "*.html"'
     ]
   }
 
 if __name__ == '__main__':
     import doit
     doit.run(globals())
```

zsh
```
 % python 01_aws_sync_api.py list
 publish   Publish to AWS S3
 
```

### API+dodoファイル 

dodoファイルから直接 doit を呼び出す方法と似ていますが、この場合は python を呼び出して API から doit を実行する方法です。
ユーザから見ると単純にコマンドのように見えます。

 01_aws_sync_api_cmd.py
```
 #!/usr/bin/env python
 
 def task_publish():
   """Publish to AWS S3"""
   return {
     "actions": [
         'echo aws s3 sync _built/html s3://buck/et --exclude "*" --include "*.html"'
     ]
   }
 
 if __name__ == '__main__':
     import doit
     doit.run(globals())
```

 zsh
```
 % chmod u+x 01_aws_sync_api_cmd.py
 % ./01_aws_sync_api_cmd.py list
 publish   Publish to AWS S3
 
```

詳しくは後述しますが、Jupyterlab / Jupyter notebook からもマジックコマンド  `%doit` を使って利用することができます。



## タスク
doitは、タスクの依存関係の管理と実行を自動化するためのものです。タスクは外部のシェルコマンドやスクリプト、Python関数（実際には任意の呼び出し可能なもの）を実行できます。つまり、タスクはあなたがコード化できるものなら何でも構いません。

タスクは、いくつかの規則に基づいて Python のモジュールとして定義されます。

 `task_` という名前で始まる関数は、doitが認識するタスククリエータを定義します。これらの関数は、タスクを表す辞書を返さなければなりません。または辞書を返すジェネレータとして定義します。doit のタスクを定義する python モジュールのファイルは dodo file と呼ばれます。これは、make コマンドの Makefile のようなものです。

次の例を見てみましょう。

 02_hello.py
```
 def task_hello():
     """hello"""
 
     def python_hello(targets):
         with open(targets[0], "a") as output:
             output.write("Python says Hello World!!!\n")
 
     return {
         'actions': [python_hello],
         'targets': ["hello.txt"],
         }
 
```





 zsh
```
 % doit -f 02_hello.py
 .  hello
 
 % cat hello.txt

 
```

出力には、どのタスクが実行されたかが表示されます。

## アクション
すべてのタスクはアクション( `actions` )を定義しなければなりません。オプションで、 `targets` 、 `file_dep` 、 `verbosity` 、 `doc` などいくつかの属性も定義することができます。

アクションはタスクが実際に行うことを定義します。アクションは常にリストであり、任意の数の要素を持つことができます。タスクのアクションは常に連続して実行されます。基本的なアクションには  `cmd-action` と  `python-action` の2つの種類があります。アクションのうち、 `result` はタスクの実行が成功したかどうかを判断するために使用されます。

### python-action
アクションが Python の呼び出し可能オブジェクト(Callable) またはタプル `(callable, *args, **kwargs)` の場合、 `callable` のみが必要です。 `callable` は、関数、メソッド、または callable オブジェクトでなければなりません。 `args` はシーケンス、 `kwargs` は辞書で、 `callable` の位置引数とキーワード引数として使用されます。キーワード引数」を参照してください。

タスクの結果は、アクション関数の戻り値で示されます。

成功した場合は、次のいずれかを返さなければなりません。

-  `True` 
-  `None` 
- １つの辞書
- １つの文字列

完了に失敗した場合は、以下のいずれかを返さなければなりません。

-  `False` はタスクが失敗したことを示します。
- 例外が発生した場合は、エラーとみなされます
-  `TaskFailed` または  `TaskError` のインスタンスを明示的に返すこともできます。

アクションがすでに説明した型以外の型を返す場合、アクションは失敗とみなされますが、この動作は将来のバージョンで変更される可能性があります。


 03_hello_with_args.py
```
 def task_hello():
     """hello py """
 
     def python_hello(times, text, targets):
         with open(targets[0], "a") as output:
             output.write(times * text)
 
     return {'actions': [(python_hello, [3, "py!\n"])],
             'targets': ["hello.txt"],
             }
             
```

 zsh
```
 % doit -f 03_hello_with_args.py hello
 .  hello
 
 % cat hello.txt

 py!
 py!
 py!
 
```

関数 `task_hello` は、タスクそのものではなく、タスククリエータです。タスククリエータの本体は、dodoファイルが読み込まれたときに常に実行されます。

### タスク・クリエーターとアクション
タスククリエータの本体は、タスクが実行される予定がなくても実行されます。タスククリエータの本体は、タスクのメタデータを作成するためだけに使うべきで、タスクを実行するために使うべきではありません。今後、ドキュメントで「タスクが実行される」と書かれている場合は、「タスクのアクションが実行される」と読んでください。

アクションへのパラメータは `kwargs` として渡すことができます。

 04_func_with_args.py
```
 def func_with_args(arg_first, arg_second):
     print(arg_first)
     print(arg_second)
     return True
 
 def task_call_func():
     return {
         'actions': [(func_with_args, [], {
             'arg_second': 'This is a second argument.',
             'arg_first': 'This is a first argument.'})
         ],
         'verbosity': 2,
     }
 
```


 zsh
```
 % doit -f 04_func_with_args.py
 .  call_func
 This is a first argument.
 This is a second argument.
 
```


### cmd-action
CmdActionはサブプロセスで実行されます(python の  `subprocess.Popen()` を使用)。

アクションが文字列の場合、コマンドはシェルを通して実行されます。( `Popen()` に `shell=True` が渡される)。

dodoファイルのpythonコードを使って、タスクに動的な動作を簡単に組み込むことができます。別の例を見てみましょう。

 05_hello_dynamic.py
```
 def task_hello():
     """hello cmd """
     msg = 3 * "hi! "
     return {
         'actions': ['echo %s ' % msg],
         }
 
```

タスククリエータの本体は常に実行されるため、(この例では、 `msg = 3 * "hi!` ) も常に実行されます。

アクションが文字列のリストであり、pathlib の Path クラスのインスタンスである場合、デフォルトではシェルなしで実行されます (  `Popen()` へ 引数  `shell=False` が渡される)。

 06_python_versio.py
```
 def task_python_version():
     return {
         'actions': [['python', '--version']]
         }
 
```

複雑なコマンドの場合は、コマンド文字列を返すcallableを渡すことも可能です。この場合、CmdActionを明示的にインポートする必要があります。

 07_hello_cmdaction.py
```
 from doit.action import CmdAction
 
 def task_hello():
     """hello cmd """
 
     def create_cmd_string():
         return "echo hi"
 
     return {
         'actions': [CmdAction(create_cmd_string)],
         'verbosity': 2,
         }
```

cwd のような追加の引数を  `Popen()` に渡したい場合には、明示的に CmdAction をインポートすることもできます。 `Popen()` のすべてのキーワード引数は、CmdAction で使用できます (ただし、 `stdout` と  `stderr` を除く)。
 `subprocess.Popen()` とは異なり、CmdAction では  `shell` 引数はデフォルトで  `True` になります

タスクの結果は、シェルの規約に従います。プロセスが値0で終了した場合は成功です。それ以外の値はタスクの失敗を意味します。

## カスタムアクション
他のタイプのアクションを作成することも可能です。

### タスク名
デフォルトでは、タスク名はタスククリエーターの関数名から取られます。例えば `def task_hello() ` とすると` hello` という名前のタスクが生成されます。

 `basename` という引数でタスク名を明示的に設定することができます。

 08_task_basename.py
```
 def task_hello():
     """say hello"""
     return {
         'actions': ['echo hello']
         }
 
 def task_xxx():
     """say hello again"""
     return {
         'basename': 'hello2',
         'actions': ['echo hello2']
         }
```


 zsh
```
 % doit -f 08_task_basename.py
 .  hello
 .  hello2
 
```

 `basename` を使って明示的にタスクを作成する場合、タスククリエーターは1つのタスクしか作成できないわけではありません。yield を使用すると、一度に複数のタスクを生成することができます。また、タスクを生成するジェネレータを yield することもできます。これは、汎用的で再利用可能なタスクジェネレータを書くのに便利です。

 09_task_generator.py
```
 def gen_many_tasks():
     yield {'basename': 't1',
            'actions': ['echo t1']}
     yield {'basename': 't2',
            'actions': ['echo t2']}
 
 def task_all():
     yield gen_many_tasks()
     
```

 zsh
```
 % doit -f 09_task_generator.py
 .  t1
 .  t2
 
```


### タスクの一覧表示
doitには、すべてのタスクをリストアップ/プリントするためのサブコマンドが組み込まれています。

 zsh
```
 % doit -f 08_task_basename.py list
 hello    say hello
 hello2   say hello again
 
 % doit -f 09_task_generator.py list
 t1
 t2
 
```

### ドキュメント
すべてのタスクには、関連するドキュメントがあります。デフォルトでは、このドキュメントはタスク作成関数の docstring から取得されます。 `doc` 属性で設定することもできます。

 10_hello_with_doc,py
```
 def task_hello():
     return {
         'actions': ['echo hello'],
         'doc': 'say hello',
     }
     
```

 zsh
```
 % doit -f 10_hello_with_doc.py list
 hello   say hello
 
```


### サブタスク
多くの場合、同じタスクを異なるコンテキストで何度も適用したいものです。

task関数は、辞書を生成するPythonのジェネレータを返すことができます。各サブタスクは一意に識別されなければならないので、追加のフィールド  `name` が必要です。

 11_subtask.py
```
 def task_create_file():
     for i in range(3):
         filename = "file%d.txt" % i
         yield {'name': filename,
                'actions': ["touch %s" % filename]}
 
```

 zsh
```
 % doit -f 11_subtask.py
 .  create_file:file0.txt
 .  create_file:file1.txt
 .  create_file:file2.txt
 
```

### 空のサブタスクを回避
与えられたベースネームに対してサブタスクが作成されるかどうかわからないけれど、タスクが存在することを確認したい場合は、 `name` を  `None` としたサブタスクを生成することができます。これは、タスクの `doc` および `watch` 属性の設定にも使用できます。

 12_avoid_emoty_subtask.py
```
 import glob
 
 def task_xxx():
     """my doc"""
     LIST = glob.glob('*.xyz') # might be empty
     yield {
         'basename': 'do_x',
         'name': None,
         'doc': 'docs for X',
         'watch': ['.'],
         }
     for item in LIST:
         yield {
             'basename': 'do_x',
             'name': item,
             'actions': ['echo %s' % item],
             'verbosity': 2,
             }
             
```

 zsh
```
 % doit -f 12_avoid_empty_subtask.py
 % doit -f 12_avoid_empty_subtask.py list
 do_x   docs for X
 
```


### 依存関係とターゲット
doit、および他のビルドツールの主なアイデアの一つは、タスク/ターゲットが最新であるかどうかをチェックすることです。依存関係に変更がなく、ターゲットがすでに存在している場合、前回の実行で同じ出力が得られるため、時間を節約するためにタスクの実行をスキップします。

- **依存関係**　依存関係は、タスク実行の入力を示します。
- **ターゲット**　タスクの実行によって生成される結果/出力ファイルです。

例えば、コンパイルタスクでは、ソースファイルが  `file_dep` で、オブジェクトファイルが  `target` となる。

 13_dependency_target.py
```
 def task_compile():
     return {'actions': ["cc -c main.c"],
             'file_dep': ["main.c", "defs.h"],
             'targets': ["main.o"]
             }
```

 main.c
```
 #include <stdio.h>
 #include "defs.h"
 
 int main() {
     printf(MESSAGE);
 }
 
```

 defs.h
```
 #define MESSAGE "Hello World!"
 
```

doitは、ファイルの依存関係を自動的に記録します。タスクが正常に完了するたびに、依存関係の署名(MD5)を保存します。


そのため、依存関係に変更がなく、再度doitを実行すると タスクのアクションの実行はスキップされます。

 zsh
```
 % doit -f 13_dependency_target.py
 .  compile
 
 % doit -f 13_dependency_target.py
 -- compile
```


2回目に実行されたときのコマンド出力にある `-- ` （ダッシュ2つ、スペース1つ）に注目してください。これは、このタスクが最新でありながら実行されなかったことを意味しています。

### file_dep (ファイルの依存関係)
ほとんどのビルドツールとは異なり、依存関係はターゲットではなくタスクにあります。そのためdoitは、ターゲットを定義していないタスクであっても、「最新でない場合のみ実行する」という機能を利用することができます。

例えば、動的言語（この例ではpython）を扱うとします。コンパイルする必要はありませんが、ソースコードファイルにlintのようなツール(pyflakesなど)を適用したいと思うでしょう。ソースコードをタスクの依存関係として定義することができます。

 `file_dep` リストのすべての依存関係は、文字列またはpathlibの任意のPathクラスのインスタンスでなければなりません。

 14_task_checker.py
```
 def task_checker():
     return {'actions': ["pyflakes sample.py"],
             'file_dep': ["sample.py"]}
             
```

 sample.py
```
 print("Hello World!")
 
```

 zsh
```
 % pip install pyflakes
 % doit -f 14_task_checker.py
 .  checker
 % doit -f 14_task_checker.py
 -- checker
```

doitは、 `file_dep` が変更されたかどうかを(ファイルの内容のMD5を比較して)チェックする。変更がなければ、アクションは同じ結果になるので再実行されない。

実行がスキップされたことを示す  `-- ` に注意してください。

従来のビルドツールでは、ファイルを依存関係としてしか扱うことができません。doitには、依存関係をチェックするいくつかの方法があります。詳しくは後述します。


doit は、アクションが実行された後に  `file_dep` の MD5チェックサム を保存します。タスクの実行中に  `file_dep` を編集すると、doit がタスクの実行に実際に使用されたものとは異なるバージョンのファイルの MD5チェックサムを保存する可能性があるので注意が必要です。 このファイルは  `.doit.db.db` です。

 zsh
```
 % doit -f 14_task_checker.py
 .  checker
 % file .doit.db.db
 .doit.db.db: Berkeley DB 1.85 (Hash, version 2, native byte-order)
 % rm .doit.db.db
 % doit -f 14_task_checker.py
 .  checker
 
```

### ターゲット
 `targets` には、任意のファイルパス（ファイルまたはフォルダ）を指定できます。ターゲットが存在しない場合は、タスクが実行されます。タスクが定義できるターゲットの数に制限はありません。異なる2つのタスクが同じターゲットを持つことはできません。ターゲットは、文字列または pathlib の任意の Path クラスのインスタンスとして指定できます。

コンパイルの例をもう一度見てみましょう。


 13_dependency_target.py
```
 def task_compile():
     return {'actions': ["cc -c main.c"],
             'file_dep': ["main.c", "defs.h"],
             'targets': ["main.o"]
             }
```

依存関係に変更がない場合、タスクの実行はスキップされます。
しかし、ターゲットが削除されると、タスクは再び実行されます。
ただし、ターゲットが存在しない場合に限ります。ターゲットが変更されても、依存関係に変化がなければ、タスクは再び実行されません。

 zsh
```
 % rm main.o
 % doit -f 13_dependency_target.py
 .  compile
 % doit -f 13_dependency_target.py
 -- compile
 % rm main.o
 % doit -f 13_dependency_target.py
 .  compile
 % echo xxx > main.o
 % doit -f 13_dependency_target.py
 -- compile
```

### 実行順序
あるタスクのターゲット(出力)が他のタスクのfile_dep(入力)となるようなタスクの相互作用がある場合、doitはタスクが正しい順序で実行されるようにします。

 15_exec_order.py
```
 def task_modify():
     return {'actions': ["echo bar > foo.txt"],
             'file_dep': ["foo.txt"],
             }
 
 def task_create():
     return {'actions': ["touch foo.txt"],
             'targets': ["foo.txt"]
             }
             
```

 zsh
```
 % doit -f 15_exec_order.py
 .  create
 .  modify
 
```

doitは `file_dep` と `targets` のファイルパス(文字列)を比較します。そのため、 `my_file` と  `./my_file` は実際には同じファイルであるにもかかわらず、doit はそれらを別のファイルであると判断してしまうことに注意してください。

### タスクの選択
デフォルトでは、すべてのタスクは定義されたのと同じ順序で実行されます（依存関係を満たすために順序が変更されることがあります）。どのタスクを実行するかは、2つの方法で制御できます。

別の例

 16_task_selection.py
```
 DOIT_CONFIG = {'default_tasks': ['t3']}
 
 def task_t1():
     return {'actions': ["touch task1"],
             'targets': ['task1']}
 
 def task_t2():
     return {'actions': ["echo task2"]}
 
 def task_t3():
     return {'actions': ["echo task3"],
             'file_dep': ['task1']}
             
```

### DOIT_CONFIG -> default_tasks
 `DOIT_CONFIG` の辞書に、 `default_tasks` というタスク名の文字列リストを定義しています。

 zsh
```
 % doit -f 16_task_selection.py
 .  t1
 .  t3
 
```

タスク  `t3` だけがデフォルトで実行されるように指定されていることに注意してください。しかし、その依存関係には別のタスク `t1 `` のターゲットが含まれています。そのため、そのタスクも自動的に実行されました。

### コマンドライン選択
コマンドラインからは、タスク名を渡すことで、どのタスクが実行されるかを制御できます。任意の数のタスクを位置引数として渡すことができます。

 zsh
```
 % doit -f 16_task_selection.py t2
 .  t2
 
```

また、どのタスクを実行するかをターゲットで指定することもできます。


 zsh
```
 % doit -f 16_task_selection.py task1
 .  t1
```


### サブタスクの選択
コマンドラインからサブタスクのフルネームを指定して選択することができます。

 17_subtask_selection.py
```
 def task_create_file():
     for i in range(3):
         filename = "file%d.txt" % i
         yield {'name': filename,
                'actions': ["touch %s" % filename]}
                
```

 zsh
```
 % doit -f 17_subtask_selection.py create_file:file2.txt
 .  create_file:file2.txt
 
```

### ワイルドカード選択
実行するタスクをPytho の [glob http://docs.python.org/library/glob.html] のような構文で選択することもできます（ `*` を含む必要があります）。

 zsh
```
 % doit -f 17_subtask_selection.py create_file:file*
 zsh: no matches found: create_file:file*
 % doit -f 17_subtask_selection.py "create_file:file*"
 .  create_file:file0.txt
 .  create_file:file1.txt
 .  create_file:file2.txt
```

シェルのワイルドカードも `*` を使用していることに留意してください。ワイルドカードを使ったタスク指定では明示的に２重引用符( `"..."` )もしくは引用符( `'...'` )で囲むようにしてください。

### アクションのパラメータ
アクションは、python-actionでは関数キーワードの引数として、オプションのパラメータを取ることができます。また、cmd-actionではC言語の `printf()` で使用するような `%指定子` のフォーマットを値として取ります。

パラメータの値には3つのソースがあります。

- アクションの kwargs 定義で指定されたもの
- 依存関係、変更、ターゲット、タスクなどのタスクメタデータのキーワード
- 他のタスクで計算された値。getargs は、タスクがどのように値を計算して保存するか、また他のタスクがどのように値を参照するかを説明します。

### タスクメタデータのキーワード
これらの値はdoitによって自動的に計算されます。

- 依存関係:  `file_dep` のリスト
- changed: 前回の実行成功後に変更されたfile_depのリスト
-  `targets` : ターゲットのリスト
- task: python-actionでのみ利用可能です。注意：値はTaskオブジェクトのインスタンスであり、メタデータのdictではありません。

### cmd-action文字列のキーワード
cmd-actionでは、pythonフォーマットを使って、cmd-action文字列上で暗黙のキーワード置換を利用することができます。
f-string表記方法と  `%` フォーマット)の両方が利用可能で、DOIT_CONFIG の  `action_string_formatting` の値で制御されます。それは可能です。

-  `'old'` ：old-string-formatting - は古い文字列フォーマットを使用する(例： `%{target}s` )
-  `'new'` ：format-string-syntax - はf-string表記 (例： `{target}` )を使用します。
-  `'both'` 古いスタイルと新しいスタイルの両方

キーワードの値は、スペース（ `" "` ）で区切られたそれぞれのファイル名をすべて含む文字列です。

 18_cmd_action_string.py
```
 DOIT_CONFIG = {'action_string_formatting': 'both'}
 
 def task_report_deps():
     """
     Report dependencies and changed dependencies to a file.
     """
     return {
         'file_dep': ['req.in', 'req-dev.in'],
         'actions': [
                 # New style formatting
                 'echo D: {dependencies}, CH: {changed} > {targets}',
                 # Old style formatting
                 'cat %(targets)s',
                 ],
         'targets': ['report.txt'],
         }
 
```

 `action_string_formatting` のデフォルトは `'old'` です。このデフォルト値は将来のバージョンで変更される可能性がありますので、常に明示的に値を指定することをお勧めします。

文字列が実際に実行される前に、DOIT_CONFIGで指定されたフォーマッタを使って常にフォーマットされます。 フォーマッタの制御文字、すなわちformat-string-syntaxでは `{` と `}` 、old-string-formattingでは `%` を必ずエスケープしてください。これは文字を二重にすることで行われます。つまり、 `{` と `}` は、 `{{` と `}}` になり、 `%` は `%%` になります。

#### 注意
cmd-actionは、文字列(例： `"echo hello world"` )や引数のリスト(例：`["echo", "hello", "world"] ` )の形式をとります。暗黙のキーワード置換は、文字列形式にのみ適用され、リスト形式には影響しません。つまり、この形式では` {}` や  `%` をエスケープする必要はありません。

### python-action のキーワード
python-actionでは、関数内にキーワードパラメータを追加すると、関数が呼ばれたときにdoitが値の受け渡しを行います。 `dependencies` 、 `changed` 、 `targets` は文字列のリストとして渡されます。

 19_keyword_python_action.py
```
 def task_hello():
     """hello"""
 
     def python_hello(targets):
         with open(targets[0], "a") as output:
             output.write("Python says Hello World!!!\n")
 
     return {
         'actions': [python_hello],
         'targets': ["hello.txt"],
         }
 
```

また、すべてのタスクのメタデータを参照することができる キーワード `task` も渡されます。

 20_pass_keyword.py
```
 def who(task):
     print('my name is', task.name)
     print(task.targets)
 
 def task_x():
     return {
         'actions': [who],
         'targets': ['asdf'],
         'verbosity': 2,
         }
```

タスクの属性を取得するだけでなく、アクションの実行中に属性を変更することも可能です。

### プライベート/隠しタスク
タスク名がアンダースコア ` '_' ` で始まる場合、出力には含まれません。

### タイトル
デフォルトでは、doitを実行すると、タスク名だけが出力されます。タスクに title 関数を渡すことで、出力をカスタマイズできます。

 21_title.py
```
 def show_cmd(task):
     return "executing... %s" % task.name
 
 def task_custom_display():
     return {'actions':['echo abc efg'],
             'title': show_cmd}
             
```

 zsh
```
 % doit -f 21_titile.py
 .  executing... custom_display
 
```

### verbosity(冗長度)
デフォルトでは、タスクの標準出力(stdout)はキャプチャされ、標準エラー出力(stderr)がコンソールに送信されます。タスクが失敗したり、エラーが発生した場合は、標準出力とトレースバック（もしあれば）が表示されます。

verbosity には3つのレベルがあります。

- 0：　タスクからのstdout/stderrをキャプチャする（印刷しない）。
- 1 (デフォルト)：　stdout のみをキャプチャする。
- 2：　何もキャプチャしない (すべてをすぐに表示する)。

冗長性をコントロールするには、以下の方法がある。

- タスク属性のverbosity で設定
- コマンドラインから  `--verbosity` につづけてレベルを指定

 22_verbosity.py
```
 def task_print():
     return {'actions': ['echo hello'],
             'verbosity': 2}
             
```

 zsh
```
 % doit -f 22_verbosity.py
 .  print
 hello
 
 % doit -f  22_verbosity.py --verbosity 1
 .  print
 
```


## pathlib
doitはpathlibをサポートしています。リストとして指定された `file_dep` 、 `targets` 、 `CmdAction` は、文字列だけでなく、pathlibの任意のPathクラスのインスタンスを要素として取ることができます。

コンパイルの例を、pathlibを使ってカレントディレクトリにある任意の数のヘッダーファイルやソースファイルを扱うように変更してみましょう。

 23_pathlib.py
```
 from pathlib import Path
 
 def task_compile():
     working_directory = Path('.')
     # Path.glob returns an iterator so turn it into a list
     headers = list(working_directory.glob('*.h'))
     for source_file in working_directory.glob('*.c'):
         object_file = source_file.with_suffix('.o')
         yield {
             'name': object_file.name,
             'actions': [['cc', '-c', source_file]],
             'file_dep': [source_file] + headers,
             'targets': [object_file],
         }
         
```


 zsh
```
 % rm main.o
 % doit -f 23_pahtlib.py
 .  compile:main.o
 % doit -f 23_pahtlib.py
 -- compile:main.o
 
```

## 依存関係の詳細
### uptodate
ファイルの依存関係とは別に、 `uptodate` 属性を使ってタスクが最新かどうかを判断する他の方法をサポートするようにdoitを拡張することができます。

これは、タスクが最新であるかどうかを判断するために、何らかの計算が必要な場合に使用できます。

 `uptodate` はリストで、各要素は `True` 、 `False` 、 `None` 、callable、command(string)のいずれかです。

-  `False` は、タスクが最新でないことを示します。
-  `True` はタスクが最新であることを示します。
-  `None` の値は単に無視されます。これは、値が動的に計算される場合に使用されます。

 `uptodate` の値が `True` になっても、他のup-to-dateのチェックを上書きすることはありません。これは、タスクが最新でないかどうかをチェックするもうひとつの方法である。

例えば、  `uptodate==True` であっても  `file_dep` が変更されていれば、 タスクはまだ最新ではないとみなされます。

 `uptodate` の項目が文字列の場合、シェル上で実行される。プロセスが終了コード 0 で終了した場合、最新とみなされる。それ以外の値は最新ではないとみなされます。

uptodate要素は、（タスクの作成時ではなく）ランタイムに実行されるcallableにすることもできます。このcallableは通常、現在の時刻の値と、最後に実行に成功したときに計算された値を比較します。

注意点
doitはチェックを短絡的に行い、タスクが最新ではないと既に判断された場合、残りのuptodateチェックは実行されません。

doit には uptodate として使われるいくつかの実装があります。これらはすべてdoit.toolsモジュールに含まれており、後で詳しく説明します。

-  `result_dep` : 他のタスクの結果が変更されたかどうかをチェックします。
-  `run_once` : タスクを一度だけ実行する(依存性のないタスクに使用)
-  `timeout` : タスクがある一定の時間後に「期限切れ」になることを示す
-  `config_changed` : 「設定」文字列または辞書の変更をチェックする
-  `check_timestamp_unchanged()` : 指定されたファイル/ディレクトリのアクセス、ステータス変更、作成、変更のタイムスタンプをチェックする。

### 最新のタスクの定義
以下のいずれかに該当する場合、タスクは最新ではないとみなされます。

-  `uptodate` 項目が `False` である（または `False` と評価される）。
-  `file_dep` にファイルが追加された、または `file_dep` からファイルが削除された
-  `file_dep` が前回の実行時から変更された場合
- ターゲットパスが存在しない
- タスクに `file_dep` がなく、 `uptodate` 項目が `True` の場合

つまり、タスクが入力(依存関係)を明示的に定義していなければ、最新とはみなされないということです。

ターゲットはタスクの出力を表すので、ターゲットがないだけでタスクが最新でないと判断されることに注意してください。しかし、ターゲットが存在するだけでは、タスクが最新であるとは言えません。

状況によっては、ターゲットはあるが依存関係のないタスクを定義すると便利です。 `uptodate` に  `True` の値を追加するか、  `run_once()` を使ってdoitによって管理された少なくとも1回の実行を強制することができます。

 24_update.py
```
 def task_touch():
     return {
         'actions': ['touch foo.txt'],
         'targets': ['foo.txt'],
         # ターゲットが削除されない限り、
         # doitが常にタスクを最新の状態としてマークするように強制する
         'uptodate': [True],
         }
```

タスクが最新であるかどうかを判断するための file_dep と uptodate 以外にも、doit には他の種類の依存関係があり、タスクを組み合わせて適切な順序で実行することができます。


## タスク作成の詳細
### タスクのインポート
doitローダーは、dodoの名前空間にあるすべてのオブジェクトを調べます。 `task_` で始まる関数や、 `create_doit_tasks` で始まるオブジェクトを探します。ですから、他のモジュールのタスク定義をdodoファイルにインポートするだけで、それを読み込むことも可能です。

 30_importing_task.py
```
 # import task_ functions
 from get_var import task_echo
 
 # import tasks with create_doit_tasks callable
 from custom_task_def import sample
 
 
 def task_hello():
     return {'actions': ['echo hello']}
     
```

 get_var.py
```
 from doit import get_var
 
 config = {"abc": get_var('abc', 'NO')}
 
 def task_echo():
     return {'actions': ['echo hi %s' % config],
             'verbosity': 2,
             }
             
```

 custom_task_def.py
```
 def make_task(func):
     """make decorated function a task-creator"""
     func.create_doit_tasks = func
     return func
 
 @make_task
 def sample():
     return {
         'verbosity': 2,
         'actions': ['echo hi'],
         }
         
```

 zsh
```
 % doit -f 30_importing_task.py list
 echo
 hello
 sample
 
```

異なるモジュールからタスクをインポートすることは、タスク定義を異なるモジュールに分割したい場合に便利です。
複数のプロジェクトで使用できる再利用可能なタスクを作成するための最良の方法は、タスク辞書を返す関数を呼び出すことです。

### 遅延タスク(delayed task )の生成
doitの実行モデルは2つのフェーズに分かれています。

- task-loading : ( `task_` という文字列で始まる)タスク作成関数を検索し、タスクのメタデータを作成します。
- task-execution : どのタスクが古くなっているかをチェックし、それを実行する。

doitでは、タスク実行中に `calc_deps` や  `uptodate` でタスクのメタデータを修正することができますが、それは既に作成されたタスクの修正に限られます...。

いくつかのタスクが実行される前に、作成されるべきすべてのタスクを知ることができないことがあります。このような場合、doitはタスクの遅延生成をサポートします。つまり、タスクのロードが完了する前にタスクの実行が開始されます。

タスク作成関数がdoit.create_afterで装飾されている場合、タスクを作成するための評価は、実行されたparamで指定されたタスクの実行後に起こるように遅延されます。

 31_delayed_task.py
```
 import glob
 
 from doit import create_after
 
 
 @create_after(executed='early', target_regex='.*\.out')
 def task_build():
     for inf in glob.glob('*.in'):
         yield {
             'name': inf,
             'actions': ['cp %(dependencies)s %(targets)s'],
             'file_dep': [inf],
             'targets': [inf[:-3] + '.out'],
             'clean': True,
         }
 
 def task_early():
     """a task that create some files..."""
     inter_files = ('a.in', 'b.in', 'c.in')
     return {
         'actions': ['touch %(targets)s'],
         'targets': inter_files,
         'clean': True,
     }
     
```

遅延タスクローダーが作成したターゲットをdoit runに指定できるようにするために、遅延タスクローダーごとに正規表現（regex）を指定することも可能です。指定された場合、この正規表現は、この遅延タスク・ジェネレーターによって生成される可能性のあるあらゆるターゲット名と一致する必要があります。この正規表現は、追加のタスクジェネレーター引数target_regexで指定できます。上記の例では、target_regexに与えている `.*\.out` という正規表現は、 `.out` で終わるすべてのターゲット名にマッチします。

正規表現として `.*` を指定することで、すべての可能なターゲット名にマッチさせることができます。また、コマンドラインオプションの `--auto-delayed-regex` を使って実行することもできます。

### パラメータ：creates
DelayedTask で生成されたタスクの `basename` がタスククリエータ関数と異なる場合や、 `basename` の異なる複数のタスクを生成する場合には、パラメータ `creates` を渡します。

doit は、必要に応じてタスク作成関数の本体を実行するだけなので、タスク名は明示的に指定する必要があります。

 32_parameter_creates.py
```
 import sys
 
 from doit import create_after
 
 def say_hello(your_name):
     sys.stderr.write("Hello from {}!\n".format(your_name))
 
 def task_a():
     return {
         "actions": [ (say_hello, ["a"]) ]
     }
 
 @create_after("a", creates=['b'])
 def task_another_task():
     return {
         "basename": "b",
         "actions": [ (say_hello, ["b"]) ],
     }
     
```

doitは通常、 `file_dep` と `target` の関係をチェックすることで、 タスク間の `task_dep` を自動的に設定する。パフォーマンス上の理由から、これらの `task_dep` 関係は、 遅延タスクのターゲットに対しては計算されません。この問題は、遅延タスクの作成を予想される実行順序で行うことで回避できます。

### カスタムタスクの定義
 `task_` で始まる関数を集める以外にも、doitローダーはタスクを実行します。doitローダーは、この属性を含むオブジェクトから create_doit_tasks callable を実行します。

 33_custom_task_define.py
```
 def make_task(func):
     """make decorated function a task-creator"""
     func.create_doit_tasks = func
     return func
 
 @make_task
 def sample():
     return {
         'verbosity': 2,
         'actions': ['echo hi'],
         }
         
```

プロジェクト [letsdoit ](https://bitbucket.org/takluyver/letsdoit/src/master/) には、実際に使用されているカスタムタスクの実装を参照してみてください。
カスタムタスクを作るときに役立つ簡単な例は、この[ブログ記事 http://blog.schettino72.net/posts/doit-task-creation.html] を参照してください。




## ツール
doit.toolsには、よく使われるコードが含まれています。これらはdoitコアでは使用されず、「標準ライブラリ」として見ることができます。

### アクション：create_folder 
フォルダがまだ存在していない場合にフォルダを作成します。 `os.makedirs()` を使用しています。

 50_create_folder.py
```
 from doit.tools import create_folder
 
 BUILD_PATH = "_build"
 
 def task_build():
     return {'actions': [(create_folder, [BUILD_PATH]),
                         'touch %(targets)s'],
             'targets': ["%s/file.o" % BUILD_PATH]
             }
             
```

### アクション: title_with_actions
タスクからタスク名のタスクアクションを返します。この関数は、タスク辞書の  `title` 属性として使用することで、 実行されるアクションのより詳細な情報を提供することができます。

 51_title_with_actions.py
```
 from doit.tools import title_with_actions
 
 def task_with_details():
     return {'actions': ['echo abc 123'],
             'title': title_with_actions}
             
```

### アクション：LongRunning 
長時間実行されているシェル・プロセス（通常はサーバーやサービス）を処理するアクションです。

- 出力はキャプチャされない
- 常に成功します（リターンコードは使用されません）
- キーボード割り込みができません（ `KeyboardInterrupt` 例外は飲み込まれます)

Webサーバなどの長時間動作するプロセスを実行するのに便利です。

 52_long_running.py
```
 from doit.tools import LongRunning
 
 def task_top():
     cmd = "top"
     return {'actions': [LongRunning(cmd)],}
     
```

### アクション：Interactive
インタラクティブ・シェル・プロセスを処理するアクションです。

- 出力はキャプチャされない

### アクション： PythonInteractiveAction
インタラクティブでPythonを処理するアクションです。

- 出力は決してキャプチャされません
- 例外が発生しない限り成功します

### set_trace
doit はデフォルトで stdout と stderr をリダイレクトします。このため、 `pdb.set_trace` でpythonデバッガを使おうとすると、正しく動作しません。適切なPDBシェルを得るためには、 `pdb.set_trace` の代わりに `doit.tools.set_trace` を使うようにしてください。

 53_set_trace.py
```
 def need_to_debug():
     # 何かのコード...
     from doit import tools
     tools.set_trace()
     # ここにもコード...
 
 def task_X():
     return {'actions':[(need_to_debug,)]}
     
```

### IPythonの統合
インタラクティブな実験のための便利な方法は、ipythonのセッションからタスクを定義し、%doitマジック関数を使ってタスクを検出して実行することです。

まず、新しいマジック関数をipythonシェルに登録する必要があります。

 CELL
```
 %load_ext doit.tools
 
```

このマジック機能をIPythonのプロファイルに恒久的に追加するには、スタートアッププロファイルの中に次のような内容の新しいスクリプトを作成します（例： `~/.ipython/profile_default/startup/00_doit_magic.py` ）。

 00_doit_magic
```
 from doit import load_ipython_extension
 load_ipython_extension()
```

スタートアッププロファイルに設定するファイル名は任意です。慣例的に数値ではじめることが多く、これは数値ソートされた順序で読み込まれることを利用するためです。

## 設定ファイル
### 設定パラメータ名
設定オプションの名前は、コマンドラインで使われる長い引数の名前とは必ずしも一致しないことに注意してください。
例えば、コマンドラインで dodo.py 以外の dodo ファイルを指定するには、オプションを  `-f` または  `--file` と指定しますが、設定ファイルでは  `dodoFile` で指定します。

### doit.cfg
doitはINIスタイルの設定ファイルを使用します。注意： `Key = Val` の形式だけが使用できます。
現在の作業ディレクトリにdoit.cfgという名前のファイルがあれば、それを処理します。3種類のセクションをサポートしています。

- **グローバルセクション**
- **各コマンド用のセクション**
- **プラグインのカテゴリーごとのセクション**

### グローバルセクション
GLOBALセクションには、すべてのコマンドで使用されるコマンドライン・オプションを含めることができます（該当する場合）。

DBバックエンドのタイプを設定する例。

 doit.cfg
```
 [GLOBAL]
 backend = json
```

バックエンドオプション（run、clean、forgetなど）を持つすべてのコマンドは、このオプションを使用します。コマンドラインでの指定は不要になります。

### コマンドセクション
特定のコマンドのオプションを設定するには、コマンド名と一緒にセクションを使用します。

 dot.cfg
```
 [list]
 status = True
 subtasks = True
```

### プラグインセクション
doit は機能を容易に拡張できるようなプラグインの機能が提供されています。
設定すべき項目についてはそれぞれのプラグインに依存していますが、次のようなカテゴリが設定されます。

- COMMAND
- BACKEND
- REPORTER
- LOADER


### タスクごとのセクション
特定のタスクのオプションを設定するには、タスク名の前に  `"task: "` を付けたセクションを使います。

 doit.cfg
```
 [task:make_cookies]
 cookie_type = chocolate
 temp = 375F
 duration = 12
```

### dodo.py での設定
便利なことに、dodo.pyに直接GLOBALオプションを設定することもできます。 `DOIT_CONFIG` ディクショナリーにオプションを入れるだけです。以下の例では、デフォルトで実行されるタスク、continueオプション、異なるレポーターを設定しています。

 dodo.py
```
 DOIT_CONFIG = {'default_tasks': ['my_task_1', 'my_task_2'],
                'continue': True,
                'reporter': 'json'}
 
```

このように設定されている dodo.py がカレントディレクトリにあるとき、doit を引数なしで実行します

 zsh
```
 % doit
```

これは、次のようにコマンドラインを実行したのと同じことになります。

zsh
```
 % doit --continue --reporter json my_task_1 my_task_2
```

## DBバックエンド
doitはタスクの実行結果を DBファイルに保存し、様々なバックエンドをサポートします。
デフォルトはPythonの標準ライブラリ dbm を使用しています。実際に使用されるデータベースは、あなたのマシン/プラットフォームで利用可能なものに依存します。

- JSON：JSON構造を使ったプレーンテキストです。速度は遅いですが、デバッグには適しています。
- SQLite3：同時アクセスをサポートしています（プロセスの終了時に一度だけDBが更新され、パフォーマンスが向上します）。

コマンドラインでは、 `--backend` オプションを使ってバックエンドを選択できます。
任意のキーバリューストアに新しいバックエンドを追加するのはとても簡単です。

## DB-ファイル
オプション  `--db-file` はDB-ファイルのファイル名を設定します。デフォルトは  `.doit.db` です。データベース・バックエンドでは複数のファイルを保存することがありますが、その場合は指定した名前がベースネームとして使われます。

dodoファイルに設定する場合、フィールド名は `dep_file` となります。


```
 DOIT_CONFIG = {
     'backend': 'json',
     'dep_file': 'doit-db.json',
 }
```


## プラグイン
doit を機能拡張するプラグインがあります。

## doit-redis
[doit-redis ](https://github.com/saimn/doit-redis) は、redis-pyクライアントを使って、新しいredisバックエンドを追加するプラグインです。ルチプロセッシングに適したバックエンドとなり、複数のdoitプロセスを並行して実行することも可能になります。


 zsh
```
 $ pip install doit-redis
 
```

 doit.cfg
```
 [GLOBAL]
 backend = redis
 
 [BACKEND]
 redis = doit_redis:RedisDB
```

backendはdodoファイルのconfigで設定することもでき、 `dep_file` はRedisのURLを指定するのに使われます。


```
 DOIT_CONFIG = {
     'backend': 'redis',
     'dep_file': 'redis://[:password]@localhost:6379/0',  # optional
 }
```

## doit-report
[doit-report ](https://github.com/saimn/doit-report) は、タスクの実行状況をレポートとして表示する新しいレポートコマンドを追加するプラグインです。
レポートはASCIIまたはHTMLで生成することができます

 zsh
```
 $ pip install doit-report
 
```

 zsh
```
 % doit report
 % doit report --html=out.html
 
```


コンソール出力例：
![](https://gyazo.com/ac6d51fd452a7b55f5607305b610a568.png)

HTML出力例：
![](https://gyazo.com/e966e104dae8400020f48ebddfd0fd13.png)


## doit-graph

graphviz を使用してdoitタスクのグラフを生成します。
使用しているプラットフォームで　ｇraphviz が利用できる必要があります。

 zsh
```
 $ pip install doit-graph
 
```

実行順序の説明で使用した例(15_exec_orderpy)を使ってグラフを生成してみます。

 15_exec_order.py
```
 def task_modify():
     return {'actions': ["echo bar > foo.txt"],
             'file_dep': ["foo.txt"],
             }
 
 def task_create():
     return {'actions': ["touch foo.txt"],
             'targets': ["foo.txt"]
             }
             
```

 bash
```
 $ doit graph -f 15_exec_order.py
 Generated file: tasks.do
 $ dot -Tpng tasks.dot -o 15_exec_order.png
 
```

![](https://gyazo.com/0b4ed06a949c7bdf78e0762d0724b915.png)

- デフォルトでは、サブタスクは隠されています。サブタスクを表示するには  `--show-subtasks` オプションを使います。
- デフォルトでは、すべてのタスクがグラフに含まれます。グラフに含まれるべきタスクを指定することができます（依存関係は自動的に含まれます）。
- タスクを実行順に（つまり依存関係の方向と逆に）描くには、オプション  `--reverse` 
- デフォルトの上から下ではなく、左から右にタスクを描画するには、 `--horizontal` または  `-h` オプションを使用します。


![](https://gyazo.com/51abc126d7a278adf14c5239db6d8858.png)

- グループタスクはノード内で二重の境界線を持つ
- * タスク完了の矢印は実線の矢印を持つ
- * setup-taskの矢印は空の矢印を持つ

制限事項：
calc_depとdelayed-tasksはサポートされていません。

## まとめ
ここまでの説明では、doit の全ての機能を説明しきれていませんが、単なるビルドツールを超えたパワーを感じることができたのではないでしょうか？

doit を使うことで、開発過程で何度も同じコマンドや手順を繰り替える煩雑さを大幅に軽減することができます。
作業や工程を人的作業からコードにすることで、工程の再現性を確実にしつつ、事前事後でのレビューを容易にすることで品質向上につながります。作業内容をgit などのバージョン管理下におくことができるようになるわけです。


## 参考
- [doit ドキュメント ](https://pydoit.org/)
- [doit ソースコード ](https://github.com/pydoit/doit)

#タスクランナー


