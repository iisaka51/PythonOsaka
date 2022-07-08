タスクランナーpypyrを使ってみよう
=================
![](https://gyazo.com/676ca89acdb2dfba802a7dd10092e374.png)

## pypyr について

pypyrは無料で使用できるオープンソースのタスクランナーです。pypr では一連のステップで自動化したいものパイプラインと呼び、パイプラインを実行することができます。機能強化されたシェルスクリプトのようなものですが、それほど気難しいものではありません。makefileよりもイライラしません。
pypyr は Python 3.6 以降で動作します。

#### Pypyrの特徴
- **コマンド、アプリケーション、スクリプトを集約する反復可能なパイプライ**　コマンド、シェル、外部実行ファイル、呼び出し可能な外部スクリプト、インラインコードのあらゆる組み合わせを同じパイプラインで実行することができ、ファイルの読み書き、JSON や YAML のフォーマット、データ構造の操作などの便利な機能を備えた合成可能なビルトインステップも用意されています。
- **YAMLフォーマットの人にやさしいパイプライン**　人が読むことができ、編集、マージも容易にできるようになっています。パイプラインは慣れ親しんだエディタで作成することができます。パイプラインをソース管理し、テキストベースの簡単な差分を得ることができるので、機械で生成された不透明な構文を解読したり、難解な XML や JSON に悩まされたりする時間を省くことができます。
- **条件付き実行、分岐、ループによる制御フローが使用することが可能**　独自のコード、スクリプト、コマンドをforeachループやwhileループで実行できます。制御するスイッチに基づいて、カスタムコードを条件付きで実行したり、スキップしたりすることができます。コーディングをしなくても、pypyrのフロー制御をコマンドやスクリプトに適用できます。これ以上のBashのIFステートメントがどのように動作するかを覚えようとしています。
- **独自のカスタム・クライアントへの引数を渡すことが可能**　pypyrは、独自のコンソールアプリケーションを書くためのフレームワークとして、入力されたclimの取得、解析、検証のためのコードを書く必要がありません。そのため、スクリプトで何かを自動化しようとしているときに、すべての重複したパイプラインを避けることができます。
- **自動再試行、エラー処理、補正が可能**　自分のコマンドやスクリプトが失敗した場合、自動的に再試行し、成功するまで、または設定した再試行制限まで再試行を続けさせることができます。パイプラインの実行を停止すべきエラーを選択できます。複数のステップで失敗ハンドラを使用して例外をキャッチし、より複雑なエラー処理ロジックをカプセル化します。
- **変数の補間と代入が可能**　文字列補間または変数置換を使用して、プレースホルダー {token} を変数の値で置き換えます。これは文字列だけでなく、複雑な型にも対応しています。文字列｛プレースホルダー｝をリストやマップなどのデータ構造全体や、intやboolなどの単純な型に置き換えることができます。
- **設定ファイルのトークン化**　pypyrは、Terraform、Cloudformation、Heatなどの大規模なシステムのブートストラップに必要な設定ファイルやテンプレートを準備するのに非常に便利です。このようなシステムでは、環境ごとに設定を重複させるのではなく、独自の変数値をその場で設定ファイルに注入する必要があります。
- **クライアントとAPIの提供**　pypyrのCLIは、最小限のタイピングと適切なデフォルトを重視しています。また、PythonパイプラインAPIを使って、単一のシンプルなエントリーポイント関数からコードからパイプラインを呼び出すことができます。
- **多くの組み込みステップと独自のカスタムタスク**　pypyrには30以上のビルトインのステップが用意されており、自分のパイプラインに合わせて使うことができます。独自のステップのコーディングは、単一の関数定義にPythonのビットとして簡単です。あなた自身のカスタムステップは、あなたが余分なコードを記述することなく、ループ、リトライ＆フロー制御のための完全に同じパワーと機能を持つ組み込みのステップと共存しています。
- **モジュール式のステップシーケンスでタスクを構成**　パイプラインは他のパイプラインを呼び出すことができます。パイプライン内のステップグループを使用してタスクを反復可能なシーケンスに編成し、より複雑なタスクシーケンスをモジュール化して分離します。
- **豊富なドキュメント**　例を示した分かりやすいヘルプドキュメントが豊富に用意されています。
- **開発 CI&CD 自動化ツール**　pypyrを使えば、どんなタスクでも自動化できます。pypyrは、CI/CD開発機能のために時間をかけて蓄積されたアドホックなスクリプトを統合することに、特に優れています。クラウド・プロバイダーと全く同じCI/CDプロセスをローカルで実行することができます。 `ci build test 5 please work this time` のようなコミットは必要ありません。
- **エージェントレスなパイプラインの実行**　pipで簡単にインストールできます。大規模な開発環境やワークフローの自動化プラットフォームでは、実行環境を提供すること自体が簡単なことではありません。pypyrは軽量なPythonアプリケーションで、依存関係はありません。用意されたDockerコンテナからpypyrを実行することもできます。


## インストール
pypyr は pip コマンドで次のようにインストールできます。

 bash
```
 $ pip install pypyr
```


## pypyr の使用方法概要

最も単純なパイプラインはステップが１つだけの、次のようなものです。

 bash
```
 % pypyr echo "I Love Beer."
 I Love Beer.
 
```

echo は pypyr の組み込みパイプラインの名前です。このパイプラインは、組み込みの echo ステップを使って、入力文字列を単純にコンソールへ出力します。
実際には、次のようなパイプラインを記述します。

 02_echoNe.yaml
```
 ontext_parser: pypyr.parser.string
 steps:
   - name: pypyr.steps.contextcopy
     comment: 入力された引数(argString)をechoMeに割り当て、
              echo stepがそれをエコーできるようにします。
     in:
       contextCopy:
         echoMe: argString
   - pypyr.steps.echo
     
```

 bash
```
 % pypyr 02_echome "I Love Beer"
 I Love Beer
 
```

コマンドラインで2番目の位置引数としてコンテキストを渡すのではなく、パイプラインにコンテキストを設定してパイプラインを実行することで、同じことができます。

 03_ecome.yaml
```
 steps:
   - name: pypyr.steps.echo
     comment: output echoMe
     in:
       echoMe: I Love Beer.
       
```

 bash
```
 % pypyr 03_echome
 I Love Beer.
 
```

## パイプライン
パイプラインとは、単なるYAMLファイルのことです。

最もシンプルなパイプラインでは、steps リストが必要です。これがデフォルトのエントリーポイントです。 stepsは、次々と実行される個々のステップを持つリストです。

例を見てみましょう。

 04_first_pipeline.yaml
```
 steps:
   - name: pypyr.steps.echo
     comment: echoMe の内容を出力
     in:
       echoMe: this is step 1
   - name: pypyr.steps.cmd
     comment: システム上の任意のプログラムを実際に起動します。
              プログラムは環境変数PATHで検索できる必要があります。
              ここでは、簡単なデモとして echo を実行しています。
     in:
       cmd: echo this is step 2
      
```

 bash
```
 % pypyr 04_first_pipeline
 this is step 1
 this is step 2
 
```

これだけ見ると、シェルスクリプトの方が楽に見えるかもしれません。
パイプラインには次の機能があります。（詳しくは後述します)

 YAML
```
 # これは、pypyrパイプラインの機能を示す例です。
 # パイプラインは {working dir}/mypipelinename.yaml として保存されます。
 # {作業ディレクトリ} から次のようにパイプラインを実行します: pypyr mypipelinename
 #　パイプラインにコマンドライン引数を渡す場合は、これに続けて与えることができます。 : pypyr mypipelinename　arg1 arg2
 context_parser: my.custom.parser
 
 # 必須
 steps: # step-group. すべてのパイプラインは、Pypyrに別の方法を指示しない限り、ステップから始まります。
   - my.package.my.module # パッケージ内のpythonモジュールを指すシンプルなステップ
   - mymodule # pythonファイルを指すシンプルなステップ
   - name: my.package.another.module # 複合ステップ。説明文とパラメータが含まれています。.
     description:オプション、人が理解しやすいための文字列で、実行時に出力されます。
     in: # key-valueペアをこのステップのコンテキストに設定します
       parameter1: value1
       parameter2: value2
     run: True # Trueであればこのステップを実行し(デフォルト)、Falseであればステップをスキップします。
     skip: False # Trueであればこのステップをスキップし、Falseであればステップを実行します(デフォルト)。
     swallow: False # Trueでステップで発生したすべてのエラーを無視します。デフォルトは False です
 
 # optional.
 on_success: # step-group
   - my.first.success.step
   - my.second.success.step
 
 # optional.
 on_failure: # step-group
   - my.failure.handler.step
   - my.failure.handler.notifier
   
```

