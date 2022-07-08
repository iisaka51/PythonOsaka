snoopモジュールを使ってみよう
=================
## snoopについて
snoop は強力な Python デバッグツールです。snoop は [PySnooper  https://github.com/cool-RR/PySnooper]をより機能的で洗練させたものです。また、独自バージョンの [icecream ](https://github.com/gruns/icecream) やその他の気の利いたものも含まれています。

### ユースケース
あなたは、自分のPythonコードがなぜあなたが思うように動かないのかを理解しようとしています。ブレークポイントや監視機能を備えた本格的なデバッガを使いたいが、今はそれを設定するのが面倒だ。
どの行が実行されていて、どの行が実行されていないのか、ローカル変数の値はどうなっているのかを知りたいのです。

ほとんどの人は、戦略的な場所に `print()` を使い、ときにには変数の値を表示することもあるでしょう。

snoopでは同じことができます。ただし、適切なプリントラインを慎重に作成する代わりに、興味のある関数にデコレーターラインを1つ追加するだけです。どの行がいつ実行されたのか、ローカル変数がいつ変更されたのかなど、関数のプレイバイプレイのログを得ることができます。

## インストール

snoop のインストールは pip  コマンドで行います。

 bash
```
 $ pip inssall snoop
```


## 基本的な使用方法

次のような、数字を2進法に変換する関数で説明してゆきます。
この関数に  `@snoop` デコレーターを追加して、その内容を調べてみましょう。


```
 In [2]: # %load 01_decorator.py
   ...: import snoop
   ...:
   ...: @snoop
   ...: def number_to_bits(number):
   ...:     if number:
   ...:         bits = []
   ...:         while number:
   ...:             number, remainder = divmod(number, 2)
   ...:             bits.insert(0, remainder)
   ...:         return bits
   ...:     else:
   ...:         return [0]
   ...:
   ...: # number_to_bits(6)
   ...:
```


```
 In [3]: number_to_bits(6)
 11:01:28.17 >>> Call to number_to_bits in File "<ipython-input-2-3559cd754fcf>", line 5
 11:01:28.17 ...... number = 6
 11:01:28.17    5 | def number_to_bits(number):
 11:01:28.17    6 |     if number:
 11:01:28.17    7 |         bits = []
 11:01:28.17    8 |         while number:
 11:01:28.17    9 |             number, remainder = divmod(number, 2)
 11:01:28.17 .................. number = 3
 11:01:28.17 .................. remainder = 0
 11:01:28.17   10 |             bits.insert(0, remainder)
 11:01:28.17 .................. bits = [0]
 11:01:28.17 .................. len(bits) = 1
 11:01:28.17    8 |         while number:
 11:01:28.17    9 |             number, remainder = divmod(number, 2)
 11:01:28.17 .................. number = 1
 11:01:28.17 .................. remainder = 1
 11:01:28.17   10 |             bits.insert(0, remainder)
 11:01:28.17 .................. bits = [1, 0]
 11:01:28.17 .................. len(bits) = 2
 11:01:28.17    8 |         while number:
 11:01:28.17    9 |             number, remainder = divmod(number, 2)
 11:01:28.17 .................. number = 0
 11:01:28.17   10 |             bits.insert(0, remainder)
 11:01:28.18 .................. bits = [1, 1, 0]
 11:01:28.18 .................. len(bits) = 3
 11:01:28.18    8 |         while number:
 11:01:28.18   11 |         return bits
 11:01:28.18 <<< Return value from number_to_bits: [1, 1, 0]
 Out[3]: [1, 1, 0]
 
 In [4]:
```

いかに簡単であるかに注目してください。ssnoopをインポートして、対象の関数に `@snoop` とアノテーションするだけです。
動作過程が、標準エラー出力(stderr) への出力されます。

魔法のように見えるインポートが好みでないなら、次のように使用することもできます。


```
 import snoop
 
 @snoop.snoop
 def number_to_bits(number):
     # ...
     
```


```
 from snoop import snoop
 
 @snoop
 def number_to_bits(number):
     # ...
     
```

プロジェクトに不要なインポートを一切したくない場合は、 `install()` をどこかで一度だけ呼んでおくだけで組み込み関数のように使用できます。（詳しくは後述します）

もっと複雑な例を見てみましょう。これは、関数の引数と戻り値をキャッシュに保存し、再計算を避けるためのものです。


```
 In [2]: # %load 02_more_complex.py
    ...: import snoop
    ...:
    ...: def cache(func):
    ...:     d = {}
    ...:
    ...:     def wrapper(*args):
    ...:         try:
    ...:             return d[args]
    ...:         except KeyError:
    ...:             result = d[args] = func(*args)
    ...:             return result
    ...:
    ...:     return wrapper
    ...:
    ...: @snoop(depth=2)
    ...: @cache
    ...: def add(x, y):
    ...:     return x + y
    ...:
    ...: # add(1, 2)
    ...: # add(1, 2)
    ...:
 
 In [3]:
 
```

ここでは  `depth=2` を指定して、内部の関数呼び出しにも1レベル下がるようにしています。そして、この関数を2回呼び出して、キャッシングの動作を確認します。


```
 In [3]: add(1,2)
 11:03:50.80 >>> Call to cache.<locals>.wrapper in File "<ipython-input-2-0e3dd32677d0>", line 7
 11:03:50.80 .......... args = (1, 2)
 11:03:50.80 .......... len(args) = 2
 11:03:50.80 .......... d = {}
 11:03:50.80 .......... func = <function add at 0x110beea60>
 11:03:50.80    7 |     def wrapper(*args):
 11:03:50.80    8 |         try:
 11:03:50.80    9 |             return d[args]
 11:03:50.81 !!! KeyError: (1, 2)
 11:03:50.81 !!! When subscripting: d[args]
 11:03:50.81   10 |         except KeyError:
 11:03:50.81   11 |             result = d[args] = func(*args)
     11:03:50.81 >>> Call to add in File "<ipython-input-2-0e3dd32677d0>", line 18
     11:03:50.81 ...... x = 1
     11:03:50.81 ...... y = 2
     11:03:50.81   18 | def add(x, y):
     11:03:50.81   19 |     return x + y
     11:03:50.81 <<< Return value from add: 3
 11:03:50.81   11 |             result = d[args] = func(*args)
 11:03:50.81 .................. result = 3
 11:03:50.81 .................. d = {(1, 2): 3}
 11:03:50.81 .................. len(d) = 1
 11:03:50.81   12 |             return result
 11:03:50.81 <<< Return value from cache.<locals>.wrapper: 3
 Out[3]: 3
 
 In [4]:
 
```

最初の呼び出しではキャッシュの検索に失敗して KeyError が発生したため、元の  `add()` 関数が呼び出されています。
もう一度呼び出してみましょう。


```
 In [4]: add(1, 2)
 11:06:13.19 >>> Call to cache.<locals>.wrapper in File "<ipython-input-2-0e3dd32677d0>", line 7
 11:06:13.19 .......... args = (1, 2)
 11:06:13.19 .......... len(args) = 2
 11:06:13.19 .......... d = {(1, 2): 3}
 11:06:13.19 .......... len(d) = 1
 11:06:13.19 .......... func = <function add at 0x1042f8940>
 11:06:13.19    7 |     def wrapper(*args):
 11:06:13.19    8 |         try:
 11:06:13.19    9 |             return d[args]
 11:06:13.19 <<< Return value from cache.<locals>.wrapper: 3
 Out[4]: 3
 
 In [5]:
 
```

2 回目の呼び出しでは以前にキャッシュされた結果がすぐに返されていることがわかります。

関数全体をトレースしたくない場合は、関連する部分を  `with` ブロックで囲むことができます。


```
 In [2]: # %load 03_context_manager.py
    ...: import snoop
    ...: import random
    ...:
    ...: def foo():
    ...:     lst = []
    ...:     for i in range(10):
    ...:         lst.append(random.randrange(1, 1000))
    ...:
    ...:     with snoop:
    ...:         lower = min(lst)
    ...:         upper = max(lst)
    ...:         mid = (lower + upper) / 2
    ...:
    ...:     return lower, mid, upper
    ...:
    ...: # foo()
    ...:
 
 In [3]:
 
```

これは次のような出力になります。


```
 In [3]: foo()
 11:08:17.62 >>> Enter with block in foo in File "<ipython-input-2-71310a58b972>", line 10
 11:08:17.62 .......... lst = [999, 914, 911, 243, 105, 585, 960, 209, 944, 347]
 11:08:17.62 .......... len(lst) = 10
 11:08:17.62 .......... i = 9
 11:08:17.62   11 |         lower = min(lst)
 11:08:17.62 .............. lower = 105
 11:08:17.62   12 |         upper = max(lst)
 11:08:17.62 .............. upper = 999
 11:08:17.62   13 |         mid = (lower + upper) / 2
 11:08:17.63 .............. mid = 552.0
 11:08:17.63 <<< Exit with block in foo
 Out[3]: (105, 552.0, 999)
 
 In [4]:
 
```

### snoop の共通の引数
snoopに引数を与えることができます。

-  `depth` : トレースする関数/ブロックのより深い呼び出しを調べます。デフォルトは1で、内部の呼び出しがないことを意味しますので、より大きな値を指定してください。
-  `watch` : 任意の式を文字列で指定して、その値を表示します。

```
 @snoop(watch=('foo.bar', 'self.x["whatever"]'))
```

-  `watch_explode` ：変数や式を展開すると、そのすべての属性やリスト/辞書の項目が表示されます。


```
 @snoop(watch_explode=['foo', 'self'])
```

これは、次のような出力になります。

 bash
```
 ........ foo[2] = 'whatever'
 ........ self.baz = 8
 
```

この引数のより高度な使い方については、「watch_explodeの制御」を参照してください。

任意の値（ローカル変数、監視対象の式、分解された項目）に関する追加情報を自動的に表示するには 「watch_extras 」を参照してください。


## pp() - 素晴らしいデバッグライト
snoopはデバッグライトとしての `print()` をタイプする手間を省くことを目的としていますが、それでも時にはデバッグライトが必要になることがあります。  `pp()` はそうしたときにうってつけのものです。 `pp()` は単独でも、snoopと組み合わせても使うことができます。 `pp()` は icecream の  `ic()` を、snioop が独自に実装したバージョンです。

 `pp(x)` は   `x = <pretty printed value of x>` を出力します。つまり、何が出力されているかがわかるように引数のソースコードを表示し、複雑なデータ構造のレイアウトを簡単に確認できるように  `pprint.pformat` で値をフォーマットします。 `prettyprinter` や `pprintpp` がインストールされている場合は、 `pprint` .pformatの代わりにそれらのpformatが使用されます。


```
 In [2]: # %load 04_pp_intro.py
    ...:
    ...: def foo(i):
    ...:     return i + 333
    ...:
    ...: print('\n単なるデバッグライト')
    ...: print(foo(123))
    ...:
    ...: print('\n説明を追加したデバッグライト')
    ...: print('foo(123)):', foo(123))
    ...:
    ...: print('\nsnoop.pp によるデバッグライト')
    ...: from snoop import pp
    ...: pp(foo(123))
    ...:
 
 単なるデバッグライト
 456
 
 説明を追加したデバッグライト
 foo(123)): 456
 
 snoop.pp によるデバッグライト
 15:01:01.19 LOG:
 15:01:01.20 .... foo(123) = 456
 Out[2]: 456
 
 In [3]:
```

 `pp()` はその引数を直接返しますので、再編成することなくコードに簡単に挿入することができます。複数の引数が与えられた場合は、タプルとして返されますので、  `foo(x, y)` を  `foo(*pp(x, y))` に置き換えても、コードの動作はそのままです。

以下はその例です。


```
 In [2]: # %load 05_pp.py
    ...: from snoop import pp
    ...:
    ...: x = 1
    ...: y = 2
    ...:
    ...: def debug():
    ...:     pp(pp(x + 1) + max(*pp(y + 2, y + 3)))
    ...:
    ...: # debug()
    ...:
 
 In [3]: debug()
 11:21:51.30 LOG:
 11:21:51.31 .... x + 1 = 2
 11:21:51.31 LOG:
 11:21:51.31 .... y + 2 = 4
 11:21:51.31 .... y + 3 = 5
 11:21:51.31 LOG:
 11:21:51.32 .... pp(x + 1) + max(*pp(y + 2, y + 3)) = 7
 
 In [4]:
```


すでにsnoopがインポートされている場合は、 `snoop.pp()` も使用できます。しかし、理想的には `install()` を使用して、インポートを一切行わないようにすることです。(詳しくは後述します）

 `pp()` が引数のソースコードを見つけられない状況がいくつかありますが、その場合は代わりにプレースホルダーを表示します。

- Pythonシェルの中にいる場合などでは、ソースは  `linecache` から取得されます。
- Python 3.4 と PyPy においてソースコードが見つけられません。
- pytest や birdseye (および @spy デコレーター) のような、内部的にソースコードを変換するマジックが存在する場合。
- pp や snoop を最初に呼び出す前にソースファイルが変更されている場合。

 `pp()` は、関数呼び出しの**抽象構文木（Abstract Syntax Tree: AST)**ノードを特定するために、ライブラリexecutingを使用しています。もし、自分でクールなユーティリティを書きたいのであれば、チェックしてみてください。

 `pp()` は icecream に触発されたもので、同じ基本的な印刷用 API を提供していますが、pp は snoop とシームレスに統合されており、独自の  `pp.deep()` を提供しています。

#### pp


##  部分式をトレースするpp.deep()
 `pp(<complicated expression>)` があって、最終的な値だけでなく、その式の内部で何が起こっているかを見たい場合は、 `pp.deep(lambda: <complicated expression>)` に置き換えてください。これにより、すべての部分式が正しい順序で記録され、追加の副作用はなく、最終値が返されます。先ほどの例を `pp.deep()` に置き換えてみます。


```
 In [2]: # %load 06_pp_deep.py
    ...: from snoop import pp
    ...:
    ...: x = 1
    ...: y = 2
    ...:
    ...: def debug():
    ...:     # pp(pp(x + 1) + max(*pp(y + 2, y + 3)))
    ...:     pp.deep(lambda: x + 1 + max(y + 2, y + 3))
    ...:
    ...: # debug()
    ...:
 
 In [3]:
 
```



```
 In [3]: debug()
 11:41:21.03 LOG:
 11:41:21.05 ............ x = 1
 11:41:21.05 ........ x + 1 = 2
 11:41:21.05 ................ y = 2
 11:41:21.05 ............ y + 2 = 4
 11:41:21.05 ................ y = 2
 11:41:21.05 ............ y + 3 = 5
 11:41:21.05 ........ max(y + 2, y + 3) = 5
 11:41:21.05 .... x + 1 + max(y + 2, y + 3) = 7
 
 In [4]:
 
```



例外が発生した場合は、どの部分式が原因なのかが表示されます。


```
 In [2]: # %load 07_exception.py
    ...: from snoop import pp
    ...:
    ...: x = 0
    ...: y = 2
    ...:
    ...: def debug():
    ...:     pp.deep(lambda: x + 1 + (y + 3) / x)
    ...:
    ...: # debug()
    ...:
 
 In [3]:
 
```

次のようになります。


```
 In [3]: debug()
 11:52:16.81 LOG:
 11:52:16.82 ............ x = 0
 11:52:16.82 ........ x + 1 = 1
 11:52:16.82 ................ y = 2
 11:52:16.82 ............ y + 3 = 5
 11:52:16.82 ............ x = 0
 11:52:16.82 ........ (y + 3) / x = !!! ZeroDivisionError!
 ---------------------------------------------------------------------------
 ZeroDivisionError                         Traceback (most recent call last)
 <ipython-input-3-562b7cea5782> in <module>
 ----> 1 debug()
 
 <ipython-input-2-b55fcd00ec9e> in debug()
       6
       7 def debug():
 ----> 8     pp.deep(lambda: x + 1 + (y + 3) / x)
       9
      10 # debug()
  (中略)
 
 ZeroDivisionError: division by zero
 
 In [4]:
```


この機能が気に入った人は、 `@spy` も好きなはずです。



## @spy
 `@spy` デコレーターを使うと、 `@snoop` と強力なデバッガであるbirdseyeを組み合わせることができます。


```
 from snoop import spy  # not required if you use install()
 
 @spy
 def foo():
     # ...
     
```

これは、次と同じことです。


```
 import snoop
 from birdseye import eye
 
 @snoop
 @eye
 def foo():
     # ...
```

 `@spy` の名前は、その機能が  `snoop` と　 `eye` を組み合わせていることに由来しています。


```
 In [2]: # %load 08_spy.py
    ...: from snoop import spy
    ...:
    ...: def add_one(a):
    ...:     return a + 1
    ...:
    ...: @spy
    ...: def myfunc(x, y):
    ...:     v =  add_one(x) + (y + 3) / x
    ...:     return v
    ...:
    ...: def main():
    ...:     try:
    ...:         myfunc(0, 1)
    ...:     except:
    ...:         pass
    ...:
    ...: # main()
    ...:
 
 In [3]:
 
```



```
 In [3]: main()
 12:29:18.77 >>> Call to myfunc in File "<ipython-input-2-b1bbcb0f2cea>", line 8
 12:29:18.77 ...... x = 0
 12:29:18.77 ...... y = 1
 12:29:18.77    8 | def myfunc(x, y):
 12:29:18.77    9 |     v =  add_one( x ) + ( y + 3 ) / x
 12:29:18.78 !!! ZeroDivisionError: division by zero
 12:29:18.79 !!! Call ended by exception
 
 In [4]:
 
```

あるいは、別ターミナルで birdseye を実行してデバッグUIを起動し、ブラウザで `http://localhost:7777/' を開きます。
次のように実行結果を参照することができます。

![](https://gyazo.com/9f76d1457884b555f108def39ee1a23f.png)


別途birdseyeをインストールする必要があります。

 bash
```
 $ pip install birdseye
```

 `@spy` の唯一の大きな欠点は、パフォーマンスが著しく低下することです。そのため、ループの繰り返しが多い関数では避けてください。それ以外は基本的に常に `@snoop` の代わりに使うことができます。ログに必要な情報がない場合は、コードを編集したり再実行したりすることなく、birdseye UIを開いて詳細を確認することができます。どのツールがいいのかわからない、というときに最適です。

 `@spy` は引数を `snoop` に渡ため、例えば `@spy(depth=2, watch='x.y')` はうまく動作します。

## install()

プロジェクトの定期的なデバッグをより便利にするために、次のコードを早い段階で実行するようにします。


```
 import snoop
 
 snoop.install()
```

 `install()` を呼び出した以降は、 `@snoop` 、 `@spy` 、 `pp()` は、インポートしなくても、すべてのファイルで利用できるようになります。

キーワード引数  `<original name>=<new name>` を渡すことで、異なる名前を選択することができます。


```
 snoop.install(snoop="ss")
```

この場合、 `@ss` で関数をデコレートすることができます。

この機能が好みでなく普通に import したいが、他の設定のために  `install()` を使いたい場合は、 `builtins=False` を渡してください。

別の方法として、Python 3.7以降では、環境変数として  `PYTHONBREAKPOINT=snoop.snoop` を設定することで、snoop を新しい breakpoint 関数を使用することができます。

## 無効化(Disable)
snoopや他の関数をコードに残しつつ、その効果を無効にしたい場合は、 `enabled=False` を渡してください。例えば、Django を使っている場合、 `settings.py` に  `snoop.install(enabled=DEBUG)` を記述すると、運用時に自動的に無効化されます。無効にすると、パフォーマンスへの影響は最小限に抑えられ、どこにも出力されません。

また、特別なビューやシグナルハンドラなどで  `snoop.install(enabled=True)` を再度呼び出すことで、任意の時点で動的に機能を再有効化することができます。

## 出力の設定
 `install()` には、 `@snoop` や `pp()` の出力を制御するためのいくつかのキーワード引数があります。

-  `out` ：　出力先を指定します。デフォルトではstderrとなります。を渡すこともできます。
  - 文字列またはPathオブジェクトを渡すと、その場所にあるファイルに書き込まれます。デフォルトでは、常にファイルに追加されます。 `overwrite=True` を渡すと、最初にファイルをクリアします。
  - sys.stdoutやファイルオブジェクトなど、 `write()` メソッドを持つもの。
  - logger.infoのように、文字列を1つ引数に持つ呼び出し可能なもの。
-  `color` :  コンソールに色付きのテキストを表示するためのエスケープ文字を出力に含めるかどうかを決定します。もし、出力に変な文字が含まれていたら、コンソールが色をサポートしていないので、 `color=False` を渡してください。
  - コードはPygmentsを使ってシンタックスハイライトされますが、この引数はスタイルとして渡されます。スタイルを指定する文字列（このギャラリーを参照）やスタイルクラスを渡すことで、異なる配色を選択することができます。デフォルトのスタイルは monokai です。
  - デフォルトでは、このパラメータは `out.isatty()` に設定されています。通常、stdoutとstderrはtrueになりますが、リダイレクトされたりパイプされたりするとfalseになります。強制的に色をつけたい場合は、Trueまたはstyleを渡します。
  - PyCharm Runウィンドウに色を表示するには、Run Configurationを編集し、"Emulate terminal in output console "にチェックを入れてください。
-  `prefix` ： 文字列を渡すと、すべてのsnoopの行がその文字列で始まり、簡単にgrepできるようになります。
-  `columns` ：　各出力行の先頭に表示する列を指定します。内蔵されているカラムの名前をスペースまたはカンマで区切って文字列を渡すことができます。利用できるカラムは以下のとおりです。
  -  `time` ：　現在の時刻。デフォルトではこの列だけです。
  -  `thread` ：　現在のスレッド名。現在のスレッドの名前です。
  -  `thread_ident` ：　スレッド名が一意でない場合に備えて、現在のスレッドの識別子です。
  -  `file` ：　現在の関数のファイル名（フルパスではありません）。
  -  `full_file` ：　ファイルのフルパス。ファイルのフルパス（関数が呼び出されたときにも表示されます）。
  -  `function` ：　現在の関数の名前を指定します。
  -  `function_qualname` ：　現在の関数の修飾名です。
-  `watch_extras` および  `replace_watch_extras` については、「高度な使い方」を参照してください。

カスタムカラムが必要な場合は、GitHubのIssueを開いて何に興味があるのか教えてください。今現在では、とりあえず、リストを渡すことができます。リストの要素は文字列か callable です。callableは1つの引数を取り、それはEventオブジェクトになります。このオブジェクトは、 `sys.settrace()` で指定された `frame` 、 `event` 、  `arg` の属性を持ち、その他の属性は変更される可能性があります。

-  `pformat` ：　ppが使用するプリティフォーマット関数を設定します。デフォルトでは、 `prettyprinter.pformat`  `pprintpp.pformat` 、 `pprint.pformat` のうち、インポート可能な最初のものを使います。


## PySnooperとのAPIの違い
snoop と　PySnooper とでは、次のようなAPIの違いがあります。もしあなたがPySnooperに慣れているのであれば、注意してください。

-  `snoop()` ではなく、 `install()` に `prefix` と `overwrite` を渡します。
-  `pysnooper.snoop()` の第一引数は  `output` と呼ばれますが、 `install()` には  `out` というキーワードで渡す必要があります。
-  `snoop(thread_info=True)` の代わりに  `install(columns='time thread thread_ident')` と記述します。
- 環境変数　 `PYSNOOPER_DISABLED` の代わりに  `install(enabled=False)` とします。
-  `custom_repr` を使用しません。「watch_extras」 および 「変数の表示をカスタマイズ」を参照してください。
- PySnooper の代わりに snoop を使う価値があるかどうかわからない場合は、こちらの比較をご覧ください。


## IPython/Jupyterの統合
snoopには、シェルやノートブックで使用できるIPythonの拡張機能が付属しています。

ノートブックのセルで `%load_ext snoop` を使うか、IPythonの設定ファイル( `~/.ipython/profile_default/ipython_config.py` など)で `c.InteractiveShellApp.extensions` リストに'snoop'を追加して、拡張機能をロードする必要があります。

 ~/.ipython/profile_default?ipython_config
```
 # snoop 拡張機能の設定例
 c.TerminalIPythonApp.extensions = [
      'snoop',
 ]
 
```

そして、ノートブックのセルの先頭にあるセルマジック  `%%snoop` を使って、そのセルをトレースします。

![](https://gyazo.com/21eab29aab48d0bd3092fa605ce0ec0c.png)




## 高度な使い方

## watch_extras
 `install()` には  `watch_extras` という別の引数があります。これに関数のリストを渡すと、ローカル変数、監視対象の式、分解された項目など、任意の値に関する追加情報を自動的に表示することができます。例えば、すべての変数の型を確認したいとします。次のように使用することができます。


```
 import snoop
  
  def type_watch(source, value):
      return 'SNOOP: type({})'.format(source), type(value)
  
  snoop.install(watch_extras=[type_watch])
     
```



```
 In [2]: # %load 20_watch_extras.py
    ...: import snoop
    ...:
    ...: def type_watch(source, value):
    ...:     return 'SNOOP: type({})'.format(source), type(value)
    ...:
    ...: snoop.install(watch_extras=[type_watch])
    ...:
    ...: @snoop
    ...: def number_to_bits(number):
    ...:     if number:
    ...:         bits = []
    ...:         while number:
    ...:             number, remainder = divmod(number, 2)
    ...:             bits.insert(0, remainder)
    ...:         return bits
    ...:     else:
    ...:         return [0]
    ...:
    ...:
    ...: # number_to_bits(6)
    ...:
 
 In [3]:
```



```
 In [3]: number_to_bits(6)
 13:34:13.64 >>> Call to number_to_bits in File "<ipython-input-2-df06e0e0a79a>", line 10
 13:34:13.64 ...... number = 6
 13:34:13.64 ...... SNOOP: type(number) = <class 'int'>
 13:34:13.64   10 | def number_to_bits(number):
 13:34:13.64   11 |     if number:
 13:34:13.64   12 |         bits = []
 13:34:13.64 .............. SNOOP: type(bits) = <class 'list'>
 13:34:13.64   13 |         while number:
 13:34:13.64   14 |             number, remainder = divmod(number, 2)
 13:34:13.64 .................. number = 3
 13:34:13.64 .................. remainder = 0
 13:34:13.64 .................. SNOOP: type(remainder) = <class 'int'>
 13:34:13.64   15 |             bits.insert(0, remainder)
 13:34:13.64 .................. bits = [0]
 13:34:13.64 .................. len(bits) = 1
 13:34:13.64   13 |         while number:
 13:34:13.64   14 |             number, remainder = divmod(number, 2)
 13:34:13.64 .................. number = 1
 13:34:13.64 .................. remainder = 1
 13:34:13.64   15 |             bits.insert(0, remainder)
 13:34:13.64 .................. bits = [1, 0]
 13:34:13.64 .................. len(bits) = 2
 13:34:13.64   13 |         while number:
 13:34:13.64   14 |             number, remainder = divmod(number, 2)
 13:34:13.64 .................. number = 0
 13:34:13.64   15 |             bits.insert(0, remainder)
 13:34:13.64 .................. bits = [1, 1, 0]
 13:34:13.64 .................. len(bits) = 3
 13:34:13.64   13 |         while number:
 13:34:13.64   16 |         return bits
 13:34:13.64 <<< Return value from number_to_bits: [1, 1, 0]
 Out[3]: [1, 1, 0]
 
 In [4]:
 
```


 `watch_extras` に与える関数は、2つの引数  `source` と  `value` を受け取るようにします。通常、これらは変数名とその実際の値になります。これらの関数は、返される情報の `source` （表示のためだけに使用され、有効なPythonである必要はありません）と実際の情報を表すペアを返す必要があります。もし、特定の値に対して何も表示したくない場合は、 `None` を返してください。発生した例外はすべてキャッチされ、黙殺されます。

 `watch_extras` には、2つの関数がデフォルトですでに有効になっています。

-  `len()` もしくは. `shape` プロパティ（numpy、pandas、tensorflowなどで使用されます）を表示する関数
- .dtype`プロパティを表示する関数

 `watch_extras` はこれら 2 つのデフォルトの関数に追加されるので、再度指定する必要はありません。これらを含めたくない場合は、代わりに `replace_watch_extras` を使って正確なリストを指定してください。

デフォルトの関数は次で定義されています。

```
 from snoop.configuration import len_shape_watch, dtype_watch
```


## watch_explodeの制御
watch_explodeは、渡された式をどのように展開するかを、そのクラスに基づいて自動的に推測します。以下のクラスのいずれかを使用することで、より具体的になります。


```
 @snoop(watch=(
     snoop.Attrs('x'),    # Attributes (specifically from __dict__ or __slots__)
     snoop.Keys('y'),     # Mapping (e.g. dict) items, based on .keys()
     snoop.Indices('z'),  # Sequence (e.g. list/tuple) items, based on len()
 ))
```

 `Attrs('x', exclude=('_foo', '_bar'))` のように、 `exclude` パラメータで特定のキー/属性/インデックスを除外します。

 `Indices` の後にスライスを追加すると、そのスライス内の値のみが表示されます。 例： `Indices('z')[-3:]` 

### 変数の表示をカスタマイズ
(watch_extras も参照)
値の表示には、パフォーマンスを向上させ、コンソールがあふれないようにするために、cheap_reprライブラリを使用しています。これは、サードパーティのライブラリを含む、ほとんどの一般的なクラスに対して、特別に定義されたrepr関数を持っています。クラスが見つからない場合は、cheap_reprに問題をレポートしてください。また、そのクラスに対する独自のreprを登録することもできます。以下はその例です。



```
 from cheap_repr import register_repr, cheap_repr
 
 class MyClass(object):
     def __init__(self, items):
         self.items = items
         
 @register_repr(MyClass)
 def repr_my_class(x, helper):
     return '{}(items={})'.format(
         x.__class__.__name__,
         cheap_repr(x.items, helper.level - 1),
     )
```

個々のクラスの冗長性を高めることもできます。


```
 from cheap_repr import find_repr_function
 
 find_repr_function(list).maxparts = 100
 
```

## 複数の個別設定
`install() `でのグローバルな設定よりも、個別の制御が必要な場合、例えば、1つのプロセスで複数の異なるファイルに書き込みたい場合には、Configオブジェクトを作成することができます。例：` config = snoop.Config(out=filename)`
そうすると、 `config.snoop` 、 `config.pp` 、 `config.spy` は、グローバルなものではなく、Configで設定されたものを使用します。
引数は、出力設定やenabledに関する  `install()` の引数と同じです。



## 参考
- [PySnoop ソースコード ](https://github.com/cool-RR/PySnooper)
- [icecream ソースコード　](https://github.com/gruns/icecream)
- [birdseye ソースコード ](https://github.com/alexmojaki/birdseye)
- [cheap_repr ソースコード　](https://github.com/alexmojaki/cheap_repr)


