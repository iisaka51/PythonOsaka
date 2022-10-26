SSPipeを使って効率良くデータを操作してみよう
=================
![](images/sspipe_logo.png)
# はじめに

## SSPipeについて
SSPipeは、 迅速にデータを操作するためのPythonの拡張ライブラリです。
SSPipe は、複雑な式を一連の単純な変換に分解し、人間の読みやすさを向上させ、括弧のマッチンを確認する手間を減少させてくれます。

## インストール

 bash
```
 # Linux or MacOS
 $ python -m pip install sspipe
```
　
- # Windows
- $ py -3 -m pip install sspipe


## 使用例
### サンプル1
次のコードは手続型プログラミングのスタイルで記述したものです。


```
 import os

 data = os.listdir(".")
 data = filter(os.path.isfile, data)
 data = map(lambda x: [x, os.path.getsize(x)], data)
 data = dict(data)
 print(data)

```


何度も変数への代入が行われています。これを関数型プログラミングスタイルでコードすると次のようになります。


```
 import os

 print(dict(sorted(
     map(
         lambda x: [x, os.path.getsize(x)],
         filter(os.path.isfile, os.listdir("."))
     ), key=lambda x: x[1], reverses=True)
 )[:5]))

```


一見するとスッキリしているようなのですが、多くの場合、括弧がきちんと合っているか確認する必要があり、これは地味に面倒な作業でストレスになります。

それに、 初期データが何かがわかりにくくなってしまっています。これは、最初の処理が最も内側にあり、その処理結果が外側に受け継がれていくような記述になるためです。最後の処理が冒頭に来ているため、処理の順序が人間の思考とは逆になってしまいます。

初期データから始めて、次々と変換を追加していく方が、コードが読みやすくなるはずです。


```
 import os
 from sspipe import p

 ( os.listdir(".")
     | p(filter, os.path.isfile)
     | p(map, lambda x: [x, os.path.getsize(x)])
     | p(sorted, key=lambda x: x[1], reverse=True)[:5]
     | p(dict)
     | p(print)
 )
```

### サンプル2
 `report.csv` に記録するコードは次のようになります。


```
 import pandas as pd

 df = pd.read_csv('data.csv')
 df2 = df['class'] == 'A19']
 df3 = df2[df2.score > df2.score.mean()]
 df3.to_csv('report.csv')
```

これを SSpipe を使って書き直すと次のようにスッキリとしたコードになります。


```
 from sspipe import p, px
 import pandas as pd

 ( pd.read_csv('data.csv')
     | px[px['class'] == 'A19']
     | px[px.score > px.score.mean()].to_csv('report.csv')
 )
```

## サンプル3
他の例として、 `cos(x)` が  `0` より小さい範囲 `(0, 2*pi)` の点の `sin(x)` を赤色でプロットするコードは次のようになります。


```
 import numpy as np
 import matplotlib.pyplot as plt

 X = np.linspace(0, 2*np.pi, 100)
 X = X[np.cos(X) < 0]
 plt.plot(X, np.sin(X), 'r')
```

これを SSpipe を使うと次のように記述することができます。


```
 from sspipe import p, px
 import numpy as np
 import matplotlib.pyplot as plt

 ( np.linspace(0, 2*np.pi, 100)
     | px[np.cos(px) < 0]
     | p(plt.plot, px, np.sin(px), 'r')
 )

```

## パイプ演算子
Unixでのシェルで使われるパイプ( `｜` )や、R での magrittr の `%>%` 演算子のように、sspipeはpythonで同じ機能を提供します。

## 詳細な説明

SSpipe では、パイプでつながれたオブジェクトに対して呼び出される関数のラッパーで>ある  `p` とパイプでつながれたオブジェクトのプレースホルダーの  `px` の2つのオブジェクトが提供されます。


### 単純な関数コール
単純な関数コールで挙動を確認してみましょう。


```
 In [2]: # %load c10_function_call.py
    ...: X = "Hello World"
    ...: print(X)
    ...:
    ...: from sspipe import p
    ...: "Hello World" | p(print)
    ...:
 Hello World
 Hello World

 In [3]:

```

## 関数に引数を与える場合
関数に引数を与える場合でも、通常のように引数を追加できます。


```
 In [2]: # %load c11_function_call_with_args.py
    ...: X = "Hello "
    ...: print(X, "World",  end='!\n')
    ...:
    ...: from sspipe import p
    ...: "Hello " | p(print, "World", end='!\n')
    ...:
 Hello  World!
 Hello  World!

 In [3]:


```


