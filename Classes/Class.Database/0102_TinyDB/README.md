TinyDBを使ってみよう
=================
## TinyDBについて
TinyDB はPythonで実装された軽量なデータベースで、ドキュメント型データベースに位置づけられるものです。次のような特徴を持っています。マイクロデータベース分類されることもあります。

- **軽量(Tiny)**：1800行のPythonコードで実装されています。（そのうち約40%はドキュメントです）
- **ドキュメント指向(Document Oriented)**：あらゆるドキュメントを格納することができます。
- **最適**：シンプルでクリーンなAPIを提供することで、ストレスなく簡単に利用できるようになっています。
- **PurePython**：Pythonだけで実装されていて、サーバを構築する必要がないためすぐに利用できます。
- **パワフルな拡張性**：新しいストレージや、ミドルウェアを取り入れるなど簡単にTinyDBを拡張することができます。
- **100%テスト済み**：約1600行のテストケースをすべてクリアしています。

逆に、次のような要求があれば、TInyDB では機能不足となることにも留意してください。

- 複数プロセスやスレッドからのアクセス
- テーブルにインデックスを作成する
- HTTPサーバ
- テーブル間のリレーションシップの管理
- [ACID ](https://ja.wikipedia.org/wiki/ACID_(コンピュータ科学)) の保証
- パフォーマンスを重視し高速なデータベースを必要としている

## インストール
TinyDB は次のようにインストールします。
conda でもインストールすることができますが、現時点では PYPIパッケージの方がバージンが新しいので pip を使用します。

 bash
```
 $ pip install tinydb
```


## 基本的な使い方

TinyDBでデータベースにアクセスするためには、 `TninyDB()` にファイル名を与えてインスタンスを生成します。デフォルトでは データは `json` モジュールを使ったJSON形式として処理されます。


```
 In [2]: # %load 01_connection.py
    ...: from tinydb import TinyDB
    ...:
    ...: db = TinyDB('db.json')
    ...:
```

もちろん、これは YAML や pickle フォーマットなど別のフォーマットを使用することもできます。（詳しくは後述しています）

### データの基本操作
データベースにエントリを追加するときは `insert()` メソッドを使います。
このとき**ドキュメントID** が返されます。これは後ほど説明します。


```
 In [4]: # %load 02_insert.py
    ...: v = db.insert({'type': 'apple', 'count': 7})
    ...: print(v)
    ...: v = db.insert({'type': 'peach', 'count': 3})
    ...: print(v)
    ...:
 1
 2
```

すべてのエントリーを参照するためには  `all()` メソッドを呼び出すか、 `for` 文でオブジェクトを取り出します。

```
 In [4]: # %load 03_retrieve.py
    ...: v = db.all()
    ...: print(v)
    ...:
    ...: for item in db:
    ...:     print(item)
    ...:
    ...:
 [{'type': 'apple', 'count': 7}, {'type': 'peach', 'count': 3}]
 {'type': 'apple', 'count': 7}
 {'type': 'peach', 'count': 3}
 
```

TinyDBでは `Query` オブジェクトを作成してデータベースを検索することができます。

```
 In [2]: # %load 04_query.py
    ...: from tinydb import TinyDB, Query
    ...:
    ...: db = TinyDB('db.json')
    ...:
    ...: fruit = Query()
    ...: v1 = db.search(fruit.type == 'peach')
    ...: v2 = db.search(fruit.count > 5 )
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 [{'type': 'peach', 'count': 3}]
 
 In [4]: print(v2)
 [{'type': 'apple', 'count': 7}]
```


クエリに合致するエントリの内容を `update()` メソッドで更新することもできます。

```
 In [6]: # %load 05_query_update.py
    ...: from tinydb import TinyDB, Query
    ...:
    ...: db = TinyDB('db.json')
    ...:
    ...: fruit = Query()
    ...: v1 = db.search(fruit.type == 'apple')
    ...: doc_id = db.update({'count': 10}, fruit.type == 'apple')
    ...: v2 = db.search(fruit.type == 'apple')
    ...:
    ...: # print(v1)
    ...: # print(doc_id)
    ...: # print(v2)
    ...:
 
 In [7]: print(v1)
 [{'type': 'apple', 'count': 7}]
 
 In [8]: print(doc_id)
 [1]
 
 In [9]: print(v2)
 [{'type': 'apple', 'count': 10}]
 
```

同様に  `remove()` メソッドではエントリを削除します。　 `remove()` メソッドは削除したドキュメントIDを返します。

```
 In [6]: # %load 06_query_remove.py
    ...: from tinydb import TinyDB, Query
    ...:
    ...: db = TinyDB('db.json')
    ...:
    ...: fruit = Query()
    ...: id1 = db.remove(fruit.count < 5)
    ...: v1 = db.all()
    ...: id2 = db.remove(fruit.count > 20)
    ...: v2 = db.all()
    ...:
    ...: # print(id1)
    ...: # print(v1)
    ...: # print(id2)
    ...: # print(v2)
    ...:
 
 In [7]: print(id1)
 [2]
 
 In [8]: print(v1)
 [{'type': 'apple', 'count': 7}]
 
 In [9]: print(id2)
 []
 
 In [10]: print(v1)
 [{'type': 'apple', 'count': 7}]
 
```


すべてのデータを削除するためには  `truncate()` を使います。

```
 In [2]: # %load 07_truncate.py
    ...: from tinydb import TinyDB
    ...:
    ...: db = TinyDB('db.json')
    ...: v1 = db.truncate()
    ...: v2 = db.all()
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 None
 
 In [4]: print(v2)
 []
```

 TinyDBの基本的なデータ操作

| メソッド | 説明 |
|:--|:--|
| db.insert(...) | エントリの追加 |
| db.all() | すべてのエントリを返す |
| intr(db) | すべてのエントリを取り出す |
| db.search(query) | queryオブジェクトに合致するエントリを返す |
| db.update(...) | エントリを更新する |
| db.remove(...) | エントリの削除 |
| db.truncate() | すべてのエントリを削除 |
| Query(...) | Queryオブジェクトを作成する |
| Query().field == 2 | Queryオブジェクトのフィールドを指定して対象を絞り込む |
|  | 演算子には ==, !=, >, >=, <, <= が使える |

## データの追加
まず、次のようなデータがあとして、これを TinyDB を使ってJSONフォーマットのデータベースとして保存しましょう。
 user_data.py
```
 user_data = [
     { 'name': 'John',
       'birthday': {'year': 1951, 'month': 8, 'day': 19},
       'country-code': 'GB'
     },
     { 'name': 'Freddie',
       'birthday': {'year': 1946, 'month': 9, 'day': 5},
       'country-code': 'GB'
     },
     { 'name': 'Brian',
       'birthday': {'year': 1947, 'month': 7, 'day': 19},
       'country-code': 'GB'
     },
     { 'name': 'Roger',
       'birthday': {'year': 1949, 'month': 7, 'day': 26},
       'country-code': 'GB'
     },
 ]
```

 `insert()` メソッドを使う場合は次のようになります。

```
 In [2]: # %load 08_insert_data.py
    ...: from tinydb import TinyDB, where
    ...: from user_data import user_data
    ...:
    ...: db = TinyDB('users.json')
    ...:
    ...: for p in user_data:
    ...:     db.insert(p)
    ...:
 
 In [4]: !cat users.json
 {"_default": {"1": {"name": "John", "birthday": {"year": 1951, "month": 8, "day": 19}, "country-code": "GB"}, "2": {"name": "Freddie", "birthday": {"year": 1946, "month": 9, "day": 5}, "country-code": "GB"}, "3": {"name": "Brian", "birthday": {"year": 1947, "month": 7, "day": 19}, "country-code": "GB"}, "4": {"name": "Roger", "birthday": {"year": 1949, "month": 7, "day": 26}, "country-code": "GB"}}}
 
```

 `insert_multiple()` で複数のデータを一括して登録することもできます。

```
 In [2]: # %load 09_insert_multiple.py
    ...: from tinydb import TinyDB, where
    ...: from user_data import user_data
    ...:
    ...: db = TinyDB('users.json')
    ...:
    ...: db.insert_multiple(user_data)
    ...:
 Out[2]: [1, 2, 3, 4]
 
 In [3]: !cat users.json
 {"_default": {"1": {"name": "John", "birthday": {"year": 1951, "month": 8, "day": 19}, "country-code": "GB"}, "2": {"name": "Freddie", "birthday": {"year": 1946, "month": 9, "day": 5}, "country-code": "GB"}, "3": {"name": "Brian", "birthday": {"year": 1947, "month": 7, "day": 19}, "country-code": "GB"}, "4": {"name": "Roger", "birthday": {"year": 1949, "month": 7, "day": 26}, "country-code": "GB"}}}
```

これ以降、何度も `users.json` へのデータベース接続を使用するので、
次のようなモジュールを用意しておきます。
 tinydb_setup.py
```
 from tinydb import TinyDB, Query, where
 from pprint import pprint
 from user_data import user_data
 
 DB_NAME='users.json'
 
 db = TinyDB(DB_NAME)
 user = Query()
  
 def database_initialized():
    global db
    db.truncate()
    db.insert_multiple(user_data)
```

## ドキュメントID
TinyDBではデータベースに登録されたデータにはドキュメントIDが割り振られます。

```
 In [2]: # %load 10_document_id.py
    ...: from tinydb_setup import *
    ...:
    ...: v1 = db.get(user.name == 'John')
    ...: v2 = db.all()[0]
    ...: v3 = db.all()[-1]
    ...:
    ...: # print(v1.doc_id, v1)
    ...: # print(v2.doc_id, v2)
    ...: # print(v3.doc_id, v3)
    ...:
 
 In [3]: print(v1.doc_id, v1)
 1 {'name': 'John', 'birthday': {'year': 1951, 'month': 8, 'day': 19}, 'country-code': 'GB'}
 
 In [4]: print(v2.doc_id, v2)
 1 {'name': 'John', 'birthday': {'year': 1951, 'month': 8, 'day': 19}, 'country-code': 'GB'}
 
 In [5]: print(v3.doc_id, v3)
 4 {'name': 'Roger', 'birthday': {'year': 1949, 'month': 7, 'day': 26}, 'country-code': 'GB'}
 
```

ドキュメントIDを指示してデータを更新したり、削除することもできます。

```
 In [2]: # %load 11_update_by_docid.py
    ...: from tinydb_setup import *
    ...:
    ...: database_initialized()
    ...:
    ...: before_data = db.all()
    ...:
    ...: db.update({'current_member': 1}, doc_ids=[3,4])
    ...: db.remove(doc_ids=[1,2])
    ...:
    ...: after_data = db.all()
    ...:
    ...: check = db.contains(doc_id=1)
    ...: doc = db.get(doc_id=3)
    ...:
    ...: # pprint(check)
    ...: # pprint(before_data)
    ...: # pprint(after_data)
    ...: # pprint(doc)
    ...:
 
 In [3]: pprint(check)
 False
 
 In [4]: pprint(before_data)
 [{'birthday': {'day': 19, 'month': 8, 'year': 1951},
   'country-code': 'GB',
   'name': 'John'},
  {'birthday': {'day': 5, 'month': 9, 'year': 1946},
   'country-code': 'GB',
   'name': 'Freddie'},
  {'birthday': {'day': 19, 'month': 7, 'year': 1947},
   'country-code': 'GB',
   'name': 'Brian'},
  {'birthday': {'day': 26, 'month': 7, 'year': 1949},
   'country-code': 'GB',
   'name': 'Roger'}]
 
 In [5]: pprint(after_data)
 [{'birthday': {'day': 19, 'month': 7, 'year': 1947},
   'country-code': 'GB',
   'current_member': 1,
   'name': 'Brian'},
  {'birthday': {'day': 26, 'month': 7, 'year': 1949},
   'country-code': 'GB',
   'current_member': 1,
   'name': 'Roger'}]
 
 In [6]: pprint(doc)
 {'birthday': {'day': 19, 'month': 7, 'year': 1947},
  'country-code': 'GB',
  'current_member': 1,
  'name': 'Brian'}
 
```



また、TinyDB には `update()` 、 `remove()` 、 `contains()` 、 `get()` のようにドキュメントID を扱うものがあります。このうち、 `update()` 、 `remove()` は、影響を受けるドキュメントIDのリストを返します。

```
 >>> db.update({'value': 2}, doc_ids=[1, 2])
 [1, 2]
 >>> db.contains(doc_id=1)
 True
 >>> db.remove(doc_ids=[1, 2])
 [1, 2]
 >>> db.get(doc_id=3)
 {'name': 'May', 'age': 44}
 >>> db.all()
 [{'name': 'May', 'age': 44}, {'name': 'Roger', 'age': 40}]
```

 TibyDBでドキュメントIDを扱うメソッド

| メソッド | 説明 |
|:--|:--|
| db.insert(...) | 追加したデータのドキュメントIDを返す |
| db.insert_multiple(...) | 追加したデータのドキュメントIDのリストを返す |
| document.doc_id | 取得したドキュメントdocument のドキュメントIDを返す |
| db.get(doc_id=...) | 与えたドキュメントIDのドキュメントを取得 |
| db.contains(doc_id=...) | 与えたドキュメントIDのドキュメントが存在するかチェックする |
| db.update({...}, doc_ids=[...]) | 与えたドキュメントIDのドキュメントを更新する |
| db.remove(doc_ids=[...]) | 与えたドキュメントIDのドキュメントを削除する |


## データの更新
前述の例のように、 `update()` メソッドでデータを更新できます。
このときに、辞書を与えるとデータベースのテーブルにのカラムを追加することになります。
カラムを削除したいときは、 `tinydb.operations` から　 `delete()` をインポートします。

データベース内のすべてのドキュメントを更新したいような場合は、クエリ引数を省略することができます。

```
 In [2]: # %load 12_update_all.py
    ...: from tinydb_setup import *
    ...: 
    ...: database_initialized()
    ...: v1 = db.all()
    ...: v2 = db.update({'genders': 'male'})
    ...: v3 = db.all()
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...: # pprint(v3)
    ...:
 
 In [3]: pprint(v1)
 [{'birthday': {'day': 19, 'month': 8, 'year': 1951},
   'country-code': 'GB',
   'name': 'John'},
  {'birthday': {'day': 5, 'month': 9, 'year': 1946},
   'country-code': 'GB',
   'name': 'Freddie'},
  {'birthday': {'day': 19, 'month': 7, 'year': 1947},
   'country-code': 'GB',
   'name': 'Brian'},
  {'birthday': {'day': 26, 'month': 7, 'year': 1949},
   'country-code': 'GB',
   'name': 'Roger'}]
 
 In [4]: pprint(v2)
 [1, 2, 3, 4]
 
 In [5]: pprint(v3)
 [{'birthday': {'day': 19, 'month': 8, 'year': 1951},
   'country-code': 'GB',
   'genders': 'male',
   'name': 'John'},
  {'birthday': {'day': 5, 'month': 9, 'year': 1946},
   'country-code': 'GB',
   'genders': 'male',
   'name': 'Freddie'},
  {'birthday': {'day': 19, 'month': 7, 'year': 1947},
   'country-code': 'GB',
   'genders': 'male',
   'name': 'Brian'},
  {'birthday': {'day': 26, 'month': 7, 'year': 1949},
   'country-code': 'GB',
   'genders': 'male',
   'name': 'Roger'}]
 
```



```
 In [2]: # %load 12_update_delete.py
    ...: from tinydb_setup import *
    ...: from tinydb.operations import delete
    ...:
    ...: database_initialized()
    ...:
    ...: v1 = db.all()
    ...: v2 = db.update({'foo': 'bar'})
    ...:
    ...: v3 = db.update(delete('foo'), user.name == 'Brian')
    ...: v4 = db.all()
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...: # pprint(v3)
    ...: # pprint(v4)
    ...:
 
 In [3]: pprint(v1)
 [{'birthday': {'day': 19, 'month': 8, 'year': 1951},
   'country-code': 'GB',
   'name': 'John'},
  {'birthday': {'day': 5, 'month': 9, 'year': 1946},
   'country-code': 'GB',
   'name': 'Freddie'},
  {'birthday': {'day': 19, 'month': 7, 'year': 1947},
   'country-code': 'GB',
   'name': 'Brian'},
  {'birthday': {'day': 26, 'month': 7, 'year': 1949},
   'country-code': 'GB',
   'name': 'Roger'}]
 
 In [4]: pprint(v2)
 [1, 2, 3, 4]
 
 In [5]: pprint(v3)
 [3]
 
 In [6]: pprint(v4)
 [{'birthday': {'day': 19, 'month': 8, 'year': 1951},
   'country-code': 'GB',
   'foo': 'bar',
   'name': 'John'},
  {'birthday': {'day': 5, 'month': 9, 'year': 1946},
   'country-code': 'GB',
   'foo': 'bar',
   'name': 'Freddie'},
  {'birthday': {'day': 19, 'month': 7, 'year': 1947},
   'country-code': 'GB',
   'name': 'Brian'},
  {'birthday': {'day': 26, 'month': 7, 'year': 1949},
   'country-code': 'GB',
   'foo': 'bar',
   'name': 'Roger'}]
 
```

TinyDBでのドキュメント操作

| 関数 | 説明 |
|:--|:--|
| delete(key) | ドキュメントからKEYを削除 |
| increment(key) | ドキュメントのKEYの値を１だけ加算する |
| decrement(key) | ドキュメントのKEYの値を１だけ減算する |
| add(key, value) | ドキュメントのKEYの値にvalueを加算する |
| subtract(key, value) | ドキュメントのKEYの値にvalueを減算する |
| set(key, value) | ドキュメントのKEYの値にvalueをセットする |



## 複数のデータを一括更新
 `update_multiple()` メソッドを使うと、複数のデータを一括して更新することができます。


```
 In [2]: # %load 13_update_multiple.py
    ...: from tinydb_setup import *
    ...:
    ...: v1 = db.update_multiple([
    ...:   ({'current_member': 0}, where('name') == 'John'),
    ...:   ({'current_member': 0}, where('name') == 'Freddie'),
    ...:   ({'current_member': 1}, where('name') == 'Brian'),
    ...:   ({'current_member': 1}, where('name') == 'Roger'),
    ...: ])
    ...:
    ...: v2 = db.all()
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...:
 
 In [3]: pprint(v1)
 [1, 2, 3, 4]
 
 In [4]: pprint(v2)
 [{'birthday': {'day': 19, 'month': 8, 'year': 1951},
   'country-code': 'GB',
   'current_member': 0,
   'name': 'John'},
  {'birthday': {'day': 5, 'month': 9, 'year': 1946},
   'country-code': 'GB',
   'current_member': 0,
   'name': 'Freddie'},
  {'birthday': {'day': 19, 'month': 7, 'year': 1947},
   'country-code': 'GB',
   'current_member': 1,
   'name': 'Brian'},
  {'birthday': {'day': 26, 'month': 7, 'year': 1949},
   'country-code': 'GB',
   'current_member': 1,
   'name': 'Roger'}]
 
```

 TinyDBでのデータ更新メソッド

| メソッド | 説明 |
|:--|:--|
| db .insert() | 追加したデータのドキュメントIDを返す |
| db.insert_multiple() | 追加したデータのドキュメントIDのリストを返す |
| doc.doc_id | ドキュメントIDを取得する |
| db.get(doc_id=...) | 指定したドキュメントIDのデータを取得 |
| db.contains(doc_id=...) | 指定したドキュメントIDのデータが存在するかチェック |
| db.update(doc_ids=..) | 指定したドキュメントIDのデータを更新する |
| db.update_multiple() | 更新したドキュメントIDのリストを返す |
| db.remove(doc_ids=...) | 指定したドキュメントIDのデータを削除する |

## アップサート upsert
場合によっては、 `update()` と `insert()` の両方を組み合わせた操作が必要になることもあります。こうしたときは、 `upsert()` を使用します（update + insert)。この操作は、ドキュメントとクエリが渡されます。クエリにマッチするドキュメントがあれば、そのドキュメントは与えられたドキュメントのデータで更新されます。しかし、マッチするドキュメントが見つからない場合は、提供されたドキュメントをテーブルに挿入します。


