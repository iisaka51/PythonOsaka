shellモジュールを使って外部コマンドを呼び出してみよう
=================
## shell について
Pythonからプラットフォームのコマンドを実行したい場合は、標準ライブラリを利用するのであれば、、subprocess を使って処理することになります。しかし、この subprocess は直感的にでないため使用方法にクセがあり、ドキュメントを調べることになる場合が多いかもしれません。
shell はPython からプラットフォームのコマンドをより簡単に使えるようにしたモジュールです。

shell は次のような方針で設計されています。

- 外部コマンドの実行をより自然にする
- デフォルトでは、出力やエラーを取り扱うことを想定しています。
- およそ80%のコマンド実行をカバー
- より良いAPI
- Linux/OS Xで動作（Windowsでは未検証だが、動作するかも？ Bash on WindowsもあるのでOKか？）

## インストール
shell は次のように pip でインストールします。

 bash
```
 $ pip install shell
 
```

コマンドのエラーハンドリングを行う場合では、ソースコードの方が少しだけ改良されています。
ソースコードからインストールする場合は次のように行います。

 nash
```
 $ git clone https://github.com/toastdriven/shell.git
 $ cd shell
 $ python setup.py install
 
```

## shell の使い方
まずは、簡単な例をお見せしましょう。

python
```
 In [2]: # %load 01_intro_simple.py
    ...: from shell import shell
    ...:
    ...: ls = shell('ls')
    ...: for file in ls.output():
    ...:     print(file)
    ...:
 01_intro_simple.py
 02_intro_with_args.py
 
```

ヘルパー関数 `shell()` を呼び出して、実行したコマンドを引数として与えます。

コマンドラインの引数を渡すときも同じようにします。


```
 In [2]: # %load 02_intro_with_args.py
    ...: from shell import shell
    ...:
    ...: ls = shell('ls /tmp')
    ...: for file in ls.output():
    ...:     print(file)
    ...:
 com.apple.launchd.DmlO1s0i7r
 com.apple.launchd.VWfokDXKVW
 com.brave.Browser.Sparkle.pid
 com.docker.docker.Sparkle.pid
 com.google.Keystone
 dummyfile
 powerlog
 
 In [3]: ls.output
 Out[3]: <bound method Shell.output of <shell.Shell object at 0x7fd8adc3de80>>
 
 In [4]: ls.output()
 Out[4]:
 ['com.apple.launchd.DmlO1s0i7r',
  'com.apple.launchd.VWfokDXKVW',
  'com.brave.Browser.Sparkle.pid',
  'com.docker.docker.Sparkle.pid',
  'com.google.Keystone',
  'dummyfile',
  'powerlog']
 
```

これを subprocess で記述すると、つぎのようなコードになります。


```
 In [2]: # %load 03_intro_subprocess.py
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
 com.apple.launchd.DmlO1s0i7r
 com.apple.launchd.VWfokDXKVW
 com.brave.Browser.Sparkle.pid
 com.docker.docker.Sparkle.pid
 com.google.Keystone
 dummyfile
 powerlog
 
 In [3]: ls.stdout
 Out[3]: 'com.apple.launchd.DmlO1s0i7r\ncom.apple.launchd.VWfokDXKVW\ncom.brave.Browser.Sparkle.pid\ncom.docker.docker.Sparkle.pid\ncom.google.Keystone\ndummyfile\npowerlog\n'
 
 In [4]: ls.stdout.splitlines()
 Out[4]:
 ['com.apple.launchd.DmlO1s0i7r',
  'com.apple.launchd.VWfokDXKVW',
  'com.brave.Browser.Sparkle.pid',
  'com.docker.docker.Sparkle.pid',
  'com.google.Keystone',
  'dummyfile',
  'powerlog']
 
```

必要な結果を得るために、 `encoding` や `stdout` の引数を与えたり、結果を `splitlines()` で処理する必要があったりするわけです。shell モジュールの方がシンプルで直感的だということがわかりますよね。

## Shellクラス
ヘルパー関数ではなく Shellクラスをインスタンスオブジェクトを生成して、 `run()` メソッドにコマンドラインを与えることもできます。


```
 In [2]: # %load 04_intro_class.py
    ...: from shell import Shell
    ...:
    ...: sh = Shell()
    ...: sh.run('ls /tmp')
    ...: for file in sh.output():
    ...:     print(file)
    ...:
    ...:
 com.apple.launchd.DmlO1s0i7r
 com.apple.launchd.VWfokDXKVW
 com.brave.Browser.Sparkle.pid
 com.docker.docker.Sparkle.pid
 com.google.Keystone
 dummyfile
 powerlog
 
```

