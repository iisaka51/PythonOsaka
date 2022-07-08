Fncを使って効率良くデータを操作してみよう
=================
## はじめに
類似のライブラリにはPydash があります。比較しやすいように、この資料のサンプルは "[Pydashを使って効率良くデータを操作してみよう](https://github.com/iisaka51/PythonOsaka/tree/main/Tutorials/Tutorial.Pydash)" とできるだけ同じ内容としています。

# Fnc について

[Fnc ](https://pypi.python.org/pypi/fnc/)は、辞書の探索、変換、集計のための多くの便利な関数を備えています。次のような特徴を持っています。

  - ジェネレータで動作し、ジェネレータを返す関数型メソッド
    - メモリ効率がよく大規模データでも処理できる
  - ショートハンドレッドスタイルのイテレート（コールバック）機能
    - データのフィルタリングやマッピングを簡単に行ことができる
  - ネストされたデータ構造を参照するための文字列オブジェクトパスのサポート
  - 100%のテストカバレッジ
  - Python 3.6+に対応


## インストール
pydash は　次のようにインストールすることができます。


 bash
```
 # Linux or MacOS
 $ python -m pip install fnc
```

 command
```
 # Windows
 $  py -3 -m pip install fnc
```


## 機能の概要紹介
まずはどんなことができるかを一覧してみましょう。


```
 In [2]: # %load c01_quickstart.py
    ...: import fnc
    ...:
    ...: # Arrays
    ...:
    ...: data = [1, 2, [3, [4, 5, [6, 7]]]]
    ...: v1 = fnc.sequences.flatten(data)
    ...: assert list(v1) == [1, 2, 3, [4, 5, [6, 7]]]
    ...:
    ...: v2 = fnc.sequences.flattendeep(data)
    ...: assert list(v2) == [1, 2, 3, 4, 5, 6, 7]
    ...:
    ...: # Collections
    ...: data = [
    ...:    {'name': 'moe', 'age': 40},
    ...:    {'name': 'larry', 'age': 50},
    ...:    ]
    ...:
    ...: v3 =  fnc.map('name', data)
    ...: assert list(v3) == ['moe', 'larry']
    ...:
    ...: ## Functions
    ...: curried = fnc.iteratee(lambda a, b, c: a + b + c)
    ...: v4 = curried(1, 2, 3)
    ...: assert v4 == 6
    ...:
    ...: # Objects
    ...: data = {'name': 'moe', 'age': 40}
    ...: v5 = fnc.mappings.pick(['age'], data)
    ...: assert v5 == {'age': 40}
    ...: v6 = fnc.mappings.omit(['age'], data)
    ...: assert v6 == {'name': 'moe'}
    ...:
    ...: # Utilities
    ...: v7 = list()
    ...: @fnc.retry(attempts=3, delay=0)
    ...: def do_something(seq):
    ...:     seq.append(len(seq))
    ...:     raise Exceptions('retry count exceeded')
    ...:
    ...: try: do_something(v7)
    ...: except Exception: pass
    ...: assert v7 == [0, 1, 2]
    ...:
    ...: # Compose as like as Chaining
    ...: data = [1, 2, 3, 4]
    ...: from functools import partial
    ...: do_without = partial(fnc.sequences.without, [2, 3])
    ...: do_reject = partial(fnc.sequences.reject, lambda x: x > 1)
    ...: do_without_reject = fnc.compose(
    ...:      do_without,
    ...:      do_reject
    ...:      )
    ...: v8 = do_without_reject(data)
    ...: assert list(v8) == [1]
    ...:

 In [3]:

```

fnc は処理結果をジェネレーターで返すため、メソッドチェーンはできないのですが、 `fnc.compose()` をfunctools.partial と組み合わせることで登録した一連の処理を連続して処理させることができます。


## リスト操作

 `flatten()` でネストされているリストを一段階展開にします。 `flattendeep()` では全ての階層を展開します。


```
 In [2]: # %load c03_flatten.py
    ...: import fnc
    ...:
    ...: data = [[1, 2], [3, [4, 5]]]
    ...:
    ...: v1 = fnc.sequences.flatten(data)
    ...: v2 = fnc.sequences.flattendeep(data)
    ...:
    ...: # list(v1)
    ...: # list(v2)
    ...:

 In [3]: list(v1)
 Out[3]: [1, 2, 3, [4, 5]]

 In [4]: list(v2)
 Out[4]: [1, 2, 3, 4, 5]

 In [5]:

```

 `chunk()` を実行すると与えた要素数のまとめたリストを返すジェネレータを返します。


```
 In [2]: # %load c04_chunk.py
    ...: import fnc
    ...:
    ...: data = [1, 2, 3, 4, 5]
    ...: v1 = fnc.sequences.chunk(2, data)
    ...: v2 = fnc.sequences.chunk(3, data)
    ...:
    ...: # list(v1)
    ...: # list(v2)
    ...:

 In [3]: list(v1)
 Out[3]: [[1, 2], [3, 4], [5]]

 In [4]: list(v2)
 Out[4]: [[1, 2, 3], [4, 5]]

 In [5]:

```

## 辞書の操作

### omit()  辞書の属性を削除 / pick() 指定した辞書の属性を取得
 `fnc.mappings.omit()` を呼び出すと、辞書の属性を削除することができます。 `fnc.mappings.pick()` を呼び出すと指定したキーで構成される辞書を返します。


```
 In [2]: # %load c05_dict_omit.py
    ...: import fnc
    ...:
    ...: data = { 'name': 'Pale Ale', 'abv': 5.5, 'stock': 6 }
    ...:
    ...: v1 = fnc.mappings.pick(["name"], data)
    ...: v2 = fnc.mappings.omit(["abv"], data)
    ...:
    ...: # v1
    ...: # v2
    ...:

 In [3]: v1
 Out[3]: {'name': 'Pale Ale'}

 In [4]: v2
 Out[4]: {'name': 'Pale Ale', 'stock': 6}

 In [5]:

```

### get()  ネストした辞書の属性を取得する
以下のようなネストされた辞書の、 `"swap"` の値を取得するとしたときなど、辞書のキーを文字列として一度に与えるだけでその値を取得することができます。



```
 In [2]: # %load c06_nested_dict.py
    ...: import fnc
    ...:
    ...: forex = {
    ...:     "mxnjpy": {
    ...:         "long": {"open": {"lots": 10000, "swap": 8}},
    ...:         "short": {"open": {"lots": 2000, "swap": -24}},
    ...:     }
    ...: }
    ...:
    ...: v1 = forex["mxnjpy"]["long"]["open"]["swap"]
    ...:
    ...: v2 = fnc.mappings.get("mxnjpy.long.open.swap", forex)
    ...:
    ...: # v1
    ...: # v2
    ...:

 In [3]: v1
 Out[3]: 8

 In [4]: v2
 Out[4]: 8

 In [5]:

```


### find_index() 　辞書のリスト内の要素のインデックスを取得
 `find_index()` 関数を使って辞書のリスト内の要素のインデックスを取得することができます。複数存在する場合は最初に見つかったインデックスを返し、ミケられなかった場合は  `-1` が返されます。


```
 In [2]: # %load c07_dict_find_index.py
    ...: import fnc
    ...:
    ...: beers = [
    ...:     { 'name': 'Pale Ale', 'abv': 5.5, 'stock': 6 },
    ...:     { 'name': 'Pale Ale', 'abv': 6.0, 'stock': 0 },
    ...:     { 'name': 'ICHII SENSHIN', 'abv': 6.5, 'stock': 6 },
    ...:     { 'name': 'ICHIGO ICHIE', 'abv': 5.5, 'stock': 24 },
    ...:     { 'name': 'Pilserl', 'abv': 4.9, 'stock': 12 },
    ...: ]
    ...:
    ...: pilserl = lambda x: x["name"] == "Pilserl"
    ...: paleale = lambda x: x["name"] == "Pale Ale"
    ...: yebisu = lambda x: x["name"] == "YEBISU"
    ...: v1 = fnc.sequences.findindex(pilserl, beers)
    ...: v2 = fnc.sequences.findindex(paleale, beers)
    ...: v3 = fnc.sequences.findindex(yebisu, beers)
    ...:
    ...: # v1
    ...: # v2
    ...: # v3
    ...:

 In [3]: v1
 Out[3]: 4

 In [4]: v2
 Out[4]: 0

 In [5]: v3
 Out[5]: -1

 In [6]:

```

### パターンに合致するオブジェクトを検索
 `fnc.sequences.filter()` メソッドは、特定のパターンにマッチするオブジェクトのリスト内のアイテムを取得するジェネレーターを返します。


```
 In [2]: # %load c08_dict_find_val.py
    ...: import fnc
    ...:
    ...: beers = [
    ...:     { 'name': 'Pale Ale', 'abv': 5.5, 'stock': 6 },
    ...:     { 'name': 'Pale Ale', 'abv': 6.0, 'stock': 0 },
    ...:     { 'name': 'ICHII SENSHIN', 'abv': 6.5, 'stock': 6 },
    ...:     { 'name': 'ICHIGO ICHIE', 'abv': 5.5, 'stock': 24 },
    ...:     { 'name': 'Pilserl', 'abv': 4.9, 'stock': 12 },
    ...: ]
    ...:
    ...: v1 = fnc.sequences.filter({"name": "Pilserl"}, beers )
    ...: v2 = fnc.sequences.filter({"name": "Pale Ale"}, beers )
    ...: v3 = fnc.sequences.filter({"name": "YEBISU"}, beers )
    ...:
    ...: # list(v1)
    ...: # list(v2)
    ...: # list(v3)
    ...:

 In [3]: list(v1)
 Out[3]: [{'name': 'Pilserl', 'abv': 4.9, 'stock': 12}]

 In [4]: list(v2)
 Out[4]:
 [{'name': 'Pale Ale', 'abv': 5.5, 'stock': 6},
  {'name': 'Pale Ale', 'abv': 6.0, 'stock': 0}]

 In [5]: list(v3)
 Out[5]: []

 In [6]:

```

 `fnc.sequences.find()` では最初にパターンに合致するオブジェクトを返します。


```
 In [2]: # %load c07_dict_find.py
    ...: import fnc
    ...:
    ...: beers = [
    ...:     { 'name': 'Pale Ale', 'abv': 5.5, 'stock': 6 },
    ...:     { 'name': 'Pale Ale', 'abv': 6.0, 'stock': 0 },
    ...:     { 'name': 'ICHII SENSHIN', 'abv': 6.5, 'stock': 6 },
    ...:     { 'name': 'ICHIGO ICHIE', 'abv': 5.5, 'stock': 24 },
    ...:     { 'name': 'Pilserl', 'abv': 4.9, 'stock': 12 },
    ...: ]
    ...:
    ...: v1 = fnc.sequences.find({"name": "Pilserl"}, beers)
    ...: v2 = fnc.sequences.find({"name": "Pale Ale"}, beers)
    ...: v3 = fnc.sequences.find({"name": "YEBISU"}, beers)
    ...:
    ...: # v1
    ...: # v2
    ...: # v3
    ...:

 In [3]: v1
 Out[3]: {'name': 'Pilserl', 'abv': 4.9, 'stock': 12}

 In [4]: v2
 Out[4]: {'name': 'Pale Ale', 'abv': 5.5, 'stock': 6}

 In [5]: v3

 In [6]: v3 is None
 Out[6]: True

 In [7]:
```


### map_()  ネストしたオブジェクトの値を取得
辞書のリストは、以下のように入れ子になっていることがあります。この場合で"abv"(アルコール度数) の値を取得するときは、 `map_()` メソッドを使用することができます。



```
 In [2]: # %load c09_get_nested_objval.py
    ...: import fnc
    ...:
    ...: beers = [
    ...:     { 'name': 'Pale Ale',
    ...:       'attributes': { 'abv': 6.0, 'stock': 0 }},
    ...:     { 'name': 'ICHII SENSHIN',
    ...:       'attributes': { 'abv': 6.5, 'stock': 6 }},
    ...:     { 'name': 'ICHIGO ICHIE',
    ...:       'attributes': { 'abv': 5.5, 'stock': 24 }},
    ...:     { 'name': 'Pilserl',
    ...:       'attributes': { 'abv': 4.9, 'stock': 12 }},
    ...: ]
    ...:
    ...: v1 = fnc.map("attributes.abv", beers)
    ...:
    ...: # list(v1)
    ...:

 In [3]: list(v1)
 Out[3]: [6.0, 6.5, 5.5, 4.9]

 In [4]:

```


## 関数操作

### 関数をN回実行する
 `fnc.retry()` デコレーターを使用すると、関数を指定した回数実行することができます。このとき遅延(delay)させることもできます。



```
 In [2]: # %load c10_times.py
    ...: import fnc
    ...:
    ...: BEER = 0
    ...: @fnc.retry(attempts=4, delay=2)
    ...: def drink_beers():
    ...:     global BEER
    ...:     BEER += 1
    ...:     print(f'I drink {BEER} paint of beers')
    ...:     raise Exceptions('retry count exceeded')
    ...:
    ...: try:
    ...:     drink_beers()
    ...: except Exception:
    ...:     pass
    ...:
 I drink 1 paint of beers
 I drink 2 paint of beers
 I drink 3 paint of beers
 I drink 4 paint of beers

 In [3]:

```


## 登録した複数の処理をオブジェクトに適用
あるオブジェクトにfncのいくつかのメソッドを適用したいことがあります。 `fnc.compose()` と functools.partial を組み合わせると、一連の連続した処理をオブジェクトに適用させることができます。メソッドチェーンの代用として使うことができます。


```
 In [2]: # %load c11_chaining.py
    ...: import fnc
    ...: from functools import partial
    ...:
    ...: beers = [ "Pale Ale", "ICHI SENSHIN", "ICHIGO ICHIE", "Pilserl" ]
    ...:
    ...: do_without_paleale = partial(fnc.sequences.without,
    ...:                             ["Pale Ale"])
    ...: do_reject_start_p = partial(fnc.sequences.reject,
    ...:                             lambda x: x.startswith("P"))
    ...:
    ...: do_choice_beers = fnc.compose(
    ...:      do_without_paleale,
    ...:      do_reject_start_p,
    ...:      )
    ...: v1 = do_choice_beers(beers)
    ...:
    ...: # list(v1)
    ...:

 In [3]: list(v1)
 Out[3]: ['ICHI SENSHIN', 'ICHIGO ICHIE']

 In [4]:
```


## カスタマイズされたメソッド
pydashのメソッドではなく、独自のメソッドを使いたい場合は、 `map()` メソッドを使用します。 `.map_()` と間違いやすいので注意してください。



```
 In [2]: # %load c12_custom_methods.py
    ...: import pydash as py_
    ...:
    ...: beers = [
    ...:     { 'name': 'Pale Ale', 'abv': 5.5, 'stock': 6 },
    ...:     { 'name': 'Pilserl', 'abv': 4.9, 'stock': 12 },
    ...: ]
    ...:
    ...: def get_abv(beer):
    ...:    v =  py_.get(beer, "abv")
    ...:    return beer["abv"]
    ...:
    ...:
    ...: v1 = ( py_.chain(beers)
    ...:        .map(get_abv)
    ...:        .sum()
    ...:      )
    ...:
    ...: # v1
    ...: # v1.value()
    ...:

 In [3]: v1
 Out[3]: <pydash.chaining.Chain at 0x104a1a080>

 In [4]: v1.value()
 Out[4]: 10.4

 In [5]:

```



## まとめ
fnc を使ってPythonのオブジェクトを効率的に操作することができます。fnc では処理結果をジェネレーターで返すため大規模データでも処理することができるようになります。　他にもたくさんの機能があるため、詳細はfncの[APIリファレンス ](https://fnc.readthedocs.io/en/latest/index.html) を参照するようにしてください。


## 参考
- fnc
  - [PyPI - fnc ](https://pypi.org/project/fnc/)
  - [ソースコード　](https://github.com/dgilland/fnc)
  - [ドキュメント　](https://fnc.readthedocs.io)
- Pydash
  - [PyPI - pydash ](https://pypi.python.org/pypi/pydash/)
