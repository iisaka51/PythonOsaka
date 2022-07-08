Pipeを使って効率良くデータを操作してみよう
=================
## Pipeモジュールについて
[Pipe ](https://pypi.org/project/pipe/) は Bash などでのパイプ処理のような構文を提供する拡張モジュールです。パイプ( `|` ) はあ関数の結果を別の関数に渡すことができます。Pythonのイテラブルオブジェクト(Iterable Object) に複数の関数を適用するときでは、コードがすっきりと簡潔に記述することができます。


## インストール
pipe は 次のようにインストールすることができます。

 bash
```
 # Linux or MacOS
 $ python -m pip install pipe
```

 command
```
 # Windows
 $  py -3 -m pip install pipe
```


## Pipe の使用方法

まずは、簡単な例がみてましょう。

 `map()` と  `filter()` を同時に使用するとコードがわかりにくくなりがちですが、これを pipe を使うととても可読性がよくなります。


```
 In [2]: # %load c01_using_pipe.py
    ...: from pipe import where, select
    ...:
    ...: data = [1, 2, 3, 4, 5]
    ...:
    ...: # map() と filter() を同時に使用するとわかりにくい
    ...: v1 = list(map(lambda x: x * 2, filter(lambda x: x % 2 == 0, data)))
    ...:
    ...: # pipe を使うとコードがわかりやすくなる
    ...: v2 = list( data
    ...:            | where(lambda x: x % 2 == 0)
    ...:            | select(lambda x: x * 2) )
    ...:

 In [3]: v1
 Out[3]: [4, 8]

 In [4]: v2
 Out[4]: [4, 8]

 In [5]:

```

## Pipeの基礎知識
Pipeモジュールの基礎知識を説明しておきます。

- **パイプ（pipe)**
パイプは、パイプ記号（ `|` ）で接続できる関数のことです。次の例にある、 `add` はパイプになります。


```
 In [1]: from pipe import add

 In [2]: [1, 2, 3] | add
 Out[2]: 6

 In [3]:

```

- **パイプ関数(Pipe Function)**
通常の関数でイテラルオブジェクトを返すものは、パイプと同じようにパイプ記号に接続することができます。


```
 In [6]: range(10) | add
 Out[6]: 45

 In [7]:
```

- **パイプの引数**
パイプには引数を受け取るものと、不要なものがあります。


```
 In [1]: from pipe import where, traverse

 In [2]: sum([1, 2, 3, 4] | where(lambda x: x % 2 == 0))
 Out[2]: 6

 In [3]: sum([1, [2, 3], 4] | traverse)
 Out[3]: 10

 In [4]:
```


## pipe 1.x の非推奨事項
この資料作成時点では、pipe のバージョンは 1.6.3 です。この pipe 1.xで提供される関数には、イテラブルオブジェクト(iterable object)を返すものと、非イテラブルオブジェクト（non-iterable object) を返すものが混在しているため、混乱を招く状況になってしまっています。非イテラブルオブジェクトを返す関数は、パイプ式の最後の関数としてしか使えないため実際には役に立ちません。


```
 In [1]: from pipe import where, add

 In [2]: range(100) | where(lambda x: x % 2 == 0) | add
 Out[2]: 2450

 In [3]:

```

これは、次のように可読性を落とさずに書き換えることができます。


```
 In [1]: from pipe import where

 In [2]: sum(range(100) | where(lambda x: x % 2 == 0))
 Out[2]: 2450

 In [3]:

```

このため、非イテラブルオブジェクトを返すパイプはすべて非推奨となり、pipe 2.0で削除される予定です。



## Pipeモジュールで使用できるパイプ


## chain   イテラルオブジェクトを展開
 `chain())` はイテラルオブジェクトの要素を連結したイテラルオブジェクトを返します。ネストされたイテラルオブジェクトはひとつレベルが展開されたようになります。


