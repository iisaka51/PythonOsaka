SQLObjectを使ってみよう
=================
## SQLObject について
SQLObject は、テーブルをクラスとして、行をインスタンスとして、列を属性として、データベースにオブジェクトインターフェイスを提供する、人気のオブジェクトリレーショナルマネージャです。

SQLObject には Python のオブジェクトベースの問い合わせ言語が含まれており、 SQL をより抽象化してデータベースに依存しないアプリケーションを容易に開発することができます。

## インストール
SQLObject は次のようにインストールします。
 bash
```
 $ pip install SQLObject
```

SQLObject を実際に使用するためには、データベースドライバが必要になります。

- **Firebird** / **Interbase** - fdb firebirdsql kinterbasdb
- **MS SQLServer** - adodbapi pymssql
- **MySQL** - mysqlclient, mysql-connector,  oursql,  pymysql,  mariadb
- **ODBC** - pyodbc, pypyodbc,  odbc
- **PostgreSQL** - psycopg2, psycopg,  postgres,  postgresql(psycopg2),  pygresql,  pypostgresql,  py-postgresql,  pg8000
- **SQLite** - sqlite,  pysqlite,  supersqlite
- その他 -  sapdb,  sybase

## SQLObject の使い方
はじめにSQLObjectをインポートします。

```
 from sqlobject import *
```

次にデータベースに接続します。そのURIの書式は次のようになります。
>  `scheme://[user[:password]@]host[:port]/database[?parameters]` 

 `scheme` はデータベースシステムを表す文字列です。
 `parameters` は、次のものを与えることができます。
-  `debug` ： デバッグモードの有効/無効 (default: False),
-  `debugOutput` ： デバッグ出力の有効/無効 (default: False),
-  `cache` ：クエリをキャッシュするかどうか (default: True)
-  `autoCommit` ：自動的にコミットするかどうか (default: True)
-  `debugThreading` ：スレッドのデバッグの有効/無効 (default: False)
-  `logger` ：ロギングを行うかどうか (default: None)
-  `loglevel` ：ログレベルの指定 (default: None)
-  `schema` ：スキーマーの指定(default: None) 

次にデータベースでのURIの例を示します。

```
 mysql://user:password@host/database
 mysql://host/database?debug=1
 postgres://user@host/database?debug=&cache=
 postgres:///full/path/to/socket/database
 postgres://host:5432/database
 sqlite:///full/path/to/database
 sqlite:/C:/full/path/to/database
 sqlite:/:memory:
```

データベースと接続してみましょう。

```
 In [2]: # %load 01_connect.py
    ...: from sqlobject import *
    ...: import os
    ...:
    ...: db_filename = os.path.abspath('test.db')
    ...: connection_string = 'sqlite:' + db_filename
    ...: connection = connectionForURI(connection_string)
    ...: sqlhub.processConnection = connection
    ...:
 
```

## モデルクラスの定義
ここでは、簡単な住所録のようなデータベースを開発してみます。
自分でテーブルを作り、SQLObjectにそのテーブルにアクセスさせても良いのですが、テーブル作成の作業はSQLObjectにさせることもできます。

テーブルを表現するモデルクラスを定義して、 `createTable()` メソッドを呼び出してテーブルを作成します。

```
 In [4]: # %load 02_model.py
    ...: class Person(SQLObject):
    ...:
    ...:     firstName = StringCol()
    ...:     middleInitial = StringCol(length=1, default=None)
    ...:     lastName = StringCol()
    ...:
    ...: # Person.createTable()
    ...:
 
 In [5]: Person.createTable()
 Out[5]: []
 
```

重複してテーブルを作成すると、 `OperationalError` の例外が発生します。

テーブルスキーマは、ほとんどの場合これ以上複雑になることはありません。 `firstName` 、 `middleInitial` 、 `lastName` はすべてデータベースのカラムに対応します。このクラス定義が意味する一般的なスキーマは次のようになります。

 SQL
```
 CREATE TABLE person (
     id INT PRIMARY KEY AUTO_INCREMENT,
     first_name TEXT,
     middle_initial CHAR(1),
     last_name TEXT
 );
```

これは、SQLiteまたはMySQLの場合です。他のデータベースでのスキーマは若干異なります（特にidカラム）。