### パイププレースホルダーで明示的に引数を渡す


```
 In [2]: # %load c12_piped_arguments.py
    ...: X = "World"
    ...: print("Hello", X, end="!\n")
    ...:
    ...: from sspipe import p, px
    ...: "World" | p(print, "World", px, end="!\n")
    ...:
 Hello World!
 World World!

 In [3]:

```

### パイプ連鎖
パイプ演算子でパイプオブジェクトを連鎖させることができます。


```
 In [2]: # %load c13_chaining_pipe.py
    ...: X = 5
    ...: X = X + 2
    ...: X = X ** 5 + X
    ...: print(X)
    ...:
    ...: from sspipe import p, px
    ...: 5 | px + 2 | px ** 5 + px | p(print)
    ...:
 16814
 16814

 In [3]:
```


## map() と filter()
組み込み関数の  `map()` と  `filter()` でも SSpipe を使うとスッキリとコードできます。


```
 In [2]: # %load c14_map_and_filter.py
    ...: X = range(5)
    ...: X = filter((lambda x:x%2==0),X)
    ...: X = map((lambda x: x + 10), X)
    ...: X = list(X)
    ...: print(X)
    ...:
    ...:
    ...: from sspipe import p, px
    ...: ( range(5)
    ...:   | p(filter, px % 2 == 0)
    ...:   | p(map, px + 10)
    ...:   | p(list) | p(print)
    ...: )
    ...:
 [10, 12, 14]
 [10, 12, 14]

 In [3]:
```


## numpy との連携
numpy の演算でも SSPipe を使うことができます。


```
 In [2]: # %load c15_numpy_expressions.py
    ...: %matplotlib
    ...: import numpy as np
    ...: import matplotlib.pyplot as plt
    ...:
    ...: X = range(10)
    ...: X = np.sin(X) + 1
    ...: plt.plot(X)
    ...:
    ...:
    ...: from sspipe import p, px
    ...: range(10) | np.sin(px)+1 | p(plt.plot)
    ...:
 Using matplotlib backend: MacOSX
 Out[2]: [<matplotlib.lines.Line2D at 0x11d6d96f0>]
 Out[2]: [<matplotlib.lines.Line2D at 0x11d735f60>]

 In [3]:

```

## DataFrameへ値のセット
DataFrameへ値をセットするときもSSpipeでコードできます。


```
 In [2]: # %load c16_assignment.py
    ...: import pandas as pd
    ...:
    ...: df = pd.read_csv('data.csv')
    ...:
    ...: df1 = df.copy()
    ...: X = df1['Name']
    ...: X = X.str.upper()
    ...: df1['Name'] = X
    ...:
    ...:
    ...: from sspipe import p, px
    ...: df2 = df.copy()
    ...: df2['Name'] |= px.str.upper()
    ...:

 In [3]: df1.head()
 Out[3]:
       Name   Score
 0     JACK     200
 1     JOHN     120
 2    EDDIE     100
 3  FREDDIE     190
 4    DAVID     130

 In [4]: df2.head()
 Out[4]:
       Name   Score
 0     JACK     200
 1     JOHN     120
 2    EDDIE     100
 3  FREDDIE     190
 4    DAVID     130

 In [5]:
```


## 変数のようにパイプを使用


```
 In [2]: # %load c17_pipe_as_vriable.py
    ...: _f1 = lambda x: x.strip().upper()
    ...: _f2 = lambda x: x.replace(' ','_')
    ...: _f3 = lambda x: _f2(_f1(x))
    ...: X = " ab cde "
    ...: X = _f3(X)
    ...: print(X)
    ...:
    ...:
    ...: from sspipe import p, px
    ...:
    ...: to_upper = px.strip().upper()
    ...: to_underscore = px.replace(' ', '_')
    ...: normalize = to_upper | to_underscore
    ...: " ab cde " | normalize | p(print)
    ...:
 AB_CDE
 AB_CDE

 In [3]:

```

## ネストしたデータ構造


```
 In [2]: # %load c18_builtin_data_structures.py
    ...: X = 2
    ...: X = {X-1: [X, (X+1, 4)]}
    ...: print(X)
    ...:
    ...:
    ...: from sspipe import p, px
    ...: 2 | p({px-1: p([px, p((px+1, 4))])}) | p(print)
    ...:
 {1: [2, (3, 4)]}
 {1: [2, (3, 4)]}

 In [3]:
```

