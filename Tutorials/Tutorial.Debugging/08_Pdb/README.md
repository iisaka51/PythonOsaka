Pythonのデバッガーpdbを使ってみよう
=================
## pdbについて
python 標準ライブラリに含まれているデバッガ [pdb ](https://docs.python.org/library/pdb.html) は、コードをインタラクティブに検査することができます。

具体的には次のようなことができます。

- ソースコードの表示
- コールスタックのアップ/ダウン
- 変数の値の検査
- 変数の値を変更
- ブレークポイントの設定
- 事後デバッグのサポート

pdb では、コードが実行される前にデバッガのプロンプトが表示されます。その状態で、pdb のコマンドを与えてブレークポイントを設定してプログラムを一時停止したり、変数の値を見たり、プログラムの実行を段階的に見たりする機能を備えており、プログラムが実際に何をしているのかを理解し、ロジックのバグを見つけることができます。

事後デバッグ(Post-Mortem Debugging)は、プログラムの実行プロセスが終了した後に、発生した障害をデバッグすることをいい
ます。（言葉の意味通りでは死後のデバッグ）

Visual Studio や PyCharm、Atom などIDEでのデバッグを行うことが多いかもしれません。しかし、pdb の使用方法を理解することは、それらのツールでも有益なはずです。


## ipdb
IPython で使用する場合は ipdb を使うこともできます。 これは、pdb の全機能に加え、タブ補完、カラーサポート、マジックファンクションなど、対話型シェルのための IPython をサポートする機能が追加されています。ipdbはpdbと同じように使うことができ、よりユーザーエクスペリエンスが向上します。

ipdb を使用したい場合は、インストールが必要です。

 bash
```
 $ pip install ipdb
```


## pdb++
pdb++はオープンソースのPythonデバッガで標準ライブラリ pdb の代替ライブラリです。pdb の全機能に加え、次のような機能が提供されます。

- Python 式のカラフルな TAB 補完機能 (fancycompleter を利用)
- コードリストのシンタックスハイライト(pygmentsを利用)
- スティッキーモード
- 対話型 (Pdb++) プロンプトから使用するいくつかの新しいコマンド
- スマートなコマンド解析 (変数の値を表示するためにプロンプトで r や c をタイプしたことはありませんか?)
- プログラムから使用するためのpdbモジュールに追加される便利な関数

pdb++ を使用したい場合は、インストールが必要です。

 bash
```
 $ pip install pdbpp
```


## pdb の起動

pdbを起動するには、次の3つの方法があります。

- pdbをインポートし、コードに  `pdb.set_trace()` を呼び出して起動する方法
- IDLE でデバッガーをインポートし、モジュールを実行させる方法
- コマンドラインで pdb コマンドを起動する方法


次のコードで試してみましょう。

 c01_sample.py
```
 def square(n):
     result = n ** 2
     print(result)
     return result

 def main():
     for i in range(1,10):
         square(i)

 if __name__ == "__main__":
     main()
```

### PythonのREPLから

 bash
```
 % python

 [Clang 11.1.0 ] on darwin
 Type "help", "copyright", "credits" or "license" for more information.
 >>> import c01_sample
 >>> import pdb
 >>> pdb.run('sample.main()')
 > <string>(1)<module>()
 (Pdb++) continue
 1
 4
 9
 16
 25
 36
 49
 64
 81
 >>>
```

 bash
```
 % ipython

 Type 'copyright', 'credits' or 'license' for more information
 IPython 7.28.0 -- An enhanced Interactive Python. Type '?' for help.

 In [1]: import c01_sample

 In [2]: import ipdb

 In [3]: ipdb.run('sample.main()')
 > <string>(1)<module>()

 ipdb> continue
 1
 4
 9
 16
 25
 36
 49
 64
 81

 In [4]:
```


サンプルとして用意したモジュール  `sample.py` と pdbをインポートします。ipython では ipdb をインポートします。そして、 `pdb.run()` メソッドを実行し、モジュールの `main()` を呼び出すとデバッガのプロンプトが表示されます。ここでは `continue` と入力し、継続させてスクリプトを実行するように指示しています。また、 `continue` のショートカットとして  `c` を入力することもできます。 `continue` を入力すると、デバッガーはブレークポイントに到達するか、スクリプトが終了するまで実行を続けます。

デバッガーを起動するもうひとつの方法は、ターミナル・セッションで次のコマンドを実行することです。(python3.7〜)

 bash
```
 $ python -m pdb c01_sample.py
```

この方法で実行すると、少し異なる結果が得られます。

 bash
```
 $ python -m pdb c01_sample.py
 > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/sample.py(1)<module>()
 -> def square(n):
 (Pdb) c
 1
 4
 9
 16
 25
 36
 49
 64
 81
 The program finished and will be restarted
 > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/sample.py(1)<module>()
 -> def square(n):
 (Pdb)

```

 bash
```
 $ ipython -m ipdb c01_sample.py
 /Users/goichiiisaka/anaconda3/envs/tutorials/lib/python3.9/runpy.py:127: RuntimeWarning: 'ipdb.__main__' found in sys.modules after import of package 'ipdb', but prior to execution of 'ipdb.__main__'; this may result in unpredictable behaviour
   warn(RuntimeWarning(msg))
 > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/sample.py(1)<module>()
 ----> 1 def square(n):
       2     result = n ** 2
       3     print(result)

 ipdb> c
 1
 4
 9
 16
 25
 36
 49
 64
 81
 The program finished and will be restarted
 > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/sample.py(1)<module>()
 ----> 1 def square(n):
       2     result = n ** 2
       3     print(result)

 ipdb>

```

PythonのREPLから起動した方法では、 `<string>(1)<module>()` となっていたのですが、 `-m pdb` オプションで実行した方法では、 `sample.py(1)<module>()` となっていて、ソースコード名が確認できるようになります。

この例では、 `continue` の代わりに  `c` を使っています。　最後にデバッガーが再起動していることに注目してください。これは、デバッガの状態（ブレークポイントなど）を保持するもので、デバッガを停止させるよりも便利な場合があります。コードのどこが問題なのかを理解するために、何度もコードを見直す必要があるからです。

## ipdb の既知の問題
また、ipdb の場合は、次のような警告が出力されています。


```
 .../LIB/runpy.py:127: RuntimeWarning: 'ipdb.__main__' found in sys.modules after import of package 'ipdb', but prior to execution of 'ipdb.__main__'; this may result in unpredictable behaviour
  warn(RuntimeWarning(msg))

```

これは Python 3での動作に影響しています。 `python -m` でモジュールを実行すると、次のように動作します。

- まずモジュールをインポート（ `__init__.py` を実行）する
- 次に  `__main__.py` を直接実行します。

つまり、ipdbが  `--m` オプションで実行されたかどうかを、 `__init__.py` で知る簡単な方法がないためです。
参考: [Issue 224 ](https://github.com/gotcha/ipdb/issues/221)

これは、実害がない警告のため無視することができます。
どうしても気になる場合は、次のようなコードに修正して実行します。

 c02_sample.py
```
 def square(n):
     result = n ** 2
     print(result)
     return result

 def main():
     for i in range(1,10):
         square(i)

 if __name__ == "__main__":
     try:
         import ipdb
     except:
         import pdb as ipdb

     ipdb.set_trace()
     main()
```

この場合は、 `-m` オプションは使用する必要がありません。

 bash
```
 $ ipytohn c02_sample.py
```

pdb++ は ipdb と同様の機能があり、IPython からも利用することができるため、これ以降は、IPython と pdb++ を使って説明することにします。pdb++ は pdb の代替モジュールであるため、呼び出し方法は同じです。


## pdbのコマンド

- **h / help**：ヘルプメッセージを表示します。help につづけてコマンドを与えて実行すると、そのコマンドの使い方が表示されます。 まず、このコマンドの存在を覚えておきましょう。

```
 (Pdb++) help

 Documented commands (type help <topic>):
 ========================================
 EOF    cl         disable  help       list      quit     step       until
 a      clear      display  hf_hide    ll        r        sticky     up
 alias  commands   down     hf_unhide  longlist  restart  tbreak     w
 args   condition  ed       ignore     n         return   track      whatis
 b      cont       edit     interact   next      retval   u          where
 break  continue   enable   j          p         run      unalias
 bt     d          exit     jump       pp        rv       undisplay
 c      debug      h        l          q         s        unt

 Miscellaneous help topics:
 ==========================
 exec  hidden_frames  pdb

 Undocumented commands:
 ======================
 f  frame  hf_list  inspect  paste  put  source

 (Pdb++) help step
 s(tep)
         Execute the current line, stop at the first possible occasion
         (either in a function that is called or in the current
         function).
 (Pdb++)
```

たくさんのコマンドがありますが、h  は help のエリアスのように、重複したものもあります。
よく使用するpdbコマンドは次のものです。

-  `s` /  `step` ：プログラムを1行進めます。その行が実行された後、pdbプロンプトが再び表示されます。
-  `n` /  `next` ：プログラムを1行進めます。その行が実行された後、pdbプロンプトが再び表示されます。
-  `j` /  `jump` ：次に実行される行を設定します。ジャンプバックしてコードを再度実行したり、ジャンプフォワードして実行したくないコードをスキップしたりすることができます。pdbプロンプトが再び表示されます。
-  `c` /  `continue` ：次のブレークポイントに到達するか、プログラムの実行が完了するまで、プログラムを継続します。

 `step` と　 `next` の違いは、関数が呼び出されている行での挙動の違いです。 `step` は関数の中のコードの行に進み、ステップイン（入り込む）するように動作します。 `next` は関数の実行を済ませて次の行に進み、跨ぐように動作します。

-  `w` /  `where` ]:   `where` はその時点でのプログラムのスタック全体を表示します。これを使うことで、現在のモジュールが他の実行中のものと比べてどこにあるかを確認できます。
-  `b` /  `break` ： `break` は指定された場所にブレークポイントを設定します。
  -  `b(reak) [([filename:]lineno | function) [, condition]]`
  -  `break` ：　引数を与えずに実行すると現在設定されているブレークポイントを一覧表示します。
  -  `break filename:lineno` ：指定したファイル:行にブレークポイントを設定します。
  -  `break lineno` ：現在のファイルの指定した行にブレークポイントを設定します。
  -  `break function` ：指定した関数にブレークポイントを設定します。
  -  `break` を指定するときカンマ( `,` )に続けて条件式を与えることができます。 `break 3 , num > 4`
-  `tbreak` ：テンポラリブレークポイント。設定方法は　 `break` と同じだが、最初にヒットしたときに自動的にクリアされます。
-  `enable` /  `disable` ：ブレークポイントを有効/無効にする。ブレークポイントは空白文字で区切って複数与えることができます。
-  `cl` /  `clear` ：ブレークポイントのクリア
-  `condition` ：指定したブレークポイントに条件を追加または更新をします。
-  `a` /  `args` ：現在の関数が受け取ったすべての引数を表示します。
-  `r` /  `return` ：現在の関数が戻る（ `return` 文)まで実行を継続します。
-  `p` /  `pp` ： 式の結果を出力
ある式の結果を  `p` で印刷(print)します。 `pp` はきれいに印刷(Printy Print)します。
-  `l` /  `list` ：ソースを表示。現在のプログラムの実行中の特定のポイントでソースコードを周辺の11行表示します。続けて引数なしで指示すると続きの11行を表示します。引数にドット( `.` )を与えると、現在に行’を中心に11行表示します。行番号を１つ与えるとその行から表示します。２つの行番号を与えるとその範囲を表示します。2 番目の引数が 1 番目の引数よりも小さい場合、それは行数を意味します。
-  `ll` /  `longlist` ：現在の関数のソースコードを表示します。
-  `!` ：ステートメントの実行。 `c=1` を実行しようとすると  `continue` と解釈されることの回避
-  `;;` ：1行に複数のpdbコマンドを記述します。例：　 `break 11 ;; continue`
どのような有効なPythonステートメントも、それに感嘆符を前置することで、現在実行中のモジュールのコンテキストで実行することができます。
-  `run` /  `restart` ：デバッガを再起動します。文字列が与えられた場合は、shlexで分割されて sys.argv に渡されます。デバッガコマンド履歴、ブレークポイント、アクション、デバッガオプションは保存されます。
-  `commands` ：ブレークポイントがヒットしたときに実行される、コマンドブロックを設定します。
-  `silent` ：コマンドをエコーバックしない
-  `alias` ：コマンドエリアスを設定します。例： `alias sl step;;list`
-  `unalias` ：コマンドエリアスを解除します。例： `unalias sl`
-  `q` /   `quit` ：pdb の終了

