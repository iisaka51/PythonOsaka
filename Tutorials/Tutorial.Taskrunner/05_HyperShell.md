hyper-shellを使ってみよう
=================
## hyper-shell について
Hyper-shellは、シェルコマンドを分散型非同期キューで処理する、エレガントでクロスプラットフォームなハイパフォーマンス・コンピューティング・ユーティリティです。
クラスタシステムや分散環境での実行に適したツールです。

- シンプル(SImple)、スケーラブル(Scalable)、弾力的(Elastic)
ハイパーシェルでは、シェルコマンドのリストを取得し、それらを並列に処理することができます。利用可能なクラスタモードを使ってローカルに処理したり、SSHやMPIを使って自動的にスケールアウトしたり、SlurmのようなHPCスケジューラやKubernetesを使ってクラウドで弾力的にスケールするようにParslを設定したりすることができます。

 bash
```
 $ seq -w 10000 | hyper-shell cluster -N24 -t 'echo {}' | tail -4
 09997
 09998
 09999
 10000
 
```

- フレキシブル(Flexible)
ハイパーシェルの斬新な機能は、あるマシンで独立してサーバーを立ち上げ、別の環境からクライアントを使ってそのサーバーに接続することができることです。

ハイパーシェルサーバーを起動し、バインドアドレスを0.0.0.0に設定してリモート接続を許可します。サーバーは、ファイル（または標準入力）からタスクを読み込み、キューに発行し、失敗したコマンドをファイル（または標準出力）に記録するという、ふるい落としのような役割を果たします。

 bash
```
 $ hyper-shell server -H 0.0.0.0 -k MY_KEY < TASKFILE > TASKFILE.failed
 
```

稼働中のサーバーに、別のホストから（Windowsなどの別のプラットフォームからでも）接続できます。任意の数のホストから任意の数のクライアントで接続することができます。それぞれのクライアントの接続は、非同期的に個々のタスクをキューから取り出し、負荷分散させることができます。

 bash
```
 $ hyper-shell client -H host-1 -k MY_KEY > TASKFILE.out
 
```

- 動的(Dynamic)
個々のタスクには特別な変数が自動的に定義されます。例えば、TASK_IDは、各タスクに一意の整数識別子を与えます（どのクライアントがタスクを実行するかに関わらず）。

また、HYPERSHELL_という接頭辞をつけて定義された環境変数は、接頭辞なしで各タスクの環境に注入されます。

t (short for --template) を使用してテンプレートを実行し、"{}" を使用して入力タスクの引数を挿入できます (代わりに TASK_ARG を使用してください)。コマンドラインを入力したシェルに変数の展開させないために、必ずシングルクォートを使用するようにしてください。

 bash
```
 $ hyper-shell cluster -t '{} >outputs/$TASK_ID.out'
 
```

## インストール
hypyer-shell は pip でインストールします。

 bash
```
 $ pip install hyper-shell
 
```

hyper-shell 自体は自体はどこにでもインストールできますし、どのように起動されるかは気にしません。ただし、- `-ssh` などでクライアントを起動する場合は、起動先のホストに互換性のあるバージョンの hyper-shell がインストールされている必要があります。
SingularityやDockerなどのコンテナ内にhyper-shellをインストールする場合は注意が必要です。MPIライブラリは、コンテナの内と外とで互換性がある必要があります。

Parslライブラリは、独自のコマンドを起動しようとするため、状況によってはうまく動作させるのが難しい場合があります。
また、HPCのような共有システムでは、Parslのインストールを自分自身に公開するようにしておう必要があります。

共有システム上では、venv などの仮想環境や Anaconda 環境にインストールして、バイナリと特定のライブラリだけを外に参照することで、hyper-shell を他のユーザーの Python 環境から隔離することが推奨されます。


- **Anaconda でのhyper-shell の隔離**
 bash
```
 $ conda create -y --name hyper-shell python==3.9
 $ conda activate hypter-shell
 (hyper-shell) $ pip install hypter-shell
 
```

- **venv での hypter-shell の隔離**
 bash
