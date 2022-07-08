Alembicでマイグレーションをしてみよう
=================

## Alembic について
Alembicは、SQLAlchemy の開発者である Mike Bayer 氏が、SQLAlchemy のためのマイグレーションツールとして開発されたものです。
Alembic という単語は、もともとアニメーションやVFXに用いられるコンピュータ・グラフィックスのためのファイル交換形式として知られています。Google などで検索するようなときはDatabase や Migration などの単語と組み合わせてください。

## インストールと準備

通常 Alembic は対象のプロジェクトと同じモジュール内、同じ Python パスにインストールされます。

 bash
```
 $ pip install alembic
```

これで  `alembic` コマンドが使えるようになります。
 bash
```
 $ alembic --help
 usage: alembic [-h] [-c CONFIG] [-n NAME] [-x X] [--raiseerr]
                {branches,current,downgrade,edit,heads,history,init,list_templates,merge,revision,show,stamp,upgrade}
                ...
 
 positional arguments:
   {branches,current,downgrade,edit,heads,history,init,list_templates,merge,revision,show,stamp,upgrade}
     branches            Show current branch points.
     current             Display the current revision for a database.
     downgrade           Revert to a previous version.
     edit                Edit revision script(s) using $EDITOR.
     heads               Show current available heads in the script directory.
     history             List changeset scripts in chronological order.
     init                Initialize a new scripts directory.
     list_templates      List available templates.
     merge               Merge two revisions together. Creates a new migration
                         file.
     revision            Create a new revision file.
     show                Show the revision(s) denoted by the given symbol.
     stamp               'stamp' the revision table with the given revision;
                         don't run any migrations.
     upgrade             Upgrade to a later version.
 
 optional arguments:
   -h, --help            show this help message and exit
   -c CONFIG, --config CONFIG
                         Alternate config file; defaults to value of
                         ALEMBIC_CONFIG environment variable, or "alembic.ini"
   -n NAME, --name NAME  Name of section in .ini file to use for Alembic config
   -x X                  Additional arguments consumed by custom env.py
                         scripts, e.g. -x setting1=somesetting -x
                         setting2=somesetting
   --raiseerr            Raise a full stack trace on error
```

 `init` サブコマンドで初期化します。
 bash
```
 $ alembic init -h
 usage: alembic init [-h] [-t TEMPLATE] [--package] directory
 
 positional arguments:
   directory             location of scripts directory
 
 optional arguments:
   -h, --help            show this help message and exit
   -t TEMPLATE, --template TEMPLATE
                         Setup template for use with 'init'
   --package             Write empty __init__.py files to the environment and
                         version locations
```
 `init` サブコマンドにはテンプレートを指定することができます。
テンプレートは `list_templates` サブコマンドで知ることができます。

 bash
```
 $ alembic list_templates 
 Available templates:
 
 multidb - Rudimentary multi-database configuration.
 pylons - Configuration that reads from a Pylons project environment.
 generic - Generic single-database configuration.
 
 Templates are used via the 'init' command, e.g.:
 
   alembic init --template generic ./scripts
```

 `--template` オプションが省略されたときは "generic" が与えられたものとして動作します。



引数はマイグレーションレポジトリのディレクトリ名を与えます。
 bash
```
 $ ls
 test.db
 $ alembic init migrations
 $ ls
 migrations		alembic.ini
 $ ls -CF migrations
 README		env.py		script.py.mako	versions/
```


### initサブコマンドで生成されるもの
- env.py
alembic のツールが起動する度に読み込まれる Python モジュール
SQLAlchemy の Engine を設定や生成を行って、 migration が実行できるようにカスタマイズする

- README.md
どのような環境で migration 環境を作成したか記述されている

- script.py.mako
新しい migration のスクリプトを生成するために使用される Mako テンプレートファイル
ここにあるものは何でも version/内の新しいファイルを生成するために使用される

- versions ディレクトリ
migration スクリプトが保存されるディレクトリ

- alembic.ini
alembic のスクリプトが実行される度に読まれる構成ファイル

 `alembic.init` にある、 `sqlalchemy.url` にSQLAlchemy が接続するためのURLを、実行する環境に応じて修正します。

```
 sqlalchemy.url = sqlite:///test.db
```

 `SQLAlchemy.url` を環境変数などから取得する必要がある場合や、マイグレーションで複数のデータベースのURLを使用する場合は、 `env.py` ファイルで設定するようにします。

## マイグレーションスクリプトを自動生成
"[SQLAlchemyを使ってみよう]" では作成したモデルクラスは次のようなものでした。
 models.py
