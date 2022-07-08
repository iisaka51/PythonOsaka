Pythonチュートリアル：Peewee ORM を使ってみよう
=================
![](https://gyazo.com/1575a65039e16bc7f076bf263d698317.png)


## Peeweeについて

Peeweeは、Python で実装さあれたシンプルで小さな**ORM(Object-Relational Mapping)**です。少しばかりの（しかし表現力のある）コンセプトを持ち、学習しやすく、直感的に使えるようになっています。
次のような特徴があります。

- 小さくて表現力豊かなORM
- Python 2.7+および3.4+ (3.6で開発)
- SQLite, MySQL, PostgreSQL, CockroachDB をサポートしています。
- 豊富な拡張機能

## インストール
Peewee のインストールは pip で行います。
 bash
```
 $ pip install peewee
```

## Peewee の使い方

### モデルの作成
データモデルを作るために、1つまたは複数のModelクラスを定義します。

 model_person.py
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

外部キーを使ってモデル間のリレーションを設定することも、Peeweeでは簡単です。
 model_per.py
```
 from model_person iport *

 class Pet(Model):
     owner = ForeignKeyField(Person, backref='pets')
     name = CharField()
     animal_type = CharField()

     class Meta:
         database = db
```


### データベースへの接続
モデルができたので、データベースに接続してみましょう。

 pyton
```
 db.connect()
```

Peewee では明示的に接続をオープンする必要はありません。最初のクエリが実行されたときに自動で処理され、データベース接続のエラーがあればすぐにわかります。また、接続が完了したら接続を閉じることができます。例えば、ウェブアプリケーションでは、リクエストを受信したときに接続を開き、レスポンスを送信したときに接続を閉じることができます。

### テーブル作成

データを格納するデータベースのテーブルを作成します。これにより、適切なカラム、インデックス、シーケンス、および外部キー制約を持つテーブルが作成されます。


```
 db.create_tables([Person, Pet])
```

ここまでの内容をモジュールにしておきます。

 models.py
```
 from peewee import *

 db = SqliteDatabase('people.db')

 class Person(Model):
     name = CharField()
     birthday = DateField()

     class Meta:
         database = db

 class Pet(Model):
     owner = ForeignKeyField(Person, backref='pets')
     name = CharField()
     animal_type = CharField()

     class Meta:
         database = db

 if __name__ == '__main__':
     db.create_tables([Person, Pet])
```

### データの保存
データベースに何人かの人を登録してみましょう。 `save()` メソッドと `create()` メソッドを使って、 `Person` のレコードを追加・更新していきます。
 `save()` メソッドは更新したデータ数を返します。 `create()` メソッドはモデル・インスタンスを返します。



```
 In [1]: !rm -f people.db

 In [2]: %run models.py

 In [3]: %load 01_step_01_store.py

 In [4]: # %load 01_step_01_store.py
    ...: from models import *
    ...: from datetime import date
    ...:
    ...: uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15))
    ...: v1 = uncle_bob.save()
    ...:
    ...: # print(uncle_bob)
    ...: # print(v1)
    ...:

 In [5]: print(uncle_bob)
 1

 In [6]: print(v1)
 1

```

### データの更新
行を更新するには、モデルのインスタンスを変更し、 `save()` メソッドを呼び出して変更を永続化します。


```
 In [8]: # %load 01_step_02_update.py
    ...: grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1))
    ...: herb = Person.create(name='Herb', birthday=date(1950, 5, 5))
    ...:
    ...: v1 = grandma.name
    ...: grandma.name = 'Grandma L.'
    ...: v2 = grandma.save()
    ...: v3 = grandma.name
    ...:
    ...: # print(grandma)
    ...: # print(herb)
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v3)
    ...:

 In [9]: print(grandma)
 2

 In [10]: print(herb)
 3

 In [11]: print(v1)
 Grandma

 In [12]: print(v2)
 1

 In [13]: print(v3)
 Grandma L.

```

これで、データベースに3人がPersonテーブルに格納されました。彼らにペットを与えてみましょう。


```
 In [15]: # %load 01_step_03_add_pet.py
     ...: bob_kitty = Pet.create(
     ...:                 owner=uncle_bob, name='Kitty', animal_type='cat')
     ...: herb_fido = Pet.create(
     ...:                 owner=herb, name='Fido', animal_type='dog')
     ...: herb_mittens = Pet.create(
     ...:                 owner=herb, name='Mittens', animal_type='cat')
     ...: herb_mittens_jr = Pet.create(
     ...:                 owner=herb, name='Mittens Jr', animal_type='cat')
     ...:

```


### データの削除
Herb が買っていた mittens が病気になって死んでしまったとします。mittensをデータベースから削除する必要があります。
こうしたときは、 `delete_instance()` メソッドを呼び出します。このメソッドは、削除したオブジェクトの数を返します。


```
 In [17]: # %load 01_step_04_delete.py
     ...: v1 = herb_mittens.delete_instance()
     ...:
     ...: # print(v1)
     ...:

 In [18]: print(v1)
 1

```

Herb が飼っていた Fido を Bob が引き取ったとします。 `owner` が変わるので次のようになります。


```
 In [20]: # %load 01_step_05_owner_change.py
     ...: herb_fido.owner = uncle_bob
     ...: v1 = herb_fido.save()
     ...:
     ...: # print(v1)
     ...:

 In [21]: print(v1)
 1

```

### データの取得
データベースを利用する利点には、クエリを使ってデータを自由に取り出すことができることがあります。リレーショナルデータベースは、その場限りの問い合わせをするのに適しています。

### 単一レコードの取得
データベースからおばあちゃんのレコードを取得してみましょう。データベースから 1 つのレコードを取得するには、 `select().get()` を使用します。あるいは、 `モデルクラス.get()` でも取得できます。


```
 In [23]: # %load 01_step_06_retreive.py
     ...: grandma = Person.select().where(Person.name == 'Grandma L.').get()
     ...: grandma = Person.get(Person.name == 'Grandma L.')
     ...:

```


### レコードのリスト化
データベースに登録されているすべての人をリストアップしてみましょう。


```
 In [25]: # %load 01_step_07_list_of_records.py
     ...: v1 = Person.select()
     ...:
     ...: def func(data):
     ...:     for d in data:
     ...:         print(f'{d.name}')
     ...:
     ...: # func(v1)
     ...: # print(v1)
     ...:

 In [26]: func(v1)
 Bob
 Grandma L.
 Herb

 In [27]: print(v1)
 SELECT "t1"."id", "t1"."name", "t1"."birthday" FROM "person" AS "t1"


```

データベースに登録されているペットの情報から猫について取得します。

```
 In [29]: # %load 01_step_08_cat_owner.py
     ...: v1 = Pet.select().where(Pet.animal_type == 'cat')
     ...:
     ...: def func(data):
     ...:     for d in data:
     ...:         print(f'{d.name} {d.owner.name}')
     ...:
     ...: # func(v1)
     ...: # print(v1)
     ...:

 In [30]: func(v1)
 Kitty Bob
 Mittens Jr Herb

 In [31]: print(v1)
 SELECT "t1"."id", "t1"."owner_id", "t1"."name", "t1"."animal_type" FROM "pet" AS "t1" WHERE ("t1"."animal_type" = 'cat')

```

この例は、期待どおりに動作しますし、何も問題ないように見えます。しかし、実は大きな問題があります。 `pet.owner.name` にアクセスしているのに、最初のクエリでこのリレーションを選択していないため、Peeweeはペットの所有者を取得するために追加のクエリを実行しなければなりません。
これは、**N+1 問題**と呼ばれ、一般的には避けるべきです。

改良したコードが次のものです。


```
 In [33]: # %load 01_step_09_select_join.py
     ...: v1 = (Pet
     ...:          .select(Pet, Person)
     ...:          .join(Person)
     ...:          .where(Pet.animal_type == 'cat'))
     ...:
     ...: def func(data):
     ...:     for d in data:
     ...:         print(f'{d.name} {d.owner.name}')
     ...:
     ...: # func(v1)
     ...: # print(v1)
     ...:

 In [34]: func(v1)
 Kitty Bob
 Mittens Jr Herb

 In [35]: print(v1)
 SELECT "t1"."id", "t1"."owner_id", "t1"."name", "t1"."animal_type", "t2"."id", "t2"."name", "t2"."birthday" FROM "pet" AS "t1" INNER JOIN "person" AS "t2" ON ("t1"."owner_id" = "t2"."id") WHERE ("t1"."animal_type" = 'cat')


```

データベースから Bob が飼っているペットの情報を取得する。

```
 In [37]: # %load 01_step_10_select_join.py
     ...: v1 = Pet.select().join(Person).where(Person.name == 'Bob')
     ...:
     ...: def func(data):
     ...:     for d in data:
     ...:         print(f'{d.name}')
     ...:
     ...: # func(v1)
     ...: # print(v1)
     ...:

 In [38]: func(v1)
 Kitty
 Fido

 In [39]: print(v1)
 SELECT "t1"."id", "t1"."owner_id", "t1"."name", "t1"."animal_type" FROM "pet" AS "t1" INNER JOIN "person" AS "t2" ON ("t1"."owner_id" = "t2"."id") WHERE ("t2"."name" = 'Bob')

```

同じ処理を uncle_bob オブジェクトを使って取得する。

```
 In [41]: # %load 01_step_11_select_wher.py
     ...: v1 = Pet.select().where(Pet.owner == uncle_bob)
     ...:
     ...: def func(data):
     ...:     for d in data:
     ...:         print(f'{d.name}')
     ...:
     ...: # func(v1)
     ...: # print(v1)
     ...:

 In [42]: func(v1)
 Kitty
 Fido

 In [43]: print(v1)
 SELECT "t1"."id", "t1"."owner_id", "t1"."name", "t1"."animal_type" FROM "pet" AS "t1" WHERE ("t1"."owner_id" = 1)

```

Bobが飼っているペットを、 `order_by()` でペットの名前で昇順にソートして取得する。

```
 In [45]: # %load 01_step_12_select_wher_orderby.py
     ...: v1 =  Pet.select().where(Pet.owner == uncle_bob).order_by(Pet.name)
     ...:
     ...: def func(data):
     ...:     for d in data:
     ...:         print(f'{d.name}')
     ...:
     ...: # func(v1)
     ...: # print(v1)
     ...:

 In [46]: func(v1)
 Fido
 Kitty

 In [47]: print(v1)
 SELECT "t1"."id", "t1"."owner_id", "t1"."name", "t1"."animal_type" FROM "pet" AS "t1" WHERE ("t1"."owner_id" = 1) ORDER BY "t1"."name"

```

データベースに登録されている人の誕生日を、 `desc()` で降順ソートして取得する。

```
 In [49]: # %load 01_step_13_select_orderby_descb.py
     ...: v1 = Person.select().order_by(Person.birthday.desc())
     ...:
     ...: def func(data):
     ...:     for d in data:
     ...:         print(f'{d.name} {d.birthday}')
     ...:
     ...: # func(v1)
     ...: # print(v1)
     ...:

 In [50]: func(v1)
 Bob 1960-01-15
 Herb 1950-05-05
 Grandma L. 1935-03-01

 In [51]: print(v1)
 SELECT "t1"."id", "t1"."name", "t1"."birthday" FROM "person" AS "t1" ORDER BY "t1"."birthday" DESC

```


データベースに登録されている人の誕生日で、日時を指定した範囲にある人を取得する。

```
 In [53]: # %load 01_step_14_combine_filter.py
     ...: d1940 = date(1940, 1, 1)
     ...: d1960 = date(1960, 1, 1)
     ...:
     ...: v1 = (Person
     ...:          .select()
     ...:          .where((Person.birthday < d1940) | (Person.birthday > d1960)))
     ...:
     ...:
     ...: def func(data):
     ...:     for d in data:
     ...:         print(f'{d.name}  {d.birthday}')
     ...:
     ...: # func(v1)
     ...: # print(v1)
     ...:

 In [54]: func(v1)
 Bob  1960-01-15
 Grandma L.  1935-03-01

 In [55]: print(v1)
 SELECT "t1"."id", "t1"."name", "t1"."birthday" FROM "person" AS "t1" WHERE (("t1"."birthday" < '1940-01-01') OR ("t1"."birthday" > '1960-01-01'))

```

上記と同じ処理を  `between()` を使って記述すると次のようになります。

```
 In [57]: # %load 01_step_15_select_between.py
     ...: v1 = (Person
     ...:          .select()
     ...:          .where(Person.birthday.between(d1940, d1960)))
     ...:
     ...: def func(data):
     ...:     for d in data:
     ...:         print(f'{d.name}  {d.birthday}')
     ...:
     ...: # func(v1)
     ...: # print(v1)
     ...:

 In [58]: func(v1)
 Herb  1950-05-05

 In [59]: print(v1)
 SELECT "t1"."id", "t1"."name", "t1"."birthday" FROM "person" AS "t1" WHERE ("t1"."birthday" BETWEEN '1940-01-01' AND '1960-01-01')

```

モデルクラスの `select()` を使うと、そのテーブル( `Person` )の行を取得できます。

```
 In [61]: # %load 01_step_16_list.py
     ...: v1 = Person.select()
     ...:
     ...: def func(data):
     ...:     for d in data:
     ...:         print(f'{d.name} {d.pets.count()} pets')
     ...:
     ...: # func(v1)
     ...: # print(v1)
     ...:

 In [62]: func(v1)
 Bob 2 pets
 Grandma L. 0 pets
 Herb 1 pets

 In [63]: print(v1)
 SELECT "t1"."id", "t1"."name", "t1"."birthday" FROM "person" AS "t1"

```

この例では、またしても、典型的な**N+1問題**となるクエリを実行しています。この場合、最初のSELECTで返されたPersonごとに追加のクエリを実行していることになります。
これを避けるためには、JOINを実行し、SQL関数を使って結果を集約する必要があります。


```
 In [65]: # %load 01_step_17_aggregate.py
     ...: v1 = (Person
     ...:          .select(Person, fn.COUNT(Pet.id).alias('pet_count'))
     ...:          .join(Pet, JOIN.LEFT_OUTER)
     ...:          .group_by(Person)
     ...:          .order_by(Person.name))
     ...:
     ...: def func(data):
     ...:     for d in data:
     ...:         print(f'{d.name} {d.pet_count} pets')
     ...:
     ...: # func(v1)
     ...: # print(v1)
     ...:

 In [66]: func(v1)
 Bob 2 pets
 Grandma L. 0 pets
 Herb 1 pets

 In [67]: print(v1)
 SELECT "t1"."id", "t1"."name", "t1"."birthday", COUNT("t2"."id") AS "pet_count" FROM "person" AS "t1" LEFT OUTER JOIN "pet" AS "t2" ON ("t2"."owner_id" = "t1"."id") GROUP BY "t1"."id", "t1"."name", "t1"."birthday" ORDER BY "t1"."name"

```

すべての人と、その人が飼っているペットの名前を取得してみましょう。ここで、気をつけないとは、これは簡単に**N+1問題** が発生するような状況になるということです。

次の例が、先ほどのペットとその飼い主の名前を取得する例とどう違うかを考えてみましょう。ペットの飼い主は1人しかいないので、PetからPersonへの結合を実行すると、必ず1つのマッチが発生します。しかし、PersonからPetに結合する場合は、状況が異なります。なぜなら、ある人はペットを飼っていない場合もあれば、複数のペットを飼っている場合もあるからです。
リレーショナルデータベースを使用しているので、PersonからPetへの結合を行うと、複数のペットを持つすべての人が、各ペットに対して1回ずつ繰り返されます。


```
 In [69]: # %load 01_step_18_left_join.py
     ...: v1 = (Person
     ...:          .select(Person, Pet)
     ...:          .join(Pet, JOIN.LEFT_OUTER)
     ...:          .order_by(Person.name, Pet.name))
     ...:
     ...: def func(data):
     ...:     for d in data:
     ...:         if hasattr(d, 'pet'):
     ...:             print(f'{d.name} {d.pet.name}')
     ...:         else:
     ...:             print(f'{d.name} no pets')
     ...:
     ...: # func(v1)
     ...: # print(v1)
     ...:

 In [70]: func(v1)
 Bob Fido
 Bob Kitty
 Grandma L. no pets
 Herb Mittens Jr

 In [71]: print(v1)
 SELECT "t1"."id", "t1"."name", "t1"."birthday", "t2"."id", "t2"."owner_id", "t2"."name", "t2"."animal_type" FROM "person" AS "t1" LEFT OUTER JOIN "pet" AS "t2" ON ("t2"."owner_id" = "t1"."id") ORDER BY "t1"."name", "t2"."name"

```

通常、このような重複は望ましいものではありません。人をリストアップして、その人のペットのリストを添付するという、より一般的な（そして直感的な）要求に対応するために、 `prefetch()` メソッドを使うことができます。


```
 In [73]: # %load 01_step_19_prefetch.py
     ...: v1 = Person.select().order_by(Person.name).prefetch(Pet)
     ...:
     ...: def func(data):
     ...:     for d in data:
     ...:         print('{data.name}')
     ...:         for pet in d.pets:
     ...:             print(f'  * {d.name}')
     ...:
     ...: # func(v1)
     ...: # print(v1)
     ...:

 In [74]: func(v1)
 {data.name}
   * Bob
   * Bob
 {data.name}
 {data.name}
   * Herb

 In [75]: print(v1)
 [<Person: 1>, <Person: 2>, <Person: 3>]

```


### SQL関数
これは、SQL関数を使って、名前が大文字または小文字のGで始まるすべての人を取得するものです。


```
 In [77]: # %load 01_step_20_sql_func.py
     ...: expression = fn.Lower(fn.Substr(Person.name, 1, 1)) == 'g'
     ...: v1 = Person.select().where(expression)
     ...:
     ...: def func(data):
     ...:     for d in data:
     ...:         print(f'{d.name}')
     ...:
     ...: # func(v1)
     ...: # print(v1)
     ...: # print(expression)
     ...:

 In [78]: func(v1)
 Grandma L.

 In [79]: print(v1)
 SELECT "t1"."id", "t1"."name", "t1"."birthday" FROM "person" AS "t1" WHERE (Lower(Substr("t1"."name", 1, 1)) = 'g')

 In [80]: print(expression)
 <peewee.Expression object at 0x10d054460>

```


### データベースとの接続をクローズ

データベースとの接続をクローズするためには、 `close()` を呼び出します。
正常にクローズできれば  `True` が返されます。クローズしている状態で再度呼び出すと `False` が返されます。


```
 In [82]: # %load 01_step_21_close.py
     ...: v1 = db.close()
     ...: v2 = db.close()
     ...:
     ...: # print(v1)
     ...: # print(v2)
     ...:

 In [83]: print(v1)
 True

 In [84]: print(v2)
 False

```

これまでに例示したコードは基本的なもので、（必要はあるかどうかは別にして）より複雑なクエリはいくらでも記述することができます。
もう少し詳しく説明してゆきましょう。

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


## モデルとフィールド

### オブジェクトに対応するデータ
Peewee でのモデルクラス、フィールド、モデルインスタンスはすべて、データベースの概念に対応しています。

 PeeWee のオブジェクトマッピング

| オブジェクト | 対応するデータ |
|:--|:--|
| モデルクラス | データベースのテーブル |
| フィールドインスタンス | カラム、テーブル |
| モデルインスタンス | データベースのテーブルが保持する行 |

### モデル
次のコードは、データベース接続とモデルクラスを定義する典型的な方法です。

 my_app.py
```
 from peewee import *
 import datetime

 db = SqliteDatabase('my_app.db')

 class BaseModel(Model):
     class Meta:
         database = db

 class User(BaseModel):
     username = CharField(unique=True)

 class Tweet(BaseModel):
     user = ForeignKeyField(User, backref='tweets')
     message = TextField()
     created_date = DateTimeField(default=datetime.datetime.now)
     is_published = BooleanField(default=True)

```

このコードについて説明してゆきましょう。
まず、データベースと接続するために  `SqlDatabase()` を呼び出しています。

```
 db = SqlDatabase('my_app.db')
```

 `SqlDatabase()` に引数でデータベースのファイル名を与えています。ファイル名の代わりに  `':memory:'` を与えるとメモリ上にデータベースを作成します。

dbオブジェクトは、Sqliteデータベースへの接続を管理するために使用されます。

次にベースモデルクラスを作成しています。


```
 class BaseModel(Model):
     class Meta:
         database = db
```

データベースへの接続を確立するベースモデルクラスを定義しておくと、他のモデルクラスの定義では、このベースモデルクラスを継承するだけです。データベースを指定する必要がなく、重複したコードがなく簡潔になります。

モデルの設定は、Meta という特別なクラスで名前空間を維持します。メタクラスの設定はサブクラスに引き継がれるため、このプロジェクトのモデルはすべて BaseModel のサブクラスになります。Model.Metaを使って設定できる属性には様々なものがあります。

モデルクラスを作成しています。

```
 class User(BaseModel):
     username = CharField(unique=True)
```

モデルの定義には、SQLAlchemy や Django などの一般的な ORM に見られる宣言型のスタイルを採用しています。User モデルがデータベース接続を継承するように BaseModel クラスを継承していることに注目してください。

Userモデルはデータベース接続を継承します。プライマリキーを指定していないので、peeweeは自動的にidという自動インクリメントの整数のプラマリキーフィールドを追加します。


### フィールド
フィールドクラスは、モデルの属性とデータベースのカラムとをマッピングを記述するために使用されます。各フィールドタイプは対応するSQLストレージクラス(例： `varchar` ,  `int` )を持ち、pythonのデータタイプとベースになるストレージの間の変換は透過的に処理されます。

モデルクラスを作成する際、フィールドはクラス属性として定義されます。


```
 class User(Model):
     username = CharField()
     join_date = DateTimeField()
     about_me = TextField()

```

この例では、どのフィールドも  `primary_key=True` で与えられていません。Peewee は  `id` とう名前のフィールドを作成して、自動インクリメントのプライマリキーとして定義します。Peeweeでは、オートインクリメントの整数型のプライマリキーを意味するために `AutoField` を使用しており、これは  `primary_key=True` を意味します。

フィールドには、 `ForeignKeyField` という特殊なタイプがあり、モデル間の外部キーの関係(リレーション)を直感的に表現することができます。


```
 class Message(Model):
     user = ForeignKeyField(User, backref='messages')
     body = TextField()
     send_date = DateTimeField(default=datetime.datetime.now)
```

このモデルのフィールドにはアトリビュートへアクセスするように記述することができます。

```
 >>> print(some_message.user.username)
 Some User

 >>> for message in some_user.messages:
 ...     print(message.body)
 some message
 another message
 yet another message
```

### フィールドのデフォルト値
Peeweeでは、モデルクラスの定義時に、フィールドのデフォルト値を設定することができます。例えば、IntegerFieldのデフォルト値をNULLではなく0にするには、デフォルト値を指定してフィールドを宣言します。


```
 class Message(Model):
     context = TextField()
     read_count = IntegerField(default=0)

```

場合によっては、デフォルトの値を動的なものにした方がよいこともあります。一般的な例では、現在の日付と時刻を使用するようなフィールドの場合です。Peeweeでは、このような場合に関数を指定することができ、その戻り値は、オブジェクトが作成されたときに使用されます。ここでは、関数を指定するだけで、実際に呼び出すわけではないことに注意してください。


```
 class Message(Model):
     context = TextField()
     timestamp = DateTimeField(default=datetime.datetime.now)

```

リストや辞書など可変型のフィールドを使用していて、デフォルト値を提供したい場合は、デフォルト値をシンプルな関数でラップして、複数のモデルインスタンスが同じ基本オブジェクトへの参照を共有しないようにするのが良いでしょう。


```
 def house_defaults():
     return {'beds': 0, 'baths': 0}

 class House(Model):
     number = TextField()
     street = TextField()
     attributes = JSONField(default=house_defaults)
```

データベースは、フィールドのデフォルト値を提供することもできます。Peeweeは、サーバ側のデフォルト値を設定するためのAPIを明示的に提供していませんが、 `constraints` 引数を使ってサーバ側のデフォルト値を指定することができます。


```
 class Message(Model):
     context = TextField()
     timestamp = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

```

モデルクラスの定義にデフォルト・パラメータを使った場合、その値は実際のテーブルや列の定義の一部ではなく、Peeweeによって設定されることに注意してください。

### フィールドタイプ
Peewee のフィールドタイプはバックエンドのデータベースでのカラムタイプにマッピングされます。
 peewee のフィールドタイプ

| Field Type | SQLite | PostgreSQL | MySQL |
|:--|:--|:--|:--|
| AutoField | integer | serial | integer |
| BigAutoField | integer | bigserial | bigint |
| IntegerField | integer | integer | integer |
| BigIntegerField | integer | bigint | bigint |
| SmallIntegerField | integer | smallint | smallint |
| IdentityField | not supported | int identity | not supported |
| FloatField | real | real | real |
| DoubleField | real | double precision | double precision |
| DecimalField | decimal | numeric | numeric |
| CharField | varchar | varchar | varchar |
| FixedCharField | char | char | char |
| TextField | text | text | text |
| BlobField | blob | bytea | blob |
| BitField | integer | bigint | bigint |
| BigBitField | blob | bytea | blob |
| UUIDField | text | uuid | varchar(40) |
| BinaryUUIDField | blob | bytea | varbinary(16) |
| DateTimeField | datetime | timestamp | datetime |
| DateField | date | date | date |
| TimeField | time | time | time |
| TimestampField | integer | integer | integer |
| IPField | integer | bigint | bigint |
| BooleanField | integer | boolean | bool |
| BareField | untyped | not supported | not supported |
| ForeignKeyField | integer | integer | integer |

ここでは、IntegerField のような一般的なフィールドタイプを説明のではなくて、より重要なフィールドタイプについて説明してゆきます。

### ForeignKeyField
ForeignKeyField は、あるモデルが別のモデルを参照できるようにする特別なフィールドタイプです。通常、外部キーには、関連するモデルのプライマリキーが含まれます（フィールドを指定することで、特定のカラムを指定することもできます）。

外部キーにより、データを正規化することができます。ここで説明しているモデルの例では、 `Tweet` モデルから `User` モデルへの外部キーがあります。これは、すべてのユーザーがツイートと同じようにテーブルに格納されており、ツイートからユーザーへの外部キーによって、各ツイートが特定のユーザーオブジェクトを指すようになっているわけです。


```
 tweets = (Tweet
           .select(Tweet, User)
           .join(User)
           .order_by(Tweet.created_date.desc()))

 for tweet in tweets:
     print(tweet.user.username, tweet.message)
```

この例では、N+1問題を回避するためにクエリの一部としてUserデータが選択されています。
しかし、ユーザーを選択しなかった場合は、関連するユーザーデータを取得するために追加のクエリが発行されます。


```
 tweets = Tweet.select().order_by(Tweet.created_date.desc())
 for tweet in tweets:
     # 各ツイートに対して、関連するユーザーデータを取得するための追加クエリが発行される
     print(tweet.user.username, tweet.message)
```

また、外部キーのカラムから、関連するプライマリキーの値だけが必要になることがあります。この場合、Peewee は 外部キーのフィールド名に  `"_id"` を追加することで、生の外部キーの値にアクセスできるようにしています。


```
 tweets = Tweet.select()
 for tweet in tweets:
     print(tweet.user_id, tweet.message)

```


ForeignKeyFieldでは、誤って外部キーを解決してしまい、追加のクエリが発生するのを防ぐために、初期化パラメタとして `lazy_load` をサポートしています。これを無効にすると、 `"_id "` 属性のように動作します。


```
 class Tweet(Model):
     user = ForeignKeyField(User, backref='tweets', lazy_load=False)

 for tweet in Tweet.select():
     print(tweet.user, tweet.message)

 # lazy-load を無効にすると、tweet.userにアクセスしても余計なクエリは実行されず、代わりにユーザーIDの値が返される
 # 1  tweet from user1
 # 1  another from user1
 # 2  tweet from user2

 # 関連するuserオブジェクトをロードすれば、user外部キーは通常通りに動作する
 for tweet in Tweet.select(Tweet, User).join(User):
     print(tweet.user.username, tweet.message)

 # user1  tweet from user1
 # user1  another from user1
 # user2  tweet from user1
```
]
### ForeignKeyFieldの後方参照
ForeignKeyFieldでは、後方参照プロパティをターゲットモデルにバインドすることができます。暗黙のうちに、このプロパティは `classname_set` という名前になり、 `classname` はモデルクラスの小文字の名前ですが、 `backref` 引数を使ってオーバーライドすることができます。