すでに  `c` 、 `a` といった名前の変数を使用している場合は、 `continue` 、 `args` といった完全なコマンドを使用して目的の操作を行います。

## ハンズオン

### コードを1行ごとに実行
コードを1行ごとに確認したい場合には、 `step` （または単に  `s` ）コマンドを使用します。


```
 % ipython -m pdb c02_sample.py
 [2] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py(1)<module>()
 -> def square(n):
```
　(Pdb++)

デバッガを起動すると、デバッガのプロンプト  `(Pdb++)` が表示されます。他に `c02_sample.py(1)<module>()` とあるため、  `c02_sample.py` の1行目で止まっていることがわかります。括弧の中の数字は、コードの現在の行番号です。
オリジナルの pdb とは異なり pdb++ では、ソースコードの表示が最小限になっています。今のソースコードで何処で止まっているかを `l` で表示させてみましょう。


```
 (Pdb++) l
   1  ->	def square(n):
   2  	    result = n ** 2
   3  	    print(result)
   4  	    return result
   5
   6  	def main():
   7  	    for i in range(1,10):
   8  	        square(i)
   9
  10  	if __name__ == "__main__":
  11  	    main()
 (Pdb++)
```

コードをステップごとに実行するように  `step` を指示します。


```
 (Pdb++) step
 [2] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py(6)<module>()
 -> def main():
 (Pdb++)
```

関数  `square()` の定義が処理されて、次の関数  `main()` を定義するところまで進みました。
もういちどステップを進ませるために、今度は  `s` を指示してみましょう。



