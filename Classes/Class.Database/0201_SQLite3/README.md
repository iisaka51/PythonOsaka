SQLite3を使ってみよう
=================
![](https://gyazo.com/68736de6f6d25d8a04b1766aa7fa2258.png)

## SQLite3 について
SQLite3 は、軽量なディスク上のデータベースです。サーバプロセスを用意する必要がなく、 SQL クエリー言語とは完全互換ではないものの、SQLを使用してデータベースにアクセスできます。

SQLite3 を使ってアプリケーションのプロトタイプを作り、その後そのコードをMySQLや PostgreSQL、Oracle といった大規模データベースに移植するということも可能です。

 `sqlite3` モジュールは [PEP 249 ](https://www.python.org/dev/peps/pep-0249/) で記述されている DB-API 2.0 に準拠した SQL インターフェイスが提供されています。

ここではSQLite3 を使ってSQLの基本操作を理解しましょう。

## SQLite3 の使用方法
はじめに、データベースへの接続をして `Connection` オブジェクトを生成します。
このコネクションオブジェクトから `Cursor` オブジェクトを生成します。

```
 In [2]: # %load 01_connection.py
    ...: import sqlite3
    ...:
    ...: conn = sqlite3.connect('example.sqlite')
    ...: c = conn.cursor()
    ...:
    ...: c.execute("""CREATE TABLE stocks
    ...:             (date text, trans text, symbol text, qty real, price real)""
    ...: ")
    ...: c.execute("""INSERT INTO stocks VALUES
    ...:              ('2020-03-06','BUY','GOOG',200,1298.41)""")
    ...: c.execute("""INSERT INTO stocks VALUES
    ...:              ('2020-03-09','BUY','AAPL',100,288.06)""")
    ...:
    ...: conn.commit()
    ...: conn.close()
    ...:
```

 `Cursor` オブジェクトにある  `execute()` メソッドを使用して SQL文を実行して、
データベースとの入出力を行います。
データベースへ行った変更は  `commit()` メソッドを呼び出すことで反映され、
 `close()` で データベースとのコネクションが削除されます。

 `sqlite3.connect(':memory:')` とすると、メモリ上のデータベースと接続します。
永続性はなくなりこととデータ量の制限は’ありますが、性能向上が期待できます。

次回以降のセッションでも、データベースへの接続をして内容を読み出すことができます。


```
 In [2]: # %load 02_select.py
    ...: import sqlite3
    ...:
    ...: conn = sqlite3.connect('example.sqlite')
    ...: c = conn.cursor()
    ...:
    ...: symbol='AAPL'
    ...: c.execute("SELECT * FROM  stocks WHERE symbol = '%s'" % symbol)
    ...: data = c.fetchone()
    ...:
    ...: conn.commit()
    ...: conn.close()
    ...:
    ...: # print(data)
    ...:
 
 In [3]: print(data)
 ('2020-03-09', 'BUY', 'AAPL', 100.0, 288.06)
```

## CREATE
先の例では、データベース  `example.sql3` にテーブル  `stocks` を作成しています。
テーブル `stocks` には、次のカラムが作成されています。

 TABLE stocks のカラム

| カラム名 | カラム型名 |
|:--|:--|
| date | text |
| trans | text |
| symbol | text |
| qty | real |
| price | real |

SQLite3 で指定できるカタム型名は、次の５種類のいずれかをセットすることができます。
デフォルトのカラム型は  `none` です。
 SQLite3 カラム型

| カラム型名 | データ型 | 意味 |
|:--|:--|:--|
| TEXT | str | テキスト, char(6)とすると６文字の文字列 |
| INTERGER | int | 符号付き整数 |
| REAL | float | 浮動小数点 |
| NUMERIC | binary | 入力データをそのまま格納 |
| NONE | none | NULL値 |


## INSERT

データベースを作成したときに使用した `INSERT` 文のようにデータをひとつずつ追加するだけでなく、データをリストにして、それを流し込むようにデータを追加することもできます。


```
 In [2]: # %load 03_insert.py
    ...: import sqlite3
    ...:
    ...: conn = sqlite3.connect('example.sqlite')
    ...: c = conn.cursor()
    ...: stock_data = [
    ...:                ('2020-03-05','BUY','HPE',80,11.99),
    ...:                ('2020-03-04','BUY','MSFT',160,161.57)
    ...:              ]
    ...: c.executemany("insert into stocks values (?,?,?,?,?)", stock_data)
    ...: conn.commit()
    ...: conn.close()
    ...:
 
```

## SELECT
ここまでで、４つのデータが  `example.sqlite` にあるはずです。
これを読み出すためには  `SELECT` 文を使います。
データは、 `fetchone()` 、 `fetchall()` 、もしくはイテレータとして読み出します。

```
 In [2]: # %load 04_fetch.py
    ...: import sqlite3
    ...: from pprint import pprint
    ...:
    ...: conn = sqlite3.connect('example.sqlite')
    ...: c = conn.cursor()
    ...:
    ...: c.execute("SELECT * FROM stocks")
    ...: v1 = c.fetchone()
    ...: v2 = c.fetchone()
    ...:
    ...: c.execute("SELECT * FROM stocks")
    ...: v3 = c.fetchall()
    ...:
    ...: conn.commit()
    ...: conn.close()
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...: # pprint(v3)
    ...:
 
 In [3]: pprint(v1)
 ('2020-03-06', 'BUY', 'GOOG', 100.0, 1298.41)
 
 In [4]: pprint(v2)
 ('2020-03-09', 'BUY', 'AAPL', 100.0, 288.06)
 
 In [5]: pprint(v3)
 [('2020-03-06', 'BUY', 'GOOG', 100.0, 1298.41),
  ('2020-03-09', 'BUY', 'AAPL', 100.0, 288.06),
  ('2020-03-05', 'BUY', 'HPE', 100.0, 11.99),
  ('2020-03-04', 'BUY', 'MSFT', 100.0, 161.57)]
  
```


```
 In [2]: # %load 05_iterate.py
    ...: import sqlite3
    ...: from pprint import pprint
    ...:
    ...: conn = sqlite3.connect('example.sqlite')
    ...: c = conn.cursor()
    ...:
    ...: def func():
    ...:     val = list()
    ...:     for row in c.execute("SELECT * FROM stocks"):
    ...:         val.append(row)
    ...:     return val
    ...:
    ...: v1 = func()
    ...:
    ...: conn.commit()
    ...: conn.close()
    ...:
    ...: # pprint(v1)
    ...:
 
 In [3]: pprint(v1)
 [('2020-03-06', 'BUY', 'GOOG', 100.0, 1298.41),
  ('2020-03-09', 'BUY', 'AAPL', 100.0, 288.06),
  ('2020-03-05', 'BUY', 'HPE', 100.0, 11.99),
  ('2020-03-04', 'BUY', 'MSFT', 100.0, 161.57)]
 
```

### WHERE
SELECT文のWHERE句を記述するとそれに合致するデータを抽出します。
 SQL
```
 SELECT カラム名, ... FROM テーブル名 WHERE カラム名 = 'データ';
```


```
 In [2]: # %load 06_where.py
    ...: import sqlite3
    ...: from pprint import pprint
    ...:
    ...: conn = sqlite3.connect('example.sqlite')
    ...: c = conn.cursor()
    ...:
    ...: c.execute("SELECT * FROM  stocks")
    ...: v1 = c.fetchall()
    ...:
    ...: c.execute("SELECT * FROM  stocks WHERE symbol='AAPL'")
    ...: v2 = c.fetchall()
    ...:
    ...: conn.commit()
    ...: conn.close()
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...:
 
 In [3]: pprint(v1)
 [('2020-03-06', 'BUY', 'GOOG', 100.0, 1298.41),
  ('2020-03-09', 'BUY', 'AAPL', 100.0, 288.06),
  ('2020-03-05', 'BUY', 'HPE', 100.0, 11.99),
  ('2020-03-04', 'BUY', 'MSFT', 100.0, 161.57)]
 
 In [4]: pprint(v2)
 [('2020-03-09', 'BUY', 'AAPL', 100.0, 288.06)]
 
```

### WHERE ... LIKE
パターン検索を行いたいときは  `LIKE` 句を使います。大文字小文字の区別はありません。
次のワイルドカードを使用することができます。
- パーセント記号( `%` ) ： 任意の0文字以上の文字列
　アンダースコア( `_` ) ：  任意の1文字
 SQL
```
 SELECT カラム名, ... FROM テーブル名 WHERE カラム名 LIKE = 'パターン';
```


```
 In [2]: # %load 07_like.py
    ...: import sqlite3
    ...: from pprint import pprint
    ...:
    ...: conn = sqlite3.connect('example.sqlite')
    ...: c = conn.cursor()
    ...:
    ...: c.execute("SELECT * FROM  stocks")
    ...: v1 = c.fetchall()
    ...:
    ...: c.execute("SELECT * FROM  stocks WHERE symbol LIKE '%PL'")
    ...: v2 = c.fetchall()
    ...:
    ...: conn.commit()
    ...: conn.close()
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...:
 
 In [3]: pprint(v1)
 [('2020-03-06', 'BUY', 'GOOG', 100.0, 1298.41),
  ('2020-03-09', 'BUY', 'AAPL', 100.0, 288.06),
  ('2020-03-05', 'BUY', 'HPE', 100.0, 11.99),
  ('2020-03-04', 'BUY', 'MSFT', 100.0, 161.57)]
 
 In [4]: pprint(v2)
 [('2020-03-09', 'BUY', 'AAPL', 100.0, 288.06)]
 
```
### WHERE ... IN
指定したカラムの値がIN句で指定した値に合致するデータを抽出します。
 SQL
```
 SELECT カラム名 , ... FROM テーブル名 WHERE カラム名 IN ('VAL1', 'VAL2', ...);
```



```
 In [2]: # %load 08_where_in.py
    ...: import sqlite3
    ...: from pprint import pprint
    ...:
    ...: conn = sqlite3.connect('example.sqlite')
    ...: c = conn.cursor()
    ...:
    ...: c.execute("SELECT * FROM  stocks")
    ...: v1 = c.fetchall()
    ...:
    ...: c.execute("SELECT * FROM  stocks WHERE symbol IN ('HPE', 'MSFT')")
    ...: v2 = c.fetchall()
    ...:
    ...: conn.commit()
    ...: conn.close()
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...:
 
 In [3]: pprint(v1)
 [('2020-03-06', 'BUY', 'GOOG', 100.0, 1298.41),
  ('2020-03-09', 'BUY', 'AAPL', 100.0, 288.06),
  ('2020-03-05', 'BUY', 'HPE', 100.0, 11.99),
  ('2020-03-04', 'BUY', 'MSFT', 100.0, 161.57)]
 
 In [4]: pprint(v2)
 [('2020-03-05', 'BUY', 'HPE', 100.0, 11.99),
  ('2020-03-04', 'BUY', 'MSFT', 100.0, 161.57)]
 
```

### ORDER BY
 `ORDER BY` 句で指定したカラムで昇順( `ASC` )/降順( `DESC` ) でソートします。
 `[ASC|DESC]` は `ASC` か `DESC` が指定でき、省略も可能という意味の表記です。
省略した場合は `ASC` が与えられたものとして動作します。
 SQL
```
 SELECT カラム名 , ... FROM テーブル名 ORDER BY カラム名 [ASC | DESC];
```


```
 In [2]: # %load 09_orderby.py
    ...: import sqlite3
    ...: from pprint import pprint
    ...:
    ...: conn = sqlite3.connect('example.sqlite')
    ...: c = conn.cursor()
    ...:
    ...: c.execute("SELECT * FROM stocks")
    ...: v1 = c.fetchall()
    ...:
    ...: c.execute("SELECT * FROM stocks ORDER BY symbol ASC")
    ...: v2 = c.fetchall()
    ...:
    ...: conn.commit()
    ...: conn.close()
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...:
 
 In [3]: pprint(v1)
 [('2020-03-06', 'BUY', 'GOOG', 100.0, 1298.41),
  ('2020-03-09', 'BUY', 'AAPL', 100.0, 288.06),
  ('2020-03-05', 'BUY', 'HPE', 100.0, 11.99),
  ('2020-03-04', 'BUY', 'MSFT', 100.0, 161.57)]
 
 In [4]: pprint(v2)
 [('2020-03-09', 'BUY', 'AAPL', 100.0, 288.06),
  ('2020-03-06', 'BUY', 'GOOG', 100.0, 1298.41),
  ('2020-03-05', 'BUY', 'HPE', 100.0, 11.99),
  ('2020-03-04', 'BUY', 'MSFT', 100.0, 161.57)]
 
```

パーセント記号( `%` ) と アンダースコア( `_` ) はSQL文では特殊文字となりますが、
これらを単に文字として使用したいときには、 `ESCAPE` でエスケープ文字を指定して、処理をする必要があります。例えばエスケープ文字がドル記号( `$` ）とすれば、パーセント記号の表記は  `$%` となります。

 SQL
```
 SELECT カラム名 , ... FROM テーブル名
   WHERE カラム LIKE パターン ESCAPE エスケープ文字;
```

 `BETWEEN` 句で２つの値の間に含まれているものを抽出します。
 SQL
```
 SELECT カラム名 , ... FROM テーブル名 WHERE カラム BETWEEN 値1 AND 値2;
```


```
 In [2]: # %load 09_between.py
    ...: import sqlite3
    ...: from pprint import pprint
    ...:
    ...: conn = sqlite3.connect('example.sqlite')
    ...: c = conn.cursor()
    ...:
    ...: c.execute("SELECT * FROM stocks")
    ...: v1 = c.fetchall()
    ...:
    ...: c.execute("SELECT * from stocks WHERE price BETWEEN 100 AND 400")
    ...: v2 = c.fetchall()
    ...:
    ...: c.execute("SELECT * from stocks WHERE price >= 100 AND price <= 400")
    ...: v3 = c.fetchall()
    ...:
    ...: conn.commit()
    ...: conn.close()
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...: # pprint(v3)
    ...:
 
 In [3]: pprint(v1)
 [('2020-03-06', 'BUY', 'GOOG', 100.0, 1298.41),
  ('2020-03-09', 'BUY', 'AAPL', 100.0, 288.06),
  ('2020-03-05', 'BUY', 'HPE', 100.0, 11.99),
  ('2020-03-04', 'BUY', 'MSFT', 100.0, 161.57)]
 
 In [4]: pprint(v2)
 [('2020-03-09', 'BUY', 'AAPL', 100.0, 288.06),
  ('2020-03-04', 'BUY', 'MSFT', 100.0, 161.57)]
 
 In [5]: pprint(v3)
 [('2020-03-09', 'BUY', 'AAPL', 100.0, 288.06),
  ('2020-03-04', 'BUY', 'MSFT', 100.0, 161.57)]
 
```

## DELETE
 `DELETE` 文は `WHERE` 句に合致するデータを削除します。
 `WHERE` 句を省略するとそのテーブルの**全てのデータが削除**されます。
 SQL
```
 DELETE FROM テーブル名 WHERE 条件式;
```


```
 In [2]: # %load 11_delete.py
    ...: import sqlite3
    ...: from pprint import pprint
    ...:
    ...: conn = sqlite3.connect('example.sqlite')
    ...: c = conn.cursor()
    ...:
    ...: c.execute("SELECT * FROM  stocks")
    ...: v1 = c.fetchall()
    ...:
    ...: c.execute("DELETE FROM  stocks WHERE symbol IN ('HPE', 'MSFT')")
    ...: c.execute("SELECT * FROM  stocks")
    ...: v2 = c.fetchall()
    ...:
    ...: conn.commit()
    ...: conn.close()
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...: # %run 03_insert.py
    ...:
 
 In [3]: pprint(v1)
 [('2020-03-06', 'BUY', 'GOOG', 100.0, 1298.41),
  ('2020-03-09', 'BUY', 'AAPL', 100.0, 288.06),
  ('2020-03-05', 'BUY', 'HPE', 100.0, 11.99),
  ('2020-03-04', 'BUY', 'MSFT', 100.0, 161.57)]
 
 In [4]: pprint(v2)
 [('2020-03-06', 'BUY', 'GOOG', 100.0, 1298.41),
  ('2020-03-09', 'BUY', 'AAPL', 100.0, 288.06)]
 
 In [5]: %run 03_insert.py
 
```

## UPDATE
 `UPDATE` 文は `WHERE` 句に合致するデータを指定したデータで置き換えます。
 `WHERE` 句を省略するとそのテーブルの**全てのデータが更新**されます。
 SQL
```
 UPDATE テーブル名 SET カラム名1 = 値1, カラム名2 = 値2, ... WHERE 条件式;
```


```
 In [2]: # %load 12_update.py
    ...: import sqlite3
    ...: from pprint import pprint
    ...:
    ...: conn = sqlite3.connect('example.sqlite')
    ...: c = conn.cursor()
    ...:
    ...: c.execute("SELECT * FROM stocks")
    ...: v1 = c.fetchall()
    ...: c.execute("UPDATE stocks SET trans = 'SELL' WHERE symbol = 'HPE'")
    ...: c.execute("SELECT * FROM stocks")
    ...: v2 = c.fetchall()
    ...:
    ...: c.execute("UPDATE stocks SET trans = 'SELL'")
    ...: c.execute("SELECT * FROM stocks")
    ...: v3 = c.fetchall()
    ...:
    ...: conn.commit()
    ...: conn.close()
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...: # pprint(v3)
    ...:
 
 In [3]: pprint(v1)
 [('2020-03-06', 'BUY', 'GOOG', 100.0, 1298.41),
  ('2020-03-09', 'BUY', 'AAPL', 100.0, 288.06),
  ('2020-03-05', 'BUY', 'HPE', 100.0, 11.99),
  ('2020-03-04', 'BUY', 'MSFT', 100.0, 161.57)]
 
 In [4]: pprint(v2)
 [('2020-03-06', 'BUY', 'GOOG', 100.0, 1298.41),
  ('2020-03-09', 'BUY', 'AAPL', 100.0, 288.06),
  ('2020-03-05', 'SELL', 'HPE', 100.0, 11.99),
  ('2020-03-04', 'BUY', 'MSFT', 100.0, 161.57)]
 
 In [5]: pprint(v3)
 [('2020-03-06', 'SELL', 'GOOG', 100.0, 1298.41),
  ('2020-03-09', 'SELL', 'AAPL', 100.0, 288.06),
  ('2020-03-05', 'SELL', 'HPE', 100.0, 11.99),
  ('2020-03-04', 'SELL', 'MSFT', 100.0, 161.57)]
 
```

## ALTER
 `ALTER` 文は作成済みのテーブルの名前の変更やカラムを追加することができます。
### テーブル名の変更
 SQL
```
 ALTER TABLE テーブル名 RENAME TO 新テーブル名;
```

### カラムの追加
 SQL
```
 ALTER TABLE テーブル名 ADD COLUMN カラム名[ データ型];
```
 `[データ型]` は省略可能という意味の表記です。

SQLite3 では  `ALTER TABLE` で[カラム名の変更やカラム削除ができない ](https://www.sqlite.org/lang_altertable.html) ことに注意してください。


## DROP
 `DROP` 文は指定したテーブルを削除します。
 SQL
```
 DROP TABLE テーブル名;
```

SQLite3ではデータベースごとにファイルに格納されるため、
標準SQLにある `DROP DATABASE` は SQLite3 では使えません。
データベースを削除するためには、格納されているファイルを削除します。
同様に、データベースのバックアップはファイルをコピーするだけです。


```
 In [2]: # %load 09_drop_database.py
    ...: import sqlite3
    ...:
    ...: conn = sqlite3.connect('example.sqlite')
    ...: conn.deleteDatabase('example.sqlite')
    ...: conn.close()
    ...:
    ...:
    ...:
 ---------------------------------------------------------------------------
 AttributeError                            Traceback (most recent call last)
 <ipython-input-2-34d73b3e9398> in <module>
       3
       4 conn = sqlite3.connect('example.sqlite')
 ----> 5 conn.deleteDatabase('example.sqlite')
       6 conn.close()
       7
 
 AttributeError: 'sqlite3.Connection' object has no attribute 'deleteDatabase'
 
```

### テーブル名を知りたい
データベースに存在しているテーブル名を知るためには次のようにSQL文を実行します。
 SQL
```
 SELECT name FROM sqlite_master WHERE type='table';
```


```
 In [2]: # %load 10_showtables.py
    ...: import sqlite3
    ...:
    ...: conn = sqlite3.connect('example.sqlite')
    ...: c = conn.cursor()
    ...:
    ...: c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    ...: data = c.fetchall()
    ...: print(data)
    ...:
    ...: conn.commit()
    ...: conn.close()
    ...:
 [('stocks',)]
 
```

 `sqlite3` コマンドを実行して `.tables` を入力してもテーブル名を知ることができます。
 bash
```
 $ sqlite3 example.sqlite
 SQLite version 3.31.1 2020-01-27 19:55:54
 Enter ".help" for usage hints.
 sqlite> .tables
 stocks
 sqlite> 
 sqlite> ^D
 
```

## テーブルのカラム名を知りたい
SELECT文でデータベースにアクセスした状態であれば、 `Cursor` オブジェクトの  `description` にカラム名が格納されます。

```
 In [2]: # %load 11_description.py
    ...: import sqlite3
    ...: from pprint import pprint
    ...:
    ...: conn = sqlite3.connect('example.sqlite')
    ...: c = conn.cursor()
    ...: print(c.description)
    ...:
    ...: symbol='AAPL'
    ...: c.execute("SELECT * from  stocks where symbol = '%s'" % symbol)
    ...:
    ...: for desc in c.description:
    ...:     pprint(desc[0])
    ...:
    ...: conn.commit()
    ...: conn.close()
    ...:
 None
 'date'
 'trans'
 'symbol'
 'qty'
 'price'
```

## テーブルスキームを知りたい
テーブルスキームとは `CREATE` 文で定義されたテーブル構造のことを言います。
SQLite3 では次のようにするとテーブルスキームを知ることができます。
 SQL
```
 SELECT * FROM sqlite_master WHERE type='table' and name='テーブル名';
```


```
 In [2]: # %load 12_table_schema.py
    ...: import sqlite3
    ...: from pprint import pprint
    ...:
    ...: conn = sqlite3.connect('example.sqlite')
    ...: c = conn.cursor()
    ...:
    ...: c.execute("SELECT * FROM sqlite_master WHERE type='table' and name='stoc
    ...: ks';")
    ...: data = c.fetchall()
    ...: pprint(data)
    ...:
    ...: conn.commit()
    ...: conn.close()
    ...:
    ...:
 [('table',
   'stocks',
   'stocks',
   2,
   'CREATE TABLE stocks\n'
   '            (date text, trans text, symbol text, qty real, price real)')]
 
```


 `sqlite3` コマンドを実行して `.schema テーブル名` を入力してもテーブルスキームを知ることができます。
 bash
```
 $ sqlite3 example.sqlite
 SQLite version 3.31.1 2020-01-27 19:55:54
 Enter ".help" for usage hints.
 sqlite> .schema stocks
 CREATE TABLE stocks
             (date text, trans text, symbol text, qty real, price real);
 sqlite> 
 
```

この他にSQLite3には、 `sum()` や `avg()` などのSQL関数、抽出データのグルーピング、
ビューと呼ばれる仮想テーブルといった多彩な機能があります。

## 参考
- [Python 公式ドキュメント SQLite3 ](https://docs.python.org/ja/3/library/sqlite3.html)
- [ PEP 249 - Python Database API Specification v2.0 ](https://www.python.org/dev/peps/pep-0249/)
- [SQLite3 オフィシャルサイト ](https://www.sqlite.org/index.html)
- [SQLite Tutorial ](https://www.sqlitetutorial.net/)

previous: [ZODBを使ってみよう]
next: [pyodbcを使ったODBCデータベースとの連携]
#Pythonセミナーデータベース編