```
 $ mkdir $HOME/envs
 $ python -m venvs $HOME/envs/hyper-shell
 $ source $HOME/envs/hypter-shell/bin/activate
 (hypter-shell) $ pip install hypter-shell
```

venv ではシステムにイントールされているPython のバージョンが踏襲され、他のバージョンを使用することができないことに注意してください。
上記のようなディレクトリ構成では、次のようなスクリプト使用すると、複数のPython 環境があるときに便です。

 bash
```
 ENVDIR=${HOME}/envs
 case $1 in
 "")
     PS3="Select python env. Enter 'q' for exit! > "
     menu=$( cd ${ENVDIR} ; ls -1d * )
     item=""
     select item in ${menu}
     do
         if [ "${REPLY}" != "q" ]; then
             if [ -n "${item}" ]; then
                 source ${ENVDIR}/${item}/bin/activate
                 break
             else
                 echo "invalid selection."
             fi
         else
             echo "nothing to do."
             break
         fi
     done
 ;;
 *)
     item=$1
     if [ -d ${ENVDIR}/${item} ] ; then
         source ${ENVDIR}/${item}/bin/activate
     else
         echo "${item}: no such venv."
         echo "You can only select follows."
         (cd ${ENVDIR}; ls -1d *)
     fi
 ;;
 esac
 
```

使用方法は次のとおり。

 bash
```
 $ source $HOME/envs/enable hypyer-shell
 
```

引数を省略すると、作成されている Python 環境を番号付きで表示されます。番号を入力すると、そのPython 環境が’有効になります。


## 基本的な使い方
ほとんどの場合、clusterサブコマンドを使用することになります。 `TASKFILE` というファイルがあり、その中に単独で実行するコマンドが、各行を連続して実行するすように記載されている場合、そのファイルをhyper-shellに渡すことで、それらのコマンドは並行して処理されます。

 nash
```
 $ hyper-shell cluster TASKFILE
 
```

同時に実行するタスクの数を指定するには、 `--num-cores` （もしくは  `-N` ）オプションを使用します。

 bash
```
 $ hyper-shell cluster TASKFILE -N16
 
```

個々のコマンドがシングルコアで動作すると仮定すると（それ自体は並列アプリケーションではありません）、システムのコア数と同じ数を使用する必要があります（指定しない場合は、hyper-shellが自動的に行います）。

何らかの理由でコマンドが失敗することがあります。どの入力コマンドの終了ステータスがゼロでなかったかを追跡するには、 `--failed` （あるいは  `-f` ）オプションを指定します。この出力ファイルには、失敗した入力ファイルの行が含まれます。

 bash
```
 $ hyper-shell cluster TASKFILE -N16 -f TASKFILE.failed
 
```


## 使用方法
hyper-Shellはある程度は、使用方法のドキュメントが内包されています。

トップレベルのコマンドを引数なしで実行すると、基本的な使用法が表示されます。トップレベルのコマンドに  `--help` オプションを渡すと、完全なヘルプリストが表示されます。

 bash
```
 % hyper-shell
 usage: hyper-shell <command> [<args>...]
        hyper-shell [--help] [--version]
 
 A cross-platform, high performance computing utility for processing
 shell commands over a distributed, asynchronous queue.
 
```

ここで提供されているのと同じドキュメントの多くは、マニュアルページを見ることでコマンドラインから直接見ることができます。

 bash
```
 $ man hyper-shell
 
```

## Serverサブコマンドの使用方法
server サブコマンドは、ファイル（または標準入力）からコマンドラインを読み込み、分散したキューに公開します。

ゼロ以外の終了ステータスを返したコマンドには警告メッセージが表示され、元のコマンドラインはファイル（または標準出力）に書き込まれます。このようにして、サーバーはコマンドを処理して、失敗を排出する「ふるい」のような役割を果たします。

入力コマンドラインから 、コマンドファイル TASKFILE が与えられた場合、以下のようになります。

 bash
```
 $ hyper-shell server - < TASKFILE > TASKFILE.failed
 
```

作成されたTASKFILE.failedには、TASKFILEからの行のサブセットが含まれます。

引数がない場合は、使用状況を表示して終了します。

 bash
