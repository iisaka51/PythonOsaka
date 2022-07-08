Pydashを使って効率良くデータを操作してみよう
=================

# Pydash について

[Pydash  https://pypi.python.org/pypi/pydash/]は、NodeJS でよく知られている [Lodash ](https://lodash.com/) をPythonにポーティングしたライブラリです。辞書の探索、変換、集計のための多くの便利な関数を備えています。データの抽出、リストの平坦化、必要なフォーマットへの変換なども簡単なコードで記述することができるなど、非常に多機能で使いやすいモジュールになっています。


## インストール
pydash は　次のようにインストールすることができます。


 bash
```
 # Linux or MacOS
 $ python -m pip install pydash
```

 command
```
 # Windows
 $  py -3 -m pip install pydash
```


## 機能の概要紹介
まずはどんなことができるかを一覧してみましょう。


```
 In [2]: # %load c01_quickstart.py
    ...: import pydash as py_
    ...:
    ...: # Arrays
    ...:
    ...: data = [1, 2, [3, [4, 5, [6, 7]]]]
    ...: v1 = py_.flatten(data)
    ...: assert v1 == [1, 2, 3, [4, 5, [6, 7]]]
    ...:
    ...: v2 = py_.flatten_deep(data)
    ...: assert v2 == [1, 2, 3, 4, 5, 6, 7]
    ...:
    ...: # Collections
    ...: data = [
    ...:    {'name': 'moe', 'age': 40},
    ...:    {'name': 'larry', 'age': 50},
    ...:    ]
    ...:
    ...: v3 =  py_.map_(data, 'name')
    ...: assert v3 == ['moe', 'larry']
    ...:
    ...: # Functions
    ...: curried = py_.curry(lambda a, b, c: a + b + c)
    ...: v4 = curried(1, 2)(3)
    ...: assert v4 == 6
    ...:
    ...: # Objects
    ...: data = {'name': 'moe', 'age': 40}
    ...: v5 = py_.omit(data, 'age')
    ...: assert v5 == {'name': 'moe'}
    ...:
    ...: # Utilities
    ...: v6 = py_.times(3, lambda index: index)
    ...: assert v6 == [0, 1, 2]
    ...:
    ...: # Chaining
    ...: v7 = ( py_.chain([1, 2, 3, 4])
    ...:        .without(2, 3)
    ...:        .reject(lambda x: x > 1)
    ...:        .value() )
    ...: assert v7 == [1]
    ...:
 
 In [3]:
```



## リスト操作

 `flatten()` でネストされているリストを一段階展開します。 `flatten_deep()` では全ての階層を展開します。


```
 In [2]: # %load c03_flatten.py
    ...: import pydash as py_
    ...:
    ...: data = [[1, 2], [3, [4, 5]]]
    ...:
    ...: v1 = py_.flatten(data)
    ...: v2 = py_.flatten_deep(data)
    ...:
    ...: # v1
    ...: # v2
    ...:
 
 In [3]: v1
 Out[3]: [1, 2, 3, [4, 5]]
 
 In [4]: v2
 Out[4]: [1, 2, 3, 4, 5]
 
 In [5]:
 
```

 `chunk()` を実行すると与えた要素数のまとめたリストを返します。


```
 In [2]: # %load c04_chunk.py
    ...: import pydash as py_
    ...:
    ...: data = [1, 2, 3, 4, 5]
    ...: v1 = py_.chunk(data, 2)
    ...: v2 = py_.chunk(data, 3)
    ...:
    ...: # v1
    ...: # v2
    ...:
 
 In [3]: v1
 Out[3]: [[1, 2], [3, 4], [5]]
 
 In [4]: v2
 Out[4]: [[1, 2, 3], [4, 5]]
 
 In [5]:
 
```

## 辞書の操作

### omit()  辞書の属性を削除
 `py_.omit()` を呼び出すと、辞書の属性を削除することができます。


```
 In [2]: # %load c05_dict_omit.py
    ...: import pydash as py_
    ...:
    ...: data = { 'name': 'Pale Ale', 'abv': 5.5, 'stock': 6 }
    ...:
    ...: v1 = py_.omit(data, "name")
    ...:
    ...: # v1
    ...:
 
 In [3]: v1
 Out[3]: {'abv': 5.5, 'stock': 6}
 
 In [4]:
 
```

### get()  ネストした辞書の属性を取得する
以下のようなネストされた辞書の、 `"swap"` の値を取得するとしたときなど、辞書のキーを文字列として一度に与えるだけでその値を取得することができます。



```
 In [2]: # %load c06_nested_dict.py
    ...: import pydash as py_
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
    ...: v2 = py_.get(forex, "mxnjpy.long.open.swap")
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
 `find_index()` 関数を使って辞書のリスト内の要素のインデックスを取得することができます。


```
 In [2]: # %load c07_list_dict.py
    ...: import pydash as py_
    ...:
    ...: beers = [
    ...:     { 'name': 'Pale Ale', 'abv': 5.5, 'stock': 6 },
    ...:     { 'name': 'Pale Ale', 'abv': 6.0, 'stock': 0 },
    ...:     { 'name': 'ICHII SENSHIN', 'abv': 6.5, 'stock': 6 },
    ...:     { 'name': 'ICHIGO ICHIE', 'abv': 5.5, 'stock': 24 },
    ...:     { 'name': 'Pilserl', 'abv': 4.9, 'stock': 12 },
    ...: ]
    ...:
    ...: filter_beer = lambda x: x["name"] == "Pilserl"
    ...: v1 = py_.find_index(beers, filter_beer)
    ...:
    ...: # v1
    ...:
    ...:
 
 In [3]: v1
 Out[3]: 4
 
 In [4]:
```

### filter_() パターンに合致するオブジェクトを検索
 `py_.filter_()` メソッドを使用すると、特定のパターンにマッチするオブジェクトのリスト内のアイテムを取得することができます。 `filter_()` は組み込み関数の  `filter()` と競合するためアンダースコア( `_` )が付加されていることに注意してください。


```
 In [2]: # %load c08_dict_find_val.py
    ...: import pydash as py_
    ...:
    ...: beers = [
    ...:     { 'name': 'Pale Ale', 'abv': 5.5, 'stock': 6 },
    ...:     { 'name': 'Pale Ale', 'abv': 6.0, 'stock': 0 },
    ...:     { 'name': 'ICHII SENSHIN', 'abv': 6.5, 'stock': 6 },
    ...:     { 'name': 'ICHIGO ICHIE', 'abv': 5.5, 'stock': 24 },
    ...:     { 'name': 'Pilserl', 'abv': 4.9, 'stock': 12 },
    ...: ]
    ...:
    ...: v1 = py_.filter_(beers, {"name": "Pilserl"} )
    ...:
    ...: # v1
    ...:
    ...:
 
 In [3]: v1
 Out[3]: [{'name': 'Pilserl', 'abv': 4.9, 'stock': 12}]
 
 In [4]:
```


### map_()  ネストしたオブジェクトの値を取得
辞書のリストは、以下のように入れ子になっていることがあります。この場合で"abv"(アルコール度数) の値を取得するときは、 `map_()` メソッドを使用することができます。



```
 In [2]: # %load c09_get_nested_objval.py
    ...: import pydash as py_
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
    ...: v1 = py_.map_(beers, "attributes.abv" )
    ...:
    ...: # v1
    ...:
    ...:
 
 In [3]: v1
 Out[3]: [6.0, 6.5, 5.5, 4.9]
 
 In [4]:
 
```


## 関数操作

### 関数をN回実行する
 `py_.times()` メソッドを使用すると、関数をN回実行することができます。このメソッドは for ループの良い代替手段です。



```
 In [2]: # %load c10_times.py
    ...: import pydash as py_
    ...:
    ...: py_.times(4, lambda n: f'I drink {n+1} paint of beers')
    ...:
 Out[2]:
 ['I drink 1 paint of beers',
  'I drink 2 paint of beers',
  'I drink 3 paint of beers',
  'I drink 4 paint of beers']
 
 In [3]:
 
```


## chain()  メソッドチェーン
あるオブジェクトにPydashのいくつかのメソッドを適用したいことがあります。何行もコードを書く代わりに、メソッドチェーンで連結させて実行することができます。
オブジェクトにメソッドチェインを適用するには、 `py_.chain()` メソッドを使用します。


```
 In [2]: # %load c11_chaining.py
    ...: import pydash as py_
    ...:
    ...: beers = [ "Pale Ale", "ICHI SENSHIN", "ICHIGO ICHIE", "Pilserl" ]
    ...:
    ...: v1 = ( py_.chain(beers)
    ...:        .without("Pale Ale")
    ...:        .reject(lambda x: x.startswith("P"))
    ...:      )
    ...:
    ...: v2 = ( py_.chain(beers)
    ...:        .without("Pale Ale")
    ...:        .reject(lambda x: x.startswith("P"))
    ...:        .value()
    ...:      )
    ...:
    ...: v3 = v1.value()
    ...:
    ...: # v1
    ...: # v2
    ...: # v3
    ...:
    ...:
 
 In [3]: v1
 Out[3]: <pydash.chaining.Chain at 0x1100f79a0>
 
 In [4]: v2
 Out[4]: ['ICHI SENSHIN', 'ICHIGO ICHIE']
 
 In [5]: v3
 Out[5]: ['ICHI SENSHIN', 'ICHIGO ICHIE']
 
 In [6]:
```

メソッドチェーンの末尾に  `.value()` を追加して初めて、最終的な値がえられることに注意してください。
pydash では遅延評価がされていて、値が必要になるまで式の評価を保持し、評価の繰り返しを避けるようになっています。


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


### plant()  値の置き換え
チェーンの初期値を別の値で置き換えるには、 `plant()` メソッドを使用します。



```
 In [6]: # %load c13_plant.py
    ...: from c12_custom_methods import v1
    ...:
    ...: kyoto_brewery = [
    ...:     { 'name': 'ICHII SENSHIN', 'abv': 6.5, 'stock': 6 },
    ...:     { 'name': 'ICHIGO ICHIE', 'abv': 5.5, 'stock': 24 },
    ...: ]
    ...:
    ...: v2 = v1.plant(kyoto_brewery).value()
    ...:
    ...: # v2
    ...:
 
 In [7]: v2
 Out[7]: 12.0
 
 In [8]:
 
```

このコードの　 `v1` は   `c12_custom_methods.py` で定義したメソッドチェーンです。この入力を  `kyoto_brewery` で置き換えたわけです。


## まとめ
pydashを使ってPythonのオブジェクトを効率的に操作することができます。pydash　にはたくさんの機能があるため、詳細はpydashの[APIリファレンス ](https://pydash.readthedocs.io/en/latest/api.html?highlight=find_index#pydash.arrays.find_index) を参照するようにしてください。


## 余談

pydash は Lodash からのポーティングをすることから生まれたプロジェクトです。オブジェクト操作で、よりメモリ効率が良く、大規模なデータセットに適したライブラリが必要なら fnc も検討する価値はあるはず。

pydash はPlotly を使った可視化ライブラリ　Dash とは何の関連性もありませんが、リストや辞書などの操作をする上では、おっても利用価値があると考えています。

同様に pydash とは何の関連性もありませんが、ほぼ同名のプロジェクトが存在しています。

- [pyDash ](https://gitlab.com/k3oni/pydash) は Django で実装された Linux のシステムモニタリングダッシュボード
- [pyDash ](https://github.com/mfcaetano/pydash) は適応型ストリーミングビデオアルゴリズム研究のためのフレームワークに基づく教育ツールです。

## 参考
- Pydash
  - [PyPI - pydash ](https://pypi.python.org/pypi/pydash/)
  - [ソースコード  ](https://github.com/dgilland/pydash)
  - [公式ドキュメント http://pydash.readthedocs.org]
- fnc
  - [PyPI - fnc ](https://pypi.org/project/fnc/)
- Lodash
  - [オフィシャルサイト ](https://lodash.com/)



