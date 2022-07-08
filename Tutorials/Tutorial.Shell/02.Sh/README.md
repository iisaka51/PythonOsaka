shモジュールを使って外部コマンドを呼び出してみよう
=================
## shモジュールについて
shモジュールは、システムのコマンドをPythonにマップする独自のsubprocessのラッパーモジュールです。
sh は、ほぼすべてのコマンドをPython の関数ように実行することができます。そして、重要なことは、subprocess.popenを使用するよりも、はるかに簡単に出力を取り込むことができるということです。

## shのインストール
sh モジュールをインストールするためには次のように実行します。
 bash
```
 $ pip install sh
```


## shの使用方法
sh の利用方法は、非常に簡単で、shを直接インポートするか、shからコマンドを"インポート"することです。 面白いことに、実行するすべてのコマンドは、他のモジュールと同じようにインポートすることができ、Pythonの関数のように使用できます。
引数は通常どおりに渡され、出力は戻り値として取り込むことができます。


```
 In [2]: # %load 01_intro.py
    ...: import sh
    ...:
    ...: v1 = sh.ls()
    ...: v2 = sh.ls("-l")
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
```

 `from sh import コマンド名` の形式でインポートして使用することもできます。

```
 In [2]: # %load 02_import_cmd.py
    ...: from sh import ls
    ...:
    ...: v1 = ls()
    ...:
    ...: v2 = ls("-l")
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
    
```

ごのように、コマンドは関数と同じように呼び出されます。
#### Pythonの関数ではなく、バイナリコマンドを実行している

## コマンドが使えるかスクリプトから確認
sh は、シェルと同じように、環境変数PATHを解決してコマンドを実行していることは説明しました。スクリプトから実行されているプラットフォームでコマンドが使えるかどうか確認したいような場合は次のようにします。


```
 In [2]: # %load 03_which.py
    ...: import sh
    ...:
    ...: has_ansible = sh.which("ansible") is not None
    ...: if not has_ansible:
    ...:     print("You should install ansible.")
    ...:
 You should install ansible.
 
```


## コマンドに引数やオプションを与える
コマンドに引数やオプションを与える場合は、それぞれの引数を文字列を分割する必要があります。これは、バックエンドの `subprocess.call()` に依存しているためです。

次のコードは動作しない例です。


```
 In [2]: # %load 04_cmd_not_work.py
    ...: from sh import ls
    ...:
    ...: ls("-l /tmp/dummyfile")
    ...:
 ---------------------------------------------------------------------------
 ErrorReturnCode_1                         Traceback (most recent call last)
 （中略)
 ErrorReturnCode_1:
 
   RAN: /bin/ls '-l /tmp/dummyfile'
 
   STDOUT:
 
 
   STDERR:
 /bin/ls: illegal option --
 usage: ls [-@ABCFGHLOPRSTUWabcdefghiklmnopqrstuwx1%] [file ...]
 
```

コマンドの引数がひとつの文字列 `'-l /tmp/test.tar'` として渡されていることがわかります。

少し面倒ですが、次のように引数ごとに分割して与えます。


```
 In [2]: # %load 05_cmd_work.py
    ...: from sh import ls
    ...: 
    ...: v1 = ls("-l", "/tmp/dummyfile")
    ...: # print(v1)
    ...:
    
```

次のようにすると、シェルでのコマンドラインでの指定に近くなり、読みやすいでしょう。ただし、この方法は１つのコマンドを実行する場合ではよいのですが、後述するパイプなどの処理では、かえって可読性が悪くなることに注意してください。


```
 In [2]: # %load 06_cmd_run.py
    ...: from sh import ls
    ...: import shlex
    ...:
    ...: cmd = "ls -l /tmp/dummyfile"
    ...: v1 = ls(shlex.split(cmd)[1:])
    ...:
    ...: # print(v1)
    ...:
    
```

 `shlex.split()` は シェルに似た文法を使って、文字列 を分割してリストにするものです。

## キーワード引数として渡す
コマンドに引数やオプションを与える場合に、オプションをキーワード引数として与えることもできます。
コマンドラインで次のように実行する場合を見てみましょう。

 bash
```
 $ curl http://www.google.com -o google.html --slient
```

前述の `ls` コマンドの例のように引数を分割するのは説明しました。
コマンドのオプションをキーワード引数として与えることもできます。


```
 In [2]: # %load 07_kwargs.py
   ...: from sh import curl
   ...:
   ...: # curl http://www.google.com -o google.html --slient
   ...:
   ...: curl("http://www.google.com/", "-o", "google.html", "--silent")
   ...: curl("http://www.google.com/", o="google.html", silent=True)
   ...:
 Out[2]:
 
```

## コマンド出力のリダイレクト
shは、 `_out` および `_err` のキーワード引数を使用して、プロセスの標準出力(STDOUT)や標準エラー出力(STDERR)をさまざまなタイプのターゲットにリダイレクトできます。