もう少しパイプラインの機能を見てみることにしましょう。

## パイプラインに引数を渡す 
コマンドラインからパイプラインに引数を渡すことは簡単です。

必要なのは、 `context_parser` を追加することだけです。

この例では、keyvaluepairsパーサーを使用します。keyvaluepairs を指定することで、必要な値にキーでアクセスできるようになります。コンテキストパーサーには、cmd 入力を別の方法で解析するタイプもあります。

コンテキストパーサーは、これらの値を pypyr コンテキストに追加してくれます。パイプラインのステップでは、{formatting expression}を使ってこれらの値を自由に使うことができます。

 05_pipeline_with_args.yaml
```
 context_parser: pypyr.parser.keyvaluepairs
 steps:
   - name: pypyr.steps.echo
     in:
       echoMe: this is akey's value {akey}. It came from the cli args.
   - name: pypyr.steps.cmd
     in:
       cmd: echo we can inject {anotherkey} into your cmd
```

 bash
```
 % pypyr 05_pipeline_with_args akey=Python anotherkey=Osaka
 this is akey's value Python. It came from the cli args.
 we can inject Osaka into your cmd
 
```

 組み込みのcontext_parserの一覧

| パーサー | コマンドラインの指定例 |
|:--|:--|
| dict | pypyr pipelinename param1=value1 param2="value 2" param3=value3 |
| json | pypyr pipelinename {"key1": "value 1", "key2": 123} |
| jsonfile | pypyr pipelinename ./path/sample.json |
| keys | pypyr pipelinename param1 'par am2' param3 |
| keyvaluepairs | pypyr pipelinename param1=value1 param2="value 2" "param 3"=value3 |
| list | pypyr pipelinename param1 param2 param3 |
| string | pypyr pipelinename arbitrary string here |
| yamlfile | pypyr pipelinename ./path/sample.yaml |


## クライアントからのパイプラインの実行 

### コマンドラインスイッチをと引数を渡す
pypyrは、コマンドラインで渡された名前で指定されたパイプラインを実行します。
引数なしで実行すると簡単な説明が表示されます。

 bash
```
 % pypyr
 usage: pypyr [-h] [--groups [GROUPS ...]] [--success SUCCESS_GROUP]
              [--failure FAILURE_GROUP] [--dir WORKING_DIR] [--log LOG_LEVEL]
              [--logpath LOG_PATH] [--version]
              pipeline_name [context_args ...]
 pypyr: error: the following arguments are required: pipeline_name
 
```

より詳細な使用方法は、 `--help` オプションで表示できます。

 bash
```
 % pypyr --help
 usage: pypyr [-h] [--groups [GROUPS ...]] [--success SUCCESS_GROUP]
              [--failure FAILURE_GROUP] [--dir WORKING_DIR] [--log LOG_LEVEL]
              [--logpath LOG_PATH] [--version]
              pipeline_name [context_args ...]
 
 pypyr pipeline runner
 
 positional arguments:
   pipeline_name         Name of pipeline to run. It should exist in the ./pipelines directory.
   context_args          Initialize context with this. Parsed by the pipeline's context_parser
                         function.
                         Separate multiple args with spaces.
 
 optional arguments:
   -h, --help            show this help message and exit
   --groups [GROUPS ...]
                         Step-Groups to run. defaults to "steps".
                         You probably want to order --groups AFTER the pipeline name and
                         context positional args. e.g
                         pypyr pipename context --groups group1 group2
                         If you prefer putting them before, use a -- to separate groups from
                         the pipeline name, e.g
                         pypyr --groups group1 group2 -- pipename context
   --success SUCCESS_GROUP
                         Step-Group to run on successful completion of pipeline.
                         Defaults to "on_success"
   --failure FAILURE_GROUP
                         Step-Group to run on error completion of pipeline.
                         Defaults to "on_failure"
   --dir WORKING_DIR     Working directory. Use if your pipelines directory is elsewhere.
                         Defaults to cwd.
   --log LOG_LEVEL, --loglevel LOG_LEVEL
                         Integer log level. Defaults to 25 (NOTIFY).
                         10=DEBUG
                         20=INFO
                         25=NOTIFY
                         30=WARNING
                         40=ERROR
                         50=CRITICAL
                         Log Level < 10 gives full traceback on errors.
   --logpath LOG_PATH    Log-file path. Append log output to this path.
   --version             Echo version number.
   
```

パイプラインをお気に入りのエディタで簡単に編集できるように、拡張子に  `.yaml` を使用しますが、入力の手間を省くために、コマンドラインで与えるときは  `.yaml` を入力する必要はありません。
例えば、 `mypipeline.yaml` を実行したいときは次のようにコマンド入力します。

 bash
```
 $ pypyr mypipeline
 
```

このとき、カレントディレクトリに  `mypipeline.yaml` がないときは、次のディレクトリを順に検索します。

-  `カレントディレクトリ/Pypr` 
-  `カレントディレクトリ/Pypr/pipelines` 
-  `.../site-packages/pypyr/pipelines` 

サブディレクトリにあるパイプラインを実行する場合は、通常のディレクトリセパレータを使用できます。
別のディレクトリにあるパイプラインを実行する場合は、 `--dir` でディレクトリを指定します。

 bash
```
 $ pypyr --dir ~/shared-pipelines subdir1/my-shared-pipe
 
```

この場合は、 `$HOME/shared-pipelines/subdir1/my-shared-pipe.yaml ` を実行します。

パイプラインで必要なパラメタはコマンドラインで与えることもできます。（詳細は後述）

 bash
```
 $  pypyr mydir/mypipeline arbitrary string here
 
```

Key-Valueのペアをキーワード引数として与えることもできます。

 bash
```
 $ pypyr mypipelinename mykey=value anotherkey=anothervalue
 
```

次のようにすると、ロギングレベルを DEBUG で  `./mypipeline.yaml` を実行します。

 bash
```
 $ pypyr mypipeline --loglevel 10
 
```

 `--log` は  `--loglevel` の別名なので、次のようにすると、ロギングレベルを INFO で  `./mypipeline.yaml` を実行します。

bash
```
 $ pypyr mypipeline --logl 20 
 
```

 `--log` や  `--loglevel` が省略された場合は、 `--loglevel 25` 、ログレベル NOTIFY で実行されます。

 bash
```
  $ pypyr mypipeline 
```



## 基本コンセプト 
パイプラインとは、一連のステップのことです。pypyrのパイプラインは、一連のステップを定義した、人が読めて編集できる単純な YAML ファイルです。

 YAML
```
 context_parser: my.custom.parser
 # パイプラインに cli 引数を渡す方法
 
 # 必須
 steps: # step-group
   - step1 # run ./step1.py
   - step2 # run ./step2.py
 
 # オプショナル
 on_success: # step-group
   - my.first.success.step  # run ./my/first/success/step.py
   - my.second.success.step # run ./my/second/success/step.py
 
 # オプショナル
 on_failure: # step-group
   - my.failure.handler.step     # run ./my/failure/handler/step.py
   - my.failure.handler.notifier # run ./my/failure/handler/notifier.py
 
```

### ステップグループ (step-group)
ステップのシーケンスをグループに整理します。デフォルトでは、pypyrはデフォルトの実行で、3つのステップグループを探します。

- step：単なるステップ
- on_success：成功したときに実行されるステップ
- on_failure：失敗したときに実行されるステップ

独自のステップグループを作成して、パイプラインをモジュール化することもできます。

#### ステップ (step)
ステップとは、実際に作業を行うものです。簡単な関数シグネチャを使って自分のステップをコード化することもできますし、もっと簡単に、自分のコードを全く書かずにpypyrの多くのビルトインステップを使うこともできます。

パイプラインでステップを指定するには2つの方法があります。

### シンプルステップ(Simple Step)
シンプルステップは、単にpythonモジュールの名前です。pypyr は作業ディレクトリ内で、これらのモジュールやパッケージを探します。

パッケージの場合は、必ず完全な名前空間を指定してください（例：単なるmymoduleではなく、mypackage.mymodule.）

 YAML
```
 steps:
   - mypackage.mymodule # パッケージ mypackage 内のpythonモジュール mymodule を指します
   - mymodule # ./mymodule.pyを指すシンプルなステップ
   - another.module # ./another/module.pyを指すシンプルなステップ。
 
```


### 複合ステップ (Complex Step)
複合ステップでは、ステップの詳細を指定することができますが、本質的にはシンプルなステップと同じで、いくつかのpythonモジュールを指しています。

 YAML