```
 class Message(Model):
     from_user = ForeignKeyField(User, backref='outbox')
     to_user = ForeignKeyField(User, backref='inbox')
     text = TextField()

 for message in some_user.outbox:
     # from_userがsome_userであるすべてのメッセージ
     print(message)

 for message in some_user.inbox:
     # to_userがsome_userであるすべてのメッセージ
     print(message)
```

### DateTimeField、DateField、TimeField
日付と時刻を扱うこれら3つのフィールドは、年、月、時間などにアクセスできる特別なプロパティを持っています。

#### DateField
- year
- month
- day

#### TimeField
- hour
- minute
- second

#### DateTimeField


```
 now = datetime.datetime.now()

 # 現在の月にイベントがある日を取得
 Event.select(Event.event_date.day.alias('day')).where(
     (Event.event_date.year == now.year) &
     (Event.event_date.month == now.month))
```

SQLite には日付型を持っていないので、日付はフォーマットされたテキストカラムに格納されます。比較が正しく機能するためには、日付は辞書的にソートされるようにフォーマットされている必要があります。
これが、デフォルトで `YYYY-MM-DD HH:MM:SS` のフォーマットで格納されている理由です。

### BitField、BigBitField
BitField は IntegerField のサブクラスで、機能のトグルを整数のビットマスクとして格納するのに適しています。
BigBitFieldは、大きなデータセットのビットマップを格納するのに適しています。例えば、メンバーシップやビットマップタイプのデータを表現する場合などです。