```
 In [2]: # %load c02_chain.py
    ...: from pipe import chain
    ...:
    ...: data = [[1, 2, [3]], [4, 5]]
    ...: v1 = list( data | chain)
    ...:
    ...: # v1
    ...:

 In [3]: v1
 Out[3]: [1, 2, [3], 4, 5]

 In [4]:

```


## chain_with()  イテラルオブジェクトを連結
 `chain_with()` は  `chain` と名前が似ていますが、挙動が異なります。 `chain_with()` の引数の与えたイテラルオブジェクトを入力に連結します。


```
 In [2]: # %load c03_chain_with.py
    ...: from pipe import chain, chain_with
    ...:
    ...: data1 = [[1, 2, [3]], [4, 5]]
    ...: data2 = [6, 7]
    ...: v1 = list( data1 | chain_with(data2) )
    ...:
    ...: # v1
    ...:

 In [3]: v1
 Out[3]: [[1, 2, [3]], [4, 5], 6, 7]

 In [4]: list( data1 | chain)
 Out[4]: [1, 2, [3], 4, 5]

 In [5]:
```


## dedup()   重複した値を削除
 `dedup` は、リスト内の重複した値を削除します。 `set()` を使うことで同様のことができますが、括弧がネストしないので読みやすくなります。


```
 In [2]: # %load c04_dedup.py
    ...: from pipe import dedup
    ...:
    ...: data = [1, 2, 2, 3, 3, 3, 4, 4, 5, 6, 7, 7, 7, 8,  9]
    ...: v1 = list(data | dedup)
    ...: v2 = list(set(data))
    ...:
    ...: # v1
    ...: # v2
    ...:

 In [3]: v1
 Out[3]: [1, 2, 3, 4, 5, 6, 7, 8, 9]

 In [4]: v2
 Out[4]: [1, 2, 3, 4, 5, 6, 7, 8, 9]

 In [5]:

```

また、 `dedup` はキーを使ってユニークな要素を得ることができるので、 `set()` よりも柔軟性があります。
例えば、5より小さいユニークな要素を種痘する場合は次のようにできます。


```
 In [2]: # %load c04_dedup_with_key.py
    ...: from pipe import dedup
    ...:
    ...: data = [1, 2, 2, 3, 3, 3, 4, 4, 5, 6, 7, 7, 7, 8,  9]
    ...: v1 = list(data | dedup( lambda key: key < 5))
    ...:
    ...: # v1
    ...:

 In [3]: v1
 Out[3]: [1, 5]

 In [4]: v1 = list(data | dedup( lambda key: key < 2))

 In [5]: v1
 Out[5]: [1, 2]

 In [6]:

```

 `dedup` も他の関数と組み合わせることで、より複雑な処理を行うことができます。


```
 In [2]: # %load c04_dedup_complex.py
    ...: from pipe import select, dedup, where
    ...:
    ...: # ABV: Alcohol by Volume (アルコール度数)
    ...: beers = [
    ...:     { 'name': 'Pale Ale', 'abv': 5.5, 'stock': 6 },
    ...:     { 'name': 'Pale Ale', 'abv': 6.0, 'stock': 0 },
    ...:     { 'name': 'ICHII SENSHIN', 'abv': 6.5, 'stock': 6 },
    ...:     { 'name': 'ICHIGO ICHIE', 'abv': 5.5, 'stock': 24 },
    ...:     { 'name': 'Pilserl', 'abv': 4.9, 'stock': 12 },
    ...: ]
    ...:
    ...: v1 = list( beers | dedup(key=lambda beer: beer["name"]) )
    ...: v2 = list( beers
    ...:            | dedup(key=lambda beer: beer["name"])
    ...:            | select(lambda beer: beer["stock"]) )
    ...: v3 = list( beers
    ...:            | dedup(key=lambda beer: beer["name"])
    ...:            | select(lambda beer: beer["stock"])
    ...:            | where(lambda stock: stock > 10))
    ...:
    ...: # v1
    ...: # v2
    ...: # v3
    ...:

 In [3]: v1
 Out[3]:
 [{'name': 'Pale Ale', 'abv': 5.5, 'stock': 6},
  {'name': 'ICHII SENSHIN', 'abv': 6.5, 'stock': 6},
  {'name': 'ICHIGO ICHIE', 'abv': 5.5, 'stock': 24},
  {'name': 'Pilserl', 'abv': 4.9, 'stock': 12}]

 In [4]: v2
 Out[4]: [6, 6, 24, 12]

 In [5]: v3
 Out[5]: [24, 12]

 In [6]:

```