```
 steps:
   - name: mypackage.anothermodule
     description: description（説明)はオプション
                  任意の(エスケープされた)YAMLで記述します。
                  実行時に通知(NOTIFY)としてコンソールに出力されます。
     comment: comment(コメント)はオプション
              パイプラインの開発/保守のするときの捕捉説明となるもの。
              実行時には何も出力されません。
     in: # in(入力値）はオプションです
       parameter1: value1
       parameter2: value2
```

 mypackage/anothermodule.py
```
 import sys
 
 def run_step(data):
     print(data)
```

 bash
```
 % pypyr 06_complex_steps
 description（説明)はオプション 任意の(エスケープされた)YAMLで記述します。 実行時に通知(NOTIFY)としてコンソールに出力されます。
 {'parameter1': 'value1', 'parameter2': 'value2'}
```

ステップに記述されるこれらの追加フィールドはデコレーターです。Python のデコレーターとは意味と挙動が違うため注意してください。このデコレータは、ステップに適用できる強力なオプションで、独自の変数を渡したり、ステップをループさせたり、リトライしたり、自動的にエラーを無視したり、特定の条件が満たされたときだけ実行したりすることができます。
詳しくは後述することにしますが、次のようなものが使用できます。

 YAML
```
 steps:
   - name: my.package.another.module
     description: description（説明)はオプション
                  任意の(エスケープされた)YAMLで記述します。
                  実行時に通知(NOTIFY)としてコンソールに出力されます
     comment: comment(コメント)はオプション
              パイプラインの開発/保守のするときの捕捉説明となるもの。
              実行時には何も出力されません。
     in: # オプション。これらのパラメータをこのステップのコンテキストに追加します
         # Key-Valueのペアはこのステップのスコープ内でのみ使用されます
       parameter1: value1
       parameter2: value2
     foreach: [] # オプション。このリストの各項目について、ステップを1回繰り返します
     onError: # オプション。ステップが失敗した場合にエラーに追加するカスタムエラー情報
       code: 111 # カスタムエラーのためにカスタム変数を指定することができます
       description: エラーの説明をここに記述する
     retry: # オプション。エラーが発生しなくなるまで、ステップを再試行します
       max: 1 # 再試行の最大回数。整数。デフォルトは None (無限) です
       sleep: 0 # 再試行の間のインターバルを秒単位で指定します。小数点以下は許されます。デフォルトは0です。
       stopOn: ['ValueError', 'MyModule.SevereError'] # これらのエラーに対して再試行を停止します。デフォルト None（すべてを再試行）。
       retryOn: ['TimeoutError'] # これらのエラーのみを再試行します。デフォルト None（すべてを再試行）
     run: True # オプション。Trueの場合はこのステップを実行し（デフォルト)、Falseの場合はステップをスキップします
     skip: False # オプション。Trueの場合はこのステップをスキップし、Falseの場合はステップを実行（デフォルト)します。
     swallow: False # オプション。True の場合はステップで発生したエラーをすべて飲み込みます。デフォルトはFalseです
     while: # オプション。stopがTrueになるか、最大反復回数に達するまでステップを繰り返します。
       stop: '{keyhere}' # キーの値がTrueと評価されるまでループします
       max: 1 # 実行するループの最大反復回数を指定します。デフォルトは None (無限) です
       sleep: 0 # イタレーション間の睡眠時間を秒単位で指定します。小数点以下も可。デフォルトは0です。
       errorOnMax: False # 最大値に達した場合、エラーを発生させます。デフォルトはFalseです。
 
```

同じパイプラインの中で、シンプルステップと複合ステップを自由に組み合わせて使うことができます。シンプルステップが存在する理由は冗長なタイピングをすることを避けることです。

### カスタムステップグループ 
しかし、これらのデフォルトのステップグループにこだわる必要はありません。独自のステップグループを指定したり、デフォルトに独自のステップグループを混ぜることもできます。

 07_custom_step.yaml
```
 sg1:
   - name: pypyr.steps.echo
     in:
       echoMe: sg1.1
   - name: pypyr.steps.echo
     in:
       echoMe: sg1.2
 sg2:
   - name: pypyr.steps.echo
     in:
       echoMe: sg2.1
   - name: pypyr.steps.echo
     in:
       echoMe: sg2.2
 sg3:
   - name: pypyr.steps.echo
     in:
       echoMe: sg3.1
   - name: pypyr.steps.echo
     in:
       echoMe: sg3.2
 sg4:
   - name: pypyr.steps.echo
     in:
       echoMe: sg4.1
   - name: pypyr.steps.echo
     in:
       echoMe: sg4.2
 
```

このパイプラインを次のように実行すると、はsg2 → sg1 → sg3 の順に実行されます。

 bash
```
 % pypyr 07_custom_step --groups sg2 sg1 sg3
 sg2.1
 sg2.2
 sg1.1
 sg1.2
 sg3.1
 sg3.2
```

ここでは、もし、 `--groups` を指定しなければ、pypyrは通常通り標準のステップグループを探します。デフォルトのステップグループから他のステップグループを呼び出したり、ジャンプしたりすることができるので、一般的なプログラミングにおける `main()` エントリーポイントのようにステップを考えることができます。

 08_step_with_custom_group.yaml
```
 steps:
   - name: pypyr.steps.echo
     in:
       echoMe: begin
   - name: pypyr.steps.jump
     in:
       jump: my_group
 
 my_group:
   - name: pypyr.steps.echo
     in:
       echoMe: my_group step 1
   - name: pypyr.steps.echo
     in:
       echoMe: my_group step 2
 
 # 全てのステップが終わったあとに on_success が実行されます
 on_success:
   - name: pypyr.steps.echo
     in:
       echoMe: end!
       
```

 bash
```
 % pypyr 08_step_with_custom_group
 begin
 my_group step 1
 my_group step 2
 end!
 
```

組み込みのパイプライン

 組み込みのパイプライン

| パイプライン | 説明 | 実行方法 |
|:--|:--|:--|
| donothing | 文字通り何もしない | pypyr donothing |
| echo | コンテキスト値 echoMe を出力する | ypyr echo text goes here |
| pypyrversion | PythinとPypyerのIバージョンを表示. | pypyr pypyrversion |
| magritte | Ester Egg (実用的な意味はない) | pypyr magritte |



## コンテキスト(Context)
pypyr のコンテキストは、パイプライン全体に渡って適用される辞書です。コンテキストを使って、パイプラインのステップ間で値を持続させたり、渡したりすることができます。

コンテキストは、単純な辞書のキーと値のペアだけではありません。どんなオブジェクトでもコンテキストに入れることができます。これは特に強力で、JSON や YAML の設定ファイル全体をコンテキストに読み込み、ステップで使用したりフォーマットしたりすることができます。典型的な使用例は、サードパーティのシステム用の設定ファイルを読み込み、いくつかの変数値を設定ファイルに注入し、新しくフォーマットされたデータでサードパーティのシステムを起動することです。

 `context_parser` は、コマンドラインからコンテキストを初期化することができます。

パイプラインのどのステップでも、コンテキスト辞書からアイテムを追加、編集、削除することができます。

コンテキストはpypyrで実際の作業を行う上で非常に重要であるため、pypyrはコンテキスト値を設定、操作、フォーマットするための多くの組み込みステップを持っています。

## パイプラインでの変数の使い方
pypyrでは、パイプラインのYAML、クライアント（またはAPI）、そしてパイプラインのステップ間でシームレスに値を渡すことができます。

pypyrは、コンテキストに変数を格納します。コンテキストは、パイプライン全体の実行中、スコープ内に留まる辞書です。

変数には、文字列(str)や整数(int)などの単純な型もあれば、辞書やリストなどの複雑な入れ子構造を含むものもあります。例えば、変数は辞書のマッピングであり、そのマッピングにはリストやアレイが含まれ、そのリストには他のディクショナリーやリストが含まれます。

## グローバル変数 
### クライアントからの引数の注入 
パイプラインでコンテキストパーサーを使用することで、cliの引数をパイプラインに注入することができます。

 bash
```
 $ pypyr mypipeline この文字列もすべてコンテキスト入力引数です。
 $ pypyr mypipeline var1=値1 var2="値2"
```

これらの値は、 `clear` で明示的に設定解除したり、ステップで明示的に上書きしたりしない限り、パイプラインの実行中はスコープ内に留まります。

### ステップでの変数設定 
変数の設定は以下の手順で行います。

-  `contextSetf` 
-  `default` 

これらの変数は後続のすべてのステップで使用できます。

 `default` と `contextSetf` の違いは、 `default` は変数がまだ存在していない場合にのみ変数を設定することです。既存の変数を上書きすることはありません。このため、 `default` は、cliから来るオプションの引数にデフォルト値を提供したい場合に特に便利です。

それに比べて  `contextSetf` は、すでに変数が存在していても上書きして常に変数を設定します。

 09_variables.yaml