```
 In [2]: # %load 14_upsert.py
    ...: from tinydb_setup import *
    ...:
    ...: adam = {
    ...:     'name': 'Adam',
    ...:     'birthday': {'year': 1982, 'month': 1, 'day': 29},
    ...:     'country-code': 'USA'
    ...: }
    ...:
    ...: database_initialized()
    ...: v1 = db.all()
    ...: v2 = db.upsert(adam, user.name == 'Freddie')
    ...: v3 = db.all()
    ...:
    ...: database_initialized()
    ...: v4 = db.upsert(adam, user.name == 'Adam')
    ...: v5 = db.all()
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...: # pprint(v3)
    ...: # pprint(v4)
    ...: # pprint(v5)
    ...:
 
 In [3]: pprint(v1)
 [{'birthday': {'day': 19, 'month': 8, 'year': 1951},
   'country-code': 'GB',
   'name': 'John'},
  {'birthday': {'day': 5, 'month': 9, 'year': 1946},
   'country-code': 'GB',
   'name': 'Freddie'},
  {'birthday': {'day': 19, 'month': 7, 'year': 1947},
   'country-code': 'GB',
   'name': 'Brian'},
  {'birthday': {'day': 26, 'month': 7, 'year': 1949},
   'country-code': 'GB',
   'name': 'Roger'}]
 
 In [4]: pprint(v2)
 [2]
 
 In [5]: pprint(v3)
 [{'birthday': {'day': 19, 'month': 8, 'year': 1951},
   'country-code': 'GB',
   'name': 'John'},
  {'birthday': {'day': 29, 'month': 1, 'year': 1982},
   'country-code': 'USA',
   'name': 'Adam'},
  {'birthday': {'day': 19, 'month': 7, 'year': 1947},
   'country-code': 'GB',
   'name': 'Brian'},
  {'birthday': {'day': 26, 'month': 7, 'year': 1949},
   'country-code': 'GB',
   'name': 'Roger'}]
 
 In [6]: pprint(v4)
 [5]
 
 In [7]: pprint(v5)
 [{'birthday': {'day': 19, 'month': 8, 'year': 1951},
   'country-code': 'GB',
   'name': 'John'},
  {'birthday': {'day': 5, 'month': 9, 'year': 1946},
   'country-code': 'GB',
   'name': 'Freddie'},
  {'birthday': {'day': 19, 'month': 7, 'year': 1947},
   'country-code': 'GB',
   'name': 'Brian'},
  {'birthday': {'day': 26, 'month': 7, 'year': 1949},
   'country-code': 'GB',
   'name': 'Roger'},
  {'birthday': {'day': 29, 'month': 1, 'year': 1982},
   'country-code': 'USA',
   'name': 'Adam'}]
  
```