### ファイル名
リダイレクト先として文字列が使用されている場合、それはファイル名であると判断されます。 ファイル名は `open()` のモード `wb` で開かれます。これは、切り捨て書き込みおよびバイナリモードを意味します。

 bash
```
 $ date > /tmp/current_time.txt
```

このコマンドラインは次のように記述することができます。


```
 In [2]: # %load 08_redirect.py
    ...: import sh
    ...:
    ...: sh.date(_out="/tmp/current_time.txt")
    ...:
    ...: #!cat /tmp/current_time.txt
    ...:
 Out[2]:
 
```


### ファイルオブジェクト
 `io.StringIO` のように、 `.write(data)` メソッドをサポートする任意のオブジェクトを使用することもできます。
例えば、コマンド出力をメモリにキャッシュする場合は次のようにします。


```
 In [2]: # %load 09_memory_cache.py
    ...: import sh
    ...: from io import StringIO
    ...:
    ...: buf = StringIO()
    ...: sh.date(_out=buf)
    ...: v1 = buf.getvalue()
    ...:
    ...: # print(v1)
    ...:
 
 In [3]: print(v1)
 Wed Sep 15 03:38:23 JST 2021
 
```

前述の例で、ファイルにリダイレクトすることはわかりましたが、
追加リダイレクトするときはファイルオブジェクトを渡します。

 bash
```
 $ date >> /tmp/current_time.txt
```

これは、次のように記述することができます。


```
 In [2]: # %load 10_redirect_fileobj.py
   ...: import sh
   ...:
   ...: with open("/tmp/current_time.txt", "a") as fp:
   ...:     sh.date(_out=fp)
   ...:
   
```


### コールバック関数
リダイレクト先としてコールバック関数を使用することもできます。 コールバック関数は、次の3つの呼び出しタイプ(関数シグネチャー）のいずれかに準拠する必要があります。

> callback(data)
この関数は、プロセスからデータを部分呼び出しで取得します。

> callback(data, stdin_queue)
前のシグネチャーに加えて、この関数は `queue.Queue` も受け取ります。これは、プログラムでプロセスと通信するために使用することができます。

> callback(data, stdin_queue, process)

前のシグネチャーに加えて、関数は `OProc` オブジェクトに `weakref.weakref` を受け取ります。

## 非同期実行
shは、コマンドを実行し、ノンブロッキング方式で出力を取得するためのいくつかの方法を提供しています。

### 反復可能オブジェクトを返す
キーワード引数  `_iter` を使用して非同期コマンドを反復処理することにより、非同期コマンドを作成することもできます。 これにより、ループできる反復可能オブジェクト（具体的にはジェネレーター）が作成されます。

デフォルトでは、 `_iter` は標準出力を反復処理しますが、 `_iter` に `True` に変えて `"err"` または `"out"` を渡すことで、これを変更することができます。 また、デフォルトでは、出力はラインバッファーされるため、ループの本体は、プロセスが改行を生成したときにのみ実行されます。 これを変更するには、コマンドの出力のバッファサイズを `_out_bufsize` で変更します。


```
 In [2]: # %load 11_iter_output.py
     ...: from sh import tail, touch
     ...: from pathlib import Path
     ...:
     ...: logfile = Path('/tmp/some_logfile.log')
     ...: logfile.unlink(missing_ok=True)
     ...: logfile.touch(exist_ok=True)
     ...:
     ...: for line in tail("-f", str(logfile), _iter=True):
     ...:     if "EXIT" in line:
     ...:         break
     ...:     else:
     ...:         print(line)
     ...:
       
```

別のターミナルで次のスクリプトを実行してみましょう。
このスクリプトでEXITが出力されるまで、上記の tail コマンドの反復処理は終わりません。


```
 In [2]: # %load 12_iter_output_data.py
    ...: with open('/tmp/some_logfile.log', 'a') as fp:
    ...:     fp.write('Hello\n')
    ...:     fp.write('Python Osaka\n')
    ...:     fp.write('EXIT\n')
    ...:
 
```

## バックグラウンドプロセス
デフォルトでは、実行したコマンドが終了するまでスクリプトはブロックされます。 長時間実行されるコマンドがある場合は、キーワード引数 `_bg=True` を使用してバックグラウンドジョブとして実行することができます。


```
 In [2]: # %load 13_background.py
    ...: import sh
    ...:
    ...: sh.sleep(3)
    ...: print("...3 seconds later")
    ...:
    ...: p = sh.sleep(3, _bg=True)
    ...: print("print immediately!")
    ...: p.wait()
    ...: print("...and 3 seconds later")
    ...:
 ...3 seconds later
 print immediately!
 ...and 3 seconds later
 
```

コマンドの終了を待つためには、 `.wait()` を呼び出す必要があります。

バックグラウンドで起動されたコマンドはSIGHUPを無視します。つまり、制御プロセス（制御端末がある場合はセッションリーダー）が終了しても、カーネルからは通知されません。 ただし、shコマンドはデフォルトで独自のセッションでプロセスを起動するため、つまり、shコマンドは独自のセッションリーダーであるため、SIGHUPを無視しても通常は影響はありません。 したがって、SIGHUPを無視すると何も起こらないのは、 `_new_session=False` を使用する場合のみです。この場合、制御プロセスはおそらくPythonを起動したシェルであり、そのシェルを終了すると、通常、すべての子プロセスにSIGHUPが送信されます。

## コマンドの終了コード
Linux系プラットフォームでコマンドを実行すると終了コードが返されます。
ほとんどの場合、正常終了するとゼロ（ `0` )が返され、何らかのエラーがあるとノンゼロの値が返されます。
この終了コードにアクセスするためには、戻り値のオブジェクトの `exit_code` アトリビュートを参照します。