```
 % hyper-shell server
 usage: hyper-shell server FILE [--output FILE] [--maxsize SIZE]
                           [--host ADDR] [--port PORT] [--authkey KEY]
                           [--verbose | --debug] [--logging]
                           [--help]
 
 Run the hyper-shell server.
 
```

- **-o, --output PATH**
0以外の終了ステータスを返したコマンドラインを書き込むためのファイルのパスです。パスが指定されていない場合は、標準出力に表示されます。

- **-s, --maxsize SIZE**
キューの最大サイズを指定します（デフォルト：10000）。サーバーがあまりにも多くのタスクをキューに入れるのを避けるために、これは、クライアントがまだ十分なコマンドを取っていない場合、サーバーを強制的にブロックします。これはパイプラインの場合に有益です。

## client サブコマンドの使用方法
client サブコマンドは、サーバーに接続してコマンドを1つずつ取り出し、ローカルシェルで実行します。シェルと環境は、クライアントの実行環境を継承します。

コマンドの出力は、 `--output` オプション で指定されていない限り、そのまま標準出力にリダイレクトされます。個々のコマンドからの出力を分離するために、コマンドテンプレートの内部からリダイレクト方法を指定することができます。

 bash
```
 $ hyper-shell client -t '{} >$TASK_ID.out'
 
```

引数がない場合、クライアントは使用状況を表示して終了します。

 bash
```
 % hyper-shell client
 usage: hyper-shell client [--host ADDR] [--port PORT] [--authkey KEY] [--timeout SEC]
                           [--template CMD] [--output FILE]
                           [--verbose | --debug] [--logging]
                           [--help]
 
 Run the hyper-shell client.
 
```

- **-x, --timeout SEC**
接続を切断するまでの時間を秒単位で指定します（デフォルト：0）。前のコマンドが終了し、この時間が経過してもサーバーから他のコマンドが発行されない場合、自動的に切断してシャットダウンします。タイムアウトが0の場合は特別で、決してタイムアウトしないことを意味します。

タスクがないときは10分後に自動的に切断してシャットダウンするには次のように起動します。

 bash
```
 $ hyper-shell client -x600
 
```

- **-t, --template CMD**
テンプレートコマンド（デフォルト： `"{}"` ）。有効なコマンドであればテンプレートになります。すべての `"{}"` は、入力タスクの引数として（存在すれば）置換されます。これは、他のコマンドや場所から引数をパイピングし、コマンドは入力引数以外はすべて同じである場合に便利です。

いくつかのスクリプト、my_codeに対して呼び出される引数として入力タスクを処理し、タスクによる出力を分離する。

 bash
```
 $ hyper-shell client -t 'my_code {} >outputs/{}.out'
 
```

- **-o, --output PATH**
コマンドの出力を書き込むためのファイルのパスです。パスが指定されていない場合は、標準出力に出力されます。

シェルのリダイレクトを使用する代わりに、出力を明示的に指定したファイルパス（outputs.txt）に書き込みます。

 bash
```
 $ hyper-shell client -o outputs.txt
 
```


すべてデフォルト引数を使って実行するようにクライアントに促すためには、二重のハイフォン記号( `--` )を与えます。これは引数なし(noarg)として解釈されます。

 bash
```
 $ hyper-shell client --
 
```


## cluster サブコマンド使用方法
clusterサブコマンドは、いくつかの一般的なシナリオの下で、サーバーとクライアントを起動するプロセスを自動化する便利な方法です。

例えば、16台のクライアントを起動するためには  `-N16` オプションを与えて実行とします。

他のマシンから自動的にクライアントを起動するためには、状況に応じて SSH または MPI を使用します。専用のホストや特別に設定されたホストでは、SSH は単にログインして接続を返します。ハイパフォーマンス・コンピューティング・クラスターのような大規模な共有システムでは、通常、ソフトウェアをロードしたり起動したりする必要があり、ログイン時に利用できるとは限りません。mpiexecコマンドは、sshと似ていますが、接続先の環境が同一であるという利点があります（例えば、カレントディレクトリとロードされたソフトウェアがすべて同じであること）。

