PyDALを使ってみよう
=================

## PyDALについて
Web2Py では**データベース抽象化レイヤ(DAL:Database Abstraction Layer)**によって、データベースが抽象化されます。
Web2Py の中核のコンポーネントとして開発された DAL は 2015年に独立したプロジェクトPyDALとして分離されています。PyDAL拡張モジュールを使うことでアプリケーションにWeb2PyのDALと同様のデータベース抽象化レイヤ機能をもたせることができるようになります。

この資料では PyDAL の全ての機能を網羅しているわけではないことに注意してください。

## ORMとの比較
ORM(Object-relational mapping) は、データベーステーブルをデータベース層からの論理的な抽象化を表すクラス（たとえば、Userクラス）にマップし、レコードをそれらのクラスのインスタンスにマップします。 
DALは、データベースのテーブルとレコードを、上位レベルの抽象化ではなくテーブルを表すクラスのインスタンスにマップします。 構文はORMとよく似ていますが、高速で、ほとんどすべてのSQLに変換することができます。

## SQLAlchemy との比較
よく SQLAlchemy と比較されることがあります。一番の違いは、SQLAlchemyはメジャーだということです。ただし、PyDALの方がより簡単にデータベースにアクセスできること、サポートしているデータベースが多いこと、PyDALはweb2pyフォームと統合されているため、REST APIを公開することができることは、SQLAlchemyよりも有益です。

コードが簡潔になる例をみてみましょう。
SQLAlchemy でデータベースを作成して、エントリを追加するときは次のようになります。

```
 In [2]: # %load 01_sample_sqlalchemy.py
    ...: from sqlalchemy import Column, Integer, String
    ...: from sqlalchemy.ext.declarative import declarative_base
    ...: from sqlalchemy import create_engine
    ...: from sqlalchemy.orm import sessionmaker
    ...:
    ...: Base = declarative_base()
    ...:
    ...: class Person(Base):
    ...:     __tablename__ = 'person'
    ...:     id = Column(Integer, primary_key=True)
    ...:     name = Column(String(250), nullable=False)
    ...:
    ...: engine = create_engine('sqlite:///sqlalchemy_example.db')
    ...: Base.metadata.create_all(engine)
    ...:
    ...: Base.metadata.bind = engine
    ...:
    ...: DBSession = sessionmaker(bind=engine)
    ...: session = DBSession()
    ...:
    ...: new_person = Person(name='new person')
    ...: session.add(new_person)
    ...: session.commit()
    ...:
  
```


これが、PyDAL だと次のように大幅にコードが少なくて済みます。
 IPython
```
 In [2]: # %load 02_sample_pydal.py
    ...: from pydal import DAL, Field
    ...:
    ...: db=DAL("sqlite://dal_example.db")
    ...:
    ...: tmp=db.define_table('person',
    ...:                     Field('id', 'integer'),
    ...:                     Field('name', 'string', length=32, required=True),
    ...:                     migrate='person.table')
    ...:
    ...: person_id=db.person.insert(name="new　person")
    ...: db.commit()
    ...:
 
```

SQLAlchemy を Flask などのWebアプリケーションフレームワークから利用するときには、面倒な手続きがフレームワーク側で補佐されていることが多く便利に利用できます。しかし、データベースにアクセスをするアプリケーションを独自に開発するようなときは、PyDAL の採用を検討する余地も大きいでしょう。


## PyDALのインストール
Web2Py を利用している限りでは、PyDALのインストールは不要です。
データベース関連の処理部分を単独でデバッグするときや、Web2Py で得た知識と技術で別のアプリケーションに取り込みたいときには、PyDALをインストールして利用します。
PyDALは拡張モジュールなので次のようにインストールします。
 bash pipの場合
```
 $ pip install pydal
```

Wen2Py では不要ですが、PyDAL を自分のプログラムで利用するときは、
次のようにインポートするとWeb2Py と同じように使用することができます。

```
 from pydal import DAL, Field
```

## DALオブジェクト
まず、データベースへの接続には次のようにURIを指定します。
 SQLite3 データベースに接続する場合
```
 db=DAL("sqlite://test.db")
```

 MySQLデータベースに接続する
```
 db=DAL("mysql://username:password@host:port/dbname")
```

 PostgreSQLデータベースに接続する場合
```
 db=DAL("postgres://username:password@host:port/dbname")
```

 主なデータベースへの接続

| データベース |  |
|:--|:--|
| SQLite | sqlite://storage.db |
| MySQL | mysql://username:password@host:port/dbname |
| PostgreSQL | postgres://username:password@host:port/dbmae |
| MSSQL | mssql://username:password@host:port/dbname |
| FireBird | firebird://username:password@host:port/dbname |
| Oracle | oracle://username/password@host:port/dbname |
| DB2 | db2://username:password@host:port/dbname |
| Ingres | ingres://username:password@host:port/dbname |
| Sybase | sybase://username:password@host:port/dbname |
| Informix | informix://username:password@host:port/dbname |
| Teradata | teradata://DSN=dsn;UID=user;PWD=pass;DATABASE=dbname |
| Cubrid | cubrid://username:password@host:port/dbname |
| SAPDB | sapdb://username:password@host:port/dbname |
| IMAP | imap://user:password@server:port |
| MongoDB | mongodb://username:password@host:port/dbname |
| Google/SQL | google:sql://project:instance/database |
| Google/NoSQL | google:datastore |

## 指定可能なフィールドタイプ
 フィールドタイプ

| フィールドタイプ | デフォルトのフィールドバリデータ |
|:--|:--|
| string | IS_LENGTH(length) default length is 512 |
| text | IS_LENGTH(65536) |
| blob | None |
| boolean | None |
| integer | IS_INT_IN_RANGE(-1e100, 1e100) |
| double | IS_FLOAT_IN_RANGE(-1e100, 1e100) |
| decimal(n,m) | IS_DECIMAL_IN_RANGE(-1e100, 1e100) |
| date | IS_DATE() |
| time | IS_TIME() |
| datetime | IS_DATETIME() |
| password | None |
| upload | None |
| reference <table> | IS_IN_DB(db,table.field,format) |
| list:string | None |
| list:integer | None |
| list:reference <table> | IS_IN_DB(db,table.field,format,multiple=True) |
| json | IS_JSON() |
| bigint | None |
| big-id | None |
| big-reference | None |


```
 tmp=db.define_table('users',\
         Field('stringf','string',length=32,required=True),\
         Field('booleanf','boolean',default=False),\
         Field('passwordf','password'),\
         Field('textf','text'),\
         Field('blobf','blob'),\
         Field('uploadf','upload'),\
         Field('integerf','integer'),\
         Field('doublef','double'),\
         Field('datef','date',default=datetime.date.today()),\
         Field('timef','time'),\
         Field('datetimef','datetime'),\
         migrate='test_user.table')
```

## プライマリキー
プライマリキー(主キー: Primary Key) はテーブルに登録するレコード(データ行)の全体のうち、ひとつのデータに特定することをデータベースが保証する列のことです。
PyDALではフィールド名が  `id` となる `integer` 型のフィールドは何も設定しなくても、プライマリキーとして扱われます。
独自にプライマリキーを設定したいときは、テーブル作成時に  `priaryey=[]` にプライマリキーとする列のフィールド名を与えます。

```
 db.define_table('sample',
     Field('number','integer', required=True),
     Field('name', 'text', required=True),
     primarykey=['number'])
```

## Fieldオブジェクト
DALでアクセスしたフィールドデータは `Field` オブジェクトとして返されます。
 IPython
```
  fieldObj = Field(‘fieldname’, ’fieldtype’, length=32,
                   default=None, required=False, requires=[])
```

## テーブルの削除
テーブル `users` を削除するときは次のように `drop()` を呼び出します。


```
 db.users.drop()
```

## データの追加
データを追加するために次のようなデータを用意します。。
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

