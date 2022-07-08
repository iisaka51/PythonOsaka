sqlite-utilsを使ってみよう
=================

## sqlite-utils について
sqlite-utils は、SQLiteデータベースファイルを素早く作成、操作するためのPythonライブラリおよびコマンドラインツールです。
sqlite-utils は ORM として開発されたわけではありませんが、SQLite の機能を柔軟により簡単に操作できるように設計されています。

このチュートリアルでは、sqlite-utils  を使用してデータを操作する方法を紹介します。

## インストール
ライブラリをインストールするには、次のように実行します。

 bash
```
 $ pip install sqlite-utils
 
```

## データベースへの接続または作成

データベースオブジェクトは、ディスク上のファイルへのパス、または既存のSQLite3データベース接続のいずれかを渡すことで構築されます。


```
 In [2]: # %load 01_connection.py
    ...: from sqlite_utils import Database
    ...:
    ...: db = Database("my_data.db", recreate=True)
    ...:
    
```

これにより、 `my_database.db` がまだ存在していなければ作成されます。

データベースをゼロから再作成したいときは、 `recreate=True` 引数を使用できます。
この引数を与えると、既存のファイルがすでに存在するときは、まずディスクから削除されます。

python
```
 db = Database("my_database.db", recreate=True)
 
```

ファイルパスの代わりに、既存のSQLite接続を渡すことができます。


```
 import sqlite3
 
 db = Database(sqlite3.connect("my_database.db"))
 
```

インメモリーのデータベースを作りたい場合は、次のようにします。


```
 db = Database(memory=True)
 
```

## テーブルの作成
Pythonの辞書リストを渡して、creaturesという名前の新しいテーブルをデータベースに作成することにします。

 `db[name_of_table]` は、その名前を持つデータベースのテーブルオブジェクトにアクセスします。
そのテーブルにデータを挿入すると、まだ存在していなければテーブルが作成されます。

 pyton
```
 In [4]: # %load 02_create_table.py
    ...: table = db["creatures"]
    ...:
    ...: table.insert_all([{
    ...:      "name": "Cleo",
    ...:      "species": "dog",
    ...:      "age": 6
    ...:  }, {
    ...:      "name": "Lila",
    ...:      "species": "chicken",
    ...:      "age": 0.8,
    ...:  }, {
    ...:      "name": "Bants",
    ...:      "species": "chicken",
    ...:      "age": 0.8,
    ...:  }])
    ...:
 Out[4]: <Table creatures (name, species, age)>
```


sqlite-utilsは、 `.insert_all()` に渡された辞書のキーとデータ型にマッチするテーブルスキーマを自動的に作成します。

そのスキーマは  `table.schema` を使って見ることができます。


```
 In [5]: print(table.schema)
 CREATE TABLE [creatures] (
    [name] TEXT,
    [species] TEXT,
    [age] FLOAT
 )
 
```

## データへのアクセス
 `table.rows` プロパティは、テーブルの行をループさせて、それぞれをPythonの辞書として返すことができます。


```
 In [7]: # %load 03_access_data.py
    ...: for row in table.rows:
    ...:     print(row)
    ...:
 {'name': 'Cleo', 'species': 'dog', 'age': 6.0}
 {'name': 'Lila', 'species': 'chicken', 'age': 0.8}
 {'name': 'Bants', 'species': 'chicken', 'age': 0.8}
 
```

 `db.query(sql)` メソッドは、SQLクエリを実行し、その結果を辞書として返すことができます。


```
 In [9]: # %load 04_sql_query.py
    ...: list(db.query("select * from creatures"))
    ...:
 Out[9]:
 [{'name': 'Cleo', 'species': 'dog', 'age': 6.0},
  {'name': 'Lila', 'species': 'chicken', 'age': 0.8},
  {'name': 'Bants', 'species': 'chicken', 'age': 0.8}]
 
```

もしくは、ループで各要素を取り出せます。


```
 In [11]: # %load 05_sql_query_with_loop.py
     ...: for row in db.query("select name, species from creatures"):
     ...:     print(f'{row["name"]} is a {row["species"]}')
     ...:
 Cleo is a dog
 Lila is a chicken
 Bants is a chicken
 
```

## SQLパラメータ
クエッション記号( `?` ) をプレースホルダーとして使い、変数のリストを渡すことで、パラメータ化されたクエリを実行することができます。渡された変数は正しく引用されるので、SQLインジェクションの脆弱性からコードを保護することができます。

 pytohn
```
 In [13]: # %load 06_sql_parameter.py
     ...: list(db.query("select * from creatures where age > ?", [1.0]))
     ...:
 Out[13]: [{'name': 'Cleo', 'species': 'dog', 'age': 6.0}]
 
```

クエスチョン記号の代わりに SQLパラメータを使い、辞書を使って値を入力することができます。


```
 In [15]: # %load 07_sql_parameter_valirable.py
     ...: list(db.query("select * from creatures where species = :species",
     ...:               {"species": "chicken"}))
     ...:
 Out[15]:
 [{'name': 'Lila', 'species': 'chicken', 'age': 0.8},
  {'name': 'Bants', 'species': 'chicken', 'age': 0.8}]
 
```

この例では、SQLパラメータとして  `:species` を使っています。パラメータに渡す辞書には、 `{'変数名:その値}` の形式でを与えます。

## プライマリキー
このテーブルを作成したとき、プライマリキーを指定しませんでした。SQLiteは、他のプライマリキーが定義されていない場合、rowidというプライマリキーを自動的に作成します。

 `select rowid, * from creatures` を実行すると、この隠されたプライマリキーを見ることができます。