```
 steps:
   - name: pypyr.steps.contextsetf
     comment: 任意の変数を設定
     in:
       contextSetf:
         var1: my value
         var2: 2
         var3: True
 
   - name: pypyr.steps.echo
     comment: 後続のステップで変数を使用
     run: '{var3}'
     in:
       echoMe: |       # YAML で複数行を記述する表記方法
               var1 is '{var1}'
               var2 is {var2}
```

 bash
```
 % pypyr 09_variables
 var1 is 'my value'
 var2 is 2
```

### 環境変数 
環境変数からpypyrの変数を設定することができます。

 10_environment_variables.yaml
```
 steps:
 - name: pypyr.steps.envget
   comment: 環境変数 MACAVITY を取得して
            それを変数 theHiddenPaw に割り当てる
            MACVITY が存在しない場合、デフォルト値を使用する
   in:
     envGet:
       env: MACAVITY
       key: theHiddenPaw
       default: but macavity wasn't there!
 
 - name: pypyr.steps.echo
   comment: theHiddenPaw に環境変数 MACAVITY の値をセット
   in:
     echoMe: the master criminal {theHiddenPaw}
     
```

 bash
```
 % pypyr 10_environment_variables
 the master criminal but macavity wasn't there!
 % env MACAVITY=Python pypyr 08_environment_variables
 the master criminal Python
```


### ファイルからの変数の読み込み
JSON や YAML ファイルから変数をロードして初期化することができます。

設定ファイルのパスをコマンドライン引数に設定したい場合は、以下のコンテキストパーサーを使用します。

-  `pypyr.parser.jsonfile` ： JSONファイルからの変数の初期化
-  `pypyr.parser.yamlfile` ： YAML ファイルからの変数の初期化

また、ステップを明示的に使用して、パイプラインの実行中の特定のポイントでファイルから変数を読み込むこともできます。

### pypyr.parser.jsonfile
JSONファイルから変数を読み込んでパイプラインに渡します。

 myvars.json
```
 {
     "key1": "value1",
     "key2": "value2",
     "key3": "value3 and {key1} and {key2}",
     "echoMe": "this is a value from a json file",
     "keyInt": 123,
     "keyBool": true
 }
```

 11_from_json.yaml
```
 context_parser: pypyr.parser.jsonfile
 steps:
   # echoMeは JSONファイルに設定されている
   - pypyr.steps.echo
   - name: pypyr.steps.contextsetf
     comment: 強制的にint型付けされたintとして使用する
     in:
         contextSetf:
             intResult: !py keyInt * 2
   - name: pypyr.steps.echo
     comment: JSONファイルのフォーマット式が動作する
     in:
         echoMe: '{key3}'
   - name: pypyr.steps.echo
     comment: 整数計算した結果を出力
     in:
         echoMe: "strongly typed happens automatically: {intResult}"
   - name: pypyr.steps.echo
     comment: 入力がブール値 true のときだけ実行
     run: '{keyBool}'
     in:
         echoMe: you'll only see me if the bool was true
         
```

 bash
```
 % pypyr 11_from_json myvars.json
 this is a value from a json file
 value3 and value1 and value2
 strongly typed happens automatically: 246
 you'll only see me if the bool was true
 
```

### pypyr.steps.fetchjson
特定のステップでJSONファイルから読み込みます。

 12_step_fetchjson.yaml
```
 steps:
   - name: mystep
     description: この段階ではまだJSONを読み込んでいない
   - name: pypyr.steps.fetchjson
     description: 指定したパスのJSONから読み込む
     in:
       fetchJson:
         path: ./myvars.json # 必須：JSONファイルへのパス
   - pypyr.steps.echo
    
```

 bash
```
 % pypyr 12_step_fetchjson
 この段階ではまだJSONを読み込んでいない
 {}
 指定したパスのJSONから読み込む
 this is a value from a json file
```

#### pypyr.parser.yamlfile
YAMLファイルから変数を読み込んでパイプラインに渡します。

 myvars.yaml
```
 key1: value1
 key2: value 2
 key3: "value3 and {key1} and {key2}"
 echoMe: "this is a value from a yaml file"
 keyInt: 123
 keyBool: True
 
```

 13_from_yaml.yaml
```
 context_parser: pypyr.parser.yamlfile
 steps:
   # echoMeは YAMLファイルに設定されている
   - pypyr.steps.echo
   - name: pypyr.steps.contextsetf
     comment: 強制的にint型付けされたintとして使用する
     in:
         contextSetf:
             intResult: !py keyInt * 2
   - name: pypyr.steps.echo
     comment: ファイルのフォーマット式が動作する
     in:
         echoMe: '{key3}'
   - name: pypyr.steps.echo
     comment: 整数計算した結果を出力
     in:
         echoMe: "strongly typed happens automatically: {intResult}"
   - name: pypyr.steps.echo
     comment: 入力がブール値 true のときだけ実行
     run: '{keyBool}'
     in:
         echoMe: you'll only see me if the bool was true
 
```

 bash
```
 % pypyr 13_from_yaml myvars.yaml
 this is a value from a yaml file
 value3 and value1 and value 2
 strongly typed happens automatically: 246
 you'll only see me if the bool was true
```

### pypyr.steps.fetchyaml
YAMLファイルから読み込んでステップのコンテキストに渡します。

 14_step_fetchyaml.yaml
```
 steps:
   - name: mystep
     description: この段階ではまだYAMLを読み込んでいない
   - name: pypyr.steps.fetchyaml
     description: 指定したパスのYAMLから読み込む
     in:
       fetchYaml:
         path: ./myvars.yaml # 必須：JSONファイルへのパス
   - pypyr.steps.echo
   
```

 bash
```
 % pypyr 14_step_fetchyaml
 この段階ではまだYAMLを読み込んでいない
 {}
 指定したパスのYAMLから読み込む
 this is a value from a yaml file
```


## ローカル変数 
 `in` デコレーターを使用すると、現在のステップのスコープ内にのみ存在する変数を設定できます。

グローバル変数を設定するのとは異なり、 `in` を使ってステップに渡した引数は後続のステップでは使用できません。

 mystep.py
```
 import sys
 
 def run_step(data):
     print(data)
```

 15_local_variable.yaml
```
 steps:
   - name: mystep
     comment: 変数 A、B、C はこのステップでだけ有効
     in:
       A: value 1
       B: 2
       C: true
   - name: pypyr.steps.echo
     in:
       echoMe: done! A, B & C are NOT available in this step.
 
```

 bash
```
 % pypyr 15_local_variable
 {'A': 'value 1', 'B': 2, 'C': True}
 done! A, B & C are NOT available in this step.
```

## 変数の設定解除
以下の手順で、変数の設定解除や削除を行うことができます。

-  `pypyr.steps.contextclear` 
-  `pypyr.steps.contextclearall` 

### contextClear
指定した項目をコンテキストから削除します。
 `contextClear` を繰り返して、それらのキーをコンテキストから削除します。

 16_contextclear.yaml
```
 steps:
   - name: pypyr.steps.contextclear
     description: 2つのコンテキストキーをクリア
     in:
       contextClear:
         - removeMe
         - removeMeToo
```


入力として次のコンテキストがあるとします。

 myvars2.yaml
```
 key1: value1
 key2: value2
 key3: value3
 key4: value4
 contextClear:
     - key2
     - key4
     - contextClear
```

これは `contextClear` 自体が、 `contextClear` により設定解除されるため、
結果的に次のコンテキストとなります。

 YAML
```
 key1: value1
 key3: value3
```

### contextClearAll
コンテキスト全体をワイプします。入力コンテキストの引数は必要ありません。
入力コンテキストを必要としないので、シンプルなステップとして `contextclearall` を常に使用することができます。

 17_contextclearall.yaml
```
 steps:
   - my.arb.step
   - pypyr.steps.contextclearall
   - another.arb.step
```


## 変数の読み取り 
置換式を使って、静的な値や変数を読み込んだり、フォーマットしたり、組み合わせたりすることができます。

この例では、2 つのローカル変数 A と B を設定し、置換式を使用してこれらをpypyr.steps.echo の 入力引数 echoMe に渡しています。

 18_read_variable.yaml
```
 steps:
   - name: pypyr.steps.echo
     comment: 静的な文字列と2つの変数を連結します。
              "pipe down the valleys wild" と出力します。
     in:
       A: down the
       B: valleys
       echoMe: piping {A} {B} wild
 
```

 bash
```
 % pypyr 18_read_variable
 piping down the valleys wild
```

ステップのinでAとBをここに割り当てる代わりに、 `contextSetf` や  `default` を使って、その前のステップでAとBをグローバル変数として設定することもできます。


 19_read_variable_global.yaml