このデータからデータベースを作成します。
 testdb.py
```
 from pydal import DAL, Field
 from test_data import test_data
 
 db=DAL("sqlite://test.db")
 
 person = db.define_table('person',
                 Field('name', required=True),
                 Field('age', type='integer'),
                 Field('belongs'),
                 migrate='person.table')
 
 if __name__ == '__main__':
     for data in test_data:
         person.insert(name=data['name'],
                   age=data['age'],
                   belongs=data['belongs'])
 
     db.commit()
     db.close()
```

これを実行して test.db を作成します。

 bash
```
 $ python testdb.py
```

 `define_table()` は、対応するテーブルが存在するかどうかをチェックします。存在しない場合は、テーブル作成のためのSQLコマンドを生成して実行します。データベース中にテーブルが存在しても定義されているものと違うものであれば、そのテーブルを変更するSQLを生成し実行します。フィールドの型を変更し名前は変更してない場合、データを変更しようと試みます。
データベース中にテーブルが存在し現在の定義と一致する場合は、そのままになります。
このような挙動を、ここでは "マイグレーション" と言います。
この例の、 `define_table()` で  `migrate` 引数は SQLiteモジュールへ渡されるもので、この引数に指定したファイル名でテーブルが作成されます。指定しないとデータベースのテーブルを接続文字列のハッシュ値を使ったファイル名で自動作成されます。

migrate引数がないときの場合：（ `migrate=True` と同じ)
 bash
```
 % ls test.db *table
 c95cf9bab36fcb04c2424cdf9be0f6e3_person.table
 test.db
```

もし複数のアプリケーションから同じデータベースにアクセスしようとする場合は、 `migrate` 引数にファイル名を与えるアプリケーションは１つだけにする必要があります。その他のアプリケーションでは  `migrate=False` を与えます。

## すべてのデータを取得

```
 In [2]: # %load 03_all.py
    ...: from testdb import *
    ...:
    ...: rows = db().select(db.person.ALL)
    ...:
    ...: def func(data):
    ...:     for row in data:
    ...:         print(f'{row.id}, {row.name}, {row.age}, {row.belongs}')
    ...:
    ...: # print(rows)
    ...: # func(rows)
    ...:
 
 In [3]: print(rows)
 person.id,person.name,person.age,person.belongs
 1,Jack Bauer,55,CTU
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
 
 In [4]: func(rows)
 1, Jack Bauer, 55, CTU
 2, Chloe O'Brian, 0, CTU
 3, Anthony Tony, 29, CTU
 4, David Gilmour, 75, Pink Floyd
 5, Ann Wilson, 71, Heart
 6, Nacy Wilson, 67, Heart
 
```

データベースのテーブルにあるすべてのデータを取得するためには、 `select()` メソッドに、 `db.person.ALL` を与えます。
ここで、 `define_table()` では `id` フィールドは定義していなくても、デフォルトでプライマリキーとしてPyDALが自動的に設定されることを思い出してください。

## select()での結果を順序付け
次の例では、データベースのPersonテーブルからすべてのデータを、 `age` フィールドの値で、昇順、降順で出力するものです。

```
 In [2]: # %load 04_ordering_data.py
    ...: from testdb import *
    ...:
    ...: v1 = db(db.person).select(orderby=db.person.age)
    ...: v2 = db(db.person).select(orderby=~db.person.age)
    ...:
    ...: def func(data):
    ...:     for p in data:
    ...:         print(f'{p.id} {p.name} {p.age}')
    ...:
    ...: # func(v1)
    ...: # func(v2)
    ...: # db.close()
    ...:
 
 In [3]: func(v1)
 2 Chloe O'Brian 0
 3 Anthony Tony 29
 1 Jack Bauer 55
 6 Nacy Wilson 67
 5 Ann Wilson 71
 4 David Gilmour 75
 
 In [4]: func(v2)
 4 David Gilmour 75
 5 Ann Wilson 71
 6 Nacy Wilson 67
 1 Jack Bauer 55
 3 Anthony Tony 29
 2 Chloe O'Brian 0
 
 In [5]: db.close()
```


## limitdby
 `select()` メソッドの `limitby` 引数を使うと、データ出力を制限することができます。

```
 In [2]: # %load 05_limitby.py
    ...: from testdb import *
    ...:
    ...: v1 = db(db.person).select(limitby=(2, 5))
    ...:
    ...: def func(data):
    ...:     for p in data:
    ...:         print(f'{p.id} {p.name} {p.age} {p.belongs}')
    ...:
    ...: # func(v1)
    ...: # db.close()
    ...:
    ...:
 
 In [3]: func(v1)
 3 Anthony Tony 29 CTU
 4 David Gilmour 75 Pink Floyd
 5 Ann Wilson 71 Heart
 
 In [4]: db.close()
 
```

## 出力行をカウント
 `count()` メソッドを使用すると、出力の検索結果をカウントすることができます。

```
 In [2]: # %load 06_count.py
    ...: from testdb import *
    ...:
    ...: v1 = db().select(db.person.ALL)
    ...: v2 = db(db.person.id).count()
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # db.close()
    ...:
    ...:
 
 In [3]: print(v1)
 person.id,person.name,person.age,person.belongs
 1,Jack Bauer,55,CTU
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
 
 In [4]: print(v2)
 6
 
 In [5]: db.close()
 
```

## 出力をJSON/XML/辞書形式で出力
 `as_csv()` 、 `as_list()` 、 `as_json()` 、 `as_xml()` 、 `as_dict()` メソッドでクエリの結果出力のフォーマットを指定できます。
 `as_csv()` がデフォルトの動作です。

```
 In [2]: # %load 07_json.py
    ...: from testdb import *
    ...: from pprint import pprint
    ...:
    ...: v1 = db().select(db.person.ALL)
    ...: v2 = v1.as_csv()
    ...: v3 = v1.as_json()
    ...: v4 = v1.as_list()
    ...: v5 = v1.as_dict()
    ...: v6 = v1.as_xml()
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # pprint(v3)
    ...: # pprint(v4)
    ...: # pprint(v5)
    ...: # print(v6)
    ...:
 
 In [3]: print(v1)
 person.id,person.name,person.age,person.belongs
 1,Jack Bauer,55,CTU
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
 
 In [4]: print(v2)
 person.id,person.name,person.age,person.belongs
 1,Jack Bauer,55,CTU
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
 
 In [5]: pprint(v3)
 ('[{"id": 1, "name": "Jack Bauer", "age": 55, "belongs": "CTU"}, {"id": 2, '
  '"name": "Chloe O\'Brian", "age": 0, "belongs": "CTU"}, {"id": 3, "name": '
  '"Anthony Tony", "age": 29, "belongs": "CTU"}, {"id": 4, "name": "David '
  'Gilmour", "age": 75, "belongs": "Pink Floyd"}, {"id": 5, "name": "Ann '
  'Wilson", "age": 71, "belongs": "Heart"}, {"id": 6, "name": "Nacy Wilson", '
  '"age": 67, "belongs": "Heart"}]')
 
 In [6]: pprint(v4)
 [{'age': 55, 'belongs': 'CTU', 'id': 1, 'name': 'Jack Bauer'},
  {'age': 0, 'belongs': 'CTU', 'id': 2, 'name': "Chloe O'Brian"},
  {'age': 29, 'belongs': 'CTU', 'id': 3, 'name': 'Anthony Tony'},
  {'age': 75, 'belongs': 'Pink Floyd', 'id': 4, 'name': 'David Gilmour'},
  {'age': 71, 'belongs': 'Heart', 'id': 5, 'name': 'Ann Wilson'},
  {'age': 67, 'belongs': 'Heart', 'id': 6, 'name': 'Nacy Wilson'}]
 
 In [7]: pprint(v5)
 {1: {'age': 55, 'belongs': 'CTU', 'id': 1, 'name': 'Jack Bauer'},
  2: {'age': 0, 'belongs': 'CTU', 'id': 2, 'name': "Chloe O'Brian"},
  3: {'age': 29, 'belongs': 'CTU', 'id': 3, 'name': 'Anthony Tony'},
  4: {'age': 75, 'belongs': 'Pink Floyd', 'id': 4, 'name': 'David Gilmour'},
  5: {'age': 71, 'belongs': 'Heart', 'id': 5, 'name': 'Ann Wilson'},
  6: {'age': 67, 'belongs': 'Heart', 'id': 6, 'name': 'Nacy Wilson'}}
 
 In [8]: print(v6)
 <rows>
   <row>
     <id>1</id>
     <name>Jack Bauer</name>
     <age>55</age>
     <belongs>CTU</belongs>
   </row>
   <row>
     <id>2</id>
     <name>Chloe O'Brian</name>
     <age>0</age>
     <belongs>CTU</belongs>
   </row>
   <row>
     <id>3</id>
     <name>Anthony Tony</name>
     <age>29</age>
     <belongs>CTU</belongs>
   </row>
   <row>
     <id>4</id>
     <name>David Gilmour</name>
     <age>75</age>
     <belongs>Pink Floyd</belongs>
   </row>
   <row>
     <id>5</id>
     <name>Ann Wilson</name>
     <age>71</age>
     <belongs>Heart</belongs>
   </row>
   <row>
     <id>6</id>
     <name>Nacy Wilson</name>
     <age>67</age>
     <belongs>Heart</belongs>
   </row>
 </rows>
 
 
```