通常、Pythonではスタイルはフィールド名には、**Snake_Case**（単語の区切りでアンダースコア( `_` )で連結した表記)が用いられることが多いです。。また一般的なJSONスタイルではフィールド名は**CamelCase** (単語の区切りで大文字にする表記)が使用されることが多いです。データベースでは、テーブルのカラム名に使用される表記はデータベースシステムに依存しています。
SQLObject では `style` オブジェクトによって制御することができます。

 `StringCol` 以外のものを使用したり、異なる引数を使用することで、様々なカラムタイプを指示することができます。これについては、「[カラムタイプ http://www.sqlobject.org/SQLObject.html#column-types]」を参照してください。

 `Person` クラス定義では `id` カラムが指定されていないことに注目してください。これは、暗黙的に `id` カラムがプライマリキーとして設定されるためです。

- MySQLデータベース -  `INT PRIMARY KEY AUTO_INCREMENT` 
- PostgreSQL -  `SERIAL PRIMARY KEY` 
- SQLite -  `INTEGER PRIMARY KEY AUTOINCREMENT` 
- その他のバックエンドでは適宜定義する必要があります。

プライマリキーが一つもないテーブルを SQLObject で使用することはできません。また、プライマリキーは不変のものとして扱う必要があります。

データベースの  `id` 名は上書きできますが、Python からは常に  `.id` のようにアクセスします。

これ以降のサンプルで利用するので、次のようなモジュールにしておきます。
 testdb.py
```
 from sqlobject import *
 import os
 
 db_filename = os.path.abspath('test.db')
 connection_string = 'sqlite:' + db_filename
 connection = connectionForURI(connection_string)
 sqlhub.processConnection = connection
 
 class Person(SQLObject):
 
     firstName = StringCol()
     middleInitial = StringCol(length=1, default=None)
     lastName = StringCol()
 
 if __name__ == '__main__':
     Person.createTable()
 
```

## モデルクラスの利用
モデルクラスから新しいオブジェクトを作るには、以下のようにクラスのインスタンスを生成します。

```
 In [2]: # %load 03_create_obj.py
    ...: from testdb import *
    ...:
    ...: v1 = Person(firstName="John", lastName="Doe")
    ...:
    ...: # print(v1)
    ...:
 
 In [3]: print(v1)
 <Person 2 firstName='John' middleInitial=None lastName='Doe'>
 
```

SQLObjectでは、 `NULL` / `None` はデフォルトを意味しません。 `NULL` は、文脈や人によって全く異なる意味を持ちます。ある時は 「デフォルト(default)」を意味し、ある時は「適用できない(not applicable)」を意味し、ある時は「不明(unknown)」を意味します。もし、常にデフォルトにしたいのであれば、クラス定義の中で明示的に指示する必要があります。
また、SQLObject のデフォルト(default)は、データベースのデフォルト(default)と同じではないことにも注意してください SQLObject はデータベースのデフォルトを使用することはしません。

 `firstName` と  `lastName` を省略した場合は、これらのカラムにデフォルトが与えられていないため、エラーが発生することになります。 ( `middleInitial` にはデフォルトがあるため、データベースで  `None` に相当する  `NULL` に設定されます)。

すでに存在するインスタンスを取得するには、 `get()` クラスメソッドを使用できます。

```
 In [2]: # %load 04_get.py
    ...: from testdb import *
    ...:
    ...: v1 = Person.get(1)
    ...:
    ...: # print(v1)
    ...:
 
 In [3]: print(v1)
 <Person 1 firstName='John' middleInitial=None lastName='Doe'>
 
```


オブジェクトを作成すると、そのオブジェクトは直ちにデータベースに挿入されます。SQLObject は、他のシステムのように明示的にオブジェクトをデータベースに保存するのではなく、データベースを即時のストレージとして使用します。

ここでは、このクラスを使用した属性を変更する例を紹介します。

```
 In [2]: # %load 05_get_more.py
    ...: from testdb import *
    ...:
    ...: p1 = Person.get(1)
    ...: v1 = p1.firstName
    ...: v2 = p1.middleInitial
    ...: p1.middleInitial = 'Q'
    ...: v3 = p1.middleInitial
    ...:
    ...: p2 = Person.get(1)
    ...: v4 = p1 is p2
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(p1)
    ...: # print(v3)
    ...: #
    ...: # print(p2)
    ...: # print(v4)
    ...:
 
 In [3]: print(v1)
 John
 
 In [4]: print(v2)
 None
 
 In [5]: print(p1)
 <Person 1 firstName='John' middleInitial='Q' lastName='Doe'>
 
 In [6]: print(v3)
 Q
 
 In [7]: print(p2)
 <Person 1 firstName='John' middleInitial='Q' lastName='Doe'>
 
 In [8]: print(v4)
 True
  
```

カラムには属性のようにアクセスすることができます（これはPythonのプロパティ機能を利用しているためで、これらの属性を取得したり設定したりすると、內部でSQLコードが実行されます）。また、オブジェクトは一意であることに注意してください。通常、特定のIDのPersonインスタンスは、一度に1つしかメモリ上に存在しません。特定のIDの人物を複数回求めると、同じインスタンスが返されます。このようにして、複数のスレッドが同じデータにアクセスする場合、ある程度の一貫性を確保することができます（もちろん、プロセス間でインスタンスを共有することはできませんが）。トランザクションを使用している場合はこの限りではありませんが、トランザクションは必然的に分離されます。

SQLObjectが何を起こなっているのかを知るために、送信されるSQLコマンドを使って説明することにしましょう。


```
 In [1]: %load 06_sql_step1
 
 In [2]: # %load 06_sql_step1
    ...: from testdb import *
    ...:
    ...: Person._connection.debug = True
    ...:
    ...: p1 = Person(firstName='Bob', lastName='Hope')
    ...:
    ...: # print(p1)
    ...:
  1/QueryIns:  INSERT INTO person (first_name, middle_initial, last_name) VALUES ('Bob', NULL, 'Hope')
  1/QueryR  :  INSERT INTO person (first_name, middle_initial, last_name) VALUES ('Bob', NULL, 'Hope')
  1/COMMIT  :  auto
  1/QueryOne:  SELECT first_name, middle_initial, last_name FROM person WHERE ((person.id) = (2))
  1/QueryR  :  SELECT first_name, middle_initial, last_name FROM person WHERE ((person.id) = (2))
  1/COMMIT  :  auto
 
 In [3]: print(p1)
 <Person 2 firstName='Bob' middleInitial=None lastName='Hope'>
 
```

 `モデルクラスインスタンス._connection.debug = True` とすると、そのクラスでSQLObjectが実行したSQLコマンドを標準出力へ表示するようになります。
また、データベース接続時に `debug=True` 引数を与えると、そのデータベースに対して実行するSQLコマンドを表示するようになります。

ここで、新しく Bob のオブジェクトを追加すると、SQLコマンドは発行されているのがわかります。


```
 In [4]: %load 06_sql_step2.py
 
 In [5]: # %load 06_sql_step2.py
    ...: v1 = p1.firstName
    ...:
    ...: # print(v1)
    ...:
 
 In [6]: print(v1)
 Bob
 
```

 pyhon
```
 In [7]: %load 06_sql_step3.py
 
 In [8]: # %load 06_sql_step3.py
    ...: v2 = p1.middleInitial
    ...:
    ...: # print(v2)
    ...:
 
 In [9]: print(v2)
 None
  
```


```
 In [10]: %load 06_sql_step4.py
 
 In [11]: # %load 06_sql_step4.py
     ...: p1.middleInitial = 'Q'
     ...:
  1/Query   :  UPDATE person SET middle_initial = ('Q') WHERE id = (2)
  1/QueryR  :  UPDATE person SET middle_initial = ('Q') WHERE id = (2)
  1/COMMIT  :  auto
 
```

インスタンスの属性を変更することで、SQLコマンドが発行されているのが確認できます。


```
 In [12]: %load 06_sql_step5.py
 
 In [13]: # %load 06_sql_step5.py
     ...: v3 = p1.middleInitial
     ...:
     ...: # print(v3)
     ...:
 
 In [14]: print(v3)
 Q
 
```


```
 In [15]: %load 06_sql_step6.py
 
 In [16]: # %load 06_sql_step6.py
     ...: p2 = Person.get(2)
     ...:
     ...: # print(p2)
     ...:
 
 In [17]: print(p2)
 <Person 2 firstName='Bob' middleInitial='Q' lastName='Hope'>
 
```

既存のインスタンスと同じものを取得するだけなので、データベースへのアクセスはしていないことに注目してください。


```
 In [18]: %load 06_sql_step7.py
 
 In [19]: # %load 06_sql_step7.py
     ...: v4 = p1 is p2
     ...:
     ...: # print(v4)
     ...:
 
 In [20]: print(v4)
 True
```

送信されるSQLはかなり明確で予測可能であることがわかります。
各属性を個別に割り当てると、SQLコマンドも都度発行されますが、代わりに、 `set()` メソッドを使うと複数の属性を１度に割り当てることができ、ちょっとした最適化を行うことができます。

```
 In [2]: # %load 07_set.py
    ...: from testdb import *
    ...:
    ...: Person._connection.debug = True
    ...:
    ...: p = Person(firstName='Freddie', lastName='Mercury')
    ...: p.set(firstName='Adam', lastName='Lambert')
    ...:
    ...: # print(p)
    ...:
  1/QueryIns:  INSERT INTO person (first_name, middle_initial, last_name) VALUES ('Freddie', NULL, 'Mercury')
  1/QueryR  :  INSERT INTO person (first_name, middle_initial, last_name) VALUES ('Freddie', NULL, 'Mercury')
  1/COMMIT  :  auto
  1/QueryOne:  SELECT first_name, middle_initial, last_name FROM person WHERE ((person.id) = (2))
  1/QueryR  :  SELECT first_name, middle_initial, last_name FROM person WHERE ((person.id) = (2))
  1/COMMIT  :  auto
  1/Query   :  UPDATE person SET first_name = ('Adam'), last_name = ('Lambert') WHERE id = (2)
  1/QueryR  :  UPDATE person SET first_name = ('Adam'), last_name = ('Lambert') WHERE id = (2)
  1/COMMIT  :  auto
 
 In [3]: print(p)
 <Person 2 firstName='Adam' middleInitial=None lastName='Lambert'>
 
```

これにより、SQLコマンド `UPDATE` が1つだけ送信されます。また、データベース以外のプロパティでも `set()` を使うことができます。この方法でのメリットはありませんが、データベースと非データベースの属性の違いを隠すことができます。

## 複数のオブジェクトを選択
リレーショナルデータベースでできるすべての種類の結合（JOIN)を、SQLObjectでサポートされているわけではありませんが、単純な `SELECT` は利用することができます。

 `select()` はクラスメソッドであり，次のように呼び出します。

```
 In [2]: # %load 08_select.py
    ...: from testdb import *
    ...:
    ...: Person._connection.debug = True
    ...:
    ...: v1 = Person.select(Person.q.firstName=="John")
    ...: v2 = list(v1)
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
  1/Select  :  SELECT person.id, person.first_name, person.middle_initial, person.last_name FROM person WHERE ((person.first_name) = ('John'))
  1/QueryR  :  SELECT person.id, person.first_name, person.middle_initial, person.last_name FROM person WHERE ((person.first_name) = ('John'))
  1/COMMIT  :  auto
 
 In [3]: print(v1)
 SELECT person.id, person.first_name, person.middle_initial, person.last_name FROM person WHERE ((person.first_name) = ('John'))
 
 In [4]: print(v2)
 [<Person 1 firstName='John' middleInitial=None lastName='Doe'>]
 
```

この例では、 `firstName` が `"John"` の人をすべて返します。

もっと複雑なクエリを見てましょう。

```
 In [2]: # %load 09_select_complex.py
    ...: from testdb import *
    ...:
    ...: Person._connection.debug = True
    ...:
    ...: v1 = Person.select(
    ...:                 OR(Person.q.firstName == "John",
    ...:                 LIKE(Person.q.lastName, "%Hope%")))
    ...: v2 = list(v1)
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
  1/Select  :  SELECT person.id, person.first_name, person.middle_initial, person.last_name FROM person WHERE (((person.first_name) = ('John')) OR (person.last_name LIKE ('%Hope%')))
  1/QueryR  :  SELECT person.id, person.first_name, person.middle_initial, person.last_name FROM person WHERE (((person.first_name) = ('John')) OR (person.last_name LIKE ('%Hope%')))
  1/COMMIT  :  auto
 
 In [3]: print(v1)
 SELECT person.id, person.first_name, person.middle_initial, person.last_name FROM person WHERE (((person.first_name) = ('John')) OR (person.last_name LIKE ('%Hope%')))
 
 In [4]: print(v2)
 [<Person 1 firstName='John' middleInitial=None lastName='Doe'>]
 
```

クラスに、 `q` という属性があり、クエリを作成するための特別なオブジェクトにアクセスしていることに注目してください。 `q` 以下のすべての属性はカラム名を参照しており、これらを使って論理的なクエリを作成すると、そのクエリに対応するSQLコマンドが生成されます。これは、q-マジックと呼ばれる機能で詳しくは後述します。

自分でSQLコマンドを記述して与えることもできます。
 pyhon
```
 In [2]: # %load 10_raw_sql.py
    ...: from testdb import *
    ...:
    ...: Person._connection.debug = True
    ...:
    ...: v1 = Person.select("""person.first_name = 'John' AND
    ...:                              person.last_name LIKE 'D%'""")
    ...: v2 = list(v1)
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
  1/Select  :  SELECT person.id, person.first_name, person.middle_initial, person.last_name FROM person WHERE person.first_name = 'John' AND
                              person.last_name LIKE 'D%'
  1/QueryR  :  SELECT person.id, person.first_name, person.middle_initial, person.last_name FROM person WHERE person.first_name = 'John' AND
                              person.last_name LIKE 'D%'
  1/COMMIT  :  auto
 
 In [3]: print(v1)
 SELECT person.id, person.first_name, person.middle_initial, person.last_name FROM person WHERE person.first_name = 'John' AND
                              person.last_name LIKE 'D%'
 
 In [4]: print(v2)
 [<Person 1 firstName='John' middleInitial=None lastName='Doe'>]
 
```

