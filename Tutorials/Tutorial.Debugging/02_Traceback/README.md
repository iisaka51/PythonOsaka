Pythonのトレースバック
=================

## トレースバック
Python ではプログラムで例外あ発生したときに、どのモジュールの、どの関数が呼び出された、どこでエラーが発生したのかを特定できる情報をトレースバックとして出力してくれます。
例示のために次のコードを用意しました。


```
 In [2]: # %load 01_mydivide.py
    ...: def my_divide(a, b):
    ...:     return a / b
    ...:
    ...: if __name__ == '__main__':
    ...:     data = [1,0,2,3]
    ...:     for n in data:
    ...:         print(my_divide(1,n))
    ...:     print('done.')
    ...:
 1.0
 ---------------------------------------------------------------------------
 ZeroDivisionError                         Traceback (most recent call last)
 <ipython-input-2-425977e6fb8b> in <module>
       6     data = [1,0,2,3]
       7     for n in data:
 ----> 8         print(my_divide(1,n))
       9     print('done.')
 
 <ipython-input-2-425977e6fb8b> in my_divide(a, b)
       1 # %load 01_mydivide.py
       2 def my_divide(a, b):
 ----> 3     return a / b
       4
       5 if __name__ == '__main__':
 
 ZeroDivisionError: division by zero
 
 In [3]:
 
```

friendly パッケージがインストールされていると、このトレースバックを実行時の変数のオブジェクトの値といっしょに整形して出力してくれます。

 bash
```
 % ipython -m friendly 01_mydivide.py
 1.0
 
 ╭────────────────────────────────── Traceback ──────────────────────────────────╮
 │ Traceback (most recent call last):                                            │
 │   File "01_mydivide.py", line 7, in <module>                                  │
 │     print(my_divide(1,n))                                                     │
 │   File "01_mydivide.py", line 2, in my_divide                                 │
 │     return a / b                                                              │
 │ ZeroDivisionError: division by zero                                           │
 │                                                                               │
 │ A ZeroDivisionError occurs when you are attempting to divide a value by zero  │
 │ either directly or by using some other mathematical operation.                │
 │                                                                               │
 │ You are dividing by the following term                                        │
 │                                                                               │
 │  b                                                                            │
 │                                                                               │
 │ which is equal to zero.                                                       │
 │                                                                               │
 │ Execution stopped on line 7 of file 01_mydivide.py.                           │
 │                                                                               │
 │        4: if __name__ == '__main__':                                          │
 │        5:     data = [1,0,2,3]                                                │
 │        6:     for n in data:                                                  │
 │     -->7:         print(my_divide(1,n))                                       │
 │                         ^^^^^^^^^^^^^^                                        │
 │        8:     print('done.')                                                  │
 │                                                                               │
 │     my_divide:  <function my_divide>                                          │
 │     n:  0                                                                     │
 │     print:  <builtin function print>                                          │
 │                                                                               │
 │ Exception raised on line 2 of file 01_mydivide.py.                            │
 │                                                                               │
 │        1: def my_divide(a, b):                                                │
 │     -->2:     return a / b                                                    │
 │                      ^^^^^                                                    │
 │                                                                               │
 │     a:  1                                                                     │
 │     b:  0                                                                     │
 ╰───────────────────────────────────────────────────────────────────────────────╯
 
```


friendly には `what()` 、 `where()` 、 `why()` 、などの関数が提供されていて、どんな例外が、どこで、なぜ発生したのかを若干詳しく示してくれます。

friendly については次の資料を参照してくだい。

- [friendly tracebackモジュールを使ってみよう]

これではプログラムが異常終了してしまうため、 `except` で例外が捕獲してプログラム側で対処したものが次のコードです。


```
 In [2]: # %load 02_except.py
    ...: def my_divide(a, b):
    ...:     return a / b
    ...:
    ...: if __name__ == '__main__':
    ...:     data = [1,0,2,3]
    ...:     for n in data:
    ...:         try:
    ...:             print(my_divide(1,n))
    ...:         except ZeroDivisionError:
    ...:             print('ZeroDivisonError Occurs')
    ...:     print('done.')
    ...:
 1.0
 ZeroDivisonError Occurs
 0.5
 0.3333333333333333
 done.
 
 In [3]:
 
```