```
 In [2]: # %load 14_exitcode.py
    ...: import sh
    ...:
    ...: output = sh.ls("/tmp")
    ...: v1 = output.exit_code
    ...:
    ...: # print(v1)
    ...:
 
 In [3]: print(v1)
 0
 
```

コマンドの終了コードがノンゼロの場合、例外が動的に生成されます。 これにより、 `ErrorReturnCode` を介してすべてのエラーリターンコードを捕獲することができます。


```
 In [2]: # %load 15_exitcode_error.py
    ...: import sh
    ...:
    ...: try:
    ...:     print(sh.ls("/tmp/python"))
    ...: except sh.ErrorReturnCode as err:
    ...:     err_msg = err.stderr.decode('utf-8')
    ...:     print(f"Error: Exit_Code={err.exit_code}, {err_msg}")
    ...:
 Error: Exit_Code=1, ls: /tmp/python: No such file or directory
 
```

 `ErrorReturnCode_終了コード` のようにして例外を捕獲lすることもできます。


```
 In [2]: # %load 16_exitcode_error.py
    ...: import sh
    ...:
    ...: try:
    ...:     print(sh.ls("/tmp/python"))
    ...: except sh.ErrorReturnCode_1 as err:
    ...:     print(f"Error: No such file or directory.")
    ...:
 Error: No such file or directory.
 
```

## プロセスのシグナル
プロセスはkillコマンドからのシグナルを受けて終了するたびにシグナルが発生します。 このとき発生する例外は、 `ErrorReturnCode` をサブクラス化する `SignalException` です。

数値またはシグナル名のいずれかを使用して、 `SignalException` をキャッチできます。 
この資料作成時点の sh 1.14.2 は、Python 3.9 ではこの例外を捕獲することができませんでした。


```
 In [2]: # %load 17_singal_exception.py
    ...: import sh
    ...:
    ...: try:
    ...:     p = sh.Sleeper(_bg=True)
    ...:     p.kill()
    ...: except sh.SignalException_SIGKILL:
    ...:     print("killed")
    ...: except:
    ...:     print("done")
    ...:
    ...: v1 = sh.SignalException_SIGKILL == sh.SignalException_9
    ...: print(v1)
    ...:
 True
 
```


## 出力コールバック
shは、 `_bg=True` でバックグラウンドジョブとして実行するとき、 `_out` や `_err` にコールバック関数を与えることで、出力を段階的に処理することができます。 この呼び出し可能オブジェクトは、コマンドが出力するデータの各行（またはチャンクデータ）に対して呼び出されます。


```
 In [2]: # %load 19_background_output_callback.py
    ...: from sh import tail
    ...: from pathlib import Path
    ...:
    ...: logfile = Path('/tmp/some_logfile.log')
    ...: logfile.unlink(missing_ok=True)
    ...: logfile.touch(exist_ok=True)
    ...:
    ...: def process_output(line):
    ...:     print(line)
    ...:
    ...: p = tail("-f", str(logfile), _out=process_output, _bg=True)
    ...: p.wait()
    ...:
 
```

コールバックが行を受け取るかチャンクデータを受け取るかを制御するためには、 `_out_bufsize` を使用します。 コールバック関数を終了するには、 `True` を返すだけです。これによりコールバックはもう呼び出されなくなります。
ただし、 `True` を返してもプロセスは強制終了されるわけではありません。コールバックが再度呼び出されないようになるだけです。 

## インタラクティブコールバック
コマンドは、特定のコールバック関数を介して、ベースとなるプロセスとインタラクティブに通信することができます。shを介して起動される各コマンドには、コールバックから使用できる内部STDINの queue.Queueがあります。