```
 (Pdb++) s
 [2] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py(10)<module>()
 -> if __name__ == "__main__":
 (Pdb++)

```

関数  `main()` の定義も終わり、 `if` 文に到達して止まりました。ここで、 `p` を使って変数の内容や条件式の評価を確認してみましょう。


```
 (Pdb++) p __name__
 '__main__'
 (Pdb++) p __name__ == "__main__"
 True
 (Pdb++)

```

 `main()` 関数を実行することになるはずだということがわかります。もう1ステップ進んでみましょう。


```
 (Pdb++) s
 [2] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py(11)<module>()
 -> main()
 (Pdb++)

```


関数 `main()` を実行する手前で止まりました。ここで、 `main()` を実行するために、 `next` を指示してみましょう。


```
 (Pdb++) next
 1
 4
 9
 16
 25
 36
 49
 64
 81
 --Return--
 [2] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py(11)<module>()->None
 -> main()
 (Pdb++)

```

 `next` は、呼び出された関数の中にステップインせずにその関数を実行します。 `main()` が実行されて戻ってきました(メッセージ： `--return--` )。もし関数にステップインしたいのであれば、 `step` を使用します。これを試すために、 `restart` を指示してみましょう。


```
 (Pdb++) restart
 Restarting /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py with arguments:

 [2] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py(1)<module>()
 -> def square(n):
 (Pdb++) l
   1  ->	def square(n):
   2  	    result = n ** 2
   3  	    print(result)
   4  	    return result
   5
   6  	def main():
   7  	    for i in range(1,10):
   8  	        square(i)
   9
  10  	if __name__ == "__main__":
  11  	    main()
 (Pdb++)
```

11行目まで `jump` を与えてジャンプしてます。


```
 (Pdb++) jump 11
 [2] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py(11)<module>()
 -> main()
 (Pdb++)
```

前回は、 `next` でしたが、 `main()` にステップインするために  `step` を指示します。


```
 (Pdb++) step
 NameError: name 'main' is not defined
 [2] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py(11)<module>()
 -> main()
 (Pdb++)
```

 `main()` が定義されていないことがわかります。 `jump` は次に実行するコードの行番号を与えます。つまり、このプログラムの関数定義を実行せずに11行目まで文字通りジャンプしたわけです。
もう一度リスタートさせて今度はブレークポイントを設定してみましょう。

 pytohn
```
 (Pdb++) restart
 Restarting /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py with arguments:

 [2] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py(1)<module>()
 -> def square(n):
 (Pdb++) break 11
 Breakpoint 1 at /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py:11
 (Pdb++)
```

行番号11 の `main()` を呼び出すところにブレークポイントが設定できした。 `continue` を指示してステップを進めましょう。


```
 (Pdb++) continue
 [2] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py(11)<module>()
 -> main()
 (Pdb++)

```

もう一度  `step` を指示して  `main()` にステップインしてみます。


```
 (Pdb++) step
 --Call--
 [3] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py(6)main()
 -> def main():
 (Pdb++) l .
   1  	def square(n):
   2  	    result = n ** 2
   3  	    print(result)
   4  	    return result
   5
   6  ->	def main():
   7  	    for i in range(1,10):
   8  	        square(i)
   9
  10  	if __name__ == "__main__":
  11 B	    main()
 (Pdb++)
```

今度は `maini()` が呼び出されて（メッセージ `--Call--` )、関数の先頭で止まっています。
順にステップを進めてみます。

 pytohn
```
 (Pdb++) step
 [3] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py(7)main()
 -> for i in range(1,10):
 (Pdb++) p i
 *** NameError: name 'i' is not defined
 (Pdb++) step
 [3] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py(8)main()
 -> square(i)
 (Pdb++) p i
 1
 (Pdb++) step
 --Call--
 [4] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/sample.py(1)square()
 -> def square(n):
 (Pdb++)
```

関数 `square()` が呼び出されてその先頭で止まりました。
ステップを進めてから `ll` を指示して現在の関数のソースコードが表示さてみましょう。
 `args` （または  `a` ）を使うと、現在の関数の引数リストを画面に表示することができます。



```
 (Pdb++) step
 [4] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py(2)square()
 -> result = n ** 2
 (Pdb++) ll
    1     def square(n):
    2  ->     result = n ** 2
    3         print(result)
    4         return result
 (Pdb++) args
```
　n = 1
　(Pdb++)


 `where` を指示するとコールスタックが表示されます。何処の今いるのかを確認することができます。


```
 Pdb++) where
 [0]   /Users/goichiiisaka/anaconda3/envs/tutorials/lib/python3.9/bdb.py(580)run()
 -> exec(cmd, globals, locals)
 [1]   <string>(1)<module>()
 [2]   /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py(11)<module>()
 -> main()
 [3]   /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py(8)main()
 -> square(i)
 [4] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py(2)square()
 -> result = n ** 2
 (Pdb++)

```

行番号3 の  `square()` の中の `はじめのコード` print()`の箇所にテンポラリブレークポイントを設定してみます。


```
 (Pdb++) tbreak 3
 Breakpoint 2 at /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py:3
 (Pdb++)
```

 `break` を引数なしで実行すると、現在設定されているブレークポイントが一覧されます。


```
 (Pdb++) break
 Num Type         Disp Enb   Where
 1   breakpoint   keep yes   at /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py:11
 	breakpoint already hit 4 times
 2   breakpoint   del  yes   at /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py:3
 (Pdb++)
```

 `continue` `で継続してみます。


```
 (Pdb++) continue
 [4] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py(3)square()
 -> print(result)
 (Pdb++)
```

期待どおりに  `print()` のところでつまりました。
ここで、もう一度 `continue` で継続してます。


```
 (Pdb++) c
 1
 4
 9
 16
 25
 36
 49
 64
 81
 The program finished and will be restarted
 [2] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py(1)<module>()
 -> def square(n):
 (Pdb++)
```

関数  `square()` の中に設定したブレークポイント番号2 は、テンポラリブレークポイントだったので一度ヒットしたときにクリアされるため、2回め以降は停止していません。 `break` だけを指示して現在のブレークポイントを確認してみます。


```
 (Pdb++) break
 Num Type         Disp Enb   Where
 1   breakpoint   keep yes   at /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py:11
 	breakpoint already hit 1 time
```

クリアされていることがわかります。
ブレークポイントは、 `enable` や  `disable` で有効/無効にすることができます。


```
 (Pdb++) disable 1
 Disabled breakpoint 1 at /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py:11
 (Pdb++) break
 Num Type         Disp Enb   Where
 1   breakpoint   keep no    at /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py:11
 	breakpoint already hit 1 time
 (Pdb++)

```

フィールド　 `Enb` の箇所が  `yes` から  `no` に変わっています。
同じように、 `clear` でブレークポイントを削除することができます。


```
 (Pdb++) clear 1
 Deleted breakpoint 1 at /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py:11
 (Pdb++)
 *** Breakpoint 1 already deleted
 (Pdb++) break
 (Pdb++)
```


