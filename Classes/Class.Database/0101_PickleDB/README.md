pickleDBを使ってみよう
=================
## pickleDBについて
pickleDBは、[redis ](https://redis.io/) に影響を受けたシンプルで軽量なデータストアです。データをキー・バリュー・ストアとして保存します。SimpleJSONというPythonモジュールをベースにしていて、開発者は**JSON（JavaScript Object Notation）** フォーマットのデータをシンプルかつ高速に扱うことができます。SimpleJSONは、依存関係がないPythonだけで実装されたモジュールで、エンコーダおよびデコーダとして機能します。

## インストール
pickledb は拡張モジュールなので、次のようにインストールします。

 bash
```
 $ pip install pickledb
```

pickleDBという名前は、pickleというPythonのモジュールに触発されたもので、pickleDBの以前のバージョンで pickle が使用されていました。pickleDBの今のバージョンではSimpleJSONモジュールが使われるようになりましたが、pickleという名前は残されました。

## 基本的な使用方法

データに接続するためみは  `load()` メソッドを使ってファイル名を与えます。


```
 In [2]: # %load 01_connection.py
    ...: import pickledb
    ...:
    ...: db = pickledb.load('example.db', False)
    ...:
```


キー・バリュー・ストアとしてアクセスするので、 `set()` と `get()` および `dump()` を使ってアクセスします。

```
 In [4]: # %load 02_set.py
    ...: db.set('key', 'value')
    ...:
 Out[4]: True
 
 In [6]: # %load 03_get.py
    ...: db.get('key')
    ...:
 Out[6]: 'value'
 
 In [8]: # %load 04_dump.py
    ...: db.dump()
    ...:
 Out[8]: True
 
```

pickleDBのよく使われるメソッドを以下に説明します。

-  `load(path)` ：ファイルからデータベースを読み込む
-  `set(key, value)` ：キーの値を文字列で指定します。キーの値を文字列で指定
-  `get(key)` ：キーを取得します。キーの値を取得する
-  `getall()` ：データベース内のすべてのキーを取得する
-  `rem(key)` ：キーを削除します。キーを削除する
-  `dump()` ：データベースをメモリからloadコマンドで指定したファイルに保存する

他にも次のメソッドがあります。
-  `append(key, more)` ：キーの値をさらに追加
-  `lcreate(name)` ；文字列 name で与えたリストを作成する
-  `ladd(name, value)` ：リスト name に値を追加する
-  `lgetall(name)` ：リスト name 内の全ての値を返す
-  `lextend(name, seq)` ：リスト name をシーケンスで拡張する
-  `lget(name, post)` ：リスト name の中の1つの値を返す
-  `lrem(name)` ：リスト name とその全ての値を削除する
-  `lpop(name, pos)` ：リスト name 内の1つの値を削除する
-  `llen(name)` ；リスト name の長さを返す
-  `laaopend(name, post, more)` ：リスト name 内の値にさらに値を追加する
-  `dcreate(name)` ：辞書を name を作成する
-  `dadd(name, pair)` ：辞書 name のキーと値のペアを追加する、"pair" はタプル
-  `dgetall(name)` ：辞書 name 全ての key-value ペアを返す
-  `dget(name, key)` ：辞書 name の key に対する値を返す
-  `dkeys(name)` ：辞書 name のすべてのキーを返す
-  `dvals(name)` ：辞書 name のすべての値を返す
-  `dexists(name, key(` ：辞書 name に key で与えるキーが存在するかチェック
-  `drem(name)` ：辞書 name のすべてのペアを削除する
-  `dmerge(name1, name2)` ：辞書　name1 と name2 をマージする
-  `dpop(name, key)` ：辞書 name の key で与えるKey-Valueを削除する
-  `deldb()` ：データベースからすべてを削除する


データを書き込む単純なサンプルコードは次のようになります。

```
 In [10]: # %load 05_sample.py
     ...: import pickledb
     ...:
     ...: db = pickledb.load('data.db', False)
     ...:
     ...: things = ['one', 'two', 'three', 'four', 'five']
     ...:
     ...: for i, thing in enumerate(things, start=1):
     ...:     db.set(thing, i)
     ...:
     ...: db.dump()
     ...:
 Out[10]: True
 
```

これにより、ファイル  `data.db` は次のようになります。

```
 In [11]: !cat data.db
  {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
```

 ipython
```
 In [12]: !cat data.db | python -m json.tool
 {
     "one": 1,
     "two": 2,
     "three": 3,
     "four": 4,
     "five": 5
 }
```

このデータベース(JSON形式）から読み出すサンプルは次のようになります。

```
 In [14]: # %load 06_get_sample.py
     ...: import pickledb
     ...:
     ...: db = pickledb.load('data.db', False)
     ...:
     ...: for k in db.getall():
     ...:     print(k, db.get(k))
     ...:
 one 1
 two 2
 three 3
 four 4
 five 5
```

## データの削除
指定したキーを削除するためには `rem()` メソッドを呼び出します。


```
 In [2]: # %load 07_data_operation.py
    ...: import pickledb
    ...:
    ...: db = pickledb.load('data.db', False)
    ...:
    ...: # db.getall()
    ...: # db.rem('one')
    ...: # db.get('one')
    ...:
 
 In [3]: db.getall()
 Out[3]: dict_keys(['one', 'two', 'three', 'four', 'five'])
 
 In [4]: db.rem('one')
 Out[4]: True
 
 In [5]: db.get('one')
 Out[5]: False
 
 In [6]: db.getall()
 Out[6]: dict_keys(['two', 'three', 'four', 'five'])
 
```

## データの追加
データベースにないキーを与えるとデータが追加されます。

```
 In [8]: # %load 08_data_append.py
    ...: import pickledb
    ...:
    ...: db = pickledb.load('data.db', False)
    ...:
    ...: # db.get('ten')
    ...: # db.set('ten', 10)
    ...: # db.get('ten')
    ...: 
 
 In [9]: db.get('ten')
 Out[9]: False
 
 In [10]: db.set('ten', 10)
 Out[10]: True
 
 In [11]: db.get('ten')
 Out[11]: 10
```

 `append()` メソッドでも追加することができますが、キーのオブジェクトの `append()` メソッドを呼び出すことに注意してください。
 `int` 型のデータに文字列を `append()` で追加するなど、保持しているオブジェクトによっては例外が発生します。


```
 In [2]: # %load 09_append.py
    ...: import pickledb
    ...:
    ...: db = pickledb.load('data.db', False)
    ...:
    ...: # db.get('ten')
    ...: # db.append('ten', 10)
    ...: # db.set('ten', 10)
    ...: # db.get('ten')
    ...: # db.append('ten', 10)
    ...: # db.get('ten')
    ...  # db.append('ten', 'ten')
    ...:
 
 In [3]: db.get('ten')
 Out[3]: False
 
 In [4]: db.append('ten', 10)
 ---------------------------------------------------------------------------
 KeyError                                  Traceback (most recent call last)
 <ipython-input-4-a95d0623bb68> in <module>
 ----> 1 db.append('ten', 10)
 
 ~/anaconda3/envs/py39/lib/python3.9/site-packages/pickledb.py in append(self, key, more)
     148     def append(self, key, more):
     149         '''Add more to a key's value'''
 --> 150         tmp = self.db[key]
     151         self.db[key] = tmp + more
     152         self._autodumpdb()
 
 KeyError: 'ten'
 
 In [5]: db.set('ten', 10)
 Out[5]: True
 
 In [6]: db.get('ten')
 Out[6]: 10
 
 In [7]: db.append('ten', 10)
 Out[7]: True
 
 In [8]: db.get('ten')
 Out[8]: 20
 
 In [9]: db.append('ten', 'ten')
 ---------------------------------------------------------------------------
 TypeError                                 Traceback (most recent call last)
 <ipython-input-9-5a41cc32beab> in <module>
 ----> 1 db.append('ten', 'ten')
 
 ~/anaconda3/envs/py39/lib/python3.9/site-packages/pickledb.py in append(self, key, more)
     149         '''Add more to a key's value'''
     150         tmp = self.db[key]
 --> 151         self.db[key] = tmp + more
     152         self._autodumpdb()
     153         return True
 
 TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

## キーに複数のデータを与える
これまでは単純にキーに対応する値をひとつだけセットしたデータ構造でした。
次は、ひとつのキーに複数のデータをもつ場合を考えてみましょう。
先の例では、キー `'one'` に対して `int` 型の `1` をセットしています。これは、キーには１つのオブジェクトをセットしているわけです。つまり、リストやタプル、辞書ほかの複数の値を持てるPythonオブジェクトを与えることで複数の値をひとつのキーに持たせることができます。


```
 In [2]: # %load 10_multiple_data.py
    ...: import pickledb
    ...:
    ...: db = pickledb.load('data.db', False)
    ...:
    ...: # db.set('ten', [10])
    ...: # db.get('ten')
    ...: # db.append('ten', 10)
    ...: # db.get('ten')
    ...: # db.append('ten', [10])
    ...: # db.get('ten')
    ...:
 
 In [3]: db.set('ten', [10])
 Out[3]: True
 
 In [4]: db.get('ten')
 Out[4]: [10]
 
 In [5]: db.append('ten', 10)
 ---------------------------------------------------------------------------
 TypeError                                 Traceback (most recent call last)
 <ipython-input-5-a95d0623bb68> in <module>
 ----> 1 db.append('ten', 10)
 
 ~/anaconda3/envs/py39/lib/python3.9/site-packages/pickledb.py in append(self, key, more)
     149         '''Add more to a key's value'''
     150         tmp = self.db[key]
 --> 151         self.db[key] = tmp + more
     152         self._autodumpdb()
     153         return True
 
 TypeError: can only concatenate list (not "int") to list
 
 In [6]: db.append('ten', [10])
 Out[6]: True
 
 In [7]: db.get('ten')
 Out[7]: [10, 10]
 
```

## シリアライズしたデータを保持
pickleでシリアライズ化された辞書 `data` はメモリ上では操作できますが、 `dumo()` したときにエラーになります。


```
 In [2]: # %load 11_serialized_data.py
    ...: import pickledb
    ...: import pickle
    ...: import base64
    ...: from pprint import pprint
    ...:
    ...: db=pickledb.load('sample.db',False)
    ...:
    ...: data={1:1, 2:2, 3:3}
    ...:
    ...: serial_data = pickle.dumps(data)
    ...: db.set('foo', serial_data)
    ...:
    ...: # pprint(serial_data)
    ...: # pprint(pickle.loads(db.get('foo')))
    ...: # pprint(type(pickle.loads(db.get('foo'))))
    ...:
    ...: # db.dump()
    ...:
 Out[2]: True
 
 In [3]: pprint(serial_data)
 (b'\x80\x04\x95\x11\x00\x00\x00\x00\x00\x00\x00}\x94(K\x01K\x01K\x02K\x02K\x03'
  b'K\x03u.')
 
 In [4]: pprint(pickle.loads(db.get('foo')))
 {1: 1, 2: 2, 3: 3}
 
 In [5]: pprint(type(pickle.loads(db.get('foo'))))
 <class 'dict'>
 
 In [6]: db.dump()
 ---------------------------------------------------------------------------
 TypeError                                 Traceback (most recent call last)
 <ipython-input-6-2b8ac98f3d25> in <module>
 ----> 1 db.dump()
 (中略)
 ~/anaconda3/envs/py39/lib/python3.9/json/encoder.py in default(self, o)
     177
     178         """
 --> 179         raise TypeError(f'Object of type {o.__class__.__name__} '
     180                         f'is not JSON serializable')
     181
 
 TypeError: Object of type bytes is not JSON serializable
```

pickleDBのバックエンドのストレージはJSON形式のフラットファイルです。バイナリデータや、シリアライズされたデータは文字列に変換する必要があります。


```
 In [2]: # %load 12_base64_data.py
    ...: import pickledb
    ...: import pickle
    ...: import base64
    ...: from pprint import pprint
    ...:
    ...: db=pickledb.load('sample.db',False)
    ...:
    ...: data={1:1, 2:2, 3:3}
    ...:
    ...: serial_data = pickle.dumps(data)
    ...: base64_data = base64.b64encode(serial_data).decode('utf-8')
    ...: db.set('foo', base64_data)
    ...:
    ...: # pprint(base64_data)
    ...: # db.dump()
    ...:
 Out[2]: True
 
 In [3]: pprint(base64_data)
 'gASVEQAAAAAAAAB9lChLAUsBSwJLAksDSwN1Lg=='
 
 In [4]:
 
 In [4]: db.dump()
 Out[4]: True
 
```

データベースから読み出すときは次のようになります。


```
 In [2]: # %load 13_base64_read.py
    ...: import pickledb
    ...: import pickle
    ...: import base64
    ...: from pprint import pprint
    ...:
    ...: db=pickledb.load('sample.db',False)
    ...:
    ...: base64_data = db.get('foo')
    ...: serial_data = base64.b64decode(base64_data)
    ...: data = pickle.loads(serial_data)
    ...:
    ...: # pprint(base64_data)
    ...: # pprint(serial_data)
    ...: # pprint(data)
    ...:
 
 In [3]: pprint(base64_data)
 'gASVEQAAAAAAAAB9lChLAUsBSwJLAksDSwN1Lg=='
 
 In [4]: pprint(serial_data)
 (b'\x80\x04\x95\x11\x00\x00\x00\x00\x00\x00\x00}\x94(K\x01K\x01K\x02K\x02K\x03'
  b'K\x03u.')
 
 In [5]: pprint(data)
 {1: 1, 2: 2, 3: 3}
```

pickle などのシリアライズ化を処理するモジュールを使うことで、クラスのインスタンスオブジェクトや関数なども保存することができるようになります。


## まとめ
pickleDB はシンプルなデータストアで、Pythonだけで動作するためデータベースなど別のミドルウェアを起動する必要がなく、手軽に利用することができます。


## 参考資料
- [pickleDB ソースコード ](https://github.com/patx/pickledb)
- [pickleDB 公式ドキュメント ](https://pythonhosted.org/pickleDB/)


previous: [データの永続性]
next: [TinyDBを使ってみよう]
#Pythonセミナーデータベース編


