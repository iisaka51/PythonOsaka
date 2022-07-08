Ponyを使ってみよう
=================
![](https://gyazo.com/7c9f770835a67a84dda1b0ffe6159f8a.png)

## Pony について
Ponyは、**オブジェクトリレーショナルマッパー(Object Relational Mapper: ORM)** のためのPython の拡張モジュールです。ORMは、開発者がオブジェクトの形でデータベースのコンテンツを扱えるようにしてくれます。リレーショナルデータベースは、テーブルに格納された**行(Raw)** を含んでいます。しかし、データベースから取得したデータにオブジェクトの形でアクセスできる方がはるかに便利です。
Django やSQLAlchemyなど、Pythonで実装された人気の高い ORMは他にもありますが、Ponyにはいくつかの利点があります。

- クエリを書くための非常に便利な構文
- クエリの自動最適化
- N+1問題のエレガントな解決策
- [オンラインデータベーススキーマエディタ ](https://editor.ponyorm.com/)


Ponyの特徴の一つに、ジェネレータ式やラムダ関数を使ってPythonでデータベースと対話できることです。
以下は、ジェネレータ式の構文を使ったクエリの例です。

```
 select(c for c in Customer if sum(c.orders.total_price) > 1000)
```

ラムダ式を使って記述することもできます。

```
 Customer.select(lambda c: sum(c.orders.total_price) > 1000)
```

 `Customer` は、アプリケーション作成時に初期記述されるエンティティクラスで、データベースのテーブルにリンクされています。このクエリでは、購入金額の合計が1000を超えるすべての顧客を検索します。データベースへの問い合わせは、Pythonのジェネレータ式の形で記述され、引数として `select()` 関数に渡されます。Ponyはこのジェネレータを実行するのではなく、SQLに変換してデータベースに送信します。これにより、開発者はSQLについて詳しくなくてもデータベースのクエリを書くことができます。

Ponyは、使いやすさに加えて、データを効率的に扱うことができます。クエリはSQLに変換され、素早く効率的に実行されます。DBMSによっては、選択したデータベースの機能を利用するために、生成されるSQLの構文が異なる場合があります。Pythonで書かれたクエリコードは、DBMSに関係なく同じように見えるので、アプリケーションの移植性が保証されます。



## インストール
Pony は次のようにインストールすることができます。
 bash
```
 $ pip install pony
```

この資料作成時点でPonyがサポートしているデータベースは次の５つです。

- SQLite
- MySQL
- PostgreSQL
- Oracle
- CockrachDB

SQLAlchemy と比較するとサポートするデータベースが少ないことが弱点だと言われています。

SQLiteデータベースを使用する場合は、他に何もインストールする必要はありません。他のデータベースを使用したい場合は、データベースへのアクセスできる権限と、対応するPython データベースドライバをインストールする必要があります。

- MySQL：　MySQL-python または PyMySQL
- PostgreSQL：　psycopg2 または psycopg2cffi
- Oracle:：　cx_Oracle
- CockroachDB：　psycopg2 または  psycopg2cffi

Pony が正常にインストールされたことを確認するには、Python を対話モードで起動し、次のように入力します。

```
 ｆrom pony.orm import *
```


## Ponyを使ってみる
Ponyに慣れる一番の方法は、インタラクティブモードで遊んでみることです。ここでは、エンティティクラスPersonを含むサンプルデータベースを作成し、そこに3つのオブジェクトを追加して、クエリを書いてみましょう。

### データベースオブジェクトの作成
Ponyのエンティティは、データベースに接続されています。そのため、まずデータベースオブジェクトを作成する必要があります。Pythonインタプリタで、次のように入力します。

```
 In [2]: # %load 01_db.py
    ...: from pony.orm import *
    ...:
    ...: db = Database()
    ...:
 
```


### エンティティの定義
次に、 `Person` と `Car` という2つのエンティティを作成してみましょう。 `Person` というエンティティは `name` と `age` という2つの属性を持ち、 `Car` は `make` と `mode` lという属性を持ちます。


```
 In [4]: # %load 02_entities.py
    ...: class Person(db.Entity):
    ...:     name = Required(str)
    ...:     age = Required(int)
    ...:     cars = Set('Car')
    ...:
    ...: class Car(db.Entity):
    ...:     make = Required(str)
    ...:     model = Required(str)
    ...:     owner = Required(Person)
    ...:
    ...: # show(Person)
 
```

今回作成したクラスは、DatabaseオブジェクトのDatabase.Entity属性から派生したものです。これは、通常のクラスではなく、エンティティであることに注意してください。エンティティのインスタンスはデータベースに格納されており、db変数にバインドされています。Ponyでは、複数のデータベースを同時に扱うことができますが、それぞれのエンティティは特定のデータベースに割り当てられています。

 `Person` というエンティティの中に、 `name` 、 `age` 、 `car` という3つの属性を作成しました。 `name` と `age` は必須の属性です。つまり、これらの属性はNoneという値を持つことはできません。 `name` は文字列で、 `age` は数値です。

 `cars` 属性は `Set()` で宣言されており、タイプは `Car` です。これは、他のエンティティと関連付け(リレーションシップ)があることを意味します。これは、 `Car` エンティティのインスタンスのコレクションを保持することができます。"Car "はここでは文字列として指定されていますが、これはその時点ではまだエンティティCarを宣言していなかったからです。

 `Car` エンティティには3つの必須属性があります。 `make` と `model` は文字列で、 `owner` 属性は一対多の関係を表す他方のものです。Ponyのリレーションシップは、常にリレーションシップの両側を表す2つの属性によって定義されます。

2つのエンティティ間で多対多のリレーションを作成する必要がある場合は、両端に2つの `Set` 属性を宣言する必要があります。Ponyは、中間データベーステーブルを自動的に作成します。

文字列(str型)は、Python3でユニコード文字列を表現するために使用されます。
インタラクティブモードでエンティティの定義を確認する必要がある場合は、 `show()` 関数を使用することができます。この関数にエンティティクラスまたはエンティティインスタンスを渡すと、定義が出力されます。

 ipython
```
 In [5]: show(Person)
 class Person(Entity):
     id = PrimaryKey(int, auto=True)
     name = Required(str)
     age = Required(int)
     cars = Set(Car)
 
```

エンティティに `id` という属性が追加されていることに注目してください。

各エンティティには、1つのエンティティを他のエンティティと区別するための**プライマリキー(Primary Key)**が必要です。ここではプライマリキー属性を定義していなかったので、自動的に作成したものです。プライマリキーが自動的に作成された場合、プライマリキーは数値(int型)の `id` という名前が使われます。プライマリキー属性を明示的に定義した場合は、任意の名前と型を指定することができます。Ponyは**複合プライマリキー(composite primary key)**にも対応しています。

プライマリキーが自動的に作成されると、オプションのautoが常にTrueに設定されます。これは、この属性の値が、データベースのインクリメンタルカウンタやデータベースシーケンスを使って自動的に割り当てられることを意味します。

### データベースへの接続
データベースオブジェクトには、 `Database.bind()` メソッドがあります。これは、宣言されたエンティティを特定のデータベースにアタッチするために使用します。

```
 db.bind(provider='sqlite', filename=':memory:')
```

この場合は、メモリ上に作成されたSQLiteデータベースに接続します。

 `bind()` に与える引数は、それぞれのデータベースに固有のものです。これらのパラメータは、DB-APIモジュールを使ってデータベースに接続する際に使用するものと同じです。

SQLite の場合は、データベースの作成場所に応じて、データベースのファイル名か文字列 ':memory:' を引数として与える必要があります。データベースがメモリー上に作成された場合は、Pythonが終了すると削除されることになります。ファイルに保存されたデータベースを扱うためには、 `bind()` を以下のように記述します。


```
 In [7]: # %load 03_connect.py
    ...: from pathlib import Path
    ...:
    ...: dir = Path.cwd()
    ...: dbfile = str(dir / 'database.sqlite')
    ...: db.bind(provider='sqlite', filename=dbfile, create_db=True)
    ...:
  
```

対話型にPythonを実行している場合は、このようにデータベースファイルは絶対パスで与える必要があります。
この例の場合は、 `create_db = True` としているので、データベースファイルが存在しなければ作成されます。

データベースへの接続方法は以下の通りです。

```
 # SQLite：インメモリ
 db.bind(provider='sqlite', filename=':memory:')
 # SQLite：ファイル
 db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
 
 # PostgreSQL
 db.bind(provider='postgres', user='', password='', host='', database='')
 
 # MySQL
 db.bind(provider='mysql', host='', user='', passwd='', db='')
 
 # Oracle
 db.bind(provider='oracle', user='', password='', dsn='')
 
 # CockroachDB
 db.bind(provider='cockroach', user='', password='', host='', database='', )
 
```

### エンティティのデータベーステーブルへのマッピング
次に、データを永続化するため、データベースにテーブルを作成する必要があります。
これには、Databaseオブジェクトの `generate_mapping()` メソッドを呼び出します。

```
 In [9]: # %load 04_mapping.py
    ...: db.generate_mapping(create_tables=True)
    ...:
 
```

 `generate_mapping()` の引数  `create_tables=True` は、テーブルがまだ存在していない場合は、SQLコマンド `CREATE TABLE` を使用してテーブルを作成します。
 `generate_mapping()` メソッドを呼び出す前に、データベースに接続されているすべてのエンティティが定義されている必要があります。

### デバッグモード
 `set_sql_debug()` 関数を使うと、Ponyがデータベースに送信するSQLコマンドを見ることができます。次のように呼び出すと、これ以後はデバッグモードをオンになります。

```
 In [11]: # %load 05_debugmode.py
    ...: set_sql_debug(True)
    ...:
```


デバッグモードでない場合で、発行されるSQLコマンドを確認したいときは、クエリオブジェクトの `get_sql()` メソッドを使用することができます。

### エンティティインスタンスの作成
3人のユーザと2台の車を表す、5つのオブジェクトを作成して、その情報をデータベースに保存してみます。


```
 In [13]: # %load 06_create_entities.py
     ...: p1 = Person(name='John', age=20)
     ...: p2 = Person(name='Mary', age=22)
     ...: p3 = Person(name='Bob', age=30)
     ...: c1 = Car(make='Toyota', model='Prius', owner=p2)
     ...: c2 = Car(make='Ford', model='Explorer', owner=p3)
     ...:
     ...: # commit()
     ...:
 
 In [14]: commit()
 GET NEW CONNECTION
 BEGIN IMMEDIATE TRANSACTION
 INSERT INTO "Person" ("name", "age") VALUES (?, ?)
 ['John', 20]
 
 INSERT INTO "Person" ("name", "age") VALUES (?, ?)
 ['Mary', 22]
 
 INSERT INTO "Person" ("name", "age") VALUES (?, ?)
 ['Bob', 30]
 
 INSERT INTO "Car" ("make", "model", "owner") VALUES (?, ?, ?)
 ['Toyota', 'Prius', 2]
 
 INSERT INTO "Car" ("make", "model", "owner") VALUES (?, ?, ?)
 ['Ford', 'Explorer', 3]
 
 COMMIT
```

Pony はトランザクションをサポートしていて、変更したオブジェクトをすぐにデータベースに保存することはしません。 `commit()` 関数が呼び出された後に、これらのオブジェクトが保存されます。
デバッグモードがオンになっている場合は、 `commit()` の間に、データベースに送信された5つのSQLコマンド `INSERT` が表示されます。 `rollback()` 関数を呼び出すと、現在のトランザクションをロールバックし、 `db_session()` のキャッシュをクリアします。

### データベースセッション

Python でデータベースとやりとりするコードは、データベースセッションの中に置かれなければなりません。対話型にPythonを使っているときは、データベースセッションを気にする必要はありません。それは、データベースセッションはPonyによって自動的に維持されるためです。しかし、PonyをPython スクリプトから使用する場合、すべてのデータベースとのやりとりは、データベースセッション内で行う必要があります。そのためには、データベースを操作する関数を `db_session()` デコレータで修飾する必要があります。


```
 In [16]: # %load 07_db_session.py
    ...: @db_session
    ...: def print_person_name(person_id):
    ...:     p = Person[person_id]
    ...:     print(p.name)
    ...:
    ...: @db_session
    ...: def add_car(person_id, make, model):
    ...:     Car(make=make, model=model, owner=Person[person_id])
    ...:
    
```

 `db_session()` デコレーターは、関数を終了する際に以下の処理を行います。

- 関数が例外を発生した場合は、トランザクションのロールバックを実行します。
- データが変更され、例外が発生しなかった場合は、トランザクションをコミットします。
- データベース接続を接続プールに戻す
- データベースのセッションキャッシュをクリアする

関数がデータを読み込んだだけで何も変更しない場合でも、コネクションプールに接続を戻すために `db_session()` を使用する必要があります。

エンティティ・インスタンスは、 `db_session()` 内でのみ有効です。これらのオブジェクトを使ってHTMLテンプレートをレンダリングする必要がある場合は、 `db_session()` 内で行う必要があります。

デコレーターの代わりに  `db_session() ` をコンテキストマネージャーとして使用する方法もあります。


```
 In [18]: # %load 08_context_manager.py
     ...: with db_session:
     ...:     p = Person(name='Kate', age=33)
     ...:     Car(make='Audi', model='R8', owner=p)
     ...:
     ...:
 BEGIN IMMEDIATE TRANSACTION
 INSERT INTO "Person" ("name", "age") VALUES (?, ?)
 ['Kate', 33]
 
 INSERT INTO "Car" ("make", "model", "owner") VALUES (?, ?, ?)
 ['Audi', 'R8', 4]
 
 COMMIT
 RELEASE CONNECTION
 
```



### クエリの作成
5つのオブジェクトが保存されたデータベースができたので、クエリを実行してみましょう。例えば、20歳以上の人のリストを返すクエリは次のようになります。


```
 In [20]: # %load 09_query.py
     ...: v1 = select(p for p in Person if p.age > 20)
     ...:
     ...: # print(v1)
     ...:
 
 In [21]: print(v1)
 <pony.orm.core.Query object at 0x106309bb0>
 
```

 `select()` 関数は、PythonジェネレータをSQLクエリに変換し、Queryクラスのインスタンスを返します。この SQL クエリは、クエリの反復処理を開始すると、データベースに送信されます。

オブジェクトのリストを取得する方法の一つとして、スライス演算子 （ `[:]` ) を適用する方法があります。

 ipytoh
```
 In [23]: # %load 10_query_slice.py
     ...: v1 = select(p for p in Person if p.age > 20)[:]
     ...:
     ...: # print(v1)
     ...:
 GET CONNECTION FROM THE LOCAL POOL
 SWITCH TO AUTOCOMMIT MODE
 SELECT "p"."id", "p"."name", "p"."age"
 FROM "Person" "p"
 WHERE "p"."age" > 20
 
 
 In [24]: print(v1)
 [Person[2], Person[3], Person[4]]
 
```

その結果、データベースに送信されたSQLクエリのテキストと、抽出されたオブジェクトのリストが表示されます。クエリの結果を印刷すると、エンティティのインスタンスは、エンティティ名とプライマリキーを角括弧で囲んだもの（例： `Person[2]` ）で表されます。

結果のリストの順序付けには、 `Query.order_by()` メソッドを使用できます。結果セットの一部だけが必要な場合は、Python のリストで行うのとまったく同じ方法で、スライス演算子を使用することができます。例えば、すべての人を名前でソートして、最初の2つのオブジェクトを抽出したい場合は、次のようにします。

 ipython
```
 In [26]: # %load 11_query_sort.py
     ...: v1 = select(p for p in Person).order_by(Person.name)[:2]
     ...:
     ...: # print(v1)
     ...:
 SELECT "p"."id", "p"."name", "p"."age"
 FROM "Person" "p"
 ORDER BY "p"."name"
 LIMIT 2
 
 
 In [27]: print(v1)
 [Person[3], Person[1]]
 
```


対話型にPythonで作業しているときに、すべてのオブジェクトの属性の値を見たいときがあります。そのような場合には、Queryクラスの `show() ` メソッドを使用することができます。

 ipython
```
 In [29]: # %load 12_query_show.py
     ...: v1 = select(p for p in Person).order_by(Person.name)[:2].show()
     ...:
     ...: # print(v1)
     ...:
 SELECT "p"."id", "p"."name", "p"."age"
 FROM "Person" "p"
 ORDER BY "p"."name"
 LIMIT 2
 
 id|name|age
 --+----+---
 3 |Bob |30
 1 |John|20
 
 In [30]: print(v1)
 None
 
```

 `show()` メソッドでは、 `to-many` 属性は表示されません。この場合は、データベースへの追加クエリが必要になるため、上記のように関連する車の情報が表示されません。しかし、 `to-one` の関係を持っているインスタンスは表示されます。

 pyhon
```
 In [32]: # %load 13_show.py
     ...: v1 = Car.select().show()
     ...:
     ...: # print(v1)
     ...:
 SELECT "c"."id", "c"."make", "c"."model", "c"."owner"
 FROM "Car" "c"
 
 id|make  |model   |owner
 --+------+--------+---------
 1 |Toyota|Prius   |Person[2]
 2 |Ford  |Explorer|Person[3]
 3 |Audi  |R8      |Person[4]
 
 In [33]: print(v1)
 None
 
```


オブジェクトのリストを取得するのではなく、得られたシーケンスを反復処理する必要がある場合は、スライス演算子を使わずにforループを使用することができます。


```
 In [35]: # %load 14_query_for.py
     ...: persons = select(p for p in Person if 'o' in p.name)
     ...:
     ...: def func(data):
     ...:     for d in data:
     ...:         print(d.name, d.age)
     ...:
     ...: # print(persons)
     ...: # func(persons)
     ...:
 
 In [36]: print(persons)
 <pony.orm.core.Query object at 0x105d54e20>
 
 In [37]: func(persons)
 SELECT "p"."id", "p"."name", "p"."age"
 FROM "Person" "p"
 WHERE "p"."name" LIKE '%o%'
 
 John 20
 Bob 30
 
```

この例では、 `name` 属性に小文字の `'o'` が含まれる `Person` オブジェクトをすべて取得し、その `name` と `age` を表示しています。

クエリは、必ずしもエンティティ・オブジェクトを返す必要はありません。
例えば、object属性で構成されたリストを取得することもできます。

```
 In [39]: # %load 15_query_as_list.py
     ...: v1 = select(p.name for p in Person if p.age != 30)[:]
     ...:
     ...: # print(v1)
     ...:
 SELECT DISTINCT "p"."name"
 FROM "Person" "p"
 WHERE "p"."age" <> 30
 
 
 In [40]: print(v1)
 ['John', 'Mary', 'Kate']
 
```



タプルのリストを取得する場合は次のようにします。

```
 In [42]: # %load 16_query_as_tuple.py
     ...: v1 = select((p, count(p.cars)) for p in Person)[:]
     ...:
     ...: # print(v1)
     ...:
 SELECT "p"."id", COUNT(DISTINCT "car"."id")
 FROM "Person" "p"
   LEFT JOIN "Car" "car"
     ON "p"."id" = "car"."owner"
 GROUP BY "p"."id"
 
 
 In [43]: print(v1)
 [(Person[1], 0), (Person[2], 1), (Person[3], 1), (Person[4], 1)]
 
```

この例では、Personオブジェクトと所有している車の台数からなるタプルのリストを取得しています。

Ponyでは、集約クエリを実行することもできます。ここでは、ある人の最高年齢を返すクエリの例を示します。

```
 In [45]: # %load 17_query_max.py
     ...: v1 = max(p.age for p in Person)
     ...:
     ...: # print(v1)
     ...:
     ...:
 SELECT MAX("p"."age")
 FROM "Person" "p"
 
 
 In [46]: print(v1)
 33
 
```



### オブジェクトの取得
プライマリキーを使ってオブジェクトを取得するには、プライマリキーの値を角括弧（ `[...]` )で囲んで指定する必要があります。