```
 In [2]: # %load 20_background_intractive_callback.py
    ...: import sh
    ...: from pathlib import Path
    ...:
    ...: logfile = Path('/tmp/some_logfile.log')
    ...: logfile.unlink(missing_ok=True)
    ...: logfile.touch(exist_ok=True)
    ...:
    ...: def interact(line, stdin):
    ...:     if line == "もうは、まだなり。まだは、もうなり。?":
    ...:         stdin.put("もうは、まだなり。まだは、もうなり。")
    ...:
    ...:     elif line == "早い利確と、遅い損切り":
    ...:         stdin.put("残念な投資行動")
    ...:         return True
    ...:
    ...:     else:
    ...:         stdin.put("知らない行")
    ...:         return True
    ...:
    ...: p = sh.tail('-f', str(logfile), _out=interact, _bg=True)
    ...: p.wait()
    ...:
    
```

キューを使用する場合は、入力の終了（EOF）を `None` で通知できます。

プロセスオブジェクトを受信するための3番目の引数を追加することにより、コールバックからプロセスを強制終了または終了する（または実際にはシグナルを送信する）こともできます。


```
 In [2]: # %load 21_background_kill.py
    ...: import sh
    ...: from pathlib import Path
    ...:
    ...: logfile = Path('/tmp/some_logfile.log')
    ...: logfile.unlink(missing_ok=True)
    ...: logfile.touch(exist_ok=True)
    ...:
    ...: def process_output(line, stdin, process):
    ...:     print(line)
    ...:     if "EXIT" in line:
    ...:         process.kill()
    ...:         return True
    ...:
    ...: p = sh.tail("-f", str(logfile), _out=process_output, _bg=True)
    ...: p.wait()
    ...:
    
```

このコードが実行され、 `some_logfile.log` から `"EXIT"` という単語が行に表示されるまで出力されます。この時点で、tailコマンドのプロセスが強制終了されてスクリプトは終了します。

 `.terminate()` メソッドを使用してSIGTERMを送信したり、 `.signal()` メソッドを使用して一般的なシグナルを送信したりすることもできます。

## 終了コールバック
正常またはエラーの終了コードや、シグナルを介してプロセスが終了したときに呼び出される終了コールバックをキーワード引数 `_done=` で与えることができ、これは、常に呼びだされます。

 `_done` を使用してマルチプロセスプールを作成する例を次に示します。
ここで、 `sh.your_parallel_command` がコマンドとしてシステムに存在する必要があります。また、この例では一度に10以下で同時に実行されます。

```
```
　In [2]: # %load 22_done_callback.py
      - ...: import sh
      - ...: from threading import Semaphore
      - ...:
      - ...: pool = Semaphore(10)
      - ...:
      - ...: def done(cmd, success, exit_code):
      - ...:     pool.release()
      - ...:
      - ...: def do_thing(arg):
      - ...:     pool.acquire()
      - ...:     return sh.sleep('20', _bg=True, _done=done)
      - ...:
      - ...: procs = []
      - ...: for arg in range(10):
      - ...:     procs.append(do_thing(arg))
      - ...:
      - ...: for p in procs:
      - ...:     p.wait()
      - ...:     print(f'{p.pid}')
      - ...:
      - ...:
- 4634
- 4635
- 4636
- 4637
- 4638
- 4639
- 4640
- 4641
- 4642
- 4643
 