## CSVファイルからの読み込みと書き出し
PyDALではデータをCSVファイルから読み取ることができます。

```
 In [2]: # %load 08_export_csv.py
    ...: from testdb import *
    ...:
    ...: v1 = db().select(db.person.ALL)
    ...:
    ...: with open('testdata.csv', 'w') as f:
    ...:     v1.export_to_csv_file(f)
    ...:
    ...: # print(v1)
    ...: # !cat testdata.csv
    ...:
 
 In [3]: print(v1)
 person.id,person.name,person.age,person.belongs
 1,Jack Bauer,55,CTU
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
 
 In [4]: !cat testdata.csv
 person.id,person.name,person.age,person.belongs
 1,Jack Bauer,55,CTU
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
```


```
 In [2]: # %load 09_import_csv.py
    ...: from testdb import *
    ...:
    ...: v1 = db().select(db.person.ALL)
    ...:
    ...: with open('testdata.csv', 'rb') as f:
    ...:     db.person.import_from_csv_file(f)
    ...:
    ...: v2 = db().select(db.person.ALL)
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 person.id,person.name,person.age,person.belongs
 1,Jack Bauer,55,CTU
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
 
 In [4]: print(v2)
 person.id,person.name,person.age,person.belongs
 1,Jack Bauer,55,CTU
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 10,Jack Bauer,55,CTU
 11,Chloe O'Brian,0,CTU
 12,Anthony Tony,29,CTU
 13,David Gilmour,75,Pink Floyd
 14,Ann Wilson,71,Heart
 15,Nacy Wilson,67,Heart
 
```

PyDALはインポートする時に、web2pyはCSVのヘッダにあるフィールド名を探します。この例では、 `person.id` と  `person.name` 、 `person.age` 、 `person.belongs` という４つのカラムを見つけます。 `person` という接頭辞と、 `"` id`フィールドは無視されます。そして全てのレコードは追加され、新しいIDが割り当てられます。

## データの取得
テーブルオブジェクトにキワード引数でフィールドと値を指定すると、合致するデータを取得することができます。


```
 In [2]: # %load 10_retrieve.py
    ...: from testdb import *
    ...:
    ...: name = person(id=1)
    ...: jack = person(name='Jack Bauer')
    ...:
    ...: # print(name)
    ...: # print(jack)
    ...:
 
 In [3]: print(name)
 <Row {'id': 1, 'name': 'Jack Bauer', 'age': 55, 'belongs': 'CTU'}>
 
 In [4]: print(jack)
 <Row {'id': 1, 'name': 'Jack Bauer', 'age': 55, 'belongs': 'CTU'}>
 
```

## 複数データの取得

```
 In [2]: # %load 11_retrieve_multi.py
    ...: from testdb import *
    ...:
    ...: people = db(person).select(orderby=person.name,
    ...:                     groupby=person.name, limitby=(0,100))
    ...:
    ...: # print(people)
    ...:
 
 In [3]: print(people)
 person.id,person.name,person.age,person.belongs
 5,Ann Wilson,71,Heart
 3,Anthony Tony,29,CTU
 2,Chloe O'Brian,0,CTU
 4,David Gilmour,75,Pink Floyd
 1,Jack Bauer,55,CTU
 6,Nacy Wilson,67,Heart
 