```
 In [48]: # %load 18_get_obj_by_id.py
     ...: p1 = Person[1]
     ...:
     ...: # print(p1)
     ...: # print(p1.name)
     ...:
 
 In [49]: print(p1)
 Person[1]
 
 In [50]: print(p1.name)
 John
 
```

デバッグモードで実行しているので、データベースにクエリが送信されるとSQLコマンドが表示されますが、この例では表示されていないことに注目してください。これは、このオブジェクトがデータベースのセッションキャッシュにすでに存在しているからです。キャッシュすることで、データベースに送信する必要のあるリクエストの数を減らすことができます。

他の属性でオブジェクトを取得するには、Entity.get()メソッドを使用します。

```
 In [52]: # %load 19_entity_get.py
     ...: mary = Person.get(name='Mary')
     ...:
     ...: # print(mary)
     ..." # print(mary.age)
     ...:
 SELECT "id", "name", "age"
 FROM "Person"
 WHERE "name" = ?
 LIMIT 2
 ['Mary']
 
 
 In [53]: print(mary)
 Person[2]
 
 In [54]: print(mary.age)
 22
 
```

このケースでは、オブジェクトがすでにキャッシュに読み込まれていたにもかかわらず、name属性がユニークキーではないため、クエリはまだデータベースに送信されなければなりません。データベース・セッション・キャッシュは、主キーまたはユニーク・キーでオブジェクトを検索する場合にのみ使用されます。