```
 from sqlalchemy import create_engine
 from sqlalchemy.ext.declarative import declarative_base
 from sqlalchemy import Column, Integer, String
 
 engine = create_engine('sqlite:///test.db')
 Base = declarative_base()
 
 class User(Base):
     __tablename__ = 'users'
     id = Column(Integer, primary_key=True)
     name = Column(String)
     fullname = Column(String)
     nickname = Column(String)
 
     def __repr__(self):
        return "<User('name={}', fullname={}, nickname={})>".format(
                      self.name, self.fullname, self.nickname)
 
```

alembic の環境設定ファイル( `env.py` ) の `target_metadata` を修正します。
アプリケーションのモデルクラスの  `Base.metada` を設定します。

```
 from models import Base
 target_metadata = Base.metadata
```

もし複数のモデルクラスを参照する必要があれば、次のように設定します。

```
 from myapp.mymodel1 import Model1Base
 from myapp.mymodel2 import Model2Base
 target_metadata = [Model1Base.metadata, Model2Base.metadata]
```

準備はこれで終わりです。

## マイグレーションスクリプトの生成
 `revison` サブコマンドを使ってマイグレーションスクリプトを生成させます。
 `--autogenerate` オプションを与えると、マイグレーション環境ファイル( `env.py` ) にある、 `targert_metadata` からデータベースを検知して、その内容とモデルクラスを比較してデータベースに反映するためのマイグレーションファイルを自動生成することができます。

 bash
```
 $ PYTHONPATH=. alembic revision --autogenerate -m "Initial"
 INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
 INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
 INFO  [alembic.autogenerate.compare] Detected added table 'users'
   Generating /Users/goichiiisaka/Downloads/Python.Osaka/PractiveClass/Alembic/migrat
   ions/versions/87e5f182b361_initial.py ...  done
  
```

 bash
```
 $ ls migrations/versions/
 __pycache__		87e5f182b361_initial.py
```

### マイグレーションスクリプト

 `versions/` 以下のディレクトリに  `revision` サブコマンドで指定したメッセージとレビジョンIDから構成されるファイル名のマイグレーションスクリプトが作成されます。
今回はデータベース  `test.db` が存在していなかったので、
次のようにテーブル作成処理が自動生成されています。


```
 """Initial
 
 Revision ID: 87e5f182b361
 Revises:
 Create Date: 2020-04-26 08:11:21.272965
 
 """
 from alembic import op
 import sqlalchemy as sa
 
 
 # revision identifiers, used by Alembic.
 revision = '87e5f182b361'
 down_revision = None
 branch_labels = None
 depends_on = None
 
 def upgrade():
     # ### commands auto generated by Alembic - please adjust! ###
     op.create_table('users',
     sa.Column('id', sa.Integer(), nullable=False),
     sa.Column('name', sa.String(), nullable=True),
     sa.Column('fullname', sa.String(), nullable=True),
     sa.Column('nickname', sa.String(), nullable=True),
     sa.PrimaryKeyConstraint('id')
     )
     # ### end Alembic commands ###
 
 def downgrade():
     # ### commands auto generated by Alembic - please adjust! ###
     op.drop_table('users')
     # ### end Alembic commands ###
```

重要なのは、このファイルにある、 `revision` と  `down_revision` の２つの変数です
alembic はマイグレーションのアップグレード/ダウングレードを行うとき、 `versions` ディレクトリにあるすべてのマイグレーションスクリプトを参照して、この２つの変数の関係を把握します。そして  `down_revison` が  `None` になっている最初のマイグレーションスクリプトファイルを認識します。

関数 `upgrade()` と  `dwongrade()` はそれぞれアップグレード、ダウングレードが実行されたときに呼び出されるものです。
 `op.create_table()` と  `op.drop_tables()` は alembic のマイグレーション操作のディレクティブです。

### 現在のレビジョンの確認
 `history` サブコマンドでレビジョンの履歴を参照することができます。
 bash
```
 $ alembic history
 <base> -> 87e5f182b361 (head), Initial
```

ここまでの作業で、データベース に `users` テーブルと、マイグレーション管理のための  `alembic_version` テーブルが作成されます。
 bash
```
 $ sqlite3 test.db
 SQLite version 3.31.1 2020-01-27 19:55:54
 Enter ".help" for usage hints.
 sqlite> select * from sqlite_master;
 table|alembic_version|alembic_version|2|CREATE TABLE alembic_version (
 	version_num VARCHAR(32) NOT NULL, 
 	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
 )
 index|sqlite_autoindex_alembic_version_1|alembic_version|3|
 table|users|users|4|CREATE TABLE users (
 	id INTEGER NOT NULL, 
 	name VARCHAR(32) NOT NULL, 
 	fullname VARCHAR(128), 
 	nickname VARCHAR(32), 
 	PRIMARY KEY (id)
 )
 sqlite> ^D
 
```

このあとマイグレーションされたことを alembic に登録しておきます。

 bash