## 焼き付け(Baking)
shは、引数を別のコマンドとして焼き付ける（ベーキング：Baking)ことができます。 これは、 `functools.partial()` で行う[パーシャルアプリケーション ](https://en.wikipedia.org/wiki/Partial_application)となります。


```
 In [2]: # %load 23_baking.py
    ...: from sh import ls
    ...:
    ...: # "/usr/bin/ls -la"
    ...: ls = ls.bake("-la")
    ...: print(ls)
    ...:
    ...: # "ls -la /tmp"
    ...: print(ls("/tmp"))
    ...:
 /bin/ls -la
 lrwxr-xr-x@ 1 root  wheel  11 Jan  1  2020 /tmp -> private/tmp
 
```

ここで注目することは、 `ls()` を呼び出すたびに、引数 `-la` がすでに指定されているということです。 ベーキングは、sshコマンドなどと組み合わせると非常に便利になります。


```
 In [2]: # %load 24_baking_subcommand.py
    ...: from sh import ssh
    ...:
    ...: iam1 = ssh("myserver.com", "-l", "iisaka", "whoami")
    ...:
    ...: myserver = ssh.bake("myserver.com", l='iisaka')
    ...: iam2 = myserver.whoami()
    ...: v1 = iam1 == iam2
    ...:
    ...: # print(myserver)
    ...: # print(v1)
    ...: # print(iam2)
    ...:
 
 In [3]: print(myserver)
 /usr/bin/ssh myserver.com -l iisaka
 
 In [4]: print(v1)
 True
 
 In [5]: print(iam2)
 iisaka
 
```

焼付られた呼び出し可能オブジェクトmyserverがsshコマンドを表すようになったので、リモートサーバー上の任意のコマンドを簡単に呼び出すことができます。


```
 In [2]: # %load 25_baking_as_sh.py
    ...: from sh import ssh
    ...:
    ...: myserver = ssh.bake("myserver.com", l='iisaka')
    ...: ls = myserver.ls('/tmp')
    ...:
    ...: # print(ls)
    ...:
 
```

## パイプ処理
### パイプの基本
bashスタイルのパイプは、関数合成を使用して実行されます。 あるコマンドを別のコマンドへの入力として渡すためには、shは内側のコマンドの出力を外側のコマンドの入力に送信します。


```
 In [2]: # %load 26_pipe.py
    ...: from sh import sort, du, wc, ls
    ...: # df -sb /tmp | sort -rn
    ...: print(sort(du("-s", "/tmp"), "-rn"))
    ...:
    ...: # ls -l /etc | wc -l
    ...: print(wc(ls("-1", "/etc"), "-l"))
    ...:
 0	/tmp
 
      113
      
```

この基本的なパイプ処理は、データを非同期的に流しません。 内部コマンドは、データを外部コマンドに送信する前に、終了するまでブロックします。

デフォルトでは、別のコマンドをパイプ処理しているコマンドは、そのコマンドが完了するのを待ちます。 この動作は、パイプされるコマンドの `_piped special` キーワード引数で変更できます。これは、データを送信する前に完了するのではなく、データを段階的に送信するように指示するためのものです。

### パイプの応用
デフォルトでは、パイプされたすべてのコマンドは順番に実行されます。 これは、内側のコマンドが最初に実行され、次にそのデータが外側のコマンドに送信されるということです。

```
 print(wc(ls("-1", "/etc"), "-l"))
```

この例では、lsコマンドが実行され、その出力が収集されてから、その出力がwcコマンドに送信されます。 これは単純なコマンドでは問題になりませんが、並列処理が必要なコマンドには十分ではありません。

```
 for line in tr(tail("-f", "test.log"), 
                "[:upper:]", "[:lower:]", _iter=True):
    print(line)
```

このコードは、tailコマンドが終了しないため、実際には機能しません。 必要なのは、tailコマンドが出力を受信したときにtrコマンドに送信することです。 ここで、 `_piped` キーワード引数の出番になります。

```
 for line in tr(tail("-f", "test.log", _piped=True), 
                     "[:upper:]", "[:lower:]", _iter=True):
     print(line)
```

 `_pipe` キーワード引数は、tailコマンドにパイプが使用されていることと、出力を行ごとにパイプで接続された別のコマンドに送信する必要があることを指示します。 デフォルトでは、 `_piped` はSTDOUTを送信しますが、 `_piped="err"` を使用することで、代わりにSTDERRを送信するように簡単に設定できます。

## サブコマンド
プログラムによっては、独自のサブコマンドを持つものがあります。
例えば、git（branch、checkout）、svn（update、status）、sudo（sudoに続くコマンドはサブコマンドと見なされます）などです。
shは、アトリビュートアクセスを通じてサブコマンドを処理することができます。


```
 In [2]: # %load 27_subcommand.py
    ...: from sh import git
    ...:
    ...: # resolves to "git branch -v"
    ...: v1 = git.branch("-v")
    ...: v2 = git("branch", "-v")
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 * main 5470bfe Delete some other repository files.
 
 
 In [4]: print(v2)
 * main 5470bfe Delete some other repository files.
 
```

## デフォルトの引数
多くの場合、shをから起動されるすべてのコマンドのデフォルト引数をオーバーライドする必要があります。 たとえば、すべてのコマンドの出力を `io.StringIO` バッファーに集約するような場合です。


```
 In [2]: # %load 28_default_args.py
   ...: import sh
   ...: from io import StringIO
   ...:
   ...: buf = StringIO()
   ...:
   ...: sh.ls("/tmp", _out=buf)
   ...: sh.whoami(_out=buf)
   ...: sh.ps("auxw", _out=buf)
   ...:
   
```


これは、明らかに面倒です。この場合、実行コンテキストを作成して、そのコンテキストから生成されたすべてのコマンドにデフォルトの引数の設定することができます。

```
 In [2]: # %load 29_default_args_smart.py
   ...: import sh
   ...: from io import StringIO
   ...:
   ...: buf = StringIO()
   ...: sh2 = sh(_out=buf)
   ...:
   ...: sh2.ls("/tmp")
   ...: sh2.whoami()
   ...: sh2.ps("auxw")
   ...:
   
```


これで、sh2から起動されたものはすべて、その出力を `StringIO` インスタンスの `buf` に送信します。

実行コンテキストは、トップレベルのshモジュールのようにインポートすることもできます。

 sh2.py
```
 import sh
 from io import StringIO
 
 buf = StringIO()
 mysh = sh(_out=buf)
```


```
 In [2]: # %load 30_import_sh2.py
   ...: from sh2 import mysh, buf
   ...: from mysh import ls, whoami
   ...:
   ...: ls("/tmp")
   ...: whoami()
   ...:
   ...: v1 = buf.getvalue()
   ...:
   ...: # print(v1)
   ...:
   
```

## 環境変数
 `_env` キーワード引数を使用すると、環境変数とそれに対応する値の辞書を渡すことができます。

確認のためのシェルスクリプトを用意してみます。
 envcheck
```
 #!/bin/bash
 
 ENVNAME=${1:-"USER"}
 env | grep ${ENVNAME}=
 
 exit 0
```

このスクリプトは環境変数名を与えるとその設定を表示します。省略した場合は USER を与えたものとして動作します。

 bash
```
 % ./envcheck
 USER=goichiiisaka
 % ./envcheck HOME
 HOME=/Users/goichiiisaka
 
```

このシェルスクリプトを呼び出して、環境変数を与えてみましょう。

 pytohn
```
 In [2]: # %load 31_environment_variable.py
    ...: import sh
    ...:
    ...: v1 = sh.envcheck("ENVVAR", _env={"ENVVAR": "Python.Osaka"})
    ...: v2 = sh.envcheck(_env={"ENVVAR": "Python.Osaka"})
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 ENVVAR=Python.Osaka
 
 
 In [4]: print(v2)
 
 
```

 `_env` は、プロセスの環境を完全に置き換えます。  `_env` のキーと値のペアのみがその環境変数として使用されます。 既存の環境に加えてプロセスに新しい環境変数を追加する場合は、次のようにしてみてください。


```
 In [2]: # %load 32_new_env.py
    ...: import os
    ...: import sh
    ...:
    ...: new_env = os.environ.copy()
    ...: new_env["USER"] = "Python_Osaka"
    ...: new_env["ENVVAR"] = "Python.Osaka"
    ...:
    ...: v1 = sh.envcheck("ENVVAR", _env=new_env)
    ...: v2 = sh.envcheck(_env=new_env)
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 ENVVAR=Python.Osaka
 
 
 In [4]: print(v2)
 USER=Python_Osaka
 
 
```

## 標準入力からの入力
コマンドの標準入力は `_in` キーワード引数を使用して、プロセスに直接送信されます。


```
 In [2]: # %load 33_stdin.py
    ...: import sh
    ...:
    ...: v1 = sh.cat(_in="test")
    ...: v2 = sh.tr("[:lower:]", "[:upper:]", _in="sh is awesome")
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 test
 
 In [4]: print(v2)
 SH IS AWESOME
 
```

 `_in` に与えるものは、文字列だけに限定されません。 ファイルオブジェクト、queue.Queue、または任意の反復可能（リスト、セット、辞書など）を使用できます。

```
 In [2]: # %load 34_stdin_from_obj.py
    ...: import sh
    ...:
    ...: stdin = ["sh", "is", "awesome"]
    ...: v1 = sh.tr("[:lower:]", "[:upper:]", _in=stdin)
    ...:
    ...: # print(v1)
    ...:
 
 In [3]: print(v1)
 SHISAWESOME
 
```

キューを使用する場合は、キューの終わり（EOF）を `None` で通知できます。

## withコンテキスト
コマンドは、withコンテキストを使用して実行することができます。 これを使用する代表的なコマンドには、sudoまたはfakerootなどがあります。


```
 In [2]: # %load 35_sudo.py
    ...: import sh
    ...: import sys
    ...:
    ...: if sys.platform == 'linux':
    ...:     syslog_file = '/var/log/messages'
    ...: elif sys.platform == 'darwin':
    ...:     syslog_file = '/var/log/system.log'
    ...: elif sys.platform.startswith('win32'):
    ...:     syslog_file = 'C:\Windows\System32\winevt\Log\system' # maybe...
    ...: else:
    ...:     syslog_file = '/tmp'    # unknown platform
    ...:
    ...: with sh.contrib.sudo:
    ...:      print(sh.ls(syslog_file))
    ...:
 [sudo] password for goichiiisaka:
 /var/log/system.log
 
```

sudo コマンドの場合インポートの仕方が少し違うことに注意してください。
withコンテキストでコマンドを実行し、引数を渡す必要がある場合（例：sudoで-pオプションを指定する場合）、 `_with=True` を使用する必要があります。

これにより、コマンドにwithコンテキストから実行されていること伝わり、正しく動作できます。


```
 In [2]: # %load 36_sudo_with_args.py
    ...: import sh
    ...: import sys
    ...:
    ...: if sys.platform == 'linux':
    ...:     syslog_file = '/var/log/messages'
    ...: elif sys.platform == 'darwin':
    ...:     syslog_file = '/var/log/system.log'
    ...: elif sys.platform.startswith('win32'):
    ...:     syslog_file = 'C:\Windows\System32\winevt\Log\system' # maybe...
    ...: else:
    ...:     syslog_file = '/tmp'    # unknown platform
    ...:
    ...: with sh.contrib.sudo(k=True, _with=True):
    ...:      print(sh.ls(syslog_file))
    ...:
 [sudo] password for goichiiisaka:
 /var/log/system.log
 
```

## コマンドのカラー出力に対応
最近のLinux系プラットフォームでは、ターミナルで実行するコマンドのいくつかはデフォルトでカラー出力になっているものがあります。（例：ls や git)
shをから呼び出されたコマンドも、そのままではカラーエスケープシーケンスが混入しるため、ターミナルで実行するようにカラー出力となります。
ログなどでは、このカラーエスケープシーケンスが邪魔になる場合があります。
こうしたときは、 `_tty_out=False` キーワード引数を使用します。