### オブジェクトの更新


```
 In [56]: # %load 20_chamge_value.py
     ...: v1 = mary.age
     ...: mary.age += 1
     ...: v2 = mary.age
     ...:
     ...: # print(v1)
     ...: # print(v2)
     ...: # commit()
     ...:
 
 In [57]: print(v1)
 22
 
 In [58]: print(v2)
 23
 
 In [59]: commit()
 BEGIN IMMEDIATE TRANSACTION
 UPDATE "Person"
 SET "age" = ?
 WHERE "id" = ?
   AND "name" = ?
   AND "age" = ?
 [23, 2, 'Mary', 22]
 
 COMMIT
 
```

Pony は、変更されたすべての属性を記録します。 `commit()` 関数が実行されると、現在のトランザクションで更新されたすべてのオブジェクトがデータベースに保存されます。Ponyは、データベースセッション中に変更された属性のみを保存します。

### SQL文でのクエリ
直接SQLクエリを実行してエンティティを選択する必要がある場合は、次のように `select_by_sql()` を使用します。


```
 In [61]: # %load 21_sql.py
     ...: x = 25
     ...: v1 = Person.select_by_sql('SELECT * FROM Person p WHERE p.age < $x')
     ...:
     ...: # print(v1)
     ...:
 BEGIN IMMEDIATE TRANSACTION
 SELECT * FROM Person p WHERE p.age < ?
 [25]
 
 
 In [62]: print(v1)
 [Person[1], Person[2]]
 
```


 `select_by_sqk()` の代わりに  `get_by_sql()` を使うこともできますが、SQLクエリを実行した結果が複数あるときは例外	 `MultipleObjectsFoundError` が発生することに注意してください。

-  `select_by_sql()` ：SQLクエリを実行した結果が複数ある場合
-  `get_by_sql()` ：SQLクレリを実行した結果が１つだけの場合


エンティティを使わずに、データベースを直接操作したい場合は、 `Database.select()` メソッドを使用します。

```
 In [64]: # %load 22_select.py
     ...: x = 25
     ...: v1 = db.select('name FROM Person WHERE age > $x')
     ...:
     ...: # print(v1)
     ...:
 select name FROM Person WHERE age > ?
 [25]
 
 
 In [65]: print(v1)
 ['Bob', 'Kate']
 
```

ここまでは、Ponyの基本的な機能を説明するために、対話型で実行して説明してきました。
次節以降では、より高度な使用方法を説明することにします。

### Ponyのクエリをもう少し詳しく説明
Pony がジェネレータ式の構文を使ってクエリを実行できることは紹介しました。この機能があるおかげで、開発者はデータベースに格納されているオブジェクトがメモリに格納されているかのように、Pythonのネイティブな構文を使って扱うことができるようになります。
また、クエリの記述には、Pythonのジェネレータ式やラムダを使うことができます。

Ponyに含まれているexample を使って実行例をみてみましょう。はじめにデータベースを初期化します。

```
 In [1]: !rm -f estore.sqlite
 
 In [2]: %load 30_db_init.py
 
 In [3]: # %load 30_db_init.py
    ...: # from pony.orm.examples.estore import *
    ...: from estore import *
    ...:
    ...: populate_database()
    ...:
 
```