```
 In [17]: # %load 08_primarykey_rowid.py
     ...: list(db.query("select rowid, * from creatures"))
     ...:
 Out[17]:
 [{'rowid': 1, 'name': 'Cleo', 'species': 'dog', 'age': 6.0},
  {'rowid': 2, 'name': 'Lila', 'species': 'chicken', 'age': 0.8},
  {'rowid': 3, 'name': 'Bants', 'species': 'chicken', 'age': 0.8}]
 
```

また、 `table.pks_and_rows_where()` を使うことでもわかります。

```
 In [19]: # %load 09_primarykey_check.py
     ...: for pk, row in table.pks_and_rows_where():
     ...:     print(pk, row)
     ...:
 1 {'rowid': 1, 'name': 'Cleo', 'species': 'dog', 'age': 6.0}
 2 {'rowid': 2, 'name': 'Lila', 'species': 'chicken', 'age': 0.8}
 3 {'rowid': 3, 'name': 'Bants', 'species': 'chicken', 'age': 0.8}
 
```


このテーブルに独自のプライマリキー  `id` を設定して再作成しましょう。

 `table.drop()` は、テーブルを削除します。


```
 In [21]: # %load 10_drop_table.py
     ...: table.drop()
     ...: table
     ...:
 Out[21]: <Table creatures (does not exist yet)>
 
```

db.tablesを使って、データベース内のテーブルの一覧を見ることができます。


```
 In [23]: # %load 11_list_tables.py
     ...: db.tables
     ...:
 Out[23]: []
 
```

このテーブルを再度作成し、今度は  `id` カラムを追加します。

 `pk="id"` を使用して、 `id` カラムをテーブルのプライマリキーとして扱うことを指定します。


```
 In [25]: # %load 12_create_table_with_pk.py
     ...: table.insert_all([{
     ...:     "id": 1,
     ...:     "name": "Cleo",
     ...:     "species": "dog",
     ...:     "age": 6
     ...: }, {
     ...:     "id": 2,
     ...:     "name": "Lila",
     ...:     "species": "chicken",
     ...:     "age": 0.8,
     ...: }, {
     ...:     "id": 3,
     ...:     "name": "Bants",
     ...:     "species": "chicken",
     ...:     "age": 0.8,
     ...: }], pk="id")
     ...:
 Out[25]: <Table creatures (id, name, species, age)>
 
```


```
 In [26]: print(table.schema)
 CREATE TABLE [creatures] (
    [id] INTEGER PRIMARY KEY,
    [name] TEXT,
    [species] TEXT,
    [age] FLOAT
 )
 
```


## さらにレコードを追加する
 `.insert_all()` を再度呼び出して、さらにレコードを挿入することができます。それでは、さらに2つのデータを追加してみましょう。


```
 In [28]: # %load 13_insert_more.py
     ...: table.insert_all([{
     ...:     "id": 4,
     ...:     "name": "Azi",
     ...:     "species": "chicken",
     ...:     "age": 0.8,
     ...: }, {
     ...:     "id": 5,
     ...:     "name": "Snowy",
     ...:     "species": "chicken",
     ...:     "age": 0.9,
     ...: }], pk="id")
     ...:
 Out[28]: <Table creatures (id, name, species, age)>
 
```


```
 In [30]: # %load 14_list_all.py
     ...: list(table.rows)
     ...:
 Out[30]:
 [{'id': 1, 'name': 'Cleo', 'species': 'dog', 'age': 6.0},
  {'id': 2, 'name': 'Lila', 'species': 'chicken', 'age': 0.8},
  {'id': 3, 'name': 'Bants', 'species': 'chicken', 'age': 0.8},
  {'id': 4, 'name': 'Azi', 'species': 'chicken', 'age': 0.8},
  {'id': 5, 'name': 'Snowy', 'species': 'chicken', 'age': 0.9}]
 
```

id 列は整数の主キーなので、ID を指定せずにレコードを挿入すると、自動的に 1 つ追加されます。

追加するレコードは1つだけなので、 `.insert_all()` ではなく  `.insert()` を使用します。


```
 In [32]: # %load 15_insert_one.py
     ...: table.insert({"name": "Blue", "species": "chicken", "age": 0.9})
     ...:
 Out[32]: <Table creatures (id, name, species, age)>
 
```

 `table.last_pk` を使えば、先ほど追加したレコードのIDを確認することができます。


```
 In [33]: table.last_pk
 Out[33]: 6
 
```

改めて全部のレコードを参照してみましょう。


```
 In [35]: # %load 14_list_all.py
     ...: list(table.rows)
     ...:
 Out[35]:
 [{'id': 1, 'name': 'Cleo', 'species': 'dog', 'age': 6.0},
  {'id': 2, 'name': 'Lila', 'species': 'chicken', 'age': 0.8},
  {'id': 3, 'name': 'Bants', 'species': 'chicken', 'age': 0.8},
  {'id': 4, 'name': 'Azi', 'species': 'chicken', 'age': 0.8},
  {'id': 5, 'name': 'Snowy', 'species': 'chicken', 'age': 0.9},
  {'id': 6, 'name': 'Blue', 'species': 'chicken', 'age': 0.9}]
 
```

既存のIDで新しいレコードを追加しようとすると、 `IntegrityError` 例外が発生します。