git では、sh.contrib.git を利用することもできます。この場合は、 `_tty_out` は不要になります。

## コマンド名にドットを含む場合
sh はアトリビュートアクセスを行うことで、サブコマンドを実行できます。しかし、make.ext4 などのように一部のコマンドにはドット( `.` )をコマンド名に含んでいるようなものがあり、こうしたコマンドはうまく処理できません。

次のシェルスクリプトで試してみましょう。

 ECHO.sh
```
 #!/bin/bash
 
 echo $@
 
```

この ECHO.sh コマンドを sh から呼び出してみます。


```
 In [2]: # %load 37_command_with_dot.py
    ...: import sh
    ...:
    ...: echo = sh.Command("ECHO.sh")
    ...: v1 = echo('Python Osaka')
    ...:
    ...: # print(v1)
    ...:
 
 In [3]: print(v1)

 
```



## サンプル：SSHでリモートサーバに接続
リモートサーバにSSHでログインするとき、パスワード認証よりも鍵認証をする方がセキュリティーの面では安全性が高まります。これには、ssh-copy-idコマンドでリモートサーバに公開鍵をコピーすることで、パスワードを入力する必要がなくなります。
このサンプルは、例としてパスワードの入力を自動処理するようにしてみます。

プロセスと対話するには、標準出力にコールバックを割り当てる必要があります。 使用するコールバックのシグネチャーは、2番目の引数としてqueue.Queueオブジェクトを受け取り、それを使用して標準入力をプロセスに送り返すものです。