エラー情報や、コマンドのプロセスID、終了コードなども属性として参照することが’できます。


```
 In [2]: # %load 05_exist_code.py
    ...: from shell import Shell
    ...:
    ...: sh = Shell()
    ...: sh.run('ls /tmp')
    ...:
    ...: # sh.errors()
    ...: # sh.pid
    ...: # sh.code
    ...:
    ...:
 Out[2]: <shell.Shell at 0x7faac2a113d0>
 
 In [3]: sh.errors()
 Out[3]: []
 
 In [4]: sh.pid
 Out[4]: 32753
 
 In [5]: sh.code
 Out[5]: 0
 
```

- last_command：最後に実行したコマンド
- pid：コマンドを実行したプロセスID
- code：コマンドの終了コード


## 標準入力から読み取ってコマンドを実行

ヘルパー関数  `shell()` に  `has_input=True` を与えると、 `sh.write()` で書き込んだ内容がコマンドの標準入力に渡されて処理されます。


```
 In [2]: # %load 06_intractive_func.py
    ...: from shell import shell
    ...:
    ...: # -u : バッファリングをしないためのオプション
    ...:
    ...: sh = shell('cat -u ', has_input=True)
    ...: sh.write('Hello World!')
    ...:
    ...: # sh.output()
    ...:
 Out[2]: <shell.Shell at 0x7ff96bc3e280>
 
 In [3]: sh.output()
 Out[3]: ['Hello World!']
 
```


Shellクラスのインスタンスを生成するときに、 `has_inout=True` を与えても同じです。


```
 In [2]: # %load 07_intractive_class.py
    ...: from shell import Shell
    ...:
    ...: # -u : バッファリングをしないためのオプション
    ...:
    ...: sh = Shell(has_input=True)
    ...: sh.run('cat -u')
    ...: sh.write('Hello World!')
    ...:
    ...: # sh.output()
    ...:
 Out[2]: <shell.Shell at 0x7f8dc749c6a0>
 
 In [3]: sh.output()
 Out[3]: ['Hello World!']
 
```


## エラー処理
コマンドラインの構築に間違いがあったり、コマンドが見つからないような場合など、いくつかコマンドでエラーが発生するケースがあります。

コマンドでエラーが発生したかどうかは、終了コードもしくは `errors()` の結果を確認する必要があります。


```
 In [2]: # %load 08_cmd_error.py
    ...: from shell import shell
    ...: ls = shell('ls /tmp/PythonOsaka')
    ...: if ls.code != 0:
    ...:     print(f'Error: {ls.errors()}')
    ...:
 Error: ['ls: /tmp/PythonOsaka: No such file or directory']
```

ソースレポジトリのバージョンでは  `die` キーワード引数を受け渡すことができるようになっていて、コマンドのエラーでは例外を発生させることができます。


```
 In [2]: # %load 09_cmd_error_die.py
    ...: from shell import shell
    ...: ls = shell('ls /tmp/PythonOsaka', die=True)
    ...: if ls.code != 0:
    ...:     print(f'Error: {ls.errors()}')
    ...:
 ---------------------------------------------------------------------------
 CommandError                              Traceback (most recent call last)
 <ipython-input-2-441b0e1e915f> in <module>
       1 # %load 09_cmd_error_die.py
       2 from shell import shell
 ----> 3 ls = shell('ls /tmp/PythonOsaka', die=True)
       4 if ls.code != 0:
       5     print(f'Error: {ls.errors()}')
  (中略)
 CommandError: Command exited with code 1
 
```

 `CommandError` を捕獲すればより柔軟にエラー処理を行うことができます。


```
 In [2]: # %load 10_cmd_error_except.py
    ...: import sys
    ...: from shell import shell, CommandError
    ...:
    ...: try:
    ...:     shell('ls /tmp/PythonOsaka', die=True)
    ...: except CommandError as e:
    ...:     print(f'Command Error: {e.stderr}')
    ...:     import __main__ as main
    ...:     if hasattr(main, '__file__'):   # running script on REPL/IPython
    ...:         sys.exit(e.code)
    ...:
 Command Error: ls: /tmp/PythonOsaka: No such file or directory
 
```