## クエリQuery

データベースとPythonのオブジェクトの関連付け（マッピング）を行うことを **ORM(Object-Relational Mapping)** と言います。
TnyDBで、一般的なORMで使用される方法でのクエリを作成してみましょう。

```
 In [2]: # %load 15_query_orm.py
    ...: from tinydb_setup import *
    ...:
    ...: v1 = db.all()
    ...: v2 = db.search(user.name == 'John')
    ...: v3 = db.search(user.name == 'Jack')
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...: # pprint(v3)
    ...:
 
 In [3]: pprint(v1)
 [{'birthday': {'day': 19, 'month': 8, 'year': 1951},
   'country-code': 'GB',
   'name': 'John'},
  {'birthday': {'day': 5, 'month': 9, 'year': 1946},
   'country-code': 'GB',
   'name': 'Freddie'},
  {'birthday': {'day': 19, 'month': 7, 'year': 1947},
   'country-code': 'GB',
   'name': 'Brian'},
  {'birthday': {'day': 26, 'month': 7, 'year': 1949},
   'country-code': 'GB',
   'name': 'Roger'},
  {'birthday': {'day': 29, 'month': 1, 'year': 1982},
   'country-code': 'USA',
   'name': 'Adam'}]
 
 In [4]: pprint(v2)
 [{'birthday': {'day': 19, 'month': 8, 'year': 1951},
   'country-code': 'GB',
   'name': 'John'}]
 
 In [5]: pprint(v3)
 []
 
```

この例での  `name` のようなフィールド名でなればなにも問題ありませんが、Pythonで使用できない識別子がフィールドにあるような場合は、配列インデックス表記にする必要があります。
具体的な例では、フィールド名にマイナス記号( `-` )を含んでいるような場合です。

 pytyhon
```
 In [2]: # %load 16_query_dot_notation.py
    ...: from tinydb_setup import *
    ...:
    ...: v1 = db.search(user.country-code == 'USA')
    ...:
 ---------------------------------------------------------------------------
 NameError                                 Traceback (most recent call last)
 <ipython-input-2-df949e57912b> in <module>
       2 from tinydb_setup import *
       3
 ----> 4 v1 = db.search(user.country-code == 'USA')
 
 NameError: name 'code' is not defined
```



```
 In [2]: # %load 17_query_index_notation.py
    ...: from tinydb_setup import *
    ...:
    ...: v1 = db.search(user['country-code'] == 'GB')
    ...:
    ...: # pprint(v1)
    ...:
 
 In [3]: pprint(v1)
 [{'birthday': {'day': 19, 'month': 8, 'year': 1951},
   'country-code': 'GB',
   'name': 'John'},
  {'birthday': {'day': 5, 'month': 9, 'year': 1946},
   'country-code': 'GB',
   'name': 'Freddie'},
  {'birthday': {'day': 19, 'month': 7, 'year': 1947},
   'country-code': 'GB',
   'name': 'Brian'},
  {'birthday': {'day': 26, 'month': 7, 'year': 1949},
   'country-code': 'GB',
   'name': 'Roger'}]
 
```


もう一つの方法が  `where` を使用してフィールドを指定したクエリの作成方法です。


```
 In [1]: %load 18_query_where.py
 
 In [2]: # %load 18_query_where.py
    ...: from tinydb_setup import *
    ...:
    ...: v1 = db.search(where('country-code') == 'USA')
    ...:
    ...: # pprint(v1)
    ...:
 
 In [3]: pprint(v1)
 [{'birthday': {'day': 29, 'month': 1, 'year': 1982},
   'country-code': 'USA',
   'name': 'Adam'}]
 
```

 `where` は  `from tinydb iport where` としてあらかじめインポートしている必要があります。
この例では、tinydb_setup モジュールのなかでインポートされています。

 `whre('field')` は、次の記述と等価で、簡潔に表記できるようにしたものです。

```
 db.search(Query()['field'] == 'value')
```

ネストされたフィールドには次のように参照することができます。

```
 In [2]: # %load 19_query_nest_data.py
    ...: from tinydb_setup import *
    ...:
    ...: database_initialized()
    ...:
    ...: v1 = db.search(where('birthday').year == 1947)
    ...: v2 = db.search(where('birthday')['year'] == 1947)
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...:
 
 In [3]: pprint(v1)
 [{'birthday': {'day': 19, 'month': 7, 'year': 1947},
   'country-code': 'GB',
   'name': 'Brian'}]
 
 In [4]: pprint(v2)
 [{'birthday': {'day': 19, 'month': 7, 'year': 1947},
   'country-code': 'GB',
   'name': 'Brian'}]
```

ここで、留意する必要があることは、Queryはキャッシュされるということです。
そのため、複数のデータベースを扱うときに同じフィールドが存在するときは期待した通りには動作しない可能性があります。

## より高度なクエリ
クエリで使用できる演算子には  `==` ,  `!=` ,  `>` ,  `>=` ,  `<` ,  `<=` が使えることは説明しました。
Queruyオブジェクトのメソッドを使用することで、より柔軟なクエリを作成することができます。

#### フィールド name が存在するかチェック

```
 In [2]: # %load 20_field_exists.py
    ...: from tinydb_setup import *
    ...:
    ...: v1 = user.name.exists()
    ...: v2 = db.search(user.name.exists())
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...:
 
 In [3]: pprint(v1)
 QueryImpl('exists', ('name',))
 
 In [4]: pprint(v2)
 [{'birthday': {'day': 19, 'month': 8, 'year': 1951},
   'country-code': 'GB',
   'name': 'John'},
  {'birthday': {'day': 5, 'month': 9, 'year': 1946},
   'country-code': 'GB',
   'name': 'Freddie'},
  {'birthday': {'day': 19, 'month': 7, 'year': 1947},
   'country-code': 'GB',
   'name': 'Brian'},
  {'birthday': {'day': 26, 'month': 7, 'year': 1949},
   'country-code': 'GB',
   'name': 'Roger'}]
   
```


#### フィールド name を正規表現で指定して絞りこむ(完全一致)
 `name` が大文字A,B,C,D,Eで始まるものを検索

```
 In [2]: # %load 21_query_regex.py
    ...: from tinydb_setup import *
    ...:
    ...: v1 = user.name.matches('[A-E][aZ]*')
    ...: v2 = db.search(user.name.matches('[A-E][aZ]*'))
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...:
 
 In [3]: pprint(v1)
 QueryImpl('matches', ('name',), '[A-E][aZ]*')
 
 In [4]: pprint(v2)
 [{'birthday': {'day': 19, 'month': 7, 'year': 1947},
   'country-code': 'GB',
   'name': 'Brian'}]
 
```

#### フィールド name を正規表現で指定して絞りこむ(部分一致)
 `name` が大文字Bではじまるものを検索

```
 In [2]: # %load 22_query_matches.py
    ...: from tinydb_setup import *
    ...:
    ...: v1 = user.name.matches('B+')
    ...: v2 = db.search(user.name.matches('B+'))
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...:
 
 In [3]: pprint(v1)
 QueryImpl('matches', ('name',), 'B+')
 
 In [4]: pprint(v2)
 [{'birthday': {'day': 19, 'month': 7, 'year': 1947},
   'country-code': 'GB',
   'name': 'Brian'}]
 
```

#### フィールド name の 'John' を検索し、大文字小文字は問わない

```
 In [2]: # %load 23_ignore_case.py
    ...: import re
    ...: from tinydb_setup import *
    ...:
    ...: v1 = db.search(user.name.matches('john', flags=re.IGNORECASE))
    ...:
    ...: # pprint(v1)
    ...:
 
 In [3]: pprint(v1)
 [{'birthday': {'day': 19, 'month': 8, 'year': 1951},
   'country-code': 'GB',
   'name': 'John'}]
 
```



#### テスト関数でフィールド birhday の yearが 1940-1948のものを絞り込む