```
 from sh import ssh
 
 remote_host = "10.10.10.100"   # このIPアドレスは適宜変更
 
 def ssh_interact(line, stdin):
     line = line.strip()
     print(line)
     if line.endswith("password:"):
         stdin.put("correcthorsebatterystaple")
 
 ssh(remote_host, _out=ssh_interact)
```

これを実行すると、コールバック関数から何も出力されないことがわかります。この問題はSTDOUTのバッファリングに関係しています。 デフォルトでは、shはSTDOUTはラインバッファされます。つまり、shが出力で改行を検出した場合だけ、 `ssh_interact()` が出力を受信することができます。 パスワードプロンプトには改行がないため、この状態になっているわけです。

 bash
```
 webapp@10.10.10.100's password:
```

改行が検出されないので、 `ssh_interact()` コールバック関数には何も送信されません。そこで、STDOUTのバッファリングを変更する必要があります。 これには、 `_out_bufsize` キーワード引数を使用し、バッファをしない出力の場合はゼロ( `0` )を設定します。


```
 from sh import ssh
 
 remote_host = "10.10.10.100"   # このIPアドレスは適宜変更
 
 def ssh_interact(line, stdin):
     line = line.strip()
     print(line)
     if line.endswith("password:"):
         stdin.put("correcthorsebatterystaple")
 
 ssh(remote_host, _out=ssh_interact, _out_bufsize=0)
```

ただし、このままでは新しい問題が発生します。
 bash
```
 w
 e
 b
 a
 p
 p
 @
 (以下略)
```

これは、コールバックが受信するSTDOUTのデータがバッファリングされていないため、行ではなく個別の文字になるからです。この場合、文字ごとのデータを、パターン `password:` があるかどうかをテストして、より意味のあるものに集約することです。
このパターンが見つかれば、SSHコマンドが入力の準備ができていることになります。

まず、単純にするためにグローバル変数を使用します。

```
 from sh import ssh
 import sys
 
 remote_host = "10.10.10.100"   # このIPアドレスは適宜変更
 
 aggregated = ""
 def ssh_interact(char, stdin):
     global aggregated
     sys.stdout.write(char)
     sys.stdout.flush()
     aggregated += char
     if aggregated.endswith("password: "):
         stdin.put(os.environ.get("PASSWORD"))
 
 ssh(remote_host, _out=ssh_interact, _out_bufsize=0)
```