自分でSQLコマンドを記述する場合は、モデルクラスのクラス変数 `sqlrepr` を使用して、使用する値を引用する必要があります (q を使用する場合は、引用は自動的に行われます)。

キーワード引数  `orderBy` を使って、 `select()` の中で SQLコマンド `ORDER BY` を作成することができます。 `orderBy` は文字列を受け取りますが、これはカラムのデータベース名か、 `Person.q.firstName` という形式のカラムでなければなりません。また、"-colname "や `DESC(Person.q.firstName)` を使って降順を指定したり(これはSQLコマンド `DESC` に変換されるので、数字以外の型でも動作します)、 `MyClass.select().reversed()` を呼び出すこともできます。
 `["-weight", "name"]` となります。

 `sqlmeta` クラス変数  `defaultOrder` を使用して、すべての  `select()` にデフォルトの順序を与えることができます。 `defaultOrder` を使用したときに順序付けされていない結果を得るには、 `orderBy=None` を使用します。

 `select()` でのクエリの結果はジェネレータであり、遅延的に評価されます。そのため、SQLが実行されるのは、クエリ結果を反復処理したときか、 `list()` を使って強制的に結果を実行したときだけです。 `select()` の結果を反復処理するとき、行は一度に1つずつ取得されます。この方法では、結果セット全体をメモリに保持することなく、大きな結果を反復処理することができます。 `.reversed()` メソッドのように、結果全体を取得して反転させるのではなく、SQLObjectが送信されるSQLを変更することで、同等の結果を得ることもできます。

また、 `select()` メソッドの結果をスライスすることもできます。これは SQL クエリを変更するもので、  `peeps[:10]` は SQL クエリの最後に LIMIT 10 を追加することになります。SQLの中でスライスを実行できない場合（例えば、 `peeps[:-10]` ）、 `select()` メソッドが実行され、結果のリストに対してスライスが実行されます。これは通常、負のインデックスを使用した場合にのみ発生します。

特定のケースでは、あるオブジェクトを含む `select()` の結果を複数回取得することがあります（一部の結合など）。このような場合には、 `select()` メソッドにキーワード引数  `distinct=True` を与えることで、SQLコマンド `SELECT DISTINCT` を呼び出すことができます。

 `MyClass.select().count()` のように、結果オブジェクトに対して  `count()` メソッド を呼び出すと、すべての結果をフェッチすることなく、結果の長さを得ることができます。このとき、SQLコマンド `COUNT(*)` が使用され、実際のオブジェクトはデータベースからフェッチされません。スライシングと合わせて、バッチ・クエリを簡単に書くことができます。


```
 start = 20
 size = 10
 query = Table.select() 
 results = query[start:start+size] 
 total = query.count() 
 print(“Showing page %i of %i” % (start/size + 1, total/size + 1))
```

このようなバッチ処理の効率を考える際には、いくつかの要素があり、バッチ処理がどのように使用されているかに大きく依存します。ウェブアプリケーションで、平均100件の結果を一度に10件ずつ表示し、結果をデータベースに追加された日付順に並べている場合を考えてみましょう。スライスすることで、データベースがすべての結果を返さなくて済む（つまり、通信時間を節約できる）一方で、データベースは結果セット全体をスキャンしてアイテムをソートしなければなりません（最初の10件がどれかわかるように）。また、クエリによってはテーブル全体をスキャンする必要があるかもしれません（インデックスの使い方によっては）。インデックスは、このような場合に重要性を高める最も重要な方法であり、スライスよりもキャッシングの方が効果的であると思われます。

この場合、キャッシングとは、完全な結果を取得することを意味します。これには、 `list(MyClass.select(...))` が使えます。ユーザーが結果をページごとに見ていくときに、ある限られた期間、これらの結果を保存することができます。つまり、検索結果の最初のページを表示するコストは少し高くなりますが、それ以降のページはすべて非常にコストが安くなります。

## q-マジック(q-magic)
q-マジック( `q` )は、SQL式を構築するための特別なオブジェクトを返すオブジェクトです。q-magicが返すオブジェクトに対する操作は、すぐには評価されず、記号代数のような方法で保存されます。式全体が評価されて文字列が作成され、バックエンドに送信されます。


```
 In [2]: # %load 20_qmagic.py
    ...: from testdb import *
    ...:
    ...: Person._connection.debug = True
    ...:
    ...: v1 = Person.select(Person.q.firstName=="John")
    ...:
    ...: # print(v1)
    ...:
 
 In [3]: print(v1)
 SELECT person.id, person.first_name, person.middle_initial, person.last_name FROM person WHERE ((person.first_name) = ('John'))
 
```

SQLObjectは `firstName` を評価せず、その式を保存します。
その後、SQLObjectはこれを文字列 `first_name = 'John'` に変換し、その文字列をバックエンドに渡します。

## selectBy()メソッド
 `select` メソッドに代わるものとして、 `selectBy` メソッドがあります。のように動作します。


```
 In [2]: # %load 21_selectby.py
    ...: from testdb import *
    ...:
    ...: Person._connection.debug = True
    ...:
    ...: v1 = Person.selectBy(firstName="John", lastName="Doe")
    ...:
    ...: # print(v1)
    ...:
 
 In [3]: print(v1)
 SELECT person.id, person.first_name, person.middle_initial, person.last_name FROM person WHERE first_name = 'John' AND last_name = 'Doe'
 
```


各キーワード引数は列であり、すべてのキーワード引数はANDされます。戻り値は `SelectResults` なので、それをスライスしたり、数えたり、並べたりすることができます。

## 遅延更新(Lazy Update)
SQLObject は、デフォルトでは属性を設定するたび、あるいは  `set()` メソッドを呼びだすたびに、データベースにSQLコマンド  `UPDATE` を送信します。データベースに対して多数の更新が行われることを避けたいときは、クラスの  `sqlmeta` の定義に  `lazyUpdate = True` を追加してください。

この場合、更新はインスタンスオブジェクトの `syncUpdate()` メソッド、または `sync()` を呼びだしたときにだけ、データベースに書き込まれます。 `sync()` メソッドは、データベースからデータをリフェッチしますが、 `syncUpdate()` メソッドではリフェッチしません。

遅延更新を有効にすると、インスタンスはプロパティ `sqlmeta.dirty` を持ち、これは保留中の更新があるかどうかを示します。
この資料作成時点では、遅延挿入はサポートされていません。

## 一対多のリレーションシップ
1対多のリレーションシップを説明するために、アドレス帳を題材にしてみます。
まず、新しいAddressテーブルを定義します。ここで、人(Person)は複数のアドレスを持つことができます。
これを、**１対多リレーションシップ(One-to-Many Relationships)**と呼びます。


```
 class Address(SQLObject):
     street = StringCol()
     city = StringCol()
     state = StringCol(length=2)
     zip = StringCol(length=9)
     person = ForeignKey('Person')
 
```

 `person = ForeignKey("Person")` というカラム定義に注目してください。これは `Person` オブジェクトへの参照です。他のクラスへの参照は、クラス名を文字列として `ForeignKey()` に与えて設定します。データベースには `person_id` カラムがあり、INT型で、person列を指しています。

>SQLObject が他のクラスを参照するのに文字列を使うのは、他のクラスがまだ存在していないことが多いからです。Python ではクラスは宣言して定義するのではなく作成されるものなので、モジュールがインポートされたときに実行されます。
>もしクラスAがクラスBを参照していたとしても、クラスBがモジュール内のAの下に定義されていた場合、Aクラスが作成されたとき（すべてのカラム属性の作成を含む）、Bクラスは存在しないことになります。SQLObject はクラス名を文字列で参照することで、必要なクラスがすべて作成されるまで待ってから、クラス間のリンクを設定します。

ある人のデータに住所を示す属性が欲しいときは、クラス定義では次のようにします。

```
 class Person(SQLObject):
     # ...
     addresses = MultipleJoin('Address')
```

既存のモデルクラスに、Addressを追加する場合は次のように行います。


```
 >>> Person.sqlmeta.addJoin(MultipleJoin('Address',
 ...                        joinMethodName='addresses'))
```

>ほとんどの場合、SQLObject クラスを作成した後でも変更することができます。クラス定義の中で  `*Col` オブジェクトを含む属性を持つことは、 特定のクラスメソッド ( `addColumn()` など) を呼び出すことと同じです。

これで、aPerson.addresssで後方参照を取得することができます。
モジュールにしておきます。
 one_relation_db.py
