pyodbcを使ったODBCデータベースとの連携
=================

## データベース
Pythonでは多くのデータベースをサポートしていて、これはつまり開発者に人気がある言語であることを示す、数多くの特徴の1つです。MySQL、Oracle、PostgreSQL、Informixなどの汎用データベースシステムをサポートしているだけでなく、SQLiteやThinkSQLのような埋め込みデータベースや、Neo4Jのようなグラフデータベースもサポートしています。

オープンソースで開発されて、広く利用されているデータベースは本当にたくさんあります。
ここでは、次の３つについて紹介することにします。

- SQLite：
- MySQL / MariaDB；
- PostgreSQL：

## SQLite
Python で利用できるデータベースとしては、SQLiteは最も簡単なデータベースです。 Python からは `sqlite3` を利用しますが、これは標準モジュールとして取り込まれているため、データベースと接続するために外部のPython モジュールをインストールする必要がありません。SQLiteデータベースは、データをファイルに読み書きするため、サーバーレスで自己完結しています。つまり、MySQLやPostgreSQLなどとは異なり、データベース操作を行うためのSQLiteサーバーをインストールして設定を行い、サービスを起動するといった作業は不要です。

ここでは、sqlite3を使ってPythonでSQLiteデータベースに接続するためには次のように行います。

```
 import sqlite3
 connection = sqlite3.connect('/tmp/sample.sqlite')
```

実際には、 `connect()` に与えたファイルへのアクセスに失敗するような場合は例外が発生するため、次のようにすることが一般的です。

```
 import sqlite3
 from sqlite3 import Error

 def create_connection(path):
     connection = None
     try:
         connection = sqlite3.connect(path)
         print("Connection to SQLite DB successful")
     except Error as e:
         print(f"The error '{e}' occurred")

     return connection

```
　connection = create_connection("/tmp/sample.sqlite")


## MySQL
SQLite とは異なり、MySQL データベースへの接続に使用できる Python 標準モジュールはありません。MySQL 用の Python SQL ドライバをインストールする必要があります。そのようなドライバの一つが  `mysql-connector-python` です。この Python SQL モジュールは pip でダウンロードできます。
MySQL の派生バージョンに MariaDB が存在します。MySQLがOrace社に買収されたとき、オリジナルの開発者が非商業版ソースコードから派生させたもので、MySQLとほぼ互換のものです。RedHatやGoogleなどは MariaDB を採用しているなど実績を積み上げています。

 bash
```
 $ pip install mysql-connector-python
```

 `mysql-connector-python` を使っててPythonでMySQLデータベースに接続するためには次のように行います。

```
 import mysql.connector

 connection = mysql.connector.connect(
              host=host_name,
              user=user_name,
              passwd=user_password
          )
```

ここでも、接続に失敗した場合の例外に対応するためには次のようにすることが一般的です。

```
 import mysql.connector
 from mysql.connector import Error

 def create_connection(host_name, user_name, user_password):
     connection = None
     try:
         connection = mysql.connector.connect(
             host=host_name,
             user=user_name,
             passwd=user_password
         )
         print("Connection to MySQL DB successful")
     except Error as e:
         print(f"The error '{e}' occurred")

     return connection

 connection = create_connection("localhost", "root", "")
```

また、上記のスクリプトでは、関数  `create_connection()` を定義しています。
 `mysql.connector` にはMySQL データベースサーバに接続するために使用するメソッド  `connect()` があります。接続が確立されると、接続オブジェクトが呼び出した関数に返されます。
ここまでは、接続を確立しただけです。データベースはまだ作成されていません。

ここで注意するべきことは、MySQLはサーバーベースの**データベース管理システム(DBMS: Database Management System)**であることです。MySQLデータベースでは1つのサーバーで複数のデータベースを持つことができます。データベースを作成すること接続を作成することが同じであるSQLiteとは異なり、MySQLデータベースはデータベース作成のための2つのステップがあります。

- MySQLサーバーへの接続を行う。
- クエリを実行してデータベースを作成する（必要があれば)。

データベースの作成では次のようなコードになります。

```
 def create_database(connection, query):
     cursor = connection.cursor()
     try:
         cursor.execute(query)
         print("Database created successfully")
     except Error as e:
         print(f"The error '{e}' occurred")

 create_database(connection, 'CREATE DATABASE sample')
```

これで、MySQLデータベースサーバにデータベース  `sample` が作成されます。しかし、 `create_connection()` が返す接続オブジェクトは、MySQLデータベースサーバーに接続されていることを思い出してください。データベース  `sample` に接続する必要があります。そのためには、 `create_connection()` を修正してデータベースを指示するようにします。


```
 def create_connection(host_name, user_name, user_password, db_name):
     connection = None
     try:
         connection = mysql.connector.connect(
             host=host_name,
             user=user_name,
             passwd=user_password,
             database=db_name                     # ここに注目
         )
         print("Connection to MySQL DB successful")
     except Error as e:
         print(f"The error '{e}' occurred")

     return connection
```