最後に、hyper-shell は Parsl を使用して弾力的に拡張することができます。有効な名前付きの設定（~/.hyper-shell/parsl_config.pyから）であれば、どのようなものでも起動できます。(詳細はParslのドキュメントを参照)

引数がない場合、クラスタは使用状況を表示して終了します。

 bash
```
 % hyper-shell cluster
 usage: hyper-shell cluster [FILE] [-f FILE] [-o FILE] [-p NUM] [-s SIZE] [-t CMD] [-k KEY]
                            [--local [--num-cores NUM] | (--ssh | --mpi) --nodefile FILE |
                             --parsl [--profile NAME]]
                            [--verbose | --debug] [--logging]
                            [--help]
 
 Run the hyper-shell cluster.
 This launches clients using one of the available schemes.
 
```

各並列化モードは相互に排他的です。関連するパートナーオプションは、その親ランチャーと一緒に与えられた場合のみ有効です。

>資料の表記上の注意
>この資料の公開している scrapbox の仕様上の問題で、省略可能なオプションを括弧( `(...)` )で表記しています。

- **--local   ( -N | --num-cores NUM ` )**
クライアントをローカルに起動します。要求された「コア」ごとに新しいクライアントプロセスが開始されます。デフォルトでは、マシン上のコア数と同じ数のクライアントを起動します。これらのクライアントは、現在の実行ファイルへの正確なパスを使用して起動します。

- **--ssh ( --nodefile FILE )**
SSHでクライアントを起動します。nodefile には、使用するホストを列挙する必要があります。このファイルの各行ごとに SSH セッションが作成されます。パスワードなしで接続できるように SSH-keys を設定してください。グローバルな ~/.hyper-shell/nodefile が存在する場合は、それをデフォルトとして使用できます。

- **--mpi ( --nodefile FILE )**
MPIでクライアントを起動します。FILE は mpiexec の -machinefile オプションに渡されます。与えられていない場合は、何をすべきかを知るために mpiexec に依存します。

- **--parsl ( --profile NAME )**
parsl モードで動作する単一のクライアントを起動します。これは、~/.hyper-shell/parsl_config.py から parsl.config.Config オブジェクトをロードします。指定しない場合、プロファイルのデフォルトは「local」で、ローカルでいくつかのスレッドを使用します。

これらのオプションは、サーバまたはクライアントの起動時に渡されます。


- **-f, --failed FILE**
0 以外のステータスで終了したコマンドを書き込むためのファイルパスを指定します。指定されない場合は、何も書き込まれません。

- **-o, --output FILE**
コマンドの出力を書き込むファイルのパスです。デフォルトでは、このオプションが指定されていない場合、すべてのコマンドの出力は標準出力にリダイレクトされます。

- **-s, --maxsize SIZE**
キューの最大サイズ（デフォルト：10000）。サーバーがあまりにも多くのタスクをキューに入れるのを避けるために、これは、クライアントがまだ十分なコマンドを取っていない場合、サーバーを強制的にブロックします。これはパイプラインに役立ちます。

- **-t, --template CMD**
テンプレートコマンド（デフォルト： `"{}"` ）。

]
[*** ネットワークオプション
ハイレベルクラスターモードを使用する場合、ネットワークオプションは必要ありません。つまり、サーバーはポートを介して共有キューを管理しています。デフォルトでは、hyper-shellはポート50001を使用します。これは任意であり、システムで許可されていれば他のポート番号を使用することができます。

クライアントがサーバー・インスタンスに接続する際には、一意の認証キーの提供が求められます。この鍵は、数字と文字の連続した有効な文字列であれば何でも構いません。長さや品質に関する特定の要件はありません。デフォルトの認証キーは（--BADKEY--として）定義されていますが、これは他の安全な環境での使用を容易にするためのものです。

クラスタモードでの実行時には、安全な認証キーが自動的に生成され、クライアントに使用されます。

- **-H, --host ADDR**
使用するホスト名またはIPアドレスです。サーバーの場合は、これがバインドアドレスになります（デフォルト：localhost）。これを変更して、リモート接続を可能にすることもできます（例：0.0.0.0）。同一マシン上にない場合、クライアントはホスト名またはIPアドレスを指定する必要があります。

サーバーを起動し、バインドアドレスを設定してリモートクライアントを許可します。

 bash
```
 $ hyper-shell server -H 0.0.0.0
 
```

クライアントが host-1 で動作しているサーバに接続するためには次のように実行します。

 bash
```
 $ hyper-shell client -H host-1
 
```

- **-p, --port PORT**
サーバーのポート番号です（デフォルト：50001）。ポート番号は任意に選択でき、システムで許可されていれば（ブロックや予約されていなければ）他のポート番号でも構いません。

サーバーの起動時に特定のポート番号を指定します。

 bash
```
 $ hyper-shell server -H 0.0.0.0 -p 54321
 
```

クライアントがこのサーバーに接続するためには、次のように実行します。

 bash
```
 $ hyper-shell client -H host-1 -p 54321
 
```

- **-k, --authkey KEY**
クライアント接続用の暗号認証キー（デフォルト： `--BADKEY--` ）。これはサーバーが設定し、クライアントが接続する際に必要となります。既定値は、より適切なものを設定するように意図されています。クラスタモードでは、セキュアキーが明示的に提供されていない場合、自動的に生成されます。

サーバーインスタンスに特定の認証キーを使用します。

 bash
```
 $ hyper-shell server -H 0.0.0.0 -k MY_SPECIAL_KEY
 
```

クライアントがキーを使ってサーバーに接続するためには、次のように実行します。

 nash
```
 $ hyper-shell client -H host-1 -k MY_SPECIAL_KEY
 
```


## ロギングオプション
すべてのログメッセージは標準エラーに書き込まれ、コマンド出力だけが標準出力に書き込まれるようになっています。Hyper-Shellのログメッセージは、 `DEBUG` 、 `INFO` 、 `WARNING` 、 `ERROR` 、 `CRITICAL` の5つのレベルで構成されています。特定のロギングレベルを設定すると、そのレベル以下のメッセージは抑制されます。

デフォルトでは、ロギングレベルは `WARNING` に設定されており、何らかの問題（タスクの終了ステータスがゼロでないなど）が発生しない限り、メッセージは表示されません。情報メッセージ（タスクがキューに入った、実行された、完了したなど）を表示するには、 `--verbose` オプションを使用します。デバッグメッセージ（クライアントの接続や切断など）を表示するためには  `--debug` オプション を使用します。

これらのレベルに加えて、ロギングには2つのモードがあります。通常のモードは、対話的な使用を目的としており、メッセージのレベルに応じて色分けされます。また、--loggingオプションで設定できるsyslogスタイルのメッセージングもあります。このモードでは色がつかず、ホスト名やタイムスタンプなどの追加メタデータが表示されます。これは、パイプラインやジョブのように、長い時間、離れた場所で実行される場合に重要です。

ロギングメッセージは重大度に応じて色分けされます。標準エラー出力がリダイレクトされている場合が色は無効になります。

-  `DEBUG` ：青
-  `INFO` ：緑
-  `WARRNING` ：黄
-  `ERROR` ：赤
-  `CRITICAL` ：紫

タスクの終了ステータスが 0 以外の場合は、エラーではなく警告とみなされます。criticalメッセージは、hyper-shellの実行を継続できない場合に表示されます。

- **-v, --verbose**
情報レベルのメッセージを含みます。(--debugと競合します)。

- **-d, --debug**
デバッグレベルのメッセージを表示します。(--verbose と競合します)。

- **-l, --logging**
詳細な syslog 形式のメッセージを表示します。これは、色付きの出力を無効にし、タイムスタンプ、ホスト名、レベル名を含むメッセージのフォーマットを変更します。


## 環境変数
この資料作成している時点でのバージョン 1.8.3 では、hyper-shell の設定ファイルはありません。しかし、hyper-shellの動作は、さまざまな環境変数の影響を受けます。

hyper-shellで定義されている変数はいくつかあります。これらはタスクごとに設定され、そのタスクに固有の情報で構成されています。これらの変数は、コマンドラインの本文の中で使用できます。


- **TASK_ID**
このタスクに固有の整数の識別子です。TASK_IDの値は、サーバーによって設定されたゼロから始まるカウントです。

- **TASK_ARG**
このコマンドの入力引数です。これは'{}'に相当する変数で、そのように代入することができます。これは、コマンドのテンプレートにシェルの機能を持たせる場合に便利です。

入力ファイルのパスからファイル名の拡張子を取り除きます。

 bash
```
 $ hyper-shell client -t 'my_code ${TASK_ARG%.*}'
 
```

ハイパーシェルの動作に影響を与える環境変数がいくつか定義されています。


- **HYPERSHELL_EXE**
クラスタを--ssh（または同様のもの）で実行する場合、リモートシステム上のhyper-shellが別の場所にあったり、PATH上で必ずしも利用できないことがよくあります。HYPERSHELL_EXE環境変数を使用して、使用する明示的なパスを設定します。

 bash
```
 $ export HYPERSHELL_EXE=/path/to/other/bin/hyper-shell
```


- **HYPERSHELL_CWD**
ハイパーシェル・クライアントを直接実行すると、クライアントが実行されているのと同じディレクトリでタスクが実行されます。これは、 `HYPERSHELL_CWD` を指定することで変更できます。

 bash
```
 $ export HYPERSHELL_CWD=$HOME/other
```


- **HYPERSHELL_LOGGING_LEVEL**
この変数を定義することで、コマンドラインスイッチを必要とせずに、使用するログレベルを指定できます。番号付きの値と名前付きの値の両方が許可されます。例えば、0～4、またはDEBUG、INFO、WARNING、ERROR、CRITICALのうちの1つです。

 bash
```
 $ export HYPERSHELL_LOGGING_LEVEL=DEBUG
 
```

- **HYPERSHELL_LOGGING_HANDLER**
この変数を定義することで、コマンドラインスイッチを必要とせずに、使用するログスタイルを指定できます。許容される値は STANDARD または DETAILED で、それぞれ基本的な色付きメッセージと syslog スタイルの詳細メッセージに対応します。

 bash
```
 $ export HYPERSHELL_LOGGING_HANDLER=DETAILED
 
```

 `HYPERSHELL_` の接頭辞で始まるすべての環境変数は、接頭辞を取り除いたタスクの実行環境に受け継がれます。

 bash
```
 $ export HYPERSHELL_PATH=/other/bin:$PATH
 $ export HYPERSHELL_OTHER=FOO
```

これにより、すべてのタスクに　 `PATH=/other/bin:$PATH` が定義され、さらに環境変数  `OTHER=foo` が定義されます。

## Parslモード

Hyper-Shellでは、シェル・コマンドを実行するスケジューラとしてParslを使用し、すべてのスケーリングを処理することができます。この目的のためには、有効なParslの設定がすべて機能するはずです。

初期状態では、hyper-shellはデフォルトの設定ファイルを  `~/.hyper-shell/parsl_config.py` に置きます。

 parsl_config.py
```
 # Hyper-shell Parsl configuration file.
 # ハイパーシェルのParsl設定ファイルです。
 
 # Import and create configuration objects via Parsl.
 # Parsl経由で設定オブジェクトをインポート、作成します。
 
 # Hyper-shell will import this module and inspect for Python
 # objects by name that have type  `parsl.config.Config` .
 # Hyper-shellはこのモジュールをインポートして、Pythonのオブジェクトのうち、
 # タイプが  `parsl.config.Config` であるものを名前で検査します。
 
 # default configuration, do not remove this line
 # デフォルトの設定なので、この行は削除しないでください
 from parsl.configs.local_threads import config as local
 
```


コメントにあるように、このモジュールファイルが実行されると、そこに定義されているConfigオブジェクトは、ローカルに定義された名前でエクスポートされます。その名前は  `--profile` オプションを使ってコマンドラインから呼び出すことができます。

初期状態では、local はデフォルトの parsl 設定で、単にローカルのスレッドを使ってタスクを実行します。


## 参考
- [hyper-shell ソースコード ](https://github.com/glentner/hyper-shell)
- [hyper-shell ドキュメント ](https://hyper-shell.readthedocs.io/en/latest/)
- [Parsl オフィシャルサイト ](https://parsl-project.org/)