```


## クエリ
PyDALはQueryで指定した条件に合致するデータを取得することができます。

```
 In [2]: # %load 12_query.py
    ...: from testdb import *
    ...:
    ...: query1 = (person.belongs == 'Heart') & (person.name.startswith('A'))
    ...: ann = db(query1).select(person.ALL)
    ...: query2 = person.age > 70
    ...: elderly = db(query2).select(person.ALL)
    ...:
    ...: # print(query1)
    ...: # print(ann)
    ...: # print(query2)
    ...: # print(elderly)
    ...:
 
 In [3]: print(query1)
 (("person"."belongs" = 'Heart') AND ("person"."name" LIKE 'A%' ESCAPE '\'))
 
 In [4]: print(ann)
 person.id,person.name,person.age,person.belongs
 5,Ann Wilson,71,Heart
 
 
 In [5]: print(query2)
 ("person"."age" > 70)
 
 In [6]: print(elderly)
 person.id,person.name,person.age,person.belongs
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
```


## 指定したレコードをUpdate
 `update_record()` を使うオブジェクトが保持している内容を更新することができます。
 IPython
```
 In [2]: # %load 13_update_record.py
    ...: from testdb import *
    ...:
    ...: jack = person(name='Jack Bauer')
    ...: v1 = f'{jack}'
    ...: v2 = jack.copy()
    ...: v3 = jack.update_record(belongs="Dangerous Man")
    ...: v4 = person(name='Jack Bauer')
    ...:
    ...: # print(v1)
    ...: # print(jack)
    ...: # print(v2)
    ...: # print(v3)
    ...: # print(v4)
    ...:
 
 In [3]: print(v1)
 <Row {'id': 1, 'name': 'Jack Bauer', 'age': 55, 'belongs': 'CTU'}>
 
 In [4]: print(jack)
 <Row {'id': 1, 'name': 'Jack Bauer', 'age': 55, 'belongs': 'Dangerous Man'}>
 
 In [5]: print(v2)
 {'id': 1, 'update_record': <pydal.helpers.classes.RecordUpdater object at 0x10b12a7c0>, 'delete_record': <pydal.helpers.classes.RecordDeleter object at 0x10b12a820>, 'name': 'Jack Bauer', 'age': 55, 'belongs': 'CTU'}
 
 In [6]: print(v3)
 <Row {'id': 1, 'name': 'Jack Bauer', 'age': 55, 'belongs': 'Dangerous Man'}>
 
 In [7]: print(v4)
 <Row {'id': 1, 'name': 'Jack Bauer', 'age': 55, 'belongs': 'Dangerous Man'}>
 
```

この例では、はじめに取得した `jack` の内容を文字列として  `v1` に保存しています。
次に、 `jack` オブジェクトを `copy()` メソッドで `v2` にセットしています。
その後、 `update_record()` で `jack` オブジェクトの内容を更新しています。
注目して欲しいことは、 `update_record()` が呼び出される前に取得した `jack` オブジェクトの内容も変更されることです。これはORMとしてデータベースの内容がPythonオブジェクト  `jack` にマッピングされたあとに、その `jack` オブジェクトを修正されたためです。

## 指定したレコードをDelete
 `delete_record()` を使うオブジェクトが保存されているレコードを削除することができます。

```
 In [2]: # %load 14_delete_record.py
    ...: from testdb import *
    ...:
    ...: id1 = person.insert(name='David Palmer', age=55, belongs='White House')
    ...: v1 = db(person).select(person.ALL)
    ...:
    ...: david = person(name='David Palmer')
    ...: v2 = f'{david}'
    ...: v3 = david.copy()
    ...: v4 = david.delete_record()
    ...: v5 = db(person).select(person.ALL)
    ...:
    ...: # print(id1)
    ...: # print(v1)
    ...: # print(david)
    ...: # print(v2)
    ...: # ...
    ...: # print(v5)
    ...:
 
 In [3]: print(id1)
 7
 
 In [4]: print(v1)
 person.id,person.name,person.age,person.belongs
 1,Jack Bauer,55,CTU
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 7,David Palmer,55,White House
 
 
 In [5]: print(david)
 <Row {'id': 7, 'name': 'David Palmer', 'age': 55, 'belongs': 'White House'}>
 
 In [6]: print(v2)
 <Row {'id': 7, 'name': 'David Palmer', 'age': 55, 'belongs': 'White House'}>
 
 In [7]: print(v3)
 {'id': 7, 'update_record': <pydal.helpers.classes.RecordUpdater object at 0x10f5ca640>, 'delete_record': <pydal.helpers.classes.RecordDeleter object at 0x10f5ca6a0>, 'name': 'David Palmer', 'age': 55, 'belongs': 'White House'}
 
 In [8]: print(v4)
 1
 
 In [9]: print(v5)
 person.id,person.name,person.age,person.belongs
 1,Jack Bauer,55,CTU
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
```

## クエリ結果に合致したデータをUpdate/Delete

```
 In [2]: # %load 15_query_update.py
    ...: from testdb import *
    ...:
    ...: id1 = person.insert(name='David Palmer', age=55, belongs='Democratic Sen
    ...: ator')
    ...: v1 = db(person).select(person.ALL)
    ...: david = person(name='David Palmer')
    ...: v2 = f'{david}'
    ...: v3 = david.copy()
    ...: v4 = db(person.belongs.like('D%')).update(belongs='White House')
    ...: v5 = db(person).select(person.ALL)
    ...:
    ...: v6 = db(person.name.lower() == 'david palmer').delete()
    ...: v7 = db(person).select(person.ALL)
    ...:
    ...: # print(id1)
    ...: # print(v1)
    ...: # print(david)
    ...: # print(v2)
    ...: # ...
    ...: # print(v7)
    ...:
 
 In [3]: print(id1)
 7
 
 In [4]: print(v1)
 person.id,person.name,person.age,person.belongs
 1,Jack Bauer,55,CTU
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 7,David Palmer,55,Democratic Senator
 
 
 In [5]: print(david)
 <Row {'id': 7, 'name': 'David Palmer', 'age': 55, 'belongs': 'Democratic Senator'}>
 
 In [6]: print(v2)
 <Row {'id': 7, 'name': 'David Palmer', 'age': 55, 'belongs': 'Democratic Senator'}>
 
 In [7]: print(v3)
 {'id': 7, 'update_record': <pydal.helpers.classes.RecordUpdater object at 0x109314e50>, 'delete_record': <pydal.helpers.classes.RecordDeleter object at 0x109314eb0>, 'name': 'David Palmer', 'age': 55, 'belongs': 'Democratic Senator'}
 
 In [8]: print(v4)
 1
 
 In [9]: print(v5)
 person.id,person.name,person.age,person.belongs
 1,Jack Bauer,55,CTU
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 7,David Palmer,55,White House
 
 
 In [10]: print(v6)
 1
 
 In [11]: print(v7)
 person.id,person.name,person.age,person.belongs
 1,Jack Bauer,55,CTU
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
```

## update_or_insert
 `update()` メソッドと `insert()` メソッドを合わせた動作をします。具体的には、更新しようとしているデータがデータベースになければ、 `insert()` の処理を行い、存在していれば `update()` の処理を行うものです。

```
 In [2]: # %load 16_upsert.py
    ...: from testdb import *
    ...:
    ...: id1 = person.update_or_insert(db.person.name == 'David Palmer',
    ...:                               name='David Palmer',
    ...:                               age=55, belongs='Democratic Senator')
    ...: v1 = db(person).select(person.ALL)
    ...:
    ...: id2 = person.update_or_insert(db.person.name == 'David Palmer',
    ...:                               name='David Palmer',
    ...:                               age=55, belongs='White House')
    ...: v2 = db(person).select(person.ALL)
    ...:
    ...: # print(id1)
    ...: # print(v1)
    ...: # print(id2)
    ...: # print(v2)
    ...:
 
 In [3]: print(id1)
 10
 
 In [4]: print(v1)
 person.id,person.name,person.age,person.belongs
 1,Jack Bauer,55,CTU
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 10,David Palmer,55,Democratic Senator
 
 
 In [5]: print(id2)
 None
 
 In [6]: print(v2)
 person.id,person.name,person.age,person.belongs
 1,Jack Bauer,55,CTU
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 10,David Palmer,55,White House
 
```



## find, exclude, sort
 `select()` メソッドを２回実行する必要があるときに、前回の `select()` の結果のRowオブジェクトを保持するしている、ということはよくあります。この場合、２度目の `select()` メソッドの処理で、再度データベースにアクセスするのは無駄なことになります。 `find()` 、 `exclude()` 、 `sort()` メソッド、Rowsオブジェクトを操作し、データベースアクセスすることなく、別のRowsオブジェクト生成することができます。

-  `find()` ： 条件でフィルタされた新規のRowsセットを返します。元のRowsはそのままです。
-  `exclude()` ： 条件でフィルタされた新規のRowsセットを返します。それらは元のRowsから取り除かれます。
-  `sort()` ： 条件でソートされた新規のRowsセットを返します。元のRowsはそのままです。


```
 In [2]: # %load 17_find.py
    ...: from testdb import *
    ...:
    ...: people = db().select(db.person.ALL)
    ...: v1 = f'{people}'
    ...:
    ...: v2 = people.find(lambda row: row.belongs == 'Heart')
    ...: v3 = people.exclude(lambda row: row.belongs == 'Heart')
    ...: v4 = people.sort(lambda row: row.name)
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v3)
    ...: # print(people)
    ...:
 
 In [3]: print(v1)
 person.id,person.name,person.age,person.belongs
 1,Jack Bauer,55,CTU
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
 
 In [4]: print(v2)
 person.id,person.name,person.age,person.belongs
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
 
 In [5]: print(v3)
 person.id,person.name,person.age,person.belongs
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
 
 In [6]: print(people)
 person.id,person.name,person.age,person.belongs
 1,Jack Bauer,55,CTU
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 
 
```

## first, last
 `first()` と `last()` メソッドを使うと、取得したデータの先頭、末尾のオブジェクトを取り出します。

```
 In [2]: # %load 18_first_last.py
    ...: from testdb import *
    ...:
    ...: rows = db().select(db.person.ALL)
    ...:
    ...: v1 = rows.first()
    ...: v2 = rows.last()
    ...:
    ...: # print(rows)
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(rows)
 person.id,person.name,person.age,person.belongs
 1,Jack Bauer,55,CTU
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
 
 In [4]: print(v1)
 <Row {'id': 1, 'name': 'Jack Bauer', 'age': 55, 'belongs': 'CTU'}>
 
 In [5]: print(v2)
 <Row {'id': 6, 'name': 'Nacy Wilson', 'age': 67, 'belongs': 'Heart'}>
 
 
```

## コミット と ロールバック
削除、更新操作は、 `commit()` が呼ばれるまでは、データベースには反映されません。
 IPython
```
 db.commit()
```

 `rollback()` を呼び出すと、これまで行った更新操作は捨てられます。

```
 db.rollback()
```


IPytho
```
 In [2]: # %load 19_commit_rollback.py
    ...: from testdb import *
    ...:
    ...: id1 = person.insert(name='David Palmer', age=55, belongs='Democratic Sen
    ...: ator')
    ...: v1 = db(person).select(person.ALL)
    ...: v2 = db.rollback()
    ...: v3 = db(person).select(person.ALL)
    ...:
    ...: id2 = person.insert(name='David Palmer', age=55, belongs='Democratic Sen
    ...: ator')
    ...: v4 = db.commit()
    ...:
    ...: from testdb import *
    ...: v5 = db(person).select(person.ALL)
    ...: david = person(name='David Palmer')
    ...: v6 = david.delete_record()
    ...: v7 = db.commit()
    ...:
    ...:
    ...: # print(id1)
    ...: # print(v1)
    ...: # ...
    ...: # print(v7)
    ...:
 
 In [3]: print(id1)
 9
 
 In [4]: print(v1)
 person.id,person.name,person.age,person.belongs
 1,Jack Bauer,55,CTU
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 9,David Palmer,55,Democratic Senator
 
 
 In [5]: print(v2)
 None
 
 In [6]: print(v3)
 person.id,person.name,person.age,person.belongs
 1,Jack Bauer,55,CTU
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
 
 In [7]: print(v4)
 None
 
 In [8]: print(v5)
 person.id,person.name,person.age,person.belongs
 1,Jack Bauer,55,CTU
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 9,David Palmer,55,Democratic Senator
 
 
 In [9]: print(v6)
 1
 
 In [10]: print(v7)
 None
```

ここで、 `David Palmer` を追加したとき、バックエンドのSQLite が自動的に割り当てる `id` の番号が飛んでいることに気づいたでしょうか？　これは、実はこの資料を各段階でなんどか実行していたために、欠落した `id` のデータが `delete_record()` で削除されたためです。SQLiteではプライマリキーに’使用される `id` は同じ番号を再利用することがないので、欠落したわけです。

## その他の操作
これまでの例でも何度か使われていますが、フィールドオブジェクトで使用できるメソッドについて説明します。

## like, ilike
ワイルドカード(パーセント記号( `%` ))で指定したパターンに合致するデータを
LIKE演算子は、ANSI SQLのLIKE句に対応しています。LIKEはほとんどのデータベースで大文字と小文字を区別し、データベース自体の照合順序に依存します。 `like()` は大文字と小文字を区別します。キーワード引数 `case_sensitive` に `False` を与えると大文字と小文字を区別しないようにすることができます。 `ilike()` は大文字と小文字を区別しません。

```
 In [2]: # %load 20_like.py
    ...: from testdb import *
    ...:
    ...: v1 = db(db.person.belongs.like('H%')).select()
    ...: v2 = db(db.person.belongs.like('h%', case_sensitive=False)).select()
    ...: v3 = db(db.person.belongs.ilike('h%')).select()
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.name} {d.age} {d.belongs}')
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v3)
    ...: # func(v1)
    ...: # func(v2)
    ...: # func(v3)
    ...:
 
 In [3]: print(v1)
 person.id,person.name,person.age,person.belongs
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
 
 In [4]: print(v2)
 person.id,person.name,person.age,person.belongs
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
 
 In [5]: print(v3)
 person.id,person.name,person.age,person.belongs
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
 
 In [6]: func(v1)
 Ann Wilson 71 Heart
 Nacy Wilson 67 Heart
 
 In [7]: func(v2)
 Ann Wilson 71 Heart
 Nacy Wilson 67 Heart
 
 In [8]: func(v3)
 Ann Wilson 71 Heart
 Nacy Wilson 67 Heart
 
```

## upper, lower
 `upper()` と  `lower()` メソッドでは、フィールドの値を大文字または小文字に変換することができ、 `like()` メソッドと組み合わせることもできます。

```
 In [2]: # %load 21_upper_lower.py
    ...: from testdb import *
    ...:
    ...: v1 = db(db.person.name.upper().like('DAVID%')).select()
    ...: v2 = db(db.person.name.lower().like('david%')).select()
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 person.id,person.name,person.age,person.belongs
 4,David Gilmour,75,Pink Floyd
 
 
 In [4]: print(v2)
 person.id,person.name,person.age,person.belongs
 4,David Gilmour,75,Pink Floyd
 
```


## regexp
 `regexp()` メソッドは `like()` メソッドと同じように動作しますが、ルックアップ式に正規表現の構文を使用できます。このメソッドは、MySQL、Oracle、PostgreSQL、SQLite、MongoDBでのみサポートされています（サポートの程度は異なります）。

```
 In [2]: # %load 22_regex.py
    ...: from testdb import *
    ...:
    ...: v1 = db(db.person.name.regexp('A.*n')).select()
    ...: v2 = db(db.person.name.regexp('A.*n$')).select()
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 person.id,person.name,person.age,person.belongs
 3,Anthony Tony,29,CTU
 5,Ann Wilson,71,Heart
 
 
 In [4]: print(v2)
 person.id,person.name,person.age,person.belongs
 5,Ann Wilson,71,Heart
 
```

## startswith, endswith, contains, case
フィールドの値の「始めの文字列」、「終わりの文字列」、「含まれる文字列」で抽出することができます。
 `case()` は条件に応じた真偽値を与えた引数の値を用いた結果で返します。

```
 In [2]: # %load 23_startswith.py
    ...: from testdb import *
    ...:
    ...: v1 = db(db.person.name.startswith('David')).select()
    ...: v2 = db(db.person.name.endswith('Wilson')).select()
    ...: v3 = db(db.person.name.contains('An')).select()
    ...: v4 = db(db.person.name.contains(['Ann', 'David'])).select()
    ...: v5 = db(db.person.name.contains(['Ann', 'David'], all=False)).select()
    ...: v6 = db(db.person.name.contains(['Ann', 'David'], all=True)).select()
    ...:
    ...: condition = db.person.belongs.contains('CTU')
    ...: yes_no = condition.case('Yes','No')
    ...: v7 = db().select(db.person.name, yes_no)
    ...:
    ...: # print(v1)
    ...: # ...
    ...: # print(v7)
    ...: # func(v7)
    ...:
 
 In [3]: print(v1)
 person.id,person.name,person.age,person.belongs
 4,David Gilmour,75,Pink Floyd
 
 
 In [4]: print(v2)
 person.id,person.name,person.age,person.belongs
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
 
 In [5]: print(v3)
 person.id,person.name,person.age,person.belongs
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 5,Ann Wilson,71,Heart
 
 
 In [6]: print(v4)
 person.id,person.name,person.age,person.belongs
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 
 
 In [7]: print(v5)
 person.id,person.name,person.age,person.belongs
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 
 
 In [8]: print(v6)
 person.id,person.name,person.age,person.belongs
 
 
 In [9]: print(v7)
 person.name,"CASE WHEN (LOWER(""person"".""belongs"") LIKE '%ctu%' ESCAPE '\') THEN 'Yes' ELSE 'No' END"
 Jack Bauer,Yes
 Chloe O'Brian,Yes
 Anthony Tony,Yes
 David Gilmour,No
 Ann Wilson,No
 Nacy Wilson,No
 
```


## year, month, day, hour, minutes, seconds
これまで例示のために使用してきた test.db には時間のフィールドがなかったので、
次のようなモジュールを用意して log.db を使用することにします。

 logdb.py
```
 from pydal import DAL, Field
 import datetime
 
 db = DAL("sqlite://log.db")
 log = db.define_table('log',
                      Field('event'),
                      Field('event_time', 'datetime'),
                      Field('severity', 'integer'),
                      migrate='log.table')
 
 if __name__ == '__main__':
     now = datetime.datetime.now()
     id = db.log.insert(event='port scan', event_time=now, severity=1)
     id = db.log.insert(event='xss injection', event_time=now, severity=2)
     id = db.log.insert(event='unauthorized login', event_time=now, severity=3)
     
     db.commit()
     db.close()
     
```

このモジュールを実行して、log.db を初期化します。
 bash
```
 $ python logdb.py
```


```
 In [2]: # %load 24_datetime.py
    ...: from logdb import *
    ...:
    ...: v1 = db().select(db.log.ALL)
    ...: v2 = db(db.log.event_time.year() > 2018).select()
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 log.id,log.event,log.event_time,log.severity
 1,port scan,2021-08-16 19:51:49,1
 2,xss injection,2021-08-16 19:51:49,2
 3,unauthorized login,2021-08-16 19:51:49,3
 
 
 In [4]: print(v2)
 log.id,log.event,log.event_time,log.severity
 1,port scan,2021-08-16 19:51:49,1
 2,xss injection,2021-08-16 19:51:49,2
 3,unauthorized login,2021-08-16 19:51:49,3
```


## belongs
SQLのIN演算子は `belongs()` メソッドで実現されており、フィールドの値が指定されたセット（リストやタプル）に属していれば真を返します。

PyDALでは、  `belongs()` メソッドの引数に `select` をネストさせることもできます。
唯一の注意点は、入れ子になった `select` は 、 `_select` でなければならないことと、セットを定義する1つのフィールドのみを明示的に選択しなければならないことに注意してください。


```
 In [2]: # %load 25_belongs.py
    ...: from logdb import *
    ...:
    ...: v1 = db(db.log.severity.belongs((1, 2))).select()
    ...: v2 = db(db.log.severity == 3)._select(db.log.event_time)
    ...: v3 = db(db.log.event_time.belongs(v2)).select()
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(d.severity, d.event)
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v3)
    ...: # func(v3)
    ...:
 
 In [3]: print(v1)
 log.id,log.event,log.event_time,log.severity
 1,port scan,2021-08-16 19:51:49,1
 2,xss injection,2021-08-16 19:51:49,2
 
 
 In [4]: print(v2)
 SELECT "log"."event_time" FROM "log" WHERE ("log"."severity" = 3);
 
 In [5]: print(v3)
 log.id,log.event,log.event_time,log.severity
 1,port scan,2021-08-16 19:51:49,1
 2,xss injection,2021-08-16 19:51:49,2
 3,unauthorized login,2021-08-16 19:51:49,3
 
 
 In [6]: func(v3)
 1 port scan
 2 xss injection
 3 unauthorized login
 
```


## sum, avg, min, max, len
 `count()` メソッドはレコード数をカウントするために使用しました。同様に `sum()` メソッド、レコードのグループから特定のフィールドの値を加算(sum)ことために使用することができます。 `count()` の場合と同様に、 `sum()` の結果は格納オブジェクトから取り出すことができます:
同様に avg、min、max で、選択されたレコードの平均値、最小値、最大値を取り出せます。
.len()は文字、テキスト、またはブーリアン型のフィールドの長さを計算します。

式を組み合わせてより複雑な式を作ることができます。この例では、logテーブルのseverity文字フィールドの長さに、1を加えた結果を合計しています。


```
 In [2]: # %load 26_sum.py
    ...: from logdb import *
    ...:
    ...: v1 = db.log.severity.sum()
    ...: v2 = db().select(v1).first()[v1]
    ...:
    ...: v3 = db.log.severity.max()
    ...: v4 = db().select(v3).first()[v3]
    ...:
    ...: v5 = db(db.log.event.len() > 13).select()
    ...:
    ...: # print(v1)
    ...: # ...
    ...: # print(v5)
    ...:
    ...:
 
 In [3]: print(v1)
 SUM("log"."severity")
 
 In [4]: print(v2)
 6
 
 In [5]: print(v3)
 MAX("log"."severity")
 
 In [6]: print(v4)
 3
 
 In [7]: print(v5)
 log.id,log.event,log.event_time,log.severity
 3,unauthorized login,2021-08-16 19:51:49,3
 
```


## スライスによる部分文字列
スライスを使って部分文字列を参照した式を作成することができます。例えば、最初の3文字の名前が同じ物をグループ化でき、各グループから1つだけ選択します:。


```
 In [2]: # %load 27_substrings.py
    ...: from testdb import *
    ...:
    ...: # v1 = db(db.person).select(distinct = db.person.name[:4])
    ...: # SyntaxError: DISTINCT ON is not supported by SQLite
    ...:
    ...: v1 = db(db.person).select(db.person.name[:4])
    ...:
    ...: # print(v1)
    ...:
 
 In [3]: print(v1)
 "SUBSTR(""person"".""name"",1,(5 - 1))"
 Jack
 Chlo
 Anth
 Davi
 Ann
 Nacy
 
```

 `select()` メソッドの `distinct` キーワード引数に与えて、重複のないレコードだけを選択することができます。ただし、、バックエンドのデータベースによってはエラーになる場合があることに注意してください。この例の場合では、SQLite を用いているため、コメントに記述しているようなエラーが発生します。

## 論理演算子
クエリには、二項演算子を使用することができます。

```
 In [2]: # %load 28_logical_operator.py
    ...: from testdb import *
    ...:
    ...: v1 = db((db.person.belongs == 'CTU') & (db.person.id >= 2)).select()
    ...: v2 = db((db.person.name == 'David Gilmour') | (db.person.id == 5)).selec
    ...: t()
    ...: v3 = db((db.person.name != 'David Gilmour') | (db.person.id > 3)).select
    ...: ()
    ...: v4 = db(~(db.person.name == 'Jack Bauer') | (db.person.id > 3)).select()
    ...:
    ...:
    ...: # print(v1)
    ...: # ...
    ...: # print(v4)
    ...:
 
 In [3]: print(v1)
 person.id,person.name,person.age,person.belongs
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 
 
 In [4]: print(v2)
 person.id,person.name,person.age,person.belongs
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 
 
 In [5]: print(v3)
 person.id,person.name,person.age,person.belongs
 1,Jack Bauer,55,CTU
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
 
 In [6]: print(v4)
 person.id,person.name,person.age,person.belongs
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
```

累積代入文を使用して、クエリを構築することもできます:

```
 In [2]: # %load 29_inplae.py
    ...: from testdb import *
    ...:
    ...: query = db.person.name != 'Jack Bauer'
    ...: q1 = f'{query}'
    ...: v1 = db(query).select()
    ...:
    ...: query &= db.person.id > 3
    ...: q2 = f'{query}'
    ...: v2 = db(query).select()
    ...:
    ...: query |= db.person.name == 'Ann Wilson'
    ...: q3 = f'{query}'
    ...: v3 = db(query).select()
    ...:
    ...: # print(q1, v1)
    ...: # print(q2, v2)
    ...: # print(q3, v3)
    ...:
 
 In [3]: print(q1, v1)
 ("person"."name" <> 'Jack Bauer') 
 person.id,person.name,person.age,person.belongs
 2,Chloe O'Brian,0,CTU
 3,Anthony Tony,29,CTU
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
 
 In [4]: print(q2, v2)
 (("person"."name" <> 'Jack Bauer') AND ("person"."id" > 3)) person.id,person.name,person.age,person.belongs
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
 
 In [5]: print(q3, v3)
 ((("person"."name" <> 'Jack Bauer') AND ("person"."id" > 3)) OR ("person"."name" = 'Ann Wilson')) person.id,person.name,person.age,person.belongs
 4,David Gilmour,75,Pink Floyd
 5,Ann Wilson,71,Heart
 6,Nacy Wilson,67,Heart
 
```

## 発行するSQLコマンドを生成
場合によっては、実行する必要はないけれど、SQLを生成させたいときがあります。PyDALでは、データベース操作を行うすべてのメソッドには、実際には実行しない同じ機能のものが用意されています。これは、実行されるはずのSQLコマンドを返すだけのものです。これらメソッドは、機能的に同じメソッドとほぼ名前と構文を持ちます。違いは、メソッド名がアンダースコア（ `_` ）で始まるということです。


```
 In [2]: # %load 30_raw_sql.py
    ...: from testdb import *
    ...:
    ...: v1 = db.person._insert(name='Alex')
    ...: v2 = db(db.person.name == 'Alex')._count()
    ...: v3 = db(db.person.name == 'Alex')._select()
    ...: v4 = db(db.person.name == 'Alex')._delete()
    ...: v5 = db(db.person.name == 'Alex')._update(name='Susan')
    ...:
    ...: # print(v1)
    ...: # ...
    ...: # print(v5)
    ...:
 
 In [3]: print(v1)
 INSERT INTO "person"("name") VALUES ('Alex');
 
 In [4]: print(v2)
 SELECT COUNT(*) FROM "person" WHERE ("person"."name" = 'Alex');
 
 In [5]: print(v3)
 SELECT "person"."id", "person"."name", "person"."age", "person"."belongs" FROM "person" WHERE ("person"."name" = 'Alex');
 
 In [6]: print(v4)
 DELETE FROM "person" WHERE ("person"."name" = 'Alex');
 
 In [7]: print(v5)
 UPDATE "person" SET "name"='Susan' WHERE ("person"."name" = 'Alex');
 
```

 SQL生成メソッド

| アクセスメソッド | 生成メソッド |
|:--|:--|
| select() | _select() |
| count() | _count() |
| insert() | _insert() |
| delete() | _delete() |
| update() | _update() |


## 直接SQLコマンドを実行

DALオブジェクトの  `executesql()` メソッドにSQL文を渡すことができます。

```
 In [1]: %load 31_executesql.py
 
 In [2]: # %load 31_executesql.py
    ...: from testdb import *
    ...: from pprint import pprint
    ...:
    ...: SQL = 'SELECT * FROM person;'
    ...: v1 = db.executesql(SQL)
    ...:
    ...: # pprint(v1)
    ...:
 
 In [3]: pprint(v1)
 [(1, 'Jack Bauer', 55, 'CTU'),
  (2, "Chloe O'Brian", 0, 'CTU'),
  (3, 'Anthony Tony', 29, 'CTU'),
  (4, 'David Gilmour', 75, 'Pink Floyd'),
  (5, 'Ann Wilson', 71, 'Heart'),
  (6, 'Nacy Wilson', 67, 'Heart')]
  
```


## _lastsql
 `executesql()` を使って手動で実行されたSQLコマンドであろうと、PyDALが生成した実行したSQLコマンドであろうと、 `db._lastsql` には必ず直前のSQLコードが保存されています。これはデバッグの際に便利です。

## select のキャッシュ
 `select()` メソッドは、 `cache` 引数を受け取ることができます。デフォルトは `None` です。キャッシュを有効にするためには、最初の要素がキャッシュモデル（ `cache.ram` 、 `cache.disk` など）で、2番目の要素が有効期限（秒単位）のタプルを与えます。

次の例では、前もって定義されたdb.logテーブルのセレクトをキャッシュするコントローラがあります。実際のセレクトは、60秒に1回以上の頻度でバックエンドデータベースからデータを取得し、その結果をメモリに保存します。このコントローラへの次の呼び出しが、最後のデータベースIOから60秒以内に行われた場合は、単にメモリから前のデータをフェッチします。


```
 def cache_db_select():
     logs = db().select(db.log.ALL, cache=(cache.ram, 60))
     return dict(logs=logs)
```

 `select()` メソッドには、オプションの  `cacheable` 引数があり、通常は  `False` に設定されます。 `cacheable=True` の場合、結果の  `rows` はシリアライズ可能ですが、 `rows` には  `update_record()` メソッドと  `delete_record()` メソッドがありません。これらのメソッドが不要な場合は、 `cacheable` 引数を設定することで select の処理を大幅に高速化することができます。


```
 rows = db(query).select(cacheable=True)
```

 `cache` 引数が  `cacheable=False` (デフォルト)で設定されている場合、データベースの結果のみがキャッシュされ、実際の  `rows` オブジェクトはキャッシュされません。 `cache` 引数を  `cacheable=True` と組み合わせて使用すると、 `rows` オブジェクト全体がキャッシュされ、非常に高速になります。


```
 rows = db(query).select(cache=(cache.ram, 3600), cacheable=True)
```



## 1 対多のリレーション
1 対多のリレーションシップでは、テーブル内の 1 つのレコードを別のテーブルの 1 つ以上のレコードと関連付けることができます。

 one_relationdb.py
```
 from pydal import DAL, Field
 
 db=DAL("sqlite://demo.db")
 
 db.define_table('person',
                 Field('name'),
                 migrate='demo_person.table')
 
 db.define_table('car',
                 Field('name'),
                 Field('owner_id', 'reference person'),
                 migrate='demo_car.table')
                 
 if __name__ == '__main__':
     db.person.insert(name='Alex')
     db.person.insert(name='Bob')
     db.person.insert(name='Carl')
     
     db.car.insert(name='Mustang Cobra', owner_id=1)
     db.car.insert(name='Corvette Stingray', owner_id=1)
     db.car.insert(name='Dodge Viper ', owner_id=2)
 
     db.commit()
     db.close()
     
```

テーブル `car` には、 `name` と `owner_id` という2つのフィールドがあります。owner_id "フィールドは参照型です。
参照型のフィールドは、そのidによって他のテーブルを参照することを意図しています。

参照型は、2つの同等の方法で指定することができます。
方法１：

```
 Field('owner_id', 'reference person')
```

方法２：

```
 Field('owner_id', db.person)
```

方法２は常に方法１に変換されます。２つの方法は、遅延テーブルや自己参照、その他のタイプの循環参照の場合で、方法１の表記だけが許される場合を除いて、等価です。


```
 In [2]: # %load 40_one_relation.py
    ...: from one_relationdb import *
    ...:
    ...: v1 = db(db.car.owner_id == 1).select()
    ...: v2 = db(db.car.name == 'Mustang Cobra').select()
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 car.id,car.name,car.owner_id
 1,Mustang Cobra,1
 2,Corvette Stingray,1
 
 
 In [4]: print(v2)
 car.id,car.name,car.owner_id
 1,Mustang Cobra,1
 
```


## 內部結合(Inner JOIN)
上記例と同様の結果を得るためのもう1つの方法は、結合（特に内部結合）を使用することです。

```
 In [2]: # %load 41_join.py
    ...: from one_relationdb import *
    ...:
    ...: v1 = db(db.person.id == db.car.owner_id).select()
    ...:
    ...: v2 = db(db.person).select(join=db.car.on(db.person.id == db.car.owner_id
    ...: ))
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.person.name} has {d.car.name}')
    ...:
    ...: # print(v1)
    ...: # func(v1)
    ...: # print(v2)
    ...: # func(v2)
    ...:
    ...:
 
 In [3]: print(v1)
 person.id,person.name,car.id,car.name,car.owner_id
 1,Alex,1,Mustang Cobra,1
 1,Alex,2,Corvette Stingray,1
 2,Bob,3,Dodge Viper ,2
 
 
 In [4]: func(v1)
 Alex has Mustang Cobra
 Alex has Corvette Stingray
 Bob has Dodge Viper
 
 In [5]: print(v2)
 person.id,person.name,car.id,car.name,car.owner_id
 1,Alex,1,Mustang Cobra,1
 1,Alex,2,Corvette Stingray,1
 2,Bob,3,Dodge Viper ,2
 
 
 In [6]: func(v2)
 Alex has Mustang Cobra
 Alex has Corvette Stingray
 Bob has Dodge Viper
 