実は、このコードはまだうまく機能しません。 それは、2つの問題があるためです。1つ目の問題は、パスワードを入力してリターンキーを押したかのように、パスワードが改行で終わる必要があることです。 これは、SSHコマンドがパスワードの長さを認識していないため、STDINをラインバッファリングしているためです。
2番目の問題は、SSH側に要因があります。SSHが正しく機能するためには、STDINにTTYを接続する必要があります。 これにより、SSHは、実際の端末セッションで実際のユーザーと対話しているものとして処理します。 TTYを有効にするために、 `_tty_in` キーワード引数を追加します。また、 `_unify_ttys` キーワード引数を使用する必要があります。 これにより、shはSTDOUTとSTDINを単一の疑似端末から取得するように指示されます。これはSSHの仕様上の要件になります。

```
 from sh import ssh
 import sys
 
 remote_host = "10.10.10.100"   # このIPアドレスは適宜変更
 
 aggregated = ""
 def ssh_interact(char, stdin):
     global aggregated
     sys.stdout.write(char)
     sys.stdout.flush()
     aggregated += char
     if aggregated.endswith("password: "):
         stdin.put(os.environ.get("PASSWORD")+"\n")
 
 ssh(remote_host, _out=ssh_interact, 
     _out_bufsize=0, _tty_in=True, _unify_ttys=True)
```

これで、ようやくリモートサーバにSSHでログインできるようになります。
この方法は、コマンドからの入力を一文字つず集約して `”password:"` で終わっているかずっとチェックし続けることには留意してください。

## sh.contrib.ssh 
上記のコードの手順は、ssh.contrib.ssh をインポートすると簡略化できます。 contrib.ssh 、長くなるキーワード引数の設定をすべて処理し、SSHでパスワード認証でのログインを実行するためのシンプルで強力なインターフェイスを提供します。


```
 from sh.contrib import ssh
 
 remote_host = "10.10.10.100"   # このIPアドレスは適宜変更
 
 def ssh_interact(content, stdin):
     sys.stdout.write(content.cur_char)
     sys.stdout.flush()
 
 # パスワードを使用して自動的にログインし、
 # 後続のコンテンツをssh_interactコールバックに提示する
 ssh(remote_host, password="secretpass", interact=ssh_interact)
```

### SSHを使ってリモートサーバ上でコマンドを実行
ローカルホストからリモートサーバ上でコマンドを実行したいため、スクリプトでSSHパスワードを入力する方法を知りたいはずです。ターミナルからSSH経由でログインして、実行するコマンドを入力して実行する代わりに、スクリプトで行ってみましょう。

まず、ターミナルを開き、ssh-copy-id をリモートサーバ上のユーザ名を引数として与えて実行します。 リモートサーバー上のユーザのパスワードを入力するように求められます。 パスワードを入力すると公開鍵がコピーされて、以降はパスワード認証なしにリモートサーバーにSSHで接続できるようになります。 これにより、shの処理が大幅に簡素化されます。また、セキュリティー面での安全性が高まります。

次に実行したいのは、SSHを使用して、SSHで接続しているサーバーで実行するコマンドを渡すことです。 リモートサーバーのシェルを使用せずに、リモートサーバーで直接calコマンドを実行する方法は次のとおりです。
 `iisaka@dev00` は リモートサーバ  `dev00` 上のユーザ  `iisaka` で接続するということです。

 bash
```
 $ ssh iisaka@dev00 cal
```

これを、sh で実装すると次のようになります。

```
 import sh
 
 print(sh.ssh("iisaka@dev", "cal"))
```

shの `bake()` を利用して、サーバーのユーザー名(あるいはIPアドレス)をコマンドオブジェクトにバインドしておくと、もっと使い勝手がよくなります。


```
 import sh
 
 dev_server = sh.ssh.bake("iisaka@dev")
 print(dev_server("cal"))
 print(dev_server("whoami"))
```

これで、リモートコマンドを呼び出すために使用できる再利用可能なコマンドオブジェクトができました。 しかし、もう1つ改善の余地があります。 アトリビュートアクセスをコマンド引数に拡張するshのサブコマンド機能を使用することもできます。

```
 import sh
 
 dev_server = sh.ssh.bake("iisaka@dev")
 print(dev_server.cal())
 print(dev_server.whoami())
```

## まとめ
sh はプラットフォームのコマンドをPython スクリプトから簡単に利用できる非常に便利なモジュールです。
依存関係やリトライなどの機能がないため、タスクランナーとしてみたときは、やはり非力だと言えます。
しかし invoke や fabric ほかのタスクランナーと共存して利用することは、問題ないため有益なツールであることは間違いありません。



## 参考
- sh モジュール - [ドキュメント ](https://amoffat.github.io/sh/index.html#)
- Qiita - [ttyとかptyとかについて確認してみる ](https://qiita.com/toshihirock/items/22de12f99b5c40365369)