## コマンドチェーン
コマンドを実行して返されるオブジェクトはチェーン化させることができます。


```
 In [2]: # %load 11_cmd_chaining.py
    ...: from shell import shell, Shell
    ...:
    ...: _MSG_='Hello World!'
    ...: v1 = shell('cat -u', has_input=True).write(_MSG_).output()
    ...: v2 = Shell(has_input=True).run('cat -u').write(_MSG_).output()
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 ['Hello World!']
 
 In [4]: print(v2)
 ['Hello World!']
 
```


## 大量すぎる結果出力を無視
デフォルトでは、シェルはすべての出力/エラーをキャプチャします。もしコマンドの出力を無視したい場合は次のようにします。


```
 In [2]: # %load 12_ignore_output.py
    ...: from shell import shell, Shell
    ...:
    ...: sh = shell('cat sample.txt', record_output=False, record_errors=False)
    ...: v1 = sh.code
    ...: v2 = sh.output()
    ...:
    ...: sh = Shell(record_output=False, record_errors=False)
    ...: sh.run('cat sample.txt')
    ...: v3 = sh.code
    ...: v4 = sh.output()
    ...:
    ...: # print(v1)
    ...: # ...
    ...: # print(v4)
    ...:
    ...:
 
 In [3]: print(v1)
 0
 
 In [4]: print(v2)
 []
 
 In [5]: print(v3)
 0
 
 In [6]: print(v4)
 []
 
```

また、 `strip_empty=True` を与えると、外部コマンドの出力から改行だけの行が削除されたものが返されます。

## バックグランドジョブ

subprocess を使った場合、バックグランドでコマンドを実行するためには、次のように行います。


```
 In [2]: # %load 13_subprocess_background.py
    ...: import shlex
    ...: import subprocess
    ...:
    ...: cmd="sleep 60"
    ...: command_bits = shlex.split(cmd)
    ...: output=subprocess.Popen(command_bits)
    ...:
    ...: print(command_bits)
    ...:
 ['sleep', '60']
 
 In [3]: !ps -efaw | grep sleep
   501 45944 45912   0  7:05AM ttys003    0:00.00 sleep 60
   501 45951 45912   0  7:05AM ttys003    0:00.01 /bin/zsh -c ps -efaw | grep sleep
   501 45953 45951   0  7:05AM ttys003    0:00.00 grep sleep
 
```

このとき、次のように `communicate()` メソッドを呼び出すと、 `Popen()` のコマンドの終了を待つようになります。


```
 In [2]: # %load 14_subprocess_background_wait.py
    ...: import shlex
    ...: import subprocess
    ...:
    ...: cmd="sleep 60"
    ...: command_bits = shlex.split(cmd)
    ...: output=subprocess.Popen(command_bits)
    ...: output.communicate()      # コマンドの終了を待つ...
    ...:
    ...: print(command_bits)
    ...:
 ['sleep', '60']
 
```

shell では、バックグランドでのコマンド実行については明確には記述されていませんが、 `has_input=False` （これはデフォルト）のときに、 `comminucate()` を呼び出すようになっています。

次の簡単なシェルスクリプトで試してみましょう。
このスクリプトは３０秒待ってから文字列  `done` を表示するだけのものです。

 Sleeper.sh
```
 #!/bin/bash
 
 sleep 60
 echo "done"
```

 `Sleeper.sh` が正常に終了すれば、出力に文字列 `done` があるはずです。


```
 In [2]: # %load 15_kill_cmd.py
    ...: from shell import Shell
    ...:
    ...: sh = Shell(has_input=True)
    ...: v1 = sh.run('./Sleeper.sh')
    ...: v2 = sh.kill()
    ...:
    ...: # v1.output()
    ...: # v2.output()
    ...:
 
 In [3]: v1.output()
 Out[3]: []
 
 In [4]: v2.output()
 Out[4]: []
 
```

何も出力されていないので、 `kill()` によって強制終了されたことがわかります。

## まとめ
shell は subprocess よりも簡単に、直感的にコマンドを実行できるため、Python スクリプトで外部コマンドを実行したい場合には有益です。


## 参考
- [shell ソースコード ](https://github.com/toastdriven/shell)
- [shell ドキュメント ](https://shell.readthedocs.io/en/latest/index.html)
- [Python ドキュメント - subprocess ](https://docs.python.org/ja/3/library/subprocess.html)