### 状態の監視
プログラムの実行中に変数の変化を「監視」できれば便利なときがあります。pdbにはデフォルトで監視コマンドが含まれていませんが、commandsを使用することで同様の機能を得ることができます。commandsはブレークポイントがヒットしたときに任意のPythonコードを実行することができます。
今度は関数 `square()` で止めてコマンドブロックを設定してみましょう。


```
 (Pdb++) l 1
   1  ->	def square(n):
   2  	    result = n ** 2
   3  	    print(result)
   4  	    return result
   5
   6  	def main():
   7  	    for i in range(1,10):
   8  	        square(i)
   9
  10  	if __name__ == "__main__":
  11  	    main()
 (Pdb++) b 3
 Breakpoint 1 at /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py:3
 (Pdb++)

```

ここで、 `commands` を指示するとプロンプトが  `(com) ` に変わります。この状態で、pdbコマンドやPythonコードを記録して最後に  `c` /  `continue` で継続をさせます。


```
 (Pdb++) commands
 (com) silent
 (com) p n, result
 (com) c
 (Pdb++)

```


```
 Pdb++) c
 (1, 1)
 1
 (2, 4)
 4
 (3, 9)
 9
 (4, 16)
 16
 (5, 25)
 25
 (6, 36)
 36
 (7, 49)
 49
 (8, 64)
 64
 (9, 81)
 81
 The program finished and will be restarted
 [2] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c02_sample.py(1)<module>()
 -> def square(n):
 (Pdb++)
```


### スタックトレースとフレーム
次のような再帰呼び出しのコードを使ってスタックトレースとフレームを説明しましょう。


 c03_fibo_sample.py
```
 def fibo(n):
     if n == 0 or n == 1:
         return 1
     else:
         return fibo(n-1) + fibo(n-2)

 if __name__ == '__main__':
     v = fibo(10)
     print(v)

```

関数  `fibo()` で、ブレークポイントを設定してみます。


```
 (Pdb++) b 2
 Breakpoint 1 at /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c03_fibo_sample.py:2
 (Pdb++)

```


pdbで `w` または  `where` は、最新のフレームまでのトラック全体を表示し、現在のフレームは `>` でマークされます。
プログラムを実行して、ブレークポイントで止まったら、 `where` を使ってスタックトレース全体を表示してみましょう。



```
 (Pdb++) c
 [3] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c03_fibo_sample.py(2)fibo()
 -> if n == 0 or n == 1:
 (Pdb++) r
 [4] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c03_fibo_sample.py(2)fibo()
 -> if n == 0 or n == 1:
 (Pdb++) r
 [5] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c03_fibo_sample.py(2)fibo()
 -> if n == 0 or n == 1:
 (Pdb++) r
 [6] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c03_fibo_sample.py(2)fibo()
 -> if n == 0 or n == 1:
 (Pdb++) r
 [7] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c03_fibo_sample.py(2)fibo()
 -> if n == 0 or n == 1:
 (Pdb++) w
 [0]   /Users/goichiiisaka/anaconda3/envs/tutorials/lib/python3.9/bdb.py(580)run()
 -> exec(cmd, globals, locals)
 [1]   <string>(1)<module>()
 [2]   /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c03_fibo_sample.py(8)<module>()
 -> v = fibo(10)
 [3]   /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c03_fibo_sample.py(5)fibo()
 -> return fibo(n-1) + fibo(n-2)
 [4]   /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c03_fibo_sample.py(5)fibo()
 -> return fibo(n-1) + fibo(n-2)
 [5]   /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c03_fibo_sample.py(5)fibo()
 -> return fibo(n-1) + fibo(n-2)
 [6]   /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c03_fibo_sample.py(5)fibo()
 -> return fibo(n-1) + fibo(n-2)
 [7] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c03_fibo_sample.py(2)fibo()
 -> if n == 0 or n == 1:
 (Pdb++)

```


ここで `[数値]` はフレームの階層を表しています。

これで、 `up` と  `down` を使ってスタック内を上下できるようになりました。
今時点での `fibo()` の引数を  `args` で確認してみましょう。


```
 (Pdb++) args
 n = 6
 (Pdb++)
```

2回  `up` してから、 `args` を指示してみましょう。


```
 (Pdb++) up
 [6] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c03_fibo_sample.py(5)fibo()
 -> return fibo(n-1) + fibo(n-2)
 (Pdb++) up
 [5] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c03_fibo_sample.py(5)fibo()
 -> return fibo(n-1) + fibo(n-2)
 (Pdb++) args
 n = 8
 (Pdb++)
```

 `n` の値が 8 になっています。

同様に 2回 `down` をしてから、もう一度  `args` を指示してみましょう。


```
 (Pdb++) d
 [6] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c03_fibo_sample.py(5)fibo()
 -> return fibo(n-1) + fibo(n-2)
 (Pdb++) d
 [7] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c03_fibo_sample.py(2)fibo()
 -> if n == 0 or n == 1:
 (Pdb++) args
 n = 6
 (Pdb++)
```

もとに戻りました。

 `up` は、誤って関数の中に入ってしまった `step` で、 もとのフレームに戻りたいときにも便利です。



## pdb++ で追加された機能
### コマンド

-  `sticky` ：スティッキーモードを切り替えます。このモードでは、現在の位置が変わるたびに、画面が再描画され、関数全体が表示されます。そのため、ステップを進めていくとき、実行の流れを簡単に追うことができます。２つの行番号を与えることができ、その場合は、その範囲でスティッキーモードが有効になります。
-  `ll` /  `longlist` ：現在の関数のソースコードを表示します。通常のpdb の  `list` コマンドと違い、 `longlist` は関数全体を表示します。現在の行は矢印( `->` )  でマークされます。事後デバッグの場合、実際に例外が発生した行は  `>>` でマークされます。highlight config オプションが設定され、pygments がインストールされている場合、ソースコードがハイライトされます。
-  `interact` ：現在のスコープで見つかったすべての名前をグローバルな名前空間に含む対話型インタープリタを起動します。
-  `track EXPRESSION` ：与えた式の値がどのオブジェクトを参照しているか、また参照されているかをグラフで表示します。このコマンドを実行するには、pypyのソースコードがインポート可能である必要があります。
-  `display EXPRESSION` ：表示リストに式を追加します。このリストの式は各ステップで評価され、その値が変化するたびに表示されます。警告：これらの式は複数回評価されるため、副作用のある式を表示リストに入れないように注意してください。
-  `undisplay EXPRESSION` EXPRESSIONの表示を解除します。
-  `source EXPRESSION` ： 指定された関数/メソッド/クラスのソースコードを表示します。
-  `edit EXPRESSION` ：指定された関数/メソッド/クラスを編集するためのエディタを適切な位置に開きます。使用するエディタは、設定オプションで指定します。
-  `hf_unhide` /  `hf_hide` /   `hf_list` ：  `@pdb.hideframe()` 関数のデコレータを使って、「隠し(hide)」としてマークすることができます。デフォルトでは、隠されたフレームはスタックトレースに表示されず、上下に移動することもできません。 `hf_unhide` を使って pdb に隠した状態を無視するように指示し (すなわち、隠したフレームを通常のフレームとして扱うように)、 `hf_hide` を使って再び隠すことができます。設定オプション  `enable_hidden_frames` を使うと、隠しフレームの扱いを全般的に無効にすることができます。