```
 In [37]: # %load 16_duplicated_id.py
     ...: table.insert({"id": 6, "name": "Red", "species": "chicken", "age": 0.9}
     ...: )
     ...:
 ---------------------------------------------------------------------------
 IntegrityError                            Traceback (most recent call last)
 <ipython-input-37-83c835667aa1> in <module>
       1 # %load 16_duplicated_id.py
 ----> 2 table.insert({"id": 6, "name": "Red", "species": "chicken", "age": 0.9})
 (中略)
 --> 419             return self.conn.execute(sql, parameters)
     420         else:
     421             return self.conn.execute(sql)
 
 IntegrityError: UNIQUE constraint failed: creatures.id
 
```

 `creatures.id` にはUNIQUE 制約があるため、 `IntegrityError` 例外が発生しました。
 `replace=True` を使うと、マッチしたレコードを新しいレコードに置き換えることができます。


```
 In [39]: # %load 17_insert_replace.py
     ...: table.insert(
     ...:       {"id": 6, "name": "Red", "species": "chicken", "age": 0.9},
     ...:       replace=True)
     ...:
 Out[39]: <Table creatures (id, name, species, age)>
 
```


```
 In [41]: # %load 14_list_all.py
     ...: list(table.rows)
     ...:
 Out[41]:
 [{'id': 1, 'name': 'Cleo', 'species': 'dog', 'age': 6.0},
  {'id': 2, 'name': 'Lila', 'species': 'chicken', 'age': 0.8},
  {'id': 3, 'name': 'Bants', 'species': 'chicken', 'age': 0.8},
  {'id': 4, 'name': 'Azi', 'species': 'chicken', 'age': 0.8},
  {'id': 5, 'name': 'Snowy', 'species': 'chicken', 'age': 0.9},
  {'id': 6, 'name': 'Red', 'species': 'chicken', 'age': 0.9}]
 
```

## レコードの更新
今度は  `table.update(pk, updates)` メソッドを使って、そのレコードの名前をBlueに戻します。


```
 In [43]: # %load 18_update.py
     ...: table.update(6, {"name": "Blue"})
     ...:
 Out[43]: <Table creatures (id, name, species, age)>
 
```


```
 In [45]: # %load 19_query_by_id.py
     ...: list(db.query("select * from creatures where id = ?", [6]))
     ...:
 Out[45]: [{'id': 6, 'name': 'Blue', 'species': 'chicken', 'age': 0.9}]
 
```

## カラムの1つを別のテーブルに取り出す
現在のテーブルには、文字列を含む種族を表すカラム species がありますが、これを別のテーブルに取り出してみましょう。

これには  `table.extract()` メソッドを使用します。


```
 In [47]: # %load 20_extract.py
     ...: table.extract("species")
     ...:
 Out[47]: <Table creatures (id, name, species_id, age)>
 
```

 `db.tables` メソッドを使って、speciesという新しいテーブルを確認することができます。

```
 In [51]: db.tables
 Out[51]: [<Table species (id, species)>, <Table creatures (id, name, species_id, age)>]
 
```



```
 In [56]: # %load 21_schema_creatures.py
     ...: from pprint import pprint
     ...:
     ...: pprint(db["creatures"].schema)
     ...: pprint(list(db["creatures"].rows))
     ...:
 ('CREATE TABLE "creatures" (\n'
  '   [id] INTEGER PRIMARY KEY,\n'
  '   [name] TEXT,\n'
  '   [species_id] INTEGER,\n'
  '   [age] FLOAT,\n'
  '   FOREIGN KEY([species_id]) REFERENCES [species]([id])\n'
  ')')
 [{'age': 6.0, 'id': 1, 'name': 'Cleo', 'species_id': 1},
  {'age': 0.8, 'id': 2, 'name': 'Lila', 'species_id': 2},
  {'age': 0.8, 'id': 3, 'name': 'Bants', 'species_id': 2},
  {'age': 0.8, 'id': 4, 'name': 'Azi', 'species_id': 2},
  {'age': 0.9, 'id': 5, 'name': 'Snowy', 'species_id': 2},
  {'age': 0.9, 'id': 6, 'name': 'Blue', 'species_id': 2}]
 
```

新しい species テーブルも作成され、レコードが入力されました。


```
 In [65]: # %load 22_schema_species.py
     ...: print(db["species"].schema)
     ...: print(list(db["species"].rows))
     ...:
 CREATE TABLE [species] (
    [id] INTEGER PRIMARY KEY,
    [species] TEXT
 )
 [{'id': 1, 'species': 'dog'}, {'id': 2, 'species': 'chicken'}]
 
```

この2つのテーブルのデータを結合するには、JOIN SQLクエリを使用します。


```
 In [67]: # %load 23_join.py
     ...: list(db.query("""
     ...:     select
     ...:       creatures.id,
     ...:       creatures.name,
     ...:       creatures.age,
     ...:       species.id as species_id,
     ...:       species.species
     ...:     from creatures
     ...:       join species on creatures.species_id = species.id
     ...: """))
     ...:
 Out[67]:
 [{'id': 1, 'name': 'Cleo', 'age': 6.0, 'species_id': 1, 'species': 'dog'},
  {'id': 2, 'name': 'Lila', 'age': 0.8, 'species_id': 2, 'species': 'chicken'},
  {'id': 3, 'name': 'Bants', 'age': 0.8, 'species_id': 2, 'species': 'chicken'},
  {'id': 4, 'name': 'Azi', 'age': 0.8, 'species_id': 2, 'species': 'chicken'},
  {'id': 5, 'name': 'Snowy', 'age': 0.9, 'species_id': 2, 'species': 'chicken'},
  {'id': 6, 'name': 'Blue', 'age': 0.9, 'species_id': 2, 'species': 'chicken'}]
 
```