このデータベースのスキームダイアグラムは、Ponyのオンラインサービスで[公開 ](https://editor.ponyorm.com/user/pony/eStore) されています。
![](https://gyazo.com/6ae04d13426ac9a5d78a5c9669744ae6.png)

ここで使用する  `estore.py` のオリジナルとの違いは次のとおりです。
オリジナルでは初期データを追加するSQLコマンドがたくさん出力されて、例示としては冗長なためデフォルトでは出力しないようにしています。
また、テーブル Customer に age フィールドを追加しています。

 estore.patch
```
 --- estore.py.orig	2021-08-18 11:03:02.000000000 +0900
 +++ estore.py	2021-08-18 10:57:24.000000000 +0900
 @@ -5,6 +5,7 @@
 
  from pony.converting import str2datetime
  from pony.orm import *
 +import os
 
  db = Database("sqlite", "estore.sqlite", create_db=True)
 
 @@ -12,6 +13,7 @@
      email = Required(str, unique=True)
      password = Required(str)
      name = Required(str)
 +    age = Required(int)
      country = Required(str)
      address = Required(str)
      cart_items = Set("CartItem")
 @@ -54,7 +56,7 @@
      name = Required(str, unique=True)
      products = Set(Product)
 
 -sql_debug(True)
 +sql_debug(os.getenv('PONY_DEBUG',False))
 
  db.generate_mapping(create_tables=True)
 
 @@ -66,19 +68,19 @@
 
  @db_session
  def populate_database():
 -    c1 = Customer(email='john@example.com', password='***',
 +    c1 = Customer(email='john@example.com', password='***', age=18,
                    name='John Smith', country='USA', address='address 1')
 
 -    c2 = Customer(email='matthew@example.com', password='***',
 +    c2 = Customer(email='matthew@example.com', password='***', age=24,
                    name='Matthew Reed', country='USA', address='address 2')
 
 -    c3 = Customer(email='chuanqin@example.com', password='***',
 +    c3 = Customer(email='chuanqin@example.com', password='***', age=38,
                    name='Chuan Qin', country='China', address='address 3')
 
 -    c4 = Customer(email='rebecca@example.com', password='***',
 +    c4 = Customer(email='rebecca@example.com', password='***', age=42,
                    name='Rebecca Lawson', country='USA', address='address 4')
 
 -    c5 = Customer(email='oliver@example.com', password='***',
 +    c5 = Customer(email='oliver@example.com', password='***', age=55,
                    name='Oliver Blakey', country='UK', address='address 5')
 
      tablets = Category(name='Tablets')
```

### Python ジェネレータを使ったクエリ
Pony では、データベースのクエリを書く非常に自然な方法として、ジェネレータを使うことができます。Pony には  `select()` 関数があり、Python ジェネレータを受け取り、それを SQL に変換してデータベースからオブジェクトを返します。

ジェネレータを使用したクエリの例は次に示します。

```
 In [5]: # %load 31_query_generator.py
    ...: v1 = select(c for c in Customer
    ...:             if sum(o.total_price for o in c.orders) > 2)
    ...:
    ...: # print(v1)
    ...:
 
 In [6]: print(v1)
 <pony.orm.core.Query object at 0x1091347f0>
 
```

Ponyでは、コレクションのアトリビュートは、コレクションがそのアイテムのアトリビュートを取得するという、**アトリビュートリフティング(attribute lifting)**を提供しています。

```
 In [7]: %load 32_query_attribute_lifting.py
 
 In [8]: # %load 32_query_attribute_lifting.py
    ...: query = select(c for c in Customer
    ...:             if sum(c.orders.total_price) > 2)
    ...:
    ...: # print(query)
    ...:
 
 In [9]: print(query)
 <pony.orm.core.Query object at 0x11206c6a0>
 
```

 `filter()` 関数でクエリの実行結果を絞り込むこともできます。

```
 In [10]: %load 33_qeury_filter.py
 
 In [11]: # %load 33_qeury_filter.py
     ...: query2 = query.filter(lambda customer: customer.age > 18)
     ...:
     ...: # print(query2)
     ...:
 
 In [12]: print(query2)
 <pony.orm.core.Query object at 0x105227dc0>
```

また、クエリの結果を他のクエリで使用することもできます。

```
 In [14]: # %load 34_query_reuse.py
     ...: query3 = select(customer.name for customer in query2
     ...:             if customer.country == 'USA')
     ...:
     ...: # print(query3)
     ...:
 
 In [15]: print(query3)
 <pony.orm.core.Query object at 0x105274a90>
 
```

 `select()` 関数は、Queryクラスのインスタンスを返すので、Queryオブジェクトのメソッドを呼び出して、結果を取得することができます。
例えば、クエリの結果からはじめのものを取得するためには次のように `first()` メソッドを呼び出します。

```
 In [17]: # %load 35_query_first.py
     ...: customer_name = query3.first()
     ...:
     ...: # print(customer_name)
     ...:
 
 In [18]: print(customer_name)
 Matthew Reed
 
```

 `first()` メソッドはクエリ結果が空（つまり該当するレコードが 0 件）だったときは  `None` を返します

クエリからは、エンティティ、属性、または任意の式のタプルを返すことができます。
少し複雑に見えますが、次のように重ねることができます。

```
 In [20]: # %load 36_query_multi.py
     ...: v1 = select((c, sum(c.orders.total_price))
     ...:             for c in Customer if sum(c.orders.total_price) > 100)
     ...:
     ...: # print(v1)
     ...: # print(v1.first())
     ...:
 
 In [21]: print(v2)
 <pony.orm.core.Query object at 0x10b321e50>
 
 In [22]: print(v2.first())
 (Customer[1], Decimal('770.5'))
 
```

### ラムダ式を使ったクエリ
Ponyでは、ジェネレータの代わりにラムダ式を使ってクエリを記述することができます。

```
 In [24]: # %load 37_query_lambda.py
     ...: v1 = Customer.select(lambda c: sum(c.orders.total_price) > 100)
     ...:
     ...: # print(v1)
     ...: # print(v1.first())
     ...:
 
 In [25]: print(v1)
 <pony.orm.core.Query object at 0x11094a520>
 
 In [26]: print(v1.first())
 Customer[1]
 
```


クエリをジェネレータで記述しても、ラムダ式で記述しても、SQLに変換するという視点では両者の違いはありません。
ただし、ラムダ式を使った場合では、エンティティのインスタンスしか返せないことに注意してください。

## クエリ関数


### sum()
> sum(gen, distinct=None)
>     gen:：Python ジェネレータ
>     distict：個別のパラメタ
>     戻り値：数値


```
 In [1]: %load 40_sum.py
 
 In [2]: # %load 40_sum.py
    ...: from estore import *
    ...:
    ...: v1 = sum(o.total_price for o in Order)
    ...:
    ...: # print(v1)
    ...:
 
 In [3]: print(v1)
 2272.8
 
```

### avg()
> avg(gen, distinct=None)
>     gen:：Python ジェネレータ
>     distict：個別のパラメタ
>     戻り値：数値


```
 In [2]: # %load 41_avg.py
    ...: from estore import *
    ...:
    ...: v1 = avg(o.total_price for o in Order)
    ...:
    ...: # print(v1)
    ...:
 
 In [3]: print(v1)
 454.56000000000006
 
```

### max()
> max(gen)
>     gen: Pythonジェネレータ

クエリは、単一の属性を返す必要があります。
 pyton
```
 In [2]: # %load 42_max.py
    ...: from university1 import *
    ...:
    ...: v1 = max(s.gpa for s in Student)
    ...:
    ...: # print(v1)
    ...:
 
 In [3]: print(v1)
 4.0
 
```

### min()
> max(gen)
>     gen: Pythonジェネレータ

クエリは、単一の属性を返す必要があります。
 pyton
```
 In [2]: # %load 43_min.py
    ...: from university1 import *
    ...:
    ...: v1 = min(s.gpa for s in Student)
    ...:
    ...: # print(v1)
    ...:
 
 In [3]: print(v1)
 3.0
 
```

### len()
> len(*args)
> args：Pythonジェネレータ
> 戻り値：数値

 `count()` と同様に、クエリ内でのみ使用できます。

```
 In [2]: # %load 44_len.py
    ...: from university1 import *
    ...: from pprint import pprint
    ...:
    ...: v1 = Student.select(lambda s: len(s.courses) > 2)
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         pprint(f'{d.name} {d.courses}')
    ...:
    ...: # print(v1)
    ...: # func(v1)
    ...:
 
 In [3]: print(v1)
 <pony.orm.core.Query object at 0x10aae68e0>
 
 In [4]: func(v1)
 ("John Smith CourseSet([Course['Quantum Mechanics',3], Course['Data Structures "
  "and Algorithms',3], Course['Web Design',1], Course['Statistical "
  "Methods',2]])")
 ("Matthew Reed CourseSet([Course['Statistical Methods',2], "
  "Course['Thermodynamics',2], Course['Web Design',1], Course['Linear "
  "Algebra',1]])")
 ("Chuan Qin CourseSet([Course['Quantum Mechanics',3], Course['Linear "
  "Algebra',1], Course['Thermodynamics',2]])")
 ("Rebecca Lawson CourseSet([Course['Web Design',1], "
  "Course['Thermodynamics',2], Course['Statistical Methods',2], Course['Quantum "
  "Mechanics',3]])")
 ("Maria Ionescu CourseSet([Course['Statistical Methods',2], Course['Web "
  "Design',1], Course['Quantum Mechanics',3], Course['Data Structures and "
  "Algorithms',3]])")
 ("Oliver Blakey CourseSet([Course['Data Structures and Algorithms',3], "
  "Course['Thermodynamics',2], Course['Web Design',1]])")
 ("Jing Xia CourseSet([Course['Web Design',1], Course['Thermodynamics',2], "
  "Course['Quantum Mechanics',3], Course['Linear Algebra',1]])")
 
```


### between()
> between(x, a, b)
>     このクエリ関数はSQLコマンド  `x BETWEEN a AND b` に変換され、 `x >= a AND x <= b` という条件と同じになります。


```
 In [2]: # %load 45_between.py
    ...: from estore import *
    ...:
    ...: v1 = select(p for p in Customer if between(p.age, 18, 65))
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.name}  {d.age}')
    ...:
    ...: # print(v1)
    ...: # func(v1)
    ...:
 
 In [3]: print(v1)
 <pony.orm.core.Query object at 0x1102f2100>
 
 In [4]: func(v1)
 John Smith  18
 Matthew Reed  24
 Chuan Qin  38
 Rebecca Lawson  42
 Oliver Blakey  55
 
```

### coalesce()
> coalesce(*args)
> args：リスト


```
 In [2]: # %load 46_coalesce.py
    ...: from estore import *
    ...:
    ...: v1 = select(coalesce(p.description, '') for p in Product)
    ...:
    ...: # print(v1)
    ...: # print(v1.first())
    ...:
 
 In [3]: print(v1)
 <pony.orm.core.Query object at 0x108931fa0>
 
 In [4]: print(v1.first())
 Amazon tablet for web, movies, music, apps, games, reading and more
 
```

### concat()
> concat(*args)
> args：リスト


```
 In [2]: # %load 47_concat.py
    ...: from estore import *
    ...:
    ...: v1 = select(concat(p.name, ' ', p.country) for p in Customer)
    ...:
    ...: # print(v1)
    ...: # print(v1.first())
    ...:
 
 In [3]: print(v1)
 <pony.orm.core.Query object at 0x10b85e1f0>
 
 In [4]: print(v1.first())
 Chuan Qin China
 
```

### count()
> count(gen, distinct=None)
>     gen:：Python ジェネレータ
>     distict：個別のパラメタ
>     戻り値：数値


```
 In [2]: # %load 48_count.py
    ...: from estore import *
    ...:
    ...: v1 = count(c for c in Customer if len(c.orders) > 1)
    ...:
    ...: # print(v1)
    ...:
 
 In [3]: print(v1)
 1
 
```


### delete()
> delete(gen, distinct=None)
>     gen:：Python ジェネレータ
>      distict：個別のパラメタ

データベースからオブジェクトを削除します。Pony はオブジェクトをメモリにロードし、それを一つずつ削除していきます。エンティティにフック `before_delete()` や `after_delete()` が定義されていれば、Ponyはそれらをそれぞれ呼び出します。
オブジェクトをメモリにロードせずに削除したい場合は、 `delete()` メソッドの引数に `bulk=True` を与えます。この場合は、エンティティにフックが定義されていても呼び出されません。
戻り値は削除したオブジェクトの数です。


```
 In [2]: # %load 49_delete.py
    ...: from estore import *
    ...:
    ...: v1 = delete(o for o in Order if o.state == CANCELLED)
    ...: v2 = delete(o for o in Order if o.state == DELIVERED)
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 0
 
 In [4]: print(v2)
 3
 
```

### desc()
> desc(attr)
>     attr: エンティティーの属性


```
 In [2]: # %load 50_desc.py
    ...: from estore import *
    ...:
    ...: v1 = select(o for o in Order).order_by(Order.date_shipped)
    ...: v2 = select(o for o in Order).order_by(desc(Order.date_shipped))
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.id} {d.date_shipped} {d.state}')
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # func(v1)
    ...: # func(v2)
    ...:
 
 In [3]: print(v1)
 <pony.orm.core.Query object at 0x10d085b80>
 
 In [4]: print(v2)
 <pony.orm.core.Query object at 0x10d09cb50>
 
 In [5]: func(v1)
 5 None CREATED
 1 2012-10-21 11:34:00 DELIVERED
 3 2012-11-04 11:47:00 DELIVERED
 2 2013-01-10 14:03:00 DELIVERED
 4 2013-03-12 09:40:00 SHIPPED
 
 In [6]: func(v2)
 4 2013-03-12 09:40:00 SHIPPED
 2 2013-01-10 14:03:00 DELIVERED
 3 2012-11-04 11:47:00 DELIVERED
 1 2012-10-21 11:34:00 DELIVERED
 5 None CREATED
```

### distinct()
>distinct(gen, distinct=None)
>      gen:：Python ジェネレータ
クエリの結果から重複したものをひとつにまとめる場合は、SQLコマンドでは `DISTINCT` を使用します。Ponyでクエリに強制的に、 `DISTINCT` を実行したい場合は、  `distinct()` 関数を使います。しかし、Pony はインテリジェントな方法で自動的に  `DISTINCT` を追加するので、通常はこの関数を使用する必要はありません。
Ponyで `distinct()` を使用するケースは次のように `sum()` などと組み合わせる場合です。


```
 In [2]: # %load 51_distinct.py
    ...: from estore import *
    ...:
    ...: v1 = distinct(o.date_shipped for o in Order)
    ...: v2 = select(sum(distinct(x.total_price)) for x in Order)
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v2.first())
    ...:
 
 In [3]: print(v1)
 <pony.orm.core.Query object at 0x1108b3730>
 
 In [4]: print(v2)
 <pony.orm.core.Query object at 0x10f6dd9d0>
 
 In [5]: print(v2.first())
 2272.8
 
```

### exists()
> exist(gen, globals=None, locals=None)
>     gen：Python ジェネレータ
>     globals：クエリで使用されるグローバル変数の辞書
>     locals：オプションのパラメータで、クエリ内で使用される変数とその値を含む辞書
> 戻り値：True、False
指定された条件のインスタンスが少なくとも1つ存在する場合は `True` 、そうでない場合は `False` を返します。


```
 In [2]: # %load 52_exists.py
    ...: from estore import *
    ...:
    ...: v1 = exists(o for o in Order if o.date_delivered is None)
    ...:
    ...: # print(v1)
    ...:
 
 In [3]: print(v1)
 True
 
```

### get()
> get(gen, globals=None, locals=None)
>     gen：Python ジェネレータ
>     globals：クエリで使用されるグローバル変数の辞書
>     locals：オプションのパラメータで、クエリ内で使用される変数とその値を含む辞書
> 戻り値：エンティティ、None
指定されたパラメータを持つオブジェクトが存在する場合はそのオブジェクトを、そのようなオブジェクトが存在しない場合は  `None` を返します。

指定されたパラメータを持つオブジェクトが複数存在する場合は、例外 `MultipleObjectsFoundError` を発生します。その場合は、 `select(...)` を使ってオブジェクトを取得してください。
クエリオブジェクトの `get()` メソッドを使うこともできます。

```
 In [2]: # %load 53_get.py
    ...: from estore import *
    ...:
    ...: v1 = get(o for o in Order if o.id == 2)
    ...:
    ...: # print(v1)
    ...:
 
 In [3]: print(v1)
 Order[2]
 
```


### group_concat()
> group_concat(gen, sep=',', distinct=False)
>     gen： Python ジェネレータ
>     sep：セパレータ文字列、デフォルトはカンマ（ `,` ）
>     distinct：重複したものをひとつのまとめるかどうか True, False、デフォルトは False


```
 In [2]: # %load 54_group_concat.py
    ...: from estore import *
    ...:
    ...: v1 = group_concat((c.name for c in Customer), sep=',')
    ...:
    ...: # print(v1)
    ...:
 
 In [3]: print(v1)
 John Smith,Matthew Reed,Chuan Qin,Rebecca Lawson,Oliver Blakey
 
```


### join()

ここで別のデータベースを利用するため次の `example.university.py` を利用します。


```
 In [1]: !rm -f university1.sqlite
 
 In [2]: %load 55_universitydb.py
 
 In [3]: # %load 51_universitydb.py
    ...: # from pony.orm.examples.university1 import *
    ...: from university1 import *
    ...:
    ...: populate_database()
    ...:
 
 In [4]: show(Student)
 class Student(Entity):
     id = PrimaryKey(int, auto=True)
     name = Required(str)
     dob = Required(date)
     tel = Optional(str, default='')
     picture = Optional(bytes)
     gpa = Required(float, default=0.0)
     group = Required(Group)
     courses = Set(Course)
 
 In [5]: show(Group)
 class Group(Entity):
     number = PrimaryKey(int)
     major = Required(str)
     dept = Required(Department)
     students = Set(Student)
 
 In [6]: show(Course)
 class Course(Entity):
     name = Required(str)
     semester = Required(int)
     lect_hours = Required(int)
     lab_hours = Required(int)
     credits = Required(int)
     dept = Required(Department)
     students = Set(Student)
     PrimaryKey(name, semester)
 
```

Ponyが自動的に最適化を行わない場合に、クエリの最適化を行うために使用します。SQLクエリ内でサブクエリを生成するのではなく、SQコマンドの `JOIN` を使用します。
> joint(*args)
> args：クエリリスト


```
 In [2]: # %load 56_join.py
    ...: from university1 import *
    ...:
    ...: sql_debug(True)
    ...: v1 = select(g for g in Group if max(g.students.gpa) < 4)
    ...: v2 = select(g for g in Group if JOIN(max(g.students.gpa) < 4))
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v1.first())
    ...: # print(v2.first())
    ...:
 
 In [3]: print(v1)
 <pony.orm.core.Query object at 0x112093040>
 
 In [4]: print(v2)
 <pony.orm.core.Query object at 0x11348b760>
 
 In [5]: print(v1.first())
 GET NEW CONNECTION
 SWITCH TO AUTOCOMMIT MODE
 SELECT "g"."number"
 FROM "Group" "g"
   LEFT JOIN "Student" "student"
     ON "g"."number" = "student"."group"
 GROUP BY "g"."number"
 HAVING MAX("student"."gpa") < 4
 ORDER BY 1
 LIMIT 1
 
 SELECT "number", "major", "dept"
 FROM "Group"
 WHERE "number" = ?
 [102]
 
 Group[102]
 
 In [6]: print(v2.first())
 SELECT "g"."number"
 FROM "Group" "g"
   LEFT JOIN (
     SELECT "student"."group" AS "group", MAX("student"."gpa") AS "expr-1"
     FROM "Student" "student"
     GROUP BY "student"."group"
     ) "t-1"
     ON "g"."number" = "t-1"."group"
 WHERE "t-1"."expr-1" < 4
 GROUP BY "g"."number"
 ORDER BY 1
 LIMIT 1
 
 Group[102]
 
```

### left_join()
> left_join(gen, globals=None, locals=None)
>     gen：Python ジェネレータ
>     globals：クエリで使用されるグローバル変数の辞書
>     locals：オプションのパラメータで、クエリ内で使用される変数とその値を含む辞書
>    戻り値：エンティティ、None
 `left_joint()` の結果は、結合条件が右テーブルにマッチするレコードが見つけられなくても、常に左テーブルの結果を含んでいます。

例えば、各顧客の注文量を計算したいときは、以下のようなクエリを書くことができます。

```
 In [2]: # %load 57_left_join.py
    ...: from university1 import *
    ...:
    ...: sql_debug(True)
    ...: v1 = left_join((g, count(s.gpa <= 3),
    ...:                count(s.gpa > 3 and s.gpa <= 4),
    ...:                count(s.gpa > 4)) for g in Group for s in g.students)
    ...:
    ...: # print(v1)
    ...:
 
 In [3]: print(v1)
 <pony.orm.core.Query object at 0x104987be0>
 
 In [4]: print(v1.first())
 GET NEW CONNECTION
 SWITCH TO AUTOCOMMIT MODE
 SELECT "g"."number", COUNT(case when "s"."gpa" <= 3 then 1 else null end), COUNT(case when "s"."gpa" > 3 AND "s"."gpa" <= 4 then 1 else null end), COUNT(case when "s"."gpa" > 4 then 1 else null end)
 FROM "Group" "g"
   LEFT JOIN "Student" "s"
     ON "g"."number" = "s"."group"
 GROUP BY "g"."number"
 ORDER BY 1, 2, 3, 4
 LIMIT 1
 
 (Group[101], 1, 2, 0)
 
```

### raw_sql()
>raw_sql(sql, result_type=None)
>     sql：生のSQLを記述した文字列
>     result_type： SQLクエリの結果のタイプ
 `result_type` が指定された場合、Pony は生の SQL フラグメントの結果を指定された形式に変換します。


```
 In [2]: # %load 60_raw_sql.py
    ...: from university1 import *
    ...:
    ...: sql_debug(True)
    ...: v1 = select(s for s in Student if raw_sql('abs("s"."gpa") > 3'))
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.name} {d.gpa}')
    ...:
    ...: # print(v1)
    ...: # func(v1)
    ...:
 
 In [3]: print(v1)
 <pony.orm.core.Query object at 0x103964d90>
 
 In [4]: func(v1)
 GET NEW CONNECTION
 SWITCH TO AUTOCOMMIT MODE
 SELECT "s"."id", "s"."name", "s"."dob", "s"."tel", "s"."gpa", "s"."group"
 FROM "Student" "s"
 WHERE abs("s"."gpa") > 3
 
 Matthew Reed 3.5
 Chuan Qin 4.0
 Rebecca Lawson 3.3
 Maria Ionescu 3.9
 Oliver Blakey 3.1
 Jing Xia 3.2
 
```

### select()
> select(gen, globals=None, locals=None)
>     gen：Python ジェネレータ
>     globals：クエリで使用されるグローバル変数の辞書
>     locals：オプションのパラメータで、クエリ内で使用される変数とその値を含む辞書
> 戻り値：クエリオブジェクト、クエリオブジェクトのリスト


```
 In [2]: # %load 61_select.py
    ...: from university1 import *
    ...:
    ...: sql_debug(True)
    ...: v1 = select(s for s in Student)
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.name} {d.gpa}')
    ...:
    ...: # print(v1)
    ...: # func(v1)
    ...:
 
 In [3]: print(v1)
 <pony.orm.core.Query object at 0x1075d8550>
 
 In [4]: func(v1)
 GET NEW CONNECTION
 SWITCH TO AUTOCOMMIT MODE
 SELECT "s"."id", "s"."name", "s"."dob", "s"."tel", "s"."gpa", "s"."group"
 FROM "Student" "s"
 
 John Smith 3.0
 Matthew Reed 3.5
 Chuan Qin 4.0
 Rebecca Lawson 3.3
 Maria Ionescu 3.9
 Oliver Blakey 3.1
 Jing Xia 3.2
 
```

オブジェクトのリストを取得する必要がある場合は、結果のフルスライスを取得することができます。

```
 In [2]: # %load 62_select_slice.py
    ...: from university1 import *
    ...:
    ...: sql_debug(True)
    ...: v1 = select(s for s in Student)[:]
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.name} {d.gpa}')
    ...:
    ...: # print(v1)
    ...: # func(v1)
    ...:
 GET NEW CONNECTION
 SWITCH TO AUTOCOMMIT MODE
 SELECT "s"."id", "s"."name", "s"."dob", "s"."tel", "s"."gpa", "s"."group"
 FROM "Student" "s"
 
 
 In [3]: print(v1)
 [Student[1], Student[2], Student[3], Student[4], Student[5], Student[6], Student[7]]
 
 In [4]: func(v1)
 John Smith 3.0
 Matthew Reed 3.5
 Chuan Qin 4.0
 Rebecca Lawson 3.3
 Maria Ionescu 3.9
 Oliver Blakey 3.1
 Jing Xia 3.2
 
```

 `select()` 関数は、単一の属性のリストやタプルのリストを返すこともできます。

### set_sql_debug()
> set_sql_debug(value=True, show_values=None)
>     value：True を与えるとデバッグモード、デフォルトはTrue
>     show_values：Trueの場合、SQLテキストに加えて、クエリパラメータがログに記録される。

デフォルトでは、Ponyはデバッグ情報を標準出力に送信します。Python の標準的なロギングが設定されている場合は、Pony は標準出力の代わりにロギングへ出力します。
デバッグ情報をファイルに保存する場合は、次のようにします。

```
 In [2]: # %load 63_set_sql_debug.py
    ...: from university1 import *
    ...: import logging
    ...:
    ...: logging.basicConfig(filename='pony.log', level=logging.INFO)
    ...:
    ...: set_sql_debug(True)
    ...: v1 = select(s for s in Student)
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.name} {d.gpa}')
    ...:
    ...: # print(v1)
    ...: # func(v1)
    ...: # !cat pony.log
    ...:
 
 In [3]: print(v1)
 <pony.orm.core.Query object at 0x1130bda00>
 
 In [4]: func(v1)
 John Smith 3.0
 Matthew Reed 3.5
 Chuan Qin 4.0
 Rebecca Lawson 3.3
 Maria Ionescu 3.9
 Oliver Blakey 3.1
 Jing Xia 3.2
 
 In [5]: !cat pony.log
 INFO:pony.orm:GET NEW CONNECTION
 INFO:pony.orm:SWITCH TO AUTOCOMMIT MODE
 INFO:pony.orm.sql:SELECT "s"."id", "s"."name", "s"."dob", "s"."tel", "s"."gpa", "s"."group"
 FROM "Student" "s"
 
```

標準ライブラリの logging のデフォルトのログレベルは `WARNING` で、Ponyはデフォルトでメッセージに `INFO` レベルを使用するため、 `level=logging.INFO` を指定しなければならないことに注意してください。Ponyは2つのロガーを使用します。データベースに送信するSQL文には `pony.orm.sql` を、その他のメッセージには `pony.orm` を使用します。

### set_sql_debugging()
> set_sql_debug(value=True, show_values=None)
>     value：True を与えるとデバッグモード、デフォルトはTrue
>     show_values：Trueの場合、SQLテキストに加えて、クエリパラメータがログに記録される。
db_session 全体のデバッグを有効にする必要がある場合は、  `db_session()` デコレータやコンテキスト・マネージャの同様のパラメータを使用します。

```
 In [1]: !rm -f pony.log
  
 In [2]: %load 64_set_sql_debugging_enable.py
  
 In [3]: # %load 64_set_sql_debugging_enable.py
    ...: from university1 import *
    ...: import logging
    ...:
    ...: logging.basicConfig(filename='pony.log', level=logging.INFO)
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.name} {d.gpa}')
    ...:
    ...: with sql_debugging:  # デバッグ出力を有効にする
    ...:     v1 = select(s for s in Student)
    ...:     func(v1)
    ...:
    ...: # !cat pony.log
    ...:
 John Smith 3.0
 Matthew Reed 3.5
 Chuan Qin 4.0
 Rebecca Lawson 3.3
 Maria Ionescu 3.9
 Oliver Blakey 3.1
 Jing Xia 3.2
 
 In [4]: !cat pony.log
 INFO:pony.orm:GET NEW CONNECTION
 INFO:pony.orm:SWITCH TO AUTOCOMMIT MODE
 INFO:pony.orm.sql:SELECT "s"."id", "s"."name", "s"."dob", "s"."tel", "s"."gpa", "s"."group"
 FROM "Student" "s"
 
```


```
 In [1]: !rm -f pony.log
 
 In [2]: %load 65_set_sql_debugging_with_params.py
 
 In [3]: # %load 65_set_sql_debugging_with_params.py
    ...: from university1 import *
    ...: import logging
    ...:
    ...: logging.basicConfig(filename='pony.log', level=logging.INFO)
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.name} {d.gpa}')
    ...:
    ...: with sql_debugging(show_values=True):  # クエリパラメタも出力する
    ...:     v1 = select(s for s in Student if s.gpa > 3)
    ...:     func(v1)
    ...:
    ...: # !cat pony.log
    ...:
 Matthew Reed 3.5
 Chuan Qin 4.0
 Rebecca Lawson 3.3
 Maria Ionescu 3.9
 Oliver Blakey 3.1
 Jing Xia 3.2
 
 In [4]: !cat pony.log
 INFO:pony.orm:GET NEW CONNECTION
 INFO:pony.orm:SWITCH TO AUTOCOMMIT MODE
 INFO:pony.orm.sql:SELECT "s"."id", "s"."name", "s"."dob", "s"."tel", "s"."gpa", "s"."group"
 FROM "Student" "s"
 WHERE "s"."gpa" > 3
 
```


```
 In [1]: !rm -f pony.log
 
 In [2]: %load 66_set_sql_debugging_disable.py
 
 In [3]: # %load 66_set_sql_debugging_disable.py
    ...: from university1 import *
    ...: import logging
    ...:
    ...: logging.basicConfig(filename='pony.log', level=logging.INFO)
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.name} {d.gpa}')
    ...:
    ...: with sql_debugging(False):  # デバッグ出力を無効にする
    ...:     v1 = select(s for s in Student if s.gpa > 3)
    ...:     func(v1)
    ...:
    ...: # !cat pony.log
    ...:
 Matthew Reed 3.5
 Chuan Qin 4.0
 Rebecca Lawson 3.3
 Maria Ionescu 3.9
 Oliver Blakey 3.1
 Jing Xia 3.2
 
 In [4]: !cat pony.log
 
```

## Ponyのオンライン・データベースエディタ

Ponyは	[オンラインデータベーススキーマエディタ ](https://editor.ponyorm.com/)　が提供されていて、データベース設計を行うときにとても便利です。
サインアップすると次にプランを選択します。

 Plan

| Plan | Price | Private diagrams | Public diagrams | Export as image | Snapshots |
|:--|:--|:--|:--|:--|:--|
| Free | $0 | 0 | Unlimited | Yes | Yes |
| Basic | $9/month | Unlimited | Unlimited | Yes | Yes |
| Basic | $90/year | Unlimited | Unlimited | Yes | Yes |

プライベートなダイアグラムを作成したいときは有料プランを選択することになりますが、
違いはそれだけです。

#### Create Diagram
何もないメニューがある画面が表示されます。
![](https://gyazo.com/fd364643713b476e2dcfa484947f6ca1.png)


ここで、**New Entry** をクリックして、エンティティーをUser を作成します。
![](https://gyazo.com/052b9a6ee03e5a009460838e895f0154.png)

するとエンティティー User のダイアログが表示されます。


![](https://gyazo.com/07c1bbf598dd659fd67590d06fe6166b.png)

#### Add atribute

![](https://gyazo.com/82d8c508e8e2b5ae69c25c065fca78ca.png)

以下のように属性を設定しましょう。


![](https://gyazo.com/10023339d796ef12ce04166563f00494.png)
このあと、メニューバーにある **Modles** をクリックすると、
モデルクラスが表示されます。



```
 from pony.orm import *
 
 db = Database()
 
 class User(db.Entity):
     id = PrimaryKey(int, auto=True)
     name = Required(str)
     password = Required(str)
     uid = Required(int)
     group = Required(str)
 
 db.generate_mapping()
```

モデルの User クラスはデータベースでのテーブルを表現するものとなっています。
ここで、メニューの **SQLite** をクリックすると、データベースへのテーブル作成のSQLコマンドが表示されます。
実際には Pony がSQLコマンドを生成して実行してくれます。


## Pony をもっと便利にする Ponywhoosh について
ponywhoosh はPonyのデータベースを検索可能にしてくれる便利な拡張モジュールで、 `search()` 関数に与えたキーワードで簡単にデータベースを検索することができるようになります。

ponywhoosh は次のようにインストールします。
 bash
```
 $ pip install ponywhoosh
```

Ponywhooshオブジェクトを初期化します。

```
 from ponywhoosh import PonyWhoosh
 pw = PonyWhoosh()
```

必要に応じて、いくつかの設定を行います。

```
 pw.search_string_min_len= 3
 pw.indexes_path='ponyindexes'
 pw.writer_timeout= 2
```

この例の設定では、インデックスを保存するデフォルトのフォルダ、デバッグを有効にするかどうか、クエリの文字列の最小長、タイムアウト（時間がかかりすぎると検索を停止するまでの時間）などを設定します。

デコレータ `@pw` を使って検索対象にするPonyのモデルクラスを修飾します。
これにより、PonyWhoosh はどのような属性が検索可能であるかを知ることができます。


```
 @pw.register_model('name','age', sortable=True,  stored=True)
 class User(db.Entity):
     _table_ = 'User'
     id = PrimaryKey(int, auto=True)
     name = Required(unicode)
     tipo = Optional(unicode)
     age = Optional(int)
     entries = Set("Entry")
     attributes = Set("Attributes")
     
```

デコレータ `@pw` に、検索対象にしたいフィールドを文字列として定義します。（上記の例では、 `name` と `age` ）。並べ替え可能かどうか( `sortable` )、保存可能かどうか( `stored` )、スコアリング可能( `scored` )など、カンマで区切って列挙するだけで、whooshのすべてのパラメータが利用できます。

ponywhoosh で配布されている [example.py ](https://raw.githubusercontent.com/jonaprieto/ponywhoosh/master/example.py) から抜粋したものを例示します。

```
 from pony.orm                import *
 from ponywhoosh              import PonyWhoosh
 
 pw = PonyWhoosh()
 
 # configurations
 pw.indexes_path          = 'ponyindexes'
 pw.search_string_min_len = 1
 pw.writer_timeout        = 2
 
 db = Database()
 
 @pw.register_model('number', 'name')
 class Department(db.Entity):
   number  = PrimaryKey(int, auto=True)
   name    = Required(str, unique=True)
   groups  = Set("Group")
   courses = Set("Course")
 
 @pw.register_model('number', 'major')
 class Group(db.Entity):
   number    = PrimaryKey(int)
   major     = Required(str)
   dept      = Required("Department")
   students  = Set("Student")
 
 @pw.register_model('name', 'semester', 'lect_hours', 'lab_hours', 'credits')
 class Course(db.Entity):
   name        = Required(str)
   semester    = Required(int)
   lect_hours  = Required(int)
   lab_hours   = Required(int)
   credits     = Required(int)
   dept        = Required(Department)
   students    = Set("Student")
   PrimaryKey(name, semester)
 
 @pw.register_model('name', 'tel', 'gpa')
 class Student(db.Entity):
   id        = PrimaryKey(int, auto=True)
   name      = Required(str)
   dob       = Required(date)
   tel       = Optional(str)
   picture   = Optional(buffer, lazy=True)
   gpa       = Required(float, default=0)
   group     = Required(Group)
   courses   = Set(Course)
   
 db.bind('sqlite', 'example.sqlite', create_db=True)
 db.generate_mapping(create_tables=True)
 
 @db_session
 def populate_database():
   if select(s for s in Student).count() > 0:
     return
     
   # データベースに登録する処理
     d1 = Department(name="Department of Computer Science")
     d2 = Department(name="Department of Mathematical Sciences")
     d3 = Department(name="Department of Applied Physics")
   
     c1 = Course(
         name="Web Design"
       , semester=1
       , dept=d1
       , lect_hours=30
       , lab_hours=30
       , credits=3
       )
       # ...(中略)
      s7 = Student(
          name='Jing Xia'
        , dob=date(1988, 12, 30)
        , gpa=3.2
        , group=g102
        , courses=[c1, c3, c5, c6]
        )
   commit()
```

このあとは、 `search()` 関数でデータベースを検索lすることができます。

```
 In [2]: # %load 90_search.py
    ...: from example import *
    ...: from ponywhoosh import search
    ...: from pprint import pprint
    ...:
    ...: populate_database()
    ...:
    ...: v1 = search(Student, "smith")
    ...:
    ...: # pprint(v1)
    ...:
 
 In [3]: pprint(v1)
 {'cant_results': 4,
  'facet_names': dict_keys([]),
  'matched_terms': {'name': [b'smith']},
  'results': [{'docnum': 21, 'pk': ('1',), 'score': 2.7227665977411037}],
  'runtime': 0.001474735999999588}
 
```

第１引数はモデルクラスを与え、第2引数に検索文字列を与えます。このとき検索文字列にワイルドカードを使用する場合は次のように引数を与えます。

```
 search(PonyModel, query, add_wildcards=True)
```


 `something=True` 引数は、最初に  `add_wildcards=False` の値で検索を実行しますが、結果が空の場合には、自動的に結果にワイルドカードを追加して検索を再実行します。


```
 In [2]: # %load 91_search_wildcard.py
    ...: from example import *
    ...: from ponywhoosh import search
    ...: from pprint import pprint
    ...:
    ...: v1 = search(Student, "s", add_wildcards=False)
    ...: v2 = search(Student, "s", add_wildcards=True)
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...:
 
 In [3]: pprint(v1)
 {'cant_results': 0,
  'facet_names': dict_keys([]),
  'matched_terms': {},
  'results': [],
  'runtime': 0.0001652000000005316}
 
 In [4]: pprint(v2)
 {'cant_results': 9,
  'facet_names': dict_keys([]),
  'matched_terms': {'name': [b'ionescu', b'smith', b'lawson']},
  'results': [{'docnum': 19, 'pk': ('4',), 'score': 2.6582280766035327},
              {'docnum': 20, 'pk': ('5',), 'score': 2.6582280766035327},
              {'docnum': 16, 'pk': ('1',), 'score': 2.6582280766035327}],
  'runtime': 0.0031039169999997895}
 
```

 `search()` 関数は、選択された情報を含む辞書を返します。

-  `cant_results` : サーチャーが収集したドキュメントの総数
-  `facet_names` ：結果をグループ化するために使用された項目を返すので、 `groupedby` 引数と一緒に使うと便利になる
-  `matched_terms` : サーチ可能なフィールドと、クエリによって与えられたマッチを保存する辞書
-  `runtime` : サーチにかかった時間
-  `results` : 個々の結果のための辞書のリスト。以下を含んだもの。
  -  `rank` : その結果の位置
  -  `result` : その項目のプライマリキーと対応する値
  -  `score` : その項目の検索結果のスコア
  -  `pk:` プライマリキーまたはプライマリキーのセット


```
 In [2]: # %load 92_search_params.py
    ...: from example import *
    ...: from ponywhoosh import search
    ...: from pprint import pprint
    ...:
    ...: v1 = search(Student, "smith", include_entity=True, use_dict=False)
    ...: v2 = search(Student, "smith", include_entity=True, use_dict=True)
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...:
 
 In [3]: pprint(v1)
 {'cant_results': 4,
  'facet_names': dict_keys([]),
  'matched_terms': {'name': [b'smith']},
  'results': [{'docnum': 21,
               'entity': [('name', 'John Smith'),
                          ('tel', '123-456'),
                          ('gpa', 3.0)],
               'model': 'Student',
               'other_fields': [('group', 101),
                                ('id', 1),
                                ('dob', datetime.date(1990, 11, 26))],
               'pk': ('1',),
               'score': 2.7227665977411037}],
  'runtime': 0.0010187430000003772}
 
 In [4]: pprint(v2)
 {'cant_results': 4,
  'facet_names': dict_keys([]),
  'matched_terms': {'name': [b'smith']},
  'results': [{'docnum': 21,
               'entity': {'dob': datetime.date(1990, 11, 26),
                          'gpa': 3.0,
                          'group': 101,
                          'id': 1,
                          'name': 'John Smith',
                          'tel': '123-456'},
               'model': 'Student',
               'pk': ('1',),
               'score': 2.7227665977411037}],
  'runtime': 0.0008094239999998365}
 
```

フィールドの値でソートした例です。

```
 In [2]: # %load 93_sarch_sortedby.py
    ...: from example import *
    ...: from ponywhoosh import search
    ...: from pprint import pprint
    ...:
    ...: v1 = search(Student,"s", add_wildcards=True, sortedby="gpa")
    ...:
    ...: # pprint(v1)
    ...:
 
 In [3]: pprint(v1)
 {'cant_results': 12,
  'facet_names': dict_keys([]),
  'matched_terms': {'name': [b'ionescu', b'lawson', b'smith']},
  'results': [{'docnum': 11, 'pk': ('5',), 'score': 0},
              {'docnum': 21, 'pk': ('1',), 'score': 0},
              {'docnum': 15, 'pk': ('4',), 'score': 0}],
  'runtime': 0.006970755999999412}
 
```


## まとめ
Pony ORM を使うことでSQLに詳しくなくても簡単にデータベース操作を行うことができるようになります。
Microsft SQLServer などサポートされていないデータベースがあることには留意が必要ですが、
データベースのスキーム設計で便利なオンラインサービスも有益で便利なため、使用検討する価値はあるでしょう。



## 参考資料
- [Pony 公式ドキュメント ](https://docs.ponyorm.org/toc.html)
  - [Pony APIレファレンス ](https://docs.ponyorm.org/api_reference.html)
- [Ponywhoosh 公式ドキュメント ](https://pythonhosted.org/ponywhoosh/index.html)

#database
#ORM