BitField の使用例として、Post モデルがあり、投稿方法に関する特定の True/False フラグを保存したいとします。これらの機能のトグルをすべて独自の BooleanField オブジェクトに格納することもできますが、代わりに BitField を使用することもできます。


```
 class Post(Model):
     content = TextField()
     flags = BitField()

     is_favorite = flags.flag(1)
     is_sticky = flags.flag(2)
     is_minimized = flags.flag(4)
     is_deleted = flags.flag(8)
```


```
 >> p = Post()
 >>> p.is_sticky = True
 >>> p.is_minimized = True
 >>> print(p.flags)  # Prints 4 | 2 --> "6"
 6
 >>> p.is_favorite
 False
 >>> p.is_sticky
 True
```


```
 # WHERE (post.flags & 1 != 0) のようなWHERE句を生成する
 favorites = Post.select().where(Post.is_favorite)

 # 記事につけられたフラグで抽出
 sticky_faves = Post.select().where(Post.is_sticky & Post.is_favorite)
```

BitField は整数で保存されるため、表現できるフラグの数は最大 64 個です (64 ビットは整数カラムの一般的なサイズです)。
任意のサイズのビットマップを保存する場合は、代わりに BigBitField を使用することができます。これは、BlobField に保存された、自動的に管理されるバイトのバッファを使用します。

BitField の 1 つまたは複数のビットを一括更新する際には、ビット演算子を使用して 1 つまたは複数のビットを設定またはクリアすることができます。


```
 # すべてのPostオブジェクトに第4ビットを設定
 Post.update(flags=Post.flags | 8).execute()

 # すべてのPostオブジェクトの第1ビットと第3ビットをクリア
 Post.update(flags=Post.flags & ~(1 | 4)).execute()
```

簡単な操作のために、フラグには個々のビットを設定またはクリアするための便利な `set()` および `clear()` メソッドが用意されています。


```
 # すべての投稿に is_deleted ビットを設定
 Post.update(flags=Post.is_deleted.set()).execute()

 # すべての投稿に is_deleted ビットをクリア
 Post.update(flags=Post.is_deleted.clear()).execute()

```


### BareField
BareField クラスは、SQLite での使用のみを目的としています。SQLite は動的型付けを使用しており、データ型は強制されないため、データ型を持たないフィールドを宣言してもエラーにならない場合があります。そのような場合は BareField を使うことができます。また、SQLite の仮想テーブルではメタカラムや型付けされていないカラムを使用するのが一般的なので、そのような場合にも型付けされていないフィールドを使用することができます。
ただし、フルテキスト検索には代わりに SearchField を使用するべきです。

BareField には特別なパラメータ adapt があります。このパラメータは、データベースから送られてくる値を受け取って、それを適切なPythonの型に変換する関数です。例えば、型付けされていないカラムを持つ仮想テーブルがあり、そのカラムが int オブジェクトを返すことがわかっている場合、 `adapt=int` と指定することができます。


```
 db = SqliteDatabase(':memory:')

 class Junk(Model):
     anything = BareField()

     class Meta:
         database = db

 # 複数のデータタイプをJunk.anything列に格納
 Junk.create(anything='a string')
 Junk.create(anything=12345)
 Junk.create(anything=3.14159)

```


### カスタム・フィールドの作成
peeweeでは、カスタム・フィールド・タイプのサポートを簡単に追加できます。この例では、（ネイティブのUUIDカラムタイプを持つ）postgresql用のUUIDフィールドを作成します。

カスタムフィールドタイプを追加するには、まず、フィールドデータが格納されるカラムのタイプを特定する必要があります。
例えば、10進数のフィールドにPythonの動作を追加したいだけなら、DecimalFieldをサブクラス化するだけです。それに対して、データベースがカスタムのカラムタイプを提供している場合は、peeweeにそれを知らせる必要があります。
これは、Field.field_type属性によって制御されます。

PeeweeにはUUIDFieldが搭載されています。次のコードはあくまでも例示のためのものです。


```
 class UUIDField(Field):
     field_type = 'uuid'

```

UUIDをネイティブのUUIDカラムに格納します。psycopg2はデフォルトではデータを文字列として扱うので、フィールドに2つのメソッドを追加して処理することにします。

- アプリケーションで使用されるデータベースからのデータ
- データベースに入るPythonアプリからのデータ


```
 import uuid

 class UUIDField(Field):
     field_type = 'uuid'

     def db_value(self, value):
         return value.hex  # convert UUID to hex string.

     def python_value(self, value):
         return uuid.UUID(value) # convert hex string to UUID

```