## コマンドラインツール

sqlite-utils にはコマンドラインツール（以降単にCLIと略します)も提供されています。
オプション `--help` を与えて実行すると、簡単な説明が表示されます。

 bash
```
 % sqlite-utils --help
 Usage: sqlite-utils [OPTIONS] COMMAND [ARGS]...
 
   Commands for interacting with a SQLite database
 
 Options:
   --version   Show the version and exit.
   -h, --help  Show this message and exit.
 
 Commands:
   query*              Execute SQL query and return the results as JSON
   add-column          Add a column to the specified table
   add-foreign-key     Add a new foreign key constraint to an existing table.
   add-foreign-keys    Add multiple new foreign key constraints to a...
   analyze-tables      Analyze the columns in one or more tables
   convert             Convert columns using Python code you supply.
   create-index        Add an index to the specified table covering the...
   create-table        Add a table with the specified columns.
   create-view         Create a view for the provided SELECT query
   disable-fts         Disable full-text search for specific table
   disable-wal         Disable WAL for database files
   drop-table          Drop the specified table
   drop-view           Drop the specified view
   dump                Output a SQL dump of the schema and full contents...
   enable-counts       Configure triggers to update a _counts table with...
   enable-fts          Enable full-text search for specific table and columns
   enable-wal          Enable WAL for database files
   extract             Extract one or more columns into a separate table
   index-foreign-keys  Ensure every foreign key column has an index on it.
   indexes             Show indexes for this database
   insert              Insert records from JSON file into a table,...
   insert-files        Insert one or more files using BLOB columns in the...
   memory              Execute SQL query against an in-memory database,...
   optimize            Optimize all full-text search tables and then run...
   populate-fts        Re-populate full-text search for specific table and...
   rebuild-fts         Rebuild all or specific full-text search tables
   reset-counts        Reset calculated counts in the _counts table
   rows                Output all rows in the specified table
   schema              Show full schema for this database or for specified...
   search              Execute a full-text search against this table
   tables              List the tables in the database
   transform           Transform a table beyond the capabilities of ALTER...
   triggers            Show triggers configured in this database
   upsert              Upsert records based on their primary key.
   vacuum              Run VACUUM against the database
   views               List the views in the database
   
```

また、各サブコマンドにも  `--help` オプションを与えると簡単な使用方法が表示されます。

 bash
```
 % sqlite-utils query --help
 Usage: sqlite-utils query [OPTIONS] PATH SQL
 
   Execute SQL query and return the results as JSON
 
 Options:
   --attach <TEXT FILE>...     Additional databases to attach - specify alias
                               and filepath
   --nl                        Output newline-delimited JSON
   --arrays                    Output rows as arrays instead of objects
   --csv                       Output CSV
   --tsv                       Output TSV
   --no-headers                Omit CSV headers
   -t, --table                 Output as a table
   --fmt TEXT                  Table format - one of fancy_grid, fancy_outline,
                               github, grid, html, jira, latex, latex_booktabs,
                               latex_longtable, latex_raw, mediawiki, moinmoin,
                               orgtbl, pipe, plain, presto, pretty, psql, rst,
                               simple, textile, tsv, unsafehtml, youtrack
   --json-cols                 Detect JSON cols and output them as JSON, not
                               escaped strings
   -r, --raw                   Raw output, first column of first row
   -p, --param <TEXT TEXT>...  Named :parameters for SQL query
   --load-extension TEXT       SQLite extensions to load
   -h, --help                  Show this message and exit.
   
```

これを見てわかるように、sqlite-utils は SQLite のほとんどすべての操作をコマンドラインから実行することができます。

これまでの例をコマンドラインから実行してみましょう。

## SQLクエリの実行
sqlite-utils の query サブコマンドを使用すると、SQLiteデータベースファイルに対して直接クエリを実行することができます。これはデフォルトのサブコマンドなので、以下の2つの例では同じように動作します。


```
 % sqlite-utils query my_data.db "select * from creatures;"
 [{"id": 1, "name": "Cleo", "species_id": 1, "age": 6.0},
  {"id": 2, "name": "Lila", "species_id": 2, "age": 0.8},
  {"id": 3, "name": "Bants", "species_id": 2, "age": 0.8},
  {"id": 4, "name": "Azi", "species_id": 2, "age": 0.8},
  {"id": 5, "name": "Snowy", "species_id": 2, "age": 0.9},
  {"id": 6, "name": "Blue", "species_id": 2, "age": 0.9}]
  
```

 bash
```
 % sqlite-utils my_data.db "select * from creatures;"
 [{"id": 1, "name": "Cleo", "species_id": 1, "age": 6.0},
  {"id": 2, "name": "Lila", "species_id": 2, "age": 0.8},
  {"id": 3, "name": "Bants", "species_id": 2, "age": 0.8},
  {"id": 4, "name": "Azi", "species_id": 2, "age": 0.8},
  {"id": 5, "name": "Snowy", "species_id": 2, "age": 0.9},
  {"id": 6, "name": "Blue", "species_id": 2, "age": 0.9}]
  
```

## データベースへの接続
上記に例でわかるように、CLIではサブコマンドにつづけてデータベースのファイル名を与えるだけです。
インメモリのデータベースを処理するためのサブコマンド memory だけは、データベースファイルを与える必要がありません。

