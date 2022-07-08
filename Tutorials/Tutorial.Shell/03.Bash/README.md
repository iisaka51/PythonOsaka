bashモジュールを使って外部コマンドを呼び出してみよう
=================
## bashモジュールについて
[bash モジュール ](https://github.com/alexcouper/bash) は、Python から外部コマンドを簡単に実行することができます。
Python の標準ライブラリ subprocess の代替として利用することができます。

subprocess でのコマンド実行の煩雑さを簡単にすることを目的として開発されていて、
シンプルな実装で、直感的に記述できるため、学習コストが低いという優れた強みがあります。
そのためか、きちんとしたドキュメントが存在していないことは弱点です。

Linux系プラットフォームで利用されているシェルに同じ名前の bash コマンドがあります。これと区別するために、この資料では、シェルコマンドを bash コマンド、bash モジュールと表記することにします。


## インストール
bash モジュールは次のように pip でインストールします。

 bash
```
 $ pip install bash
 
```


## bash モジュール の使い方
bashモジュールの使用方法をお見せしましょう。


```
 In [2]: # %load 01_intro_simple.py
    ...: from bash import bash
    ...:
    ...: ls = bash('ls /tmp')
    ...: for file in ls.value().splitlines():
    ...:     print(file)
    ...:
 
```

bash モジュールをインポートして bash クラスのコンストラクタにコマンドラインを与えます。
コマンドラインの出力は  `value()` メソッドで取得します。

これを subprocess を使って記述すると次のようになります。


```
 n [2]: # %load 02_intro_subprocess.py
    ...: import subprocess
    ...: import shlex
    ...:
    ...: cmdline = 'ls /tmp'
    ...:
    ...: ls = subprocess.run(shlex.split(cmdline),
    ...:                        encoding='utf-8', stdout=subprocess.PIPE)
    ...: for file in ls.stdout.splitlines():
    ...:     print(file)
    ...:
    ...:
 
```

呼び出し方が簡単になっていて、読みやすいことがわかりますよね。

### bash クラスの属性値
bash クラスのインスタンスオブジェクトには、次の属性値を持っています。

- stdout：subprocess.Popen() からの標準出力（byte文字列)
- stderr：subprocess.Popen() からの標準エラー出力(byte文字列)
- code：コマンドの終了コード


```
 In [2]: # %load 03_intro_attribute.py
    ...: from bash import bash
    ...:
    ...: ls = bash('ls /tmp')
    ...:
    ...: # ls.value()
    ...: # ls.stdout
    ...: # ls.stderr
    ...: # ls.code
    ...:
 
 In [3]: ls.value()
 Out[3]: 'FirstBootAfterUpdate\nFirstBootCleanupHandled\n_MEIubHlfI\ncom.apple.launchd.9WKFMCb6kv\ncom.apple.launchd.dx5ZAvQMdp\ncom.brave.Browser.Sparkle.pid\ncom.google.Keystone\nfseventsd-uuid\nkjnsdfBSDFBo2pnwvpd\npowerlog\nsdfvSDFVGver27zv93\nsome_logfile.log'
 
 In [4]: ls.stdout
 Out[4]: b'FirstBootAfterUpdate\nFirstBootCleanupHandled\n_MEIubHlfI\ncom.apple.launchd.9WKFMCb6kv\ncom.apple.launchd.dx5ZAvQMdp\ncom.brave.Browser.Sparkle.pid\ncom.google.Keystone\nfseventsd-uuid\nkjnsdfBSDFBo2pnwvpd\npowerlog\nsdfvSDFVGver27zv93\nsome_logfile.log\n'
 
 In [5]: ls.stderr
 Out[5]: b''
 
 In [6]: ls.code
 Out[6]: 0
 
```

## コマンド出力のリダイレクト
bashは、 `stdout` および `stderr` のキーワード引数を使用して、プロセスの標準出力(STDOUT)や標準エラー出力(STDERR)をさまざまなファイルオブジェクトにリダイレクトできます。

標準出力をリダイレクトする場合は、 `stdout` キーワード引数にファイル部ジェクトを与えます。


```
 In [2]: # %load 04_redirect.py
    ...: from bash import bash
    ...:
    ...: with open('/tmp/current_time.txt', 'w') as fp:
    ...:     bash("date", stdout=fp)
    ...:
    ...: #!cat /tmp/current_time.txt
    ...:
 
 In [3]: !cat /tmp/current_time.txt
 Wed Sep 15 18:39:25 JST 2021
 
```

標準エラー出力のリダイレクトは  `stderr` キーワードにファイルオブジェクトを与えます。


```
 In [2]: # %load 05_redirect_sterr.py
    ...: from bash import bash
    ...:
    ...: with open('/tmp/error.txt', 'w') as fp:
    ...:     bash("ls -l /tmp/dummyfile", stderr=fp)
    ...:
    ...: #!cat /tmp/error.txt
    ...:
 
 In [3]: !cat /tmp/error.txt
 ls: /tmp/dummyfile: No such file or directory
 
```
逆に出力を無視したいときは、 `stdout = subprocess.DEVNULL` や  `stderr = subprocess.DEVNULL` を与えます。

