# 演習４ SQLAlchemy ORM と Alembic

## 演習4.1  SQLAlchemy ORMでデータベースを作成しよう
まず、`exercise4` というディレクトリを作成しましょう。

```
 $ mkdir exercise4
 $ cd exercise4
```

ここに、SQLAlchemy ORM を使って、
次のフィールドを持つ `accounts` という名前のテーブルをもつデータベース
`account.db` を作成するスクリプト `db.py` 作りましょう。

|カラム名    | 型          |説明
|------------|-------------|------------
| username	 | String(32)  | ユーザ名
| fullname	 | String(32)  | 姓名
| password	 | String(256) | パスワード
| about_you	 | TEXT(256)   | 自己紹介


## 演習4.2 Alembicでマイグレーションスクリプトを自動生成させてみましょう
alembic を使って、データベース `account.db` をマイグレーションしてみましょう。

## 演習4.3： SQLAlchemy ORMでデータベースにエントリーを追加しよう
SQLAlchemy ORM を使って、次のCSVのエントリーをテーブル `accounts`に登録する
`add_user.py` を作成しましょう。


```
username,fullname,password,about_you
freddie,"Freddie Mercury",Queen,"Main Vocal of Queen"
David,"David Coverdale",WhiteSnake,"Main Vocal of WhiteSnake"
jack,"Jack Bauer",24,"Cast of TWENTY FOUR"
```