```
 In [2]: # %load 24_custom_test_func.py
    ...: import re
    ...: from tinydb_setup import *
    ...:
    ...: def year_check(val, m, n):
    ...:     return m <= val < n
    ...:
    ...: v1 = db.search(user.birthday.year.test(year_check, 1940, 1948))
    ...:
    ...: # pprint(v1)
    ...:
 
 In [3]: pprint(v1)
 [{'birthday': {'day': 5, 'month': 9, 'year': 1946},
   'country-code': 'GB',
   'name': 'Freddie'},
  {'birthday': {'day': 19, 'month': 7, 'year': 1947},
   'country-code': 'GB',
   'name': 'Brian'}]
```


#### ラムダ式で定義したテスト関数でフィールド絞りこむ
name に  `"John"` があるものを絞り込むときは次のようにします。

```
 In [2]: # %load 25_custom_test_lambda.py
    ...: from tinydb_setup import *
    ...:
    ...: test_john =  lambda n: n == 'John'
    ...:
    ...: v1 = db.search(user.name.test(test_john))
    ...:
    ...: # pprint(v1)
    ...:
 
 In [3]: pprint(v1)
 [{'birthday': {'day': 19, 'month': 8, 'year': 1951},
   'country-code': 'GB',
   'name': 'John'}]
 
```

#### 辞書に合致するエントリを絞りこむ

```
 In [2]: # %load 26_fragment_dict.py
    ...: from tinydb_setup import *
    ...:
    ...: test_d = {'name': 'John', 'country-code': 'GB'}
    ...: v1 = db.search(Query().fragment(test_d))
    ...:
    ...: # pprint(v1)
    ...:
 
 In [3]: pprint(v1)
 [{'birthday': {'day': 19, 'month': 8, 'year': 1951},
   'country-code': 'GB',
   'name': 'John'}]
```


この場合は、次のコードと同じになります。

```
 In [2]: # %load 27_fragment_dict_alias.py
    ...: from tinydb_setup import *
    ...:
    ...: v1 = db.search((Query().name == 'John') & (Query()['country-code'] == 'GB
    ...: '))
    ...:
    ...: # pprint(v1)
    ...:
 
 In [3]: pprint(v1)
 [{'birthday': {'day': 19, 'month': 8, 'year': 1951},
   'country-code': 'GB',
   'name': 'John'}]
```

#### 指定したフィールドの内容の絞り込みに辞書を使用

```
 In [2]: # %load 28_fragment_field.py
    ...: from tinydb_setup import *
    ...:
    ...: test_d1 = {'year': 1946, 'month': 9, 'day': 5}
    ...: test_d2 = {'month': 7}
    ...:
    ...: v1 = db.search(Query().birthday.fragment(test_d1))
    ...: v2 = db.search(Query().birthday.fragment(test_d2))
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...:
 
 In [3]: pprint(v1)
 [{'birthday': {'day': 5, 'month': 9, 'year': 1946},
   'country-code': 'GB',
   'name': 'Freddie'}]
 
 In [4]: pprint(v2)
 [{'birthday': {'day': 19, 'month': 7, 'year': 1947},
   'country-code': 'GB',
   'name': 'Brian'},
  {'birthday': {'day': 26, 'month': 7, 'year': 1949},
   'country-code': 'GB',
   'name': 'Roger'}]
```

### any()と all() メソッド
フィールドにリストが含まれている場合は、 `any()` および  `all()` メソッドも使用することができます。
例を示すために、次のようななデータを用意します。
 user_group_data.py
```
 user_data = [
     { 'name': 'John',
       'group': ['user', 'operator', 'admin'],
     },
     { 'name': 'Freddie',
       'group': ['user','operator'],
     },
     { 'name': 'Brian',
       'group': ['user'],
     },
     { 'name': 'Roger',
       'group': ['user']
     },
 ]
 
 group_data = [
     { 'name': 'user',
       'permissions': [{'type': 'read'}]
     },
     { 'name': 'operator',
       'permissions': [{'type': 'read'}, {'type': 'sudo'}]
     },
     { 'name': 'operator',
       'permissions': [{'type': 'read'}, {'type': 'sudo'}, {'type': 'write'}]
     }
 ]
 
```

このデータを登録するために次にモジュールを作成します。

 tinydb_usersetup.py
```
 rom tinydb import TinyDB, Query, where
 from pprint import pprint
 from user_auth_data import user_data, group_data
 
 DB_NAME='usergroup.json'
 
 db = TinyDB(DB_NAME)
 user = Query()
 db_group = db.table('group')
 
 def database_initialized():
     global db, db_group
     db.truncate()
     db_group.truncate()
     db.insert_multiple(user_data)
     db_group = db.table('group')
     db_group.insert_multiple(group_data)
```

これまではデフォルトデーブル１つだけをもつデータベース構造でしたが、この例では  `group` テーブルを作成しています。



```
 In [1]: from tinydb_usersetup import *
 
 In [2]: database_initialized()
 
 In [3]: db.all()
 Out[3]:
 [{'name': 'John', 'group': ['user', 'operator', 'admin']},
  {'name': 'Freddie', 'group': ['user', 'operator']},
  {'name': 'Brian', 'group': ['user']},
  {'name': 'Roger', 'group': ['user']}]
 
 In [4]: db_group.all()
 Out[4]:
 [{'name': 'user', 'permissions': [{'type': 'read'}]},
  {'name': 'operator', 'permissions': [{'type': 'read'}, {'type': 'sudo'}]},
  {'name': 'operator',
   'permissions': [{'type': 'read'}, {'type': 'sudo'}, {'type': 'write'}]}]
 
 
```

フィールド名  `group` に対して　 `any()` で与えたリストを含むエントリを検索。どれかひとつでもあればヒットします。

```
 In [2]: # %load 30_query_any.py
    ...: from tinydb_usersetup import *
    ...:
    ...: v1 = db.search(user.group.any(['user']))
    ...: v2 = db.search(user.group.any(['operator']))
    ...: v3 = db.search(user.group.any(['operator', 'admin']))
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...: # pprint(v3)
    ...:
 
 In [3]: pprint(v1)
 [{'group': ['user', 'operator', 'admin'], 'name': 'John'},
  {'group': ['user', 'operator'], 'name': 'Freddie'},
  {'group': ['user'], 'name': 'Brian'},
  {'group': ['user'], 'name': 'Roger'}]
 
 In [4]: pprint(v2)
 [{'group': ['user', 'operator', 'admin'], 'name': 'John'},
  {'group': ['user', 'operator'], 'name': 'Freddie'}]
 
 In [5]: pprint(v3)
 [{'group': ['user', 'operator', 'admin'], 'name': 'John'},
  {'group': ['user', 'operator'], 'name': 'Freddie'}]
  
```

フィールド名  `groups` に対して `all()` に’与えたリストをすべて含む のエントリを検索。

```
 In [2]: # %load 31_query_all.py
    ...: from tinydb_usersetup import *
    ...:
    ...: v1 = db.search(user.group.all(['user']))
    ...: v2 = db.search(user.group.all(['operator']))
    ...: v3 = db.search(user.group.all(['operator', 'admin']))
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...: # pprint(v3)
    ...:
 
 In [3]: pprint(v1)
 [{'group': ['user', 'operator', 'admin'], 'name': 'John'},
  {'group': ['user', 'operator'], 'name': 'Freddie'},
  {'group': ['user'], 'name': 'Brian'},
  {'group': ['user'], 'name': 'Roger'}]
 
 In [4]: pprint(v2)
 [{'group': ['user', 'operator', 'admin'], 'name': 'John'},
  {'group': ['user', 'operator'], 'name': 'Freddie'}]
 
 In [5]: pprint(v3)
 [{'group': ['user', 'operator', 'admin'], 'name': 'John'}]
 
```


Groups の権限に  `read` があるエントリを検索

```
 In [2]: # %load 32_query_any_table.py
    ...: from tinydb_usersetup import *
    ...:
    ...: q = group.permission.any(permission.type == 'read')
    ...: v = db_group.search(group.permission.any(permission.type == 'read'))
    ...:
    ...: # pprint(q)
    ...: # pprint(v)
    ...:
 
 In [3]: pprint(q)
 QueryImpl('any', ('permission',), QueryImpl('==', ('type',), 'read'))
 
 In [4]: pprint(v)
 [{'name': 'user', 'permission': [{'type': 'read'}]},
  {'name': 'operator', 'permission': [{'type': 'read'}, {'type': 'sudo'}]},
  {'name': 'admin',
   'permission': [{'type': 'read'}, {'type': 'sudo'}, {'type': 'write'}]}]
   
```


Groups  の権限が  `read` だけがあるのエントリを検索

```
 In [2]: # %load 33_query_all_read.py
    ...: from tinydb_usersetup import *
    ...:
    ...: q = group.permission.any(permission.type == 'read')
    ...: v = db_group.search(group.permission.all(permission.type == 'read'))
    ...:
    ...: # pprint(q)
    ...: # pprint(v)
    ...:
 
 In [3]: pprint(q)
 QueryImpl('any', ('permission',), QueryImpl('==', ('type',), 'read'))
 
 In [4]: pprint(v)
 [{'name': 'user', 'permission': [{'type': 'read'}]}]
 
```

 `one_of()` を使うと、リストにアイテムが含まれているかどうかをチェックします。
 `name` フィールドの値が  `jane` もしくは `john` のエントリを取得。

```
 In [2]: # %load 34_query_on_of.py
    ...: from tinydb_usersetup import *
    ...:
    ...: v = db.search(user.name.one_of(['Jack', 'John']))
    ...:
    ...: # pprint(v)
    ...:
 
 In [3]: pprint(v)
 [{'group': ['user', 'operator', 'admin'], 'name': 'John'}]
 
```


### クエリ修飾子
TinyDB ではクエリに論理演算を記述できます。

#### NOT

```
 In [2]: # %load 35_query_not.py
    ...: from tinydb_usersetup import *
    ...:
    ...: v = db.search(~ (user.name == 'Freddie'))
    ...:
    ...: # pprint(v)
    ...:
 
 In [3]: pprint(v)
 [{'group': ['user', 'operator', 'admin'], 'name': 'John'},
  {'group': ['user'], 'name': 'Brian'},
  {'group': ['user'], 'name': 'Roger'}]
```

#### AND