sqlite-utils memory は sqlite-utils query とよく似た動作をしますが、インメモリデータベースに対してクエリを実行することができます。

memory サブコマンドはインメモリ・データベースに対して直接SQLを実行します。

 bash
```
 % sqlite-utils memory 'select sqlite_version()'
 [{"sqlite_version()": "3.36.0"}]
```

## テーブルの作成
CLIでテーブルを作成するためには、create-table サブコマンドを使います。

 bash
```
 % sqlite-utils create-table --help
 Usage: sqlite-utils create-table [OPTIONS] PATH TABLE COLUMNS...
 
   Add a table with the specified columns. Columns should be specified using
   name, type pairs, for example:
 
   sqlite-utils create-table my.db people \
       id integer \
       name text \
       height float \
       photo blob --pk id
 
 Options:
   --pk TEXT                 Column to use as primary key
   --not-null TEXT           Columns that should be created as NOT NULL
   --default <TEXT TEXT>...  Default value that should be set for a column
   --fk <TEXT TEXT TEXT>...  Column, other table, other column to set as a
                             foreign key
   --ignore                  If table already exists, do nothing
   --replace                 If table already exists, replace it
   --load-extension TEXT     SQLite extensions to load
   -h, --help                Show this message and exit.
   
   
```

次のスキーマをもつテーブルを作成してみます。

 SQL
```
 CREATE TABLE [creatures] (
     [name] TEXT,
     [species] TEXT,
     [age] FLOAT
  )
   
```

テーブル作成を行う方法はいくつかありますが、基本的には create_table サブコマンドで行います。

 bash
```
 # 50_create_table.sh
 sqlite-utils create-table my_data2.db creatures \
     name text    \
     species text \
     age float    
 
```

カラム名とカラムの型のペアは、いくつでも渡すことができます。有効な型は、 `integer` 、 `text` 、 `float` 、 `blob` です。

オプション `--not-null カラム名` を使うと、指定したカラムにNOT NULL制約を設定できます。 `--default カラム名 デフォルト値` を使って、カラムのデフォルト値を指定できます。

データベースにあるテーブルを tables サブコマンドで確認してみましょう。

 bash
```
 # 51_tables.sh
 sqlite-utils tables my_data2.db
 [{"table": "creatures"}]
```

オプション  `--counts` を使うと、各テーブルの行数のカウントが含まれます。

 bash
```
 # 52_table_record_count.sh
 % sqlite-utils tables my_data2.db --counts
 [{"table": "creatures", "count": 3}]
 
```

オプション  `--columns` を与えると、各テーブルにカラムのリストを含めることができます。

 bash
```
 # 53_table_columns.sh
 % sqlite-utils tables my_data2.db --columns
 [{"table": "creatures", "columns": ["name", "species", "age"]}]
```

オプション  `--schema` を与えると、テーブルのスキーマを含めることができます。

 bash
```
 # 54_tables_schema.sh
 % sqlite-utils tables my_data2.db --schema
 [{"table": "creatures", "schema": "CREATE TABLE [creatures] (\n   [name] TEXT,\n   [species] TEXT,\n   [age] FLOAT\n)"}]
 
```

## JSON データの挿入
JSON 形式のデータがあれば、sqlite-utils insert テーブル名 を使用してデータベースに挿入することができます。テーブルがまだ存在しない場合は、正しい（自動的に検出された）カラムでテーブルが作成されます。

単一のJSONオブジェクトまたはJSONオブジェクトのリストを、ファイル名として、または標準入力に直接パイプで（ファイル名に-を使用して）渡すことができます。

 bash
```
 # 55_insert_json.sh
 % cat creatures.json
 [
   { "name": "Cleo", "species": "dog", "age": 6 },
   { "name": "Lila", "species": "chicken", "age": 0.8 },
   { "name": "Bants", "species": "chicken", "age": 0.8 }
 ]
 % sqlite-utils insert my_data2.db creatures creatures.json
 % # cat creatures.json | sqlite-utils insert my_data2.db creatures - 
 
```

## テーブル内のすべてのレコードを返す
rows サブコマンドを使うと、指定したテーブルのすべての行を返すことができます。

 bash
```
 # 56_rows.sh
 % sqlite-utils rows my_data2.db creatures
 [{"name": "Cleo", "species": "dog", "age": 6.0},
  {"name": "Lila", "species": "chicken", "age": 0.8},
  {"name": "Bants", "species": "chicken", "age": 0.8}]
  
```

テーブルの内容がJSON配列で出力されます。
オプション  `--nl` を与えると、配列ではなくそれぞれのレコードが出力されます。

 bash
```
 # 57_rows_nl.sh
 % sqlite-utils rows my_data2.db creatures --nl
 {"name": "Cleo", "species": "dog", "age": 6.0}
 {"name": "Lila", "species": "chicken", "age": 0.8}
 {"name": "Bants", "species": "chicken", "age": 0.8}
 
```

Python の json モジュールを使って整形させることもできます。

 bash
```
 # 58_rows_json.sh
 % sqlite-utils rows my_data2.db creatures | python -mjson.tool
 [
     {
         "name": "Cleo",
         "species": "dog",
         "age": 6.0
     },
     {
         "name": "Lila",
         "species": "chicken",
         "age": 0.8
     },
     {
         "name": "Bants",
         "species": "chicken",
         "age": 0.8
     }
 ]
 
```


