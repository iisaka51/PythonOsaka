datasetを使ってみよう
=================
![](https://gyazo.com/a8cd7d9c457a5a8103f4c97e7f4ee4f4.png)

## dataset について
Python でデータベースを利用したアプリケーションを作成することはよくありますが、データベースサービスを安定して維持することは非常にコストが高いものとなります。そのため、ちょっとだけ便利になればよいというレベルではなかなかデータベースを採用しにくいものです。

>**公式ドキュメントから**
>  リレーショナルデータベースでデータを管理することには多くの利点があります。しかし、小・中規模のデータセットを扱う日常業務ではほとんど使われません。それはなぜでしょうか？　なぜ、CSVやJSON形式の静的なファイルに保存されているデータが非常に多いのでしょうか？
>
> その答えは、プログラマーは怠け者であり、見つけたソリューションのなかで最も簡単な方法を好む傾向があるからです。そしてPythonでは、データベースは構造化されたデータセットを保存するための最も簡単なソリューションではありません。
> これを変えようとしているのがdatasetです。

dataset には次のような特徴があります。

- **自動スキーマ(Automatic schema)**：データベースに存在しないテーブルやカラムが書き込まれた場合、自動的に作成される
- **アップサート(Upsert)**：既存のバージョンが見つかるかどうかに応じて、レコードが作成または更新される。
- **クエリヘルパー(Query helpers )**：テーブルのすべての行や、一連のカラムのすべての値を検索するなど、シンプルなクエリを実行します。
- **互換性(Compatibility)**：SQLAlchemyの上に構築されているので、データセットは、SQLite、PostgreSQL、MySQLなどの主要なデータベースで動作します。


## インストール
dataset のインストールは次のように pip で行います。

 bash
```
 $ pip install dataset
```

## 簡単な使用方法

dataset の使い方は次のようになります。


```
 In [2]: # %load 01_sample.py
    ...: import dataset
    ...:
    ...: db = dataset.connect('sqlite:///:memory:')
    ...:
    ...: table = db['users']
    ...: table.insert(dict(name='Jack Bauer', age=55))
    ...: table.insert(dict(name='Jack Bauer', age=55, belongs='CTU'))
    ...:
    ...: jack = table.find_one(name='Jack Bauer')
    ...:
    ...: # print(jack)
    ...:

 In [3]: print(jack)
 OrderedDict([('id', 1), ('name', 'Jack Bauer'), ('age', 55), ('belongs', None)])

```

同じ処理を SQLite で記述すると次のようになります。

```
 In [1]: %load 02_sample_sqlite3.py

    ...: import sqlite3
    ...:
    ...: conn = sqlite3.connect(':memory:')
    ...: c = conn.cursor()
    ...:
    ...: c.execute('CREATE TABLE IF NOT EXISTS users (name, age INTEGER)')
    ...: conn.commit()
    ...:
    ...: c.execute('INSERT INTO users values (?, ?) ', ('Jack Bauer', 55))
    ...: conn.commit()
    ...:
    ...: c.execute('ALTER TABLE users ADD COLUMN belongs TEXT')
    ...: conn.commit()
    ...:
    ...: c.execute('INSERT INTO users values (?, ?, ?) ', ('Jack Bauer', 55, 'CTU
    ...: '))
    ...: conn.commit()
    ...:
    ...: c.execute('SELECT name, age FROM users WHERE name = ?', ('Jack Bauer', )
    ...: )
    ...: row = list(c)[0]
    ...: jack = dict(name=row[0], age=row[1])
    ...:
    ...: # print(jack)
    ...:

 In [3]: print(jack)
 {'name': 'Jack Bauer', 'age': 55}

```

簡単かつスッキリと記述できることをわかっていただけるでしょう。

## DSN

 `データベース+ドライバ://...` "という書式で構成される文字列を**DSN(Data Source Name)**として `connect()` に与えます。
これは、SQLAlchemy で使用されるDSNと同じです。

#### SQLite データベースへの接続

```
 db = dataset.connect('sqlite:///mydatabase.db')
```

#### MySQLデータベースへの接続

```
 db = dataset.connect('mysql://user:password@localhost/mydatabase')
```

#### PostgreSQデータベースへの接続

```
 db = dataset.connect('postgresql://scott:tiger@localhost:5432/mydatabase')
```

## データベースとの切断
通常のORMであれば、  `close()` を呼び出すことでデータベースとのコネクションを切ることができますが、dataset は少しクセがあって  `close()` だけを呼び出しても、コネクションが切断されません。
明示的に次のようにすることで、任意のタイミングでデータベースとのコネクションを切断することができます。


```
 db.executable.invalidate()
 db.executable.engine.dispose()
 db.close()
```

## データの保存
データを保存するには、テーブルへの参照を取得する必要がありますが。テーブルがすでに存在しているかどうかは気にする必要はありません。


```
 table = db['user']
```

このあと、テーブルにデータを格納するのは、関数 `insert()` に辞書を渡す呼び出しをを1回行うだけです。
ここで、テーブルに `name` と `age` などのカラムを作る必要はありません。datasetが自動的に作成してくれます。


```
 table.insert(dict(name='Jack Bauer', age=55, belons='CTU'))

```

追加したデータに別のカラムがあるときもそのまま `insert()` を呼び出すだけです。
データベースへの反映は、datasetが自動的に処理してくれます。
ただし、カラムが増えますが値は `None` とされます。

```
 In [2]: # %load 03_add_columns.py
    ...: import dataset
    ...:
    ...: db = dataset.connect('sqlite:///:memory:')
    ...:
    ...: table = db['users']
    ...: table.insert(dict(name='Jack Bauer', age=55))
    ...: v1 = table.find_one(name='Jack Bauer')
    ...:
    ...: table.insert(dict(name='David Gilmour', age=75, belongs='PinkFloyd'))
    ...: v2 = table.find_one(name='David Gilmour')
    ...: v3 = table.find_one(name='Jack Bauer')
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v3)
    ...:

 In [3]: print(v1)
 OrderedDict([('id', 1), ('name', 'Jack Bauer'), ('age', 55)])

 In [4]: print(v2)
 OrderedDict([('id', 2), ('name', 'David Gilmour'), ('age', 75), ('belongs', 'PinkFloyd')])

 In [5]: print(v3)
 OrderedDict([('id', 1), ('name', 'Jack Bauer'), ('age', 55), ('belongs', None)])

```


## データの更新
既存データの更新も簡単です。
 `update()` の第１引数に変更後のデータと絞り込むための情報を設定します。。2番目の引数で与えたカラムのリストで絞り込みます。それぞれのデータに自動的に付与される `id` カラムを使用することもできます。

```
 table.update(dict(id=1, name='John Doe', age=47), ['id'])
```

## キャッシュ
データを読み出すとキャッシュされます。同じクエリ条件で読み出すとデータベースにアクセスすることなく、キャッシュされたものを返します。場合によっては期待どおりにならないことがあるので注意が必要です。

```
 In [2]: # %load 04_cache.py
    ...: import dataset
    ...:
    ...: db = dataset.connect('sqlite:///:memory:')
    ...:
    ...: table = db['users']
    ...: table.insert(dict(name='Jack Bauer', age=55))
    ...: v1 = table.find_one(name='Jack Bauer')
    ...:
    ...: table.insert(dict(name='Jack Bauer', age=55, belongs='CTU'))
    ...: v2 = table.find_one(name='Jack Bauer')
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:

 In [3]: print(v1)
 OrderedDict([('id', 1), ('name', 'Jack Bauer'), ('age', 55)])

 In [4]: print(v2)
 OrderedDict([('id', 1), ('name', 'Jack Bauer'), ('age', 55), ('belongs', None)])

```

データベースが変更になる作業を行う場合は、次で説明するコミットを行う必要があります。

## トランザクション
データベースへの一連の更新を1つのトランザクションにまとめることができます。その場合、すべての更新が一度にコミットされ、例外が発生した場合はすべての更新が取り消されます。トランザクションはコンテキストマネージャでサポートされているため、 `with` 文で使用することができます。

```
 with dataset.connect() as tx:
     tx['user'].insert(dict(name='Jack Bauer', age=55, belongs='CTU'))
```

これと同じ機能は、 `begin()` 、 `commit()` 、 `rollback()` のメソッドを明示的に呼び出すことでも実現することができます。

```
 db = dataset.connect()
 db.begin()
 try:
     db['user'].insert(dict(name='Jack Bauer', age=55, belongs='CTU'))
     db.commit()
 except:
     db.rollback()
```

トランザクションはネストさせることもできます。

```
 db = dataset.connect()
 with db as tx1:
     tx1['user'].insert(dict(name='Jack Bauer', age=55, belongs='CTU'))
     with db as tx2:
         tx2['user'].insert(dict(name='Jack Bauer', age=55, belongs='CTU', gender='female'))
```


## データベースとテーブルの確認
未知のデータベースを扱う際には、まずその構造を確認したいと思うかもしれません。はじめに、データベースにどのようなテーブルが格納されているのかを調べてみましょう。

```
 >>> print(db.tables)
 ['user']
```

テーブルに含まれるカラムを確認しましょう。

```
 >>> db['users'].columns
 ['id', 'name', 'age', 'belons']
```

データベースに格納されているレコード数を確認するためには `len()` を使います。

```
 >>> len(db['users'])
 1
```

> **注意**
> dataset がスキームレスでデータベースを作成できるメリットとデメリットがあります。
> テーブルやカラムに指定するキーの文字列を間違えないようにしてください。
> もし間違えてしまうと、そのテーブルやカラムが作成されてしまいます。


## データの読み込み
テストのためのデータを用意します。
 test_data.py
```
 test_data = [
     { 'name': 'Jack Bauer',
       'age': 55,
       'belongs': 'CTU'
     },
     { 'name': "Chloe O'Brian",
       'age': 0,
       'belongs': 'CTU'
     },
     { 'name': 'Anthony Tony',
       'age': 29,
       'belongs': 'CTU'
     },
     { 'name': 'David Gilmour',
       'age': 75,
       'belongs': 'Pink Floyd'
     },
     { 'name': 'Ann Wilson',
       'age': 71,
       'belongs': 'Heart'
     },
     { 'name': 'Nacy Wilson',
           'age': 67,
           'belongs': 'Heart'
     },
 ]
```

データベース  `users.sqlite` を、以降のサンプルで何度もアクセスすることになるので次のようなモジュールを用意します。
 testsdb.py
```
 import dataset

 db = dataset.connect('sqlite:///users.sqlite')
 table = db['users']

 if __name__ == '__main__':
     try:
         from test_data import test_data
     except ModuleNotFoundError as msg:
         import sys
         print(msg)
         sys.exit(0)

     for t in test_data:
         table.insert(t)

     db.commit()
     db.close()
```

データベースを初期化するために、このモジュールを実行しておきます。
 bash
```
 $ python testdb.py
```

データベースのテーブルからすべてのデータを読み出すためには `all()` を呼び出します。テーブルはイテレートオブジェクトになるので `for` 文で処理することもできます。

```
 In [2]: # %load 10_all.py
    ...: from testdb import *
    ...:
    ...: v1 = table.all()
    ...:
    ...: def func():
    ...:     for user in table.all():
    ...:         print(user)
    ...:
    ...: # print(v1)
    ...: # func()
    ...:

 In [3]: print(v1)
 <dataset.util.ResultIter object at 0x107755a00>

 In [4]: func()
 OrderedDict([('id', 1), ('name', 'Jack Bauer'), ('age', 55), ('belongs', 'CTU')])
 OrderedDict([('id', 2), ('name', "Chloe O'Brian"), ('age', 0), ('belongs', 'CTU')])
 OrderedDict([('id', 3), ('name', 'Anthony Tony'), ('age', 29), ('belongs', 'CTU')])
 OrderedDict([('id', 4), ('name', 'David Gilmour'), ('age', 75), ('belongs', 'Pink Floyd')])
 OrderedDict([('id', 5), ('name', 'Ann Wilson'), ('age', 71), ('belongs', 'Heart')])
 OrderedDict([('id', 6), ('name', 'Nacy Wilson'), ('age', 67), ('belongs', 'Heart')])

```

特定のエントリを  `find()` と  `find_one()` で絞り込むことができます。

```
 In [2]: # %load 12_find_advancefilter.py
    ...: from testdb import *
    ...:
    ...: v1 = table.find(age={'<=': '55'})
    ...: v2 = table.find(age={'<': '30'})
    ...: v3 = table.find(age={'>': '70'})
    ...: v4 = table.find(age={'>=': '71'})
    ...: v5 = table.find(age={'=': '0'})
    ...: v6 = table.find(age={'!=': '0'})
    ...: v7 = table.find(age={'between': [1, 60]})
    ...: v8 = table.find(name={'like': '%Wilson'})
    ...: v9 = table.find(name={'ilike': '%WILSON'})
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(d)
    ...:
    ...: # func(v1)
    ...:

 In [3]: func(v1)
 OrderedDict([('id', 1), ('name', 'Jack Bauer'), ('age', 55), ('belongs', 'CTU')])
 OrderedDict([('id', 2), ('name', "Chloe O'Brian"), ('age', 0), ('belongs', 'CTU')])
 OrderedDict([('id', 3), ('name', 'Anthony Tony'), ('age', 29), ('belongs', 'CTU')])

 In [4]: func(v2)
 OrderedDict([('id', 2), ('name', "Chloe O'Brian"), ('age', 0), ('belongs', 'CTU')])
 OrderedDict([('id', 3), ('name', 'Anthony Tony'), ('age', 29), ('belongs', 'CTU')])

 In [5]: func(v3)
 OrderedDict([('id', 4), ('name', 'David Gilmour'), ('age', 75), ('belongs', 'Pink Floyd')])
 OrderedDict([('id', 5), ('name', 'Ann Wilson'), ('age', 71), ('belongs', 'Heart')])

 In [6]: func(v4)
 OrderedDict([('id', 4), ('name', 'David Gilmour'), ('age', 75), ('belongs', 'Pink Floyd')])
 OrderedDict([('id', 5), ('name', 'Ann Wilson'), ('age', 71), ('belongs', 'Heart')])

 In [7]: func(v5)
 OrderedDict([('id', 2), ('name', "Chloe O'Brian"), ('age', 0), ('belongs', 'CTU')])

 In [8]: func(v6)
 OrderedDict([('id', 1), ('name', 'Jack Bauer'), ('age', 55), ('belongs', 'CTU')])
 OrderedDict([('id', 3), ('name', 'Anthony Tony'), ('age', 29), ('belongs', 'CTU')])
 OrderedDict([('id', 4), ('name', 'David Gilmour'), ('age', 75), ('belongs', 'Pink Floyd')])
 OrderedDict([('id', 5), ('name', 'Ann Wilson'), ('age', 71), ('belongs', 'Heart')])
 OrderedDict([('id', 6), ('name', 'Nacy Wilson'), ('age', 67), ('belongs', 'Heart')])

 In [9]: func(v7)
 OrderedDict([('id', 1), ('name', 'Jack Bauer'), ('age', 55), ('belongs', 'CTU')])
 OrderedDict([('id', 3), ('name', 'Anthony Tony'), ('age', 29), ('belongs', 'CTU')])

 In [10]: func(v8)
 OrderedDict([('id', 5), ('name', 'Ann Wilson'), ('age', 71), ('belongs', 'Heart')])
 OrderedDict([('id', 6), ('name', 'Nacy Wilson'), ('age', 67), ('belongs', 'Heart')])

 In [11]: func(v9)
 OrderedDict([('id', 5), ('name', 'Ann Wilson'), ('age', 71), ('belongs', 'Heart')])
 OrderedDict([('id', 6), ('name', 'Nacy Wilson'), ('age', 67), ('belongs', 'Heart')])

```

次のの２つの例は同じ結果となりますが、後者はSQLAlchemy のクエリをそのまま記述しています。

```
 In [2]: # %load 13_sqlalchemy_query.py
    ...: from testdb import *
    ...:
    ...: v1 = table.find(age={'=': '0'})
    ...: v2 = table.find(table.table.columns.age == 0)
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(d)
    ...:
    ...: # func(v1)
    ...:

 In [3]: func(v1)
 OrderedDict([('id', 2), ('name', "Chloe O'Brian"), ('age', 0), ('belongs', 'CTU')])

 In [4]: func(v2)
 OrderedDict([('id', 2), ('name', "Chloe O'Brian"), ('age', 0), ('belongs', 'CTU')])

```

次の２つは同じ結果となります。表記方法が違うだけです。

```
 In [2]: # %load 14_notation.py
    ...: from testdb import *
    ...:
    ...: v1 = table.find(age=0)
    ...: v2 = table.find(age={'=': '0'})
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(d)
    ...:
    ...: # func(v1)
    ...:

 In [3]: func(v1)
 OrderedDict([('id', 2), ('name', "Chloe O'Brian"), ('age', 0), ('belongs', 'CTU')])

 In [4]: func(v2)
 OrderedDict([('id', 2), ('name', "Chloe O'Brian"), ('age', 0), ('belongs', 'CTU')])

```

 `IN` に相当する記述は次のようになります。

```
 In [2]: # %load 15_in.py
    ...: from testdb import *
    ...:
    ...: v1 = table.find(belongs=('Pink Floyd', 'Hear'))
    ...: v2 = table.find(belongs={'in': ('Pink Floyd', 'Hear')})
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(d)
    ...:
    ...: # func(v1)
    ...:

 In [3]: func(v1)
 OrderedDict([('id', 4), ('name', 'David Gilmour'), ('age', 75), ('belongs', 'Pink Floyd')])

 In [4]: func(v2)
 OrderedDict([('id', 4), ('name', 'David Gilmour'), ('age', 75), ('belongs', 'Pink Floyd')])

```

 datasetで使用する演算子

| 演算子 |  説明 |
|:--|:--|
| gt, >  | より大きい |
| lt, < | より小さい |
| gte, >= | 以上 |
| lte, <=  | 以下 |
| !=, <>, not | 比較した値が異なる |
| in |  与えたシーケンスに含まれる |
| notin | 与えたシーケンスに含まれない |
| like, ilike | 文字列検索、 ilike は大文字小文字を区別しない。ワイルドカードは% |
| notlike |  パターンに合致する文字列が存在しないかチェック |
| between, .. |  値が与えたタプルの間の値 |
| startswith |  与えた文字列で始まっている文字列 |
　endswith	 与えた文字列で終わっている文字列


 `distinct()` を使うと、1つまたは複数のカラムでユニークな値を持つ行のセットを取得できます。


```
 In [2]: # %load 16_distinct.py
    ...: from testdb import *
    ...:
    ...: v1 = table.distinct('belongs')
    ...:
    ...: def func(data):
    ...:     for p in data:
    ...:         print(p)
    ...:
    ...: # print(v1)
    ...: # func(v1)
    ...:

 In [3]: print(v1)
 <dataset.util.ResultIter object at 0x105f7fc70>

 In [4]: func(v1)
 OrderedDict([('belongs', 'CTU')])
 OrderedDict([('belongs', 'Heart')])
 OrderedDict([('belongs', 'Pink Floyd')])

```

これまでの例では、結果データは辞書型で返されていました。datasetでは、 `connect()` へ `row_type` 引数を使って、結果を返すデータタイプを指定することができます。

説明のために、まず、モデルクラスを定義しましょう。
Userクラスにはコンストラクタで辞書型データを与えるようにしています。これはこれまでの例でデータベースに辞書型で保存されているので、これをUserクラスの属性(name, age, belongs)に変換するためです。

 usermode.py
```
 class User:
     nme: str
     age: int
     belongs: str

     def __init__(self, profile: dict):
         self.data = dict(profile)
         self.name = self.data['name']
         self.age = int(self.data['age'])
         self.belongs = self.data['belongs']

     def __repr__(self):
         return( f'User: name:"{self.name}", age:{self.age}, belongs:"{self.belongs}"' )

```


このUserクラスを `connect()` の引数 `row_type=User` として与えます。

```
 In [2]: # %load 17_row_type.py
    ...: import dataset
    ...: from usermodel import User
    ...:
    ...: db = dataset.connect('sqlite:///users.sqlite', row_type=User)
    ...: table = db['users']
    ...:
    ...: v1 = table.all()
    ...:
    ...: def func(data):
    ...:     for user in data:
    ...:         print(user, f'  name="{user.name}"')
    ...:
    ...: # print(v1)
    ...: # func(v1)
    ...:

 In [3]: print(v1)
 <dataset.util.ResultIter object at 0x1056888e0>

 In [4]: func(v1)
 User: name:"Jack Bauer", age:55, belongs:"CTU"   name="Jack Bauer"
 User: name:"Chloe O'Brian", age:0, belongs:"CTU"   name="Chloe O'Brian"
 User: name:"Anthony Tony", age:29, belongs:"CTU"   name="Anthony Tony"
 User: name:"David Gilmour", age:75, belongs:"Pink Floyd"   name="David Gilmour"
 User: name:"Ann Wilson", age:71, belongs:"Heart"   name="Ann Wilson"
 User: name:"Nacy Wilson", age:67, belongs:"Heart"   name="Nacy Wilson"
 User: name:"Jack Bauer", age:55, belongs:"CTU"   name="Jack Bauer"
 User: name:"Chloe O'Brian", age:0, belongs:"CTU"   name="Chloe O'Brian"
 User: name:"Anthony Tony", age:29, belongs:"CTU"   name="Anthony Tony"
 User: name:"David Gilmour", age:75, belongs:"Pink Floyd"   name="David Gilmour"
 User: name:"Ann Wilson", age:71, belongs:"Heart"   name="Ann Wilson"
 User: name:"Nacy Wilson", age:67, belongs:"Heart"   name="Nacy Wilson"

```

これにより、コンテンツはUserクラスオブジェクトで返されます。
データベースに辞書型データとして格納されているデータが、Userクラスにマッピングされ、name, age, belongs はドット表記でアクセスできるようになります。


## カスタムSQLクエリ
データベースを使用する最大の理由は、SQLクエリの能力を最大限に利用したいからです。ここでは、datasetからSQLクエリの実行方法を紹介します。


```
 In [2]: # %load 20_custom_query.py
    ...: from testdb import *
    ...:
    ...: v1 = db.query('SELECT belongs, COUNT(*) c FROM users GROUP BY belongs')
    ...:
    ...: def func(data):
    ...:     for row in data:
    ...:         print(row['belongs'], row['c'])
    ...:
    ...: # print(v1)
    ...: # func(v1)
    ...:

 In [3]: print(v1)
 <dataset.util.ResultIter object at 0x10afbf940>

 In [4]: func(v1)
 CTU 6
 Heart 4
 Pink Floyd 2

```

 `query()` メソッドは、基礎となる[SQLAlchemyコアAPI http://docs.sqlalchemy.org/en/latest/orm/query.html#the-query-object] にアクセスするためにも使うことができ、より複雑なクエリを実装することができます。

## 制限事項
dataset は、比較的基本的な操作をPythonicな方法で表現することで、基本的なデータベース操作をより簡単にすることを目的にしています。このアプローチは簡単に利用できる反面、アプリケーションがより複雑になってくると、より高度な操作が必要になり、SQLAlchemy を使わざる得なくなってしまう場合があります。
また、SQLAlchemy では Alembic と連携したデータベースのマイグレーション機能を提供しますが、dataset にはそうした機能はありません。大規模なプロジェクトではじめから採用するときは慎重に検討をするようにしてください。

## 余談
今回、例示したプログラムを実行すると、カレントディレクトリに次のようなデータベースができます。
 bash
```
 % ls users.sqlite*
 users.sqlite		users.sqlite-shm	users.sqlite-wal
```

- users.sqlite： SQLite のデータベース
- users.sqlite-shm：トランザクションの更新内容が書き込まれる。クロースしたときに削除される。
- users.sqlte-wal：コミットしたときに更新内容が書き込まれる。クローズしたときに削除される。

SQLiteでは、トランザクション開始から終了までの更新内容を、 `*-shm` ファイルに書き込んおき、コミットした時に `*-wal` ファイルへ更新内容を書き込む処理行っています。


## まとめ
dataset はデータベースに格納されたデータを気軽にPython の辞書オブジェクトにマッピングさせることができます。
本格的にORMを利用するほどでもないという場合は、スキームレスでデータベース設計を考えずに、まずはプロトタイプの開発を進められるメリットがあります。


## 参考資料
- [dataset 公式ドキュメント ](https://dataset.readthedocs.io/en/latest/)
