SQLAlchemyを使ってみよう
=================
![](https://gyazo.com/328cdc85d2a936706e8b47f5dd92df2a.png)

## SQLAlchemyについて
ORMが内部で行っていることは、高レベルの操作をデータベースコマンド（SQL)に変換することです。このため、ORMを使用すると、アプリケーションはテーブルやSQLではなく、クラス、オブジェクト、メソッドなどでデータベースにアクセスすることができます。 

SQLAlchemyは、 DB-API 2.0 に準拠した SQL インターフェイスが提供されています。
また、MySQL、PostgreSQL、SQLiteなど、多数のデータベースをサポートしていて、これが人気の高さの理由のひとつにあげられます。また、開発段階では、サーバーを必要としないシンプルなSQLiteデータベースを使用して、アプリケーションを本番サーバーにデプロイするときは、より堅牢なMySQLまたはPostgreSQLサーバーを利用することができるようになります。

> 余談:
> SQL は日本では単純にエス・キュー・エルと発音しますが、欧米ではほとんどの場合、
> シークェル（ 'sequel' ）と発音されます。
> これは、SQLが1970年代はじめにIBM社によって開発されたとき、
> “SEQUEL (Structured English Query Language)”と名前を定義したことによります。
> その後、名前が "SQL (Structured Query Language)" に変えられたのですが、
> もとの発音が主流のまま使われ続けています。
> SQLAlchemy は シークェルクミー('sequel-(ar)quemie' のように発音されます。
> SQLite はシークェル・ライ (ト) ('sequelite') と発音されていることもありますが、
> こればかりは聞き取りが比較的難しくなるためか、
> エスキュー・ライ(ト)（ 'essque-lite' ） と発音されることが多いようです。
> ちなみに MySQL はマイ・エス・キュー・エル（'My Ess Que Ell’）と発音されます。
> 参考：  [S.Q.L or Sequel: How to Pronounce SQL? ](https://www.vertabelo.com/blog/sql-or-sequel/)

## インストールと準備

 bash
```
 $ pip install sqlalchemy sqlalchemy-utils
```


## SQLAlchemy ORMの使い方

SQLAlcheny の公式ドキュメントからORMの部分について説明していきます。

### データベースへの接続
SQLAlchemy を使うときは、まずはじめにデータベースへ接続します。
 `create_engine` をインポートします。

```
 from sqlalchemy import create_engine
```

基本的には、 `データベース+ドライバ://...` "書式で構成される文字列を**DSN(Data Source Name)**として `create_engine()` に与えます。
引数に  `echo=True` を与えるとアクセスログが表示されるようになります。
ドライバも複数あるのでここでは一例となります。

 メモリ上のSQLite3 データベースに接続するDSN
```
 DSN='sqlite:///:memory:'
```

 SQLite3 データベースに接続するDSN
```
 DSN="sqlite://test.db"
```

 サポートしているデータベース

| データベース | URL |
|:--|:--|
| SQLite | sqlite://storage.db |
| MySQL | mysql://user:password@host:port/dbname |
| PostgreSQL | postgresql+psycopg2://user:password@host:port/dbname |
| Microsoft SQL Server | mssql+pyodbc://user:password@host:port/dbname |
| Oracle | oracle://user:password@Iosth:port/dbname |
サードパーティーのモジュールを使うことで、もっと多くのデータベースに接続することができます。

データベースエンジンを作成します。
 IPython
```
 In [3]: # %load 01_connect.py 
    ...: from sqlalchemy import create_engine 
    ...: engine = create_engine('sqlite:///test.db') 
    ...:                                                                           
```

### モデルクラスをマッピング
ORMではテーブルを**モデル(Model)**、あるいは**モデルクラス(Model Class)** と呼びます。
宣言ベースクラス `declarative_base` から**抽象クラス(Abstract Class)** を作成します。
モデルクラスはこれを継承して定義します。
 IPython
```
 In [5]: # %load 02_declaretive_mapping.py 
    ...: from sqlalchemy.ext.declarative import declarative_base 
    ...: Base = declarative_base() 
 
 IPython
```
 In [6]: # %load 03_models.py 
    ...: from sqlalchemy import Column, Integer, String 
    ...:  
    ...: class User(Base): 
    ...:     __tablename__ = 'users' 
    ...:     id = Column(Integer, primary_key=True) 
    ...:     name = Column(String) 
    ...:     fullname = Column(String) 
    ...:     nickname = Column(String) 
    ...:  
    ...:     def __repr__(self): 
    ...:        return "<User('name={}', fullname={}, nickname={})>".format( 
    ...:                      self.name, self.fullname, self.nickname) 
    ...:  
   
```
テーブル名は、アトリビュート `__tablename__` で定義することができます。
これが無いときはクラス名から自動生成されます。例えば、クラス名が  `UserTable` だった場合は、テーブル名は `user_table` となります。

 `__table__` アトリビュートを参照するとモデルクラスの定義内容を知ることができます。
 IPython
```
 In [8]: User.__table__                                                            
 Out[8]: Table('users', MetaData(bind=None), Column('id', Integer(), table=<users>, primary_key=True, nullable=False), Column('name', String(), table=<users>), Column('fullname', String(), table=<users>), Column('nickname', String(), table=<users>), schema=None)
```

 `create_all()` を呼び出すとデータベースにテーブルが作成されます。
 Ipython
```
 In [9]: Base.metadata.create_all(engine)                                         
```

### セッションの作成
はじめに `create_engine()` で作成したデータベースエンジンへの `Session` オブジェクトを作ります。
 IPytohn
```
 In [17]: # %load 04_create_session.py 
     ...: from sqlalchemy.orm import sessionmaker 
     ...: Session = sessionmaker(bind=engine) 
     ...:                                                                          
```

まだ、データベースエンジンを作成していないときは次のように `Session` を作成します。

```
 Session = sessionmaker()
```
このあと、 `create_engine()` でデータベースエンジンを作成してから、 `Session` に登録します。

```
 Session.configure(bind=engine) 
```

 `Session` をインスタンス化します。
以後は、この  `session` エンティティーを使ってデータベースにアクセスします。
 IPython
```
 In [23]: session = Session()
```

モデルクラス `User` のインスタンスオブジェクトを作成します。
Ipython
```
 In [13]: # %load 05_create_object_user.py 
     ...: ed_user = User(name='ed', 
     ...:                fullname='Ed Jones', 
     ...:                nickname='edsnickname') 
     ...:  
 In [14]: ed_user.name
 Out[14]: 'ed'
 
 In [15]: ed_user.nickname
 Out[15]: 'edsnickname'
 
 In [16]: str(ed_user.id)
 Out[16]: 'None'
 
```
この時点では  `id` フィールドには値が設定されていません。

### データベースへの反映
 `add()` メソッドを使ってオブジェクトを追加します。
 IPython
```
 In [17]: session.add(ed_user) 
```

追加したオブジェクトは  `query()` を使って取得することができます。
 IPython
```
 In [26]: users = session.query(User) 
 In [27]: users
 Out[27]: <sqlalchemy.orm.query.Query at 0x103337a90>
 
 In [28]: print(users)
 SELECT users.id AS users_id, users.name AS users_name, users.fullname AS users_fullname, users.nickname AS users_nickname 
 FROM users
 
```
 `Query` オブジェクトはSQL文を保持しています。

 Ipython
```
 In [24]: ed.name 
 Out[24]: 'ed'
 
 In [25]: ed.nickname 
 Out[25]: 'edsnickname'
 
 In [26]: ed.id
 Out[26]: 1
 
```
 `add()` で追加すると `id` フィールドの値が自動的に設定されます。
モデル  `User` の定義を思い出してほしいのですが、 `id` フィールドには  `primary_key=True` が設定されて、このフィールドが**主キー(Primary Key)** となります。
主キーは常に一意となるように設定されるので、追加されたオブジェクトに対して自動的に値がアサインされます。

> 主キー (Primary Key)
> このフィールドがデータベースのなかで重複しないデータだと定義されたものです。
> プライマリキーを定義することは、データベース検索を効率的にするためには、
> とても重要なことです 

追加するときに使った  `ed_user` と 検索で帰ってきた  `ed` を比較してみます。
 IPython 
```
 In [27]: ed is ed_user
 Out[27]: True
 
```

ORMの**IDマップ(ID Mapping)** 機能により、セッション内の特定のレコードに対するすべての操作が同じデータのセットに対して操作されることが保証されます。このため、特定の主キーを持つオブジェクトがセッションに存在すると、そのセッションに対するすべてのSQLクエリは常にその特定の主キーに対して同じPythonオブジェクトを返します。

複数のデータを追加する場合は  `add_all()` を使います。
 IPython
```
 In [15]: # %load 07_add_all.py 
     ...: userList=[ 
     ...:   User(name='wendy', fullname='Wendy Williams', nickname='windy'), 
     ...:   User(name='mary', fullname='Mary Contrary', nickname='mary'), 
     ...:   User(name='fred', fullname='Fred Flintstone', nickname='freddy') 
     ...: ] 
     ...:  
     ...: session.add_all(userList) 
```

オブジェクトを変更する場合も簡単です。
 IPython
```
 In [18]: # %load 08_update_one.py 
     ...: ed_user.nickname = 'eddie' 
```

セッションは状態を監視していて、変更されたことを認識します。
これは `dirty` を参照すると知ることができます。
 IPython
```
 In [19]: session.dirty
 Out[19]: IdentitySet([<User('name=ed', fullname=Ed Jones, nickname=eddie)>])
```

追加されたオブジェクトは  `new` を参照すると知ることができます。
 IPython
```
 In [20]: session.new
 Out[20]: IdentitySet([<User('name=wendy', fullname=Wendy Williams, nickname=windy)>, <User('name=mary', fullname=Mary Contrary, nickname=mary)>, <User('name=fred', fullname=Fred Flintstone, nickname=freddy)>])
```

この時点ではまだメモリ上にあるため、実際にデータベースに反映させるためには `commit()` を実行します。
 IPython
```
 In [21]: session.commit()
 
```

基本的には次のような手順で追加/削除/更新を行います。
セッションへの変更は  `commit()` しない限りはデータベースには反映されません。

- **追加**： `session.add(object)` 、 `session.add_all(object_list)` 
- **更新**： `object.attr = value` でオブジェクトを変更する
- **削除**： `object.delete()` 

### ロールバック
#### ロールバック(Rollback)
これを説明するために、ユーザ ed の  `name` を Edwardo に変更して、あわせて fakeuser というユーザを追加しましょう。
 IPython
```
```
　In [29]: # %load 09_fakcuser.py 
        - ...: ed_user.name='Edwardo' 
        - ...: fake_user = User(name='fakeuser', 
        - ...:                  fullname='Invalid', 
        - ...:                  nickname='12345') 
        - ...:  
        - ...: session.add(fake_user) 
        - ...:                                                                            

 `name` フィールド が  Edwardo もしくは fakeuser であるユーザを検索してみます。
 IPython
```
 In [33]: # %load 10_fackuser_check.py 
     ...: checklist = ['Edwardo', 'fakeuser'] 
     ...: session.query(User).filter(User.name.in_(checklist)).all() 
     ...:                                                                          
 Out[33]: 
 [<User('name=Edwardo', fullname=Ed Jones, nickname=eddie)>,
  <User('name=fakeuser', fullname=Invalid, nickname=12345)>]
 
```

フィールドを指定して検索するときは、 `filter()` に `モデル名.フィールド名` のように引数に与えます。(詳細は後述します）

ここで、ロールバックを行ってみます。
 IPython
```
 In [34]: session.rollback()                                                
```

もう一度検索してみると、今度は該当データがありません。
もとに戻っていますね。
 Ipython
```
 In [35]: # %load 11_fackuser_check.py 
     ...: checklist = ['Edwardo', 'fakeuser'] 
     ...: session.query(User).filter(User.name.in_(checklist)).all() 
     ...:                                                                          
 Out[35]: []
 
 
 In [36]: ed.name
 Out[36]: 'ed'
 
 In [37]: fake_user in session
 Out[37]: False
 
```

### SQLAlchmey ORM でのクエリ
 `query()` メソッドで作成される `Query` オブジェクトは検索結果を保持します。
取り出すためには次のようにします。
 IPython
```
 In [28]: # %load 12_query_all.py 
     ...: all_users = session.query(User).order_by(User.id) 
     ...:  
     ...: for user in all_users: 
     ...:     print(user.fullname) 
     ...:                                                                          
 Ed Jones
 Wendy Williams
 Mary Contrary
 Fred Flintstone
```

フィールドを指定して直接値をとりだすこともできます。
 IPython
```
 In [33]: # %load 13_query_columns.py 
     ...: all_users = session.query(User.name, User.fullname) 
     ...: for name, fullname in all_users: 
     ...:     print(name, fullname) 
     ...:                                                                          
 ed Ed Jones
 wendy Wendy Williams
 mary Mary Contrary
 fred Fred Flintstone
```

 `query()` は `KeyedTuple` クラスで提供される名前付きタプルが返されます。
フィールド名が名前として付与されて、アトリビュートとして使用することができます。
 IPython
```
 In [40]: # %load 14_query_keyedtutle.py 
     ...: all_users = session.query(User, User.name).all() 
     ...: for row in all_users: 
     ...:    print(row.User, row.name) 
     ...:                                                                          
 <User('name=ed', fullname=Ed Jones, nickname=eddie)> ed
 <User('name=wendy', fullname=Wendy Williams, nickname=windy)> wendy
 <User('name=mary', fullname=Mary Contrary, nickname=mary)> mary
 
```

個別にカラム(フィールド）を参照するためには、 `ColumnElement.label()` の派生オブジェクトを使用して参照します。 `User` モデルの `name` フィールドのラベルを指定する場合は、 `User.name.label()` と呼び出して、引数には付与する名前( `name_label` )を与えてます。

 IPython
```
 In [47]: # %load 15_query_column_label.py 
     ...: all_users = session.query(User.name.label('name_label')).all() 
     ...: for row in all_users: 
     ...:    print(row.name_label) 
     ...:                                                                          
 ed
 wendy
 mary
 fred
```

 `Session` が保持しているモデルの名前は  `aliased()` で別名にすることができます。
 IPython
```
 In [51]: # %load 16_alias.py 
     ...: from sqlalchemy.orm import aliased 
     ...: user_alias = aliased(User, name='user_alias') 
     ...:  
     ...: all_users = session.query(user_alias, user_alias.name).all() 
     ...: for row in all_users: 
     ...:    print(row.user_alias) 
     ...:                                                                          
 <User('name=ed', fullname=Ed Jones, nickname=eddie)>
 <User('name=wendy', fullname=Wendy Williams, nickname=windy)>
 <User('name=mary', fullname=Mary Contrary, nickname=mary)>
 <User('name=fred', fullname=Fred Flintstone, nickname=freddy)>
```

検索結果を絞り込むには  `filter_by()` にカラム名（フィールド名）をキーワード引数で与えて行います。
 IPython
```
 In [85]: # %load 17_query_filter_by.py 
     ...: all_users =  session.query(User.name).filter_by(fullname='Ed Jones') 
     ...: for name, in all_users: 
     ...:    print(name) 
     ...:                                                                          
 ed
```

SQLスタイルで記述するときは  `filter()` を使います。
 IPYthon
```
 In [87]: # %load 18_query_filter.py 
     ...: all_users =  session.query(User.name).filter(User.fullname=='Ed Jones') 
     ...: for name, in all_users: 
     ...:    print(name) 
     ...:                                                                          
 ed
```

#### クエリの作成方法
 query()の使用方法

| クエリ | パターン |
|:--|:--|
| query(User) | 全件取得(Queryオブジェクトで返す) |
| query(User).all() | 全件取得(リストで返す) |
| query(User).first() | モデルオブジェクトの先頭を返す |
|  | 該当なしの場合 None |
| query(User).one() | モデルオブジェクトを１つ返す |
|  | 該当なしの場合 NoResultFound エラーが発生 |
| query(User).one_or_none() | モデルオブジェクトを１つ返す |
|  | 該当なしの場合 None |
| query(User).count() | カウント |

#### filter()での条件指定
基本的には filter_by() とほぼ同じ呼び出し形式です。違いは  `filter_buy()` ではフィールド名がキーワード引数となることです。
 SQL WHEREとの比較

| パターン | 例 |
|:--|:--|
| equal | filter(User.name == "ed") |
| not equal | filter(User.name != "ed") |
| greater than | filter(User.id > 20) |
| greater than or equal | filter(User.id >= 20) |
| less than | filter(User.id < 20) |
| less than or equal | filter(User.id <= 20) |
| Like | filter(User.name.like("%ed%")) |
| IN | filter(User.id.in_([1, 2])) |
| NOT IN | filter(~User.id.in_([1, 2])) |
| AND | filter(User.name == "ed", User.nickname == "Edwardo") |
| AND (_andメソッド) | filter(and_(User.name == "ed", User.nickname == "Edwardo")) |
| OR (_orメソッド) | filter(or_(User.name == "ed", User.nickname == "Edwardo") |


### 集計
 `sqlalchemy.sql.func` をインポートする必要があります。

 SQLAlchemy ORMでの集計

| パターン | 例 |
|:--|:--|
| 合計 | query(func.sum(User.id).label("sum_id")).first() |
| 平均 | query(func.avg(User.id).label("avg_id")).first() |
| カウント | query(func.count(User.id).label("count_users")).first() |
|  | query(User.id).count() |
| ソート(昇順） | query(User).order_by(User.id).all() |
|  | query(User).order_by(User.id.asc()).all() |
| ソート(降順) | query(User).order_by(User.id.desc()).all() |
| LIMIT | query(User).limit(2).offset(2).all() |
| GROUP_BY | query(User.id, func.count(User.id)).group_by(User.id).all() |

### リレーションの設定
 `User` に登録されているユーザのメールアドレスのためのモデル `Adress` を作成して、
 `relationship()` を使ってリレーションを設定します。
ひとつのユーザ に対して複数のメールアドレスを紐付けることができるので、１対多の関係となります。
 Ipython
```
 In [51]: # %load 20_relation.py 
     ...: from sqlalchemy import ForeignKey 
     ...: from sqlalchemy.orm import relationship 
     ...:  
     ...: class Address(Base): 
     ...:     __tablename__ = 'addresses' 
     ...:     id = Column(Integer, primary_key=True) 
     ...:     email_address = Column(String, nullable=False) 
     ...:     user_id = Column(Integer, ForeignKey('users.id')) 
     ...:  
     ...:     user = relationship("User", back_populates="addresses") 
     ...:  
     ...:     def __repr__(self): 
     ...:         return f"<Address(email_address='{self.email_address}')>" 
     ...:  
     ...: User.addresses = relationship( "Address", 
     ...:                      order_by=Address.id, back_populates="user") 
     ...:                                                                   
     
 In [52]: Base.metadata.create_all(engine)                                              
```

 `user_id` は  `ForeignKey()` を使ってテーブル  `users` の  `id` フィールドが指定されます。
これで２つのモデル（テーブル）にリレーションが設定されました。
確認のためにユーザ jack を追加してみます。
 IPython
```
 In [102]: jack = User(name='jack', 
      ...:     fullname='Jack Bean', 
      ...:     nickname='gjffdd')
 
 In [103]: jack.addresses
 Out[103]: []
 
```

Userモデルのオブジェクト jack にメールアドレスを登録してみます。
 IPython
```
 In [115]: # %load 22_add_jack_address.py 
      ...: jack.addresses = [ 
      ...:     Address(email_address='jack@google.com'), 
      ...:     Address(email_address='j25@yahoo.com') 
      ...:     ] 
      ...:  
      ...: # jack.addresses[1] 
      ...: # jack.addresses[1].user 
      ...:                                                                  
 In [116]: jack.addresses[1]
 Out[116]: <Address(email_address='j25@yahoo.com')>
 
 In [117]: jack.addresses[1].user 
 Out[117]: <User('name=jack', fullname=Jack Bean, nickname=gjffdd)>
```

２つのモデル `User` と  `Address` にリレーションが設定されていることが確認できます。

### JOIN
次のようなコードでSQLのJOINを実現できます。
 `sqlalchemy.orm.join` のインポートが必要になります。


```
 In [65]: # %load 24_join.py 
     ...: for u, a in session.query(User, Address).\ 
     ...:               filter(User.id==Address.user_id).\ 
     ...:               filter(Address.email_address=='jack@google.com').\ 
     ...:               all(): 
     ...:      print(u) 
     ...:      print(a) 
     ...:                                                                          
 <User('name=jack', fullname=Jack Bean, nickname=gjffdd)>
 <Address(email_address='jack@google.com')>
 
```

## 基本的なリレーションのパターン
ここで例示するコードでは次のインポートが必要です。


```
 from sqlalchemy import Table, Column, Integer, ForeignKey
 from sqlalchemy.orm import relationship
 from sqlalchemy.ext.declarative import declarative_base
 
 Base = declarative_base()
 
```

いま２つのテーブル Parent と Child があるとき、この２つのテーブルのリレーションのパターンを例示してゆきます。

### 一対多(One-to-Many)
一対多のリレーションでは、Parent テーブルを参照する子テーブルに外部キーを設定します。Parent には `relationship()` を設定することで、Child が表すアイテムのコレクションを参照できるようになります。


```
 class Parent(Base):
     __tablename__ = 'parent'
     id = Column(Integer, primary_key=True)
     children = relationship("Child")
 
 class Child(Base):
     __tablename__ = 'child'
     id = Column(Integer, primary_key=True)
     parent_id = Column(Integer, ForeignKey('parent.id'))
```

一対多で双方向のリレーションを確立するには、 `relationship()` を追加して、 `relationship.back_populates` 引数をを使って2つのテーブルをつなぎます。


```
 class Parent(Base):
     __tablename__ = 'parent'
     id = Column(Integer, primary_key=True)
     children = relationship("Child", back_populates="parent")
 
 class Child(Base):
     __tablename__ = 'child'
     id = Column(Integer, primary_key=True)
     parent_id = Column(Integer, ForeignKey('parent.id'))
     parent = relationship("Parent", back_populates="children")
 
```

Childテーブルは、多対一の意味を持つParentテーブルの属性を取得します。
また、 `relationship.back_populates` を使う代わりに、 `relationship.backref` 引数を単一の `relationship()` に対して使用することもできます。


```
 class Parent(Base):
     __tablename__ = 'parent'
     id = Column(Integer, primary_key=True)
     children = relationship("Child", backref="parent")
     
```

#### 一対多の削除動作の設定
Parent オブジェクトが削除されたときに、すべてのChildオブジェクトが削除される必要がある場合があります。この動作を設定するには、deleteで説明したカスケード削除オプションを使用します。さらに、ChildオブジェクトがParentから切り離されたときに、Childオブジェクト自体を削除することもできます。

### 多対一のリレーション
多対一のリレーションは、Prent テーブルにChildを参照する外部キーを配置します。 Parent テーブルで `relationship()` が宣言され、そこで新しいスカラー保持属性(scalar-holding  attribute) が作成されます。


```
 class Parent(Base):
     __tablename__ = 'parent'
     id = Column(Integer, primary_key=True)
     child_id = Column(Integer, ForeignKey('child.id'))
     child = relationship("Child")
 
 class Child(Base):
     __tablename__ = 'child'
     id = Column(Integer, primary_key=True)
     
```

双方向のリレーションを実現するためには、2つ目の  `relationship()` を追加し、 `relationship.back_populates` 引数を両方向に設定します。


```
 class Parent(Base):
     __tablename__ = 'parent'
     id = Column(Integer, primary_key=True)
     child_id = Column(Integer, ForeignKey('child.id'))
     child = relationship("Child", back_populates="parents")
 
 class Child(Base):
     __tablename__ = 'child'
     id = Column(Integer, primary_key=True)
     parents = relationship("Parent", back_populates="child")
     
```

また、 `relationship.backref` 引数は、 `Parent.child` のような単一の `relationship()` に適用することもできます。

```
 class Parent(Base):
     __tablename__ = 'parent'
     id = Column(Integer, primary_key=True)
     child_id = Column(Integer, ForeignKey('child.id'))
     child = relationship("Child", backref="parents")
     
```

### 一対一のリレーション
一対一(One To One)は基本的に、双方にスカラー属性を持つ双方向のリレーションです。ORMでは、"One-to-One "は、Parentのレコードに対して関連するレコードが一つだけ存在することを期待する慣習と考えられています。

>  スカラー(scalar)とは、 長さ、面積、重さなど、大きさだけで定まる量。簡単にいうと数値。

一対一は、 `relationship()` の  `relationship.uselist` 引数に  `False` を適用することで実現されます。場合によっては  `backref()` の  `relationship.uselist` 引数に  `False` を適用し、リレーションシップの「一対多」または「コレクション」側に適用します。

以下の例では、一対多のリレーション（Parent.children）と多対一のリレーション（Child.parent）の両方を含む双方向のリレーションを示しています。


```
 class Parent(Base):
     __tablename__ = 'parent'
     id = Column(Integer, primary_key=True)
 
     # one-to-many collection
     children = relationship("Child", back_populates="parent")
 
 class Child(Base):
     __tablename__ = 'child'
     id = Column(Integer, primary_key=True)
     parent_id = Column(Integer, ForeignKey('parent.id'))
 
     # many-to-one scalar
     parent = relationship("Parent", back_populates="children")
     
```

この例では、Parent.children はコレクションを参照する「一対多」の側であり、Child.parentは単一のオブジェクトを参照する「多対一」の側です。これを「一対一」に変換するには、「一対多」または「コレクション」側を  `uselist=False` 引数を使用してスカラー関係に変換し、わかりやすくするためにParent.childrenをParent.childに名前を変えておきます。


```
 class Parent(Base):
     __tablename__ = 'parent'
     id = Column(Integer, primary_key=True)
 
     # previously one-to-many Parent.children is now
     # one-to-one Parent.child
     child = relationship("Child", back_populates="parent", uselist=False)
 
 class Child(Base):
     __tablename__ = 'child'
     id = Column(Integer, primary_key=True)
     parent_id = Column(Integer, ForeignKey('parent.id'))
 
     # many-to-one side remains, see tip below
     parent = relationship("Parent", back_populates="child")
 
```

この例では、Parentオブジェクトをロードすると、Parent.child属性は、コレクションではなく単一のChildオブジェクトを参照します。Parent.childの値を新しいChildオブジェクトに置き換えると、ORMの単位作業プロセスは、特定のカスケード動作が設定されていない限り、前のChild.parent_id列をデフォルトでNULLにして、前のChildレコードを新しいChildレコードに置き換えます。

> 前述したように、ORMは "1対1 "のパターンを慣例としており、ParentオブジェクトのParent.child属性をロードした場合、
> 1つのレコードしか返ってこないと仮定しています。複数のレコードが返された場合、ORMは警告を発します。
> 
> しかし、上記の関係のChild.parent側は「多対一」の関係として残り、変更はありません。また、ORM自体には、永続化の際に同じParentに対して複数のChildオブジェクトが作成されるのを防ぐ本質的なシステムはありません。代わりに、ユニーク制約などの技術を実際のデータベーススキーマで使用して、この配置を強制することができます。
> Child.parent_idカラムに対するユニーク制約は、一度に1つのParentテーブルのレコードを参照できるChildテーブルのレコードが1つだけであることを保証します。


```
 from sqlalchemy.orm import backref
 
 class Parent(Base):
     __tablename__ = 'parent'
     id = Column(Integer, primary_key=True)
 
 class Child(Base):
     __tablename__ = 'child'
     id = Column(Integer, primary_key=True)
     parent_id = Column(Integer, ForeignKey('parent.id'))
     parent = relationship("Parent", backref=backref("child", uselist=False))
 
```

### 多対多のリレーション
多対多(Many to Many)のリレーションは、2つのモデルクラスの間に関連テーブル(association table)を追加します。関連テーブルは、  `relationship()` の  `relationship.secondary` 引数で指定します。通常、テーブルは宣言ベースクラス(declarative base class)に関連付けられたメタデータオブジェクトを使用し、 ForeignKey ディレクティブがリンク先のリモートテーブルを特定できるようにします。

 pyton
```
 association_table = Table('association', Base.metadata,
     Column('left_id', ForeignKey('left.id')),
     Column('right_id', ForeignKey('right.id'))
 )
 
 class Parent(Base):
     __tablename__ = 'left'
     id = Column(Integer, primary_key=True)
     children = relationship("Child", secondary=association_table)
 
 class Child(Base):
     __tablename__ = 'right'
     id = Column(Integer, primary_key=True)
     
```

この例での「関連テーブル(association table)」には、関係の両側にある2つのエンティティ・テーブルを参照する外部キー制約(ForeignKey)が設定されています。 `association.left_id` と  `association.right_id` のそれぞれのデータ型は、通常、参照されるテーブルのデータ型から推測されるので、省略することができます。また、SQLAlchemyでは必須ではありませんが、2つのエンティティテーブルを参照するカラムは、ユニーク制約か、より一般的なプライマリキー制約のどちらかで設定することをお勧めします。これにより、アプリケーション側の問題に関わらず、テーブル内に重複したレコードが永続化されないことが保証されます。


```
 association_table = Table('association', Base.metadata,
     Column('left_id', ForeignKey('left.id'), primary_key=True),
     Column('right_id', ForeignKey('right.id'), primary_key=True)
 )
 
```

双方向の関係では、関係の両サイドにコレクションが含まれます。 `relationship.back_populates` で指定し、各 `relationship()` には、共通の関連テーブルを指定します。


```
 association_table = Table('association', Base.metadata,
     Column('left_id', ForeignKey('left.id'), primary_key=True),
     Column('right_id', ForeignKey('right.id'), primary_key=True)
 )
 
 class Parent(Base):
     __tablename__ = 'left'
     id = Column(Integer, primary_key=True)
     children = relationship(
         "Child",
         secondary=association_table,
         back_populates="parents")
 
 class Child(Base):
     __tablename__ = 'right'
     id = Column(Integer, primary_key=True)
     parents = relationship(
         "Parent",
         secondary=association_table,
         back_populates="children")
         
```

 `relationship.back_populates` の代わりに `relationship.backref` 引数を使用した場合、 `backref` は自動的に同じ `relationship.secondary` 引数を逆方向の関係に使用します。


```
 association_table = Table('association', Base.metadata,
     Column('left_id', ForeignKey('left.id'), primary_key=True),
     Column('right_id', ForeignKey('right.id'), primary_key=True)
 )
 
 class Parent(Base):
     __tablename__ = 'left'
     id = Column(Integer, primary_key=True)
     children = relationship("Child",
                     secondary=association_table,
                     backref="parents")
 
 class Child(Base):
     __tablename__ = 'right'
     id = Column(Integer, primary_key=True)
     
```

また、 `relationship()のrelationship.secondary` 引数には、マッパーが最初に使用されたときにのみ評価される、callableが渡されます。これを使えば、モジュールの初期化がすべて完了した後、callableが利用可能であれば、後からassociation_tableを定義することができます。

```
 class Parent(Base):
     __tablename__ = 'left'
     id = Column(Integer, primary_key=True)
     children = relationship("Child",
                     secondary=lambda: association_table,
                     backref="parents")
                     
```

宣言型の拡張機能を使用すると、従来の「テーブルの文字列名」も受け入れられ、 `Base.metadata.tables` に格納されているテーブルの名前と一致します。


```
 class Parent(Base):
     __tablename__ = 'left'
     id = Column(Integer, primary_key=True)
     children = relationship("Child",
                     secondary="association",
                     backref="parents")
 
```

#### 多対多のテーブルからのレコードの削除
 `relationship()` の  `relationship.secondary` 引数に特有の動作として、ここで指定されたテーブルは、オブジェクトがコレクションに追加されたり削除されたりすると、自動的にINSERTおよびDELETE文の対象となります。このテーブルから手動で削除する必要はありません。コレクションからレコードを削除する行為は、フラッシュ上でレコードが削除されたという効果をもたらします。


```
 # レコードは自動的に "secondary "テーブルから削除される
 myparent.children.remove(somechild)
 
```

よくある疑問として、子オブジェクトがSession.delete()に直接渡されたときに、どうやって「二次」テーブルのレコードを削除するかということがあります。


```
 session.delete(somechild)
 
```

ここではいくつかの可能性があります。

- Paren から Child 子へのリレーションがあっても、特定の Child と各Parentを結びつける逆のリレーションがない場合、SQLAlchemyは、この特定のChild オブジェクトを削除する際に、Parent にリンクしている「二次」テーブルを維持する必要があることを認識しません。二次 "テーブルの削除は行われません。

- 特定の Child と各 Parent を結びつける関係がある場合、仮にそれが Child.parents と呼ばれているとすると、SQLAlchemy はデフォルトで Child.parents コレクションを読み込んですべてのParent オブジェクトを探し、このリンクを確立している「二次」テーブルから各レコードを削除します。この関係は双方向である必要はなく、SQLAlchemyは削除されるChildオブジェクトに関連するすべてのリレーションシップ()を厳密に見ていることに注意してください。

- ここで、よりパフォーマンスの高いオプションとして、データベースで使用される外部キーに ON DELETE CASCADE を使用することができます。データベースがこの機能をサポートしていれば、"child" の参照レコードが削除されると、データベース自体が "secondary" テーブルのレコードを自動的に削除するようにすることができます。SQLAlchemy は、 `relationship()` の  `relationship.passive_deletes` 引数を使用して、この場合に Child.parents コレクションを積極的に読み込むことを避けるように指示することができます。こ

繰り返しになりますが、これらの動作は  `relationship()` で使用される  `relationship.secondary` 引数にのみ関連しています。明示的にマッピングされた関連テーブルを扱う場合で、 関連する  `relationship()` の  `relationship.secondary` オプションに存在しない場合は、 代わりにカスケード・ルールを使用して、関連するエンティティが削除されたときに自動的にエンティティを削除することができます。 この機能については、「カスケード」を参照してください。




### SQLで検索
アプリケーションの性能を追求したいような場合にSQLを直接実行したくなりますが、
データベースエンジンにバインドされたORMからでもSQLで検索することが可能です。
ただし、あまり使いすぎるとORMを利用している意味が薄れることと、保守性が低くなるので注意してください。

 IPython
```
 In [76]: # %load 30_sql.py 
     ...: for user in session.execute("select * from users"): 
     ...:     print(user.name) 
     ...:                                                                          
 ed
 wendy
 mary
 fred
 jack
```


## カラムタイプ
モデルでフィールドを定義するとき型を指定することができます。

 SQLAlchemy のカラム

| カタムタイプ  | 説明 |
|:--|:--|
| BigInteger | 大きな整数を表す型 |
| Boolean | ブール値を表す型 |
| Date | datetime.date()オブジェクト |
| DateTime | datetime.datetime() オブジェクト |
| Enum | 列挙型(Enum型)を表す型 |
| Float | FLOATやREALなどの浮動小数点型を表す型 |
| Integer | 整数を表す型 |
| Interval | datetime.timedelta() オブジェクト |
| LargeBinary | 大きなバイナリデータ |
| MatchType | MATCH演算子の戻り値を表す型 |
| Numeric | 固定精度の数値を表す型（NUMERICやDECIMALなど） |
| PickleType  | pickleでシリアル化されたPythonオブジェクト |
| SchemaType | スキーマレベルのDDLが必要になる可能性があるとマークする型 |
| SmallInteger  | 小さい整数を表す型 |
| String | すべての文字列および文字型のベースの型 |
| Text | 可変サイズの文字列を保持する型 |
| Time | datetime.time() オブジェクト |
| Unicode | 可変サイズのUNICODE文字列を保持する型 |
| UnicodeText | 結合されていない(UNBOUNDED)長さのUNICODE文字列を保持する型 |

それぞれのタイプは引数を取ることができます。
例えば、３２文字の文字列を受け入れる name フィールドと、整数を保持する `id` フィールドをプライマリキーとする場合は、
次のように記述します。


```
 class User(Base):
     id = Column(Integer(Primary_Key=Try))
     name = Column(String(32))
     
```


## SQLAlchemy-Utilsを使ってみよう 
SQLAlchemy-Utils は SQLAlchemy をスキーム定義やデータ検証を助けるための、フィールドタイプ(型)やヘルパー関数、クラスが提供されます。

追加されるフィールドタイプ

| フィールドタイプ | 説明 |
|:--|:--|
| ArrowType | Apache Arrowオブジェクトを格納する |
| ChoiceType | 受け入れ可能な値をタプルのリストで与える |
| ColorType | Colourモジュールのcolorオブジェクトを格納する |
| CompositeType | PostgreSQLの CompositeType 型 |
| CountryType | BabelモジュールのCountryオブジェクトを格納 |
| CurrencyType | BabelモジュールのCurrencyオブジェクトを格納 |
| EmailType | Eメールアドレスを小文字で格納 |
| EncryptedType | Cryptographyモジュールを使って暗号化/復号化を行うフィールド |
| JSONType | JSONデータを格納 |
| LocaleType | BabelモジュールのLocaleオブジェクトを格納 |
| LtreeType | PostgreSQL のLtreeType 型 |
| IPAddressType | IPアドレスを格納 |
| PasswordType | パスワードをハッシュ化して格納 |
| PhoneNumberType | python-phonenumbersモジュールを使って電話番号を検証して格納 |
| ScalarListType | 複数のスカラ値を格納する（リストのように振る舞う） |
| TimezoneType | pytz や date-util のタイムゾーンを格納 |
| TSVectorType | PostgreSQL の TSVECTOR型 |
| URLType | furlモジュールを使ってURLオブジェクトを格納 |
| UUIDType | UUIDを格納 |
| WeekDaysType  | BabelモジュールのWeekDaysオブジェクトを格納 |


例えば、カラムフィールドにリストを定義したい場合は、 `ScalarListType` を使用します。
厳密にはリストのように振る舞うカラムを定義しているわけです。


```
 import sqlalchemy as sa
 from sqlalchemy import types
 from sqlalchemy_utils import ScalarListType
 
 class User(Base):
     __tablename__ = 'user'
     id = sa.Column(sa.Integer, autoincrement=True)
     hobbies = sa.Column(ScalarListType())
 
 user = User()
 user.hobbies = [u'football', u'ice_hockey']
 session.commit()
 
```

## 参考
- [SQLAlchemy オフィシャルサイト ](https://www.sqlalchemy.org/)
- [SQLAlchemy 公式ドキュメント - ORM ](https://docs.sqlalchemy.org/en/13/orm/)
- [SQLAlchemy-Utils ソースコード ](https://github.com/kvesteri/sqlalchemy-utils)