## パイプ処理
bashコマンドでのパイプ処理は、コマンドをパイプ記号( `|` )でコマンドを繋いで、あるコマンドの出力を別のコマンドへの入力として実行するものです、bash モジュールでのパイプ処理では２つの方法があります。
１つは、パイプ記号を含むコマンドラインをそのまま記述する方法と、もう１つは、オブジェクトをチェーンして記述する方法です。
どちらも直感的でわかりやすいものです。


```
 In [2]: # %load 05_pipe.py
    ...: from bash import bash
    ...:
    ...: # ls -l /etc/ | wc -l
    ...: v1 = bash('ls -l /etc/ | wc -l').value()
    ...: v2 = bash('ls -l /etc/').bash('wc -l').value()
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 114
 
 In [4]: print(v2)
 114
 
 In [5]: !ls -l /etc/ | wc -l
      114
 
```

## バックグランドでコマンドを実行
デフォルトでは、実行したコマンドが終了するまでスクリプトはブロックされます。 長時間実行されるコマンドがある場合は、キーワード引数 `sync=False` を使用してバックグラウンドジョブとして実行することができます。


```
 In [2]: # %load 06_background.py
    ...: from bash import bash
    ...:
    ...: bash('sleep 3')
    ...: print("...3 seconds later")
    ...:
    ...: p = bash('sleep 3', sync=False)
    ...: print("print immediately!")
    ...: p.sync()
    ...: print("...and 3 seconds later")
    ...:
 ...3 seconds later
 print immediately!
 ...and 3 seconds later
 
```

 `sync()` メソッドを呼び出すと、バックグラウンドで実行したプロセスが終了するまで、呼び出し側のプロセスはブロックされます。つまり、実行した外部コマンドが終了するまで、呼び出したスクリプトは待たされます。

## タイムアウト
 `timeout=` キーワード引数に秒数を指定すると、外部コマンドを呼び出してからその時間が経過したときに、そのコマンド実行を強制終了させることができます。


```
 In [2]: # %load 07_timeout.py
    ...: from bash import bash
    ...: from subprocess import TimeoutExpired
    ...:
    ...: try:
    ...:     bash('sleep 10', timeout=5)
    ...: except TimeoutExpired as e:
    ...:     print(f'Timeoout: {e}')
    ...: except:
    ...:     print('unknown')
    ...: print('done')
    ...:
 Timeoout: Command 'sleep 10' timed out after 5 seconds
 done
 
```


## 環境変数
 `env` キーワード引数を使用すると、環境変数とそれに対応する値の辞書を渡すことができます。

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


```
 In [2]: # %load 10_environment_variable.py
    ...: from bash import bash
    ...:
    ...: v1 = bash('envcheck ENVVAR', env={"ENVVAR": "Python.Osaka"}).value()
    ...: v2 = bash('envcheck', env={"ENVVAR": "Python.Osaka"}).value()
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 ENVVAR=Python.Osaka
 
 In [4]: print(v2)
 
```

 `env` キーワード引数与えた辞書は、プロセスの環境を完全に置き換えます。  `env` のキーと値のペアのみがその環境変数として使用されます。 既存の環境に加えてプロセスに新しい環境変数を追加する場合は、次のようにしてみてください。


```
 In [2]: # %load 11_new_env.py
    ...: import os
    ...: from bash import bash
    ...:
    ...: new_env = os.environ.copy()
    ...: new_env["USER"] = "Python_Osaka"
    ...: new_env["ENVVAR"] = "Python.Osaka"
    ...:
    ...: v1 = bash('envcheck ENVVAR', env=new_env)
    ...: v2 = bash('envcheck', env=new_env)
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 ENVVAR=Python.Osaka
 
 In [4]: print(v2)
 USER=Python_Osaka
 
```


## 制限：できないこと
bashモジュールでできないことを理解しておきましょう。

- バックグラウンドでの実行したコマンドのプロセスIDを知ることができない
- バックグラウンドでの実行したコマンドへシグナルを送信できない
- バックグラウンドでの実行したコマンドの標準入力を変更できない

## まとめ
bash モジュールを使用すると、subprocess で外部コマンドを呼び出すときの面倒な手続きを気にすることなく、直感的に記述することができ、コードも読みやすくなります。
ただし、バックグラウンドでの実行した外部コマンドにシグナルを送信したり、ファイルからのダータをバックグラウンドのコマンドの標準入力に割り当てたりといった、より複雑な機能は提供されていません。
しかし、このため返って覚えやすくて使いやすいものになっています。
ちょっとしたスクリプトやコンソールコマンドでは採用しても問題ないはずです。

## 参考
- [bashモジュールソースコード ](https://github.com/alexcouper/bash)