### スマートなコマンドパーシング
デフォルトでは、pdbはコマンドプロンプトで入力されたものを内蔵コマンドの一つとして解釈しようとします。しかし、たまたまコマンドの一つと同じ名前を持つローカル変数の値を表示したい場合、これは少し不便です。

例えば、以下を見てください。(ファイル名  `c04_command_variable.py` )

- オリジナルのpdbの挙動

```
 (Pdb) l 1
   1  ->	def square(n):
   2  	    a = n ** 2
   3  	    print(a)
   4  	    return a
   5
   6  	def main():
   7  	    for i in range(1,10):
   8  	        square(i)
   9
  10  	if __name__ == "__main__":
  11  	    main()
 (Pdb) break 3
 Breakpoint 1 at /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c04_command_variable.py:3
 (Pdb) c
 > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c04_command_variable.py(3)square()
 -> print(a)
 (Pdb) a
 n = 1
 (Pdb)
```

 `a = n ** 2` の結果としての変数  `a` を参照したいのですが、 `args` のエリアスとしての  `a` が実行されてしまっています。
 `c` の場合は `continue` と解釈されてしまうため、デバッグしたい箇所が過ぎ去ってしまいます。これは、まずいことに `c.__class__` などのように属性値を確かめようとしたときにも発生します。

pdb++ では変数が存在する場合は常にそのスコープ内の変数を優先します。もし、本当に対応するコマンドを実行したいのであれば、２つの感嘆符（ `!!` )を前置してコマンド実行します。

- pdb++ での挙動

```
 (Pdb++) l
   1  	def square(n):
   2  	    a = n ** 2
   3 B->	    print(a)
   4  	    return a
   5
   6  	def main():
   7  	    for i in range(1,10):
   8  	        square(i)
   9
  10  	if __name__ == "__main__":
  11  	    main()
 (Pdb++) a
 1
 (Pdb++) c
 1
 [4] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c04_command_variable.py(3)square()
 -> print(a)
 (Pdb++) a
 4
 (Pdb++) !!a
 n = 2
 (Pdb++)
```


この スマートな動作は、曖昧さがある場合、つまりコマンドと同じ名前の変数が存在する場合にのみ行われることに注意してください。

 `list` コマンドについては、 `list(...)` を使用するとPythonの組み込み関数として処理される特殊なケースです。

- pdbでの挙動

```
 (Pdb) list([1, 2])
 *** Error in argument: '([1, 2])'
 (Pdb)
```

- pdb++での挙動

```
 (Pdb++) list([1, 2])
 [1, 2]
 (Pdb++)
```

## 事後デバッグ
事後デバッグ(Post-mortem debugging)は、通常通りプログラムを実行しますが、処理されない例外が発生するたびに、デバッガに戻ってプログラムの状態を調べます。その後、修正を試み、問題が解決するまでこのプロセスを繰り返していきます。

次のコードで説明してゆきましょう。

 c05_exception_sample.py
```
 def divide(a, b):
     v =  a / b
     return v

 def main():
     data = [1, 2, 0, 4]
     for i, d in enumerate(data):
         divide(i, d)

 if __name__ == "__main__":
     main()

```

このコードにはバグがあるため、実行すると例外が発生して異常終了してしまいます。

 bash
```
 $ ipython c05_exception_sample.py
 ---------------------------------------------------------------------------
 ZeroDivisionError                         Traceback (most recent call last)
 ~/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c05_exception_sample.py in <module>
       9
      10 if __name__ == "__main__":
 ---> 11     main()

 ~/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c05_exception_sample.py in main()
       6     data = [1, 2, 0, 4]
       7     for i, d in enumerate(data):
 ----> 8         divide(i, d)
       9
      10 if __name__ == "__main__":

 ~/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c05_exception_sample.py in divide(a, b)
       1 def divide(a, b):
 ----> 2     v =  a / b
       3     return v
       4
       5 def main():

 ZeroDivisionError: division by zero
```

このコードを実行するときに、 `python -m pdb` オプションを与えて実行すると、事後デバッグが行えます。

 bash
```
 $ ipython -m pdb  c05_exception_sample.py
 [2] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c05_exception_sample.py(1)<module>()
 -> def divide(a, b):
 (Pdb++)
```

デバッガが起動するので、 `continue` で継続すると例外発生までコードが進みます。

 bash
```
 (Pdb++) continue
 Traceback (most recent call last):
   File "/Users/goichiiisaka/anaconda3/envs/tutorials/lib/python3.9/pdb.py", line 1723, in main
     pdb._runscript(mainpyfile)
   File "/Users/goichiiisaka/anaconda3/envs/tutorials/lib/python3.9/pdb.py", line 1583, in _runscript
     self.run(statement)
   File "/Users/goichiiisaka/anaconda3/envs/tutorials/lib/python3.9/bdb.py", line 580, in run
     exec(cmd, globals, locals)
   File "<string>", line 1, in <module>
   File "/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c05_exception_sample.py", line 1, in <module>
     def divide(a, b):
   File "/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c05_exception_sample.py", line 8, in main
     divide(i, d)
   File "/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c05_exception_sample.py", line 2, in divide
     v =  a / b
 ZeroDivisionError: division by zero
 Uncaught exception. Entering post mortem debugging
 Running 'cont' or 'step' will restart the program
 [6] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c05_exception_sample.py(2)divide()
 -> v =  a / b
 (Pdb++) a
 2
 (Pdb++) b
 0
 (Pdb++)
```

 `b` の値がゼロ( `0` )だったために、 `ZeroDivisionError` が発生しています。

pdbは  `-c pdbコマンド` の引数を受け付けます。Python で実行する場合は、`コマンドラインで pdb コマンドを指定することが’できます。

 bash
```
 $ python -m pdb -cc exception_sample.py
 Traceback (most recent call last):
   File "/Users/goichiiisaka/anaconda3/envs/tutorials/lib/python3.9/pdb.py", line 1723, in main
     pdb._runscript(mainpyfile)
   File "/Users/goichiiisaka/anaconda3/envs/tutorials/lib/python3.9/pdb.py", line 1583, in _runscript
     self.run(statement)
   File "/Users/goichiiisaka/anaconda3/envs/tutorials/lib/python3.9/bdb.py", line 580, in run
     exec(cmd, globals, locals)
   File "<string>", line 1, in <module>
   File "/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c05_exception_sample.py", line 1, in <module>
     def divide(a, b):
   File "/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c05_exception_sample.py", line 8, in main
     divide(i, d)
   File "/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c05_exception_sample.py", line 2, in divide
     v =  a / b
 ZeroDivisionError: division by zero
 Uncaught exception. Entering post mortem debugging
 Running 'cont' or 'step' will restart the program
 [6] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c05_exception_sample.py(2)divide()
 -> v =  a / b
 (Pdb++)
```

> **注意**: IPython では  `-m pdb -cc` をうまく処理してくれません。

### コード中からの事後デバッグ

 c06_exception_post_mortem.py
```
 def divide(a, b):
     v =  a / b
     return v

 def main():
     data = [1, 2, 0, 4]
     for i, d in enumerate(data):
         divide(i, d)

 if __name__ == "__main__":
     import pdb
     try:
         main()
     except ZeroDivisionError:
         pdb.post_mortem()