```
 steps:
   - name: pypyr.steps.contextsetf
     in:
       contextSetf:
         A: down the
         B: valleys
 
   - name: pypyr.steps.echo
     comment: 静的な文字列と2つの変数を連結します。
               "pipe down the valleys wild" と出力します。
     in:
       echoMe: piping {A} {B} wild
       
```

 bash
```
 % pypyr 19_read_variable_global
 piping down the valleys wild
```


## 条件付きロジック 
### ステップを選択的に実行またはスキップする 
条件文が True と評価されたかどうかに基づいてステップを選択的に実行またはスキップすることで、パイプラインの実行の流れを制御できます。

ステップを実行するかどうかの条件を設定するには、任意のステップで  `run` または  `skip` デコレータを使用します。
デフォルトでは、明示的な指示をしない限り、すべてのステップが実行されます。

 20_basic_condition.yaml
```
 steps:
   - name: pypyr.steps.echo
     comment: step1
     in:
       echoMe: begin
 
   - name: pypyr.steps.cmd
     comment: step2
     run: False
     in:
       cmd: echo this will not run
 
   - name: pypyr.steps.cmd
     comment: step3
     skip: True
     in:
       cmd: echo this will not run
 
   - name: pypyr.steps.echo
     comment: step4
     in:
       echoMe: end
             
```

このパイプラインを実行すると、step2 と step3 は実行されずにスキップされます。

 bash
```
 % pypyr 20_basic_condition
 begin
 end
 
```

### 変数を使ってステップの実行を制御する 
変数を使って条件文をパラメータ化することができます。前のステップで変数を設定したり、クライアントから変数を渡したり、環境変数を使用したり、 `fetchjson` や  `fetchyaml` などを使って別の設定ファイルから変数を読み込むこともできます。

### パイプラインでの条件付きロジックの設定 
あるステップが実行されるかどうかを制御する変数を、パイプライン自体の前のステップで設定することができます。


 21_variable_condition.yaml
```
 steps:
   - name: pypyr.steps.echo
     in:
       echoMe: begin
 
   - name: pypyr.steps.contextsetf
     comment: set variables for use in run/skip later
     in:
       contextSetf:
         arbVar1: False
         arbVar2: arbitrary str
         # arbVar3 will eval True
         arbVar3: !py arbVar2 == 'arbitrary str'
 
   - name: pypyr.steps.cmd
     run: '{arbVar1}'
     in:
       cmd: echo this will not run
 
   - name: pypyr.steps.cmd
     skip: '{arbVar3}'
     in:
       cmd: echo this will not run
 
   - name: pypyr.steps.echo
     in:
       echoMe: end
```

このパイプラインを実行すると、２番目と３番目のステップは実行されません。

 bash
```
 % pypyr  21_variable_condition
 begin
 end
 
```

### ステップを条件付きで実行するためにクライアントの引数を使用する 
pypyrでは、コンテキストパーサーを使用して、クライアントからパイプラインに独自の引数を渡すことができます。
これらの変数をステップ条件の中で直接使用して、ステップを実行するかどうかを制御することができます。
この例では、キーのコンテキストパーサーを使用します。なぜなら、コマンドライン・アプリケーションの自然な構文を作成するためのよくあるパターンは、select機能を実行するための引数として動詞を渡すことだからです。

 22_cli_condition.yaml
```
 context_parser: pypyr.parser.keys
 steps:
   - name: pypyr.steps.default
     comment: set default values for optional cli inputs
     in:
       defaults:
         lint: False
         build: False
 
   - name: pypyr.steps.echo
     in:
       echoMe: begin - always runs
 
   - name: pypyr.steps.cmd
     run: '{lint}'
     in:
       cmd: echo this will only run if you pass lint from cli
 
   - name: pypyr.steps.cmd
     run: '{build}'
     in:
       cmd: echo this will only run if you pass build from cli
 
   - name: pypyr.steps.echo
     in:
       echoMe: end - always runs
 
```

 bash
```
 % pypyr 22_cli_condition
 begin - always runs
 end - always runs
 
 % pypyr 22_cli_condition lint
 begin - always runs
 this will only run if you pass lint from cli
 end - always runs
 
 % pypyr 22_cli_condition build
 begin - always runs
 this will only run if you pass build from cli
 end - always runs
 
 % pypyr 22_cli_condition lint build
 begin - always runs
 this will only run if you pass lint from cli
 this will only run if you pass build from cli
 end - always runs
 
 
```


### 制御フローにPython式を使う
ステップが実行されるかどうかを制御するために、 `!py 文字列` を使い任意の有効なPython式を使用することができます。

 23_python_condition.yaml
```
 steps:
   - name: pypyr.steps.echo
     in:
       echoMe: begin
 
   - name: pypyr.steps.contextsetf
     comment: 任意の変数を設定し、後のステップのラン/スキップ条件に使用
     in:
       contextSetf:
         breakfasts:
           - fish
           - bacon
           - spam
 
         numbersList:
           - 3
           - 4
 
   - name: pypyr.steps.cmd
     run: !py "'eggs' in breakfasts"
     in:
       cmd: echo this will not run
 
   - name: pypyr.steps.cmd
     skip: !py sum(numbersList) < 42
     in:
       cmd: echo this will not run
 
   - name: pypyr.steps.echo
     in:
       echoMe: end
       
```

このパイプラインの実行結果は次のようになります。

 bash
```
 % pypyr  23_python_condition
 begin
 end
 
```


### 複数のステップを同じ条件で制御 
複数のステップの条件付き実行を同じ条件文で制御したい場合、各ステップで同じ条件文を複製するか、カスタムステップグループでステップをグループ化し、コールステップでの1つの条件評価のみでステップグループ全体の実行を制御することができます。


 24_multiple_step_condition.yaml
```
 context_parser: pypyr.parser.keys
 steps:
   - name: pypyr.steps.default
     comment: オプションのCLI入力のデフォルト値設定
     in:
       defaults:
         lint: False
         build: False
 
   - name: pypyr.steps.echo
     in:
       echoMe: begin - always runs
 
   - name: pypyr.steps.call
     run: '{lint}'
     in:
       call: lint
 
   - name: pypyr.steps.call
     run: '{build}'
     in:
       call: build
 
   - name: pypyr.steps.echo
     in:
       echoMe: end - always runs
 
 lint:
   - name: pypyr.steps.cmd
     in:
       cmd: echo lint cmd 1 here
 
   - name: pypyr.steps.cmd
     in:
       cmd: echo lint cmd 2 here
 
 build:
   - name: pypyr.steps.cmd
     in:
       cmd: echo build cmd 1 here
 
   - name: pypyr.steps.cmd
     in:
       cmd: echo build cmd 2 here
 
```

このパイプラインはコマンドラインから制御することができます。

 bash
```
 % pypyr 24_multiple_step_condition
 begin - always runs
 end - always runs
 
 % pypyr 24_multiple_step_condition lint
 begin - always runs
 lint cmd 1 here
 lint cmd 2 here
 end - always runs
 
 % pypyr 24_multiple_step_condition build
 begin - always runs
 build cmd 1 here
 build cmd 2 here
 end - always runs
 
 % pypyr 24_multiple_step_condition lint build
 begin - always runs
 lint cmd 1 here
 lint cmd 2 here
 build cmd 1 here
 build cmd 2 here
 end - always runs
 
```


### 動的にステップを実行
パイプライン用の拡張可能なカスタムCLIを作成するためのコンパクトなパターンは、 `list` コンテキストパーサーと組み合わせて `call` ステップを使用することです。

この方法では、どのステップグループを実行するかをハードコーディングすることはありません。クライアントから渡されたグループ名が順番に実行されます。

 build.yaml
```
 context_parser: pypyr.parser.list
 steps:
   - name: pypyr.steps.call
     comment: lint と test これはすべてのパイプラインの起動時に実行される
     in:
       call:
         - lint
         - test
   - name: pypyr.steps.call
     comment: オプション lint と testの後に packageやpublish などを追加実行
     run: '{argList}'
     in:
       call: '{argList}'
 
 lint:
   - name: pypyr.steps.cmd
     in:
       cmd: echo lint command here
 
 test:
   - name: pypyr.steps.cmd
     in:
       cmd: echo test command here
 
 package:
   - name: pypyr.steps.cmd
     in:
       cmd: echo package command here
 
 publish:
   - name: pypyr.steps.cmd
     in:
       cmd: echo publish command here
 
```

わかりやすくするために、各ステップグループには1つのステップしかありませんが、必要に応じて複数のステップを指定することもできます。

 bash
```
 % pypyr build
 lint command here
 test command here
 
 % pypyr build package
 lint command here
 test command here
 package command here
 
 % pypyr build package publish
 lint command here
 test command here
 package command here
 publish command here
```