```
 $ PYTHONPATH=. alembic stamp head
 INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
 INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
 INFO  [alembic.runtime.migration] Running stamp_revision  -> 87e5f182b361
```

alembic の  `revision` サブコマンドでマイグレーションスクリプトの生成したときは、
 `upgrade` サブコマンドを実行してデータベースをマイグレーションする必要があります。
アプリケーション側で  `Base.metadata.create_all()` を実行してデータベースに反映ずみのたときは、 `stamp` サブコマンドを実行してマイグレーション済みなことを登録する必要が’あります。

### レコードの追加
アプリケーション側で、テーブル `users` にユーザを追加しておきましょう。
 add_users.py
```
 from models import session, User
 
 userList=[
   User(name='wendy', fullname='Wendy Williams', nickname='windy'),
   User(name='mary', fullname='Mary Contrary', nickname='mary'),
   User(name='fred', fullname='Fred Flintstone', nickname='freddy')
 ]
 
 session.add_all(userList)
 session.commit()
```

 bash
```
 $ python add_users.py
 $ sqlite3 test.db 
 SQLite version 3.31.1 2020-01-27 19:55:54
 Enter ".help" for usage hints.
 sqlite> select * from users;
 1|wendy|Wendy Williams|windy
 2|mary|Mary Contrary|mary
 3|fred|Fred Flintstone|freddy
 sqlite> ^D
 
```

### スキームを変更
ここで、モデルクラスを修正して、データベースのテーブル `users` に `password` カラムを追加してみましょう。

```
 from sqlalchemy import create_engine
 from sqlalchemy.ext.declarative import declarative_base
 from sqlalchemy import Column, Integer, String
 
 engine = create_engine('sqlite:///test.db')
 Base = declarative_base()
 
 class User(Base):
     __tablename__ = 'users'
     id = Column(Integer, primary_key=True)
     name = Column(String)
     password = Column(String)
     fullname = Column(String)
     nickname = Column(String)
 
     def __repr__(self):
        return "<User('name={}', fullname={}, nickname={})>".format(
                      self.name, self.fullname, self.nickname)
 
```

 bash
```
 $ PYTHONPATH=. alembic history
 <base> -> 87e5f182b361 (head), Initial
```

 bash
```
 $ PYTHONPATH=. alembic revision --autogenerate -m "Add password field"
 INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
 INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
 INFO  [alembic.autogenerate.compare] Detected added column 'users.password'
   Generating /Users/goichiiisaka/Downloads/Python.Osaka/PractiveClass/Alembic/migrat
   ions/versions/f8264676c887_add_password_field.py ...  done
```

新しいマイグレーションスクリプトが作成されました。
 bash
```
 $ ls migrations/versions/
 87e5f182b361_initial.py			f8264676c887_add_password_field.py
 __pycache__
 
```


```
 """Add password field
 
 Revision ID: f8264676c887
 Revises: 87e5f182b361
 Create Date: 2020-04-27 11:31:50.462764
 
 """
 from alembic import op
 import sqlalchemy as sa
 
 
 # revision identifiers, used by Alembic.
 revision = 'f8264676c887'
 down_revision = '87e5f182b361'
 branch_labels = None
 depends_on = None
 
 
 def upgrade():
     # ### commands auto generated by Alembic - please adjust! ###
     op.add_column('users', sa.Column('password', sa.String(), nullable=True))
     # ### end Alembic commands ###
 
 
 def downgrade():
     # ### commands auto generated by Alembic - please adjust! ###
     op.drop_column('users', 'password')
     # ### end Alembic commands ###
```

 `op.add_column()` と  `op.drop_column()` はカラム追加のためのディレクティブです。

マイグレーションの履歴を確認してみましょう。
 bash
```
 $ PYTHONPATH=. alembic history
 87e5f182b361 -> f8264676c887 (head), Add password field
 <base> -> 87e5f182b361, Initial
```

 `upgrade` サブコマンドにレビジョンIDを与えるとその状態までデータベースがアップグレードされます。 レビジョンIDがに変えて  `head` を与えると最新の状態になります。

 bash
```
 $ PYTHONPATH=. alembic upgrade head
 INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
 INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
 INFO  [alembic.runtime.migration] Running upgrade 87e5f182b361 -> f8264676c887, Add password field
 
```

これでデータベースに反映されます。
 SQL
```
 sqlite> .schema users
 CREATE TABLE users (
 	id INTEGER NOT NULL, 
 	name VARCHAR, 
 	fullname VARCHAR, 
 	nickname VARCHAR, password VARCHAR, 
 	PRIMARY KEY (id)
 );
```

## データベースをダウングレード
 `downgrade` サブコマンドにレビジョンIDを与えるとその状態までデータベースがダウングレードされます。 レビジョンIDに変えて  `base` を与えると最初の状態まで戻ります。