### フィールド名の競合
モデルクラスは、 `Model.save()` や `Model.create()` などの多くのクラスメソッドやインスタンスメソッドを実装しています。モデルメソッドと名前が同じフィールドを宣言すると、問題が発生する可能性があります。


```
 class LogEntry(Model):
     event = TextField()
     create = TimestampField()  # ダメ！
     update = TimestampField()  # ダメ！

```

この問題を回避しつつ、データベーススキーマで目的のカラム名を使用するには、 `column_name` 引数で、フィールド属性に別の名前を明示的に指定します。


```
 class LogEntry(Model):
     event = TextField()
     create_ = TimestampField(column_name='create')
     update_ = TimestampField(column_name='update')

```

### モデルテーブルの作成
モデルを使い始めるためには、まずデータベースへの接続を開き、テーブルを作成する必要があります。Peeweeは、必要なCREATE TABLEクエリを実行し、さらに制約やインデックスを作成します。


```
 # データベースに接続
 db.connect()

 # テーブルを作成
 db.create_tables([User, Tweet])

```


## クエリ
ここでは、リレーショナル・データベースでよく行われる基本的なCRUD操作について説明します。
CRUD操作とは、生成(Create)、読み込み(Read)、更新(Update) 、削除(Delete) からなる、永続的なデータを取り扱うソフトウェアに要求される4つの基本機能を言います。

-  `Model.create()` ： INSERTクエリの実行.
-  `Model.save()` / `Model.update()` ：UPDATEクエリの実行
-  `Model.delete_instance()` /  `Model.delete()` ：DELETEクエリの実行
-  `Model.select()` ： SELECTクエリの実行

### 新しいレコードの作成
 `Model.create()` を使って新しいモデル・インスタンスを作成することができます。このメソッドはキーワード引数を受け入れ、キーはモデルのフィールド名に対応します。新しいインスタンスが返され、テーブルに行が追加されます。

python
```
 User.create(username='Charlie')

```

これにより、データベースにSQLコマンドINSERTが発行されて、新しい行が追加されます。プライマリキーは自動的に取得されて、モデル・インスタンスに保存されます。

また、プログラムでモデル・インスタンスを構築してから `save()` メソッドを呼び出すこともできます。


```
 >>> user = User(username='Charlie')
 >>> user.save()  # save() returns the number of rows modified.
 1
 >>> user.id
 1
 >>> huey = User()
 >>> huey.username = 'Huey'
 >>> huey.save()
 1
 >>> huey.id
 2

```

モデルに外部キーがある場合、新規レコード作成時に外部キーフィールドにモデルインスタンスを直接割り当てることができます。


```
 >>> tweet = Tweet.create(user=huey, message='Hello!')

```

また、関連オブジェクトのプライマリキーの値を使用することもできます。


```
 >>> tweet = Tweet.create(user=2, message='Hello again!')

```

単にデータを挿入したいだけで、モデルのインスタンスを作成する必要がない場合は、 `Model.insert()` を使用することができます。挿入クエリを実行すると、新しい行の主キーが返されます。


```
 >>> User.insert(username='Mickey').execute()
 3

```

### BulkInsert 一括挿入
大量のデータを素早追加するためには、いくつかの方法があります。単純な方法は、 `Model.create()` をループで呼び出すことです。


```
 data_source = [
     {'field1': 'val1-1', 'field2': 'val1-2'},
     {'field1': 'val2-1', 'field2': 'val2-2'},
     # ...
 ]

 for data_dict in data_source:
     MyModel.create(**data_dict)

```

この方法では、次のような理由で処理に時間がかかります。

1. ループをトランザクションでラップしていない場合、create()の各呼び出しはそれぞれのトランザクションで行われます。
これは本当に遅くなります。
2. かなりの量のPythonロジックが邪魔をしますし、それぞれの InsertQuery が生成され、SQLに解析されなければなりません。
3  このコードは（SQLの生のバイト数としての）大量のデータをデータベースに送って解析していることになります。
4. 最後の挿入IDを取得しているので、場合によっては追加のクエリが実行されることになります。

これを単純に `atomic()` を使ったトランザクションでラップすることで、大幅なスピードアップを図ることができます。


```
 with db.atomic():
     for data_dict in data_source:
         MyModel.create(**data_dict)

```

このコードでは、前述の処理時間が遅くなる理由(2、3、4)から問題があります。 `insert_many()` を使えば、さらに大きな効果が得られます。このメソッドは、タプルや辞書のリストを受け取り、一回のクエリで複数の行を挿入します。


```
 data_source = [
     {'field1': 'val1-1', 'field2': 'val1-2'},
     {'field1': 'val2-1', 'field2': 'val2-2'},
     # ...
 ]

 # 複数の行をINSERTする最速の方法
 MyModel.insert_many(data_source).execute()

```


 `insert_many()` メソッドは、対応するフィールドを指定することで、行タプルのリストも受け取ることができます。


```
 # タプルをINSERTすることもできるけれど...。
 data = [('val1-1', 'val1-2'),
         ('val2-1', 'val2-2'),
         ('val3-1', 'val3-2')]

 # しかし、その値がどのフィールドに対応しているかを示す必要がある
 MyModel.insert_many(data, fields=[MyModel.field1, MyModel.field2]).execute()

```

また、一括挿入をトランザクションで処理するのも良い方法です。


```
 with db.atomic():
     MyModel.insert_many(data, fields=fields).execute()

```

バックエンドのデータベースシステムがSQLite の場合では、BulkInsertを使用する際にいくつかの注意点があります。具体的には、BulkInsert APIを利用するには、SQLite3のバージョンが3.7.11.0以降である必要があります。また、SQLite のSQLクエリ内のバインド変数の数には、バージョンによって上限に差異があります。

### 一括して行を挿入
データソースの行数によっては、行を分割する必要があります。特にSQLiteでは、1つのクエリあたりの変数数が999または32766に制限されています（バッチサイズは１行あたり999の長さ、または１行あたり32766の長さとなります）。

次のようにループを書いてデータを塊にまとめることができます。（トランザクションを使用することを強くお勧めします）


```
 with db.atomic():
     for idx in range(0, len(data_source), 100):
         MyModel.insert_many(data_source[idx:idx+100]).execute()

```

Peeweeには `chunked()` というヘルパー関数が用意されており、これを使うことで、一般的なイテレートテーブルを一連のバッチサイズのイテレートテーブルに効率的に分割して処理することができます。

 pytohn
```
 from peewee import chunked

 with db.atomic():
     for batch in chunked(data_source, 100):
         MyModel.insert_many(batch).execute()
```

代替案
 `Model.bulk_create()` メソッドは、 `Model.insert_many()` とよく似た動作をします。違いは、 `Model.bulk_create()` が挿入する未保存のモデル・インスタンスのリストを受け取り、オプションで  `batch_size` 引数を受け取ることです。


```
 with open('user_list.txt') as fh:
     # Create a list of unsaved User instances.
     users = [User(username=line.strip()) for line in fh.readlines()]

 # 操作をトランザクションで処理し、ユーザーを一度に100人ずつバッチでINSERTする
 with db.atomic():
     User.bulk_create(users, batch_size=100)

```

バックエンドのデータベースシステムに、RETURNING句をサポートしているPostgreSQLを使用している場合、以前に保存されていなかったモデルインスタンスには、新しいプライマリキーの値が自動的に入力されます。

さらに、Peeweeには、モデルのリストの1つまたは複数のカラムを効率的に更新できる  `Model.bulk_update()` があります。

 pyton
```
 u1, u2, u3 = [User.create(username='u%s' % i) for i in (1, 2, 3)]

 u1.username = 'u1-x'
 u2.username = 'u2-y'
 u3.username = 'u3-z'

 User.bulk_update([u1, u2, u3], fields=[User.username])

```

また、 `Database.batch_commit()` メソッドを使用して、バッチサイズのトランザクション内で行のチャンクを処理することもできます。この方法は、PostgreSQL 以外のデータベースで、新しく作成された行のプライマリキーを取得しなければならない場合の回避策になります。


```
 row_data = [{'username': 'u1'}, {'username': 'u2'}, ...]

 # row_data に789個のアイテムがあるとき、以下のコードは合計8つのトランザクションが発生する（7x100行＋1x89行）
 for row in db.batch_commit(row_data, 100):
     User.create(**row)

```


### 別のテーブルからの一括読み込み
一括読み込みしたいデータが別のテーブルに格納されているとき、 `Model.insert_from()` メソッドを使用して、SELECT クエリを元とする INSERT クエリを作成することもできます。


```
 res = (TweetArchive
        .insert_from(
            Tweet.select(Tweet.user, Tweet.message),
            fields=[TweetArchive.user, TweetArchive.message])
        .execute())

```

このクエリは以下のSQLと同等です。

SQL
```
 INSERT INTO "tweet_archive" ("user_id", "message")
 SELECT "user_id", "message" FROM "tweet";

```


### 既存のレコードの更新
モデルのインスタンスにプライマリキーが設定されると、その後の  `save()` の呼び出しでは INSERT ではなく UPDATE が行われます。モデルのプライマリキーは変更されません。


```
 >>> user.save()  # save() returns the number of rows modified.
 1
 >>> user.id
 1
 >>> user.save()
 >>> user.id
 1
 >>> huey.save()
 1
 >>> huey.id
 2

```

複数のレコードを更新したい場合は、UPDATEクエリを発行します。次の例では、すべてのTweetオブジェクトを更新し、今日以前に作成されたものは公開されたものとしてマークします。 `Model.update(` )は、モデルのフィールド名に対応するキーを持つキーワード引数を受け付けます。


```
 >>> today = datetime.today()
 >>> query = Tweet.update(is_published=True).where(Tweet.creation_date < today)
 >>> query.execute()  # Returns the number of rows that were updated.
 4

```

### アトミック・アップデート
Peeweeでは、微小(atomic)な更新を行うことができます。例えば、いくつかのカウンタを更新する必要があるとしましょう。単純に考えれば、次のように書くことになるでしょう。


```
 >>> for stat in Stat.select().where(Stat.url == request.url):
 ...     stat.counter += 1
 ...     stat.save()

```

実は、これは良くない例です。遅いだけでなく，複数のプロセスが同時にカウンタを更新している場合，競合状態に陥りやすくなります。
このコードを， `update()` を使ってアトミックにカウンタを更新することができます。


```
 >>> query = Stat.update(counter=Stat.counter + 1).where(Stat.url == request.url)
 >>> query.execute()
```

これらの  `update()` は、いくらでも複雑にすることができます。
例えば全社員に、前回のボーナスに給与の10％を加えた額のボーナスを支給することにしましょう。


```
 >>> query = Employee.update(bonus=(Employee.bonus + (Employee.salary * .1)))
 >>> query.execute()

```

サブクエリを使用して列の値を更新することもできます。例えば、Userモデルに正規化されたカラムがあり、そのカラムにはユーザのツイート数が格納されていて、この値を定期的に更新していたとします。


```
 >>> subquery = Tweet.select(fn.COUNT(Tweet.id)).where(Tweet.user == User.id)
 >>> update = User.update(num_tweets=subquery)
 >>> update.execute()

```

### Upsert
Peeweeでは、様々な種類のアップサート機能をサポートしています。3.24.0以前のSQLiteと、MySQLがバックエンドの場合、Peeweeは  `replace()` を提供していて、レコードを更新したり、そのレコードが存在しない場合は挿入することができます。