```


これを実行すると、例外を補足して事後デバッグを開始します。

 bash
```
 $ ipython c06_exception_post_mortem.py
 [2] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c06_exception_post_mortem.py(2)divide()
 -> v =  a / b
 (Pdb++) a
 2
 (Pdb++) b
 0
 (Pdb++)
```


### コンテキストマネージャから事後デバッグ
 `contextlib.contextmanager` を使ってコンテキストマネージャとして事後デバッグを開始できるようにしてみましょう。
まず、次のような  `context_debug.py` を用意します。

 context_debug.py
```
 """
 Usage:

 from context_debug import debug

 with debug():
     raise Exception("now testing")
 """

 from contextlib import contextmanager

 @contextmanager
 def debug(use_pdb=True):
     try:
         yield
     except Exception as e:
         if not use_pdb:
             raise
         import sys
         import traceback
         import pdb
         info = sys.exc_info()
         traceback.print_exception(*info)
         pdb.post_mortem(info[2])

```

 07_exception_contextmanager.py
```
 def divide(a, b):
     v =  a / b
     return v

 def main():
     data = [1, 2, 0, 4]
     for i, d in enumerate(data):
         divide(i, d)

 if __name__ == "__main__":
     from context_debug import debug
     with debug():
         main()
```

 `try/except` を使用しなくてもよくなるのでスッキリします。

 bash
```
 % ipython 07_exception_contextmanager.py
 Traceback (most recent call last):
   File "/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/context_debug.py", line 15, in debug
     yield
   File "/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/07_exception_contextmanager.py", line 13, in <module>
     main()
   File "/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/07_exception_contextmanager.py", line 8, in main
     divide(i, d)
   File "/Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/07_exception_contextmanager.py", line 2, in divide
     v =  a / b
 ZeroDivisionError: division by zero
 [3] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/07_exception_contextmanager.py(2)divide()
 -> v =  a / b
 (Pdb++) a
 2
 (Pdb++) b
 0
 (Pdb++)
