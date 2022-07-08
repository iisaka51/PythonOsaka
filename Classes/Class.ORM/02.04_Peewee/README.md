Peeweeを使ってみよう
=================
![](https://gyazo.com/a3c7acc1174f47fcc4521f147d6dd98b.png)


## Peeweeについて

Peeweeは、Python で実装さあれたシンプルで小さな**ORM(Object-Relational Mapping)**です。ORMは、オブジェクト指向的な操作でリレーショナルデータベースにアクセスする技術で、リレーショナルデータソースの操作が容易になり、論理的なビジネスモデルと物理的なストレージモデルを仲介します。これは、PythonのデータベースAPIを抽象化したものです。

Peewee には次のような特徴があります。

- 小さくて表現力豊かなORM
- Python で実装
- SQLite, MySQL, PostgreSQL, CockroachDB をサポート
- 豊富な拡張機能

この資料では、Peewee ORMの操作方法を紹介します。

## インストール
Peewee のインストールは pip で行います。
 bash
```
 $ pip install peewee
```


## データベース

PeeweeのDatabaseオブジェクトは、データベースへの接続を表しています。Databaseクラスは、データベースへの接続を開くために必要なすべての情報を持ってインスタンス化されます。Databaseオブジェクトは次のように使われます。。

- 接続を開いたり閉じたりします。
- クエリを実行する。
- トランザクション（およびセーブポイント）の管理
- テーブル、カラム、インデックス、制約を調べる。

Peeweeは、SQLite、MySQL、PostgreSQL、cockroachdb に対応しています。
データベースにアクセスするためにSQLにドライバが別途必要です。

- SQLite: [sqlite3 ](https://docs.python.org/2/library/sqlite3.html#sqlite3.connect) (Python標準ライブラリ)
- MySQL: [MySQLdb http://mysql-python.sourceforge.net/] あるいは [pymysql ](https://github.com/PyMySQL/PyMySQL)
- Postgres: [psycopg2 ](https://www.psycopg.org/)
- CockroachDB: [psycopg2 ](https://www.psycopg.org/)

各データベースクラスには、データベース固有の基本的な設定オプションがあります。


```
 from peewee import *
 
 # SQSQLite：ジャーナルモードをWAL(Write-Ahead-Log)、キャッシュを64MBに設定
 sqlite_db = SqliteDatabase('/path/to/app.db', 
                 pragmas={
                      'journal_mode': 'wal',
                      'cache_size': -1024 * 64})
 
 # MySQL: ネットワーク経由でMySQLサーバに接続.
 mysql_db = MySQLDatabase('my_app', user='app', password='db_password',
                          host='10.1.0.8', port=3306)
 
 # PostgreSQL: ネットワーク経由でPostgreSQLサーバに接続.
 pg_db = PostgresqlDatabase('my_app', user='postgres', password='secret',
                            host='10.1.0.9', port=5432)
 
 # CockrochDB：ネットワーク経由でCockrochDBサーバに接続
 db = CockroachDatabase('my_app', user='root', password='secret',
                        host='localhost', port=26257)
                        
```


## Peeweeのマッピング

モデルはデータベースのテーブルに、フィールドはテーブルのカラムに、インスタンスはテーブルの行にマッピングされます。

 PeeWee のオブジェクトマッピング

| オブジェクト | 対応するデータ |
|:--|:--|
| モデルクラス | データベースのテーブル |
| フィールドインスタンス | カラム、テーブル |
| モデルインスタンス | データベースのテーブルが保持する行 |



```
  from peewee import *
  
  db = SqliteDatabase('people.db')
  
  class Person(Model):
      name = CharField()
      birthday = DateField()
  
      class Meta:
          database = db
 
```


Peeweeは、クラスの名前から、データベースのテーブル名を自動的に推測します。内側の "Meta "クラスにtable_name属性を指定することで、デフォルトの名前を上書きすることができます(database属性と一緒に指定します)。

また、モデルの名前をPeopleではなくPersonにしていることにも注意してください。これは、テーブルに複数の人が含まれていても、常に単数形でクラス名を付けるという決まりがあるからです。

様々な種類のデータを保存するのに適した[フィールドタイプ http://docs.peewee-orm.com/en/latest/peewee/models.html#fields]がたくさんあります。Peeweeは、Pythonの値とデータベースで使用される値との間の変換を行ってくれるので、特別気にすることなくPythonの型を使用することができます。


Peeweeモデルのフィールドタイプは、モデルのストレージタイプを定義します。これらは、対応するデータベースのカラムタイプに変換されます。
次の表は、Peeweeのフィールドタイプと、それに対応するSQLite、PostgreSQL、MySQLのカラムタイプの一覧です。

 フィールドタイプとデータベースのカラムタイプ

| フィールドタイプ | SQLite | PostgreSQL | MySQL |
|:--|:--|:--|:--|
| CharField | varchar | varchar | varchar |
| TextField | text | text | longtext |
| DateTimeField | datetime | timestamp | datetime |
| IntegerField | integer | integer | integer |
| BooleanField | smallint | boolean | bool |
| FloatField | real | real | real |
| DoubleField | real | double precision | double precision |
| BigIntegerField | integer | bigint | bigint |
| DecimalField | decimal | numeric | numeric |
| PrimaryKeyField | integer | serial | integer |
| ForeignKeyField | integer | integer | integer |
| DateField | date | date | date |
| TimeField | time | time | time |


## 使用例

Peewee の使用方法を説明するために、次のモデルクラスを用意します。
 notedb.py
```
 from peewee import *
 import datetime
 
 db = SqliteDatabase('note.db')
 
 class BaseModel(Model):
     class Meta:
         database = db
         db_table = 'notes'
 
 class Note(BaseModel):
     text = CharField()
     created = DateField(default=datetime.date.today)        
     
         
 def populate_database():
 
     data = [
         {'text': 'Went to buy beer', 'created': datetime.date(2021, 8, 17)},
         {'text': 'Drinking beer', 'created': datetime.date(2021, 8, 17)},
         {'text': 'Making pizza', 'created': datetime.date(2021, 8, 19)},
         {'text': 'Eating pizza' }
     ]
 
     Note.create_table()
 
     notes = Note.insert_many(data)
     notes.execute()
 
 def remove_table():
     Note.drop_table()
 
 
 if __name__ == '__main__':
     populate_database()
```

はじめにこのモジュールを実行してデータベースを初期化しておきます。
 bash
```
 $ python notedb.py
```

以降、このサンプルコードについて説明してゆきます。

### データベースとの接続

```
 from peewee import *
 db = SqliteDatabase('note.db')
```

このコードは、バックエンドのデータベースシステムとしてSQLite に接続しています。
 `SQLiteDatabase()` の第１引数にはデータベースのファイル名を与えます。もし、メモリ上にデータベースを作成する場合は、
次のようにします。


```
 db = SqliteDatabase(':memory:')
```

### モデルクラスの定義

 `peewee.Model` を継承した  `BaseModel` クラスを作成しています。


```
 class BeseModel(Model):
      class Meta:
          database = db
          db_table = 'notes'
          
```

ここで、データベースへの接続と、データベース中のテーブル名を明示的に指示しています。
データベースへの接続を確立するベースモデルクラスを定義しておくと、他のモデルクラスの定義では、このベースモデルクラスを継承するだけです。データベースを指定する必要がなく、重複したコードがなくなり簡潔になります。



```
 class Note(BaseModel):
     # ...
 
```

Noteというデータベース・モデルを定義しています。このモデルは、 `BaseModel` を継承しています。


```
     text = peewee.CharField()
     created = peewee.DateField(default=datetime.date.today)
```

モデルのフィールドを指定します。 `CharField` と  `DateField` があります。 `CharField` は文字列を格納するためのフィールドクラスです。 `DateField` は、日付を格納するフィールドクラスです。指定されていない場合は、デフォルト値が設定されます。
Noteクラスは、プライマリキーを指定していないので、peeweeは自動的に `id` という自動インクリメントの整数のプラマリキーフィールドを追加します。

### テーブルの作成

データベースの初期化を行う関数です。初期データ  `data` を定義しています。
 `モデルクラス名.create_table()` を呼び出すだすことで、データベースにテーブルを作成します。


```
 def populate_database():
 
     data = [
         # ...
     ]
 
     Note.create_table()
```



### テーブルの削除

モデルクラスのメソッド  `drop_table()` を呼び出すと、テーブルを削除することができます。


```
 def remove_table():
     Note.drop_table()
 
```

### データの追加


```
     notes = Note.insert_many(data)
     notes.execute()
 
```

モデルクラスの `insert_many()` メソッドに `data` を与えて、一括してデータを登録しています。
データ１つ毎に処理する場合は次のように、 `insert()` あるいは  `create()` メソッドを使用します。


```
     for d in data:
         note = Note.create(d)
         note.save()
```



```
     for d in data:
         note = Note.insert(d)
         note.execute()
```

すぐにわかるはずですが、データ１つ毎に処理する場合はデータベースへ登録処理が繰り返されるため非効率です。

### データの確認
次のように、モデルクラスの `select()` を呼び出すと、そのテーブルに登録されているデータを取得することができます。


```
 In [2]: # %load 01_list_data.py
    ...: from notedb import *
    ...:
    ...: notes = Note.select()
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.text} {d.created}' )
    ...:
    ...: # func(notes)
    ...:
 
 In [3]: func(notes)
 Went to buy beer 2021-08-17
 Drinking beer 2021-08-17
 Making pizza 2021-08-19
 Eating pizza 2021-08-22
 
```

ここで、関数 `func()` を定義して、それを呼び出すことで表示させています。これは、ハンズオンを目的にしていることと、出力を明確にするためなので、実際には関数にする必要はありません。

### WHEREによるフィルタリング
 `where()` メソッドは、指定された条件に基づいてデータをフィルタリングすることができます。

 pytnon
```
 In [2]: # %load 02_query_where.py
    ...: from notedb import *
    ...:
    ...: notes = Note.select().where(Note.id > 3)
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.id} {d.text} {d.created}' )
    ...:
    ...: # func(notes)
    ...:
 
 In [3]: func(notes)
 4 Eating pizza 2021-08-22
 
```

### 複数のwhere表現
複数のwhere式を組み合わせることができます。


```
 In [2]: # %load 03_multiple_where.py
    ...: from notedb import *
    ...:
    ...: notes = Note.select().where((Note.id > 1) & (Note.id < 4))
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.id} {d.text} {d.created}' )
    ...:
    ...: # func(notes)
    ...:
 
 In [3]: func(notes)
 2 Drinking beer 2021-08-17
 3 Making pizza 2021-08-19
 
```


### 単一のインスタンスの取得
単一のインスタンスを選択するには2つの方法があり、それぞれ `get()` メソッドを使用します。


```
 In [2]: # %load 04_retreive.py
    ...: from notedb import *
    ...:
    ...: v1 = Note.select().where(Note.text == 'Went to buy beer').get()
    ...: v2 = Note.get(Note.text == 'Eating pizza')
    ...:
    ...: def print_obj(data):
    ...:     print(data.id)
    ...:     print(data.text)
    ...:     print(data.created)
    ...:
    ...: # print_obj(v1)
    ...: # print_obj(v2)
    ...:
 
 In [3]: print_obj(v1)
 1
 Went to buy beer
 2021-08-17
 
 In [4]: print_obj(v2)
 4
 Eating pizza
 2021-08-22
```

ごらんのように、データを取得する方法は２つあります。

### 特定のカラムの選択
 `select()` メソッドの中では、クエリに含めるフィールド名を指定することができます。


```
 In [2]: # %load 05_select_specific_field.py
    ...: from notedb import *
    ...: from pprint import pprint
    ...:
    ...: notes = Note.select(Note.text, Note.created)
    ...:
    ...: v1 = [e for e in notes.tuples()]
    ...:
    ...: # pprint(v1)
    ...:
 
 In [3]: pprint(v1)
 [('Went to buy beer', datetime.date(2021, 8, 17)),
  ('Drinking beer', datetime.date(2021, 8, 17)),
  ('Making pizza', datetime.date(2021, 8, 19)),
  ('Eating pizza', datetime.date(2021, 8, 22))]
 
```

この例では、 `text` と `created` の2つのフィールドを指定しています。 `Id` はスキップされます。

### インスタンスオブジェクトのカウント
表の中のモデル・インスタンスの数を計算するには、 `count()` メソッドを使います。


```
 In [2]: # %load 06_count.py
    ...: from notedb import *
    ...:
    ...: v1 = Note.select().count()
    ...: v2 = (Note
    ...:       .select()
    ...:       .where(Note.created >= datetime.date(2021, 8, 20))
    ...:       .count())
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 4
 
 In [4]: print(v2)
 1
 
```

クエリが長くなるとコードが読みにくくなるので、このコードの v2 を得るクエリのように括弧( `(...)` で囲んで、複数行に分けて記述することをおすすめします。

### SQL文の表示
生成されたSQL文を `sql()` メソッドで表示することができます。


```
 In [2]: # %load 07_show_sql.py
    ...: from notedb import *
    ...:
    ...: v1 = Note.select().where(Note.id == 3)
    ...: v2 = v1.sql()
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 SELECT "t1"."id", "t1"."text", "t1"."created" FROM "note" AS "t1" WHERE ("t1"."id" = 3)
 
 In [4]: print(v2)
 ('SELECT "t1"."id", "t1"."text", "t1"."created" FROM "note" AS "t1" WHERE ("t1"."id" = ?)', [3])
 
```

### offset、limit
offset属性とlimit属性を使用して、インスタンスのスキップオブジェクト数と `select()` に含まれるインスタンスの数を定義することができます。


```
 In [2]: # %load 08_offset_limit.py
    ...: from notedb import *
    ...:
    ...: v1 = Note.select().offset(2)
    ...: v2 = Note.select().limit(3)
    ...: v3 = Note.select().offset(2).limit(3)
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.id} {d.text} {d.created}' )
    ...:
    ...: # func(v1)
    ...: # func(v2)
    ...: # func(v3)
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v3)
    ...:
 
 In [3]: func(v1)
 3 Making pizza 2021-08-19
 4 Eating pizza 2021-08-22
 
 In [4]: func(v2)
 1 Went to buy beer 2021-08-17
 2 Drinking beer 2021-08-17
 3 Making pizza 2021-08-19
 
 In [5]: func(v3)
 3 Making pizza 2021-08-19
 4 Eating pizza 2021-08-22
 
 In [6]: print(v1)
 SELECT "t1"."id", "t1"."text", "t1"."created" FROM "note" AS "t1" LIMIT -1 OFFSET 2
 
 In [7]: print(v2)
 SELECT "t1"."id", "t1"."text", "t1"."created" FROM "note" AS "t1" LIMIT 3
 
 In [8]: print(v3)
 SELECT "t1"."id", "t1"."text", "t1"."created" FROM "note" AS "t1" LIMIT 3 OFFSET 2
 
```


### 順序付け
検索されたインスタンスは、 `order_by()` で並べることができます。


```
 In [2]: # %load 09_order_by.py
    ...: from notedb import *
    ...:
    ...: v1 = (Note
    ...:       .select(Note.text, Note.created)
    ...:       .order_by(Note.created))
    ...: v2 = (Note
    ...:       .select(Note.text, Note.created)
    ...:       .order_by(Note.created.desc()))
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.text} {d.created}' )
    ...:
    ...: # func(v1)
    ...: # func(v2)
    ...:
 
 In [3]: func(v1)
 Went to buy beer 2021-08-17
 Drinking beer 2021-08-17
 Making pizza 2021-08-19
 Eating pizza 2021-08-22
 
 In [4]: func(v2)
 Eating pizza 2021-08-22
 Making pizza 2021-08-19
 Went to buy beer 2021-08-17
 Drinking beer 2021-08-17
 
```

このコードでは、インスタンスを作成日順に並べています。 `order_by()` メソッドにしたいしたフィールドを値で並べ替えます。もし、引数を与えない場合は、プライマリキー(この例の場合  `id` )の値で並べ替えられます。
フィールドオブジェクトの `desc()` を呼び出すと降順に並べ替えられます。

### インスタンスオブジェクトの削除
 `delete_by_id()` メソッドは、 `Id` で特定されるインスタンスを削除します。削除されたインスタンスの数を返します。


```
 In [1]: !rm -f note.db
 
 In [2]: %run notedb.py
 
 In [3]: %load 10_delete_obj.py
 
 In [4]: # %load 10_delete_obj.py
    ...: from notedb import *
    ...: from pprint import pprint
    ...:
    ...: def func(data):
    ...:     output = list()
    ...:     for d in data:
    ...:         output.append(f'{d.id} {d.text} {d.created}' )
    ...:     return output
    ...:
    ...: before_data = Note.select()
    ...: v1 = func(before_data)
    ...: v2 = Note.insert(text='Watching YouTube.com').execute()
    ...: after_insert = Note.select()
    ...: v3 = func(after_insert)
    ...:
    ...: v4 = Note.delete_by_id(5)
    ...:
    ...: after_delete = Note.select()
    ...: v5 = func(after_delete)
    ...:
    ...: # pprint(v1)
    ...: # ...
    ...: # pprint(v5)
    ...:
 
 In [5]: pprint(v1)
 ['1 Went to buy beer 2021-08-17',
  '2 Drinking beer 2021-08-17',
  '3 Making pizza 2021-08-19',
  '4 Eating pizza 2021-08-23']
 
 In [6]: pprint(v2)
 5
 
 In [7]: pprint(v3)
 ['1 Went to buy beer 2021-08-17',
  '2 Drinking beer 2021-08-17',
  '3 Making pizza 2021-08-19',
  '4 Eating pizza 2021-08-23',
  '5 Watching YouTube.com 2021-08-23']
 
 In [8]: pprint(v4)
 1
 
 In [9]: pprint(v5)
 ['1 Went to buy beer 2021-08-17',
  '2 Drinking beer 2021-08-17',
  '3 Making pizza 2021-08-19',
  '4 Eating pizza 2021-08-23']
 
```


### 複数オブジェクトの一括削除
複数のオブジェクトを一括して削除するためには、モデルクラスの  `delete()` メソッドを呼び出します。このメソッドは、正常に削除されたインスタンスの数を返します。

 ppython
```
 In [1]: !rm -f note.db
 
 In [2]: %run notedb.py
 
 In [3]: %load 11_multiple_delete_obj.py
 
    ...: from notedb import *
    ...: from pprint import pprint
    ...:
    ...: def func(data):
    ...:     output = list()
    ...:     for d in data:
    ...:         output.append(f'{d.id} {d.text} {d.created}' )
    ...:     return output
    ...:
    ...: before_data = Note.select()
    ...: v1 = func(before_data)
    ...: v2 = Note.insert(text='Watching YouTube.com').execute()
    ...: v3 = Note.insert(text='Went to buy Wine').execute()
    ...: after_insert = Note.select()
    ...: v4 = func(after_insert)
    ...:
    ...: v5 = Note.delete().where(Note.id > 4).execute()
    ...:
    ...: after_delete = Note.select()
    ...: v6 = func(after_delete)
    ...:
    ...: # pprint(v1)
    ...: # ...
    ...: # pprint(v5)
    ...:
 
 In [5]: pprint(v1)
 ['1 Went to buy beer 2021-08-17',
  '2 Drinking beer 2021-08-17',
  '3 Making pizza 2021-08-19',
  '4 Eating pizza 2021-08-23']
 
 In [6]: pprint(v2)
 5
 
 In [7]: pprint(v3)
 6
 
 In [8]: pprint(v4)
 ['1 Went to buy beer 2021-08-17',
  '2 Drinking beer 2021-08-17',
  '3 Making pizza 2021-08-19',
  '4 Eating pizza 2021-08-23',
  '5 Watching YouTube.com 2021-08-23',
  '6 Went to buy Wine 2021-08-23']
 
 In [9]: pprint(v5)
 2
 
 In [10]: pprint(v6)
 ['1 Went to buy beer 2021-08-17',
  '2 Drinking beer 2021-08-17',
  '3 Making pizza 2021-08-19',
  '4 Eating pizza 2021-08-23']
 
```


### インスタンスオブジェクトのの更新
モデルクラスの `update()` メソッドは、インスタンスオブジェクトを更新します。更新に成功したインスタンスの数を返します。


```
 In [1]: !rm -f note.db
 
 In [2]: %run notedb.py
 
 In [3]: %load 12_update_obj.py
 
 In [4]: # %load 12_update_obj.py
    ...: from notedb import *
    ...: from pprint import pprint
    ...:
    ...: def func(data):
    ...:     output = list()
    ...:     for d in data:
    ...:         output.append(f'{d.id} {d.text} {d.created}' )
    ...:     return output
    ...:
    ...: before_update = Note.select()
    ...: v1 = func(before_update)
    ...:
    ...: v2 = (Note
    ...:       .update(created=datetime.date(2021, 8, 8))
    ...:       .where(Note.id == 1)
    ...:       .execute())
    ...:
    ...: after_update = Note.select()
    ...: v3 = func(after_update)
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...: # pprint(v3)
    ...:
 
 In [5]: pprint(v1)
 ['1 Went to buy beer 2021-08-17',
  '2 Drinking beer 2021-08-17',
  '3 Making pizza 2021-08-19',
  '4 Eating pizza 2021-08-23']
 
 In [6]: pprint(v2)
 1
 
 In [7]: pprint(v3)
 ['1 Went to buy beer 2021-08-08',
  '2 Drinking beer 2021-08-17',
  '3 Making pizza 2021-08-19',
  '4 Eating pizza 2021-08-23']
 
```

## 一対多のリレーションシップ
モデルを既存のテーブルにマッピングすることができます。モデル間のリレーションは `ForeignKeyField` で作成されます。
これを説明するために、別のモデルクラスを作成しましょう。

 custmerdb.py
```
 from peewee import *
 import datetime
 
 db = SqliteDatabase('customer.db')
 
 class Customer(Model):
 
     name = TextField()
     age = IntegerField()
 
     class Meta:
         database = db
         db_table = 'customers'
 
 class Reservation(Model):
 
     customer = ForeignKeyField(Customer, backref='reservations')
     created = DateField(default=datetime.date.today)
 
     class Meta:
         database = db
         db_table = 'reservations'
 
 
 def populate_database():
 
     customer_data = [
         { 'name': 'Jack Bauer',    'age': 55 },
         { 'name': "Chloe O'Brian", 'age': 0  },
         { 'name': 'Anthony Tony',  'age': 29 },
         { 'name': 'David Gilmour', 'age': 75 },
         { 'name': 'Ann Wilson',    'age': 71 },
         { 'name': 'Nacy Wilson',   'age': 67 },
     ]
     order_data = [
         { 'customer': 1, 'created': '2021-8-17' },
         { 'customer': 2, 'created': '2021-8-18' },
         { 'customer': 3, 'created': '2021-8-19' },
         { 'customer': 4, 'created': '2021-8-20' },
         { 'customer': 5, 'created': '2021-8-21' },
     ]
 
     Customer.create_table()
     Reservation.create_table()
 
     customers = Customer.insert_many(customer_data)
     customers.execute()
     reservations = Reservation.insert_many(order_data)
     reservations.execute()
 
 
 if __name__ == '__main__':
     populate_database()    
```

この例では、 `Customer` と  `Reservation` の2つのモデルを定義しています。
 `Customer` モデルと  `Reservation` モデルの間の関係は  `ForeignKeyField` で作成されます。 `backref` 引数は、顧客からの予約をどのように参照するか設定します。　ここで指定した値がプロパティ名となります。


ここで、データベースを初期化しておきます。

 bash
```
 $ python customerdb.py
 
```

### データの読み出し

次のようにしてデータを読み出してみましょう。
 `Customer` モデルのインスタンスオブジェクトは、対応する `Reservation` モデルを示すプロパティ  `reservations` を持っています。



```
 In [2]: # %load 20_list_data.py
    ...: from customerdb import *
    ...:
    ...: customer = (Customer
    ...:             .select()
    ...:             .where(Customer.name == 'Jack Bauer')
    ...:             .get())
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.id} {d.created}')
    ...:
    ...: # print(customer)
    ...: # print(customer.name)
    ...: # func(customer.reservations)
    ...: # print(customer.reservations)
    ...:
 
 In [3]: print(customer)
 1
 
 In [4]: print(customer.name)
 Jack Bauer
 
 In [5]: func(customer.reservations)
 1 2021-08-17
 
 In [6]: print(customer.reservations)
 SELECT "t1"."id", "t1"."customer_id", "t1"."created" FROM "reservations" AS "t1" WHERE ("t1"."customer_id" = 1)
 
```



## ロギング
以下のコードを追加することで、すべてのクエリをコンソールに記録することができます。


```
 import logging
 logger = logging.getLogger('peewee')
 logger.addHandler(logging.StreamHandler())
 logger.setLevel(logging.DEBUG)
```




## 既存データベースとの連携
既存データベースを利用する場合、モデル・ジェネレータである [pwiz ](https://raw.githubusercontent.com/coleifer/peewee/master/pwiz.py) を使って、peeweeのモデルを自動生成することができます。
例えば、この資料で使用した customer.db について、モデルを自動生成してみましょう。

 bash
```
 $ python pwiz.py  -e sqlite customer.db > customerdb_auto.py
```


```
 In [1]: %run pwiz.py -e sqlite customer.db
 from peewee import *
 
 database = SqliteDatabase('customer.db')
 
 class UnknownField(object):
     def __init__(self, *_, **__): pass
 
 class BaseModel(Model):
     class Meta:
         database = database
 
 class Customers(BaseModel):
     age = IntegerField()
     name = TextField()
 
     class Meta:
         table_name = 'customers'
 
 class Reservations(BaseModel):
     created = DateField()
     customer = ForeignKeyField(column_name='customer_id', field='id', model=Customers)
 
     class Meta:
         table_name = 'reservations'
 
```

## Playhouse 拡張モジュール
Peewee のソースレポジトリには、[Playhouse ](https://github.com/coleifer/peewee/tree/master/playhouse) という名前のディレクトリに集められた数多くの拡張モジュールが付属しています。特に、SQLite ExtensionsやPostgresql Extensionsのように、ベンダー固有のデータベース機能を提供する拡張モジュールがあり、非常に便利です。
- ベンダーエクステンション
  - SQLiteの拡張機能
  - フルテキスト検索 (FTS3/4/5)
  - BM25 ランキングアルゴリズムが SQLite C 拡張として実装され、FTS4 にバックポートされました。
  - 仮想テーブルとC拡張
  - クロージャテーブル
  - JSON 拡張のサポート
  - LSM1 (キー/バリューデータベース)のサポート
  - BLOB API
- オンライン・バックアップAPI
- APSW拡張: 強力なAPSW SQLiteドライバと一緒にPeeweeを使うことができます。
- SQLCipher: SQLiteデータベースを暗号化します。
- SqliteQ: マルチスレッドのSQLiteアプリケーションのための専用ライタースレッド。詳細はこちらをご覧ください。
- Postgresqlの拡張機能
  - JSONおよびJSONB
  - HStore
  - 配列
  - サーバーサイドカーソル
  - フルテキスト検索
- MySQL拡張
- 高レベルライブラリ
  - 追加フィールド
    - 圧縮されたフィールド
    - PickleField
  - ショートカット/ヘルパー
    - モデルから辞書へのシリアライザ
    - 辞書からモデルへのデシリアライザ
  - ハイブリッド属性
  - シグナル: プリ/ポストセーブ、プリ/ポストデリート、プリイン。
  - Dataset: 同名のプロジェクトで開発された、データベースを操作するための高レベル API。
  - Key/Value Store: SQLiteを使用したキー/バリューストアです。Pandasスタイルのクエリのためのスマートインデックスをサポートしています。
- データベース管理とフレームワークのサポート
  - pwiz: 既存のデータベースからモデルコードを生成します。
  - スキーママイグレーション: ハイレベルなAPIを使用してスキーマを変更することができます。SQLiteのカラムの削除や名前の変更もサポートしています。
  - 接続プール: シンプルな接続プーリング
  - Reflection: 低レベルでクロスプラットフォームなデータベースイントロスペクション
  - データベース URL: データベースへの接続に URL を使用します。
  - Test utils: Peeweeアプリケーションのユニットテストを行うためのヘルパーです。
  - Flask utils: ページ分割されたオブジェクトリスト、データベース接続管理など。

## peewee-extra-fields の紹介

カスタムフィールドを積極的に保守しているプロジェクトで、多数のフィールドタイプを提供します。また、フィールド用のHTML5ウィジェットを自動生成することもできます。

サンプルは次のようなものです。


```
 from datetime import date
 from peewee import Model, SqliteDatabase
 from peewee_extra_fields import *
 from peewee_extra_fields import exceptions
 
 db = SqliteDatabase('testing.db')
 
 class Person(Model):  # All peewee_extra_fields.
     name = CharFieldCustom()
     password = PasswordField()
     birthday = PastDateField()
     cuit = ARCUITField()
     postal_code = ARZipCodeField()
     country = CountryISOCodeField()
     currency = CurrencyISOCodeField()
     language = LanguageISOCodeField()
     age = PositiveSmallIntegerField()
     interests = CSVField()
     mail = EmailField()
     ip = IPAddressField()
     color = ColorHexadecimalField()
     hexa = SmallHexadecimalField()
     json = JSONField()
     files = FileField()
     text = TextField(validators=["test_text"])
 
     class Meta:
         database = db
```

## peewee-migrate2 の紹介
peewee-migrate2 はPeewee のためのマイグレーションツールです。
アプリケーションでバージョン更新を行うとき、データベースのスキームが変更になることがあります。こうした手続や処理は非常に面倒で憂鬱なもので、かう、間違いを犯しやすいものです。
マイグレーションツールを使用すると人為的なエラーを削減することができます。

 bash
```
 $ pip install peewee-migrate2
```

peewee-migrate2 をインストールすると　pw_migrate というコマンドが使えるようになります。

 bash
```
 $ pw_migrate --help
 
 Usage: pw_migrate [OPTIONS] COMMAND [ARGS]...
 
 Options:
     --help  Show this message and exit.
 
 Commands:
     create   Create migration.
     migrate  Run migrations.
     rollback Rollback migration.
     
```

 bash
```
 $ pw_migrate create --help
 
 Usage: pw_migrate create [OPTIONS] NAME
 
     Create migration.
 
 Options:
     --auto                  FLAG  Scan sources and create db migrations automatically. Supports autodiscovery.
     --auto-source           TEXT  Set to python module path for changes autoscan (e.g. 'package.models'). Current directory will be recursively scanned by default.
     --database              TEXT  Database connection
     --directory             TEXT  Directory where migrations are stored
     --schema                TEXT  Database schema
     -v, --verbose
     --help                        Show this message and exit.
     
```

 bash
```
 $ pw_migrate migrate --help
 
 Usage: pw_migrate migrate [OPTIONS]
 
     Run migrations.
 
 Options:
     --name                  TEXT  Select migration
     --database              TEXT  Database connection
     --directory             TEXT  Directory where migrations are stored
     --schema                TEXT  Database schema
     -v, --verbose
     --help     
     
```

 bash
```
 $ pw_migrate makemigrations --help
 
 Usage: pw_migrate makemigrations [OPTIONS]
 
   Create a migration automatically
 
   Similar to  `create` command, but  `auto` is True by default, and  `name` not
   required
 
 Options:
     --name TEXT         Migration file name. By default will be
                       'auto_YYYYmmdd_HHMM'
     --auto              Scan sources and create db migrations automatically.
                       Supports autodiscovery.
     --auto-source TEXT  Set to python module path for changes autoscan (e.g.
                       'package.models'). Current directory will be recursively
                       scanned by default.
     --database TEXT     Database connection
     --directory TEXT    Directory where migrations are stored
     --schema                TEXT  Database schema
     -v, --verbose
     --help              Show this message and exit.
 
```


## Peewee の拡張モジュール
Peewee をサポートするたくさんの有益な拡張モジュールがあります。

- [peewee-migrate2 ](https://github.com/spumer/peewee_migrate2)：Peeweeのためのシンプルなマイグレーションフレームワーク
- [aio-peewee ](https://github.com/klen/aio-peewee)：Peewee を非同期処理フレームワーク(Asyncio, Trio, Curio)に対応させるためのもの
- [peewee_mssqlserv ](https://github.com/brake/peewee_mssql)：Peewee のバックエンドに Microsoft SQLServer を利用するためのもの
- [peewee-validates ](https://github.com/timster/peewee-validates)：Peeweeのためのシンプルで柔軟なモデルおよびデータ検証ツール 
- [peewee-storages ](https://github.com/python-folks/peewee-storages)：Peewee に FileField を追加するためももの
- [Marshmallow-Peewee ](https://github.com/klen/marshmallow-peewee)：Peewee でMarshmallowを使ってシリアル化/非シリアル化を行うためのもの
- [wtf-peewee ](https://github.com/coleifer/wtf-peewee/)： peeweeモデルとwtformsの橋渡しをし、モデルのフィールドをフォームのフィールドにマッピングするもの
- [PeeweeExtraFields ](https://github.com/YADRO-KNS/PeeweeExtraFields)：Peewee に PasswordMD5Field などいくつかのフィールドタイプを追加するもの
- [peewee-extra-fields ](https://github.com/juancarlospaco/peewee-extra-fields)：多数おフィールドタイプを追加し、フィールド用のHTML5ウィジェットを自動生成するもの。


## まとめ
Peewee は 多対多のリレーションシップなど多くの機能を提供しています。
Django や Flask などで利用するための拡張モジュールも提供されているため、Webアプリケーションとの親和性も高くなっています。




## 参考資料

- [Peewee 公式ドキュメント http://docs.peewee-orm.com/en/latest/]