このコードは次の処理を行っています。
-  `beers` から重複した名前のデータを削除
- 在庫数 `stock` を抜き出してリストにする
- 在庫数 `stock` が10以上あるものだけに絞り込む


## groupby()  リスト内の要素をグループ化
リスト内の要素をある関数を使ってグループ化すると便利な場合があります。それは、 `groupby()` を使えば簡単にできます。
このメソッドがどのように機能するかを見るために、数字のリストを偶数か奇数かに基づいて数字をグループ化する辞書に変えてみましょう。


```
 In [2]: # %load c05_grouppy.py
    ...: from pipe import select, groupby
    ...:
    ...: data = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    ...: v1 = list( data | groupby(lambda x: "Even" if x % 2 == 0  else "Odd"))
    ...: v2 = list( data
    ...:              | groupby(lambda x: "Even" if x % 2 == 0  else "Odd")
    ...:              | select(lambda x: { x[0]: list(x[1])} ))
    ...:
    ...: # v1
    ...: # v2
    ...:

 In [3]: v1
 Out[3]:
 [('Even', <itertools._grouper at 0x111843c10>),
  ('Odd', <itertools._grouper at 0x111843af0>)]

 In [4]: v2
 Out[4]: [{'Even': [2, 4, 6, 8]}, {'Odd': [1, 3, 5, 7, 9]}]

 In [5]:

```

さらにフィルタリングしたいときも  `where` を使うだけです。


```
 In [2]: # %load c05_groupby_complex.py
    ...: from pipe import select, groupby, where
    ...:
    ...: data = (1, 2, 3, 4, 5, 6, 7, 8, 9)
    ...: v1 = list( data
    ...:              | groupby(lambda x: "Even" if x % 2 == 0  else "Odd")
    ...:              | select(lambda x: { x[0]: list( x[1]
    ...:                                         | where(lambda x: x> 4))} ))
    ...:
    ...: # v1
    ...:

 In [3]: v1
 Out[3]: [{'Even': [6, 8]}, {'Odd': [5, 7, 9]}]

 In [4]:
```


## islice() - リスト内の要素を抜き出す
 `islice()` はリストの  `slice()` のように動作します。 `islice(start, [stop, [step]])` として呼び出すと、 `next()` で選択された値を返すイテレータを返します。 `start` が指定された場合、直前の要素をすべてスキップする。
 `start` のデフォルトは0である。  `sstep` のデフォルトは1です。


```
 In [1]: %load c06_islice.py

 In [2]: # %load c08_islice.py
    ...: from pipe import islice
    ...:
    ...: data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    ...: v1 = list( data | islice(2, 8, 2))
    ...:
    ...: # v1
    ...:

 In [3]: v1
 Out[3]: [3, 5, 7]

 In [4]:
```

## izip()　指定した長さのタプルを生成
 `izip()` はn個の長さのタプルを生成します。ここでnは反復子 zip() の位置引数として渡される。
各タプルの i 番目の要素は   は zip() の i 番目のイテラルオブジェクトが使用されます。
strict が真で、引数の1つが先に使い果たされた場合は、 ValueError を発生させる。


```
 In [2]: # %load c07_izip.py
    ...: from pipe import izip
    ...:
    ...: v1 = list(zip('abcdefg', range(3), range(4)))
    ...:
    ...: # v1
    ...:

 In [3]: v1
 Out[3]: [('a', 0, 0), ('b', 1, 1), ('c', 2, 2)]

 In [4]:

```


## lstrip  文字列の先頭の空白文字を除去
 `lstrip(chars=None, /)`