```
 from sqlobject import *
 import os
 
 db_filename = os.path.abspath('one_rel.db')
 connection_string = 'sqlite:' + db_filename
 connection = connectionForURI(connection_string)
 sqlhub.processConnection = connection
 
 class Address(SQLObject):
 
     street = StringCol()
     city = StringCol()
     state = StringCol(length=2)
     zip = StringCol(length=9)
     person = ForeignKey('Person')
 
 class Person(SQLObject):
 
     firstName = StringCol()
     middleInitial = StringCol(length=1, default=None)
     lastName = StringCol()
     address = MultipleJoin('Address')
 
 
 if __name__ == '__main__':
     Address.createTable()
     Person.createTable()
     
     d = Person(firstName="John", lastName="Doe")
```

試してみましょう。


```
 In [2]: # %load 30_add_address.py
    ...: from one_relation_db import *
    ...:
    ...: p = Person.get(1)
    ...: v1 = p.address
    ...: v2 = Address(street='123 W Main St', city='Smallsville',
    ...:              state='MN', zip='55407', person=p)
    ...:
    ...: v3 = p.address
    ...:
    ...: # print(p)
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v3)
    ...:
 
 In [3]: print(p)
 <Person 1 firstName='John' middleInitial=None lastName='Doe'>
 
 In [4]: print(v1)
 []
 
 In [5]: print(v2)
 <Address 1 street='123 W Main St' city='Smallsville' state='MN' zip='55407' personID=1>
 
 In [6]: print(v3)
 [<Address 1 street='123 W Main St' city='Smallsville' state='MN' zip='55407' personID=1>]
 
```

>既存クラスへリレーションシップを設定する `sqlmeta.addJoin()` に用いる、 `MultipleJoin()` は、 `RelatedJoin()` と同様に、結果のリストを返します。代わりに `SelectResults` オブジェクトを取得する方が望ましい場合が多く、その場合は `SQLMultipleJoin()` や `SQLRelatedJoin()` を使用するべきです。これらの結合の宣言は上記と変わりませんが、返されるイテレータには多くの追加の便利なメソッドがあります。

## 多対多のリレーションシップ
多対多のリレーションシップを説明するために、ユーザ情報を保持するUserクラスと、役割情報を保持するRoleクラスを使って説明することにします。この2つのクラスオブジェクトは多対多の関係にあり、 `RelatedJoin()` で表現します。

 m2m_relation_db.py
```
 from sqlobject import *
 import os
 
 db_filename = os.path.abspath('m2m_rel.db')
 connection_string = 'sqlite:' + db_filename
 connection = connectionForURI(connection_string)
 sqlhub.processConnection = connection
 
 class User(SQLObject):
 
     class sqlmeta:
         table = "user_table"
 
     username = StringCol(alternateID=True, length=20)
     roles = RelatedJoin('Role')
 
 class Role(SQLObject):
 
     name = StringCol(alternateID=True, length=20)
     users = RelatedJoin('User')
 
 if __name__ == '__main__':
     User.createTable()
     Role.createTable()
 
```

 `sqlmeta` クラスは、さまざまな種類のメタデータを格納するために使用されます。モデルクラス User については、一部のデータベースで User/user が予約後になっているので、 `table` のメタデータをオーバーライドして、明示的にテーブル名を指定しています。


```
 In [2]: # %load 40_add_user.py
    ...: from m2m_relation_db import *
    ...:
    ...: bob = User(username='bob')
    ...: tim = User(username='tim')
    ...: jay = User(username='jay')
    ...:
    ...: admin = Role(name='admin')
    ...: editor = Role(name='editor')
    ...:
    ...: bob.addRole(admin)
    ...: bob.addRole(editor)
    ...: tim.addRole(editor)
    ...:
    ...: v1 = bob.roles
    ...: v2 = tim.roles
    ...: v3 = jay.roles
    ...: v4 = admin.users
    ...: v5 = editor.users
    ...:
    ...: # print(v1)
    ...: # ...
    ...: # print(v5)
    ...:
 
 In [3]: print(v1)
 [<Role 1 name='admin'>, <Role 2 name='editor'>]
 
 In [4]: print(v2)
 [<Role 2 name='editor'>]
 
 In [5]: print(v3)
 []
 
 In [6]: print(v4)
 [<User 1 username='bob'>]
 
 In [7]: print(v5)
 [<User 1 username='bob'>, <User 2 username='tim'>]
 
```

この処理では、両方のクラスを参照する中間テーブル `role_user` が作成されます。このテーブルはクラスとして公開されることはなく、そのデータにマッピングされるPythonオブジェクトを持っていません。これにより、多対多のリレーションでの複雑で面倒な部分が隠されています。

もし、独自の中間テーブルを作成したいときで、追加のカラムを持つ場合は標準的なSQLObjectメソッドの `add()` / `removesomething()` は期待通りに動作しないかもしれないことに注意してください。正しい  `joinColumn` と  `otherColumn` 引数を使って結合を行っていると、このようなメソッドを使って追加のデータを挿入することはできませんし、デフォルト値も設定されないことに注意してください。

例えば、以前のUser/Roleシステムでは、 `UserRole` 中間テーブルを作成し、多対多リレーションの外部キーを含む2つのカラムと、 `datetime.datetime.now` をデフォルトとする、DateTimeColを追加します。中間テーブルから直接データのリストを取得したい場合は、 `User` または `Role` クラスに `MultipleJoin` を追加してください。

カラムには、キーワード引数 `alternateIDが` 追加されていることに注目してください。 `alternateID=True` を使用すると、ユーザ名がユーザを一意に識別するように、そのカラムが行を一意に識別することを意味します。この識別子は、常に存在するプライマリキー( `id` )に加えて使用されます。

>SQLObject は、主キーが一意であること、そして不変であることを強く要求しています。SQLObject を通して主キーを変更することはできませんし、他のメカニズムで主キーを変更すると、実行中の SQLObject プログラム（そしてデータ）に不整合が生じます。このような理由から、無意味な整数の ID が推奨されています。将来変更される可能性のあるユーザ名のようなものは、行を一意に識別することができるかもしれませんが、それは将来変更されるかもしれません。このIDが行の参照に使われない限り、将来変更しても問題ありません。

 `alternateID` カラムは、 `username` という名前のカラムに対する `byUsername` のようなクラスメソッドを作成します（または、 `alternateMethodName` キーワード引数を使用してこれをオーバーライドすることもできます）。
次の’ように使用します。

```
 In [2]: # %load 41_byname.py
    ...: from m2m_relation_db import *
    ...:
    ...: v1 = User.byUsername('bob')
    ...: v2 = Role.byName('admin')
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 <User 1 username='bob'>
 
 In [4]: print(v2)
 <Role 1 name='admin'>
 
```


## リレーションシップによるオブジェクトの選択
 `select` 式では、以下のように複数のクラスを参照することができます。

```
 In [2]: # %load 50_retrieve_obj.py
    ...: from one_relation_db import *
    ...:
    ...: Person._connection.debug = False
    ...:
    ...: p1 = Person.select(
    ...:         AND(Address.q.personID == Person.q.id,
    ...:             Address.q.zip.startswith('504')))
    ...: v1 = list(p1)
    ...:
    ...: p2 = Person.select(
    ...:         AND(Address.q.personID == Person.q.id,
    ...:             Address.q.zip.startswith('554')))
    ...: v2 = list(p2)
    ...:
    ...: # print(p1)
    ...: # print(v1)
    ...: # print(p2)
    ...: # print(v2)
    ...:
 
 In [3]: print(p1)
 SELECT person.id, person.first_name, person.middle_initial, person.last_name FROM address, person WHERE (((address.person_id) = (person.id)) AND (address.zip LIKE ('504%') ESCAPE '\'))
 
 In [4]: print(v1)
 []
 
 In [5]: print(p2)
 SELECT person.id, person.first_name, person.middle_initial, person.last_name FROM address, person WHERE (((address.person_id) = (person.id)) AND (address.zip LIKE ('554%') ESCAPE '\'))
 
 In [6]: print(v2)
 [<Person 1 firstName='John' middleInitial=None lastName='Doe'>]
 
```

また、次のような複雑なクエリを構築する際にq-マジック属性を使用することも可能です。

```
 In [2]: # %load 51_query_qmagic.py
    ...: from one_relation_db import *
    ...:
    ...: Person._connection.debug = False
    ...:
    ...: v1 = Person.select("""address.person_id = person.id AND
    ...:                          address.zip LIKE '504%'""",
    ...:                       clauseTables=['address'])
    ...:
    ...: # print(v1)
    ...:
 
 In [3]: print(v1)
 SELECT person.id, person.first_name, person.middle_initial, person.last_name FROM address, person WHERE address.person_id = person.id AND
                          address.zip LIKE '504%'
 
```

選択しているテーブル以外のテーブルを使用している場合は、  `clauseTables` を使用しなければならないことに注意してください。 `q` 属性を使用した場合、SQLObjectはあなたが使用した余分なクラスを自動的に把握します。

## sqlmetaクラス
SQLObject 0.7 から導入されたこの新しいクラスは、クラス名空間がたくさんの属性で汚れることなく、より明確な方法でメタデータを指定することができます。
このクラスの中で使用できるいくつかの特別な属性があり、その属性を含むクラスの動作を変更します。