以後は次のようにMySQLデータベースに接続することができます。

```
 connection = create_connection(host="localhost", user="root", passwd="", database="sample")
```

## PostgreSQL
MySQL と同様に、PostgreSQL データベースと接続するためのPython 標準ライブラリはありません。サードパーティの Python SQL ドライバをインストールする必要があります。そのような PostgreSQL 用 Python SQL ドライバにはいくつかありますが、代表的なものが  `psycopg2` です。

 bash
```
 $ pip install psycopg2
```

SQLiteや MySQLと同じように  `connect()` を呼び出してデータベースと接続します。

```
 import psycopg2
 connection = psycopg2.connect(
              database=db_name,
              user=db_user,
              password=db_password,
              host=db_host,
              port=db_port,
          )
```

これも実際には接続エラーで発生する例外に対処するために次のようなコードにするのが一般的です。

```
 import psycopg2
 from psycopg2 import OperationalError

 def create_connection(db_name, db_user, db_password, db_host, db_port):
     connection = None
     try:
         connection = psycopg2.connect(
             database=db_name,
             user=db_user,
             password=db_password,
             host=db_host,
             port=db_port,
         )
         print("Connection to PostgreSQL DB successful")
     except OperationalError as e:
         print(f"The error '{e}' occurred")
     return connection
```

次に、create_connection()を使用して、PostgreSQLデータベースへの接続を作成します。まず、以下の文字列を使用して、デフォルトのデータベースである `postgres` への接続を行います。


```
 connection = create_connection(
     "postgres", "postgres", "abc123", "127.0.0.1", "5432"
 )
```

PostgreSQLがインストールされている環境によっては、ユーザ名やパスワード、ホスト、ポート番号などが変更されている場合があります。
MySQL のときと同様にクエリを実行してデータベースを作成します。（もちろん必要があればです）

```
 def create_database(connection, query):
     connection.autocommit = True
     cursor = connection.cursor()
     try:
         cursor.execute(query)
         print("Query executed successfully")
     except OperationalError as e:
         print(f"The error '{e}' occurred")

 create_database(connection, "CREATE DATABASE sample")
```

以後は次のコードでデータベース  `sample` に接続することができます。

```
 connection = create_connection(
     "sample", "postgres", "abc123", "127.0.0.1", "5432"
 )
```

## ユーザとアクセス権限
MySQLとPostgreSQLではアクセスするユーザ情報を管理することができ、アクセスすることができるデータベースやクエリの実行できる権限を設定することができます。例えば、読み出し専用のユーザなどを設定することができます。

## SQLについて
ここまでの例で、データベースを作成するためにクエリとい文を実行していました。
データベースに接続したあと、データの操作や定義を行うためのデータベース言語を**SQL**と言います。
クエリとはこのSQL文のことです。SQLの標準化に時間がかかったことから、多くのデータベースシステムが独自に拡張をしていったために、多くの方言のようなものが存在することになりました。

## pyodbc について
ODBC は、データベース管理システム (DBMS) にアクセスするプログラムを、特定の DBMS 設計に依存しないようにするための、業界標準のアプリケーション・プログラム・インターフェース (API) です。pyodbc は ODBC データベースへのアクセスを提供するオープンソースの Python モジュールで、Python DB API 2.0 仕様を実装しています。

Python DB API はリレーショナルデータベースに格納されたデータへのデータベースに依存しないインターフェースを定義しています。Python DB は適合モジュールが異なるデータベース製品に対して一貫したインターフェースを提供できるように設計されています。これは開発者がデータベース間で移植可能な Python アプリケーションを書くのに役立ちます。

Python には MySQLに接続するための  `mysql-connector-python` や、PostgreSQL に接続するための  `psycopg2` など、データベースライブラリが存在していますが、 `pydobc` を使ってODBCドライバを経由することで、Linux や Unix 上の Python を Microsoft SQL Server, Oracle®, DB2, Microsoft Access, Sybase ASE, InterBase などのリモートデータベースに接続することができるようになります。

## インストール
pyodbc のインストールは次のような手順です。
 bash
```
 $ pip install pyodbc
```

pyodbcを使用するには、PythonがインストールされているマシンにODBCドライバをインストールする必要があります。

## ODBCドライバ

#### Ubuntu の場合
 bash
```
 $sudo apt-get install unixODBC unixODBC-dev
```

#### RedHatの場合
 bash
```
 $sudo dnf install unixODBC unixODBC-devel
```

登録済みのデータベースを参照する
 bash
```
 $ odbcinst -q -d
 CData ODBC Driver for MySQL
 ...
```

登録済みのデータソースを参照する
 bash
```
 $ odbcinst -q -s
 CData MySQL Source
 ...
```


お使いのPythonとデータベースのプラットフォームに対応したODBCドライバをダウンロードします。ドライバによっては登録が必要なものもあります。