python の組み込み関数の `lstrip()` と同じように、文字列の先頭の空白を除去したコピーを返します。 `chars` が与えられ、かつ  `None` でない場合、 `chars` に含まれる文字を代わりに削除します。


```
 In [2]: # %load c08_lstrip.py
    ...: from pipe import lstrip
    ...:
    ...:
    ...: v1 =  'abc   ' | lstrip
    ...: v2 = '.,[abc] ] ' | lstrip('.,[] ')
    ...:

 In [3]: v1
 Out[3]: 'abc   '

 In [4]: v2
 Out[4]: 'abc] ] '

 In [5]:

```

## map()  イテラブルオブジェクトに関数を適用
 `map()` はイテラブルオブジェクトのすべての要素に関数を適用してくれます。組み込み関数の  `map()` と似ていますが、受け取る引数が異なります。名前が同じことから混乱するようであれば、 `select()` を使うこともできます。



```
 In [2]: # %load c09_map_select.py
    ...: from pipe import select, map
    ...:
    ...: data = [1, 2, 3, 4, 5]
    ...: v1 = list( data | select(lambda x: x * 2) )
    ...: v2 = list( data | map(lambda x: x * 2) )
    ...:
    ...: # v1
    ...: # v2
    ...:

 In [3]: v1
 Out[3]: [2, 4, 6, 8, 10]

 In [4]: v2
 Out[4]: [2, 4, 6, 8, 10]

 In [5]:

```

 `map()` や  `filter()` という組み込み関数があるのに、同じ機能をもつ関数  `where()` や  `select()` が必要になるのは、
パイプが関数の結果を別の関数の入力として、後ろに追加することができるからです。パイプを使うことでネストした関数の括弧（ `(...)` ) を取り除くことができ、コードを読みやすくすることができます。( `c01_using_pipe.py` 参照)


## permutations()　可能なすべての並べ換えを返す
 `permutations()` は可能なすべての並べ換えを返します。


```
 In [2]: # %load c10_permutations.py
    ...: from pipe import permutations
    ...:
    ...: v1 = list('ABC' | permutations(2))
    ...: v2 = list(range(3) | permutations)
    ...:

 In [3]: v1
 Out[3]: [('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')]

 In [4]: v2
 Out[4]: [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]

 In [5]:

```


## reverse - リストを逆順にする
Pythonの組み込み関数  `reverse()` と同様に、リストを逆順にしたイテラルオブジェクトを返します。


```
 In [2]: # %load c11_reverse.py
    ...: from pipe import reverse
    ...:
    ...: data = [1, 2, 3, 4, 5]
    ...: v1 = list( data| reverse)
    ...:
    ...: # v1
    ...: # data
    ...:

 In [3]: v1
 Out[3]: [5, 4, 3, 2, 1]

 In [4]: data
 Out[4]: [1, 2, 3, 4, 5]

 In [5]:

```



## rstrip
 `lstrip(chars=None, /)`
python の組み込み関数の `rstrip()` と同じように、文字列の末尾の空白を除去したコピーを返します。 `chars` が与えられ、かつ  `None` でない場合、 `chars` に含まれる文字を代わりに削除します。


```
 In [2]: # %load c12_rstrip.py
    ...: from pipe import rstrip
    ...:
    ...:
    ...: v1 =  'abc   ' | rstrip
    ...: v2 = '.,[abc] ] ' | rstrip('.,[] ')
    ...:

 In [3]: v1
 Out[3]: 'abc'

 In [4]: v2
 Out[4]: '.,[abc'

 In [5]:

```


## select() イテラブルオブジェクトに関数を適用
 `select()` はイテラブルオブジェクトのすべての要素に関数を適用してくれます。組み込み関数の  `map()` と似ていますが、受け取る引数が異なります。組み込み関数の `map()` と同じ名前のパイプも提供されていますが、混乱するようであれば、 `select()` を使用するようにしてください。



## skip() 与えた数の要素だけスキップ
与えられたイテラルオブジェクトの要素から与えられた要素数をスキップしたコピーを返します。