> 補足説明：
>  `on_confilict_replace()` が理解しずらいかもしれませんが、
> INSERTしようとしたときに制約違反があるときは更新することになります。
> 要点は replace() を行うことに視点があるわけで、そのレコードがないときはINSERTが発行されることになります。
>
>  `on_conflist_repllace()` に加えて、SQLite、MySQL、PostgreSQL では、単に挿入して
> 、潜在的な制約違反を無視したい場合には、無視をするアクション  `on_conflict_ignore()` を提供しています。
>
>


```
 class User(Model):
     username = TextField(unique=True)
     last_login = DateTimeField(null=True)

 # ユーザーの挿入または更新を行う
 # last_login の値は、そのユーザーが以前から存在していたかどうかにかかわらず更新されます。
 user_id = (User
            .replace(username='the-user', last_login=datetime.now())
            .execute())

 # このクエリは上記の
 user_id = (User
            .insert(username='the-user', last_login=datetime.now())
            .on_conflict_replace()
            .execute())
```

### レコードの削除
 `delete_instance()` メソッドは、指定されたモデル・インスタンスを削除します。引数  `recursive=True` が与えられていると、依存するオブジェクトを再帰的に削除することができます。


```
 >> user = User.get(User.id == 1)
 >>> user.delete_instance()  # Returns the number of rows deleted.
 1

 >>> User.get(User.id == 1)

```


任意の行のセットを削除するには、DELETEクエリを発行します。
次の例では、1年以上前のTweetオブジェクトをすべて削除します。


```
 >> query = Tweet.delete().where(Tweet.creation_date < one_year_ago)
 >>> query.execute()  # Returns the number of rows deleted.
 7

```

### ひとつのレコードを選択
 `Model.get()` メソッドを使って、与えられたクエリにマッチする単一のインスタンスを取得することができます。プライマリキーによる検索では、 `Model.get_by_id()` というショートカット・メソッドを使用することもできます。

このメソッドは、与えられたクエリで  `Model.select()` を呼び出すショートカットですが、結果は一行に制限されます。さらに、指定されたクエリにマッチするモデルがない場合は、 `DoesNotExist` 例外が発生します。


```
 >>> User.get(User.id == 1)
 <__main__.User object at 0x25294d0>

 >>> User.get_by_id(1)  # Same as above.
 <__main__.User object at 0x252df10>

 >>> User[1]  # Also same as above.
 <__main__.User object at 0x252dd10>

 >>> User.get(User.id == 1).username
 u'Charlie'

 >>> User.get(User.username == 'Charlie')
 <__main__.User object at 0x2529410>

 >>> User.get(User.username == 'nobody')
 UserDoesNotExist: instance matching query does not exist:
 SQL: SELECT t1."id", t1."username" FROM "user" AS t1 WHERE t1."username" = ?
 PARAMS: ['nobody']

```


より高度な操作を行うには、 `SelectBase.get()` を使用します。
次のクエリは、charlie というユーザーの最新のツイートを取得します。

 pyton
```
 >>> (Tweet
 ...  .select()
 ...  .join(User)
 ...  .where(User.username == 'charlie')
 ...  .order_by(Tweet.created_date.desc())
 ...  .get())
 <__main__.Tweet object at 0x2623410>

```

他に次のようなメソッドが提供されています。

- Model.get()
- Model.get_by_id()
- Model.get_or_none() 　　 一致する行が見つからない場合は、Noneを返します。
- Model.select()
- SelectBase.get()
- SelectBase.first() 　　結果セットの最初のレコード、またはNoneを返します。

### 作成または取得
Peeweeには、get、create　の操作を行うためのヘルパー・メソッドが1つあります。 `Model.get_or_create()` は、まず一致する行を取得しようとします。これに失敗すると、新しい行が作成します。

取得/作成型のロジックでは、通常、重複したオブジェクトの作成を防ぐために、一意性制約やプライマリキーに依存します。
例えば、Userモデルを使って新しいユーザーアカウントの登録を実装したいとするとき、Userモデルはusernameフィールドに一意の制約を持っているので、データベースの整合性保証に頼って、ユーザー名が重複しないようにします。


```
 try:
     with db.atomic():
         return User.create(username=username)
 except peewee.IntegrityError:
     # username`はユニークなカラムなので、このユーザー名はすでに存在しており、.get()を呼び出しても問題はない
     return User.get(User.username == username)

```

この種のロジックは、独自のモデルクラスのクラスメソッドとして簡単にカプセル化できます。

上記の例では、最初に作成を試み、その後、データベースに依存して一意性制約を強化するために検索にフォールバックしています。もし、最初にレコードの取得を試みたい場合は、  `get_or_create()` を使用することができます。このメソッドは Django の同名の関数と同じように実装されています。Django スタイルのキーワード引数フィルタを使って、WHERE 条件を指定することができます。この関数は、インスタンスと、そのオブジェクトが作成されたかどうかを示す boolean 値を含む 2 タプルを返します。

ここでは  `get_or_create()` を使ってユーザアカウント作成するような場合は、次のコードとなります。


```
 user, created = User.get_or_create(username=username)

```

例えば、Personという別のモデルがあり、Personオブジェクトを取得したり作成したりしたいとします。Person を取得する際に気にする条件は、姓と名だけですが、もし新しいレコードを作成する必要がある場合は、生年月日と好きな色も指定します。


```
 person, created = Person.get_or_create(
     first_name=first_name,
     last_name=last_name,
     defaults={'dob': dob, 'favorite_color': 'green'})

```

 `get_or_create()` メソッドに渡されたキーワード引数は、ロジックの `get()` 部分で使用されます。ただし、 `defaults` で与えた辞書は、新しく作成されたインスタンスに値を入力するために使用されます。


### 複数のレコードを選択

 `Model.select()` を使ってテーブルから行を取り出すことができます。SELECTクエリを作成すると、データベースは、クエリに対応するすべての行を返します。Peeweeでは、これらの行を繰り返し処理したり、インデックスやスライシング操作を使用することができます。


```
 >> query = User.select()
 >>> [user.username for user in query]
 ['Charlie', 'Huey', 'Peewee']

 >>> query[1]
 <__main__.User at 0x7f83e80f5550>

 >>> query[1].username
 'Huey'

 >>> query[:2]
 [<__main__.User at 0x7f83e80f53a8>, <__main__.User at 0x7f83e80f5550>]

```

Select クエリはスマートで、反復処理やインデックス作成、スライスなどを複数回行うことができますが、クエリは一度しか実行されないという特徴があります。

次の例では、単純に  `select()` メソッドを呼び出して、戻り値である Select インスタンスを反復処理します。これにより、User テーブルのすべての行が取得できます。


```
 >>> for user in User.select():
 ...     print(user.username)
 ...
 Charlie
 Huey
 Peewee

```

同じクエリを再度実行する場合では、初回の結果がキャッシュされているため、データベースにアクセスしません。この動作を無効にする（つまり、メモリ使用量を削減する）には、反復処理の際に  `Select.iterator()` を呼び出します。

外部キーを含むモデルを反復処理するときは、関連するモデルの値にアクセスする方法に注意してください。N+1クエリの動作を引き起こす可能性があります。

Tweet.userのような外部キーを作成すると、後方参照を使って後方参照(User.tweets)を作成することができます。後方参照はSelectインスタンスとして公開されます


```
 >>> tweet = Tweet.get()
 >>> tweet.user  # Accessing a foreign key returns the related model.
 <tw.User at 0x7f3ceb017f50>

 >>> user = User.get()
 >>> user.tweets  # Accessing a back-reference returns a query.
 <peewee.ModelSelect at 0x7f73db3bafd0>

```

user.tweetsの後方参照は、他のSelectと同様に反復することができます。


```
 >>> for tweet in user.tweets:
 ...     print(tweet.message)
 ...
 hello world
 this is fun
 look at this picture of my food

```

Select クエリは、モデル・インスタンスを返すだけでなく、タプル、名前付きタプル、辞書を返すことができます。
場合によっては、例えば行を辞書として扱う方が簡単だと思うかもしれません。


```
 >>> query = User.select().dicts()
 >>> for row in query:
 ...     print(row)

 {'id': 1, 'username': 'Charlie'}
 {'id': 2, 'username': 'Huey'}
 {'id': 3, 'username': 'Peewee'}

```


### 大きな結果セットの反復処理
デフォルトでは、PeeweeはSelectクエリの反復処理で返される行をキャッシュします。これは、追加のクエリを発生させずに、複数の反復処理やインデックス作成、スライスを可能にするための最適化です。しかし、このキャッシュは、大量の行を繰り返し処理する場合には問題となります。

クエリを反復処理する際にpeeweeが使用するメモリの量を減らすには、 `iterator()` メソッドを使用します。このメソッドを使うと、返された各モデルをキャッシュせずに反復処理を行うことができ、大きな結果セットを反復処理する際のメモリ使用量を大幅に削減することができます。


```
 # 1,000万個のstatオブジェクトをcsvファイルにダンプするとき...
 stats = Stat.select()

 # 架空のシリアライザークラス
 serializer = CSVSerializer()

 # すべての統計情報をループし、シリアル化する
 for stat in stats.iterator():
     serializer.serialize_object(stat)

```

単純なクエリの場合、行をディクショナリ、namedtuples、またはタプルとして返すことで、さらに速度が向上します。
以下のメソッドは、任意の Select クエリで結果の行の種類を変更するために使用することができます。

- dicts()
- namedtuples()
- tuples()

メモリの消費を抑えるために、iterator()メソッドの呼び出しを追加することも忘れないでください。
たとえば、上記のコードは次のようになります。


```
 #  1,000万個のstatオブジェクトをcsvファイルにダンプする
 stats = Stat.select()

 # 架空のシリアライザークラス
 serializer = CSVSerializer()

 # すべての統計情報（タプルとしてレンダリング、キャッシュなし）をループし、シリアル化する
 for stat_tuple in stats.tuples().iterator():
     serializer.serialize_tuple(stat_tuple)
```

複数のテーブルの列を含む大量の行を繰り返し処理する場合、peeweeは返された各行のモデル・グラフを再構築します。この操作は、複雑なグラフの場合には時間がかかります。例えば、ツイートのリストを、そのツイートの作者のユーザ名とアバターとともに選択する場合、Peeweeは各行に対して2つのオブジェクト（ツイートとユーザ）を作成する必要があります。上記の行タイプに加えて、4つ目のメソッド  `objects()` があります。このメソッドは、行をモデル・インスタンスとして返しますが、モデル・グラフの解決は行いません。


```
 query = (Tweet
          .select(Tweet, User)  # Select tweet and user data.
          .join(User))

 # ユーザーのカラムは、tweet.userでアクセスできる別のUserインスタンスに格納されていることに注意
 for tweet in query:
     print(tweet.user.username, tweet.content)

 # .objects()」を使用すると、tweet.userオブジェクトは作成されず、
 # すべてのユーザー属性がtweetインスタンスに割り当てられる
 for tweet in query.objects():
     print(tweet.username, tweet.content)
```

最大限のパフォーマンスを得るためには、クエリを実行し、その結果を基礎となるデータベースカーソルを使って反復処理することができます。 `Database.execute()` は、クエリオブジェクトを受け取り、クエリを実行し、DB-API 2.0 のCursor オブジェクトを返します。このカーソルは、生の行タプルを返します。


```
 query = Tweet.select(Tweet.content, User.username).join(User)
 cursor = database.execute(query)
 for (content, username) in cursor:
     print(username, '->', content)

