Inspectモジュールを使ってみよう
=================

## inspectモジュールについて
Python 標準ライブラリの inspect モジュールを利用すると実行中のコードやオブジェクトの情報を取得することができます。
これは、**イントロスペクション(introspection)** と言われるもので実行状況の確認を行うときに重要になります。
言葉の意味としては「内省（自らを省みる）」ということなのですが、日常的に使われる言葉でもなく、うまい日本語訳がないためか単にイントロスペクションと言われることが多いです。


### __file__ 
Pythonでの  `__file__` は、直接 inspect とは関係しないのですが注意が必要なものなので説明しておきます。
これは、スクリプト中ではコードが記述されているファイルのパスが格納されます。

- PATHを検索して実行された場合：絶対パス 
- 絶対パス指定で実行した場合：絶対パス
- 相対パス指定で実行した場合：相対パス

ただし、Pythonを対話型に実行しているときはこれが失敗します。


```
 In [2]: # %load 01_file.py
    ...: print(__file__)
    ...:
 ---------------------------------------------------------------------------
 NameError                                 Traceback (most recent call last)
 <ipython-input-2-00f266d7a3d2> in <module>
       1 # %load 00_file.py
 ----> 2 print(__file__)
 
 NameError: name '__file__' is not defined
 
 In [3]: %run 00_file.py
 /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/02_Inspect/00_file.py
 
 In [4]:
```

対話型に実行されているためファイルを実行していないので当然です。
このためロギングで実行中のファイル名を記録するためには使用しない方が望ましいです。

inspect を使うことでこの対話型に実行された場合でも、とりあえず文字列を返すことはできます。


```
 In [2]: # %load 02_file_ok.py
    ...: import inspect
    ...:
    ...: filepath = inspect.getfile(lambda: None)
    ...: print(filepath)
    ...:
 <ipython-input-2-0d02c5117669>
 
 In [3]: %run 02_file_ok.py
 /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/02_Inspect/02_file_ok.py
 
 In [4]:
```


### getsource()
getsource は引数に与えたオブジェクトのソースコードを取得します。

 ackermann.py
```
 import sys
 sys.setrecursionlimit(100000)
 
 def ackermann(m, n):
     if m == 0:
         return n + 1
     if n == 0:
         return ackermann(m - 1, 1)
     return ackermann(m - 1, ackermann(m, n - 1))
   
```


```
 In [2]: # %load 01_getsource.py
    ...: import inspect
    ...: from ackermann import ackermann
    ...:
    ...: _ = ackermann(3, 10)
    ...:
    ...: src = inspect.getsource(ackermann)
    ...: print(src)
    ...:
 def ackermann(m, n):
     if m == 0:
         return n + 1
     if n == 0:
         return ackermann(m - 1, 1)
     return ackermann(m - 1, ackermann(m, n - 1))
 
 
 In [3]:
```

デバッグ中などでソースコードを参照したいときに便利です。

### currentframe()
実行中のコードのトレースバックオブジェクトの情報を参照する


```
 In [2]: # %load 02_currentframe.py
    ...: import inspect
    ...:
    ...: def my_function():
    ...:     frame = inspect.currentframe()
    ...:     return inspect.getframeinfo(frame)
    ...:
    ...: f = my_function()
    ...: print(f'filename={f.filename}')
    ...: print(f'lineno={f.lineno}')
    ...: print(f'function={f.function}')
    ...: print(f'code_context={f.code_context}')
    ...: print(f'index={f.index}')
    ...:
 filename=<ipython-input-2-ee00dd1d2964>
 lineno=6
 function=my_function
 code_context=['    return inspect.getframeinfo(frame)\n']
 index=0
 
 In [3]:
 
```

トレースバックで詳細な情報を取得


```
 inspect.stack(context)[frame][content]
```

context は、コンテキストとして取得する前後の総行数を指定します。以下の例では1なので1行のみを取得します。frame は、呼び出し元が最初の要素に入り、末尾が最も外側になります。以下の例では、get_inspect_stack が 0、get_inspect_stack を呼び出した場所のフレーム情報が 1、get_inspect_stack を呼び出した場所を含む関数を呼び出した場所のフレーム情報が 2 になります。content を指定することで、次のの6つの情報のどれかを取得できます。