これでも問題ないといえばそうですが、もう少し詳しく情報を提示するようにしてみましょう。
こうしたときは、Python 標準ライブラリの [traceback ](https://docs.python.org/ja/3/library/traceback.html) を使うことができます。


```
 In [2]: # %load 03_traceback.py
    ...: def my_divide(a, b):
    ...:     return a / b
    ...:
    ...: if __name__ == '__main__':
    ...:     import traceback
    ...:     data = [1,0,2,3]
    ...:     for n in data:
    ...:         try:
    ...:             print(my_divide(1,n))
    ...:         except ZeroDivisionError:
    ...:             print(traceback.format_exc())
    ...:     print('done.')
    ...:
 1.0
 Traceback (most recent call last):
   File "<ipython-input-2-266d14cb72fb>", line 10, in <module>
     print(my_divide(1,n))
   File "<ipython-input-2-266d14cb72fb>", line 3, in my_divide
     return a / b
 ZeroDivisionError: division by zero
 
 0.5
 0.3333333333333333
 done.
 
 In [3]:
 
```


はじめの　 `01_mydivide.py` を実行したときと同じトレースバックが出力されました。ここで、注目してほしいことは、 `01_mydivide.py` のときはすべてのデータを処理できずに異常終了していましたが、traceback モジュールを使ってプログラマが処理することで最後まで処理できていることです。

logging などを用いてログに出力することができるわけです。

 pytohn
```
 In [2]: # %load 04_format_stack.py
    ...: def my_divide(a, b):
    ...:     return a / b
    ...:
    ...: if __name__ == '__main__':
    ...:     import traceback
    ...:     from pprint import pprint
    ...:     data = [1,0,2,3]
    ...:     for n in data:
    ...:         try:
    ...:             print(my_divide(1,n))
    ...:         except ZeroDivisionError:
    ...:             print('# --- format_stack()')
    ...:             pprint(traceback.format_stack())
    ...:             print('# --- extract_stack()')
    ...:             pprint(traceback.extract_stack())
    ...:             print('# --- print_stack()')
    ...:             pprint(traceback.print_stack())
    ...:     print('done.')
    ...:
 1.0
 # --- format_stack()
 ['  File "/Users/goichiiisaka/anaconda3/envs/tutorials/bin/ipython", line 8, '
  'in <module>\n'
  '    sys.exit(start_ipython())\n',
  '  File '
  '"/Users/goichiiisaka/anaconda3/envs/tutorials/lib/python3.9/site-packages/IPython/__init__.py", '
 (中略)
 # --- extract_stack()
 [<FrameSummary file /Users/goichiiisaka/anaconda3/envs/tutorials/bin/ipython, line 8 in <module>>,
  <FrameSummary file /Users/goichiiisaka/anaconda3/envs/tutorials/lib/python3.9/site-packages/IPython/__init__.py, line 126 in start_ipython>,
  (中略)
  # --- print_stack()
    File "/Users/goichiiisaka/anaconda3/envs/tutorials/bin/ipython", line 8, in <module>
      sys.exit(start_ipython())
    File "/Users/goichiiisaka/anaconda3/envs/tutorials/lib/python3.9/site-packages/IPython/__init__.py", line 126, in start_ipython
      return launch_new_instance(argv=argv, **kwargs)
    File "/Users/goichiiisaka/anaconda3/envs/tutorials/lib/python3.9/site-packages/traitlets/config/application.py", line 846, in launch_instance
      app.start()
  (中略)
    File "<ipython-input-2-c2cea1aeca79>", line 18, in <module>
      pprint(traceback.print_stack())
  None
  0.5
  0.3333333333333333
  done.
  
  In [3]:
```


### トレースバックをロギング
発生したれ以外をロギングする場合は、次のようにします。


```
 In [2]: # %load 08_logging_exception.py
    ...: def my_divide(a, b):
    ...:     return a / b
    ...:
    ...: if __name__ == '__main__':
    ...:     import traceback
    ...:     import logging
    ...:     LOG_FILENAME = 'logging_example.log'
    ...:     logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
    ...:
    ...:     data = [1,0,2,3]
    ...:     for n in data:
    ...:         try:
    ...:             print(my_divide(1,n))
    ...:         except ZeroDivisionError as e:
    ...:             logging.error(e, exc_info=True)
    ...:     print('done.')
    ...:
 1.0
 0.5
 0.3333333333333333
 done.
 
 In [3]: !cat logging_example.log
 ERROR:root:division by zero
 Traceback (most recent call last):
   File "<ipython-input-2-3c5adcedeb57>", line 14, in <module>
     print(my_divide(1,n))
   File "<ipython-input-2-3c5adcedeb57>", line 3, in my_divide
     return a / b
 ZeroDivisionError: division by zero
 
 In [4]:
 
```

実際のところ、機能的にはこれで必要十分なはずですから、ヘルパー関数やクラスはその存在を覚えてるだけでよいです。


### traceback のヘルパー関数

-  `traceback.print_tb(tb, limit = None, file = None) ` : limit が正であれば、トレースバックオブジェクト tb から limit までのスタックトレースエントリを出力します。そうでなければ、最後の  `abs(limit) ` エントリを出力します。limitが省略されたり、 `None` の場合は、すべてのエントリを出力する。 `file` が省略されたか  `None` の場合、出力は  `sys.stderr` に送られます。そうでない場合は、出力を受け取るためのオープンファイルまたはファイルライクオブジェクトでなければなりません。
-  `traceback.print_exception(etype, value, tb, limit = None, file = None, chain = True)` : トレースバックオブジェクト tb からの例外情報とスタックトレースエントリをファイルに出力します。 `tb` が `None` でない場合は、ヘッダを出力します 
-  `Traceback (most recent call last)` : . スタックトレースの後に、例外のタイプと値を出力します。 `type(value)` が `SyntaxError` で `value` が適切なフォーマットであれば、シンタックスエラーが発生した行を、エラーのおおよその位置を示すキャレットとともに出力します。
-  `traceback.print_exc(limit = None, file = None, chain = True)` : print_exception(*sys.ex_info(), limit, file, chain)の省略形です。
-  `traceback.print_last(limit = None, file = None, chain = True)` : 例外がインタラクティブなプロンプトに達した後にのみ動作します。これは print_exception(sys.last_type, sys.last_value, sys.last_traceback, limit, file, chain) の省略形です。
-  `traceback.print_stack(f = None, limit = None, file = None)` : limitが正であれば、limitまでのスタックトレースを出力します。そうでなければ、最後のabs(limit)エントリを出力します。limitが省略されたり、Noneの場合は、すべてのエントリを出力する。オプションの f 引数は、開始する別のスタックフレームを指定するために使用できます。
-  `traceback.extract_tb(tb, limit = None)` : トレースバックオブジェクトtbから抽出された「プリプロセスされた」スタックトレースエントリ（属性 `filename` ,  `lineno` ,  `name` ,  `line` を含む `FrameSummary` オブジェクト）のリストを表す `StackSummary` オブジェクトを返す。これは、スタックトレースの代替フォーマットに役立ちます。
-  `traceback.extract_stack(f = None, limit = None) ` : 現在のスタックフレームから生のトレースバックを抽出します。戻り値は extract_tb() と同じフォーマットです。
-  `traceback.format_list(extracted_list)` : タプルまたは `FrameSummary` オブジェクトのリストが与えられた場合、印刷に適した文字列のリストを返します。抽出されたリストの各文字列は、引数リストの同じインデックスを持つ項目に対応します。各文字列は、改行で終わります。文字列は、内部の改行も含むことができます。
-  `traceback.format_exception_only(etype, value)` : トレースバックの例外部分をフォーマットします。引数は、例外のタイプと値（ `sys.last_type` と `sys.last_value` で与えられるもの）です。これは、それぞれが新しい行で終わる文字列のリストを返します。
-  `traceback.format_exception(etype, value, tb, limit = None, chain = True) ` : スタックトレースと例外情報をフォーマットします。引数は、 `print_exception()` の引数と同じ意味です。この関数は、それぞれが改行で終わる文字列のリストを返し、中には内部に改行があるものもあります。これらの行を連結して印刷すると、 `print_exception()` と全く同じ出力が得られます。
-  `traceback.format_exc(limit = None, chain = True)` :  `print_exc(limit)` と似ていますが、ファイルに出力するのではなく文字列を返します。
-  `traceback.format_tb(tb, limit = None) ` :  `format_list(extract_tb(tb, limit))` の省略形です。
-  `traceback.format_stack(f = None, limit = None)` :  `format_list(extract_stack(f, limit))` の省略形です。
-  `traceback.clear_frames(tb)` : 各フレームオブジェクトの `clear()` メソッドを呼び出して、トレースバックtb内のすべてのスタックフレームのローカル変数をクリアします。
- `traceback.walk_stack(f)  `: 与えられたフレームから` f.f_back` を辿ってスタックを歩き、各フレームのフレーム番号と行番号を得る。 `f` が  `None` の場合は、現在のスタックが使用されます。このヘルパーは `StackSummary.extract()` と一緒に使われます。
-  `traceback.walk_tb(tb)` :  `tb_next` に続いてトレースバックを歩き、各フレームのフレームと行番号を得る。このヘルパーは  `StackSummary.extract()` と一緒に使われます。 


#### TracebackExceptionクラス

 `TracebackException` クラスには、以下のオブジェクトが含まれています。

-  `__cause__` : オリジナルの `__cause__` の `TracebackException` です。
-  `__context__` : オリジナルの `__context__` の `TracebackException` です。
-  `_suppress_context__` : 元の例外の `_suppress_context__` の値。
-  `stack` : トレースバックを表す `StackSummary` 
-  `exc_type` : 元のトレースバックのクラス。
-  `filename` : 構文エラーの場合、エラーが発生したファイル名。
-  `lineno` : シンタックスエラーの場合、エラーが発生した行番号。
-  `text` : 構文エラーの場合、エラーが発生したテキストです。
-  `offset` : シンタックスエラーの場合、エラーが発生したテキストのオフセットです。
-  `msg` : シンタックスエラーの場合 - コンパイラのエラーメッセージです。
-  `classmethod from_exception(exc, *, limit = None, lookup_lines = True, capture_locals = False)` : 後でレンダリングするために例外をキャプチャします。
-  `format(*, chain=True)` : 例外をフォーマットします。 `chain` が `True` でない場合、 `__cause__` と `__context__` はフォーマットされません。この関数は、それぞれが改行で終わる文字列を返しますが、中には内部改行を含むものもあります。どの例外が発生したかを示すメッセージは、常に出力の最後の文字列となります。
-  `format_exception_only() ` : トレースバックの例外部分をフォーマットします。また、改行の終わった文字列を返します。通常、ジェネレーターは単一の文字列を出力しますが、 `SyntaxError` 例外の場合は、複数の行を出力し、（印刷すると）構文エラーが発生した場所に関する詳細な情報を出力します。どの例外が発生したかを示すメッセージは、常に出力の最後の文字列となります。


```
 In [2]: # %load 05_format_execption_only.py
    ...: def my_divide(a, b):
    ...:     return a / b
    ...:
    ...: if __name__ == '__main__':
    ...:     import sys
    ...:     from traceback import TracebackException
    ...:     data = [1,0,2,3]
    ...:     for n in data:
    ...:         try:
    ...:             print(my_divide(1,n))
    ...:         except ZeroDivisionError:
    ...:             exc_type, exc_value, exc_tb = sys.exc_info()
    ...:             tb = TracebackException(exc_type, exc_value, exc_tb)
    ...:             print(''.join(tb.format_exception_only()))
    ...:     print('done.')
    ...:
 1.0
 ZeroDivisionError: division by zero
 
 0.5
 0.3333333333333333
 done.
 
 In [3]:
```


#### StackSummaryクラス
 `StackSummary` クラスののオブジェクトは、フォーマットに対応したコールスタックを表しています。

-  `classmethod extract(frame_gen, *, limit = None, lookup_lines = True, capture_locals = False)` : フレームジェネレータから `StackSummary` オブジェクトを生成します。 `lookup_lines` がFalseの場合、返された `FrameSummary` オブジェクトはまだラインを読み込んでいないので、 `StackSummary` を作成するコストが安くなります。 `capture_locals` が `True` の場合は、各 `FrameSummary` のローカル変数がオブジェクトの表現としてキャプチャされます。
-  `classmethod from_list(a_list) ` : 与えられた `FrameSummary` オブジェクトのリスト、または旧式のタプルのリストから `StackSummary` オブジェクトを構築します。
-  `format() ` : 印刷に適した文字列のリストを返します。結果として得られるリストの各文字列は、スタックからの1つのフレームに対応します。各文字列は、改行で終わります。文字列には、内部の改行も含まれます。同じフレームと行の長いシーケンスの場合、最初の数回の繰り返しが出力され、その後、さらに繰り返しの正確な数を示す要約行が続きます。しかし、新しいバージョンでは、繰り返されるフレームの長いシーケンスは省略されます。


```
 In [2]: # %load 06_stacksummary.py
    ...: def my_divide(a, b):
    ...:     return a / b
    ...:
    ...: if __name__ == '__main__':
    ...:     import sys
    ...:     from traceback import StackSummary, walk_stack
    ...:     data = [1,0,2,3]
    ...:     for n in data:
    ...:         try:
    ...:             print(my_divide(1,n))
    ...:         except ZeroDivisionError:
    ...:             summary = StackSummary.extract(walk_stack(None))
    ...:             print(''.join(summary.format()))
    ...:     print('done.')
    ...:
 1.0
   File "<ipython-input-2-92a0d0edd298>", line 13, in <module>
     summary = StackSummary.extract(walk_stack(None))
   File "/Users/goichiiisaka/anaconda3/envs/tutorials/lib/python3.9/site-packages/IPython/core/interactiveshell.py", line 3444, in run_code
     exec(code_obj, self.user_global_ns, self.user_ns)
   File "/Users/goichiiisaka/anaconda3/envs/tutorials/lib/python3.9/site-
```
　(中略)
    - File "/Users/goichiiisaka/anaconda3/envs/tutorials/bin/ipython", line 8, in <module>
        - sys.exit(start_ipython())
 
- 0.5
- 0.3333333333333333
- done.
 
- In [3]:


#### FrameSummaryクラス
 `FrameSummary` クラスのオブジェクトは、トレースバックの1つのフレームを表します。


```
 In [2]: # %load 07_frame_summary.py
    ...: def my_divide(a, b):
    ...:     return a / b
    ...:
    ...: if __name__ == '__main__':
    ...:     import sys
    ...:     from traceback import StackSummary, walk_stack
    ...:     template = (
    ...:         '{frame.filename}:{frame.lineno}:{frame.name}:\n'
    ...:         '    {frame.line}'
    ...:     )
    ...:     data = [1,0,2,3]
    ...:     for n in data:
    ...:         try:
    ...:             print(my_divide(1,n))
    ...:         except ZeroDivisionError:
    ...:             summary = StackSummary.extract(walk_stack(None))
    ...:             for frame in summary:
    ...:                 print(template.format(frame=frame))
    ...:     print('done.')
    ...:
 1.0
 <ipython-input-2-b8c6392c077d>:17:<module>:
     summary = StackSummary.extract(walk_stack(None))
 /Users/goichiiisaka/anaconda3/envs/tutorials/lib/python3.9/site-packages/IPython/core/interactiveshell.py:3444:run_code:
     exec(code_obj, self.user_global_ns, self.user_ns)
 (中略)
  /Users/goichiiisaka/anaconda3/envs/tutorials/bin/ipython:8:<module>:
     sys.exit(start_ipython())
 0.5
 0.3333333333333333
 done.
 
 In [3]:
 
```