```
 In [2]: # %load c13_skip.py
    ...: from pipe import skip
    ...:
    ...: data = [1, 2, 3, 4, 5]
    ...: v1 = list( data| skip(3))
    ...:
    ...: # v1
    ...: # data
    ...:

 In [3]: v1
 Out[3]: [4, 5]

 In [4]: data
 Out[4]: [1, 2, 3, 4, 5]

 In [5]:

```


## skip_while 与えた条件が真となる要素をスキップ
 `itertools.dropwhile()` のように、引数で与えた条件が真の間は与えられたイテラブルオブジェクトの要素をスキップし、その後、他の要素を返します。


```
 In [2]: # %load c14_skip_while.py
    ...: from pipe import skip_while
    ...:
    ...: data = [1, 2, 3, 4, 5]
    ...: v1 = list( data| skip_while(lambda x: x < 3))
    ...:
    ...: # v1
    ...:

 In [3]: v1
 Out[3]: [3, 4, 5]

 In [4]:

```

## sort()
 `sort(*, key=None, reverse=False)`
Pythonの組み込み関数の  `sort()` と同様に、与えたイテラルオブジェクトをインプレース(リスト自体が変更される)でソートしたものを返します。  `key` 関数が与えられた場合、それを各リスト項目に一度だけ適用してソートします。 `reverse=True` を与えると降順にソートします。


```
 In [2]: # %load c15_sort.py
    ...: from pipe import sort
    ...:
    ...: data = [1, 2, 3, -4, 5]
    ...: v1 = list( data| sort())
    ...: v2 = list( data| sort(reverse=True))
    ...: v3 = list( data| sort(key=abs))
    ...:
    ...: # v1
    ...: # v2
    ...: # v3
    ...:

 In [3]: v1
 Out[3]: [-4, 1, 2, 3, 5]

 In [4]: v2
 Out[4]: [5, 3, 2, 1, -4]

 In [5]: v3
 Out[5]: [1, 2, 3, -4, 5]

 In [6]:

```


## strip()
 `strip(chars=None, /)`
python の組み込み関数の `strip()` と同じように、文字列から空白を除去したコピーを返します。 `chars` が与えられ、かつ  `None` でない場合、 `chars` に含まれる文字を代わりに削除します。


```
 In [2]: # %load c16_strip.py
    ...: from pipe import strip
    ...:
    ...:
    ...: v1 =  'abc   ' | strip
    ...: v2 = '.,[abc] ] ' | strip('.,[] ')
    ...:

 In [3]: v1
 Out[3]: 'abc'

 In [4]: v2
 Out[4]: 'abc'

 In [5]:

```



## t() イテラルオブジェクトを結合する
Haskellの `:` 演算子のように右結合を行った結果を返します。


```
 In [2]: # %load c17_t.py
    ...: from pipe import t
    ...:
    ...: v1 = list( 0 | t(1) | t(2) )
    ...: v2 = list( 0 | t([1, 2]) | t([3, 4]) )
    ...:
    ...: # v1
    ...: # v2
    ...:

 In [3]: v1
 Out[3]: [0, 1, 2]

 In [4]: v2
 Out[4]: [0, [1, 2], [3, 4]]

 In [5]:

```


## tail()
与えられたイテラルオブジェクトの最後の要素から、指示された要素数を返します。


```
 In [2]: # %load c18_tail.py
    ...: from pipe import tail
    ...:
    ...: data = [1, 2, 3, 4, 5]
    ...: v1 = list( data| tail(3))
    ...:
    ...: # v1
    ...: # data
    ...:

 In [3]: v1
 Out[3]: [3, 4, 5]

 In [4]:

```

## take()　与えた数の要素だけ返す
与えられたイテラルオブジェクトの要素の先頭から与えられた要素数をを返します。

 pytohn