- フレームオブジェクト
- ファイル名
- 実行中の行番号
- 実行中の関数名
- コンテキストのソースリスト、
- ソースリストの中でのの実行中の行


```
 In [2]: # %load 05_stack.py
    ...: import inspect
    ...:
    ...: def my_function():
    ...:     filename = inspect.stack()[1][1]
    ...:     line = inspect.stack()[1][2]
    ...:     method = inspect.stack()[1][3]
    ...:
    ...:     print(f'Method not implemented: {method} at line: {line} of {filenam
    ...: e}')
    ...:
    ...: _ = my_function()
    ...:
 Method not implemented: <module> at line: 11 of <ipython-input-2-1fb5be573ff5>
 
 In [3]:
 
```

### getclosurevars()


```
 In [2]: # %load 06_getclosurevars.py
    ...: import inspect
    ...:
    ...: def stock():
    ...:     eqty  = 0
    ...:
    ...:     def buy(price, log):
    ...:         return price * log
    ...:     return buy
    ...:
    ...: print(inspect.getclosurevars(stock))
    ...:
 ClosureVars(nonlocals={}, globals={}, builtins={}, unbound=set())
 
 In [3]:
 
```



```
 In [2]: # %load 07_logging_with_inspect.py
    ...: import inspect
    ...: import logging
    ...: from models import User
    ...: from pprint import pprint, pformat
    ...:
    ...: stack_content = [
    ...:     'frame obj  ',
    ...:     'file name  ',
    ...:     'line num   ',
    ...:     'function   ',
    ...:     'context    ',
    ...:     'index      ',
    ...:     ]
    ...:
    ...: LOG_FILENAME = 'logging_example.log'
    ...: logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
    ...: log = logging.getLogger("__name__")
    ...:
    ...: def get_inspect_stack():
    ...:     context, frame = 1, 2
    ...:     return dict(zip(stack_content, inspect.stack(context)[frame]))
    ...:
    ...: def outer_func():
    ...:     log.debug(pformat(get_inspect_stack()))
    ...:     def inner_func():
    ...:         log.debug("Current line  : %s", inspect.currentframe().f_lineno)
    ...:
    ...:         log.debug(pformat(get_inspect_stack()))
    ...:         log.debug("Caller's line : %s", inspect.currentframe().f_back.f_
    ...: lineno)
    ...:         def inner_inner_func():
    ...:             log.debug(pformat(get_inspect_stack()))
    ...:         inner_inner_func()
    ...:     inner_func()
    ...:
    ...: def main():
    ...:     user = User(first_name='David', last_name='Coverdale')
    ...:     outer_func()
    ...:
    ...: if __name__ == '__main__':
    ...:     main()
    ...:
 
 In [3]: !cat logging_example.log
 DEBUG:__name__:{'context    ': ['    outer_func()\n'],
  'file name  ': '<ipython-input-2-47522eca1617>',
  'frame obj  ': <frame at 0x10f9a0550, file '<ipython-input-2-47522eca1617>', line 37, code main>,
  'function   ': 'main',
  'index      ': 0,
  'line num   ': 37}
 DEBUG:__name__:Current line  : 27
 DEBUG:__name__:{'context    ': ['    inner_func()\n'],
  'file name  ': '<ipython-input-2-47522eca1617>',
  'frame obj  ': <frame at 0x10f9a4640, file '<ipython-input-2-47522eca1617>', line 33, code outer_func>,
  'function   ': 'outer_func',
  'index      ': 0,
  'line num   ': 33}
 DEBUG:__name__:Caller's line : 33
 DEBUG:__name__:{'context    ': ['        inner_inner_func()\n'],
  'file name  ': '<ipython-input-2-47522eca1617>',
  'frame obj  ': <frame at 0x1107d0550, file '<ipython-input-2-47522eca1617>', line 32, code inner_func>,
  'function   ': 'inner_func',
  'index      ': 0,
  'line num   ': 32}
 
 In [4]:
 
```