```

### レコードのフィルタリング
PeeWee では、通常のpythonの演算子を使って、特定のレコードをフィルタリングすることができます。Peeweeは、様々なクエリ演算子をサポートしています。


```
 >>> user = User.get(User.username == 'Charlie')
 >>> for tweet in Tweet.select().where(Tweet.user == user, Tweet.is_published == True):
 ...     print(tweet.user.username, '->', tweet.message)
 ...
 Charlie -> hello world
 Charlie -> this is fun

 >>> for tweet in Tweet.select().where(Tweet.created_date < datetime.datetime(2011, 1, 1)):
 ...     print(tweet.message, tweet.created_date)
 ...
 Really old tweet 2010-01-01 00:00:00

```

複数テーブルを横断したフィルタもできます。


```
 >>> for tweet in Tweet.select().join(User).where(User.username == 'Charlie'):
 ...     print(tweet.message)
 hello world
 this is fun
 look at this picture of my food

```

複雑なクエリを表現したい場合は、pythonのビット演算子である、 `|` (OR) と  `&` (AND) を使用します。


```
 >>> Tweet.select().join(User).where(
 ...     (User.username == 'Charlie') |
 ...     (User.username == 'Peewee Herman'))
```

> Peeweeでは、論理演算子（ `and` と `or` ）ではなく、ビット演算子（ `&` と `|` ）を使用していることに注意してください。これは、Pythonが論理演算の戻り値をブール値に変換するためです。これは、"IN "のクエリが、 `in` 演算子ではなく  `.in_()` を使って表現されなければならない理由でもあります。


 クエリ演算子

| 演算子 | 説明 |
|:--|:--|
| == | x と y が等しい |
| < | x は y より小さい |
| <= | x は y 以下 |
| > | x は y より大きい |
| >= | x は y 以上 |
| != | x と y が等しくない |
| << | x が y に含まれる x IN y ( y がリストかクエリのとき) |
| >> | x と y が同じ x IS y ( y が None/NULLのときき) |
| % | x  の一部分にが y がマッチ x LIKE y ( y にワイルドカードを含めることができる） |
| ** | x  の一部分にが y がマッチ(大文字小文字不問)  x LIKE y  ( y にワイルドカードを含めることができる） |
| ^ | x と y の排他的論理和  x XOR y |
| ~ | 否定演算子　 (例 NOT x) |


 メソッド

| メソッド | 説明 |
|:--|:--|
| .in_(value) | value は含まれているか IN  (演算子 << と同じ ). |
| .not_in(value) | value が含まれていないか NOT IN lookup. |
| .is_null(value) | value が NULL か NULLでないかを返す ( value にはブール値も受け付ける) |
| .contains(substr) |  substr が部分文字列を返す（substrにはワイルドカードを含めることができる） |
| .startswith(prefix) | prefix で始まる値を返す. |
| .endswith(suffix) | suffix で終わる値を返す |
| .between(low, high) | low と high の間の値を返す |
| .regexp(exp) | Regular expression match (case-sensitive). |
| .iregexp(exp) | Regular expression match (case-insensitive). |
| .bin_and(value) | Binary AND. |
| .bin_or(value) | Binary OR. |
| .concat(other) | Concatenate two strings or objects using ||. |
| .distinct() | Mark column for DISTINCT selection. |
| .collate(collation) | Specify column with the given collation. |
| .cast(type) | Cast the value of the column to the given type. |


 論理演算子

| 演算子 | 説明 | 記述例 |
|:--|:--|:--|
| & | AND | (User.is_active == True) & (User.is_admin == True) |
| | (pipe) | OR | (User.is_admin) | (User.is_superuser) |
| ~ | NOT | ~(User.username.contains('admin')) |





## リレーションシップと結合
Peeweeがモデル間のリレーションをどのように扱うかを説明します。
まず、次のような  `tweetdb.py` を作成します。
ここでは、ForeignKeyFieldを使って、モデル間の外部キーの関係を定義しています。すべての ForeignKeyField には、暗黙の後方参照があり、提供されたbackref属性を使って、事前にフィルタリングされたSelectクエリとして公開されます。


 tweetdb.py
```
 import datetime
 from peewee import *

 db = SqliteDatabase('tweet.db')

 class BaseModel(Model):
     class Meta:
         database = db

 class User(BaseModel):
     username = TextField()

 class Tweet(BaseModel):
     content = TextField()
     timestamp = DateTimeField(default=datetime.datetime.now)
     user = ForeignKeyField(User, backref='tweets')

 class Favorite(BaseModel):
     user = ForeignKeyField(User, backref='favorites')
     tweet = ForeignKeyField(Tweet, backref='favorites')


 def populate_test_data():
     db.create_tables([User, Tweet, Favorite])

     data = (
         ('huey', ('meow', 'hiss', 'purr')),
         ('mickey', ('woof', 'whine')),
         ('zaizee', ()))
     for username, tweets in data:
         user = User.create(username=username)
         for tweet in tweets:
             Tweet.create(user=user, content=tweet)

     # Populate a few favorites for our users, such that:
     favorite_data = (
         ('huey', ['whine']),
         ('mickey', ['purr']),
         ('zaizee', ['meow', 'purr']))
     for username, favorites in favorite_data:
         user = User.get(User.username == username)
         for content in favorites:
             tweet = Tweet.get(Tweet.content == content)
             Favorite.create(user=user, tweet=tweet)

 if __name__ == '__main__':
    populate_test_data()
```


```
 In [1]: !rm -f tweet.db

 In [2]: %run tweetdb.py
```

> SQLiteでは、デフォルトでは外部キーが有効になっていません。Peewee の foreign-key API を含め、ほとんどのものは問題なく動作しますが、 ForeignKeyField に on_delete を明示的に指定しても、ON DELETE の動作は無視されます。デフォルトのAutoFieldの動作（削除されたレコードIDが再利用できる）と合わせて、これはバグを引き起こす可能性があります。
> この問題を回避するためには、SQLiteを使用するときは次のようにデータベースと接続して、SQLite での外部キーを有効にすることをお勧めします。
>
>       `db = SqliteDatabase('my_app.db', pragmas={'foreign_keys': 1})`
>

### 単純な結合の実行
Peeweeで結合を行う練習として、"huey "のツイートをすべて出力するクエリを書いてみましょう。このクエリでは、Tweetモデルから選択し、Userモデルに結合します。これにより、User.usernameフィールドでフィルタリングすることができます。


```
 In [4]: # %load 30_simple_join.py
    ...: from tweetdb import *
    ...:
    ...: query = Tweet.select().join(User).where(User.username == 'huey')
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(d.content)
    ...:
    ...: # func(query)
    ...:

 In [5]: func(query)
 meow
 hiss
 purr

```

Peeweeは、TweetからUserに結合する際、Tweet.userのForeignKeyFieldで結合していることをモデルから推測しているので、結合述語（"ON "節）を明示的に指定する必要はありません。
次のコードは上記の例と同等ですが、より明示的です。


```
 In [2]: # %load 31_simple_join_on.py
    ...: from tweetdb import *
    ...:
    ...: query = (Tweet
    ...:          .select()
    ...:          .join(User, on=(Tweet.user == User.id))
    ...:          .where(User.username == 'huey'))
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(d.content)
    ...:
    ...: # func(query)
    ...:

 In [3]: func(query)
 meow
 hiss
 purr

```

もし "huey "のUserオブジェクトへの参照がすでにあるなら、User.tweetsの後方参照を使って、hueyのすべてのツイートをリストアップすることができます。


```
 In [2]: # %load 32_back_reference.py
    ...: from tweetdb import *
    ...:
    ...: huey = User.get(User.username == 'huey')
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(d.content)
    ...:
    ...: # func(huey.tweets)
    ...: # huey.tweets
    ...: # huey.tweets.sql()
    ...:

 In [3]: func(huey.tweets)
 meow
 hiss
 purr

 In [4]: huey.tweets
 Out[4]: <peewee.ModelSelect at 0x11061f850>

 In [5]: huey.tweets.sql()
 Out[5]:
 ('SELECT "t1"."id", "t1"."content", "t1"."timestamp", "t1"."user_id" FROM "tweet" AS "t1" WHERE ("t1"."user_id" = ?)',
  [1])

```

huey.tweetsを詳しく見てみると、これは単純なフィルタリング済みのSELECTクエリであることがわかります。

### 複数のテーブルを結合
ユーザーのリストを照会して、そのユーザーが作成したツイートでお気に入りに登録された数を取得することで、結合をもう一度見てみましょう。この場合、ユーザーからツイート、ツイートからお気に入りというように、2回結合する必要があります。さらに、ツイートを作成していないユーザーや、ツイートがお気に入りに登録されていないユーザーも含める必要があるとしています。SQLで表現すると、次のようなクエリになります。

 SQL
```
 SELECT user.username, COUNT(favorite.id)
 FROM user
 LEFT OUTER JOIN tweet ON tweet.user_id = user.id
 LEFT OUTER JOIN favorite ON favorite.tweet_id = tweet.id
 GROUP BY user.username

```

上記のクエリでは、両方の結合がLEFT OUTERとなっています。これは、ユーザーがツイートを持っていない場合や、ツイートを持っていてもその中にお気に入りのものがない場合があるからです。

Peeweeには結合コンテキストという概念があり、join()メソッドを呼び出すと、暗黙のうちに以前に結合されたモデル（最初の呼び出しであれば、選択しているモデル）に結合していることになります。ユーザーからツイートへ、そしてツイートからお気に入りへと、直接結合しているので、単純に次のように書けます。


```
 In [2]: # %load 33_multiple_join.py
    ...: from tweetdb import *
    ...:
    ...: query = (User
    ...:          .select(User.username, fn.COUNT(Favorite.id).alias('count'))
    ...:          .join(Tweet, JOIN.LEFT_OUTER)
    ...:          .join(Favorite, JOIN.LEFT_OUTER)
    ...:          .group_by(User.username))
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.username} {d.count}')
    ...:
    ...: # func(query)
    ...:

 In [3]: func(query)
 huey 3
 mickey 1
 zaizee 0

```

複数のjoinとjoinコンテキストの切り替えを含む、より複雑な例として、Hueyのすべてのツイートと、そのツイートがお気に入りに登録された回数を調べてみましょう。そのためには、2つのジョインを実行する必要があります。また、集約関数を使用してお気に入りの回数を計算します。

このクエリをSQLで記述すると、次のようになります。

 SQL
```
 SELECT tweet.content, COUNT(favorite.id)
 FROM tweet
 INNER JOIN user ON tweet.user_id = user.id
 LEFT OUTER JOIN favorite ON favorite.tweet_id = tweet.id
 WHERE user.username = 'huey'
 GROUP BY tweet.content;

```

前述の例ではtweetからfavoriteへのLEFT OUTER JOINを使用しています。これは、tweetにfavoriteがない場合でも、その内容を結果セットに表示したいからです（カウントは0です）。

Peeweeでは、Pythonで書かれたコードは、SQLで書かれたものと非常によく似ています。


```
 In [2]: # %load 34_favorite_count.py
    ...: from tweetdb import *
    ...:
    ...: query = (Tweet
    ...:          .select(Tweet.content, fn.COUNT(Favorite.id).alias('count'))
    ...:          .join(User)
    ...:          .switch(Tweet)
    ...:          .join(Favorite, JOIN.LEFT_OUTER)
    ...:          .where(User.username == 'huey')
    ...:          .group_by(Tweet.content))
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.content} favorited {d.count} times')
    ...:
    ...: # func(query)
    ...:

 In [3]: func(query)
 hiss favorited 0 times
 meow favorited 1 times
 purr favorited 2 times