## ループ 
pypyrパイプラインの任意のステップをループ（または反復）することができます。
これは、追加のコードを書かずに独自のカスタムコマンドを繰り返し実行したり、ループさせたりできることを意味します。
ループはステップレベルで行われ、以下のステップデコレーターを使用します。

-  `foreach` 
-  `while` 

違いは、 `foreach` が反復可能な要素（リストなど）のすべてを反復するのに対し、 `while` は停止条件がTrueと評価されるまでループを続けることです。

任意のステップで  `foreach` や  `while` ループを指定することができます。また、同じステップで  `foreach` や  `while` のループを入れ子にすることもできます。

### foreach 
ここでは、簡単な  `foreach` ループを実行しています。簡単な例のために、ここでは echo を呼び出していますが、任意のコマンドを実行することができます。

イテレータは  `{i}` です。これは、 `foreach` のイテレータの各反復において、現在の項目を表しています。

 25_foreatch.yaml
```
 steps:
   - name: pypyr.steps.cmd
     comment: mycommand を繰り返すループ
     foreach: ['apple', 'pear', 'banana']
     in:
       cmd: echo mycommand --arg={i}
       
```

 bash
```
 % pypyr 25_foreatch
 mycommand --arg=apple
 mycommand --arg=pear
 mycommand --arg=banana
 
```

### 最大カウントまでwhile  
whileループは、ブーリアン式がTrueになるなどの停止条件が満たされるか、反復回数が一定に達するまで反復します。
現在のイテレーション回数は  `{whileCounter}` です。

最大の反復回数に達するまで継続する while ループの簡単な例を示します。

 26_while_max.yaml
```
 steps:
   - name: pypyr.steps.cmd
     while:
       max: 3
     in:
       cmd: echo mycommand --arg={whileCounter}
       
```

 bash
```
 % pypyr  26_while_max
 mycommand --arg=1
 mycommand --arg=2
 mycommand --arg=3
 
```

### 停止条件付きwhile 
ここでは、停止条件が True になるまで継続する  `while` ループの簡単な例を紹介します。この例では、 `pypyr.steps.py` ステップを使用して、ループの繰り返しごとにカスタムのインラインpythonを実行していますが、これまでと同様に、好きなステップを使用することができます（cmd経由で外部コマンドやスクリプトを実行することもできます）。


 27_while_step.yaml
```
 steps:
   - name: pypyr.steps.py
     while:
       stop: !py arb_value > 5
     in:
       py: |
         arb_value = whileCounter * 2
         print(f'{arb_value=}')
         save('arb_value')
 
```

 bash
```
 % pypyr  27_while_step
 arb_value=2
 arb_value=4
 arb_value=6
 
```

### retry 
あるステップが成功するまでループさせたい場合、自分で  `while` ループを作る代わりに `retry` デコレーターを使うことができます。
 `retry` デコレーターは、様々なバックオフ戦略による再試行間のスリープ間隔の追加をサポートしています。
次の例では、コマンドを最大3回まで自動的に再試行し、最大制限内でコマンドが成功した場合のみ続行します。

 28_retry.yaml
```
 steps:
   - name: pypyr.steps.cmd
     retry:
       max: 3
     in:
       cmd: mycommand --arg=myvalue
   - name: pypyr.steps.echo
     comment: output echoMe
     in:
       echoMe: I Love Beer.
       
```

このパイプラインを実行すると、mycommand が見つからないのでリトライがされ、３回失敗したので終了しています。
そのため、次のステップが実行されなかったために、"I Love Beer" が’表示されていません。

bash
```
 % pypyr 28_retry
 retry: ignoring error because retryCounter < max.
 FileNotFoundError: [Errno 2] No such file or directory: 'mycommand'
 retry: ignoring error because retryCounter < max.
 FileNotFoundError: [Errno 2] No such file or directory: 'mycommand'
 Error while running step pypyr.steps.cmd at pipeline yaml line: 2, col: 5
 Something went wrong. Will now try to run on_failure.
 
 FileNotFoundError: [Errno 2] No such file or directory: 'mycommand'
 
```

もし、成功するまで繰り返す必要があれば、 `max` をゼロ( `0` )に設定します。


### 変数を使ったループ処理 
変数を使ってループステートメントをパラメータ化することができます。前のステップで変数を設定したり、クライアントから変数を渡したり、環境変数を使用したり、fetchjsonやfetchyamlのようなものを使って別の設定ファイルから変数を読み込むこともできます。

次の例では、cliに与えられたすべての引数をループして、カスタムコマンドに注入します。

 29_foreatch_variable.yaml
```
 context_parser: pypyr.parser.list
 steps:
   - name: pypyr.steps.contextsetf
     comment: set defaults for optional cli args
     run: !py len(argList) == 0
     in:
       contextSetf:
         argList: ['one', 'two']
 
   - name: pypyr.steps.cmd
     foreach: '{argList}'
     in:
       cmd: echo mycommand --arg={i}
       
```

この例では、 `pypyr.parser.list` コンテキストパーサーの  `argList` を使用していますが、任意のリストを使用することができます。


 bash
```
 % pypyr  29_foreatch_variable
 mycommand --arg=one
 mycommand --arg=two
 
 % pypyr 29_foreatch_variable four five six
 mycommand --arg=four
 mycommand --arg=five
 mycommand --arg=six
```


### while の反復回数を変数で制御する
どのようなループデコレーターでも、変数を使用することができます。ここでは、環境変数で反復回数の上限を制御する  `while` ループの例を示します。

 3)_while_variable.yaml
```
 steps:
   - name: pypyr.steps.envget
     comment: 環境変数 ARB の値を取得して my_counter にセット
     in:
       envGet:
         env: ARB
         key: my_counter
         default: 3
 
   - name: pypyr.steps.cmd
     while:
       max: '{my_counter}'
     in:
       cmd: echo mycommand --arg={whileCounter}
       
```


 bash
```
 % pypyr 30_while_variable
 mycommand --arg=1
 mycommand --arg=2
 mycommand --arg=3
 
 % env ARB=2 pypyr 30_while_variable
 mycommand --arg=1
 mycommand --arg=2
 
```


### 複数のステップをループさせる 
複数のステップを1つのユニットとしてループさせたい場合は、これらのステップをカスタムステップグループにグループ化してから `call` を使用します。
また、pypeを使って別のパイプラインをループ内で繰り返し呼び出すこともできます。
いずれにしても、これらのステップでは `foreach` や `while` を自由に使うことができます。


 31_foreatch_call.yaml
```
 steps:
   - name: pypyr.steps.call
     foreach: ['apple', 'pear', 'banana']
     in:
       call: my_step_group
 
 my_step_group:
   - name: pypyr.steps.echo
     in:
       echoMe: processing '{i}'
 
   - name: pypyr.steps.cmd
     in:
       cmd: echo mycommand --arg={i}
       
```

この例では、ステップグループの中に `echo` ステップと `cmd` ステップを入れていますが、これは要点を説明するためで、カスタムステップグループの中には、必要に応じて便利なステップをいくつでも入れることができます。
このパイプラインを実行すると、このように表示されます。

 bash
```
 % pypyr 31_foreach_call
 processing 'apple'
 mycommand --arg=apple
 processing 'pear'
 mycommand --arg=pear
 processing 'banana'
 mycommand --arg=banana
 
```


## エラー処理 
### エラー時にすべての処理を停止する 
pypyrはパイプラインを実行します。デフォルトでは、前のステップが失敗した場合、シーケンス内の後続のステップは実行されません。そのため、もしどこかでエラーが発生したら、パイプラインの処理を停止し、後続のステップを実行しないようにしたい場合は、特別なことをする必要はありません。

 32_error_handling.yaml
```
 steps:
   - name: pypyr.steps.echo
     in:
       echoMe: A
   - name: pypyr.steps.py
     comment: 意図的にエラーを起こす
     in:
       py: raise ValueError('arb')
   - name: pypyr.steps.echo
     comment: 前のステップが常に失敗する
              このステップは実行されない
     in:
       echoMe: unreachable
       
```

 bash
```
 % pypyr  32_error_handling
 A
 Error while running step pypyr.steps.py at pipeline yaml line: 5, col: 5
 Something went wrong. Will now try to run on_failure.
 
 ValueError: arb
 
```


### 特定のステップでのエラーを無視する 
 `swallow` デコレーターを True にすると、特定のステップでのエラーを無視することができます。

 33_ignore_error.yaml
```
 steps:
   - name: pypyr.steps.echo
     in:
       echoMe: A
   - name: pypyr.steps.py
     swallow: True
     in:
       py: raise ValueError('arb')
   - name: pypyr.steps.echo
     in:
       echoMe: You'll see me, you set swallow in previous step
```


 bash