ただし、今回のケースでは次のようにエラーになってしまいます。
 basg
```
 $ PYTHONPATH=. alembic downgrade 87e5f182b361
 INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
 INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
 INFO  [alembic.runtime.migration] Running downgrade f8264676c887 -> 87e5f182b361, Add password field
     :
     :
 sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) near "DROP": syntax error
 [SQL: ALTER TABLE users DROP COLUMN password]
 (Background on this error at: http://sqlalche.me/e/e3q8)
 
```

これは、SQLite3 の  `ALTER TABLE` は[カラム削除やリネームには対応していない ](https://www.sqlite.org/lang_altertable.html) ことが原因です。

SQLite3 で カラム削除を行うためには次の手順が必要となります。

- 新しいスキームのテーブルのコピーを作成
- 既存のテーブルから新しいテーブルにデータを転送
- 古いテーブルを削除

Alembicはこの処理を行うための バッチ操作コンテキスト( `BatchOperationConext` )を提供しています。


```
 with op.batch_alter_table("some_table") as batch_op:
     batch_op.add_column(Column('foo', Integer))
     batch_op.drop_column('bar')
```

上記のディレクティブがマイグレーションスクリプトで呼び出されると、バックエンドのSQLite3 では次のようなSQLが実行されます。
 SQL
```
 CREATE TABLE _alembic_batch_temp (
   id INTEGER NOT NULL,
   foo INTEGER,
   PRIMARY KEY (id)
 );
 INSERT INTO _alembic_batch_temp (id) SELECT some_table.id FROM some_table;
 DROP TABLE some_table;
 ALTER TABLE _alembic_batch_temp RENAME TO some_table;
```

これをふまえて、マイグレーションスクリプトの  `drowngrade()` を次のように修正します。


```
 def downgrade():
      with op.batch_alter_table("users") as batch_op:
           batch_op.drop_column('password')
      
```

もう一度、ダウングレードしてみましょう。
 bash
```
 $ PYTHONPATH=. alembic downgrade 87e5f182b361
 INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
 INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
 INFO  [alembic.runtime.migration] Running downgrade f8264676c887 -> 87e5f182b361, Add password field
 
```

確認してみましょう。 `password` カラムが削除されていますが、データはそのまま残っています。
 bash
```
 $ sqlite3 test.db 
 SQLite version 3.31.1 2020-01-27 19:55:54
 Enter ".help" for usage hints.
 sqlite> .schema users
 CREATE TABLE IF NOT EXISTS "users" (
 	id INTEGER NOT NULL, 
 	name VARCHAR, 
 	fullname VARCHAR, 
 	nickname VARCHAR, 
 	PRIMARY KEY (id)
 );
 sqlite> select * from users;
 1|wendy|Wendy Williams|windy
 2|mary|Mary Contrary|mary
 3|fred|Fred Flintstone|freddy
 sqlite> ^D
 
```

## Alembicの自動検出
#### 自動検出できるパターン
 `revision --autogenerate` で自動検出できるパターンは次の通りです。

- テーブルの追加・削除
- カラムの追加・削除
- カラムの nullable 状態の変更
- インデックスおよび明示的な名前付きユニーク制約の基本的な変更
- 外部キー制約の基本的な変更

#### オプションで自動検出できるパターン
マイグレーション環境ファイル( `env.py` ) を修正して有効にします。
- カラムの種類（型）の変更
  -  `EnvironmentContext.configure.compare_type = True` 
- サーバデフォルトの変更
  -  `EnvironmentContext.configure.compare_server_default = True` 

カラムの型の変更を検出するようにすると、バックエンドのデータベースエンジンによっては、問題となることがあります。
例えば、MySQLでは、Boolean型 はtinyint型 で設定されますが、alembic は比較する際に型が違うものと判断してしまい、該当するカラムを毎回削除して作成することを繰り返してしまいます。
また tinyint から integer に型を変えたときもうまく検出できません。

####  自動検出できないパターン
- テーブル名の変更
- カラム名の変更
- 名前の付いていないユニーク制約
- データベースが直接サポートしていない特殊な SQLAlchemy の型を使う場合

データベースバックエンドがデフォルト値として設定するものを、誤検知せずに正しく処理することは難しいことを理解するべきでしょう。

## まとめ
Alembic を利用することで、データベース・マイグレーションでの作業ミスが軽減できることが期待できます。
また、なによりその作業工数を削減することができることは非常に有益です。


## 参考
- [Alembic オフィシャルサイト ](https://alembic.sqlalchemy.org/en/latest/)
- [SQLAlchmey オフィシャルサイト ](https://www.sqlalchemy.org/)
- [SQLite オフィシャルサイト ](https://www.sqlite.org/index.html)

#database
#migration