- **table**
データベース内のテーブルの名前。明示的な名前が与えられていない場合は、styleとクラス名から派生します。名前が与えられておらず、代替のスタイルも定義されていない場合は、標準の MixedCase から mixed_case への変換が行われます。
- **idName**
データベース内の主キーカラムの名前です。明示的な名前が与えられていない場合は、styleから派生します。デフォルトの名前は id です。
- **idType**
IDを設定する際に、IDを強制的に正規化する関数です。これはデフォルトではintです（すべてのIDはintegersに正規化されます）。
- **style**
スタイルオブジェクト - このオブジェクトは、Pythonの属性名やクラス名と、データベースのカラム名やテーブル名との間の変換に、他のアルゴリズムを使用することができます。詳しくは、名前の付け方の変更を参照してください。これは、IStyleインターフェースのインスタンスです。
- **lazyUpdate**
真偽値（デフォルトはfalse）です。trueの場合、インスタンスに属性を設定しても（またはinst.set(.)を使用しても）、UPDATEクエリはすぐには送信されません（最初にinst.syncUpdates()またはinst.sync()を呼び出す必要があります）。
- **defaultOrder**
オブジェクトを選択する際に、明示的な順序を与えない場合、この属性はデフォルトの順序を示します。この値は、.select() および関連するメソッドに渡されます。詳細は、これらのメソッドのドキュメントを参照してください。
- **cacheValues**
真偽値（デフォルトはtrue）。True の場合、インスタンスが保持されている (そして inst.expire() が呼び出されていない) 限り、行の値がキャッシュされます。
False に設定すると、データベースからの属性の値はキャッシュされません。したがって、オブジェクトの属性にアクセスするたびに、データベースに値を問い合わせることになり、SELECT が発行されます。複数のプロセスからのデータベースへの同時アクセスを処理したい場合には、この方法が適しているでしょう。
- **registry**
SQLObject はクラスを関連付けるのに文字列を使用しますが、この文字列はモジュール名を尊重しないため、異なるシステムを組み合わせた場合に名前の衝突が発生します。この文字列の値は、クラスの名前空間の役割を果たします。
- **fromDatabase**
ブール値を設定します。(デフォルトは  `False` です。 `True` に設定した場合、クラスの作成時にデータベースにテーブルのカラムを問い合わせ、不足しているカラム (すべてのカラムの可能性もあります) が自動的に追加されます。すべての接続がデータベースイントロスペクションを完全に実装しているわけではないことに注意してください。
- **dbEncoding**
 `UnicodeCol` は、 `column.dbEncoding` が `None` の場合、 `sqlmeta.dbEncoding` を検索します（ `sqlmeta.dbEncoding` が `None` の場合、 `UnicodeColはconnection.dbEncoding` を検索し、 `dbEncoding` がどこにも定義されていない場合、デフォルトで  `"utf-8"` になります）。Python 3では、接続のためのエンコーディングは1つでなければなりません - 異なるエンコーディングで異なるカラムを定義しないでください、それは実装されていません。

以下の属性は**内的性質(introspection)**を提供しますが、直接設定るようなものではありません。こ
れらのクラス要素を動的に変更するためには [実行時のカラムと結合の変更 http://www.sqlobject.org/SQLObject.html#runtime-column-and-join-changes]を参照してください。

- **columns**
 `columnName` : anSOColInstance}の辞書です。この読み取り専用の属性によって、列に関する情報を得ることができます。
- **columnList**
columns の値のリスト。カラムの安定した順序付けが必要な場合もあり、その際に使用されます。
- **columnDefinitions**
columnのような辞書ですが、オリジナルのカラム定義（クラス固有ではなく、ロジックを持たないもの）が含まれています。
- **joins**
このクラスのすべてのJoinオブジェクトのリストです。
- **indexes**
このクラスのすべてのインデックスのリストです。
- **createSQL**
createSQL は、単一の SQL コマンドを含む文字列、SQL コマンドのリスト、または dbNames をキーとし、単一の SQL コマンド文字列または SQL コマンドのリストを値とするディクショナリです。これは通常、ALTER TABLEコマンドのためのものです。

また、1つのインスタンス属性があります。

- **expired**
Bool値を指定します。 `True` であれば、次にこのオブジェクトのカラム属性にアクセスしたときに、クエリが実行されます。


>**注意**:
>  `InheritedSQLObject` を使用した場合、 `sqlmeta` の属性は継承されません。
> 例えば、 `sqlmeta.columns` 辞書から親クラスのカラムオブジェクトにアクセスすることはできません。


## sqlmetaの使い方
sqlmetaを使用するには、次の例のようなコードを書く必要があります。

```
 class MyClass(SQLObject):
 
     class sqlmeta:
         lazyUpdate = True
         cacheValues = False
 
     columnA = StringCol()
     columnB = IntCol()
 
     def _set_attr1(self, value):
         # 何かの属性を設定
 
     def _get_attr1(self):
         # 何かの属性の値を取得
```

上記の定義では、 `columnA` と `columnB` という2つのカラムを持つテーブル `my_class` （使用するスタイルを変更した場合、テーブル名が異なることがあります）を作成しています。また、 `MyClass.attr1` を使ってアクセスできる3番目のフィールドもあります。 `sqlmeta` クラスは、 `MyClass` の動作を変更して、遅延更新を行うようにしています(更新をデータベースに書き込むには  `sync()` メソッドを呼ばなければなりません)。また、 `MyClass` はキャッシュを持たないので、情報を要求するたびにデータベースから取得されます。

## j-マジック
 `ForeignKey` と  `SQLMultipleJoin` / `SQLRelatedJoin` の属性を持つ  `q` と同様のマジック属性  `j` があり、 `SQLBuilder` の結合式が与えられた関係を横断するための略記法を提供します。例えば、 `ForeignKey` の `AClass.j.someB` は( `AClass.q.someBID==BClass.q.id` )と同等であり、一致する `SQLMultipleJoin` の `BClass.j.someAs` も同様です。

## SQLObjectクラス
特別な属性として  `_connection` があります。これはテーブルに定義されたデータベースへの接続オブジェクトです。

### _connection
DBConnectionの接続オブジェクトを使用しています。また、 `__connection__` という変数を周囲のモジュールで設定すると、それがピックアップされます（必ずクラスの前に `__connection__` を定義する必要があります）。トランザクションで説明したように、インスタンス生成時に接続オブジェクトを渡すこともできます。

 `sqlhub.processConnection` を定義していれば、この属性をクラスから省略することができ、代わりに `sqlhub` が使用されます。複数のクラスで同じ接続を使用している場合は、入力の手間が省けるだけでなく、メリットもあります。

## オブジェクトのカスタマイズ
今回の例では行っていませんが、クラス定義に独自のメソッドを含めることができます。独自のメソッドを記述することは、他のクラスと同様に簡単ですが、他にもいくつか注意すべき点があります。

### オブジェクトの初期化
SQLObject のインスタンスを生成する方法は、データベースから取得する方法と、データベースに挿入する方法の 2 通りがあります。どちらの場合も、新しいPythonオブジェクトが作成されます。このことが  `__init__()` の役割を少し混乱させています。

ここでは、 `__init__()` について説明する代わりに、オブジェクトが取得または挿入された後に呼び出される `_init()` メソッドを使用してください。このメソッドは `_init(self, id, connection=None, selectResults=None)` というシグネチャを持っていますが、 `_init(self, *args, **kw)` を使いたい場合もあるでしょう。
> 注意: このメソッドをオーバーライドする場合は、  `SQLObject._init(self, *args, **kw)` を呼び出す必要があります。


### マジック属性（プロパティ）の追加
このクラスのメソッドを定義するのに、 `classmethod` 、 `staticmethod` 、 `property` といった通常の手法をすべて使うことができますが、ショートカットを使うこともできます。 `set_` ,  `_get_` ,  `_del_` ,  `_doc_` で始まる名前のメソッドがあれば、それを使ってプロパティが作成されます。
例えば、 `/var/people/images` ディレクトリに人物のIDで保存されている画像ファイルがあるとします。


```
 class Person(SQLObject):
     # ...
 
     def imageFilename(self):
         return 'images/person-%s.jpg' % self.id
 
     def _get_image(self):
         if not os.path.exists(self.imageFilename()):
             return None
         f = open(self.imageFilename())
         v = f.read()
         f.close()
         return v
 
     def _set_image(self, value):
         f = open(self.imageFilename(), 'w')
         f.write(value)
         f.close()
 
     def _del_image(self, value):
         os.unlink(self.imageFilename())
```

後で、 `image` プロパティを属性のように使用すれば、これらのメソッドを呼び出すことで、ファイルシステムに変更が反映することができます。これは、画像のような大きく中身が不明瞭なデータなどのように、データベースではなくファイルに保存したほうがよい情報に適した手法です。

 `Person(..., image=imageText)` のように、コンストラクタや  `set()` メソッドに  `image` キーワードの引数を渡すこともできます。

すべてのメソッド（ `_get_` 、 `_set_` など）はオプションで、他のメソッドを使わずにどれか1つを使うことができます。つまり、_get_attrメソッドだけを定義して、attrを読み取り専用にすることができます。

## カラム属性の上書き
データベースのカラム属性の動作を上書きしたい場合は、もう少し複雑になります。例えば、ある人の名前が変わったときに実行したい特別なコードがあるとします。多くのシステムでは、いくつかのカスタムコードを実行してから、スーパークラスのコードを呼び出します。しかし、スーパークラス(SQLObject)は、あなたのサブクラスのカラムについて何も知りません。プロパティの場合はさらに状況は悪くなります。

SQLObject はそれぞれのカラムに対して  `_set_lastName` のようなメソッドを作成しますが、やはり参照するスーパークラスがないので、これを使うことはできません。(また、SQLObject クラスはあなたのクラスのカラムについて知らないので、 `SQLObject._set_lastName(...)` と書くこともできません。この  `_set_lastName()` メソッドを自分でオーバーライドしたいのです。

これに対処するために、SQLObject はゲッターとセッターのそれぞれに 2 つのメソッドを作っています。
例えば、 `_set_lastName` と  `_SO_set_lastName` です。

```
 class Person(SQLObject):
     lastName = StringCol()
     firstName = StringCol()
 
     def _set_lastName(self, value):
         self.notifyLastNameChange(value)
         self._SO_set_lastName(value)
 
```

また、 `phoneNumber` は数字であること、適切な長さであることを制約し、フォーマットを美しくしたい場合もあります。


```
 import re
 
 class PhoneNumber(SQLObject):
     phoneNumber = StringCol(length=30)
 
     _garbageCharactersRE = re.compile(r'[\-\.\(\) ]')
     _phoneNumberRE = re.compile(r'^[0-9]+$')
     def _set_phoneNumber(self, value):
         value = self._garbageCharactersRE.sub('', value)
         if not len(value) >= 10:
             raise ValueError(
                 'Phone numbers must be at least 10 digits long')
         if not self._phoneNumberRE.match(value):
             raise ValueError, 'Phone numbers can contain only digits'
         self._SO_set_phoneNumber(value)
 
     def _get_phoneNumber(self):
         value = self._SO_get_phoneNumber()
         number = '(%s) %s-%s' % (value[0:3], value[3:6], value[6:10])
         if len(value) > 10:
             number += ' ext.%s' % value[10:]
         return number
```

属性に設定されたデータを変更する際には、少し注意が必要です。一般的に、クラスを使用するプログラマーは、属性に設定した値と同じ値が返ってくることを期待するものです。しかしこの例では、データベースに入れる前にいくつかの文字を削除し、データベースから出すときに再フォーマットしています。
属性へ直接アクセスするのではなくメソッドを使うことの利点は、プログラマーが想定しやすいこうした期待を根絶することです。
また、カラムの取得や設定の際には変換が行われますが、クエリでは変換が行われないことに注意してください。
つまり、 `.select()` や `.selectBy()` を使用したクエリを実行する場合では、SQL/データベースの表現を使用する必要があります。これらのコマンドは、データベース上で実行されるSQLを生成するためです。

## 未定義の属性
SQLObject は、以前に定義されていない属性を設定しても、文句を言ったり、 エラーを起こしたりすることはありません。
データベースに何の変更も加えずに、 単に属性を設定するだけです。これは、タイプミスをしたときに想定外の結果になるかもしれないことに留意してください。
例えば、オブジェクト `a` が `name` 属性を持っていて、 `a.namme="Victor"` と属性名をタイプミスして記述し設定した場合では、エラーも警告も何も出ないため、なぜその値がデータベースに設定されないのかを理解するのに時間を要することになるかもしれません。


## Col Class: カラムの指定
SQLObject では、カラムのリストは、 `Col` オブジェクトのリストとして保持されています。これらのオブジェクトは、それ自体に機能はありませんが、カラムを指定する方法を与えてくれます。

- **dbName**
これは、データベース内のカラムの名前です。名前を指定しない場合、Pythonic名は大文字と小文字が混在したものからアンダースコアで区切られたものに変換されます。
- **default**
このカラムのデフォルト値です。新しい行を作成する際に使用されます。呼び出し可能なオブジェクトや関数を与えた場合は、その関数が呼び出され、その戻り値が使用されます。つまり、DateTimeCol.nowを与えると、デフォルト値を現在の時刻にすることができます。また、sqlbuilder.func.NOW()を使えば、データベースが内部的にNOW()関数を使うようになります。デフォルト値を指定しない場合、newの呼び出しでこのカラムが指定されていないと例外が発生します。
- **defaultSQL**
デフォルトのSQL属性です。
- **alternateID**
このブール値（デフォルトは False）は、主キーではないものの、このカラムをフィールドの ID として使用できるかどうかを示します（例えば、ユーザ名など）。その場合、byUsernameのように、そのオブジェクトを返すクラスメソッドが追加されます。by* の名前が気に入らない場合は alternateMethodName を使用してください (例: alternateMethodName="username")。
このカラムはテーブルスキーマでUNIQUEと宣言されていなければなりません。
- **uniq**
 `True` の場合、SQLObject がテーブルを作成する際に、このカラムが UNIQUE であることを宣言します。
- **notNone**
 `True` の場合、 `None` / `NULL` はこのカラムでは使用できません。SQLObject を使用してテーブルの作成している場合に便利です。
- **sqlType**
このカラムのSQL型（ `INT` 、 `BOOLEAN` など）。これを設定するためのカラムタイプのクラスを使用することができますが、クラスが機能しない場合、単に `sqlType` を使用するのが最も簡単な場合があります。SQLObjectがテーブルを作成する場合にのみ必要です。
- **validator**
フォームエンコードのようなバリデータ。簡単に説明すると、これは `to_python() ` と` from_python()` を提供するオブジェクトで、データベースとの間で読み書きされる値を検証し、変換 (適応またはキャスト) します。
このバリデータは、カラムのバリデータ一覧の最後に追加されます。カラムがバリデータのリストを持っている場合、それらの `from_python()` メソッドはリストの最初から最後まで実行され、 `to_python()` は逆の順序で実行されます。つまり、このバリデータの `from_python()` メソッドはリスト内のすべてのバリデータの後で最後に呼ばれ、 `to_python()` は最初に呼ばれます。
- **validator2**
もうひとつのバリデータです。バリデータのリストの先頭に挿入されます。つまり、その  `from_python()` メソッドは最初に呼ばれ、  `to_python()` は最後に呼ばれます。


## カラムの種類
カラムが他のテーブル/クラスへの参照である場合、 `Col` の代わりに `ForeignKey` クラスを使用する必要があります。一般的には `ForeignKey('Role')` のように使用され、この例ではテーブル `Role` への参照を作成します。これは、 `Col(foreignKey='Role', sqlType='INT')` とほぼ同じです。通常、2つの属性が作成されます。  `role` は `Role` のインスタンスを返し、 `roleID` は関連する `Role` の整数 `ID` を返します。

 `Col` には他にもいくつかのサブクラスがあります。 これらは、SQLObjectがテーブルを作成する際に、異なる種類のカラムを示すために使用されます。

- **BLOBCol**
バイナリデータ用のカラムです。現在のところ、MySQL、PostgreSQL および SQLite のバックエンドでのみ動作します。
- **BoolCol**
PostgresSQLでは BOOLEAN、その他のデータベースでは INT のカラムを作成します。また、データベースのバックエンドに応じて、値を "t"/"f "または0/1に変換します。
- **CurrencyCol**
 `DecimalCol(size=10, precision=2)` に相当します。
警告： `DecimalCol` はSQLでの `MAY` カラムとなるので、正確な数値を返してはいけません、
- **DateTimeCol**
日付と時刻 (通常は datetime または mxDateTime オブジェクトとして返されます)。
- **DateCol**
日付 (通常は datetime または mxDateTime オブジェクトとして返されます)
- **TimeCol**
時刻(通常は datetime または mxDateTime オブジェクトとして返されます)
- **TimestampCol**
MySQLの `TIMESTAMP` 型をサポート。
- **DecimalCol**
Base-10、正確な数値。キーワード引数  `size` で格納する桁数を、 `precision` で小数点以下の桁数を指定します。
警告：DecimalCol の値が DB に正しく格納されているにもかかわらず、小数ではなく浮動小数点として返されることがあります。たとえば、SQLite は型の親和性により、小数を整数または浮動小数点として格納します（NUMERIC ストレージクラス）。SQLObject をインポートする前に、お使いのデータベースアダプタでテストし、Decimal 型と DB アダプタをインポートしてみてください。
#### DecimalStringCol
`DecimalCol ` に似ていますが、データを文字列として格納することで、 一部のドライバでの問題や SQLite での型の親和性の問題を回避します。データを文字列として格納するため、このカラムは SQL 式` (column1 + column2) `で使用することができないため、おそらく  `ORDER BY` で問題が発生することに注意してください。
- **EnumCol**
 `enumValues` キーワード引数で可能な文字列をリストとして与えた、文字列値の 1 つ。
MySQLにはネイティブな `ENUM` 型がありますが、他のデータベースでも動作します（ストレージの効率が悪くなるだけです）。
PostgreSQLでは、EnumColはチェック制約を使用して実装されています。PostgreSQLが `NULL` を含むチェック制約を処理する方法のため、 `EnumCol` のメンバに `None` を指定すると、事実上、SQLレベルでチェック制約が無視されることになります。
（詳細はhttp://archives.postgresql.org/pgsql-sql/2004-12/msg00065.php を参照してください）
- **SetCol**
MySQL  `SET` タイプをサポートします。
- **FloatCol**
浮動小数点
- **ForeignKey**
他のテーブル/クラスへのキー。 `user = ForeignKey('User')` のように使用します。
キーワード引数のカスケードを使って参照整合性をチェックすることができます。
- **IntCol**
整数
- **JsonbCol**
 `jsonb` オブジェクト用のカラムです。PostgresSQL でのみサポートされています。
json.dumps でシリアライズ可能な Python オブジェクトであれば保存可能です。
#### JSONCol
単純な Python オブジェクト ( `None` ,  `bool` ,  `int` ,  `float` ,  `long` ,  `dict` ,  `list` ,  `str` / `unicode` ) を  `json.dumps` / `loads` を使用して JSON との間で変換するユニバーサルな json カラムです。バックエンドに  `VARCHAR` / `TEXT` カラムが必要で、 `JSON` カラムでは動作しません。
- **PickleCol**
BLOBCol の拡張で、このカラムは任意の Python オブジェクトを格納/取得できます。実際にオブジェクトを文字列に(un)pickle し、その文字列を格納/取得します。
このカラムの値を取得・設定することはできますが、 `WHERE` を使用した検索はできません。
- **StringCol**
文字列（キャラクタ）のカラム。追加のキーワード
  - **len** - 文字列の長さを指定します。 与えられた場合、タイプはVARCHAR(length)のようになります。与えられていない場合は、TEXTが想定されます（つまり、長さなし）。
  - **varchar** - boolean; 長さがある場合、 `CHAR` と `VARCHAR` を区別します。デフォルトは `True` 、つまり `VARCHAR` を使用します。
- **UuidCol**:
UUIDを表すカラムです。
PostgreSQLでは `UUID` データ型を使用し、その他のバックエンドでは `VARCHAR(36)` を使用します。
- **UnicodeCol**
 `dbEncoding` キーワード引数も受け付けます。デフォルトは `None` で、これは `sqlmeta` と `connection` で `dbEncoding` を検索することを意味し、 `dbEncoding` がどこにも定義されていない場合はデフォルトで  `"utf-8"` となります
  - 単純な q-マジックフィールドにのみ対応しており、式は使えません。
  - 演算子は  `==` と `!=` にのみ対応しています。

次のコードは動作します。

```
 MyTable.select(u'value' == MyTable.q.name)
 MyTable.select(MyTable.q.name != u'value')
 MyTable.select(OR(MyTable.q.col1 == u'value1', MyTable.q.col2 != u'value2'))
 MyTable.selectBy(name = u'value')
 MyTable.selectBy(col1=u'value1', col2=u'value2')
 MyTable.byCol1(u'value1') 
```

次のコードは動作しません。

```
 MyTable.select((MyTable.q.name + MyTable.q.surname) == u'value')
```

この場合は、次のように記述する必要があります。

```
 MyTable.select((MyTable.q.name + MyTable.q.surname) == u'value'.encode(dbEncoding))
```


## クラステーブル間のリレーションシップ
### ForeignKey
テーブル内の外部参照を扱うのに `ForeignKey` を使用できますが、後方参照や多対多の関係には結合( `JOIN` )を使用します。

ForeignKeyでは、キーワード `cascade` を使って参照整合性を指定することができ、以下の値を持つことができます。

- **None**
削除された関連カラムに対して何のアクションも行わない（これがデフォルト）。 `Person` / `Address` の例では、 `id` 1の `Person` オブジェクト（ `"John Doe"` ）を削除しても、 `id` 1の `Address（123 W Main St）` はそのまま維持されます（ `personID=1` の場合）。
- **False**
 `ForeignKey` を使用して関連する他のオブジェクトを持つオブジェクトの削除は失敗します ( `set ON DELETE RESTRICT` )。 `Person` / `Address` の例では、 `ID` 1 の  `Person (John Doe)` というオブジェクトを削除すると、 `ID` 1 の  `Address (123 W Main St) ` に参照 ( `personID=1` ) があるため、 `SQLObjectIntegrityError` 例外が発生します。
- **True**
 `ForeignKey` を使って関連する他のオブジェクトを持つオブジェクトを削除すると、関連するオブジェクトもすべて削除されます ( `set ON DELETE CASCADE` )。 `Person` / `Address` の例では、 `id1` の `Person（John Doe）` というオブジェクトを削除すると、 `id1` の `Address（123 W Main St）` も削除されます。
- **NULL**
 `ForeignKey` を使用して関連する他のオブジェクトを持つオブジェクトを削除すると、 `ForeignKey` カラムが `NULL` / `None` に設定されます（ `set ON DELETE SET NULL` ）。 `Person` / `Address` の例では、 `id` 1の `Person(John Doe)` というオブジェクトを削除すると、id 1の `Address(123 W Main St)` は維持されますが、 `person` への参照は `NULL` / `None` （ `personID=None` ）に設定されます。

## 一対多結合：MultipleJoinおよびSQLMultipleJoin。
 `MultipleJoin` は結果のリストを返し、 `SQLMultipleJoin` は `SelectResults` オブジェクトを返します。
 `MultipleJoin` のコンストラクタには、いくつかのキーワード引数を指定することができます。

- **joinColumn**
このテーブルを指し示すキーの列名。つまり、テーブルProductがあり、別のテーブルにこのテーブルを指す列ProductNoがある場合、joinColumn="ProductNo "とします。警告: 渡す引数は、クラス内のカラムではなく、データベース内のカラム名に一致していなければなりません。つまり、ProductNo カラムを含む SQLObject がある場合、これはおそらく DB の product_no_id に変換されるでしょう (product_no は通常の大文字から小文字への変換＋アンダースコアの SQLO 翻訳で、_id が追加されているのは、テーブルを参照するカラムがおそらく ForeignKey であり、SQLO が外部キーをそのように変換するためです)。このパラメータを渡す必要があります。
- **orderBy**
select() の orderBy 引数と同様に、結合されたオブジェクトを返す順序を指定できます。defaultOrder が指定されていない場合は、これが使用されます。
- **joinMethodName**
動的に結合を追加する場合（クラスメソッドのaddJoinを使用）、結合のアクセサの名前を指定できます。これは、自動的に作成することもでき、通常は暗示されます( `addresss = MultipleJoin(...) implies joinMethodName="addresss"` ）。

## 多対多結合：RelatedJoinとSQLRelatedJoin
 `RelatedJoin` は結果のリストを返し、 `SQLRelatedJoin` は  `SelectResults` オブジェクトを返します。
 `RelatedJoin` は、 `MultipleJoin` のすべてのキーワード引数と、以下のキーワード引数を持ちます。

- **otherColumn**
 `joinColumn` と似ていますが、結合されたクラスを参照します。カラム名に関する警告は同じです。
- **intermediateTable**
両方のクラスを参照する中間テーブルの名前です。警告: SQLO クラスを表す名前ではなく、データベースのテーブル名を渡す必要があります。
- **addRemoveName**
 `user` / `role` の例では、 `addRole(role)` と `removeRole(role)` というメソッドが作られます。これらのメソッド名の `Role` 部分は、ここに文字列値を与えることで変更できます。
- **createRelatedTable**
デフォルトは Trueです。Falseの場合、関連テーブルは自動的には作成されません。代わりに手動で作成する必要があります 


SQLObject を継承したクラス Alpha と Beta があり、多対多のリレーションに AlphasAndBetas が使用されているとします。AlphasAndBetasには、Alphaを参照するalphaIndex Foreign Keyカラムと、Betaを参照するbetaIndex FKカラムが含まれています。Alphaに'betas'のRelatedJoinを追加したい場合は、Alphaに'Beta'(クラス名!)を最初のパラメータとして渡し、'alpha_index_id'をjoinColumnに、'beta_index_id'をotherColumnに、'alphas_and_betas'をintermediateTableに渡して追加します。

joinColumn、otherColumn、intermediateTableを使う必要があるスキーマの例です。


```
 class Person(SQLObject):
     username = StringCol(length=100, alternateID=True)
     roles = RelatedJoin('Role', joinColumn='person', otherColumn='role',
                         intermediateTable='assigned_roles')
 class Role(SQLObject):
     name = StringCol(length=50, alternateID=True)
     roles = RelatedJoin('Person', joinColumn='role', otherColumn='person',
                         intermediateTable='assigned_roles')
```


 SQL
```
 CREATE TABLE person (
     id SERIAL,
     username VARCHAR(100) NOT NULL UNIQUE
 );
 
 CREATE TABLE role (
     id SERIAL,
     name VARCHAR(50) NOT NULL UNIQUE
 );
 
 CREATE TABLE assigned_roles (
     person INT NOT NULL,
     role INT NOT NULL
 );
```

## １対１の結合：SingleJoin
MultipleJoinと似ていますが、リストではなく1つのオブジェクトを返します。

## 接続プール(Connection Pooling)
接続オブジェクトは、プールから新しい低レベルのDB API接続を取得して保存します。低レベルの接続はプールから削除されます。「リリース(Release)」は 「プールに戻す」ことを意味します。シングル・スレッド・プログラムの場合、プールには1つの接続があります。

プールが空の場合、新しい低レベル接続が開かれます。プールを無効にしている（ `conn._pool = None` を設定されている）場合、接続はプールに戻るのではなく閉じられます。


## トランザクション
SQLObject におけるトランザクションのサポートは、データベースに依存しています。トランザクションは以下のように使用できます。


```
 conn = DBConnection.PostgresConnection('yada')
 trans = conn.transaction()
 p = Person.get(1, trans)
 p.firstName = 'Bob'
 trans.commit()
 p.firstName = 'Billy'
 trans.rollback()
```

ここでのtransオブジェクトは基本的に1つのデータベース接続のラッパーであり、 `commit()` と `rollback()` はそのメッセージを低レベルの接続に渡すだけです。

 `commit()` はいくらでも呼ぶことができますが、 `rollback()` の後には. `begin()` を呼ばなければなりません。最後の `commit()` は `commit(close=True)` とし、低レベル接続を接続プールに戻すようにします。

 `SELECT FOR UPDATE` をサポートしているデータベースでは、 `SELECT FOR UPDATE` を使用することができます。


```
 Person.select(Person.q.name=="value", forUpdate=True, connection=trans)
```

メソッド  `sqlhub.doInTransaction` を使用すると、トランザクション内でコードの一部を実行することができます。このメソッドは、 `callable` 、位置引数、キーワード引数を受け入れます。 `processConnection` または `threadConnection` を使用してトランザクションを開始し、 `callable` を呼び出し、トランザクションをコミットして基礎となる接続を閉じ、 `callable` が返したものを返します。 `callable` の呼び出し中にエラーが発生した場合は、トランザクションをロールバックし、例外を発生させます。

## スキーマの自動生成
すべての接続は、クラス定義に基づいてテーブルの作成と削除をサポートしています。まず、クラス定義を準備する必要があります。つまり、カラムに型情報を含める必要があります。

### インデックス
これは、SQLObject を使用してテーブルを作成する場合にのみ意味があります (SQLObject はインデックスの実装をデータベースに依存します)。これもまた、以下のような属性の割り当てで行います。


```
 firstLastIndex = DatabaseIndex('firstName', 'lastName')
```

これにより、2つのカラムに対するインデックスが作成され、特定の名前を選択する場合に便利です。もちろん、単一のカラムを指定することもできますし、文字列の名前ではなくカラムオブジェクト（firstName）を指定することもできます。なお、uniqueやalternateID（uniqueを意味する）を使用すると、データベースがインデックスを作成する可能性がありますが、主キーは常にインデックスが作成されます。

DatabaseIndexにキーワード引数uniqueを与えると、ユニークなインデックスが作成されます - カラムの組み合わせはユニークでなければなりません。

辞書をカラム名の代わりに使用して、追加のオプションを追加することもできます。例えば、以下のようになります。

```
 lastNameIndex = DatabaseIndex({'expression': 'lower(last_name)'})
```

この場合、インデックスは小文字バージョンのカラムになります。これをサポートしているのはPostgreSQLだけのようです。することもできます。

```
 lastNameIndex = DatabaseIndex({'column': lastName, 'length': 10})
```

これは、データベースに最初の10文字にのみ注意を払うように求めるものです。MySQLだけがこれをサポートしていますが、他のデータベースでは無視されます。

## テーブルの作成と削除
テーブルを作成するには、createTable を呼び出します。これは2つの引数を取ります。

- **ifNotExists**
テーブルがすでに存在している場合は、作成を試みません。デフォルトはFalseです。
- **createJoinTables**
テーブルを作成します。
多対多のリレーションを使用した場合、中間テーブルを作成します（ただし、関係する2つのクラスのうち1つに対してのみ）。デフォルトは True です。

dropTableは引数ifExistsとdropJoinTablesを取りますが、これは自明です。

## 動的なクラス
SQLObject クラスは動的に操作することができます。これにより、XML ファイル、データベースのイントロスペクション、 グラフィカルインターフェイスなどから SQLObject クラスを構築することができます。

### クラスの自動生成
SQLObject は、データベースからテーブルの記述を読み込み、クラスの列を（通常 _columns 属性で記述されるように）記入することができます。これは次のように行います。

```
 class Person(SQLObject):
     class sqlmeta:
         fromDatabase = True
```

 `_columns` でカラムを指定しても、不足しているカラムだけが追加されます。

## 実行時のカラムと結合の変更
クラスへのカラムの追加や削除は、ランタイムに行うことができます。このような変更は、クラスにその場で変更が加えられるため、すべてのインスタンスに影響します。 `sqlmeta` オブジェクトのクラスには、 `addColumn` と `delColumn` という2つのメソッドがあり、どちらも引数として `Col` オブジェクト（またはサブクラス）を取ります。また、オプション引数として `changeSchema` があり、これがTrueの場合、データベースに列を追加したり、データベースから列を削除したりします（通常は `ALTER` コマンドを使用します）。

カラムを追加する際には、 `StringCol("username", length=20)` のように、カラムのコンストラクタの一部として名前を渡す必要があります。カラムを削除する際には、 `Col` オブジェクト ( `sqlmeta.columns` にあるもの、または  `addColumn` で使用したもの) を使用するか、カラム名を使用することができます ( `MyClass.delColumn("username")` のように)。

また、 `MyClass.addJoin(MultipleJoin("MyOtherClass"))` のようにJoinを追加したり、 `delJoin` で `Join` を削除することもできます。  `delJoin` は文字列を取らないので、 `sqlmeta.joins` 属性から `Join` オブジェクトを取り出す必要があります。

```
 class Person(SQLObject):
     class sqlmeta:
         style = MixedCaseStyle(longID=True)
     firstName = StringCol()
     lastName = StringCol()
```

ここで、 `Person.createTable()` を実行すると、次のSQLコマンドが発行されます。 
 SQL
```
 CREATE TABLE Person (
     PersonID INT PRIMARY KEY,
     FirstName Text,
     LastName Text
 )
```

MixedCaseStyle オブジェクトは、単語の最初の大文字化を処理しますが、それ以外はそのままにしておきます。longID=Trueを使用することで、主キーが通常の参照のように見えることを示しています（MixedCaseStyleの場合はPersonID、デフォルトスタイルの場合はperson_id）。

スタイルをグローバルに変更したい場合は、次のように接続にスタイルを割り当てます。

```
 __connection__.style = MixedCaseStyle(longID=True)
```

## 整数以外のキー
厳密にはレガシーデータベースの問題ではありませんが、これは「イレギュラー」のカテゴリーに当てはまります。非整数キーを使用した場合、すべての主キーの管理は自分で行わなければなりません。また、インスタンスを作成する際には、 コンストラクタに id キーワード引数を渡さなければなりません (Person(id='555-55-5555', ...)のように)。

## データベース接続：DBConnection
DBConnectionモジュールには、この資料作成時点で次の6つの外部クラスがあります。

- MySQLConnection
- PostgresConnection
- SQLiteConnection
- SybaseConnection
- MaxdbConnection
- MSSQLConnection

キーワード引数 `debug` を任意のコネクタに渡すことができます。 `True` に設定すると、データベースに送信されたすべてのSQLがコンソールにも出力されます。

また、 `logger` キーワード引数を渡すことができます。このキーワードが指定され、 `debug` が  `True` の場合、SQLObject は、コンソールに直接出力するのではなく、その  `logger` を通してデバッグ用の出力を行います。引数  `loglevel` では、ログレベルを選択することができます。これは、 `debug` 、 `info` 、 `warning` 、 `error` 、 `critical` 、 `exception` のいずれかです。 `logger` が存在しない、あるいは空の場合、SQLObject はロギングの代わりに  `print()` を使用します。この場合、 `logoglevel` は  `stdout` (標準出力) または  `stderr` (標準エラー出力) になります。

次のコードは、ロギングを設定するときのサンプルです。

```
 import logging
 logging.basicConfig(
     filename='test.log',
     format='[%(asctime)s] %(name)s %(levelname)s: %(message)s',
     level=logging.DEBUG,
 )
 log = logging.getLogger("TEST")
 log.info("Log started")
 
 __connection__ = "sqlite:/:memory:?debug=1&logger=TEST&loglevel=debug"
```

このコードは、SQLObject のデバッグメッセージを  `test.log` ファイルにリダイレクトします。


## まとめ
SQLObject を使うとデータベース操作をPythonらしいオブジェクト操作で処理することができるため、データベースやSQLに対する知識量が少なくてすみます。
SQLObject はモデルクラスからテーブルを自動作成することができます。
これは既存データベースに対して利用するようなときは、属性名のタイプミスがデータベースを汚すことになるので、注意が必要です。それでも、SQLObject の有益性を損なうものではありません。


## 参考資料
- [SQLObject ソースコード ](https://github.com/sqlobject/sqlobject)
- [SQLObject 公式ドキュメント http://sqlobject.org/]