```
 n [2]: # %load 36_query_and.py
    ...: from tinydb_usersetup import *
    ...:
    ...: v = db.search((user.name == 'Freddie') & (user.group.any(['user'])))
    ...:
    ...: # pprint(v)
    ...:
 
 In [3]: pprint(v)
 [{'group': ['user', 'operator'], 'name': 'Freddie'}]
```

#### OR

```
 In [2]: # %load 37_query_or.py
    ...: from tinydb_usersetup import *
    ...:
    ...: v = db.search((user.name == 'John') | (user.name == 'Brian'))
    ...:
    ...: # pprint(v)
    ...:
 
 In [3]: pprint(v)
 [{'group': ['user', 'operator', 'admin'], 'name': 'John'},
  {'group': ['user'], 'name': 'Brian'}]
```

クエリ修飾子に使用されるPythonの二項演算子は、比較演算子よりも演算子の優先順位が高いことに注意してください。
つまり、  `~ User.name == 'John' ` は Python では  `~(User.name == 'John')` ではなく  `(~User.name) == 'John' ` と解析されます。バグを埋め込むことを回避するためにクエリをカッコ( `(...)` ）で囲むようにしましょう。


 TinyDBのクエリ操作

| メソッド | 説明 |
|:--|:--|
| Query().field.exists() | "field"で指定したフィールドが存在するかチェック |
| Query().field.matches(regex) | "filed"で指定したフィールドに正規表現にマッチするデータ存在するかチェック |
| Query().field.search(regex) | "filed"で指定したフィールドから正規表現にマッチするデータを取り出す |
| Query().field.test(func, *args) | "filed"で指定したフィールドでテスト関数が真値を返すデータを取り出す |
| Query().field.all(query | list) | "filed"で指定したフィールドのうち、与えたリストにすべて合致するデータを取り出す |
| Query().field.any(query | list) | "filed"で指定したフィールドのうち、与えたリストのいずれかに合致するデータを取り出す |
| Query().field.one_of(list) | "filed"で指定したフィールドのうち、与えたリストのいずれかを含むデータを取り出す |
| ~ (query) | クエリに合致しないデータ |
| (query1) & (query2) | ２つのクエリの両方に合致するデータ |
| (query1) | (query2) | ２つのクエリのいずれかに合致するデータ |




## ドキュメントを取得
### ドキュメント数を取得
保存されているドキュメントの数を取得するためには、次のようにします。

```
 In [2]: # %load 50_len.py
    ...: from tinydb_setup import *
    ...:
    ...: v1 = db.all()
    ...: v2 = len(db)
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...:
 
 In [3]: pprint(v1)
 [{'birthday': {'day': 19, 'month': 8, 'year': 1951},
   'country-code': 'GB',
   'name': 'John'},
  {'birthday': {'day': 5, 'month': 9, 'year': 1946},
   'country-code': 'GB',
   'name': 'Freddie'},
  {'birthday': {'day': 19, 'month': 7, 'year': 1947},
   'country-code': 'GB',
   'name': 'Brian'},
  {'birthday': {'day': 26, 'month': 7, 'year': 1949},
   'country-code': 'GB',
   'name': 'Roger'}]
 
 In [4]: pprint(v2)
 4
 
```

この例で使用している
このとき、ドキュメントの数として数えられる対象はデフォルトテーブルです。

### ドキュメントを１つ取得
ドキュメントを１つだけ取得する場合は、クエリで絞り込むこと処理できます。結果はリストで返ってくるので次のようにします。

```
 In [2]: # %load 51_retrieve_search.py
    ...: from tinydb_setup import *
    ...:
    ...: v1 = db.search(user.name == 'John')
    ...:
    ...: try:
    ...:     v2 = db.search(user.name == 'Jack')[0]
    ...: except IndexError:
    ...:     v2 = None
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
    ...:
 
 In [3]: pprint(v1)
 [{'birthday': {'day': 19, 'month': 8, 'year': 1951},
   'country-code': 'GB',
   'name': 'John'}]
 
 In [4]: pprint(v2)
 None
 
```

> **注意**
> クエリに合致するデータが複数存在する場合は、ランダムに返されることに注意してください。


 `contains()` メソッドを使ってクエリに合致するドキュメントがあるかチェックしてから、取得する方法もあります。

```
 In [2]: # %load 52_retrieve_contains.py
    ...: from tinydb_setup import *
    ...:
    ...: v1 = db.contains(user.name == 'John')
    ...: v2 = v1 and db.search(user.name == 'John')[0] or None
    ...:
    ...: v3 = db.contains(user.name == 'Jack')
    ...: v4 = v3 and db.search(user.name == 'Jack')[0] or None
    ...:
    ...: # print(v1, v2)
    ...: # print(v3, v4)
    ...:
    ...:
 
 In [3]: print(v1, v2)
 True {'name': 'John', 'birthday': {'year': 1951, 'month': 8, 'day': 19}, 'country-code': 'GB'}
 
 In [4]: print(v3, v4)
 False None
 
```

 `count()` メソッドでクエリに合致するドキュメント数が１つ以上あるときに、ドキュメントを取得する方法です。

```
 In [2]: # %load 53_retrieve_count.py
    ...: from tinydb_setup import *
    ...:
    ...: v1 = db.count(user.name == 'John')
    ...: v2 = v1  and db.search(user.name == 'John')[0] or None
    ...:
    ...: v3 = db.count(user.name == 'Jack')
    ...: v4 = v3 and db.search(user.name == 'Jack')[0] or None
    ...:
    ...: # print(v1, v2)
    ...: # print(v3, v4)
    ...:
    ...:
 
 In [3]: print(v1, v2)
 1 {'name': 'John', 'birthday': {'year': 1951, 'month': 8, 'day': 19}, 'country-code': 'GB'}
 
 In [4]: print(v3, v4)
 0 None
 
```


別の方法は `get()` にクエリを与えて合致するドキュメントを取得する方法です。

```
 In [2]: # %load 54_retrieve_get.py
    ...: from tinydb_setup import *
    ...:
    ...: v1 = db.get(user.name == 'John')
    ...: v2 = db.get(user.name == 'Jack')
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...:
 
 In [3]: pprint(v1)
 {'birthday': {'day': 19, 'month': 8, 'year': 1951},
  'country-code': 'GB',
  'name': 'John'}
 
 In [4]: pprint(v2)
 None
```


## テーブル操作
TinyDBでは複数のテーブルを扱えます。 `Table` オブジェクトを作成するには、 `db.table(name)` を使用します。
これまでの例で使用してきた  `tinydb_usersetup.py` をここでも一度みてみましょう。

 tyinydb_usersetup.py
```
 from tinydb import TinyDB, Query, where
 from pprint import pprint
 from user_auth_data import user_data, group_data
 
 DB_NAME='usergroup.json'
 
 db = TinyDB(DB_NAME)
 db_group = db.table('group')
 
 user = Query()
 group = Query()
 permission = Query()
 
 def database_initialized():
     global db, db_group
     db.truncate()
     db_group.truncate()
     db.insert_multiple(user_data)
     db_group = db.table('group')
     db_group.insert_multiple(group_data)
     
```

見てわかるように、 `Table` クラスは、TinyDB クラスと同じように動作します。
データベースに含まれているテーブルを参照するためには  `tables()` メソッドを使います。

```
 In [2]: # %load 60_table.py
    ...: from tinydb_usersetup import *
    ...:
    ...: v1 = db.all()
    ...: v2 = db_group.all()
    ...: v3 = db.tables()
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...: # pprint(v3)
    ...:
 
 In [3]: pprint(v1)
 [{'group': ['user', 'operator', 'admin'], 'name': 'John'},
  {'group': ['user', 'operator'], 'name': 'Freddie'},
  {'group': ['user'], 'name': 'Brian'},
  {'group': ['user'], 'name': 'Roger'}]
 
 In [4]: pprint(v2)
 [{'name': 'user', 'permission': [{'type': 'read'}]},
  {'name': 'operator', 'permission': [{'type': 'read'}, {'type': 'sudo'}]},
  {'name': 'admin',
   'permission': [{'type': 'read'}, {'type': 'sudo'}, {'type': 'write'}]}]
 
 In [5]: pprint(v3)
 {'group', '_default'}
 
 
```


テーブルを削除するためには  `drop_table()` メソッドを使います。

```
 In [2]: # %load 61_drop_table.py
    ...: from tinydb_usersetup import *
    ...:
    ...: database_initialized()
    ...:
    ...: v1 = db.tables()
    ...: v2 = db_group.all()
    ...: v3 = db.drop_table('group')
    ...: v4 = db_group.all()
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...: # pprint(v3)
    ...: # pprint(v4)
    ...:
 
 In [3]: pprint(v1)
 {'group', '_default'}
 
 In [4]: pprint(v2)
 [{'name': 'user', 'permission': [{'type': 'read'}]},
  {'name': 'operator', 'permission': [{'type': 'read'}, {'type': 'sudo'}]},
  {'name': 'admin',
   'permission': [{'type': 'read'}, {'type': 'sudo'}, {'type': 'write'}]}]
 
 In [5]: pprint(v3)
 None
 
 In [6]: pprint(v4)
 []
 
```

すべてのテーブルを削除するためには、 `drop_tables()` メソッドを使います。

```
 In [1]: !rm -f usergroup.json
 
 In [2]: %load 62_drop_table_all.py
 
    ...: database_initialized()
    ...:
    ...: v1 = db.tables()
    ...: db.drop_table('group')
    ...: v2 = db.tables()
    ...:
    ...: table_devision = db.table('devision')
    ...: table_role = db.table('role')
    ...:
    ...: v3 = db.tables()
    ...: table_devision.insert({'name': 'devops'})
    ...: table_role.insert({'name': 'manager'})
    ...: v4 = db.tables()
    ...:
    ...: db.default_table_name = 'role'
    ...: v5 = db.tables()
    ...: db.drop_tables()
    ...: v6 = db.tables()
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...: # pprint(v3)
    ...: # pprint(v4)
    ...: # pprint(v5)
    ...: # pprint(v6)
    ...:
    ...:
 
 In [4]: pprint(v1)
 {'_default', 'group'}
 
 In [5]: pprint(v2)
 {'_default'}
 
 In [6]: pprint(v3)
 {'_default'}
 
 In [7]: pprint(v4)
 {'devision', '_default', 'role'}
 
 In [8]: pprint(v5)
 {'devision', '_default', 'role'}
 
 In [9]: pprint(v6)
 set()
 
```

 `db,.tables()` でテーブル名が取得できるのは実際にデータベースにテーブルが書き込まれたときです。
つまり、何かしかのデータが書き込まれたタイミングです。


## デフォルトテーブル
TinyDB では、 `_default` という名前のテーブルをデフォルト テーブルとして使用します。データベースオブジェクトに対するすべての操作 ( `db.insert(...)` など) は、このデフォルトテーブルに対して行われます。このテーブルの名前を変更するには、クラス変数  `default_table_name` を設定して、すべてのインスタンスのデフォルトテーブル名を変更します。

## クエリ・キャッシュ
TinyDB はパフォーマンスのためにクエリ結果をキャッシュします。これにより、データベースが変更されていない限り、クエリを再実行してもストレージからデータを読み取りません。 `table(...)` メソッドに  `cache_size` を与えることで、クエリ・キャッシュ・サイズを指示することができます。


```
 >>> table = db.table('table_name', cache_size=30)
```


TinyDB のクエリ・キャッシュは、データベースが使用するストレージが外部プロセスによって変更されたかどうかはチェックしません。このような場合、クエリ・キャッシュは古い結果を返すことがあります。キャッシュをクリアしてストレージからデータを再度読み込むには、 `db.clear_cache()` を使用します。

 `cache_size` に  `None` を与えると無制限にキャッシュします。また、ゼロ( `0` )を与えるとキャッシュが無効になります。
無制限のキャッシュ・サイズと test() クエリを使用すると、TinyDB はテスト関数への参照を保存します。この動作の結果、ラムダ関数をテスト関数として使用する長時間実行するアプリケーションでは、メモリリークが発生する可能性があることに注意してください。

## ストレージとビドルウェア

### ストレージタイプ
TinyDBにはJSON とインメモリの2つのストレージタイプがあります。デフォルトでは、TinyDBはデータをJSONファイルに保存します。データへのパスを指定することもできます。

```
 >>> from tinydb import TinyDB, where
 >>> db = TinyDB('/tmp/userdb.json')
```

パスが指定されていない場合は、Pythonプロセスが実行中のディレクトリに存在するものとして動作します。
次の２つの指示は同じことになります。

```
 >>> db = TinyDB('userdb.json')
 >>> db = TinyDB('./userdb.json')
```

インメモリストレージを使用する場合は、次のようにします。

```
 >>> from tinydb.storages import MemoryStorage
 >>> db = TinyDB(storage=MemoryStorage)
```

 `storage` 引数を除くすべての引数は、ベースのストレージクラスに渡されます。例えば、JSONストレージでは、Pythonの `json.dump(...)` メソッドに追加のキーワード引数を渡すような場合です。

```
 >>> from tinydb import TinyDB
 >>> db = TinyDB('db.json', sort_keys=True, indent=4, separators=(',', ': '))
```

デフォルトのストレージクラスを変更する場合は、TinyDB のクラス変数 default_storage_class にセットします。


```
 >>> from tinydb import TinyDB
 >>> TinyDB.default_storage_class = MemoryStorage
```


ストレージのインスタンスに直接アクセスする必要がある場合は、TinyDB インスタンスの storage プロパティを使用できます。これは、ストレージやミドルウェアのメソッドを直接呼び出すのに便利です。

```
 >>> from tinydb.middlewares import CachingMiddleware
 >>> from tinydb import TinyDB
 >>> from tinydb.storages import MemoryStorage
 >>> from tinydb.middlewares import CachingMiddleware
 >>> db = TinyDB(storage=CachingMiddleware(MemoryStorage))
```


## ミドルウェア
ミドルウェアは、既存のストレージの動作をカスタマイズするものです。

```
 >>> from tinydb.storages import JSONStorage
 >>> from tinydb.middlewares import CachingMiddleware
 >>> db = TinyDB('/tmp/db.json', storage=CachingMiddleware(JSONStorage))
```

### CacigMiddleware
 `CachingMiddleware` は、ディスクI/Oを減らすことで速度を向上させます。すべての読み取り操作をキャッシュし、設定された数の書き込み操作の後にデータをディスクに書き込みます。

テーブルを閉じるときにすべてのデータが安全に書き込まれるようにするには、次のいずれかの方法を使用します。

#### コンテキストマネージャを使用する

```
 >>> with database as db:
 ...     #  何かの操作 (例: db.update(...))
```

#### クローズメソッドを使用する

```
 >>> db.close()
```

TinyDBには、APIを正しく使用していることを確認するためにMyPyが使用できるタイプアノテーションが付属しています。残念ながら、MyPy は TinyDB が使用するすべてのコード パターンを理解しているわけではありません。そのため、TinyDB には、TinyDB を使用するコードを正しく型チェックするのに役立つ MyPy プラグインが同梱されています。これを使用するには、MyPy 設定ファイル（通常は setup.cfg または mypy.ini にあります）のプラグイン リストに追加します。

 mypy.ini
```
 [mypy]
 plugins = tinydb.mypy_plugin
```


## TinyDBの拡張

TinyDBを拡張して、その動作を変更する方法は主に3つあります。

- カスタム ストレージ
- カスタム ミドルウェア。
- フックやオーバーライド

これらは、TinyDB と Table をサブクラス化することです。
この順番で見ていきましょう。

### カスタムストレージの作成
まずは、カスタムストレージのサポートです。デフォルトのTinyDBには、インメモリ・ストレージとJSONファイル・ストレージが搭載されています。しかし、もちろん自分で追加することもできます。PyYAMLを使ってYAMLストレージを追加する方法を見てみましょう。


```
 import yaml
 from tinydb.table import Storage
 
 class YAMLStorage(Storage):
     def __init__(self, filename):                     # (1)
         self.filename = filename
 
     def read(self):
         with open(self.filename) as handle:
             try:
                 data = yaml.safe_load(handle.read())  # (2)
                 return data
             except yaml.YAMLError:
                 return None                           # (3)
 
     def write(self, data):
         with open(self.filename, 'w+') as handle:
             yaml.dump(data, handle)
 
     def close(self):                                  # (4)
         pass
```


1. コンストラクターは、データベースインスタンスを作成する際に TinyDB に渡されたすべての引数を受け取ります (TinyDB 自体iが使用する storageを除く)。つまり、 `TinyDB('something', storage=YAMLStorage)` を呼び出すと、 `'something'` を引数として  `YAMLStorage` に渡すことになります。

2. 信頼できない可能性のあるソースからのデータを処理する際には、PyYAML のドキュメントで推奨されているように  `yaml.safe_load` を使用します。

3. ストレージが初期化されていない場合、TinyDB はストレージが None を返すことを期待しているので、 必要な内部初期化を行うことができます。

4. インスタンスが破棄される前にストレージが何らかのクリーンアップ (ファイルハンドルのクローズなど) を必要とする場合は、 `close()` メソッドにそれを記述します。これらを実行するには、TinyDB インスタンスで  `db.close()` を実行するか、以下のようにコンテキストマネージャーとして使用する必要があります。

```
 with TinyDB('db.yml', storage=YAMLStorage) as db:
     # ...
```

ここで定義した YAMLStorage の使用方法は簡単です。

```
 db = TinyDB('db.yml', storage=YAMLStorage)
```

### カスタムミドルウェアの作成
新規にストレージモジュールを作成するのではなく、既存のストレージモジュールの動作を変更したい場合があります。
ここでは、空のアイテムをフィルタリングするミドルウェアを作ってみましょう。

ミドルウェアはストレージのラッパーとして動作するので、 `read()` と `write(data)` のメソッドが必要です。さらに、これらのミドルウェアは、 `self.storage` を介して基礎となるストレージにアクセスできます。ミドルウェアを実装する前に、ミドルウェアが受け取るデータの構造を見てみましょう。ミドルウェアを通過するデータは以下のようになっているとします。


```
 {
     '_default': {
         1: {'key': 'value'},
         2: {'key': 'value'},
         # 他のアイテム
     },
     # 他のテーブル
 }
```

このデータを処理するためには、2つのネストしたループが必要になります。

- すべてのテーブルを処理するループ
- すべてのアイテムを処理するループ

では、これを実装してみましょう。


```
 from tibydb.middlewares import Middleware
 
 class RemoveEmptyItemsMiddleware(Middleware):
     def __init__(self, storage_cls):
         # ミドルウェアは、storage_clsを使ってスーパーコンストラクタを呼び出す必要がある
         super(self).__init__(storage_cls)  　　　　　　　　# (1)
 
     def read(self):
         data = self.storage.read()
 
         for table_name in data:
             table_data = data[table_name]
 
             for doc_id in table:
                 item = table_data[doc_id]
 
                 if item == {}:
                     del table_data[doc_id]
 
         return data
 
     def write(self, data):
         for table_name in data:
             table_data = data[table_name]
 
             for doc_id in table:
                 item = table_data[doc_id]
 
                 if item == {}:
                     del table_data[doc_id]
 
         self.storage.write(data)
 
     def close(self):
         self.storage.close()
 
```

コンストラクタはミドルウェアのコンストラクタを呼び出し、ストレージクラスをミドルウェアのコンストラクタに渡していることに注意してください。（１）

この新しいミドルウェアでストレージをラップするには、次のように使います。


```
 db = TinyDB(storage=RemoveEmptyItemsMiddleware(SomeStorageClass))
```

### フックとオーバーライドの使用
カスタム ストレージを作成したり、カスタム ミドルウェアを使用したりしても、TinyDB の動作に適応させることができない場合があります。このような場合は、定義済みのフックやオーバーライドポイントを使用して、TinyDBの動作を変更することができます。例えば、 `TinyDB.default_table_name` を設定することで、デフォルトのテーブルの名前を設定できます。

```
 from tibydb import TinyDB
 TinyDB.default_table_name = 'my_table_name'
```

 `TinyDB` と  `Table` クラスは、フックとオーバーライドを使用して動作を変更することができます。 `Table` のオーバーライドを使用するには、 `TinyDB.table_class` を使用してクラスにアクセスします。

```
 TinyDB.table_class.default_query_cache_capacity = 100
```


### TinyDBとTableのサブクラス化
最後に、サブクラスを作成することでTinyDB の動作を変更することができます。これは、他の拡張メカニズムを使用するよりも、TinyDB 自体の動作をより深く変更することができます。

サブクラスを作成する際には、フックやオーバーライドを使用して、TinyDBが使用するデフォルトのクラスをオーバーライドして使用することができます。


```
 from tinydb.table import Table
 
 class MyTable(Table):
     # オーバーライドするメソッド
     # ...
 
 TinyDB.table_class = MyTable
 
```

TinyDBのソースコードには、拡張機能を念頭に置いて文書化されているため、内部のメソッドやクラスなど、すべての動作が説明されています。

## TinyDB-Baseを使ってみる
TinyDBを使うとすぐに気づくことなのですが、データベース接続で毎回同じようなコードを記述する必要があります。
[TinyDB-Base ](https://github.com/MechaCoder/tinydb-baseClass)を使うと、ベースクラスが提供され、ルート・オブジェクトとテーブルの両方を同じオブジェクトで操作することができコードが簡潔になって読みやすくなります。

### インストール
 bash
```
 $ pip install tinydb-baseClass
```


### Factoryクラス
Factoryクラスを使う、Tinydbと、ルート・オブジェクトとテーブルの両方を同じオブジェクトで操作することができます。


```
 In [2]: # %load 80_factory.py
    ...: from tinydb_usersetup import *
    ...: from tinydb_base import Factory
    ...:
    ...: database_initialized()
    ...:
    ...: db = Factory('usergroup.json', 'group')
    ...: v1 = db.db          # TinyDBと同じ
    ...: v2 = db.tbl         # TinyDB.Tableと同じ
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # db.close()
    ...:
 
 In [3]: print(v1)
 <TinyDB tables=['group', '_default'], tables_count=2, default_table_documents_count=4, all_tables_documents_count=['group=3', '_default=4']>
 
 In [4]: print(v2)
 <Table name='group', total=3, storage=<tinydb.storages.JSONStorage object at 0x111815a30>>
 
 In [5]: db.close()
 Out[5]: True
 
```

### DatabaseBaseクラス
DatabaseBaseクラスをインポートして、それを自分のクラスに派生させた独自クラスを作成して、アプリケーションに必要な機能をうまく処理することができます。データレイヤーを簡単に実装することができます。

例えばタスクリストを管理するデータベースを考えてみます。
次のようなモデルクラスを作成するだけなので簡単です。

```
 In [2]: # %load 81_baseclass.py
    ...: from tinydb_base import DatabaseBase
    ...:
    ...: class Task(DatabaseBase):
    ...:
    ...:     def __init__(self,
    ...:         file='tasks.json',
    ...:         table='tasks',
    ...:         requiredKeys='title:str,item:str,quantity:int'):
    ...:         super().__init__(file=file,
    ...:                          table=table,
    ...:                          requiredKeys=requiredKeys)
    ...:
    ...: task = Task()
    ...: task.create({'title': 'Buy Beer', 'item': 'Badweiser', 'quantity':1})
    ...: # task.readAll()
    ...:
 Out[2]: 1
 
 In [3]: task.readAll()
 Out[3]: [{'title': 'Buy Beer', 'item': 'Badweiser', 'quantity': 1}]
 
 
```
 `requiredKeys` 引数でカラムを定義します。


 DatabaseBaseクラスのメソッド

| メソッド | 引数 | 説明 |
|:--|:--|:--|
| create(dict,pw) | 辞書型データ, パスワード | データベースに新しい行をひとつ追加する |
| createMultiple(dict_list) | 辞書型データのリスト | データベースに複数行を追加する |
| createObj() |  | Factoryオブジェクトを返 |
| readAll(pw) | パスワード | オブジェクトのリストを返す |
| readById(id) | ドキュメントID | 指定したドキュメントIDの行を取得する |
| removeById(id) | ドキュメントID | 指定したドキュメントIDの行を削除する |
| clear() |  | テーブルにある全てのデータを削除する |
| exists(tag, value) | タグ、値 | タグと値のペアのデータが存在するかチェックして真偽値を返す |
| now_ts() |  | UNIXのエポックタイムを返す(浮動小数点) |


### DatabaseBaseSecureクラス
DatabaseBaseSecureクラスは、DatabaseBaseクラスと全く同じように機能しますが、Fernetモジュールを使って暗号化できるソルト値を提供します。それでも、独自のソルトを定義する方が安全であることは理解しておきましょう。

```
 In [2]: # %load 82_basssecure.py
    ...: from tinydb_base.cryptography import DatabaseBaseSercure
    ...:
    ...: class Diary(DatabaseBaseSercure):
    ...:
    ...:     def __init__(self,
    ...:         file='diary.json',
    ...:         table='diary',
    ...:         requiredKeys='title,content',
    ...:         salt='salt'):
    ...:         super().__init__(file=file,
    ...:                          table=table,
    ...:                          requiredKeys=requiredKeys,
    ...:                          salt=salt)
    ...:
    ...: diary = Diary(salt='this_is_my_salt')
    ...: diary.create({'title': '2021-08-08', 'content': "Open Lion's Gate"},
    ...:              'myp@ssw0rd')
    ...: # diary.readAll('myp@ssw0rd')
    ...:
 Out[2]: 1
 
 In [3]: diary.readAll('myp@ssw0rd')
 Out[3]: [{'doc_id': 1, 'title': '2021-08-08', 'content': "Open Lion's Gate"}]
 
 In [4]: diary.readAll()
 ---------------------------------------------------------------------------
 TypeError                                 Traceback (most recent call last)
 <ipython-input-4-f12a0a45b491> in <module>
 ----> 1 diary.readAll()
 
 TypeError: readAll() missing 1 required positional argument: 'pw'
 
 In [5]: diary.readAll('mypass')
 Out[5]: [{'doc_id': 1}]
 
 In [6]: !cat diary.json
 {"diary": {"1": {"gAAAAABhExI_FvpdzYVzzwbE9D0w368l5mTDI0VQnO3Yf5qAo1JU6E0PpOvUoer2qRONfgatry9iCFevydA2S68WHY9ShurqiQ==": "gAAAAABhExI_xPzho9YjouHMDWpUyQkk55s_wm5w9oh-I-eQi5cSHJYfOT5AjxTAjCG_lTTuGNFzcQEmpSjQdpZN5QL8LGZBpQ==", "gAAAAABhExI_lNz0RuxKvv8XACP42NePQlu0TdhrCLnieiZjE6BoTi9KNKaYq4JHylu1TjqwTL2nbtaKt2fXbqdWi475tg9zrw==": "gAAAAABhExI_QgtVRMrAx1Bl9KGt3ilfQkUfaRXNI6UWWDoN7vV9maKeurnyFghmXIxzaK4ShzDAs0s2Z2BOh-_4DqL2j-5MZwwMFYMNHTQm1AtqZRMTGoo="}}}
```

 `create()` と `readAll()` ともにパスワードを与える必要があります。

この例では、例示が目的なのでパスワードを平文でコード中にハードコーディングしていますが、実際のアプリケーションでは、python-dotenv や pidantic などを使って環境変数や外部の構成ファイルに’記述する方が安全になります。


 DatabaseBaseSecureクラスのメソッド

| メソッド | 引数 | 説明 |
|:--|:--|:--|
| create(dict) | 辞書型データ | データベースに新しい行を１つ追加する |
| createMultiple(dict_list) | 辞書型データのリスト | this added multiple rows |
| readAll |  | オブジェクトのリストを返す |
| readById(id) | ドキュメントID | 指定したドキュメントIDの行を取得する |
| removeById(id) | ドキュメントID | 指定したドキュメントIDの行を削除する |
| clear |  | テーブルにある全てのデータを削除する |

### Userクラス
多くのアプリケーションで必要とされるのは、ユーザーコンポーネントの処理です。これは、ユーザーの作成を可能にするシンプルなクラスで、DatabaseBaseを継承したクラスですが、ユーザーに関連する特殊なメソッドを持っています。
データベース名のデフォルトは  `ds.json` ですが、Userクラスに `file` 引数でデータベースのファイル名を与えることができます。

```
 In [2]: # %load 83_user.py
    ...: from tinydb_base import User
    ...:
    ...: usrTable = User(file='user_db.json')
    ...:
    ...: # usrTable.makeUser('jack', 'thinkBig')
    ...: # usrTable.authUser('jack', 'thinkBig')
    ...: # usrTable.authUser('jack', '!mypassword')
    ...:
 
 In [3]: usrTable.makeUser('jack', 'thinkBig')
 Out[3]: 1
 
 In [4]: usrTable.authUser('jack', 'thinkBig')
 Out[4]: True
 
 In [5]: usrTable.authUser('jack', '!mypassword')
 Out[5]: False
 
 In [6]: !cat user_db.json
 {"users": {"1": {"username": "jack", "password": "641343fa43c038240332f7414970e667adfa745e30c8c9f1cba35a2eec732b4da80d7b1a5fcdd9a5693f85cd924c1d5892b36f73eff7ab1f905c3497ca4ca534"}}}
 
```

 Userクラスのメソッド

| メソッド | 引数 | 説明 |
|:--|:--|:--|
| makeUser(username, password) | ユーザ名、パスワード | ユーザを作成する |
| testUser(userid, password) | ユーザID、パスワード | ユーザIDを持つユーザが存在するかチェックして真偽値を返す |
| authUser(username,, password) | ユーザ名、パスワード | ユーザ名とパスワードで認証を行って結果を真偽値で返す |

### GetSetクラス
GetSetクラス、タグに基づいて値を設定したり取得したりすることができる、非常にシンプルなインターフェイスです。
構成ファイルなどの利用に便利です。

```
 In [2]: # %load 84_getset.py
    ...: from tinydb_base.getSet import GetSet
    ...:
    ...: class Settings(GetSet):
    ...:
    ...:     def __init__(self,
    ...:                  file: str = 'config.json',
    ...:                  table: str = __name__):
    ...:         super().__init__(file=file, table=table)
    ...:
    ...: config = Settings()
    ...: config.set('logfile', '/tmp/sample.log')
    ...: # config.get('logfile')
    ...:
    ...:
 Out[2]: 1
 
 In [3]: config.set('logfile', '/tmp/sample.log')
 Out[3]: 1
 
 In [4]: config.get('logfile')
 Out[4]: '/tmp/sample.log'
 
 In [5]: !cat config.json
 {"__main__": {"1": {"tag": "logfile", "val": "/tmp/sample.log", "timeout": null}}}
```

構成ファイルなどでは、デフォルトの値が設定されていると便利はときがあります。こうしたように、データベースにキーに該当する値が設定されていることが必要な場合は、デフォルトキーを設定することができます。


```
 In [2]: # %load 85_defaultkey.py
    ...: from tinydb_base.getSet import GetSet
    ...:
    ...: class Settings(GetSet):
    ...:
    ...:     def __init__(self,
    ...:                  file: str = 'config.json',
    ...:                  table: str = __name__):
    ...:         super().__init__(file=file, table=table)
    ...:         self.defaultRows({
    ...:             'logfile': 'tmp/sample.log'
    ...:         })
    ...:
    ...: config = Settings()
    ...: # config.get('logfile')
    ...:
    ...:
 
 In [3]: config.get('logfile')
 Out[3]: 'tmp/sample.log'
```


### 有効期限の設定
 `futureTimeStamp()` 関数を使ってデータベースの値に有効期限を設定することができます。指定した時間を超えるデータベースからデータは削除されます。これはsetメソッドに渡される引数によって管理されます。

```
 In [1]: %load 86_timeout.py
 
    ...: from time import sleep
    ...: from tinydb_base.getSet import GetSet, futureTimeStamp
    ...: from tinydb_base.exceptions import RowNotFound_Exception
    ...:
    ...: class Settings(GetSet):
    ...:
    ...:     def __init__(self,
    ...:                  file: str = 'config.json',
    ...:                  table: str = __name__):
    ...:         super().__init__(file=file, table=table)
    ...:
    ...: config = Settings()
    ...: v1 = config.set('api-key', 'this_is_APIKEY', futureTimeStamp(second=10))
    ...: v2 = config.get('api-key')
    ...: sleep(20)
    ...: try:
    ...:     v3 = config.get('api-key')
    ...: except RowNotFound_Exception:
    ...:     v3 = None
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v3)
    ...:
 
 In [3]: print(v1)
 1
 
 In [4]: print(v2)
 this_is_APIKEY
 
 In [5]: print(v3)
 None
 
```

 `futureTimeStamp()` には次の引数に数値(int型)で有効期限を設定することができます。

  - day
  - month
  - year
  - hour
  - minute
  - second

### GetSetSercureクラス
GetSetSercureクラスは、GetSetクラスと全く同じように機能しますが、Fernetモジュールを使って暗号化できるソルト値を提供します。(GetSetSecure ではなく　GetSetSercure なので注意：おそらくバグ)


```
 In [2]: # %load 86_getsetsecure.py
    ...: from tinydb_base.getSetSercure import GetSetSercure as GetSetSecure
    ...:
    ...: class Settings(GetSetSecure):
    ...:
    ...:     def __init__(self,
    ...:                  file: str = 'config_secure.json',
    ...:                  table: str = __name__,
    ...:                  salt: str = 'this_is_my_salt',
    ...:                  pw: str = 'I_love_IPA'):
    ...:         super().__init__(file=file, table=table, salt=salt, pw=pw)
    ...:
    ...: config = Settings()
    ...: config.set('password', 'myp@ssw0rd')
    ...: # config.get('password')
    ...:
    ...:
 Out[2]: True
 
 In [3]: config.get('password')
 Out[3]: 'myp@ssw0rd'
 
 In [4]: !cat config_secure.json
 {"__main__": {"1": {"tag": "gAAAAABhEyB4h9EqPGN85IEP93YP36VNmDthQ8FXLu4WrzBlJgMB5jjoh-wy9YGUG3t08vASn7MaQgz0fSIKC2J5kVh7UWNK7g==", "val": "gAAAAABhEyB4dm-E_oZ0BSb0-__40fwqZ6V3Q_YMNluOFSuvp7bXY6Gd6CLpqR7Q1Kz7jdWk_GbwQWKkWHNV60L2DrDe8gYOSw=="}}}
```

### テーブルのデータをファイルへのエクスポート
関数  `jsonExport()` 、  `ymalExport` は、ドキュメントのリストをJSONまたはYAMLフォーマットにエクスポートします。これらの関数は、ドキュメントのリストとエクスポートするファイルパスを受け取ります。
(yamlExport ではなく ymalExport であることに注意：おそらくバグ)


```
 In [1]: %load 88_exporting.py
 
    ...: from tinydb_base import DatabaseBase
    ...: from tinydb_base.exporter import jsonExport
    ...: from tinydb_base.exporter import ymalExport as yamlExport
    ...:
    ...: class MyDB(DatabaseBase):
    ...:     def __init__(self,
    ...:         file: str ='mydb.json',
    ...:         table: str ='tasks',
    ...:         requiredKeys: str ='title:str,data:int'):
    ...:         super().__init__(file=file,
    ...:                          table=table,
    ...:                          requiredKeys=requiredKeys)
    ...:
    ...: db = MyDB()
    ...: for index in range(0, 10):
    ...:     db.create({'title': f'data_{index}', 'data': index})
    ...:
    ...: v1 = jsonExport(db.readAll(), 'jsonData.json')
    ...: v2 = yamlExport(db.readAll(), 'yamlData.yaml')
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # !cat jsonData.json
    ...: # !cat yamlData.json
    ...:
 
 In [3]: print(v1)
 jsonData.json
 
 In [4]: print(v2)
 yamlData.yaml
 
 In [5]: !cat jsonData.json
 {
     "data": [
         {
             "data": 0,
             "documentId": 1,
             "title": "data_0"
         },
         {
             "data": 1,
             "documentId": 2,
             "title": "data_1"
         },
         {
             "data": 2,
             "documentId": 3,
             "title": "data_2"
         },
         {
             "data": 3,
             "documentId": 4,
             "title": "data_3"
         },
         {
             "data": 4,
             "documentId": 5,
             "title": "data_4"
         },
         {
             "data": 5,
             "documentId": 6,
             "title": "data_5"
         },
         {
             "data": 6,
             "documentId": 7,
             "title": "data_6"
         },
         {
             "data": 7,
             "documentId": 8,
             "title": "data_7"
         },
         {
             "data": 8,
             "documentId": 9,
             "title": "data_8"
         },
         {
             "data": 9,
             "documentId": 10,
             "title": "data_9"
         }
     ],
     "export-ts": "11:05 - 11/08/2021"
 }
 In [6]: !cat yamlData.yaml
 data:
 - data: 0
   documentId: 1
   title: data_0
 - data: 1
   documentId: 2
   title: data_1
 - data: 2
   documentId: 3
   title: data_2
 - data: 3
   documentId: 4
   title: data_3
 - data: 4
   documentId: 5
   title: data_4
 - data: 5
   documentId: 6
   title: data_5
 - data: 6
   documentId: 7
   title: data_6
 - data: 7
   documentId: 8
   title: data_7
 - data: 8
   documentId: 9
   title: data_8
 - data: 9
   documentId: 10
   title: data_9
 export-ts: 11:05 - 11/08/2021
 
```


## TinyDBの拡張モジュール
前述の TInyDB-Baseのように、TinyDBをサポートするたくさんの有益な拡張モジュールがあります。

### TinyDB-Base
ソースコード：https://github.com/MechaCoder/tinydb-baseClass
ステータス：stable
説明：TinyDBを利用したベースクラスを提供するもの。コードの記述が軽減されます。

### tinyindex
ソースコード： https://github.com/eugene-eeo/tinyindex
ステータス： 実験的
説明： TinyDB 用のドキュメントインデックスです。テーブルに変更がない限り決定論的
なドキュメントの生成を保証します。

### tinymongo
ソースコード： https://github.com/schapman1974/tinymongo
ステータス： 実験的
説明： TinyDBをMongoDBをフラットファイルとして使用できるようにするシンプルなラッ
パーです。

### TinyMP
ソースコード： https://github.com/alshapton/TinyMP
ステータス： stable
説明： MessagePack ベースの tinydb のストレージ拡張です。(http://msgpack.org)

### tinyrecord
ソースコード： https://github.com/eugene-eeo/tinyrecord
ステータス： stable
説明：
Tinyrecord は、アトミックトランザクションのサポートを
TinyDB NoSQL データベースに実装したライブラリです。
record-first then execute アーキテクチャを使用しており、
スレッドロック内にいる時間を最小限に抑えることができます。

### tinydb-appengine
ソースコード： https://github.com/imalento/tinydb-appengine
ステータス： stable
説明： tinydb-appengine は App Engine 用の TinyDB ストレージを提供します。
JSON の readonly を使用することができます。

### tinydb-serialization
ソースコード： https://github.com/msiemens/tinydb-serialization
ステータス： stable
説明： tinydb-serialization は、他の方法では TinyDB が処理できないオブジェクトの
シリアライゼーションを提供します。

### tinydb-smartcache
ソースコード： https://github.com/msiemens/tinydb-smartcache
ステータス： stable
説明： tinydb-smartcache は、TinyDB 用のスマートなクエリキャッシュを提供します。
ドキュメントの挿入/削除/更新時にクエリキャッシュを更新するので、
キャッシュが無効になることはありません。データの変更が少ないのに多くのクエリを実
行する場合に便利りなります。


### aiotinydb
ソースコード： https://github.com/ASMfreaK/aiotinydb
ステータス： stable
説明： TinyDB の asyncio 互換シムです。非同期を意識したコンテキストで、遅い同期IOなしでTinyDBを使用できるようにします。

### TinyDBTimestamps
ソースコード： https://github.com/pachacamac/TinyDBTimestamps
ステータス： 実験的
説明： TinyDB ドキュメントで  `create at` / `update at` のタイムスタンプを自動追加します。



## まとめ
TinyDB は、Pythonだけで動作するためデータベースなど別のミドルウェアを起動する必要がなく、手軽に利用することができます。また、データ取得時ではORMのようにクエリを使用できることから学習国ストが低くなるだけでなく、SQLiteやDatasetでは難しかった正規表現を使ったクエリを記述できるためコードが簡潔になり判読性も向上します。
しかしながら、SQLiteをドロップインリプレースするようなものではないため、


## 参考資料
　[TinyDB公式ドキュメント ](https://tinydb.readthedocs.io/en/latest/)
　[設定ファイルを考えてみよう]


previous: [pickleDBを使ってみよう]
next: [ZODBを使ってみよう]
#Pythonセミナーデータベース編