# 動作の仕組み
 `p(func, *args, **kwargs)` 式は、 `__or__` と  `__ror__` 演算子をオーバーロードした Pipe オブジェクトを返します。このオブジェクトは  `x | <Pipe>` が評価されるまで  `func` と  `args` と  `kwargs` を保持し、Python から  `Pipe.__ror__` が呼び出されたときに実行されます。そして、 `func(x, *args, **kwargs)` を評価し、その結果を返します。

 `px` オブジェクトは単に  `p(lambda x: x)` です。

SSPipe は変換する関数をラップするだけで、パイプされたオブジェクトをラップしないことに注意してください。したがって、 `x` のような変数が  `Pipe` クラスのインスタンスでない場合、python が  `y = x | p(func)` を評価した後、結果の変数  `y` は  `Pipe` オブジェクトとして機能しません。したがって、 `y = func(x)` と評価したのと全く同じオブジェクトになります。


## 制約事項

SSPipe は、 `dict.items()` 、 `dict.keys()` 、 `dict.values()` との非互換性。

 `dict.keys()` 、 `dict.values()` 、`dict.items() ` が返すオブジェクトは、ビューオブジェクトと呼ばれ、Python はこれらの型に対して、クラスがパイプ演算子(` | `)をオーバーライドすることを許可していません。回避策として、ビューオブジェクトのためにスラッシュ演算子（` /`)が実装されています。


```
 In [2]: # %load c20_slash_operator.py
    ...: from sspipe import p
    ...:
    ...: # ビューオブジェクトにはパイプ演算子は使用できない
    ...: # 次の式は返ってこない...
    ...: #  {1: 2, 3: 4}.items() | p(list) | p(print)
    ...:
    ...: # スラッシュ演算子ではOK
    ...: {1: 2, 3: 4}.items() / p(list) | p(print)
    ...:
    ...: # 私はこちらの記述の方が好き。 pathlib の Path との関係
    ...: list({1: 2, 3: 4}.items()) | p(print)
    ...:
 [(1, 2), (3, 4)]
 [(1, 2), (3, 4)]

 In [3]:

```

これは私見なのですが、pathlib の Path オブジェクトが パス演算子( `/` 呼び名が違うだけで同じ記号）を使用するため、
このスラッシュ演算子はあまり好きではありません。

## Pipeとの互換性
このライブラリは、JulienPalard氏の知的で簡潔な [Pipe ](https://github.com/JulienPalard/Pipe)に触発され、それに依存したものです。もし単一の pipe.py スクリプトや、SSPipe のコア機能とロジックを実装した軽量なライブラリを求めているなら、Pipe は完璧なものです。

SSPipeは、一般的なライブラリとの統合や、 `px` の概念の導入、pythonの演算子のオーバーライドによって、パイプをファーストクラスオブジェクトにすることで、pipe の利用を容易にすることに焦点を合わせています。

Pipe ライブラリによって実装された既存のパイプはすべて `p.<original_name>` を通してアクセスでき、SSPipe と互換性を持っています。SSPipeは特定のパイプ関数を実装せず、パイプ関数の実装と命名をPipeに委譲しています。

例えば、Pipe での「フィボナッチの偶数項のうち400万を超えないものの総和を求めよ」を解く例は、sspipeを使って書き直すことが可能です。


```
 In [2]: # %load c21_fibonacchi.py
    ...: from sspipe import p, px
    ...:
    ...: def fib():
    ...:     a, b = 0, 1
    ...:     while True:
    ...:         yield a
    ...:         a, b = b, a + b
    ...:
    ...: v1 = (fib() | p.where(lambda x: x % 2 == 0)
    ...:             | p.take_while(lambda x: x < 4000000)
    ...:             | p.add())
    ...:
    ...: v2 = (fib() | p.where(px % 2 == 0)
    ...:             | p.take_while(px < 4000000)
    ...:             | p.add())
    ...:

 In [3]: v1
 Out[3]: 4613732

 In [4]: v2
 Out[4]: 4613732

 In [5]:

```

# 参考
- SSPipe
  - [PyPI - sspipe ](https://pypi.org/project/sspipe/)
  - [ソースコード ](https://github.com/sspipe/sspipe)
- PythonOsaka
  - [Pipeを使ってみよう](https://github.com/iisaka51/PythonOsaka/tree/main/Tutorials/Tutorial.Pipe/)

