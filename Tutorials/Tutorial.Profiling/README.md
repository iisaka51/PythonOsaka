Python チュートリアル：プロファイリングツール
=================

![](https://gyazo.com/153a339305d78fc4fa4850753e4b1594.png)


## プロファイリング
プログラムを高速化/並列化を行うためには、プログラム内のホットスポットを見つけることが、最初のステップです。 これを**プロファイリング (profiling) **といます。プロファイリングでは、プログラムの各部分がどれだけ頻繁に呼ばれたか、そして実行にどれだけ時間がかかったかという統計情報を収集します。 重要な点は、実際には遅い関数または広範囲に呼び出される関数のみを最適化することです。 プロファイラーは、処理時間、関数呼び出し、中断、キャッシュ障害など、いくつかのタイプの情報を収集することができます。

プロファイリングには2つのタイプがあります。

- **決定論的プロファイリング**：すべてのイベントが監視されます。 正確な情報を提供しますが、オーバーヘッドはパフォーマンスに大きな影響を与えます。 つまり、プロファイリングの下でコードの実行が遅くなります。 運用中のシステムでの使用は、多くの場合非現実的です。 このタイプのプロファイリングは、小さな関数に適しています。
- **統計プロファイリング**：インジケーターを計算するために定期的に実行状態をサンプリングします。 この方法は精度が低くなりますが、オーバーヘッドも削減されます。


## time
Python標準ライブラリの time モジュールを使って２点間での時間を調べることで性能評価の指針にすることができます。

例え次の関数は、[アッカーマン関数 ](https://ja.wikipedia.org/wiki/アッカーマン関数) と呼ばれるもので、与える数が大きくなると爆発的に計算量が大きくなるという特徴を持っています。この関数を使って説明してみましょう。


```
 In [2]: # %load 01_ackermann.py
    ...: import sys
    ...: sys.setrecursionlimit(100000)
    ...:
    ...: def ackermann(m, n):
    ...:     if m == 0:
    ...:         return n + 1
    ...:     if n == 0:
    ...:         return　ackermann(m - 1, 1)
    ...:     return ackermann(m - 1, ackermann(m, n - 1))
    ...:
    ...: if __name__ == '__main__':
    ...:     a = ackermann(3, 10)
    ...:     print(a)
    ...:
 8189
 
```

これだけではどれだけ時間がかっかたかを定量的に知ることができません。
そこで、次のようにコードを追加します。


```
 In [2]: # %load 02_ackermann_time.py
    ...: import time
    ...: import sys
    ...: sys.setrecursionlimit(100000)
    ...:
    ...: def ackermann(m, n):
    ...:     if m == 0:
    ...:         return n + 1
    ...:     if n == 0:
    ...:         return ackermann(m - 1, 1)
    ...:     return ackermann(m - 1, ackermann(m, n - 1))
    ...:
    ...: if __name__ == '__main__':
    ...:     t1 = time.time()
    ...:     a = ackermann(3, 10)
    ...:     calc_time = time.time() - t1
    ...:     print(f'{a}: {calc_time:.2f}sec')
    ...:
 8189: 17.90sec
 
 In [3]:
 
```

時間計測したい処理を  `time.time()` で挟んで、その時間差を調べるわけです。

 `time.time()` の代わりに　`次の関数も使用することもできます。


-  `time()` ：エポック からの秒数を浮動小数点数で返します。 
-  `time_ns()` ： `time()` に似ていますが、ナノ秒単位の時刻を返します。
-  `perf_counter()` ：パフォーマンスカウンターの値 (小数点以下がミリ秒) を返します。クロックは短期間の計測が行えるよう、可能な限り高い分解能をもちます。これにはスリープ中の経過時間も含まれます。
-  `perf_counte_ns()` ： `perf_counter()` に似ていますが、ナノ秒単位の時刻を返します。
-  `process_time()` ：現在のプロセスのシステムおよびユーザー CPU 時間の合計値 (小数点以下はミリ秒) を返します。プロセスごとに定義され、スリープ中の経過時間は含まれません。
-  `process_time_ns()` ： `process_time()` に似ていますが、ナノ秒単位の時刻を返します。
-  `thread_time()` ：現在のスレッドのシステムおよびユーザーの CPU 時間の合計値 (小数点以下ありの秒数) を返します。 スリープ中の経過時間は含まれません。 
-  `thread_time_ns()` ： `thread_time()` に似ていますが、ナノ秒単位の時刻を返します。


```
 In [2]: # %load 03_ackermann_perfcounter.py
    ...: import time
    ...: import sys
    ...: sys.setrecursionlimit(100000)
    ...:
    ...: def ackermann(m, n):
    ...:     if m == 0:
    ...:         return n + 1
    ...:     if n == 0:
    ...:         return ackermann(m - 1, 1)
    ...:     return ackermann(m - 1, ackermann(m, n - 1))
    ...:
    ...: if __name__ == '__main__':
    ...:     t1 = time.perf_counter()
    ...:     a = ackermann(3, 10)
    ...:     calc_time = time.perf_counter() - t1
    ...:     print(f'{a}: {calc_time:.2f}sec')
    ...:
 8189: 18.50sec
 
 In [3]:
 
```

性能評価をしたい２点にコードを挿入することになりますが、
調べる箇所が多い場合ときなどでは、次のようなモジュールにしておくと便利です。

 perftest.py
```
 import time
 from contextlib import contextmanager
 
 @contextmanager
 def perftest():
     t = time.perf_counter()
     yield None
     perf_time = time.perf_counter() - t
     print(f'Elapsed: {perf_time:.4f}sec')
     
```


```
 In [2]: # %load 04_ackermann_contextmanager.py
    ...: from perftest import perftest
    ...: import sys
    ...: sys.setrecursionlimit(100000)
    ...:
    ...: def ackermann(m, n):
    ...:     if m == 0:
    ...:         return n + 1
    ...:     if n == 0:
    ...:         return ackermann(m - 1, 1)
    ...:     return ackermann(m - 1, ackermann(m, n - 1))
    ...:
    ...: if __name__ == '__main__':
    ...:     with perftest():
    ...:         a = ackermann(3, 10)
    ...:         print(a)
    ...:
 8189
 Elapsed: 24.9091sec
 
 In [3]:
```


## timeit
Python 標準ライブラリの timeit モジュールは、Python コードをの時間を計測するシンプルな手段を提供しています。
 `time` との違いは２点間でのカウンターの差異を調べるのではなくて、調べたいPython式を引数で与えることです。
次の例は、test_code に文字列で定義した python式を、100回繰り返して性能評価を行うものです。


```
 In [2]: # %load 01_timeit.py
    ...: from timeit import timeit
    ...:
    ...: test_code = '"-".join(str(n) for n in range(1000))'
    ...: test = timeit(test_code, number=100)
    ...:
    ...: print(f'{test}')
    ...:
 0.03832157200000008
 
 In [3]:
```

 `number` のデフォルト値は 100万回です

前述の例のように定義済みの関数の性能評価をする場合は、その関数をインポートするようにします。


```
 In [2]: # %load 02_ackermann.py
    ...: import sys
    ...: sys.setrecursionlimit(100000)
    ...:
    ...: def ackermann(m, n):
    ...:     if m == 0:
    ...:         return n + 1
    ...:     if n == 0:
    ...:         return ackermann(m - 1, 1)
    ...:     return ackermann(m - 1, ackermann(m, n - 1))
    ...:
    ...: if __name__ == '__main__':
    ...:     import  timeit
    ...:     t = timeit.timeit('ackermann(3, 10)',
    ...:                       'from __main__ import ackermann',
    ...:                       number=1)
    ...:     print(f'Elapsed: {t}sec')
    ...:
 Elapsed: 19.784244177sec
 
 In [3]:
```

使用する関数が複数あるような場合は、次のようにする方が簡単です。


```
 In [2]: # %load 03_ackermann_globals.py
    ...: import sys
    ...: sys.setrecursionlimit(100000)
    ...:
    ...: def ackermann(m, n):
    ...:     if m == 0:
    ...:         return n + 1
    ...:     if n == 0:
    ...:         return ackermann(m - 1, 1)
    ...:     return ackermann(m - 1, ackermann(m, n - 1))
    ...:
    ...: if __name__ == '__main__':
    ...:     import  timeit
    ...:     t = timeit.timeit('ackermann(3, 10)',
    ...:                       globals=globals(),
    ...:                       number=1)
    ...:     print(f'Elapsed: {t}sec')
    ...:
 Elapsed: 18.961754934sec
 
 In [3]:
 
```

timeiut は次のようにコマンドラインツールとしても理療することができます。

 bash
```
 $ python3 -m timeit '"-".join(str(n) for n in range(100))'
 10000 loops, best of 5: 31.7 usec per loop
 
 $ python3 -m timeit '"-".join([str(n) for n in range(100)])'
 10000 loops, best of 5: 35.2 usec per loop
 
 $ python3 -m timeit '"-".join(map(str, range(100)))'
 10000 loops, best of 5: 26.9 usec per loop
 
```

## cProfile
[cProfile ](https://docs.python.org/ja/3/library/profile.html)は、Python 標準ライブラリで使用できるプロファイラー。C言語で書かれた拡張モジュールで、オーバーヘッドが少ないため長時間実行されるプログラムのプロファイルに適しています。プラットフォームによってはcProfileが使用できない場合は、Pythonで実装されたprofile を使用してください。
大まかにどの関数がホットポットになっているかを調べるときに便利です。

### 使用方法

1つの引数を取る関数をプロファイルしたい場合、次のようにします。

```
 In [2]: # %load 01_intro.py
    ...: import cProfile
    ...: import re
    ...:
    ...: cProfile.run('re.compile("foo|bar")')
    ...:
          216 function calls (209 primitive calls) in 0.000 seconds
 
    Ordered by: standard name
 
    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
         1    0.000    0.000    0.000    0.000 <string>:1(<module>)
         2    0.000    0.000    0.000    0.000 enum.py:358(__call__)
         2    0.000    0.000    0.000    0.000 enum.py:670(__new__)
         1    0.000    0.000    0.000    0.000 enum.py:977(__and__)
         1    0.000    0.000    0.000    0.000 re.py:250(compile)
         1    0.000    0.000    0.000    0.000 re.py:289(_compile)
         1    0.000    0.000    0.000    0.000 sre_compile.py:249(_compile_charset)
         1    0.000    0.000    0.000    0.000 sre_compile.py:276(_optimize_charset)
         2    0.000    0.000    0.000    0.000 sre_compile.py:453(_get_iscased)
         1    0.000    0.000    0.000    0.000 sre_compile.py:461(_get_literal_prefix)
         1    0.000    0.000    0.000    0.000 sre_compile.py:492(_get_charset_prefix)
         1    0.000    0.000    0.000    0.000 sre_compile.py:536(_compile_info)
         2    0.000    0.000    0.000    0.000 sre_compile.py:595(isstring)
         1    0.000    0.000    0.000    0.000 sre_compile.py:598(_code)
       3/1    0.000    0.000    0.000    0.000 sre_compile.py:71(_compile)
         1    0.000    0.000    0.000    0.000 sre_compile.py:759(compile)
         3    0.000    0.000    0.000    0.000 sre_parse.py:111(__init__)
         7    0.000    0.000    0.000    0.000 sre_parse.py:160(__len__)
        18    0.000    0.000    0.000    0.000 sre_parse.py:164(__getitem__)
         7    0.000    0.000    0.000    0.000 sre_parse.py:172(append)
       3/1    0.000    0.000    0.000    0.000 sre_parse.py:174(getwidth)
         1    0.000    0.000    0.000    0.000 sre_parse.py:224(__init__)
         8    0.000    0.000    0.000    0.000 sre_parse.py:233(__next)
         2    0.000    0.000    0.000    0.000 sre_parse.py:249(match)
         6    0.000    0.000    0.000    0.000 sre_parse.py:254(get)
         1    0.000    0.000    0.000    0.000 sre_parse.py:286(tell)
         1    0.000    0.000    0.000    0.000 sre_parse.py:435(_parse_sub)
         2    0.000    0.000    0.000    0.000 sre_parse.py:493(_parse)
         1    0.000    0.000    0.000    0.000 sre_parse.py:76(__init__)
         2    0.000    0.000    0.000    0.000 sre_parse.py:81(groups)
         1    0.000    0.000    0.000    0.000 sre_parse.py:921(fix_flags)
         1    0.000    0.000    0.000    0.000 sre_parse.py:937(parse)
         1    0.000    0.000    0.000    0.000 {built-in method _sre.compile}
         1    0.000    0.000    0.000    0.000 {built-in method builtins.exec}
        25    0.000    0.000    0.000    0.000 {built-in method builtins.isinstance}
         1    0.000    0.000    0.000    0.000 {built-in method builtins.iter}
     29/26    0.000    0.000    0.000    0.000 {built-in method builtins.len}
         2    0.000    0.000    0.000    0.000 {built-in method builtins.max}
         9    0.000    0.000    0.000    0.000 {built-in method builtins.min}
         1    0.000    0.000    0.000    0.000 {built-in method builtins.next}
         6    0.000    0.000    0.000    0.000 {built-in method builtins.ord}
        48    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
         5    0.000    0.000    0.000    0.000 {method 'find' of 'bytearray' objects}
         1    0.000    0.000    0.000    0.000 {method 'items' of 'dict' objects}
 
 
 
 In [3]:
 
```

最初の行は 216回の呼び出しを測定したことを示しています。その中で 209回は プリミティブ です。すなわち再帰呼び出しではないことを表しています。次の行の  `Ordered by: standard name` は一番右の列の文字列が出力のソートに用いられたことを示します。
フィールドの見出しは以下を含みます:

- **ncalls**: 呼び出し回数
- **tottime**:与えられた関数に消費された合計時間 
  - sub-function の呼び出しで消費された時間は除外されている
- **percall**: tottime を ncalls で割った値
- **cumtime**: この関数と全ての subfunction に消費された累積時間 (起動から終了まで)。
  - この数字は再帰関数についても正確です。
- **percall**: cumtime をプリミティブな呼び出し回数で割った値
- **filename:lineno(function)**: その関数のファイル名、行番号、関数名

最初の行に 2 つの数字がある場合 (たとえば 3/1) は、関数が再帰的に呼び出されたということです。2 つ目の数字はプリミティブな呼び出しの回数で、1 つ目の数字は総呼び出し回数です。関数が再帰的に呼び出されなかった場合、それらは同じ値で数字は 1 つしか表示されないことに留意してください。

 `run()` 関数に `filename=` 引数にファイル名を指定することで、プロファイル実行の終了時に出力を表示する代わりに、指定したファイルにデータを保存することが出来ます。

 pytohn
```
 In [2]: # %load 02_save_to_file.py
    ...: import cProfile
    ...: import re
    ...:
    ...: cProfile.run('re.compile("foo|bar")', filename='re_test.log')
    ...:
 
 In [3]: !file re_test.log
 re_test.log: data
 
 In [4]:
```

pstats モジュールは、このファイルからプロファイルの結果を読み込んで様々な書式に整えることができます。

ファイルcProfileおよびprofileは、別のスクリプトをプロファイルするためのスクリプトとして呼び出すこともできます。 


 bash
```
 $ python -m cProfile [-o output_file] [-s sort_order] (-m module | myscript.py)
```

-  `-o` はプロファイルの結果を標準出力の代わりにファイルに書き出す
-  `-s` は出力を sort_stats() で出力をソートする値を指定します。-o がない場合に有効
-  `-m` スクリプトの代わりにモジュールがプロファイリングされることを指定.

 bash
```
 % python -m cProfile -m re 02_save_to_file.py
          821 function calls (818 primitive calls) in 0.001 seconds
 
    Ordered by: standard name
 
    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:231(_verbose_message)
         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:385(cached)
         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap>:398(parent)
         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1031(get_filename)
         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1036(get_data)
         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:1077(path_stats)
         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:121(_path_join)
         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:123(<listcomp>)
         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:127(_path_split)
         2    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:129(<genexpr>)
         1    0.000    0.000    0.000    0.000 <frozen importlib._bootstrap_external>:135(_path_stat)
 (以下略)
```

[pstats ](https://docs.python.org/ja/3/library/profile.html#module-pstats) モジュールの Stats クラスにはプロファイル結果のファイルに保存されているデータを処理して出力するための様々なメソッドがあります。


```
 In [2]: # %load 03_pstats.py
    ...: import pstats
    ...: from pstats import SortKey
    ...:
    ...: p = pstats.Stats('re_test.log')
    ...: t = p.strip_dirs().sort_stats(-1).print_stats()
    ...:
 Mon Oct 18 09:55:36 2021    re_test.log
 
          3 function calls in 0.000 seconds
 
    Ordered by: standard name
 
    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
         1    0.000    0.000    0.000    0.000 <string>:1(<module>)
         1    0.000    0.000    0.000    0.000 {built-in method builtins.exec}
         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
 
 
 
 In [3]:
```

 `strip_dirs()` メソッドによって全モジュール名から無関係なパスが取り除かれました。 `sort_stats()` メソッドにより、出力される標準的な モジュール/行/名前 文字列にしたがって全項目がソートされました。 `print_stats()` メソッドによって全統計が出力されました。以下のようなソート呼び出しを試すことができます:


```
 In [2]: # %load 04_sort_funcname.ppy
    ...: import pstats
    ...: from pstats import SortKey
    ...:
    ...: p = pstats.Stats('re_test.log')
    ...: t1 = p.sort_stats(SortKey.NAME)
    ...: t2 = p.print_stats()
    ...:
 Mon Oct 18 09:55:36 2021    re_test.log
 
          3 function calls in 0.000 seconds
 
    Ordered by: function name
 
    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
         1    0.000    0.000    0.000    0.000 {built-in method builtins.exec}
         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
         1    0.000    0.000    0.000    0.000 <string>:1(<module>)
 
 
 
 In [3]:
 
```

最初の行ではリストを関数名でソートしています。2行目で情報を出力しています。


```
 In [2]: # %load 05_sort_cumulative.py
    ...: import pstats
    ...: from pstats import SortKey
    ...:
    ...: p = pstats.Stats('re_test.log')
    ...: t1 = p.sort_stats(SortKey.CUMULATIVE).print_stats(10)
    ...:
 Mon Oct 18 09:55:36 2021    re_test.log
 
          3 function calls in 0.000 seconds
 
    Ordered by: cumulative time
 
    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
         1    0.000    0.000    0.000    0.000 {built-in method builtins.exec}
         1    0.000    0.000    0.000    0.000 <string>:1(<module>)
         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
 
 
 
 In [3]:
 
```

このようにすると、関数が消費した累計時間でソートして、さらにその上位10件だけを表示します。どのアルゴリズムが時間を多く消費しているのか知りたいときは、この方法が役に立つはずです。

ループで多くの時間を消費している関数はどれか調べたいときは、次のようにします:


```
 In [2]: # %load 06_detect_loop.py
    ...: import pstats
    ...: from pstats import SortKey
    ...:
    ...: p = pstats.Stats('re_test.log')
    ...: t1 = p.sort_stats(SortKey.TIME).print_stats(10)
    ...:
 Mon Oct 18 09:55:36 2021    re_test.log
 
          3 function calls in 0.000 seconds
 
    Ordered by: internal time
 
    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
         1    0.000    0.000    0.000    0.000 {built-in method builtins.exec}
         1    0.000    0.000    0.000    0.000 <string>:1(<module>)
         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
 
 
 
 In [3]:
 
```

上記はそれぞれの関数で消費された時間でソートして、上位10件の関数の情報が表示されます。


```
 In [2]: # %load 07_sort_filename.py
    ...: import pstats
    ...: from pstats import SortKey
    ...:
    ...: p = pstats.Stats('re_test.log')
    ...: t1 = p.sort_stats(SortKey.FILENAME).print_stats('__init__')
    ...:
 Mon Oct 18 09:55:36 2021    re_test.log
 
          3 function calls in 0.000 seconds
 
 
 In [3]:
 
```

これは、ファイル名でソートされ、そのうちクラスの初期化メソッド (メソッド名 __init__) に関する統計情報だけが表示されます:


```
 In [2]: # %load 08_sort_time.py
    ...: import pstats
    ...: from pstats import SortKey
    ...:
    ...: p = pstats.Stats('re_test.log')
    ...: t1 = ( p.sort_stats(SortKey.TIME, SortKey.CUMULATIVE)
    ...:         .print_stats(.5, 'init'))
    ...:
 Mon Oct 18 09:55:36 2021    re_test.log
 
          3 function calls in 0.000 seconds
 
 
 In [3]:
 
```

上記は時間 (time) をプライマリキー、累計時間 (cumulative time) をセカンダリキーにしてソートした後でさらに条件を絞って統計情報を出力します。 .5 は上位 50% だけを選択することを意味し、さらにその中から文字列 init を含むものだけが表示されます。

どの関数がどの関数を呼び出しているのかを知りたければ、次のようにします (p は最後に実行したときの状態でソートされています):


```
 In [2]: # %load 09_function_tree.py
    ...: import pstats
    ...: from pstats import SortKey
    ...:
    ...: p = pstats.Stats('re_test.log')
    ...: t1 = p.print_callers(.5, 'init').print_stats(10)
    ...:
 Mon Oct 18 09:55:36 2021    re_test.log
 
          3 function calls in 0.000 seconds
 
    Random listing order was used
 
    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
         1    0.000    0.000    0.000    0.000 {built-in method builtins.exec}
         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
         1    0.000    0.000    0.000    0.000 <string>:1(<module>)
 
 
 
 In [3]:
```

 sort_stas()に与えるキー

| 文字列指定 | Enum指定 | 意味 |
|:--|:--|:--|
| 'calls' | SortKey.CALLS | 呼び出し数 |
| 'cumulative' | SortKey.CUMULATIVE | 累積時間 |
| 'cumtime' | N/A | 累積時間 |
| 'file' | N/A | ファイル名 |
| 'filename' | SortKey.FILENAME | ファイル名 |
| 'module' | N/A | ファイル名 |
| 'ncalls' | N/A | 呼び出し数 |
| 'pcalls' | SortKey.PCALLS | プリミティブな呼び出し回数 |
| 'line' | SortKey | LINE 行番号 |
| 'name' | SortKey.NAME | 関数名 |
| 'nfl' | SortKey.NFL | 関数名/ファイル名/行番号 |
| 'stdname' | SortKey.STDNAME | 標準名 |
| 'time' | SortKey.TIME | 内部時間 |
| 'tottime' | N/A | 内部時間 |


### dump_stats
次のようにすると指定した２点間のプロファイルデータを書き出すことができます。


```
 In [2]: # %load 10_dump.py
    ...: import cProfile
    ...: import sys
    ...: sys.setrecursionlimit(100000)
    ...:
    ...: def ackermann(m, n):
    ...:     if m == 0:
    ...:         return n + 1
    ...:     if n == 0:
    ...:         return ackermann(m - 1, 1)
    ...:     return ackermann(m - 1, ackermann(m, n - 1))
    ...:
    ...: if __name__ == '__main__':
    ...:     pr = cProfile.Profile()
    ...:     pr.enable()
    ...:     a = ackermann(3, 10)
    ...:     pr.disable()
    ...:     pr.dump_stats('ackermann.prof')
    ...:     print(a)
    ...:
 8189
 
 In [3]:
```

## Py-Spy 
[py-spy ](https://github.com/benfred/py-spy) は、すべての呼び出しを記録しようとするのではなく、プログラムの呼び出しスタックの状態を定期的にサンプリングすることで機能します。 運用中の実行されているコードでも安全に使用することができます。
![](https://gyazo.com/418b7397af1b8a6994f73b98b3606699.png)


 bash
```
 $ pip install py-spy
```

これで py-spy コマンドが利用できるようになります。 `--help` オプションを与えると簡単な使用方法が表示されます。



 bash
```
 % py-spy --help
 py-spy 0.3.10
 Sampling profiler for Python programs
 
 USAGE:
     py-spy <SUBCOMMAND>
 
 OPTIONS:
     -h, --help       Prints help information
     -V, --version    Prints version information
 
 SUBCOMMANDS:
     record    Records stack trace information to a flamegraph, speedscope or
               raw file
     top       Displays a top like view of functions consuming CPU
     dump      Dumps stack traces for a target program to stdout
     help      Prints this message or the help of the given subcommand(s)
     
```

record サブコマンドで実行状況を記録します。

 bash
```
 % py-spy record --help
 py-spy-record
 Records stack trace information to a flamegraph, speedscope or raw file
 
 USAGE:
     py-spy record [OPTIONS] --pid <pid> [python_program]...
 
 OPTIONS:
     -p, --pid <pid>              PID of a running python program to spy on
         --full-filenames
             Show full Python filenames, instead of shortening to show only the
             package part
     -o, --output <filename>      Output filename
     -f, --format <format>
             Output file format [default: flamegraph]  [possible values:
             flamegraph, raw, speedscope]
     -d, --duration <duration>
             The number of seconds to sample for [default: unlimited]
 
     -r, --rate <rate>
             The number of samples to collect per second [default: 100]
 
     -s, --subprocesses           Profile subprocesses of the original process
     -F, --function
             Aggregate samples by function's first line number, instead of
             current line number
         --nolineno               Do not show line numbers
     -t, --threads                Show thread ids in the output
     -g, --gil
             Only include traces that are holding on to the GIL
 
     -i, --idle                   Include stack traces for idle threads
         --nonblocking
             Don't pause the python process when collecting samples. Setting this
             option will reduce the perfomance impact of sampling, but may lead
             to inaccurate results
     -h, --help                   Prints help information
     -V, --version                Prints version information
 
 ARGS:
     <python_program>...    commandline of a python program to run
```


次のように実行します。

 bash
```
 $ sudo py-spy record — python3 script.py
```

Pythonスクリプトの実行中にプロファイラーをアタッチすることができます。 その場合、プロセスのPIDを与えます。

 bash
```
 $ sudo py-spy record --pid PID
```

py-spy プロファイラーは実行状況を定期的にサンプリングして情報を更新します。

 bash
```
 $ sudo py-spy top python 01_ackermann.py
```



py-spy は、システム管理者権限が必要になるため’、sudo が許可されているユーザで実行する必要があります。この点では、使い勝手がよいとは言えないいかも知れません。

## Pyinstrument
[pyinstrumen ](https://github.com/joerick/pyinstrument) は、コード中の最も遅い関数を表示することが主な目的のツールです。単純にそれだけですが、コードに多数の関数があるときは、その原因の分析に集中できるので、このツールの価値が高まります。
また、Pyinstrumentは、関数呼び出しのすべてのインスタンスをフックしようとはしません。プログラムのコールスタックをミリ秒ごとにサンプリングするため、個別の情報は目立たなくなりますが、プログラムのホットスポットを検出するのには十分な感度があります。

Pyinstrumentには、cProfileで使用できる便利な機能も多数サポートしています。プロファイラーをアプリケーションのオブジェクトとして使用し、アプリケーション全体ではなく、選択した関数の動作を記録することもできます。出力は、HTMLを含め、さまざまな方法でレンダリングできます。

ただし、次の２つの弱点があります
- Cythonで作成されたものなど、Cでコンパイルされた拡張機能を使用する一部のプログラムは、コマンドラインからPyinstrumentで呼び出すと正しく機能しない場合があるります。プログラム自体でPyinstrumentが使用されている場合は正常に機能します。
- Pyinstrumentは、複数のスレッドで実行されるコードでは正しく機能しません。こうしたコードにはPy-spyが良い選択になるかもしれません。

 bash
```
 $ pip install pyinstrument
```

引数なしで実行すると簡単な使用方法が表示されます。

 bash
```
  pyinstrument
 Usage: pyinstrument [options] scriptfile [arg] ...
 
 Options:
   --version             show program's version number and exit
   -h, --help            show this help message and exit
   --load-prev=ID        instead of running a script, load a previous report
   -m MODULE_NAME        run library module as a script, like 'python -m
                         module'
   --from-path           (POSIX only) instead of the working directory, look
                         for scriptfile in the PATH environment variable
   -o OUTFILE, --outfile=OUTFILE
                         save to <outfile>
   -r RENDERER, --renderer=RENDERER
                         how the report should be rendered. One of: 'text',
                         'html', 'json', or python import path to a renderer
                         class
   -t, --timeline        render as a timeline - preserve ordering and don't
                         condense repeated calls
   --hide=EXPR           glob-style pattern matching the file paths whose
                         frames to hide. Defaults to hiding non-application
                         code
   --hide-regex=REGEX    regex matching the file paths whose frames to hide.
                         Useful if --hide doesn't give enough control.
   --show=EXPR           glob-style pattern matching the file paths whose
                         frames to show, regardless of --hide or --hide-regex.
                         For example, use --show '*/<library>/*' to show frames
                         within a library that would otherwise be hidden.
   --show-regex=REGEX    regex matching the file paths whose frames to always
                         show. Useful if --show doesn't give enough control.
   --show-all            show everything
   --unicode             (text renderer only) force unicode text output
   --no-unicode          (text renderer only) force ascii text output
   --color               (text renderer only) force ansi color text output
   --no-color            (text renderer only) force no color text output
```

次にように実行すると、コードのHTMLレポートを生成します。
 bash
```
 $ pyinstrument -r html script.py
```


## line_profile

ホットスポットの原因が実際には関数内の1行にあり、その行はソースコードを読み取るだけでは明らかでない場合があります。 こうしたケースは、科学技術計算で非常に頻繁に発生します。 この領域でのプログラムでは、正当なアルゴリズムの複雑さや、プログラマーがFORTRANのようにコードを書き込もうとしているなどの理由で、関数は大きくなる傾向があります。
numpyのようなライブラリーを使用すると、関数呼び出しのない単一のステートメントが大量の計算をトリガーする可能性があります。 [cProfile ](https://docs.python.org/ja/3/library/profile.html) は、明示的な関数呼び出しのみを実行し、構文のために呼び出される特別なメソッドは実行しません。
- 次のような大きな配列でのnumpy操作は比較的遅い結果となることがあります。


```
 a[large_index_array] = some_other_large_array
```

このようなコードには明示的な関数呼び出しがないため、cProfileによって解析されることのないホットスポットです。

LineProfilerにはプロファイルする関数を指定でき、それらの関数内の**個々の行の実行時間**を計測します。 

#### インストール
line_profile は拡張モジュールなので、利用するためにはインストールする必要があります。

 bash
```
 $ pip install line_profiler
```

#### 使用方法
通常のワークフローでは、コードの1行ごとのタイミングの結果を確認するのは大変な作業になるため、いくつかの関数の行のタイミングだけを気にします。 ただし、LineProfilerには、プロファイルする関数を明示的に指示する必要があります。 開始する最も簡単な方法は、kernprofスクリプトを使用することです。

 bash
```
 $ kernprof -l script_to_profile.py
```


-  `-l` Profileの代わりにline_profilerモジュールの行ごとのプロファイラーを使用する
-  `-b` / `--builtin` : `profile` モジュールを使って計測します。
  -  `profile.enable()` と `profile.disable()` を使用してオンとオフを切り替えて計測
  -  `@profile` でデコレートしたひとつの関数を計測
  -  `with profile:` を使用してコード中のひとつのブロックを計測
-  `-o OUTFILE` /  `--outfile=OUTFILE` : 集計情報を保存するファイルを指定
-  `-s SETUP` / `--setup SETUP` : プロファイルするコードの前に実行するコード
-  `-v` /  `--view` : 集計情報をファイルに保存するだけでなく、端末に表示

kernprofは、LineProfilerのインスタンスを作成し、それをprofileという名前の `__builtins__` 名前空間に挿入します。 計測対象のスクリプトでは、プロファイルする関数を `@profile` でデコレートします。

```
 @profile
 def slow_function(a, b, c):
     ...
```

kernprofのデフォルトの動作は、結果をバイナリファイル `script_to_profile.py.lprof` に保存されます。  `[-v / -view]` オプションを使用すると、ターミナルでフォーマットされた結果をすぐに表示するようになります。

 bash
```
 Pystone(1.1) time for 50000 passes = 0.64814
 This machine benchmarks at 77143.8 pystones/second
 Wrote profile results to pystone.py.lprof
 Timer unit: 1e-06 s
 
 Total time: 0.154174 s
 File: pystone.py
 Function: Proc2 at line 153
 
 Line #      Hits         Time  Per Hit   % Time  Line Contents
 ==============================================================
    153                                           @profile
    154                                           def Proc2(IntParIO):
    155     50000      18192.0      0.4     11.8      IntLoc = IntParIO + 10
    156     50000      15349.0      0.3     10.0      while 1:
    157     50000      18615.0      0.4     12.1          if Char1Glob == 'A':
    158     50000      17864.0      0.4     11.6              IntLoc = IntLoc - 1
    159     50000      17989.0      0.4     11.7              IntParIO = IntLoc - IntGlob
    160     50000      16769.0      0.3     10.9              EnumLoc = Ident1
    161     50000      17831.0      0.4     11.6          if EnumLoc == Ident1:
    162     50000      16319.0      0.3     10.6              break
    163     50000      15246.0      0.3      9.9      return IntParIO
```

それ以外の場合は、後で次のように結果を表示できます。

 bash
```
 $ python -m line_profiler script_to_profile.py.lprof
```

出力では６つのフィールドがあり、次の意味を表します。
- **Line**: 全体の中の行数
- **Hits**: 呼び出し回数
- **Time**: 消費した時間
- **Per Hit**: １呼び出しあたりにかかった時間
- **% Time**: その関数内でかかった時間の割合
- **Line Contents**: その行の内容

### IPython での利用
IPythonを使用している場合は、プロファイルする関数と実行するステートメントを指定できる `％lprun` マジックコマンドが使用できます。 

IPython 0.11以降の場合、IPython構成ファイル `~/.ipython/profile_default/ipython_config.py` を編集して、 `line_profiler` を拡張機能リストに追加することでインストールすることができます。


```
 c.TerminalIPythonApp.extensions = [
     'line_profiler',
 ]
```

 `％lprun` の使用法のヘルプを取得するには、標準のIPythonヘルプメカニズムを使用します。


```
 In [1]: %lprun?
```

次のようにコードセルに入力することで計測することができます。

 ipython
```
 %lprun -f func1 -f func2 <statement>
```



## Yappi

[Yappi ](https://github.com/sumerc/yappi/) は **Y**et **A**nother **P**ython **P**rof**I**ler の略で、もう一つのPythonプロファイラです.が、スレッド、コルーチン、グリーンレットに対応しています。
次のような特徴があります。

- **高速**：Yappiは高速です。完全にC言語で書かれており、高速化のために多くの愛と配慮がなされています。
- **ユニーク**：Yappiは高速です。Yappiはマルチスレッド、asyncio、geventのプロファイリングをサポートしています。複数のプロファイラの結果にタグを付けたり、フィルタリングしたりすることもできます。
- **直感的**：プロファイラの開始/停止が可能で、いつでも、どのスレッドからでも結果を得ることができます。
- **標準に準拠**：プロファイラの結果はcallgrindまたはpstat形式で保存できます。
- **豊富な機能**： プロファイラの結果は、ウォールタイムまたは実際のCPUタイムのいずれかを表示することができ、異なるセッションから集約することができます。プロファイラの結果をフィルタリングしたり、ソートするための様々なフラグが定義されています。
- **堅牢**：Yappiは何年にもわたって本番環境で使用されてきました。


 bash
```
 $ pip install yappi
```



 c01_package_a.py
```
 def a():
     for _ in range(10000000):
         pass
 
 
 if __name__ == '__main__':
     import yappi
 
     yappi.set_clock_type("cpu")
     yappi.start()
     a()
     yappi.get_func_stats().print_all()
     yappi.get_thread_stats().print_all()
     
```

 bash
```
 $ python c01_package_a.py
 
 Clock type: CPU
 Ordered by: totaltime, desc
 
 name                                  ncall  tsub      ttot      tavg
 ..ling/07_Yappi/c01_package_a.py:1 a  1      0.337101  0.337101  0.337101
 
 name           id     tid              ttot      scnt
 _MainThread    0      4663713280       0.338377  1
 
```

 `yappi.set_clock_type()` に与えることができるクロックタイプは次のものどす。

- "cpu"：CPUクロック
- ”wall"：実経過時間(Wall Time)

 `yappi.get_func_stats().print_all()` による、プロファイルの結果が出力されます。

 yappiの出力のキーワード

| キーワード | 説明 |
|:--|:--|
| name | 呼び出された関数の完全な一意の名前です |
| ncall | この関数が何回呼び出されたか |
| tsub | この関数がサブコールを除いて全体で費やした時間 |
| ttot | この関数がサブコールを含めて合計で費やした時間 |
| tavg | この関数が平均で費やした時間（サブコールを含む） |

その次の行は、 `yappi.get_thread_stats().print_all()` による、
スレッドプロファイルの結果です。

 get_thread_stats()でのキーワードと意味

| キーワード 説明 |
|:--|
| name 呼び出された関数の完全な一意の名前です |
| ncall この関数が呼び出された回数 |
| tsub サブコールを除いた、この関数が費やした合計時間 |
| ttot サブコールを含む、この関数が費やした合計時間 |
| tavg サブコールを含む、この関数が費やした平均時間 |



 c02_multi_thread.py
```
 import yappi
 import time
 import threading
 
 _NTHREAD = 3
 
 def _work(n):
     time.sleep(n * 0.1)
 
 yappi.start()
 
 threads = []
 # スレッドを生成
 for i in range(_NTHREAD):
     t = threading.Thread(target=_work, args=(i + 1, ))
     t.start()
     threads.append(t)
 
 # スレッドが終了するのを待つ
 for t in threads:
     t.join()
 
 yappi.stop()
 
 # スレッドIDによるスレッド統計情報の取得
 threads = yappi.get_thread_stats()
 for thread in threads:
     print(
         "Function stats for (%s) (%d)" % (thread.name, thread.id)
     )
     yappi.get_func_stats(ctx_id=thread.id).print_all()
     
```


 bash
```
 $ python  c02_multi_thread.py
 Function stats for (_MainThread) (0)
 
 Clock type: CPU
 Ordered by: totaltime, desc
 
 name                                  ncall  tsub      ttot      tavg
 ..n3.9/threading.py:873 Thread.start  3      0.000092  0.000914  0.000305
 ..n3.9/threading.py:1021 Thread.join  3      0.000081  0.000828  0.000276
 ..:1059 Thread._wait_for_tstate_lock  3      0.000121  0.000689  0.000230
 ..hon3.9/threading.py:556 Event.wait  3      0.000081  0.000580  0.000193
 ..n3.9/threading.py:985 Thread._stop  3      0.000169  0.000437  0.000146
 ...9/threading.py:280 Condition.wait  3      0.000140  0.000414  0.000138
 ..9/threading.py:795 Thread.__init__  3      0.000147  0.000396  0.000132
 ..hon3.9/threading.py:899 Thread.run  3      0.000104  0.000350  0.000117
 ..7_Yappi/02_multi_thread.py:7 _work  3      0.000086  0.000246  0.000082
 ..ng.py:768 _maintain_shutdown_locks  3      0.000076  0.000215  0.000072
 ...9/threading.py:521 Event.__init__  3      0.000054  0.000105  0.000035
 ..hon3.9/threading.py:778 <listcomp>  3      0.000069  0.000104  0.000035
 ..9/threading.py:1338 current_thread  6      0.000062  0.000087  0.000015
 ..n3.9/_weakrefset.py:86 WeakSet.add  3      0.000035  0.000049  0.000016
 ...py:268 Condition._acquire_restore  3      0.000030  0.000044  0.000015
 ..hreading.py:259 Condition.__exit__  3      0.000031  0.000043  0.000014
 ..reading.py:256 Condition.__enter__  3      0.000029  0.000042  0.000014
 ..ing.py:265 Condition._release_save  3      0.000029  0.000041  0.000014
 ..reading.py:271 Condition._is_owned  3      0.000028  0.000041  0.000014
 ..hreading.py:228 Condition.__init__  3      0.000037  0.000037  0.000012
 ..n3.9/threading.py:529 Event.is_set  6      0.000030  0.000030  0.000005
 ..reading.py:1127 _MainThread.daemon  6      0.000030  0.000030  0.000005
 ..ython3.9/threading.py:750 _newname  3      0.000019  0.000019  0.000006
 ..ng.py:1209 _make_invoke_excepthook  3      0.000018  0.000018  0.000006
 Function stats for (Thread) (1)
 
 Clock type: CPU
 Ordered by: totaltime, desc
 
 name                                  ncall  tsub      ttot      tavg
 ..hon3.9/threading.py:899 Thread.run  1      0.000029  0.000144  0.000144
 ..7_Yappi/c02_multi_thread.py:7 _work 1      0.000033  0.000115  0.000115
 Function stats for (Thread) (3)
 
 Clock type: CPU
 Ordered by: totaltime, desc
 
 name                                  ncall  tsub      ttot      tavg
 ..hon3.9/threading.py:899 Thread.run  1      0.000043  0.000110  0.000110
 ..7_Yappi/c02_multi_thread.py:7 _work 1      0.000028  0.000067  0.000067
 Function stats for (Thread) (2)
 
 Clock type: CPU
 Ordered by: totaltime, desc
 
 name                                  ncall  tsub      ttot      tavg
 ..hon3.9/threading.py:899 Thread.run  1      0.000032  0.000096  0.000096
 ..7_Yappi/c02_multi_thread.py:7 _work 1      0.000025  0.000064  0.000064
 
```


モジュールでフィルタリングする場合は次のようにします。


 03_module_filtering.py
```
 import pc01_ackage_a as package_a
 import yappi
 import sys
 
 def a():
     pass
 
 def b():
     pass
 
 yappi.start()
 a()
 b()
 package_a.a()
 yappi.stop()
 
 # モジュールでフィルタリング：外部モジュールは除外
 current_module = sys.modules[__name__]
 stats = yappi.get_func_stats(
     filter_callback=lambda x: yappi.module_matches(x, [current_module])
 )  # x is a yappi.YFuncStat object
 stats.sort("name", "desc").print_all()
 
```

 bash
```
 $ python c03_module_filtering.py
 
 Clock type: CPU
 Ordered by: name, desc
 
 name                                  ncall  tsub      ttot      tavg
 .._Yappi/c03_module_filtering.py:8 b  1      0.000003  0.000003  0.000003
 .._Yappi/c03_module_filtering.py:5 a  1      0.000004  0.000004  0.000004
 
```


関数でフィルタリングする場合は次のようにします。

 c04_function_filtering.py
```
 import c01_package_a as package_a
 import yappi
 import sys
 
 def a():
     pass
 
 def b():
     pass
 
 yappi.start()
 a()
 b()
 package_a.a()
 yappi.stop()
 
 # 関数でフィルタリング：関数 a(), b() だけ
 current_module = sys.modules[__name__]
 stats = yappi.get_func_stats(
     filter_callback=lambda x: yappi.func_matches(x, [a, b])
 )
 stats.print_all()
 
```

 bash
```
 $ python c04_function_filtering.py
 
 Clock type: CPU
 Ordered by: totaltime, desc
 
 name                                  ncall  tsub      ttot      tavg
 ..appi/c04_function_filtering.py:5 a  1      0.000003  0.000003  0.000003
 ..appi/c04_function_filtering.py:8 b  1      0.000003  0.000003  0.000003
 
```


 c05_module_name_filtering.py
```
 import c01_package_a as package_a
 import yappi
 import sys
 
 def a():
     pass
 
 def b():
     pass
 
 yappi.start()
 a()
 b()
 package_a.a()
 yappi.stop()
 
 # モジュール名でフィルタリング：package_a モジュールのものだけ
 current_module = sys.modules[__name__]
 stats = yappi.get_func_stats(
     filter_callback=lambda x: 'package_a' in x.module
 )
 stats.print_all()
```


 bash
```
 $ python  c05_module_name_filtering.py
 
 Clock type: CPU
 Ordered by: totaltime, desc
 
 name                                  ncall  tsub      ttot      tavg
 ..ling/07_Yappi/c01_package_a.py:1 a  1      0.311336  0.311336  0.311336
 
```



 c06_function_name_filtering.ppy
```
 import c01_package_a as package_a
 import yappi
 import sys
 
 def a():
     pass
 
 def b():
     pass
 
 yappi.start()
 a()
 b()
 package_a.a()
 yappi.stop()
 
 # 関数名でフィルタリング： 関数名が a() のものだけ
 current_module = sys.modules[__name__]
 stats = yappi.get_func_stats(
     filter_callback=lambda x: 'a' in x.name
 )
 stats.print_all()
 
```

 bash
```
 $ python c06_function_name_filtering.py
 
 Clock type: CPU
 Ordered by: totaltime, desc
 
 name                                  ncall  tsub      ttot      tavg
 ..ling/07_Yappi/c01_package_a.py:1 a  1      0.318673  0.318673  0.318673
 ..c06_function_name_filtering.py:5 a  1      0.000006  0.000006  0.000006
 
```




### asyncio アプリケーション
コルーチンの wall-time が正しくプロファイリングされていることがわかります。

 c07_asyncio.py
```
 import asyncio
 import yappi
 
 async def foo():
     await asyncio.sleep(1.0)
     await baz()
     await asyncio.sleep(0.5)
 
 async def bar():
     await asyncio.sleep(2.0)
 
 async def baz():
     await asyncio.sleep(1.0)
 
 yappi.set_clock_type("WALL")
 with yappi.run():
     asyncio.run(foo())
     asyncio.run(bar())
 
 yappi.get_func_stats().print_all()
 
```

 bash
```
 % python c07_asyncio.py
 
 Clock type: WALL
 Ordered by: totaltime, desc
 
 name                                  ncall  tsub      ttot      tavg
 ..python3.9/asyncio/runners.py:8 run  2      0.000084  4.518389  2.259194
 ..lectorEventLoop.run_until_complete  6      0.000111  4.516125  0.752687
 .._UnixSelectorEventLoop.run_forever  6      0.000146  4.515682  0.752614
 ..5 _UnixSelectorEventLoop._run_once  20     0.000458  4.515431  0.225772
 ..thon3.9/asyncio/tasks.py:636 sleep  4      4.514231  4.514440  1.128610
 ..ctors.py:554 KqueueSelector.select  20     0.000149  4.513940  0.225697
 ..ling/07_Yappi/c07_asyncio.py:4 foo  1      0.000029  2.510629  2.510629
 ..ling/07_Yappi/c07_asyncio.py:9 bar  1      0.000007  2.003854  2.003854
 ..ing/07_Yappi/c07_asyncio.py:12 baz  1      0.000007  1.004189  1.004189
 ..py:57 _UnixSelectorEventLoop.close  2      0.000025  0.001096  0.000548
 ..py:87 _UnixSelectorEventLoop.close  2      0.000042  0.001070  0.000535
 (中略)
  .._.py:1675 Logger.getEffectiveLevel  1      0.000002  0.000002  0.000002
 ..rs.py:64 _SelectorMapping.__init__  2      0.000002  0.000002  0.000001
 ..g/__init__.py:1276 Manager.disable  1      0.000001  0.000001  0.000001
 .. _GeneratorContextManager.__exit__  1      0.000000  0.000000  0.000000
```


### geventアプリケーション

 c08_gevent.py
```
 import yappi
 from greenlet import greenlet
 import time
 
 class GreenletA(greenlet):
     def run(self):
         time.sleep(1)
 
 yappi.set_context_backend("greenlet")
 yappi.set_clock_type("wall")
 
 yappi.start(builtins=True)
 a = GreenletA()
 a.switch()
 yappi.stop()
 
 yappi.get_func_stats().print_all()
 
```


 bash
```
 % python c08_gevent.py
 
 Clock type: WALL
 Ordered by: totaltime, desc
 
 name                                  ncall  tsub      ttot      tavg
 ..h' of 'greenlet.greenlet' objects>  1      1.003298  1.003298  1.003298
 ..appi/c08_gevent.py:6 GreenletA.run  1      0.000006  1.003263  1.003263
 time.sleep                            1      1.003257  1.003257  1.003257
 
```



## IPython
IPythonはには、コードのタイミングやプロファイリングのための様々な機能が提供されています。ここでは、以下のIPythonのマジックコマンドについて説明します。

-  `%time` : 1つの文の実行時間を計る
-  `timeit` : 1つのステートメントの繰り返し実行をより正確に計る。
-  `%prun` : プロファイラでコードを実行する
-  `%lprun` : line-by-line プロファイラでコードを実行します。
-  `%memit` : 1 つのステートメントのメモリ使用量を測定します。
-  `%mprun` : コードをライン・バイ・ライン・プロファイラで実行します。mprun: コードをラインバイラインのメモリプロファイラで実行する

最後の4つのコマンドはIPythonにバンドルされていませんので、line_profilerとmemory_profilerの拡張機能を入手する必要があります

 `%timeit` ラインマジックとと  `%%timeit` セルマジックは、コードのスニペットを繰り返し実行する時間を計るのに使えます。

 pytohn
```
 In [2]: # %load 01_timeit.py
    ...: %timeit sum(range(100))
    ...:
 1.53 µs ± 140 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
 
```

この例のように短い処理の場合では、 `%timeit` は自動的に多くの繰り返しを行うことに注意してください。逆に遅い処理の場合は、 `%timeit` が自動的に調整して、少ない回数の繰り返しで計測します。


```
 In [1]: %load 02_timeit_cell.py
 
 In [2]: %%timeit
    ...: total = 0
    ...: for i in range(1000):
    ...:     for j in range(1000):
    ...:         total += i * (-1) ** j
    ...:
    ...:
 543 ms ± 30.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
 
 In [3]:
```

 `%load 02_timeit_cell.py` を実行したあとに、セルを上記のように修正して実行してください。


ある操作を繰り返すことが最良の選択ではない場合があります。例えば、ソートしたいリストがある場合、繰り返しの操作に惑わされてしまうかもしれません。ソート済みのリストをソートする方が、ソートされていないリストをソートするよりもはるかに速いので、繰り返し操作すると結果が歪んでしまいます。


```
 In [2]: # %load 03_sort.py
    ...: import random
    ...:
    ...: L = [random.random() for i in range(100000)]
    ...:
    ...: # %timeit L.sort()
    ...:
 
 In [3]: %timeit L.sort()
 2.85 ms ± 53.7 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
 
 In [4]:
```

このような場合は、 `%time` マジックコマンドの方が良いかもしれません。また、システムに起因する短時間の遅延が結果に影響を与えないような、実行時間の長いコマンドにも適しています。では、ソートされていないリストとソートされているリストのソートを計ってみましょう。


```
 In [2]: # %load 04_sort_list.py
    ...: import random
    ...:
    ...: L = [random.random() for i in range(100000)]
    ...:
    ...: # %time L.sort() # unsorted list
    ...: # %time L.sort() # sorted list
    ...:
 
 In [3]: %time L.sort()
 CPU times: user 33 ms, sys: 818 µs, total: 33.8 ms
 Wall time: 36.1 ms
 
 In [4]: %time L.sort()
 CPU times: user 3.09 ms, sys: 152 µs, total: 3.24 ms
 Wall time: 4.68 ms
 
 In [5]:
 
```

しかし、ソートされたリストであっても、 `%time` と  `%timeit` では、タイミングがどれだけ長くかかるかにも注目してください。これは、 `%timeit` が、システムコールがタイミングに干渉するのを防ぐために、フードの下でいくつかの巧妙なことを行っているという事実の結果です。例えば、他の方法でタイミングに影響を与える可能性のある、使用されていないPythonオブジェクトのクリーンアップ（ガベージコレクションとして知られています）を防ぎます。このような理由から、 `%timeit` の結果は、通常、 `%time ` の結果よりも明らかに速くなります。

Timeitと同様に、 `%time` においても、パーセント記号を２つ（ `%%` )で始めると、セルマジック構文となり、複数行のスクリプトのタイミングを取ることができます。


```
 In [1]: %load 05_time_cell.py
 
 In [2]: %%time
    ...: total = 0
    ...: for i in range(1000):
    ...:     for j in range(1000):
    ...:         total += i * (-1) ** j
    ...:
    ...:
 CPU times: user 558 ms, sys: 11 ms, total: 569 ms
 Wall time: 605 ms
 
 In [3]:
 
```


 `%load 05_time_cell.py` を実行したあとに、セルを上記のように修正して実行してください。

### 関数ごとのプロファイリング: %prun
プログラムは多くの単一のステートメントで構成されていますが、これらのステートメントの文脈の中でタイミングを取ることは、それら単独でタイミングを取ることよりも重要な場合があります。Pythonにはコードプロファイラが組み込まれていますが、IPythonはこのプロファイラをより便利に使う方法を提供しています。

例として、いくつかの計算を行う簡単な関数を定義してみましょう。


```
 In [2]: # %load 06_prun.py
    ...: def sum_of_lists(N):
    ...:     total = 0
    ...:     for i in range(5):
    ...:         L = [j ^ (j >> i) for j in range(N)]
    ...:         total += sum(L)
    ...:     return total
    ...:
    ...: # %prun sum_of_lists(1000000)
    ...:
 
 In [3]: %prun sum_of_lists(1000000)
          14 function calls in 1.023 seconds
 
    Ordered by: internal time
 
    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
         5    0.909    0.182    0.909    0.182 <ipython-input-2-5bb76001f08a>:5(<listcomp>)
         5    0.051    0.010    0.051    0.010 {built-in method builtins.sum}
         1    0.047    0.047    1.007    1.007 <ipython-input-2-5bb76001f08a>:2(sum_of_lists)
         1    0.016    0.016    1.023    1.023 <string>:1(<module>)
         1    0.000    0.000    1.023    1.023 {built-in method builtins.exec}
         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
 
 In [4]:
 
```


この結果、各関数呼び出しの合計時間の順に、実行に最も時間がかかっている場所を示されます。この場合、実行時間の大部分は `sum_of_lists()` 内のリスト内包にかかっています。ここから、アルゴリズムのパフォーマンスを向上させるために、どのような変更を加えるかを考え始めることができます。

 `%prun` の詳細や使用可能なオプションについては、IPythonのプロンプトに  `%prun?` を入力すると、IPythonのヘルプ機能が起動して、使用方法が表示されます。



```
 Docstring:
 Run a statement through the python code profiler.
 
 Usage, in line mode:
   %prun [options] statement
 
 Usage, in cell mode:
   %%prun [options] [statement]
   code...
   code...
 
 In cell mode, the additional code lines are appended to the (possibly
 empty) statement in the first line.  Cell mode allows you to easily
 profile multiline blocks without having to put them in a separate
 function.
 
 The given statement (which doesn't require quote marks) is run via the

 Namespaces are internally managed to work correctly; profile.run
 cannot be used in IPython because it makes certain assumptions about
 namespaces which do not hold under IPython.
 
 Options:
 (以下略)
```

### 行ごとのプロファイリング： %lprun
 `%prun` による関数ごとのプロファイリングは便利ですが、時には行ごとのプロファイリングレポートがあるとより便利です。line_profiler パッケージがインストールするとこの機能が追加されます。

 bash
```
 $ pip install line_profiler
```

次に、IPythonに拡張機能 line_profiler を読み込みませます。


```
 %load_ext line_profiler
```

これで、%lprun コマンドは任意の関数の行ごとのプロファイリングを行うことができます。
この場合、どの関数のプロファイリングに興味があるかを明示的に伝える必要があります。


```
 In [2]: # %load 07_lprun.py
    ...: def sum_of_lists(N):
    ...:     total = 0
    ...:     for i in range(5):
    ...:         L = [j ^ (j >> i) for j in range(N)]
    ...:         total += sum(L)
    ...:     return total
    ...:
    ...: # %load_ext line_profiler
    ...: # %lprun -f sum_of_lists sum_of_lists(5000)
    ...:
 
 In [3]: %load_ext line_profiler
 
 In [4]: %lprun -f sum_of_lists sum_of_lists(5000)
 Timer unit: 1e-06 s
 
 Total time: 0.01216 s
 File: <ipython-input-2-e305294cbc33>
 Function: sum_of_lists at line 2
 
 Line #      Hits         Time  Per Hit   % Time  Line Contents
 ==============================================================
      2                                           def sum_of_lists(N):
      3         1          9.0      9.0      0.1      total = 0
      4         6          9.0      1.5      0.1      for i in range(5):
      5         5      11880.0   2376.0     97.7          L = [j ^ (j >> i) for j in range(N)]
      6         5        261.0     52.2      2.1          total += sum(L)
      7         1          1.0      1.0      0.0      return total
 
 In [5]:
 
```

時間はマイクロ秒単位で表示され、プログラムが最も時間を費やしている場所がわかります。この時点で、この情報を使ってスクリプトの一部を変更し、より良いパフォーマンスを実現できるかもしれません。

 `%lprun` やそのオプションの詳細については、IPythonのヘルプ機能（IPythonのプロンプトで `%lprun?` で知ることができます。


### メモリ使用量のプロファイリング: %memit および %mprun
プロファイリングのもう一つの側面は、ある操作が使用するメモリの使用量についての計測です。これはIPythonのもう一つの拡張機能であるmemory_profiler をインストールすることで評価できます。

 bash
```
 $ pip install memory_profiler
```

次に、IPythonに拡張機能 memory_profiler を読み込みませます。


```
 %load_ext memory_profiler
```



```
 In [2]: # %load 08_memit.py
    ...: def sum_of_lists(N):
    ...:     total = 0
    ...:     for i in range(5):
    ...:         L = [j ^ (j >> i) for j in range(N)]
    ...:         total += sum(L)
    ...:     return total
    ...:
    ...: # %load_ext memory_profiler
    ...: # %memit sum_of_lists(1000000)
    ...:
 
 In [3]: %load_ext memory_profiler
 
 In [4]: %memit sum_of_lists(1000000)
 peak memory: 164.61 MiB, increment: 100.33 MiB
 
 In [5]:
 
```

この例では、関数が　164MBのメモリを使用していることがわかります。

メモリ使用量を一行ごとに説明するには、 `%mprun` マジックを使用します。このマジックコマンドは、指定した関数がモジュールとして存在していることを期待しているので、まず  `mprun_demo.py` というシンプルなモジュールを作成しておきます。このモジュールには、sum_of_lists 関数が含まれていますが、メモリ・プロファイリングの結果をより明確にするために `del L` を 1 つ追加しています。

 mprun_demo.py
```
 def sum_of_lists(N):
     total = 0
     for i in range(5):
         L = [j ^ (j >> i) for j in range(N)]
         total += sum(L)
         del L # remove reference to L
     return total
 
```



```
 In [2]: # %load 09_mprun.py
    ...: from mprun_demo import sum_of_lists
    ...:
    ...: # %load_ext memory_profiler
    ...: # %mprun -f sum_of_lists sum_of_lists(100000)
    ...:
 
 In [3]: %load_ext memory_profiler
 
 In [4]: %mprun -f sum_of_lists sum_of_lists(100000)
 Filename: /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Profiling/08_IPython/mprun_demo.py
 
 Line #    Mem usage    Increment  Occurences   Line Contents
 ============================================================
      1     65.3 MiB     65.3 MiB           1   def sum_of_lists(N):
      2     65.3 MiB      0.0 MiB           1       total = 0
      3     69.6 MiB      0.0 MiB           6       for i in range(5):
      4     72.3 MiB -366101.6 MiB      500015           L = [j ^ (j >> i) for j in range(N)]
      5     72.3 MiB      0.0 MiB           5           total += sum(L)
      6     69.6 MiB    -11.0 MiB           5           del L
      7     69.6 MiB      0.0 MiB           1       return total
 
 
 In [5]:
```

ここでは、 `Increment` の欄に、各行が総メモリに与える影響が表示されています。リストLには、約11MBのメモリが使用されることがわかります。これは、Python インタープリタ自体が使用するバックグラウンドメモリに加算されていることに留意してください。

 `%memit` と  `%mprun` の詳細および使用可能なオプションについては、IPythonのヘルプ機能を使用してください（IPythonのプロンプトで  `%memit?` と入力してください）。



### line_profiler とmemory_profiler  の自動読み込み

 `line_profiler` と `memory_profiler` を 常に有効にさせるためには、 `~/.ipython/profile_default/ipython_config.py` に次のコードを追加にしてください。

 ~/.ipython/profile_default/ipython_config
```
 c.TerminalIPythonApp.extensions = [
      'line_profiler',
      'memory_profiler',
 ]
```




## gprof2dot
大規模なプログラムがある場合、関数が互いにどのように呼び出されるかを確認したい場合があります。 [gprof2dot ](https://github.com/jrfonseca/gprof2dot) を使用すると、プロファイラーの出力からGraphvizのdotグラフを生成します。


![](https://gyazo.com/9f20e497994ab69f671aae4f6a0f8a4a.png)

cProfile / profileを含む多くの有名なプロファイラーをサポートしています。

 bash
```
 $ python -m cProfile -o output.pstats path/to/your/script arg1 arg2
 $ gprof2dot.py -f pstats output.pstats | dot -Tpng -o output.png
```


## SnakeViz

SnakeViz は cProfile で生成したプロファイルデータ( `*.prof` ) を読み取って可視化するWebアプリケーションです。

pip でインストールすることができます。

 bash
```
 $ pip install snakeviz
```

profファイルが置かれているディレクトリに移動し、コマンドラインで次のように入力します。

 bash
```
 $ snakeviz output.prof
```

デフォルトのブラウザに、.profファイルのデータを表示するインタラクティブなウィンドウが開きます。デフォルトでは、データはサンバーストプロット(sunburst plot:)で表示されます。

![](https://gyazo.com/5d4803a90f27607f99d337bd7081e853.png)

コールスタックの深さを調整して、より深い関数を表示することができます。また、特定の関数をクリックすると、選択した関数を中心とした新しいプロットが生成されます。

また、データをつらら状に表示(icicle plot:)することもできます。


![](https://gyazo.com/631b7719c695cbc2a84a04b4c03e1a7c.png)


また、SnakeVizではコールスタックの中で最もコストのかかる関数を降順に並べて表示することもできます。

![](https://gyazo.com/ac31d7e2e09d545aee5cde5444980d53.png)




## まとめ
次のようなフローで行うと効率的なプロファイリングができます。

- 運用中のサービスでは
  - py-spy や pyinstrument でホットスポットを絞り込みむ
- cProfile/profile を遅い関数を絞り込む
- line-profiler で原因を特定する
- 非同期/並列処理では yappi を使用してみる



## 参考
- Python公式ドキュメント  [time --- 時刻データへのアクセスと変換 ](https://docs.python.org/ja/3.7/library/time.html?highlight=time%20perf_counter#module-time)
- Python公式ドキュメント [timeit --- 小さなコード断片の実行時間計測 ](https://docs.python.org/ja/3/library/timeit.html#module-timeit)
- Python公式ドキュメント [cProfile/profile ](https://docs.python.org/ja/3/library/profile.html)
- line-profile: [ソースコード ](https://github.com/rkern/line_profiler)
- [WindowsでGraphViz をインストール ](https://www.kkaneko.jp/tools/win/graphviz.html)

#### その他のプロファイラー
- [profiling ](https://github.com/what-studio/profiling) threadやgreenlet単位で計測できる
- [vmprof-python ](https://github.com/vmprof/vmprof-python): 