オプション  `--csv` または `--tsv` を使用すると出力をCSVおよびTSVフォーマットで出力することができます。

 bash
```
 # 59_rows_csv.sh
 % sqlite-utils rows my_data2.db creatures --csv
 name,species,age
 Cleo,dog,6.0
 Lila,chicken,0.8
 Bants,chicken,0.8
 
```

 bash
```
 # 60_rows_tsv.sh
 % sqlite-utils rows my_data2.db creatures --tsv
 name	species	age
 Cleo	dog	6.0
 Lila	chicken	0.8
 Bants	chicken	0.8
 
```


オプション  `--no-headers` を与えるとヘッダ行の出力を抑制することができます。

 bash
```
 # 61_rows_csv_noheaders.sh
 % sqlite-utils rows my_data2.db creatures --csv --no-headers
 Cleo,dog,6.0
 Lila,chicken,0.8
 Bants,chicken,0.8
 
```


## 表形式での出力
オプション  `--table` を与えると出力が表形式となります。

 bash
```
 # 62_rows_table.sh
 % sqlite-utils rows my_data2.db creatures --table
 name    species      age
 ------  ---------  -----
 Cleo    dog          6
 Lila    chicken      0.8
 Bants   chicken      0.8
 
```


オプション  `--fmt` を使うと、異なるテーブルフォーマットを指定することができます。

 bash
```
 # 63_rows_table_fmt_rst.sh
 % sqlite-utils rows my_data2.db creatures --table --fmt rst
 ======  =========  =====
 name    species      age
 ======  =========  =====
 Cleo    dog          6
 Lila    chicken      0.8
 Bants   chicken      0.8
 ======  =========  =====
 
```

 bash
```
 # 64_rows_table_fmt_grid.sh
 % sqlite-utils rows my_data2.db creatures --table --fmt grid
 +--------+-----------+-------+
 | name   | species   |   age |
 +========+===========+=======+
 | Cleo   | dog       |   6   |
 +--------+-----------+-------+
 | Lila   | chicken   |   0.8 |
 +--------+-----------+-------+
 | Bants  | chicken   |   0.8 |
 +--------+-----------+-------+
 
```

## テーブルの内容をSQLクエリで読み出す
query サブコマンドに SQLクエリを与えて、テーブルの内容を読み出してみましょう。

 bash
```
 # 65_query.sh
 % sqlite-utils query my_data2.db "select * from creatures;"
 [{"name": "Cleo", "species": "dog", "age": 6.0},
  {"name": "Lila", "species": "chicken", "age": 0.8},
  {"name": "Bants", "species": "chicken", "age": 0.8}]
  
```


## 名前付きパラメータの使用
名前付きのパラメータをクエリに渡すためには、オプション `-p` を使用します。

 bash
```
 # 66_sql_named_paramaters.sh
 % sqlite-utils query my_data2.db \
     "select * from creatures where species = :species;" \
     -p species chicken
 [{"name": "Lila", "species": "chicken", "age": 0.8},
  {"name": "Bants", "species": "chicken", "age": 0.8}]
  
```


## プライマリキー
このテーブルを作成したとき、プライマリキーを指定しませんでした。SQLiteは、他のプライマリキーが定義されていない場合、rowidというプライマリキーを自動的に作成します。

 `select rowid, * from creatures` を実行すると、この隠されたプライマリキーを見ることができます。

 bash
```
 # 67_rowid.sh
 % sqlite-utils query my_data2.db "select rowid, * from creatures;"
 [{"rowid": 1, "name": "Cleo", "species": "dog", "age": 6.0},
  {"rowid": 2, "name": "Lila", "species": "chicken", "age": 0.8},
  {"rowid": 3, "name": "Bants", "species": "chicken", "age": 0.8}]
  
```


テーブル creatures に独自のプライマリキー  `id` を設定して再作成しましょう。

drop-table サブコマンドでテーブルを削除します。

 bash
```
 # 68_drop_table.sh
 % sqlite-utils drop-table my_data2.db creatures
 
```


このテーブルを再度作成し、今度は  `id` カラムを追加します。

 `pk="id"` を使用して、 `id` カラムをテーブルのプライマリキーとして扱うことを指示します。
 bash
```
 # 69_craete_table_pk.sh
 % sqlite-utils create-table my_data2.db creatures \
     id   integer \
     name text    \
     species text \
     age float    \
     --pk="id"
```

テーブルを確認してみましょう。

 bash
```
 # 70_tables_check.py
 % sqlite-utils tables my_data2.db
 [{"table": "creatures"}]
 % sqlite-utils tables my_data2.db --schema | python -mjson.tool
 [
     {
         "table": "creatures",
         "schema": "CREATE TABLE [creatures] (\n   [id] INTEGER PRIMARY KEY,\n   [name] TEXT,\n   [species] TEXT,\n   [age] FLOAT\n)"
     }
 ]
```

 bash
```
 # 71_insert_pk_json.sh
 % cat creatures_pk.json
 [
   { "id": 1, "name": "Cleo", "species": "dog", "age": 6 },
   { "id": 2, "name": "Lila", "species": "chicken", "age": 0.8 },
   { "id": 3, "name": "Bants", "species": "chicken", "age": 0.8 }
 ]
 
 % sqlite-utils insert my_data2.db creatures creatures_pk.json
 %
```

## さらにレコードを追加
insert サブコマンドはなんども実行することができます。さらにレコードを追加してみましょう。

 bash