```

出力は同じですが、この2つのケースでは生成されるSQLが異なる場合があります。

## 左外部結合(Left Outer Join)
 `person` でのユーザが車を所有しているかどうか評価して、車を所有しているのであれば、 `car` を選択する場合は、LEFT OUTER JOINを行う必要があります。これは、 `select` の引数  `left` を使って行います。


```
 In [2]: # %load 42_left_outer_join.py
    ...: from one_relationdb import *
    ...:
    ...:
    ...: v1 = db().select(db.person.ALL, db.car.ALL,
    ...:                  left=db.car.on(db.person.id == db.car.owner_id))
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.person.name} has {d.car.name}')
    ...:
    ...: # print(v1)
    ...: # func(v1)
    ...:
    ...:
 
 In [3]: print(v1)
 person.id,person.name,car.id,car.name,car.owner_id
 1,Alex,2,Corvette Stingray,1
 1,Alex,1,Mustang Cobra,1
 2,Bob,3,Dodge Viper ,2
 3,Carl,<NULL>,<NULL>,<NULL>
 
 
 In [4]: func(v1)
 Alex has Corvette Stingray
 Alex has Mustang Cobra
 Bob has Dodge Viper
 Carl has None
 
```

左外部結合(Left Outer Join)では、どのフィールドを選択するかは明示的にする必要があり、左側で指定したテーブルのフィールドのデータが出力にあります。

## グループ化とカウント
結合を行うとき、時々、ある基準に従って行をグループ化し、それらをカウントしたいことがあります。上記の例で言えば、すべての人が所有している車の数を数えるときなどです。

```
 In [2]: # %load 43_grouping_count.py
    ...: from one_relationdb import *
    ...:
    ...: count = db.person.id.count()
    ...: v1 = db(db.person.id == db.car.owner_id).select(
    ...:                             db.person.name, count, groupby=db.person.nam
    ...: e)
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.person.name} has {d[count]} cars')
    ...:
    ...: # print(v1)
    ...: # func(v1)
    ...:
 
 In [3]: print(v1)
 person.name,"COUNT(""person"".""id"")"
 Alex,2
 Bob,1
 
 
 In [4]: func(v1)
 Alex has 2 cars
 Bob has 1 cars
 