```

この例での、 `switch()` の呼び出しに注目してください。この呼び出しは、結合コンテキストをTweetに戻すようPeeweeに指示しています。もし  `switch()` の呼び出しを明示的に行わなかった場合、PeeweeはUser（最後に参加したモデル）を結合コンテキストとして使用し、Favorite.userの外部キーを使用してUserからFavoriteへの結合を構築するため、誤った結果になってしまいます。

結合コンテキストの切り替えを省略したい場合は、代わりに  `join_from()` メソッドを使用します。次のクエリは、前のクエリと同じです。


```
 In [2]: # %load 35_join_from.py
    ...: from tweetdb import *
    ...:
    ...: query = (Tweet
    ...:          .select(Tweet.content, fn.COUNT(Favorite.id).alias('count'))
    ...:          .join_from(Tweet, User)
    ...:          .join_from(Tweet, Favorite, JOIN.LEFT_OUTER)
    ...:          .where(User.username == 'huey')
    ...:          .group_by(Tweet.content))
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.content} favorited {d.count} times')
    ...:
    ...: # func(query)
    ...:

 In [3]: func(query)
 hiss favorited 0 times
 meow favorited 1 times
 purr favorited 2 times

```


### 複数のソースからの選択
データベースに登録されているすべてのツイートを、その作者のユーザー名とともにリストアップしたい場合、次のように書いてみましょう。


```
 In [2]: # %load 36_multiple_source.py
    ...: from tweetdb import *
    ...:
    ...: query = Tweet.select()
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.user.username} -> {d.content}')
    ...:
    ...: # func(query)
    ...:

 In [3]: func(query)
 huey -> meow
 huey -> hiss
 huey -> purr
 mickey -> woof
 mickey -> whine

```

実は、この例のループには大きな問題があります。それは、tweet.user foreign-keyを調べるために、すべてのツイートに対して追加のクエリを実行することです。今回のような小さなテーブルでは、パフォーマンス低下は気にならない程度ですが、行数が増えていくと遅延が大きくなっていきます。
SQLに慣れている方なら、複数のテーブルからSELECTできることを覚えているかもしれません。これにより、1つのクエリでツイート内容とユーザー名を取得することができます。

 SQL
```
 SELECT tweet.content, user.username
 FROM tweet
 INNER JOIN user ON tweet.user_id = user.id;
```

Peeweeでは、こうした複数のテーブルからSELECTを簡単に記述することができます。実際には、クエリを少し変更するだけで済みます。Peeweeに、Tweet.contentとUser.usernameフィールドを選択したいと伝え、tweetからuserへの結合を行います。正しい動作をしていることをもう少しわかりやすくするために、Peeweeに行を辞書として返すように指示することができます。


```
 In [2]: # %load 37_select_from_multi.py
    ...: from tweetdb import *
    ...:
    ...: query = Tweet.select(Tweet.content, User.username).join(User).dicts()
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(d)
    ...:
    ...: # func(query)
    ...: # print(query)
    ...:

 In [3]: func(query)
 {'content': 'meow', 'username': 'huey'}
 {'content': 'hiss', 'username': 'huey'}
 {'content': 'purr', 'username': 'huey'}
 {'content': 'woof', 'username': 'mickey'}
 {'content': 'whine', 'username': 'mickey'}

 In [4]: print(query)
 SELECT "t1"."content", "t2"."username" FROM "tweet" AS "t1" INNER JOIN "user" AS "t2" ON ("t1"."user_id" = "t2"."id")

```

ここでは、".dicts() "の呼び出しをやめて、行をTweetオブジェクトとして返します。Peeweeは、ユーザー名の値をtweet.user.usernameではなく、tweet.usernameに割り当てていることに注目してください。tweetからuserへの外部キーがあり、両方のモデルからフィールドを選択しているので、Peeweeはモデルグラフを再構築してくれます。


```
 In [2]: # %load 38_select_no_dict.py
    ...: from tweetdb import *
    ...:
    ...: query = Tweet.select(Tweet.content, User.username).join(User)
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.user.username} -> {d.content}')
    ...:
   ...: # func(query)
    ...: # print(query)
    ...:

 In [3]: func(query)
 huey -> meow
 huey -> hiss
 huey -> purr
 mickey -> woof
 mickey -> whine

 In [4]: print(query)
 SELECT "t1"."content", "t2"."username" FROM "tweet" AS "t1" INNER JOIN "user" AS "t2" ON ("t1"."user_id" = "t2"."id")

```

必要であれば、join()メソッドにattrを指定することで、上記のクエリでPeeweeが結合したUserインスタンスをどこに置くかを制御することができます。


```
 In [2]: # %load 39_join_attr.py
    ...: from tweetdb import *
    ...:
    ...: query = (Tweet
    ...:          .select(Tweet.content, User.username)
    ...:          .join(User, attr='author'))
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.author.username} -> {d.content}')
    ...:
    ...: # func(query)
    ...: # print(query)
    ...:

 In [3]: func(query)
 huey -> meow
 huey -> hiss
 huey -> purr
 mickey -> woof
 mickey -> whine

 In [4]: print(query)
 SELECT "t1"."content", "t2"."username" FROM "tweet" AS "t1" INNER JOIN "user" AS "t2" ON ("t1"."user_id" = "t2"."id")

```

逆に、単に選択したすべての属性をTweetインスタンスの属性にしたい場合は、（ `dicts()` を呼び出したのと同様に）クエリの最後に `objects()` の呼び出しを追加します。


```
 In [2]: # %load 40_query_object.py
    ...: from tweetdb import *
    ...:
    ...: query = (Tweet
    ...:          .select(Tweet.content, User.username)
    ...:          .join(User, attr='author'))
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.username} -> {d.content}')
    ...:
    ...: # func(query.objects())
    ...: # print(query.objects())
    ...:

 In [3]: func(query.objects())
 huey -> meow
 huey -> hiss
 huey -> purr
 mickey -> woof
 mickey -> whine

 In [4]: print(query.objects())
 SELECT "t1"."content", "t2"."username" FROM "tweet" AS "t1" INNER JOIN "user" AS "t2" ON ("t1"."user_id" = "t2"."id")

```

### より複雑な例
もっと複雑な例として、このクエリでは、すべてのお気に入りを、そのお気に入りを作成したユーザー、お気に入りにされたツイート、そのツイートの作者とともに選択する単一のクエリを書きます。

SQLでは次のように書きます。
 SQL
```
 SELECT owner.username, tweet.content, author.username AS author
 FROM favorite
 INNER JOIN user AS owner ON (favorite.user_id = owner.id)
 INNER JOIN tweet ON (favorite.tweet_id = tweet.id)
 INNER JOIN user AS author ON (tweet.user_id = author.id);

```

これは、お気に入りを作成したユーザのコンテキストと、ツイートの作者のコンテキストの2つです。

Peeweeでは、 `Model.alias()` を使ってモデルクラスの別名をつけ、1つのクエリで2回参照できるようにしています。
結果を反復処理し、結合された値にアクセスすることができます。選択した様々なモデルのフィールドをPeeweeがどのように解決し、モデルグラフを再構築したかに注目してください。


```
 In [2]: # %load 41_alias.py
    ...: from tweetdb import *
    ...:
    ...: Owner = User.alias()
    ...: query = (Favorite
    ...:          .select(Favorite, Tweet.content, User.username, Owner.username)
    ...:
    ...:          .join(Owner)   # Join favorite -> user (owner of favorite).
    ...:          .switch(Favorite)
    ...:          .join(Tweet)   # Join favorite -> tweet
    ...:          .join(User))   # Join tweet -> user
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.user.username} liked ', end='')
    ...:         print(f'{d.tweet.content} by {d.tweet.user.username}')
    ...:
    ...: # func(query)
    ...: # print(query)
    ...:

 In [3]: func(query)
 huey liked whine by mickey
 mickey liked purr by huey
 zaizee liked meow by huey
 zaizee liked purr by huey

 In [4]: print(query)
 SELECT "t1"."id", "t1"."user_id", "t1"."tweet_id", "t2"."content", "t3"."username", "t4"."username" FROM "favorite" AS "t1" INNER JOIN "user" AS "t4" ON ("t1"."user_id" = "t4"."id") INNER JOIN "tweet" AS "t2" ON ("t1"."tweet_id" = "t2"."id") INNER JOIN "user" AS "t3" ON ("t2"."user_id" = "t3"."id")

```


### サブクエリ
Peeweeでは、サブクエリや**共通テーブル式(CTE: Common Table Expression)** など、テーブルに似たあらゆるオブジェクトに結合することができます。サブクエリでの結合を説明するために、すべてのユーザとその最新のツイートを検索してみましょう。

以下がそのSQLです。

 SQL
```
 SELECT tweet.*, user.*
 FROM tweet
 INNER JOIN (
     SELECT latest.user_id, MAX(latest.timestamp) AS max_ts
     FROM tweet AS latest
     GROUP BY latest.user_id) AS latest_query
 ON ((tweet.user_id = latest_query.user_id) AND (tweet.timestamp = latest_query.max_ts))
 INNER JOIN user ON (tweet.user_id = user.id)

```

このためには、各ユーザーとその最新ツイートのタイムスタンプを選択するサブクエリを作成します。そして、外側のクエリでtweetsテーブルを照会し、サブクエリのユーザとタイムスタンプの組み合わせで結合します。
このクエリを繰り返し実行することで、各ユーザーとその最新のツイートを見ることができます。


```
 In [1]: %load 42_subquery.py
    ...: from tweetdb import *
    ...:
    ...: # 最初にサブクエリを定義
    ...: # 外側のクエリではTweetモデルから直接クエリを行うため、
    ...: # Tweetモデルのエイリアスを使用する
    ...: Latest = Tweet.alias()
    ...: latest_query = (Latest
    ...:                 .select(Latest.user,
    ...:                         fn.MAX(Latest.timestamp).alias('max_ts'))
    ...:                 .group_by(Latest.user)
    ...:                 .alias('latest_query'))
    ...:
    ...: # 結合述語(predicate)は、timestampとuser_idに基づいてツイートをマッチさせる
    ...: predicate = ((Tweet.user == latest_query.c.user_id) &
    ...:              (Tweet.timestamp == latest_query.c.max_ts))
    ...:
    ...: # tweet からのクエリと predicate 使ったサブクエリの結合を行う
    ...: query = (Tweet
    ...:          .select(Tweet, User)
    ...:          .join(latest_query, on=predicate)
    ...:          .join_from(Tweet, User))
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.user.username} -> {d.content}')
    ...:
    ...: # func(query)
    ...: # print(query)
    ...:

 In [3]: func(query)
 huey -> purr
 mickey -> whine

 In [4]: print(query)
 SELECT "t1"."id", "t1"."content", "t1"."timestamp", "t1"."user_id", "t2"."id", "t2"."username" FROM "tweet" AS "t1" INNER JOIN (SELECT "t3"."user_id", MAX("t3"."timestamp") AS "max_ts" FROM "tweet" AS "t3" GROUP BY "t3"."user_id") AS "latest_query" ON (("t1"."user_id" = "latest_query"."user_id") AND ("t1"."timestamp" = "latest_query"."max_ts")) INNER JOIN "user" AS "t2" ON ("t1"."user_id" = "t2"."id")