```

## デバッグに役立つPythonの属性

-  `dir(obj)` ：Python オブジェクトの属性を一覧します。
-  `help(obj)` ：Python オブジェクトのdocstrings を表示します。
-  `help(obj.__class__)` ：クラスの docstrinigs を表示します。
-  `pp locals()` ：現在のフレームのローカル変数を表示します。
-  `obj.__dict__` ：オブジェクトが保持している辞書
-  `obj.__class__.__dict___` ：クラスの辞書
-  `pp dict(obj.__class__.__dict__)` ：クラスの辞書を表示します。


```
 import inspect
 print(inspect.getsource(obj.__class__)
 inspect.getmro(obj.__class__)
```

## ヘルパー関数

pdb では以下のヘルパー関数が定義されており、それぞれが少しずつ異なる方法でデバッガを起動します。

#### pdb.run(statement, globals=None, locals=None)
ステートメント(文字列またはコードオブジェクトとして与えられる)をデバッガの制御下で実行します。コードが実行される前にデバッガのプロンプトが表示されます。ブレークポイントを設定して「continue」と入力するか、「step」または「next」を使用してステートメントをステップ実行することができます (これらのコマンドはすべて以下で説明します)。オプションの globals および locals 引数は、コードが実行される環境を指定します。デフォルトでは、モジュール __main__ の辞書が使用されます。(組み込みのexec()やeval()関数の説明を参照してください。)

#### pdb.runeval(expression, globals=None, locals=None)
(文字列またはコードオブジェクトとして与えられた)式をデバッガの制御下で評価します。runeval() が戻ると、式の値を返します。それ以外の場合、この関数は run() と似ています。

#### pdb.runcall(function, *args, **kwds)
与えられた引数を用いて、関数 (文字列ではなく関数またはメソッドオブジェクト) を呼び出します。runcall()が戻るときには、関数呼び出しが返したものをそのまま返します。関数が入力されると同時に、デバッガのプロンプトが表示されます。

#### pdb.set_trace(*, header=None)
呼び出し側のスタックフレームでデバッガを入力します。これは、コードがデバッグされていなくても、プログラムの特定のポイントにブレークポイントをハードコードするのに便利です (例: アサーションが失敗したときなど)。与えられれば、デバッグが始まる直前にコンソールに header が表示されます。 (Pytohn3.7 での変更点: キーワードのみの引数 header)

#### pdb.post_mortem(traceback=None)
与えられたトレースバックオブジェクトのポストモーテムデバッグを開始します。トレースバックが与えられない場合、現在処理されている例外のものを使用します（デフォルトを使用する場合、例外が処理されていなければなりません）。

#### pdb.pm()
sys.last_traceback で見つかったトレースバックのポストモーテムデバッグに入ります。

run*関数とset_trace()は、Pdbクラスをインスタンス化して同名のメソッドを呼び出すためのエイリアスです。更なる機能にアクセスしたい場合は、自分でこれを行う必要があります。

## pdb++ の新しいヘルパー関数
pdb++ には、新しい便利なヘルパー関数がいくつか提供されています。

#### pdb.xpm()
拡張された事後デバッグ(eXtended Post Mortem): これは  `pdb.post_mortem(sys.exc_info()[2]) ` と同等です。except 節の中で使用された場合、捕捉した例外を発生させた行から事後デバッグの pdb プロンプトを開始します。
#### pdb.disable()
 `pdb.set_trace()` を無効にします: これ以降の呼び出しは無視されます。
#### pdb.enable()
 `pdb.set_trace()` を再び有効にします ( `pdb.disable()` により無効化された場合)。
#### @pdb.hideframe
関数に対応するフレームを隠すように pdb++ に指示する関数デコレータです。隠されたフレームは、hf_unhide が起動されない限り、up, down または where のような対話的なコマンドを使用する際には表示されません。
#### @pdb.break_on_setattr(attrname, condition=always)
クラスデコレータ: クラスのインスタンスに属性 attrname が設定されるたびに、プログラムの実行を中断します。 `condition` は  `setattr()` のターゲットオブジェクトと実際の値を受け取る callable です。

### break_on_setattr() の使用例

 c06_break_on_setattr_demo1.py
```
 from pdb import break_on_setattr

 @break_on_setattr('bar')
 class Foo(object):
     pass
 f = Foo()
 f.bar = 42
```


このコードは、 `Foo` クラスのインスタンスの属性　 `bar` に価がセットされるたびにプログラムの実行を中断します。ブレークポイントが設定されているわけではありません。

 bash
```
 $ python c06_break_on_setattr_demo1.py
 [0] > /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/06_Pdb/c06_break_on_setattr_demo1.py(8)<module>()
 -> f.bar = 42
 (Pdb++) break
 (Pdb++)
```

例えば、特定のオブジェクトの属性が設定されたときにブレークしたい場合など、クラスがすでに作成された後でも、 `if` を使用することができます。

 c07_break_on_setattr_demo2.py
```
 from pdb import break_on_setattr

 class Foo(object):
     pass
 a = Foo()
 b = Foo()

 def break_if_a(obj, value):
     return obj is a

 break_on_setattr('bar', condition=break_if_a)(Foo)
 b.bar = 10   # ブレークはしない
 a.bar = 42   # ここでブレーク
```

このヘルパー関数は、pdb.set_trace()の後にも使用できます。

 bash
```
 (Pdb++) import pdb
 (Pdb++) pdb.break_on_setattr('tree_id')(obj.__class__)
 (Pdb++) continue
```


## コマンドヒストリ
pdb にはコマンドヒストリがあり、 `Ctrl+P` /  `Ctrl+N` などのキー操作で実行したコマンド履歴をさかのぼってコマンドを再実行することができます。ただし、デフォルトでは、pdb が終了してしまうとヒストリも消えてしまいます。

ここでは、pdb を終了時にコマンドヒストリを保存しておき、pdb 起動時には保存しておいたコマンドヒストリを読み込むようにしてみましょう。

まず、 `~/.pdb-init.py` を用意します。

 ~/.pdb-init
```
 def _pdb_init():
     import readline
     import atexit
     from pathlib import Path

     histfile = Path('~/.pdb-history').expanduser()
     if histfile.exists():
         readline.read_history_file(histfile)

     atexit.register(readline.write_history_file, histfile)
     readline.set_history_length(500)

 _pdb_init()
 del _pdb_init

```

このファイルを読み込ませるために、カレントディレクトリかホームディレクトリに次のような　 `.pdbrc` を配置します。

 .pdbrc
```
 # CAUTION: pdb only accepts single-line statements
 import os
 with open(os.path.expanduser('~/.pdb-init.py')) as _f: _f = _f.read()
 exec(_f)
 del _f

```

デフォルトでは、pdbは複数行を読みません。これで少し便利になりますよ。

## pdbrcファイル
コマンドヒストリでも触れましたが、pdb は起動時にカレントディレクトリかホームディレクトリに `.pdbrc` があれば、その内容を読み取ってくれます。


 `.pdbrc` 　のサンプル


```
 # Enable tab completion
 import pdb
 import rlcompleter
 pdb.Pdb.complete = rlcompleter.Completer(locals()).complete

 # まれにターミナルのエコーが消えてしまうことがあります
 # 次の設定は、新しい pdb をき遠うするときに復元されるはず
 import termios, sys
 termios_fd = sys.stdin.fileno()
 termios_echo = termios.tcgetattr(termios_fd)
 termios_echo[3] = termios_echo[3] | termios.ECHO
 termios_result = termios.tcsetattr(termios_fd, termios.TCSADRAIN, termios_echo)

 # 通常のPythonオブジェクトの場合、ppo　でメンバーとその値をきれいに印刷
 alias po pp %1.__dict__

 # ppioは一連のオブジェクトに対してppoを実行
 alias ppo po [a.__dict__ for a in %*]

 # 辞書をソートして印刷します。
 # 1 は辞書、%2 は名前のプレフィックスです。
 # alias p_ for k in sorted(%1.keys()): print("%s%-15s= %-80.80s" % ("%2", k, repr(%1[k])))
 alias p_ for k in sorted(%1): print("%s = %-80.80s" % (k, repr(%1[k])))

 # あるもののメンバー変数を表示
 # alias pi p_ %1.__dict__ %1.
 alias pi p_ %1.__dict__

 # selfのインスタンス変数を表示
 alias ps pi self

 # ローカル変数を表示
 alias pl p_ locals()

 # Nextしてlist, それと stepしてlist.
 alias nl n;;l
 alias sl s;;l

 # 'nspect x' は、メソッド、クラス、関数のソースコードを表示
 alias inspect import inspect; print(inspect.getsource(%1))

 # 'help x' は、オブジェクト上のインタプリタから man スタイルのヘルプを表示
 alias hh !print(help(%1))

 # pdbの小技、必要に応じてアンコメント
 # !global __currentframe, __stack; from inspect import currentframe as __currentframe, stack as __stack
 # !global __copy; from copy import copy as __copy
 # for Python <= 3.6
 # !global __Pdb; from IPython.terminal.debugger import TerminalPdb as __Pdb
 # for Python >= 3.7
 # !global __Pdb; from pdb import Pdb as __Pdb
 # !global __pdb_list; __pdb_list = [__fr[0].f_locals.get("pdb") or __fr[0].f_loc# als.get("self") for __fr in __stack() if ((type(__fr[0].f_locals.get("pdb")) is __Pdb) or (type(__fr[0].f_locals.get("self")) is __Pdb))]
 # !global __pdb; __pdb = __pdb_list[0]
 # alias _setup_watchpoint !global __key, __dict, __val; __key = '%1'; __dict = __currentframe().f_locals if (__key in __currentframe().f_locals) else __currentframe().f_globals; __val = __copy(%1)
 # alias _nextwatch_internal next;; !if __dict[__key] == __val: __pdb.cmdqueue.append("_nextwatch_internal %1")
 # alias _stepwatch_internal step;; !if __dict[__key] == __val: __pdb.cmdqueue.append("_stepwatch_internal %1")
 # alias nextwatch __pdb.cmdqueue.extend(["_setup_watchpoint %1", "_nextwatch_internal"])
 # alias stepwatch __pdb.cmdqueue.extend(["_setup_watchpoint %1", "_stepwatch_internal"])

 # for inspect
 import inspect
 alias inspect print(inspect.getsource(%1)
```



### pdb++ の設定とカスタマイズ
pdb++ をカスタマイズするには、ホームディレクトリに  `.pdbrc.py` というファイルを置きます。このファイルには、 `pdb.DefaultConfig` を継承した `Config` クラスを記述し、必要な値をオーバーライドする必要があります。
この `.pdbrc.py` は、 `.pdbrc` のような1行で定義する制約はありません。

以下に、カスタマイズできるオプションの一覧とそのデフォルト値を示します。

-  `prompt = '(Pdb++) '`
対話モードのときに表示するプロンプトです。
-  `highlight = True`
関数のロングリストを表示するとき、またはスティッキーモードのときに行番号と現在の行をハイライトします。
-  `encoding = 'utf-8'`
ファイルのエンコーディングです。文字列リテラルやコメントに国際的な文字が含まれている場合に便利です。
-  `sticky_by_default = False`
pdb++がスティッキーモードで起動するかどうかを決定します。
-  `line_number_color = Color.turquoise`
行番号に使用する色を指定します。
-  `filename_color = Color.yellow`
スタックエントリを印刷する際にファイル名に使用する色です。
-  `current_line_color = "39;49;7"`
現在の行をハイライトするANSIエスケープシーケンスのSGRパラメータです。これは、SGR エスケープシーケンス ˶sm の中で設定される。SGR パラメータを参照してください。以下は、「すべての色をリセットする」（0）、前景色を18（48;5;18）、背景を21に設定することを意味します。デフォルトでは、前景色(39)と背景色(49)を反転(7)させて使用します。
-  `use_pygments = True`
pygmentsがインストールされていて、highlight == Trueの場合、関数のロングリストを表示するときや、スティッキーモードのときに、ソースコードにシンタックスハイライトを適用します。
-  `bg = 'dark'`
 `pygments.formatters.TerminalFormatter` のコンストラクタに直接渡されます。端末の背景色に応じて、使用する配色を選択します。明るい背景色の場合には、 `'light'` に設定するようにします。
-  `colorscheme = None`
 `pygments.formatters.TerminalFormatter` のコンストラクタに直接渡されます。トークンタイプを `(lightbg, darkbg)` 色名にマップする辞書か、  `None` (デフォルト: None = 内蔵の colorscheme を使用)を想定しています。
-  `editor = '${EDITOR:-vi}'`
editコマンドを使用する際に起動するコマンドです。デフォルトでは、環境変数 EDITOR が設定されていればそれを使用し、そうでなければ  `vi` コマンドを使用します。コマンドは、ファイル名をn行目で開く標準的な記法： `COMMAND +n filename` をサポートしていなければなりません。
-  `truncate_long_lines = True`
端末の幅を超える行を切り捨てます。
-  `exec_if_unfocused = None`
pdbプロンプトを起動し、ターミナルウィンドウがフォーカスされていない場合に実行するシェルコマンドです。プログラムの実行が停止したことをユーザに知らせるために音を鳴らすなどの目的で使用します。これには wmctrl モジュールが必要です。
-  `disable_pytest_capturing = False`
古いバージョンの pytest では、テスト内で pdb.set_trace() を実行した際に、標準出力がキャプチャされているとクラッシュします (つまり、デフォルトの動作である -s オプションを使用しない場合です)。このオプションをオンにすると、対話型プロンプトを表示する前に、標準出力のキャプチャが自動的に無効になります。
-  `enable_hidden_frames = True`
特定のフレームをデフォルトで隠すことができます。このオプションを有効にすると、 hf_unhide, hf_hide, hf_list コマンドを使って、フレームの表示を制御できます。
-  `show_hidden_frames_count = True`
 `enable_hidden_frames` が `True` の場合、隠しフレームの数を表示するかどうかをコントロールします。
-  `def setup(self, pdb): pass`
このメソッドはPdbクラスの初期化中に呼ばれます。複雑なセットアップを行うのに便利です。
-  `show_traceback_on_error = True`
Pdb.errorを介したエラーのトレースバックを表示します。 `Pdb.error` は  `Pdb.default` (認識されないpdbコマンドの実行など)に由来するもので、式自体が直接の原因ではありません(例：doesnotexistのようなコマンドによるNameError)。

このオプションを無効にすると、 `*** exception string` のみが表示されますが、これは有用な文脈を欠いてしまうことがよくあります。

-  `show_traceback_on_error_limit = None`
このオプションは、 `show_traceback_on_error` が有効な場合に、 `traceback.format_exception` で使用する制限値を設定します。


 .pdbrc
```
 import pdb


 class Config(pdb.DefaultConfig):

     use_pygments = True
     disable_pytest_capturing = True
     stdin_paste = "epaste"
     filename_color = pdb.Color.lightgray
     use_terminal256formatter = False

     def __init__(self):
         try:
             from pygments.formatters import terminal
         except ImportError:
             pass
         else:
             self.colorscheme = terminal.TERMINAL_COLORS.copy()
             self.colorscheme.update(
                 {
                     terminal.Keyword: ("darkred", "red"),
                     terminal.Number: ("darkyellow", "yellow"),
                     terminal.String: ("brown", "green"),
                     terminal.Name.Function: ("darkgreen", "blue"),
                     terminal.Name.Namespace: ("teal", "turquoise"),
                 }
             )

     def setup(self, pdb):
         Pdb = pdb.__class__
         Pdb.do_l = Pdb.do_longlist
         Pdb.do_st = Pdb.do_sticky

```


## IPythonマジックコマンド
PythonのREPLより IPython をおすすめしたい理由は、[マジックコマンド ](https://ipython.readthedocs.io/en/stable/interactive/magics.html) をサポートするIPythonシェルが非常に強力であるということです。

デバッガで `IPython.embed()` を呼び出すと、IPythonインタラクティブシェルが表示されます。


```
 (Pdb++) from IPython import embed
 (Pdb++) embed()

 Type 'copyright', 'credits' or 'license' for more information
 IPython 7.28.0 -- An enhanced Interactive Python. Type '?' for help.

 In [1]: square(3)
 9
 Out[1]: 9

 In [2]: %lsmagic
 Out[2]:
 Available line magics:
 %alias  %alias_magic  %autoawait  %autocall  %autoindent  %automagic  %bookmark  %cat  %cd  %clear  %colors  %conda  %config  %cp  %cpaste  %debug  %dhist  %dirs  %doctest_mode  %ed  %edit  %env  %exit_raise  %gui  %hist  %history  %kill_embedded  %killbgscripts  %ldir  %less  %lf  %lk  %ll  %load  %load_ext  %loadpy  %logoff  %logon  %logstart  %logstate  %logstop  %ls  %lsmagic  %lx  %macro  %magic  %man  %matplotlib  %mkdir  %more  %mv  %notebook  %page  %paste  %pastebin  %pdb  %pdef  %pdoc  %pfile  %pinfo  %pinfo2  %pip  %popd  %pprint  %precision  %prun  %psearch  %psource  %pushd  %pwd  %pycat  %pylab  %quickref  %recall  %rehashx  %reload_ext  %rep  %rerun  %reset  %reset_selective  %rm  %rmdir  %run  %save  %sc  %set_env  %sx  %system  %tb  %time  %timeit  %unalias  %unload_ext  %who  %who_ls  %whos  %xdel  %xmode

 Available cell magics:
 %%!  %%HTML  %%SVG  %%bash  %%capture  %%debug  %%file  %%html  %%javascript  %%js  %%latex  %%markdown  %%perl  %%prun  %%pypy  %%python  %%python2  %%python3  %%ruby  %%script  %%sh  %%svg  %%sx  %%system  %%time  %%timeit  %%writefile

 Automagic is ON, % prefix IS NOT needed for line magics.

 In [3]: exit

 (Pdb++)
```

 `embed()` は，呼び出したフレームからすべての変数とオブジェクトを読み込んだ ipython のREPLシェルが開きます。シェルを終了すると、デバッガのプロンプトに戻ります。ipythonシェルで行った変更は、ipdbシェルのオブジェクトや変数には影響しません。
ipdb だと複数行の挿入ができませんし、シェルコマンドを実行することも面倒なのですが、そうした問題が解消されるため使い勝手がよくなります。




## 参考
- Python公式ドキュメント
  - [traceback --- スタックトレースの表示または取得 ](https://docs.python.org/ja/3/library/traceback.html)
  - [inspect --- 活動中のオブジェクトの情報を取得する ](https://docs.python.org/ja/3/library/inspect.html)
  - [pdb --- Python デバッガ  ](https://docs.python.org/ja/3/library/pdb.html)
- [Python のダンダーな名前まとめ ](https://github.com/gh640/python-dunder-names-ja)
- [ipdb ソースコード ](https://github.com/gotcha/ipdb)
- [pdb++ ソースコード　](https://github.com/pdbpp/pdbpp)
- [watchpoints ソースコード ](https://github.com/gaogaotiantian/watchpoints)