```
 % pypyr 33_ignore_error
 A
 pypyr.steps.py Ignoring error because swallow is True for this step.
 ValueError: arb
 You'll see me, you set swallow in previous step
 
```

### エラー時の再試行 
 `retry` デコレーターを設定することで、任意のステップがエラー時に自動的に再試行されるようになります。

 34_retry_error.yaml
```
 steps:
   - name: pypyr.steps.cmd
     comment: 与えたURLへのcurlを自動的に再試行します
              パイプラインは、curlが成功するとすぐに次のステップに進みます
              リトライの間に0.5秒のスリープを挟み、4回のリトライを行います
              4回目のリトライでも失敗した場合は、
              エラーを発生させて失敗を報告します。
     retry:
       max: 4
       sleep: 0.5
     in:
       cmd: curl https://arb-unreliable-url-example/
 
```

 bash
```
 % pypyr  34_retry_error
 curl: (6) Could not resolve host: arb-unreliable-url-example
 retry: ignoring error because retryCounter < max.
 CalledProcessError: Command '['curl', '](https://arb-unreliable-url-example/')' returned non-zero exit status 6.
 curl: (6) Could not resolve host: arb-unreliable-url-example
 retry: ignoring error because retryCounter < max.
 CalledProcessError: Command '['curl', '](https://arb-unreliable-url-example/')' returned non-zero exit status 6.
 curl: (6) Could not resolve host: arb-unreliable-url-example
 retry: ignoring error because retryCounter < max.
 CalledProcessError: Command '['curl', '](https://arb-unreliable-url-example/')' returned non-zero exit status 6.
 curl: (6) Could not resolve host: arb-unreliable-url-example
 Error while running step pypyr.steps.cmd at pipeline yaml line: 2, col: 5
 Something went wrong. Will now try to run on_failure.
 
 CalledProcessError: Command '['curl', '](https://arb-unreliable-url-example/')' returned non-zero exit status 6.
 
```

### 失敗ハンドラー
失敗ハンドラー(failure handler) とは、エラーが発生したときにpypyrがジャンプする省略可能なステップグループのことです。伝統的なプログラミング用語で言えば、Catchブロックのようなものです。failure ハンドラーが完了すると、パイプラインは失敗を報告して終了します。

pypyrは、失敗したステップの `swallow` がFalseの場合に失敗ハンドラを探し、そのステップのリトライが終了した後にのみ失敗ハンドラを探します。

任意の step-group が失敗ハンドラになり得ます。失敗ハンドラを明示的に指定しない場合、pypyr は  `on_failure` という名前のステップグループを探します。 `on_failure` が存在しなくても問題はなく、pypyrは元のエラーを報告するパイプラインを終了します。


 35_failure_handler.yaml
```
 steps:
   - name: pypyr.steps.echo
     in:
       echoMe: A
   - name: pypyr.steps.py
     in:
       py: raise ValueError('arb')
   - name: pypyr.steps.echo
     comment: 前のステップが常に失敗するため
              このステップは実行されない
     in:
       echoMe: unreachable
 
 on_failure:
   - name: pypyr.steps.echo
     in:
       echoMe: B
       
```

 bash
```
 % pypyr  35_failure_handler
 A
 Error while running step pypyr.steps.py at pipeline yaml line: 5, col: 5
 Something went wrong. Will now try to run on_failure.
 B
 
 ValueError: arb
 
 % echo $?
 255
 
```

失敗ハンドラが例外処理中に別の例外に遭遇した場合、pypyrはその例外と元の原因の例外の両方を記録して報告しますが、元の原因の例外は、pypyrがCLI終了時に終了コードとして渡されます。

### 独自の失敗ハンドラを設定する 
任意のステップグループを失敗ハンドラに設定することができます。

 `on_failure` が存在しない場合と同様に、指定されたカスタムの失敗ハンドラーが存在しない場合、pypyrは追加のエラーを発生させません。ログ出力では、探したが見つからなかったことがわかります。

 36_own_failure_handler.yaml
```
 steps:
   - name: pypyr.steps.echo
     in:
       echoMe: A
   - name: pypyr.steps.py
     in:
       py: raise ValueError('arb')
   - name: pypyr.steps.echo
     in:
       echoMe: unreachable
 
 on_failure:
   - name: pypyr.steps.echo
     in:
       echoMe: B
 
 arb_group:
   - name: pypyr.steps.echo
     in:
       echoMe: C
       
```

このパイプラインを実行してみます。

 bash
```
 % pypyr 36_own_failure_handler
 A
 Error while running step pypyr.steps.py at pipeline yaml line: 5, col: 5
 Something went wrong. Will now try to run on_failure.
 B
 
 ValueError: arb
 
```

失敗ハンドラー arb_group を作っていますが、そのままでは  `on_failure` が’呼ばれてしまいます。


### コマンドライン・オプション--failure で指示
コマンドラインからpypyrを起動し、デフォルトの `on_failure` 失敗ハンドラを使用したくない場合は、 `--failure` オプションで失敗ハンドラーを指示できます。

 bash
```
 % pypyr 36_own_failure_handler --failure arb_group
 A
 Error while running step pypyr.steps.py at pipeline yaml line: 5, col: 5
 Something went wrong. Will now try to run arb_group.
 C
 
 ValueError: arb
 
```


### パイプラインの呼び出し時に指示
pypeを使って他のパイプラインの中からパイプラインを呼び出した場合、デフォルトの `on_failure` をオーバーライドすることができます。
 `pypyr.steps.pype` を使って別のパイプラインの中からパイプラインを呼び出す場合、デフォルトの `on_failure` をオーバーライドして独自の `on_failure` を設定することができます。

 37_own_failure_from_pipeline.yaml
```
 steps:
   - name: pypyr.steps.pype
     in:
       pype:
         name: 36_own_failure_handler
         failure: arb_group
         
```

 bash
```
 % pypyr 37_own_failure_from_pipeline
 A
 Error while running step pypyr.steps.py at pipeline yaml line: 5, col: 5
 Something went wrong. Will now try to run arb_group.
 C
 Something went wrong pyping 36_own_failure_handler. ValueError: arb
 Error while running step pypyr.steps.pype at pipeline yaml line: 2, col: 5
 Something went wrong. Will now try to run on_failure.
 
 ValueError: arb
```


### パイプライン内から指示
パイプライン内で別のステップグループを呼び出したり、ジャンプしたりする際に、独自の失敗ハンドラを指定することができます。

 38_call_with_failure_group.yaml
```
 steps:
   - name: pypyr.steps.echo
     in:
       echoMe: A
   - name: pypyr.steps.call
     in:
       call:
         groups: call_me
         failure: arb_group
   - name: pypyr.steps.echo
     in:
       echoMe: unreachable
 
 call_me:
   - name: pypyr.steps.echo
     in:
       echoMe: B
   - name: pypyr.steps.assert
     in:
       assert: False
   - name: pypyr.steps.echo
     in:
       echoMe: unreachable
 
 arb_group:
   - name: pypyr.steps.echo
     in:
       echoMe: C
       
```

 bash
```
 % pypyr  38_call_with_failure_group
 A
 B
 Error while running step pypyr.steps.assert at pipeline yaml line: 18, col: 5
 Something went wrong. Will now try to run arb_group.
 C
 Error while running step pypyr.steps.call at pipeline yaml line: 5, col: 5
 Something went wrong. Will now try to run on_failure.
 
 AssertionError: assert False evaluated to False.
```