```
 # 72_insert_pk_more.sh
 % cat creatures_pk_more.json
 [
  { "id": 4, "name": "Azi", "species": "chicken", "age": 0.8 },
  { "id": 5, "name": "Snowy", "species": "chicken", "age": 0.9 }
 ]
 % sqlite-utils insert my_data2.db creatures creatures_pk_more.json
 %
```


 bash
```
 # 73_rows.sh
 % sqlite-utils rows my_data2.db creatures
 [{"id": 1, "name": "Cleo", "species": "dog", "age": 6.0},
  {"id": 2, "name": "Lila", "species": "chicken", "age": 0.8},
  {"id": 3, "name": "Bants", "species": "chicken", "age": 0.8},
  {"id": 4, "name": "Azi", "species": "chicken", "age": 0.8},
  {"id": 5, "name": "Snowy", "species": "chicken", "age": 0.9}]
  
```

レコードを１つ追加するときも、insert サブコマンドで処理できます。

 bash
```
 # 74_insert_one.sh
 % echo '{"id": 6, "name": "Red", "species": "chicken", "age": 0.9}' | \
       sqlite-utils insert my_data2.db creatures -
```

標準入力からJSONを読み取るときは、sqlite-utils のコマンドラインでファイル名の部分にマイナス記号( `-` ) を与えます。

 `id` カラムにはプライマリキーが設定されているため、UNIQUE制約があるため、
既存のIDで新しいレコードを追加しようとすると、次のようなエラーとなります。

 bash
```
 # 75_insert_duplicate_id.sh
 % echo '{"id": 6, "name": "Red", "species": "chicken", "age": 0.9}' | sqlite-utils insert my_data2.db creatures -
 Error: UNIQUE constraint failed: creatures.id
 
 sql = INSERT INTO [creatures] ([age], [id], [name], [species]) VALUES (?, ?, ?, ?);
 parameters = [0.9, 6, 'Red', 'chicken']
 
 %
 
```

オプション  `--replace` を与えると、該当するIDのレコードを新しいレコードに置き換えることができます。

 bash
```
 # 76_insert_duplicate_id_replace.sh
 % echo '{"id": 6, "name": "Red", "species": "chicken", "age": 0.9}' | \
     sqlite-utils insert my_data2.db creatures - --replace
 %
 
```

 bash
```
 # 77_rows.sh
 % sqlite-utils rows my_data2.db creatures
 [{"id": 1, "name": "Cleo", "species": "dog", "age": 6.0},
  {"id": 2, "name": "Lila", "species": "chicken", "age": 0.8},
  {"id": 3, "name": "Bants", "species": "chicken", "age": 0.8},
  {"id": 4, "name": "Azi", "species": "chicken", "age": 0.8},
  {"id": 5, "name": "Snowy", "species": "chicken", "age": 0.9},
  {"id": 6, "name": "Red", "species": "chicken", "age": 0.9}]
  
```

## レコードの更新
sqlite-utils の Pythn ライブラリでは  `update()` がありますが、CLIでは query サブコマンドを用いて SQLコマンドのUPDATEを使用します。

 bash
```
 # 78_update_record.sh
 % sqlite-utils query my_data2.db "update creatures set name = :name where id=6;" -p name blue
 [{"rows_affected": 1}]
 
 % sqlite-utils rows my_data2.db creatures
 [{"id": 1, "name": "Cleo", "species": "dog", "age": 6.0},
  {"id": 2, "name": "Lila", "species": "chicken", "age": 0.8},
  {"id": 3, "name": "Bants", "species": "chicken", "age": 0.8},
  {"id": 4, "name": "Azi", "species": "chicken", "age": 0.8},
  {"id": 5, "name": "Snowy", "species": "chicken", "age": 0.9},
  {"id": 6, "name": "blue", "species": "chicken", "age": 0.9}]
  
```


## カラムの1つを別のテーブルに取り出す
現在のテーブルには、文字列を含む種族を表すカラム species がありますが、これを別のテーブルに取り出してみましょう。

 bash
```
 # 79_extract.sh
 % sqlite-utils extract my_data2.db creatures species
 %
```

これで カラム species のデータが取り出されて species テーブルが作成されてレコードが挿入されています。

 bash
```
 # 80_table_check.sh
 % sqlite-utils tables my_data2.db
  [{"table": "species"},
   {"table": "creatures"}]
 
 % sqlite-utils tables my_data2.db --schema | python -mjson.tool
 [
     {
         "table": "species",
         "schema": "CREATE TABLE [species] (\n   [id] INTEGER PRIMARY KEY,\n   [species] TEXT\n)"
     },
     {
         "table": "creatures",
         "schema": "CREATE TABLE \"creatures\" (\n   [id] INTEGER PRIMARY KEY,\n   [name] TEXT,\n   [species_id] INTEGER,\n   [age] FLOAT,\n   FOREIGN KEY([species_id]) REFERENCES [species]([id])\n)"
     }
 ]
 
 % sqlite-utils rows my_data2.db species
  [{"id": 1, "species": "dog"},
   {"id": 2, "species": "chicken"}]
  
```

この２つのテーブルを結合するためには、JOIN SQLクエリを使用します。

 bash