```
 In [2]: # %load c19_take.py
    ...: from pipe import take
    ...:
    ...: data = [1, 2, 3, 4, 5]
    ...: v1 = list( data| take(3))
    ...:
    ...: # v1
    ...:

 In [3]: v1
 Out[3]: [1, 2, 3]

 In [4]:

```

## take_while() 与えた条件が真となる要素を返す
 `itertools.takewhile()` のように、引数で与えた条件が真となるイテラブルオブジェクトの要素を返します。


```
 In [2]: # %load c20_take_while.py
    ...: from pipe import take_while
    ...:
    ...: data = [1, 2, 3, 4, 5]
    ...: v1 = list( data| take_while(lambda x: x<3))
    ...:
    ...: # v1
    ...:

 In [3]: v1
 Out[3]: [1, 2]

 In [4]:
```


## tee 標準出力への出力
tee は与えられたイテラルオブジェクトを変更せずに標準出力へ出力します。デバッグ時に使用されまうs。


```
 In [2]: # %load c21_tee.py
    ...: from pipe import tee
    ...:
    ...: data = [1, 2, 3, 4, 5]
    ...: v1 = sum( data | tee )
    ...:
    ...: # v1
    ...:
 1
 2
 3
 4
 5

 In [3]: v1
 Out[3]: 15

 In [4]:

```

## transpose() 転置行列を返す
転置行列（行列の列と行を入れ替えた要素）を返します。


```
 In [2]: # %load c22_transpose.py
    ...: from pipe import transpose
    ...:
    ...: data = [[1, 2, 3],
    ...:         [4, 5, 6],
    ...:         [7, 8, 9] ]
    ...: v1 = data | transpose
    ...:
    ...: # v1
    ...: # v1[0]
    ...: # v1[1]
    ...: # v1[2]
    ...:

 In [3]: v1
 Out[3]: [(1, 4, 7), (2, 5, 8), (3, 6, 9)]

 In [4]: v1[0]
 Out[4]: (1, 4, 7)

 In [5]: v1[1]
 Out[5]: (2, 5, 8)

 In [6]: v1[2]
 Out[6]: (3, 6, 9)

 In [7]:

```

## traverse - 再帰的にイテラブルシーケンスを展開する
 `traverse` は、イテラブルシーケンスを再帰的に展開することができます。 `traverse` を使えば、深くネストされたリストを簡単にフラットなリストにすることができます。


```
 In [2]: # %load c23_traverse.py
    ...: from pipe import traverse
    ...:
    ...: data = [[1, 2, [3]], [4, 5]]
    ...: v1 = list( data | traverse)
    ...:
    ...: # v1
    ...:

 In [3]: v1
 Out[3]: [1, 2, 3, 4, 5]

 In [4]:

```

冒頭で例示したように、これらの関数は組み合わせることができます。



```
 In [2]: # %load c23_select_traverse.py
    ...: from pipe import select, traverse
    ...:
    ...: # ABV: Alcohol by Volume (アルコール度数)
    ...: beers = [
    ...:     { 'name': 'Pale Ale', 'abv': [5.5, 6.0], 'stock': 6 },
    ...:     { 'name': 'ICHII SENSHIN', 'abv': 6.5, 'stock': 6 },
    ...:     { 'name': 'ICHIGO ICHIE', 'abv': 5.5, 'stock': 24 },
    ...:     { 'name': 'Pilserl', 'abv': 4.9, 'stock': 12 },
    ...: ]
    ...:
    ...: v1 = list( beers
    ...:              | select(lambda x: x["abv"])
    ...:              | traverse)
    ...:
    ...: # v1
    ...:

 In [3]: v1
 Out[3]: [5.5, 6.0, 6.5, 5.5, 4.9]

 In [4]:

```

## uniq() 連続した重複データを削除
 `dedup()` と似ていますが、連続した値のみを重複排除しjます。  `key` に関数が与えられている場合は、その関数を適用した結果で判断されます。