```

このセクションのクエリを作成するために使用したコードには、これまで見たことがないものがいくつかあります。

 `join_from()` を使って、結合コンテキストを明示的に指定しています。 `.join_from(Tweet, User)` と書いていますが、これは. `switch(Tweet).join(User)` と同じ意味です。
サブクエリ内のカラムを参照するのに、魔法のような.c属性を使用しました。.c属性は列の参照を動的に作成するために使用されます。
個別のフィールドを  `Tweet.select()` に渡すのではなく、TweetとUserのモデルを渡しました。これは、与えられたモデルのすべてのフィールドを選択するための省略形です。

### テーブル共通式
前のセクションでは副問い合わせで結合しましたが、共通テーブル式（CTE）を使用することも簡単にできました。ユーザーとその最新のツイートをリストアップするという、前と同じクエリを繰り返しますが、今回はCTEを使って行います。

以下がそのSQLです。
 SQL
```
 WITH latest AS (
     SELECT user_id, MAX(timestamp) AS max_ts
     FROM tweet
     GROUP BY user_id)
 SELECT tweet.*, user.*
 FROM tweet
 INNER JOIN latest
     ON ((latest.user_id = tweet.user_id) AND (latest.max_ts = tweet.timestamp))
 INNER JOIN user
     ON (tweet.user_id = user.id)

```

この例は、サブクエリを使った前の例と非常によく似ています。


```
 In [1]: %load 43_cte.py
    ...: from tweetdb import *
    ...:
    ...: # まずCTEを定義する
    ...: # メインのクエリではTweetモデルから直接クエリを行うため、
    ...: # Tweetモデルのエイリアスを使用する
    ...: Latest = Tweet.alias()
    ...: cte = (Latest
    ...:        .select(Latest.user, fn.MAX(Latest.timestamp).alias('max_ts'))
    ...:        .group_by(Latest.user)
    ...:        .cte('latest'))
    ...:
    ...: # 結合述語(predicate)は、timestampとuser_idに基づいてツイートをマッチさ
    ...: る
    ...: predicate = ((Tweet.user == cte.c.user_id) &
    ...:              (Tweet.timestamp == cte.c.max_ts))
    ...:
    ...: # tweetからのクエリと、predicateを使ったCTEでの結合を行う
    ...: query = (Tweet
    ...:          .select(Tweet, User)
    ...:          .join(cte, on=predicate)
    ...:          .join_from(Tweet, User)
    ...:          .with_cte(cte))
    ...:
    ...: def func(data):
    ...:     for d in data:
    ...:         print(f'{d.user.username} -> {d.content}')
    ...:
    ...: # func(query)
    ...: # print(query)
    ...:

 In [3]: func(query)
 huey -> purr
 mickey -> whine

 In [4]: print(query)
 WITH "latest" AS (SELECT "t1"."user_id", MAX("t1"."timestamp") AS "max_ts" FROM "tweet" AS "t1" GROUP BY "t1"."user_id") SELECT "t2"."id", "t2"."content", "t2"."timestamp", "t2"."user_id", "t3"."id", "t3"."username" FROM "tweet" AS "t2" INNER JOIN "latest" ON (("t2"."user_id" = "latest"."user_id") AND ("t2"."timestamp" = "latest"."max_ts")) INNER JOIN "user" AS "t3" ON ("t2"."user_id" = "t3"."id")

```

### 同一モデルへの複数の外部キー
同じモデルに複数の外部キーがある場合は、どのフィールドで結合するかを明示的に指定するのが良い方法です。

サンプルアプリのモデルに戻って、あるユーザーが別のユーザーをフォローする際に使用されるRelationshipモデルを考えてみましょう。
![](https://gyazo.com/f74095804a0ffccc096b4d6573dbb9b9.png)



 tweepeedb.py
```
 from peewee import *

 DATABASE = 'tweepee.db'
 database = SqliteDatabase(DATABASE)

 class BaseModel(Model):
     class Meta:
         database = database

 class User(BaseModel):
     username = CharField(unique=True)
     password = CharField()
     email = CharField()
     join_date = DateTimeField()

 class Relationship(BaseModel):
     from_user = ForeignKeyField(User, backref='relationships')
     to_user = ForeignKeyField(User, backref='related_to')

     class Meta:
         indexes = (
             (('from_user', 'to_user'), True),
         )

 class Message(BaseModel):
     user = ForeignKeyField(User, backref='messages')
     content = TextField()
     pub_date = DateTimeField()

 def create_tables():
     with database:
         database.create_tables([User, Relationship, Message])


 if __name__ == '__main__':
     create_tables()
```

Userには2つの外部キーがあるので、結合の際には必ずどちらのフィールドを使うかを指定する必要があります。

例えば、charlie がフォローしているユーザーを特定するためには、次のように書きます。


```
 # このコードは例示のためのもので、charlie が定義されていないので実際には動作しない
 query = (User
          .select()
          .join(Relationship, on=Relationship.to_user)
          .where(Relationship.from_user == charlie))

```


一方、どのユーザーが charlie をフォローしているかを判断したい場合は、代わりにカラム `from_user` で結合し、リレーションのto_userでフィルタリングします。



```
 # このコードは例示のためのもので、charlie が定義されていないので実際には動作しない
 query = (User
          .select()
          .join(Relationship, on=Relationship.to_user)
          .where(Relationship.to_user == charlie))

```


### 任意のフィールドでの結合
2 つのテーブル間に外部キーが存在しない場合でも結合を実行できますが、結合述語を手動で指定する必要があります。

次の例では、User と ActivityLog の間に明示的な外部キーはありませんが、ActivityLog.object_id フィールドと User.id の間には暗黙の関係があります。特定のフィールドで結合するのではなく、式を使用して結合します。

 pyton
```
 user_log = (User
             .select(User, ActivityLog)
             .join(ActivityLog, on=(User.id == ActivityLog.object_id), attr='log')
             .where(
                 (ActivityLog.activity_type == 'user_activity') &
                 (User.username == 'charlie')))

 for user in user_log:
     print(user.username, user.log.description)

 #### Print something like ####
 charlie logged in
 charlie posted a tweet
 charlie retweeted
 charlie posted a tweet
 charlie logged out

```


## 自己結合
Peeweeは、自己結合を含むクエリを作成することができます。

### モデルの別名の使用
同じモデル(テーブル)に2回結合するには、クエリの中でテーブルの2番目のインスタンスを表すモデルの別名を作成する必要があります。


```
 class Category(Model):
     name = CharField()
     parent = ForeignKeyField('self', backref='children')

```

親カテゴリーが Electronics であるすべてのカテゴリーを検索したい場合はどうすればよいでしょうか。
一つの方法は、自己結合を行うことです。


```
 Parent = Category.alias()
 query = (Category
          .select()
          .join(Parent, on=(Category.parent == Parent.id))
          .where(Parent.name == 'Electronics'))
```

ModelAliasを使った結合を行う際には、onキーワード引数を使って結合条件を指定する必要があります。この例では、カテゴリとその親カテゴリを結合しています。

### サブクエリの使用
あまり一般的ではない方法として、サブクエリの使用があります。ここでは、サブクエリを使用して、親カテゴリが Electronics であるすべてのカテゴリを取得するクエリを構築する方法を紹介します。


```
 Parent = Category.alias()
 join_query = Parent.select().where(Parent.name == 'Electronics')

 # Subqueries used as JOINs need to have an alias.
 join_query = join_query.alias('jq')

 query = (Category
          .select()
          .join(join_query, on=(Category.parent == join_query.c.id)))

```

 SQL
```
 SELECT t1."id", t1."name", t1."parent_id"
 FROM "category" AS t1
 INNER JOIN (
   SELECT t2."id"
   FROM "category" AS t2
   WHERE (t2."name" = ?)) AS jq ON (t1."parent_id" = "jq"."id")

```


サブクエリからid値にアクセスするには、適切なSQL式を生成する.c magic lookupを使用します。

 pyton
```
 Category.parent == join_query.c.id

```

## 多対多リレーションの実装
Peeweeには、Djangoのように多対多の関係を表現するフィールドが用意されています。この機能はユーザからの多くの要望により追加されましたが、私はこの機能を使わないことを強くお勧めします。なぜなら、フィールドの概念をジャンクションテーブルや隠し結合と混同しているからです。これは便利なアクセサを提供するための厄介なハックに過ぎません。

peeweeで多対多を正しく実装するためには、自分で中間テーブルを作成し、それを介してクエリを行うことになります。

 pyton
```
 class Student(Model):
     name = CharField()

 class Course(Model):
     name = CharField()

 class StudentCourse(Model):
     student = ForeignKeyField(Student)
     course = ForeignKeyField(Course)

```

例えば、数学のクラスに在籍している生徒を探したいとします。

```
 query = (Student
          .select()
          .join(StudentCourse)
          .join(Course)
          .where(Course.name == 'math'))
 for student in query:
     print(student.name)

```

ある学生がどのクラスに登録しているかを照会する。


```
 courses = (Course
            .select()
            .join(StudentCourse)
            .join(Student)
            .where(Student.name == 'da vinci'))

 for course in courses:
     print(course.name)

```

多対多のリレーションを効率的に処理するために、すなわち、すべての学生とそれぞれのコースをリストアップするために、スルーモデルStudentCourseに問い合わせ、学生とコースを事前に計算します。


```
 query = (StudentCourse
          .select(StudentCourse, Student, Course)
          .join(Course)
          .switch(StudentCourse)
          .join(Student)
          .order_by(Student.name))

```

生徒とそのコースのリストを印刷するには、次のようにします。


```
 for student_course in query:
     print(student_course.student.name, '->', student_course.course.name)

```

クエリのselect句でStudentとCourseのすべてのフィールドを選択しているので、これらの外部キーのトラバースは「自由」であり、たった1つのクエリですべての反復を行っています。

### ManyToManyField
ManyToManyField は、多対多のフィールドに対するフィールドライクな API を提供します。最も単純な多対多の状況を除いては、標準の peewee API を使用した方が良いでしょう。しかし、モデルが非常にシンプルで、クエリのニーズがそれほど複雑でない場合は、ManyToManyField を使用できます。

ManyToManyField を使用した学生とコースのモデリング。


```
 from peewee import *

 db = SqliteDatabase('school.db')

 class BaseModel(Model):
     class Meta:
         database = db

 class Student(BaseModel):
     name = CharField()

 class Course(BaseModel):
     name = CharField()
     students = ManyToManyField(Student, backref='courses')

 StudentCourse = Course.students.get_through_model()

 db.create_tables([
     Student,
     Course,
     StudentCourse])

 # "huey "が受講しているすべてのクラスを取得
 huey = Student.get(Student.name == 'Huey')
 for course in huey.courses.order_by(Course.name):
     print(course.name)

 # すべての生徒を "English 101" に入れる。
 engl_101 = Course.get(Course.name == 'English 101')
 for student in engl_101.students:
     print(student.name)

 # 多対多のリレーションにオブジェクトを追加する際には、
 # 単一のモデル・インスタンス、モデルのリスト、あるいはモデルのクエリを渡すことができる
 huey.courses.add(Course.select().where(Course.name.contains('English')))

 engl_101.students.add(Student.get(Student.name == 'Mickey'))
 engl_101.students.add([
     Student.get(Student.name == 'Charlie'),
     Student.get(Student.name == 'Zaizee')])

 # 多対多からアイテムを削除する場合も、同じルールが適用される
 huey.courses.remove(Course.select().where(Course.name.startswith('CS')))

 engl_101.students.remove(huey)

 # .clear()を呼び出すと、関連するすべてのオブジェクトが削除される
 cs_150.students.clear()

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
既存データベースを利用する場合、モデル・ジェネレータである [pwiz ](https://github.com/coleifer/peewee/blob/master/pwiz.py) を使って、peeweeのモデルを自動生成することができます。
例えば、charles_blogという名前のpostgresqlのデータベースがある場合、次のように実行します。

 bash
```
 $ python -m pwiz -e postgresql charles_blog > blog_models.py
```

## 参考資料

- [Peewee 公式ドキュメント http://docs.peewee-orm.com/en/latest/]


#database
#ORM