- MySQL： [mysql-connector-odbc ](https://dev.mysql.com/downloads/file/?id=396575)
- PostgreSQL： [PostgreSQL ODBC driver (psqlODBC) ](https://www.postgresql.org/ftp/odbc/versions/)
- Microsoft SQLServer：[ODBC Driver for SQL Server ](https://docs.microsoft.com/ja-jp/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15)

etc/odbc.iniにあるいは  `$HOME/.odbc.init` 、アクセスしたいデータベースに接続するODBCデータソースを作成します。例えば、この SQL Server ODBC データソースは、Northwind データベースを提供する SQL Server Express インスタンスに接続します。

## ODBCドライバの設定
ドライバの定義を  `/etc/odbcinst.ini` に記述します。
  /etc/odbcinst.ini
```
 [PostgreSQL]
 Description     = ODBC for PostgreSQL
 Driver          = /usr/lib/psqlodbcw.so
 Setup           = /usr/lib/libodbcpsqlS.so
 Driver64        = /usr/lib64/psqlodbcw.so
 Setup64         = /usr/lib64/libodbcpsqlS.so
 FileUsage       = 1

 [MySQL]
 Description     = ODBC for MySQL
 Driver          = /usr/lib/libmyodbc5.so
 Setup           = /usr/lib/libodbcmyS.so
 Driver64        = /usr/lib64/libmyodbc5.so
 Setup64         = /usr/lib64/libodbcmyS.so
 FileUsage       = 1

 [SQL Server]
 Driver=/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.4.so.2.1
 UsageCount=1
```

この例では、３つのデータベースシステムを登録していますが、もちろん１つだけ登録するだけでも問題ありません。また、Driver64 他で指定しているシェアードライブラリのパスはインストールされている データベースシステムやバージョンによって異なることに留意してください。


データソースは  `/etc/odbc.ini` または、ユーザ毎の  `$HOME/.odbc.ini` に記述します。
こちらも定義されているデータベース名などは、データベースの運用環境に依存することに留意してください。
 /etc/odbc.ini
```
 [PostgreSQL_DS1]
 Description         = PostgreSQL Datasource 1
 Driver              = PostgreSQL
 Database            = db1
 Servername          = dbhost.example.com
 Port                = 5432
 Protocol            = 7.4-2
 CommLog             = 0
 Debug               = 0

 [MySQL]
 Driver = MySQL
 Database = mysql
 Server = localhost
 Socket = /var/lib/mysql/mysql.sock
 User = <username>
 Password = <password>

 [MSSQL]
 Driver         = MSSQL Driver
 Server         = <host>,<port>
 Database       = <database>
```



## 接続テスト
unixODBC に付属する  `isql` コマンドを使うと簡単に接続テストすることができます。

 bash
```
 $ isql PostgreSQL_DS1 dbuser pass
 +---------------------------------------+
 | Connected!                            |
 |                                       |
 | sql-statement                         |
 | help [tablename]                      |
 | quit                                  |
 |                                       |
 +---------------------------------------+
 SQL> SELECT id FROM t1 ;
 +------------+
 | id         |
 +------------+
 | 1          |
 | 2          |
 | 3          |
 +------------+
 SQLRowCount returns 3
 3 rows fetched
 SQL> quit
 $

```


## pyodbc の使用方法

DRIVERには  `/etc/odbcinst.ini` で定義したセクション名を与えます。

```
 import pyodbc

 cnn_postgres = pyodbc.connect(
     'DRIVER=PostgreSQL;UID=ユーザ;PWD=パスワード;DATABASE=データベース;SERVER=ホスト;')
 cnn_mysql = pyodbc.connect(
     'DRIVER=MySQL;UID=ユーザ;PWD=パスワード;DATABASE=データベース;SERVER=ホスト;')
 cnn_sqlserfer = pyodbc.connect(
      'DRIVER=SQL Server;UID=ユーザ;PWD=パスワード;DATABASE=データベース;SERVER=ホスト;')
```


## まとめ
ここで、説明したような データベースによって異なるPython SQL ドライバを利用することはできるだけ避けたほうが好ましいと考えています。
理由の一つには、将来の拡張性や運用時に柔軟性が挙げられます。特定のデータベースシステムに依存したコードをハードコーディングしてしまうと、将来アプリケーションを機能拡張するような場合に、非常に困難になることがあります。
pyodbc を使ってODBC経由でデータベースシステムにアクセスすることで、コードの汎用性と運用時の柔軟性が増すことになります。



## 参考資料
- [SQLite オフィシャルサイト ](https://www.sqlite.org/index.html)
- [MySQL オフィシャルサイト ](https://www.mysql.com/jp/)
- [日本PostgreSQLユーザ会 ](https://www.postgresql.jp/)
- [pyodbc ソースコード　](https://github.com/mkleehammer/pyodbc/wiki)
- Wikipedia - [SQL ](https://ja.wikipedia.org/wiki/SQL)
- Wikipedia - [MariaDB ](https://ja.wikipedia.org/wiki/MariaDB)
- [Introduction to Python SQL Libraries ](https://realpython.com/python-sql-libraries/)

