演習２：実際にORMでデータを操作してみよう
=================

## 演習 2.1 dataset

### 演習 2.1.1 dataset を使ってデータをSQLite データベースに格納する

演習 1.1 で使用した movie_data.py から SQLite のデータベースにしてみましょう。
データベースは  `moviedb/moviedb.sqlite` として保存しましょう。

### アドバイス
はじめに制約事項があることを確認しましょう。
できることと、できないことの把握をすることはとても重要です。

- dataset ではテーブルのリレーションシップをサポートしていません。
- カラムタイプの定義では次の制約があります。
    - SQLAlchemy は sqlalchemy-utils の ScalarListType でリストを定義できますが、これを SQLite と dataset が理解できません。
    - SQLite はJSONをカラムタイプとして定義できますが、SQLAlchemy での実装は少し複雑になるため dataset では記述できません。

まったくダメとあきらめるのではなく、次のように考えてみましょう。

    - カラムタイプは文字列とする
    - MovieテーブルのIDのリストを文字列としてデータベースに格納
    - 読み出すときは、文字列として読み出し、利用時にリストに再変換


```
 # 文字列に変換
 movie_ids = [ 1, 2, 3 ]
 actor['movies'] = f'{movie_ids}'
 
 # 文字列からリスト変換
 movie_ids = eval(actor['movies'])
        
```

雛形のスクリプトを用意しましたので、適宜修正して完成させてみましょう。

 exercise_02_01_01_hint.py
```
 import dataset
 from sqlalchemy.types import Integer
 from pathlib import Path
 from movie_data import actors
 
 data_dir = 'moviedb'
 Path(data_dir).mkdir(exist_ok=True)
 
 DSN = f'sqlite:///{data_dir}/movidb.sqlite'
 db = dataset.connect(DSN)
 
 actor_table = db['actor']
 actor_table.create_column('id', type=Integer, autoincrement=True)
 actor_table.create_index(['id'])
 
 movie_table = db['movie']
 movie_table.create_column('id', type=Integer, autoincrement=True)
 movie_table.create_index(['id'])
 
 
 movie_id = 0
 for actor in actors:
     movie_list = list()
     for movie in actor['movies']:
         # ...
 
     actor['movies'] = f'{movie_list}'
     actor_table.insert(actor)
 
 db.commit()
 db.executable.invalidate()
 db.executable.engine.dispose()
 db.close()
```

### 演習 2.1.1 保存したSQLite データベースに格納されているデータを表示する

演習 2.1.1 で作成された SQLite データベース  `moviedb/moviedb.sqlite` を読み出して、データを表示してみましょう。

出力のフォーマットは次のようにしてみましょう。

 bash
```
 * Name: Robert de Niro
  - Birthday: 1943-08-17
  - IMDB: https://www.imdb.com/name/nm0000134/
  - Movies:
    - "Taxi Driver" 1976
    - "The Deer Hunter" 1978
    - "Falling in Love" 1984
    - "The Intern" 2015
    
```

雛形のスクリプトを用意しましたので、適宜修正して完成させてみましょう。

 exercise_02_01_02_hint.py
```
 import dataset
 from pathlib import Path
 
 data_dir = 'moviedb'
 Path(data_dir).mkdir(exist_ok=True)
 
 DSN = f'sqlite:///{data_dir}/movidb.sqlite'
 db = dataset.connect(DSN)
 
 actor_table = db['actor']
 movie_table = db['movie']
 
 actors = actor_table.all()
 movies = movie_table.all()
 
 for actor in actors:
     print(f'* Name: {actor["name"]}')
     print(f' - Birthday: {actor["birthday"]}')
     print(f' - IMDB: {actor["imdb"]}')
     print( ' - Movies: ')
     # ...
         print(f'   - "{movie["title"]}" {movie["year"]}')
 
 db.commit()
 db.executable.invalidate()
 db.executable.engine.dispose()
 db.close()
 
```

## 演習 2.2 SQLAlchemy

### 演習 2.2.1 テーブル作成のハンズオン

ここに、SQLAlchemy を使って、次のフィールドを持つ  `accounts` という名前のテーブルを、SQLite データベース  `sampledb/account.sqlite` に作成してみましょう。

 accounts のカラム

| カラム名 | 型 | 説明 |
|:--|:--|:--|
| id | Integer | ユーザID (プライマリキー) |
| username | String(32) | ユーザ名 |
| fullname | String(32) | 姓名 |
| password | String(256) | パスワード |
| about_me | TEXT(256) | 自己紹介 |


雛形のスクリプトを用意していますので、適宜修正して完成させてみましょう。

 exercise_02_02_01_hint.py
```
 from sqlalchemy import create_engine, Column, Integer, String, Text
 from sqlalchemy.ext.declarative import declarative_base
 from pathlib import Path
 
 data_dir = 'sampledb'
 Path(data_dir).mkdir(exist_ok=True)
 
 DSN = f'sqlite:///{data_dir}/account.sqlite'
 
 engine = create_engine(DSN)
 Base = declarative_base()
 
 class Account(Base):
     # ...
 
     def __repr__(self):
        return "<User(f'id={id}, username={username}', fullname={fullname}, password={password})>")
 
 # ...       
```


sqlite3 でデータベースがどう作成されたかを確認することができます。

 bash
```
 % sqlite3 sampledb/account.sqlite
 SQLite version 3.36.0 2021-06-18 18:36:39
 Enter ".help" for usage hints.
 sqlite> .table
 accounts
 sqlite> SELECT * FROM sqlite_master WHERE type='table' and name='accounts';
 table|accounts|accounts|2|CREATE TABLE accounts (
 	id INTEGER NOT NULL,
 	username VARCHAR,
 	fullname VARCHAR,
 	password VARCHAR,
 	about_me TEXT,
 	PRIMARY KEY (id)
 )
 sqlite>
 
```



### 演習 2.2.2 SQLAlchemy を使ってデータをSQLite データベースに格納する

演習 1.1 で使用した movie_data.py から SQLAlchemy を使って SQLite のデータベースにしてみましょう。
データベースは  `moviedb/moviedb2.sqlite` として保存しましょう。

### アドバイス
- Actor と Movie の２つのモデルを作ります。
- SQLAlchemy ではテーブルのリレーションシップを定義できます。
- SQLAlchemy-Utils の ScalarListType の利用も選択肢のひとつです。