```
 # 81_query_join.sh
 sqlite-utils query my_data2.db """
 select
    creatures.id,
    creatures.name,
    creatures.age,
    species.id as species_id,
    species.species
    from creatures
  join species on creatures.species_id = species.id;
  """
 [{"id": 1, "name": "Cleo", "age": 6.0, "species_id": 1, "species": "dog"},
  {"id": 2, "name": "Lila", "age": 0.8, "species_id": 2, "species": "chicken"},
  {"id": 3, "name": "Bants", "age": 0.8, "species_id": 2, "species": "chicken"},
  {"id": 4, "name": "Azi", "age": 0.8, "species_id": 2, "species": "chicken"},
  {"id": 5, "name": "Snowy", "age": 0.9, "species_id": 2, "species": "chicken"},
  {"id": 6, "name": "blue", "age": 0.9, "species_id": 2, "species": "chicken"}]
  
```

## CLIだけで使える便利な機能
sqlite-utils memoryコマンドはsqlite-utils queryと似た動作をしますが、インメモリデータベースに対してクエリを実行することができます。

このコマンドにCSVファイルやJSONファイルを渡すと、一時的なインメモリテーブルに読み込まれ、データをSQLiteに変換する別のステップを経ることなく、そのデータに対してSQLを実行することができます。


## CSV または JSON に対して直接クエリを実行
CSVやJSON形式のデータがあれば、インメモリのSQLiteデータベースにロードして、sqlite-utils memory を使って、次のように1つのコマンドで直接クエリを実行することができます。

 bash
```
 # 82_memory_csv.sh
 % cat stockcat stock.csv
 cat: stockcat: No such file or directory
 date,trans,symbol,qty,price
 2020-03-06,BUY,GOOG,200.0,1298.41
 2020-03-09,BUY,AAPL,100.0,288.06
 
 % sqlite-utils memory stock.csv "select * from stock;"
 [{"date": "2020-03-06", "trans": "BUY", "symbol": "GOOG", "qty": 200.0, "price": 1298.41},
  {"date": "2020-03-09", "trans": "BUY", "symbol": "AAPL", "qty": 100.0, "price": 288.06}]
  
```

sqlite-utils queryと同じ出力フォーマットオプションをすべて受付ます。 ( `-tsv` 、 `--csv` 、  `--table` 、  `--nl` )

 bash
```
 % sqlite-utils memory stock.csv "select * from stock;" --table --fmt grid
 +------------+---------+----------+-------+---------+
 | date       | trans   | symbol   |   qty |   price |
 +============+=========+==========+=======+=========+
 | 2020-03-06 | BUY     | GOOG     |   200 | 1298.41 |
 +------------+---------+----------+-------+---------+
 | 2020-03-09 | BUY     | AAPL     |   100 |  288.06 |
 +------------+---------+----------+-------+---------+
 
```

コストは少し高いですが、CSVファイルを表形式に簡単に変換できるわけです。

異なるファイルのデータ間で結合を実行したい場合は、コマンドに複数のファイルを渡すことができます。

 bash
```
 # 83_memory_different_format.sh
 % cat creatures.csv
 id,name,species_id,age
 1,Cleo,1,6.0
 2,Lila,2,0.8
 3,Bants,2,0.8
 4,Azi,2,0.8
 5,Snowy,2,0.9
 6,blue,2,0.9
 
 % cat species.json
 [{"id": 1, "species": "dog"},
  {"id": 2, "species": "chicken"}]
 
 % sqlite-utils memory creatures.csv species.json \
     "select * from creatures join species on creatures.id = species.id"
 [{"id": 1, "name": "Cleo", "species_id": 1, "age": 6.0, "species": "dog"},
  {"id": 2, "name": "Lila", "species_id": 2, "age": 0.8, "species": "chicken"}]
```

## データベースをバックアップ
SQLite ではデータベースは単一のファイルで構成されるため、ただ単にコピーをすることでバックアップができますが、スキーマーレベルでバックアップしたいときや、SQLite　から MySQL など他のデータベースシステムにポーティングするような場合は、dumpサブコマンドを使ってバックアップを行うことができますｌ．

 bash
```
 % sqlite-utils dump my_data2.db
 BEGIN TRANSACTION;
 CREATE TABLE "creatures" (
    [id] INTEGER PRIMARY KEY,
    [name] TEXT,
    [species_id] INTEGER,
    [age] FLOAT,
    FOREIGN KEY([species_id]) REFERENCES [species]([id])
 );
 INSERT INTO "creatures" VALUES(1,'Cleo',1,6.0);
 INSERT INTO "creatures" VALUES(2,'Lila',2,0.8);
 INSERT INTO "creatures" VALUES(3,'Bants',2,0.8);
 INSERT INTO "creatures" VALUES(4,'Azi',2,0.8);
 INSERT INTO "creatures" VALUES(5,'Snowy',2,0.9);
 INSERT INTO "creatures" VALUES(6,'blue',2,0.9);
 CREATE TABLE [species] (
    [id] INTEGER PRIMARY KEY,
    [species] TEXT
 );
 INSERT INTO "species" VALUES(1,'dog');
 INSERT INTO "species" VALUES(2,'chicken');
 CREATE UNIQUE INDEX [idx_species_species]
     ON [species] ([species]);
 COMMIT;
 
```

## まとめ

sqlite-utils を使うことで、SQLite データベースをより簡単に’操作できるようになります。知っておいて損はない便利なツールです。



## 参考資料
- [sqlite-utils ソースコード ](https://github.com/simonw/sqlite-utils)
- [sqlite-utils 公式ドキュメント ](https://sqlite-utils.datasette.io/en/stable/)
- [sqlite-utilsを使ってみよう(Pythonライブラリ)]
- [sqlite-utilsを使ってみよう(コマンドライン)]

#database
#SQLite