```
 In [2]: # %load c24_uniq.py
    ...: from pipe import uniq
    ...:
    ...: data = [1, 1, 2, 2, 3, 3, 2, 1, 2, 3]
    ...: v1 = list(data | uniq)
    ...: v2 = list(data | uniq(key=lambda x: x % 2))
    ...:
    ...: # v1
    ...: # v2
    ...:

 In [3]: v1
 Out[3]: [1, 2, 3, 2, 1, 2, 3]

 In [4]: v2
 Out[4]: [1, 2, 3, 2, 1, 2, 3]

 In [5]:

```

## where() イテレート可能な要素をフィルタリング
 `where()` はPythonの組み込み関数  `filter()` と同様に、イテレート可能な要素のフィルタリングしてくれます。反復処理可能な要素をフィルタリングするために使用することができます。


```
 In [2]: # %load c25_where.py
    ...: from pipe import where
    ...:
    ...: data = [1, 2, 3, 4, 5]
    ...: v1 = list(data | where(lambda x: x % 2 == 0))
    ...:
    ...: # v1
    ...:

 In [3]: v1
 Out[3]: [2, 4]

 In [4]:

```


## 独自のパイプを作成する
Pipeクラスを `lambda` で初期化したものを使って独自のパイプを作成することができます。


```
 In [2]: # %load c26_custom_pipe.py
    ...: from pipe import Pipe
    ...:
    ...: first = Pipe(lambda iterable: next(iter(iterable)))
    ...: v1 = [1, 2, 3] | first
    ...:
    ...: # v1
    ...:

 In [3]: v1
 Out[3]: 1

 In [4]:

```


あるいは、 `@Pipe` デコレーターを使用して関数で実装することもできます。


```
 In [2]: # %load c27_custom_pipe_decorator.py
    ...: from pipe import Pipe
    ...:
    ...: @Pipe
    ...: def first(x):
    ...:     return next(iter(x))
    ...:
    ...: v1 = [1, 2, 3] | first
    ...:
    ...: # v1
    ...:

 In [3]: v1
 Out[3]: 1

 In [4]:

```


## 遅延評価
Pipe モジュールを使うと、2つのレベルで遅延評価を行うことができます。

- パイプラインで得られたオブジェクトはジェネレータであり、必要な場合にのみ評価されます。
- 一連のパイプコマンドの中で、実際に必要とされる要素のみが評価されます。



```
 In [2]: # %load c30_lazy_evaluation.py
    ...: from itertools import count
    ...: from pipe import select, where, take
    ...:
    ...: def dummy_func(x):
    ...:     print(f"processing at value {x}")
    ...:     return x
    ...:
    ...: print("----- test using a generator as input -----")
    ...:
    ...: print(f"we are feeding in a: {type(count(100))}")
    ...:
    ...: res_with_count = (count(100) | select(dummy_func)
    ...:                              | where(lambda x: x % 2 == 0)
    ...:                              | take(2))
    ...:
    ...: print(f"the resulting object is: {res_with_count}")
    ...: print(f"when we force evaluation we get:")
    ...: print(f"{list(res_with_count)}")
    ...:
    ...: print("----- test using a list as input -----")
    ...:
    ...: list_to_100 = list(range(100))
    ...: print(f"we are feeding in a: {type(list_to_100)} which has length {len(list_to_100)}")
    ...:
    ...: res_with_list = (list_to_100 | select(dummy_func)
    ...:                              | where(lambda x: x % 2 == 0)
    ...:                              | take(2))
    ...:
    ...: print(f"the resulting object is: {res_with_list}")
    ...: print(f"when we force evaluation we get:")
    ...: print(f"{list(res_with_list)}")
    ...:
 ----- test using a generator as input -----
 we are feeding in a: <class 'itertools.count'>
 the resulting object is: <generator object take at 0x107a62650>
 when we force evaluation we get:
 processing at value 100
 processing at value 101
 processing at value 102
 processing at value 103
 processing at value 104
 [100, 102]
 ----- test using a list as input -----
 we are feeding in a: <class 'list'> which has length 100
 the resulting object is: <generator object take at 0x107a625e0>
 when we force evaluation we get:
 processing at value 0
 processing at value 1
 processing at value 2
 processing at value 3
 processing at value 4
 [0, 2]

 In [3]:

```