```

 `count()` メソッドがフィールドとして使われていることに注目してください。ここでの問題は、どうやってその情報を取り出すかということです。各行には明らかに `person` と  `count` の結果が含まれていますが、 `count` は `person` のフィールドでもなければ、テーブルでもありません。この場合、クエリ式自身と同じキーを持つ、レコードを表すストレージ・オブジェクトに格納されます。

Field オブジェクトの  `count()` メソッドには、オプションで  `distinct` 引数があります。これを  `True` に設定すると、対象となるフィールドの個別の値のみ(つまり、重複したデータを除外した値)をカウントすることになります。

## 多対多リレーション
前述の例では、1つの車は1人の持ち主(owner_id)を持つけれど、1人の持ち主は多くの車を持てるようになっています。
では、AlexとCurtが持っているボートは関連づける場合はどうすればよいのでしょうか？
これには**多対多のリレーション(many-to-many relation)** が必要です。そしてこれは、所有(ownership)関係で1人の持ち主と1つ物をリンクする中間テーブル（結合テーブル)を介して実現されます。

あるテーブルの複数のレコードが別のテーブルの複数のレコードと関連付けられている場合は多対多のリレーションシップが発生します。しかし、リレーショナルデータベースシステムでは、2 つのテーブル間に多対多のリレーションシップを直接設定することはできません。
ユーザを参照するとき、同じユーザIDが多数あったとすると、ユーザIDを照会されても、ユーザ特定することができません。ユーザごとに固有の値を割り当てるのはそのためです。

結合テーブルと呼ばれる第３のテーブルを使用すると、多対多のリレーションシップを 2 つの 1 対多のリレーションシップに分割することができます。

```
 from pydal import DAL, Field
 
 db = DAL("sqlite://manyrel.db")
 
 db.define_table('person',
                 Field('name')
                 migrate='manyrel_person.table')
 db.define_table('thing',
                 Field('name'),
                 migrate='manyrel_thing.table')
 db.define_table('ownership',
                 Field('person', 'reference person'),
                 Field('thing', 'reference thing'),
                 migrate='manyrel_ownership.table')
 
 if __name__ == '__main__':
     person_data = [(dict(name='Alex'), dict(name='Bob'), dict(name='Carl')]
     thing_data  = [(dict(name='Boat'), dict(name='Chair'), dict(name='Shoes')]
 
     db.person.bulk_insert(person_data)
     db.thing.bulk_insert(thing_data)
 
     db.ownership.insert(person=1, thing=1)  # Alex owns Boat
     db.ownership.insert(person=1, thing=2)  # Alex owns Chair
     db.ownership.insert(person=2, thing=3)  # Bob owns Shoes
     db.ownership.insert(person=3, thing=1)  # Curt owns Boat too
     
     db.commit()
     db.close()
 
```

テーブル間に3者間の関係ができたので、操作を実行するための新しいセットを定義すると便利です。新しいセットからすべての人とその物を簡単に選択できるようになります。


```
 In [1]: %load 44_many_relation.py
 
    ...: v1 = db((db.person.id == db.ownership.person) &
    ...:         (db.thing.id == db.ownership.thing))
    ...:
    ...: v2 = v1.select()
    ...: v3 = v1(db.person.name == 'Alex').select()
    ...: v4 = v1(db.thing.name == 'Boat').select()
    ...:
    ...: def func(out_type, data):
    ...:     for d in data:
    ...:         if out_type == 1:   # all
    ...:             print(f'{d.person.name} has {d.thing.name}')
    ...:         elif out_type == 2: # thing
    ...:             print(f'{d.thing.name}')
    ...:         elif out_type == 3:   # person
    ...:             print(f'{d.person.name}')
    ...:         else:               # other
    ...:             print(f'{d.id}, {d.name}')
    ...:
    ...: # print(v1)
    ...: # ...
    ...: # print(v4)
    ...: # func(1, v2)
    ...: # func(2, v3)
    ...: # func(3, v4)
    ...:
 
 In [3]: print(v1)
 <Set (("person"."id" = "ownership"."person") AND ("thing"."id" = "ownership"."thing"))>
 
 In [4]: print(v2)
 thing.id,thing.name,ownership.id,ownership.person,ownership.thing,person.id,person.name
 1,Boat,1,1,1,1,Alex
 2,Chair,2,1,2,1,Alex
 3,Shoes,3,2,3,2,Bob
 1,Boat,4,3,1,3,Carl
 
 
 In [5]: print(v3)
 thing.id,thing.name,ownership.id,ownership.person,ownership.thing,person.id,person.name
 1,Boat,1,1,1,1,Alex
 2,Chair,2,1,2,1,Alex
 
 
 In [6]: print(v4)
 thing.id,thing.name,ownership.id,ownership.person,ownership.thing,person.id,person.name
 1,Boat,1,1,1,1,Alex
 1,Boat,4,3,1,3,Carl
 
 
 In [7]: func(1, v2)
 Alex has Boat
 Alex has Chair
 Bob has Shoes
 Carl has Boat
 
 In [8]: func(2, v3)
 Boat
 Chair
 
 In [9]: func(3, v4)
 Alex
 Carl
 
```

## まとめ
PyDAL を使うとデータベースのデータをPythonオブジェクトにマッピングできるため、SQLの知識が深くなくてもデータベースを用いたプログラムを開発できるようになります。また、SQLコマンドをコード中に埋め込む必要がないため、保守性が向上にします。



## 参考
- [PyDALソースコード ](https://github.com/web2py/pydal)
- [PyDAL ドキュメント - Web2Py Database Abstraction Layer http://www.web2py.com/books/default/chapter/29/06/the-database-abstraction-layer] ([日本語 http://www.web2py.com/books/default/chapter/33/06/the-database-abstraction-layer])
- [Web2Py Chapter6. データベース抽象化レイヤ http://www.web2py.com/books/default/chapter/33/06//]


#database
#ORM