### 失敗ハンドラーをcall と jump
失敗ハンドラで呼び出しやジャンプを行うことができます。これは、エラー時と成功時で異なる条件で実行したい共有コードや共通コードがある場合に便利です。典型的なシナリオは、成功時と失敗時の両方で通知を送りたい場合です。
 3(_call_on_failure.yaml
```
 steps:
   - name: pypyr.steps.assert
     in:
       assert: False
   - name: pypyr.steps.echo
     in:
       echoMe: unreachable
 
 sg1:
   - name: pypyr.steps.echo
     in:
       echoMe: B
   - name: pypyr.steps.call
     in:
       call: sg2
   - name: pypyr.steps.echo
     in:
       echoMe: D
 
 sg2:
   - name: pypyr.steps.echo
     in:
       echoMe: C
 
 on_failure:
   - name: pypyr.steps.echo
     in:
       echoMe: A
   - name: pypyr.steps.call
     in:
       call: sg1
   - name: pypyr.steps.echo
     in:
       echoMe: E
       
```

 bash
```
 % pypyr  39_call_on_failure
 Error while running step pypyr.steps.assert at pipeline yaml line: 2, col: 5
 Something went wrong. Will now try to run on_failure.
 A
 B
 C
 D
 E
 
 AssertionError: assert False evaluated to False.
 
```

呼び出されたグループは、別のグループを呼び出すこともできることに注意してください。

失敗ハンドラーからジャンプしても、失敗ハンドラーの実行コンテキスト内にいることになります。つまり、ジャンプ先のグループが完了しても、実行チェーンのどこかでStop命令を使用しない限り、pypyrは失敗を報告して終了します。

### パイプラインを失敗ハンドラーで終了させない 
パイプラインの失敗ハンドラが完了すると、デフォルトでは、pypyrは失敗を報告してパイプラインを終了します。エラーを処理して、成功を報告するパイプラインを終了させたい場合は、Stop命令を使って失敗ハンドラが完了してエラーが発生するのを防ぐことができます。

pypyrを完全に停止させたいのか、パイプラインのみを停止させたいのか、現在呼び出されているグループやジャンプしたグループのみを停止させたいのかによって、stop、stoppipeline、stopstepgroupのいずれかを使用することができます。

 40_stop_on_failure.yaml
```
 steps:
   - name: pypyr.steps.assert
     in:
       assert: False
   - name: pypyr.steps.echo
     in:
       echoMe: unreachable
 
 on_failure:
   - name: pypyr.steps.echo
     in:
       echoMe: A
   - pypyr.steps.stop
   - name: pypyr.steps.echo
     in:
       echoMe: unreachable
       
```

このパイプラインを実行してみます。

 bash
```
 % pypyr  40_stop_on_failure
 Error while running step pypyr.steps.assert at pipeline yaml line: 2, col: 5
 Something went wrong. Will now try to run on_failure.
 A
 
 % echo $?
 0
 
```

終了コードがゼロ( `0` )になっていることに注目してください。

失敗ハンドラ内で `call` や  `jump` を使用した場合、呼び出したグループ内で適切なStop命令を発行することができます。


### パイプライン内でランタイムエラーの詳細を使用する
pypyrはすべてのランタイムエラーをコンテキスト内の `runErrors` というリストに保存します。

 YAML
```
 runErrors:
   - name: エラー名
     description: エラーの詳細
     customError: # wステップ定義のonErrorに入れたもの
     line: 1 # 失敗したステップのパイプラインの行
     col: 1 # 失敗したステップのパイプラインのカラム
     step: my.bad.step.name # 失敗したステップ名
     exception: ValueError('arb') # 実際のPythonエラーオブジェクト
     swallowed: False # errがswallowされていたらtrue
```

エラーが発生すると `runErrors` に情報が追加されていきます。つまり、最初のエラーはリストの最初にあり、直近に発生したエラーはリストの最後にあります。

### 後続のステップでのエラー情報の使用
ステップグループの失敗ハンドラで  `runErrors` を使用することができます。また、失敗したステップで  `swallow: True` を設定した場合、後続のステップで  `runErrors` を使用して実際のエラー情報を使用することができます。

 41_use_error_info.yaml
```
 steps:
   - name: pypyr.steps.echo
     in:
       echoMe: A
   - name: pypyr.steps.assert
     swallow: True
     in:
       assert: False
   - name: pypyr.steps.echo
     in:
       echoMe: there was a problem on line {runErrors[0][line]}
   - name: pypyr.steps.py
     in:
       py: raise ValueError('arb')
   - name: pypyr.steps.echo
     in:
       echoMe: unreachable
 
 on_failure:
   - name: pypyr.steps.echo
     in:
       echoMe: B
   - name: pypyr.steps.assert
     in:
       assert:
         this: '{runErrors[0][name]}'
         equals: AssertionError
   - name: pypyr.steps.assert
     in:
       assert:
         this: '{runErrors[1][name]}'
         equals: ValueError
   - name: pypyr.steps.assert
     in:
       assert:
         this: '{runErrors[1][description]}'
         equals: arb
         
```

 bash
```
 % pypyr  41_use_error_info
 A
 pypyr.steps.assert Ignoring error because swallow is True for this step.
 AssertionError: assert False evaluated to False.
 there was a problem on line 5
 Error while running step pypyr.steps.py at pipeline yaml line: 12, col: 5
 Something went wrong. Will now try to run on_failure.
 B
 
 ValueError: arb
 
```

### エラー情報の追加 
onError デコレーターを使用すると、独自の追加説明や独自のオブジェクトをエラーに追加することができます。

 42_on_error.yaml
```
 steps:
   - name: pypyr.steps.assert
     comment: カスタム・エラー・オブジェクトで
              意図的にエラーを発生させる
     in:
       assert: False
     onError:
       myerr_code: 123
       myerr_description: "my err description"
 
 on_failure:
   - name: pypyr.steps.echo
     comment: カスタムエラーは runErrors にある
     in:
       echoMe: |
         the error code: {runErrors[0][customError][myerr_code]}
         the error description: {runErrors[0][customError][myerr_description]}
         
```

 bash
```
 % pypyr 42_on_error
 Error while running step pypyr.steps.assert at pipeline yaml line: 2, col: 5
 Something went wrong. Will now try to run on_failure.
 the error code: 123
 the error description: my err description
 
 
 AssertionError: assert False evaluated to False.
```



### カスタムエラーを発生させる
pypyrでは独自のエラーを発生させることができます。最も簡単には、組み込みの `assert` を使用しますが、Pythonの組み込みエラーを発生させることもできます。

### assertionエラー 
assertを使って、アサーション条件が失敗した場合にエラーを発生させることができます。

 43_asser_error.yaml
```
 steps:
   - name: pypyr.steps.assert
     in:
       assert: False
   - name: pypyr.steps.echo
     comment: this step won't ever run because pipeline always
              fails on previous step.
     in:
       echoMe: unreachable
       
```

 `AssertionError` 例外を発生させるかどうかは `assert` の条件に依存していて、条件には `'{token}'` のように置換を使用することができます。

### カスタムエラー 
インラインの python ステップから任意の組み込み Python 例外を発生させることができます。

また、通常のPythonモジュールのインポート参照に従って、適切なモジュールを  `py` ステップの一部としてインポートすれば、pypyrのビルトインエラーや独自のカスタムエラーオブジェクトを発生させることもできます。

 44_pyhton_error.yaml
```
 steps:
   - name: pypyr.steps.echo
     in:
       echoMe: begin
   - name: pypyr.steps.py
     in:
       py: raise ValueError('arb error text here')
   - name: pypyr.steps.echo
     comment: this step won't ever run 
              because pipeline always
              fails on previous step.
     in:
       echoMe: unreachable
       
```

 bash
```
 % pypyr  44_python_error
 begin
 Error while running step pypyr.steps.py at pipeline yaml line: 5, col: 5
 Something went wrong. Will now try to run on_failure.
 
 ValueError: arb error text here
 
```

## カスタム引数をコマンドラインから渡す
別途コードを書くことなく、独自の引数をパイプラインに渡すことができます。パイプラインごとに、Key-Valueのペア、単一の文字列、ブーリアンスイッチなど、どのようなスタイルの引数がそのパイプラインに適しているかを決めることができます。

 50_cli_switches.yaml
```
 context_parser: pypyr.parser.keys
 steps:
   - name: pypyr.steps.default
     in:
       defaults:
         isCI: False
         isRetry: False
   - name: pypyr.steps.echo
     run: '{isRetry}'
     in:
       echoMe: you'll only see me if IsRetry is True
   - name: pypyr.steps.echo
     run: '{isCI}'
     in:
       echoMe: this only runs in the CI environment, not on dev
   - name: pypyr.steps.echo
     in:
       echoMe: done!
       
```


 bash
```
 % pypyr 50_cli_switches
 done!
 
 % pypyr 50_cli_switches isRetry
 you'll only see me if IsRetry is True
 done!
 
 % pypyr 50_cli_switches isRetry isCI
 you'll only see me if IsRetry is True
 this only runs in the CI environment, not on dev
 done!
 
 % pypyr 50_cli_switches isCI IsRetry
 this only runs in the CI environment, not on dev
 done!
 
```

ここまでの説明では、pypyr の全ての機能を説明できてはいません。しかし、タスクランナーとしての有益性は理解できるのではないでしょうか？

## まとめ
pypy を使うと定期的、定常的に実行されるような作業をコード化することができます。つまり、工程を人的作業からコードにすることで、工程の再現性を確実にしつつ、事前事後でのレビューを容易にすることで品質向上につながります。作業内容をバージョン管理を行うことができるようになるわけです。


## 参考
- [pypyr オフィシャルサイト ](https://pypyr.io/)
- [pypyr ソースコード ](https://github.com/pypyr/pypyr)

#タスクランナー