## サンプル
サンプルとして[オイラープロジェクト ](https://projecteuler.net/about) の問題について、解法をPipeで実装してみます。

## EX1
[問題1 ](https://projecteuler.net/problem=1) は、1000以下の3または5の倍数の合計を求めよというもの。

単純に forループで実装すると次のようになるでしょう。


```
 In [2]: # %load c40_euler_ex1_simple.py
    ...: euler1 = 0
    ...: for i in range(1000):
    ...:     if i % 3 == 0 or i % 5 == 0:
    ...:         euler1 += i
    ...:
    ...: assert euler1 == 233168
    ...:

 In [3]:
```

リスト内包表記を使って記述すると次のようになります。


```
 In [2]: # %load c40_euler_ex1_lambda.py
    ...: max_num = 1000
    ...: mul_3_5 = [i for i in range(1,max_num) if i % 3 == 0 or i % 5 == 0]
    ...: euler1 = sum(mul_3_5)
    ...: assert euler1 == 233168
    ...:

 In [3]:
```

今度は、Pipe を使うと次のように記述することができます。


```
 In [2]: # %load c40_euler_ex1.py
    ...: import itertools
    ...: from pipe import select, take_while
    ...:
    ...: euler1 = (
    ...:     sum(itertools.count()
    ...:         | select(lambda x: x * 3)
    ...:         | take_while(lambda x: x < 1000))
    ...:     + sum(itertools.count()
    ...:         | select(lambda x: x * 5)
    ...:         | take_while(lambda x: x < 1000))
    ...:     - sum(itertools.count()
    ...:         | select(lambda x: x * 15)
    ...:         | take_while(lambda x: x < 1000))
    ...: )
    ...:
    ...: assert euler1 == 233168
    ...:

 In [3]:

```

この問題自体はやさしいのでPipeで実装したものが一番コード量が多くなっていますが、ロジックは単純になります。


## EX2
[問題2 ](https://projecteuler.net/problem=2) は、フィボナッチ数列の項の値が400万以下の, 偶数値の項の総和を求めよとうもの。

これも単純にコードすると次のようになります。


```
 In [2]: # %load c41_euler_ex2_simple.py
    ...: num1 = 0
    ...: num2 = 1
    ...:
    ...: max_num = 400_0000
    ...: euler2 = 0
    ...:
    ...: while(True):
    ...:     num_tmp = num2
    ...:     num2 += num1
    ...:     num1 = num_tmp
    ...:     if num2 > max_num:
    ...:         break
    ...:     if num2 % 2 == 0:
    ...:         euler2 += num2
    ...:
    ...: assert euler2 == 4613732
    ...:

 In [3]:

```


これを Pipe を使って実装すると次のようになります。


```
 In [2]: # %load c41_euler_ex2.py
    ...: from pipe import where, take_while
    ...:
    ...: def fib(n):
    ...:     a, b = 0, 1
    ...:     for _ in range(n):
    ...:         yield a
    ...:         a, b = b, a + b
    ...:
    ...: euler2 = sum(fib(100)
    ...:              | where(lambda x: x % 2 == 0)
    ...:              | take_while(lambda x: x < 400_0000))
    ...:
    ...: assert euler2 == 4613732
    ...:

 In [3]:

```


## まとめ

イテラルオブジェクトを処理するとき、for 文を避けるためのリスト内包表記を使うことがあります。これは、慣れていないと混乱しがちで保守がしずらいものでしたPiipeモジュールを使うことで、こうした処理を簡潔に記述できるようになり、コードの可読性が高まり保守しやすいコードになります。
ただし、オーバーヘッドがあることには注意してください。リスト内包表記だけで実装するものがもっとも性能がよくなります。


## 参考
- Pipe
  - [PyPI - Pipe ](https://pypi.org/project/pipe/)
  - [ソースコード ](https://github.com/JulienPalard/Pipe)
