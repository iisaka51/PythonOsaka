BlitzDBを使ってみよう
=================
## BlitzDB について
[BlitzDB  https://github.com/adewes/blitzdb] は、Pythonで実装された、ドキュメントベースのオブジェクト指向のトランザクションデータベースです。BlitzDB には、外部に依存関係のあるモジュールはありません。さらに、[MongoDB ](https://www.mongodb.com/try/download/community) のような他のデータベースエンジンのフロントエンドとして使用することもでき、より強力な機能が必要な場合にも対応できます。

### 主な機能
BlitzDB の主な機能には次のものがあります。

- ドキュメントベースのオブジェクト指向インターフェース
- 強力で豊富なクエリ言語
- 任意のフィールドに対する深いドキュメントインデックス
- ドキュメントの圧縮保存
- 複数のバックエンドをサポート（例：ファイルベースのストレージ、MongoDB、SQLAlchemy)
- データベーストランザクションのサポート(現在はファイルベースのバックエンドのみ)
- Pythonアプリケーションに簡単に組み込むことができる

Blitzは、組み込み可能で使いやすい、高速なデータベースとして設計されています。一般的には、インデックス機能をうまく利用すれば、中程度の規模（100,000エントリ以上）のドキュメントのコレクションでもうまく動作します。
しかし、MySQLや MongoDB のような本格的なデータベースシステムではありません。

現在のバージョンでは、データベースへの同時書き込み/読み取りをサポートしていません。
ハッシュテーブルに基づいた比較的シンプルなインデックス機能を使用し、ディスク上のフラットファイルにドキュメントを保存するため、通常、クエリのパフォーマンスは最先端のデータベースシステムと比較して遜色ありません。
しかし、より高い要求には、Blitzをサードパーティのバックエンド（特にMongoDB）のフロントエンドとして使用することができます。

Blitzは、すべてのドキュメントを単一のJSONファイルとして保存するため、データベース全体をgitなどのバージョン管理ツールの管理下に置くことができます。


## インストール
オリジナルのBlitzdb は Andreas Dewes氏によって開発されました。すでに公式のサポートが終了した Python2系のコードを含んでいます。Githubで公開されているレポジトリは、2014年12月以降更新されていないため、 2017年１月に PYPI で公開されているものが最新となります。
Blitzdb3 は オリジナルのBlitdz レポジトリをフォークして、既知のバグを修正したもので、これはPython2 のコードを削除しソースコードを綺麗にしています。

blitzdb のインストールは次のように行います。

 bash
```
 $ pip install blitzdb3
 
```

Blitzでは、実行時に非標準のPythonモジュールを必要としません。しかし、Blitzのすべての機能を利用するためには、以下のPythonライブラリをインストールすることをお勧めします。

- [SQLAlchemy ](https://pypi.org/project/SQLAlchemy/)：バックエンドにSQLAlchemy を使用するときに必要
- [pymongo ](https://pypi.org/project/pymongo/) ：バックエンドにMongoDB を使用するときに必要
- [cjson ](https://pypi.org/project/python-cjson/)：CJsonEncoderに必要（JSONのシリアライズ速度が向上する）
- [pytest ](https://pypi.org/project/pytest/)：テストスイートの実行に必要です。
- [faker ](https://pypi.org/project/Faker/)：テスト用の疑似データを生成するために必要


## bliztzdb の使い方

まず、データを読み出したり格納するためには、バックエンドデータベースエンジンを指示する必要があります。

### バックエンド
BlitzDBは、単なるデータベースエンジンではなく、[SQLAlchemy ](https://www.sqlalchemy.org/support.html) のようなデータベースラッパーです。独自のファイルベースのバックエンドを提供しているので、単独で使用することができます。例えば、より多くのパワーが必要な場合や、実際のデータベースが提供する追加的なクエリ効率が必要な場合などには、MongoDB やSQLAlchemy を経由したサードパーティのデータベースシステムをバックエンドで使用すると便利です。

現在、Blitzには３つのバックエンドがプリインストールされています。

- ネイティブバックエンド：ネイティブバックエンドは、ファイルベースのバックエンドと呼ばれることもありますが、ファイルベースのインデックスとフラットファイルを使用して、ローカルディレクトリにオブジェクトを保存します。外部に依存しないので、ローエンドからミドルエンドのアプリケーションには十分な機能を備えています。
- SQLバックエンド：SQLAlchemy を使って各種データベースからドキュメントを保存・取得します。
- MongoDBバックエンド： MongoDBバックエンドは、[PyMongo ](https://pymongo.readthedocs.io/en/stable/) を使ってMongoDBデータベースからドキュメントを保存・取得します。アクセス要求が多いハイエンドのアプリケーションでは、プロフェッショナルなデータベースエンジンの使用が推奨されています。

### データベースとの接続

 `FileBackend()` を使って、ローカルファイルシステムにあるファイルからバックエンドオブジェクトを作成することができます。



```
 from blitzdb import FileBackend
 
 backend = FileBackend("datadir")
 
```

ファイルベースのバックエンドを使用する際には、Pythonライブラリの json、pickle、marshal などを使用して、ドキュメントのファイrフォーマットを選択することができます。バックエンドを作成する際に、設定用の辞書を渡してドキュメントのフォーマットを選択します。

- ファイルバックエンド

```
 backend = FileBackend("./mydata.db", {'serializer_class': 'json'})   #  デフォルト
 
```


- SQLバックエンド

```
 from sqlalchemy import create_engine
 from blitzdb.backends.sql import Backend as SQLBackend
 
 my_engine = create_engine(DSN)
 backend = SQLBackend(my_engine)
 
```

ここで、DSN は次のような情報を文字列で与えたもので、SQLAlchemy の仕様に依存しています。

>  `{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}?charset={charset_type})` 

 DSN の各パラメタ

| 要素         | 説明 |
|:--|:--|
| dialect | DBMSの種類を指定　sqlite, mysql, postgresql, oracle, mssql ... |
| driver | DBMSに接続するためのドライバーの指定　デフォルトはPytho のDBAPI． |
| username | DBMSに接続することができるユーザ名を指定 |
| password | DBMSに接続するためのパスワードを指定 |
| host | ホスト名を指定．localhost もしくは IPアドレス |
| port | ポート番号を指定　指定しなければ，バックエンドDBMSのdefaultのポート番号 |
| database | 接続するデータベース名を指定する． |
| charset_type | 文字コードを指定する．utf8とか． |

### モデルの作成
Python と同様に、Blitzではすべてのドキュメントはオブジェクトです。新しいタイプのドキュメントを作成するには、	 `blitzdb.document.Document` を継承したクラスを定義するだけです。


```
 from blitzdb import Document
 
 class Beer(Document):
     pass
 
 class Brewery(Document):
     pass
         
```

これで完了です。これだけで、ActorとMovieのドキュメントのインスタンスを作成し、扱うことができるようになります。


```
 In [2]: beer = Beer({ 'name': 'Pale Ale', 'adv': 5.5 })
 
 In [3]: beer
 Out[3]: Beer({'name': 'Pale Ale', 'adv': 5.5})
 
 In [4]: beer.name
 Out[4]: 'Pale_Ale'
 
```

プライマリキーが明示されていない場合は、 `pk` というフィールドが自動的に追加されます。
また、コレクション名（データベースでのテーブル名に相当）はクラス名から作成されます。
これを変更したい場合は、次のようにします。


```
 class Beer(Document):
      class Meta(Document.Meta):
          pk = 'name'
          collection = 'craft_beer'
```

生成されるドキュメントクラスのインスタンスオブジェクトの属性をクラス属性としてアクセスすることができます。

### ドキュメントを格納
保存するためには、次の２つの方法があります。

- バックエンドオブジェクトの `save()` メソッドを呼び出す方法
 pypthon
```
 backend.save(beer)
 
```


- インスタンスオブジェクトの `save()` メソッドを呼び出す方法

```
 beer.save(backend)
```

Blitz はトランザクション・データベースなので、バックエンドの `commit()` メソッドを呼び出して、新しいドキュメントをディスクに書き込む必要があります。


```
 backend.commit()
 
```


ここまでをハンズオンするために、次のモジュールを用意しました。
 model_beerdb.py
```
 from blitzdb import Document, FileBackend
 
 data_dir = './beerdb'
 backend = FileBackend( data_dir )
 
 class Beer(Document):
     pass
 
 class Brewery(Document):
     pass
 
 def population_database():
     # abv: Alcohol by Volume (アルコール度数)
     beer_data = [
         { 'name': 'Pale Ale', 'abv': 5.5, 'stock': 6 },
         { 'name': 'ICHII SENSHIN', 'abv': 6.5, 'stock': 6 },
         { 'name': 'ICHIGO ICHIE', 'abv': 5.5, 'stock': 24 },
         { 'name': 'Pilserl', 'abv': 4.9, 'stock': 12 },
     ]
     
     brewery_data = [
         { 'name': 'Minoh', 'country': 'Japan' },
         { 'name': 'Kyoto', 'country': 'Japan' },
         { 'name': 'Plank', 'country': 'Germany' },
     ]
 
     for d in beer_data:
         v = Beer(d)
         v.save(backend)
 
     for d in brewery_data:
         v = Brewery(d)
         v.save(backend)
 
     backend.commit()
     
     
 if __name__ == '__main__':
     import subprocess
 
     subprocess.call(['rm', '-rf', data_dir])
     population_database()
 
```

データベースを作成しておきます。


```
 In [1]: %run model_beerdb.py
 
 In [2]: !tree beerdb
 beerdb
 ├── beer
 │   ├── indexes
 │   │   └── 37ec8ed6ef9d4bb4b7aeecb89aaeb16d
 │   │       └── all_keys_with_undefined
 │   └── objects
 │       ├── 1387f01b8a6a4c2d930ccb1da0a9436a
 │       ├── 4b78766cbbef47a5893df46708de624d
 │       ├── 6edd89cbcb7c42bdb8fe94b74fa1f454
 │       └── 8775d3c9550f4d8a8ac10dbb57d607bb
 ├── brewery
 │   ├── indexes
 │   │   └── 89dbfa7792b047c493fe2265ce322aef
 │   │       └── all_keys_with_undefined
 │   └── objects
 │       ├── 283714c85f664829be2df7fb9488f671
 │       ├── 9e431d918c0d4bab8ad8e48d60ccdb50
 │       └── c87d9b21c2e44ec9b6577e5046a6210b
 └── config.json
 
 8 directories, 10 files
 
 In [3]: !cat beerdb/beer/objects/1387f01b8a6a4c2d930ccb1da0a9436a
 {"name": "ICHIGO_ICHIE", "abv": 5.5, "stock": 24, "pk": "5aba966647004f2f87398e7ca69e4a8f"}
 
```

 `FileBackend()` に与えた文字列をディレクトリとしてデータにアクセスします。なければディレクトリやデータファイルは作成されます。

### オブジェクトの取得
データベースからオブジェクトを取得するのも簡単です。単一のオブジェクトを取得したい場合は  `get()` メソッドを使用し、 Document クラスとそのドキュメントを一意に識別する任意の属性の組み合わせを指定します。


```
 In [2]: # %load 02_retreive.py
    ...: from model_beerdb import *
    ...:
    ...: beer = backend.get(Beer, {'name': 'Pale Ale'})
    ...:
    ...: # print(beer)
    ...: # print(beer.name)
    ...: # print(beer.abv)
    ...:
 
 In [3]: print(beer)
 Beer({pk : '43059df084d545939a3a14b4db892861'},lazy = False)
 
 In [4]: print(beer.name)
 Pale Ale
 
 In [5]: print(beer.abv)
 5.5
 
```

ここで、Beerモデルではプライマリキーを指示していませんでしたが、プライマリキーとして `pk` が自動的に追加されていることに注目してください。

クエリに一致するドキュメントが見つからない場合は、 `Document.DoesNotExist` 例外が発生します。同様に、クエリに一致するドキュメントが 2 つ以上見つかった場合は、 `Document.MultipleDocumentsReturned` 例外が発生します。これらの例外は所属するドキュメント クラスに固有のもので、そのクラスの属性としてアクセスできます。

 pyhhon
```
 In [2]: # %load 03_not_exists.py
    ...: from model_beerdb import *
    ...:
    ...: try:
    ...:     v1 = backend.get(Beer,{'name' : 'Hysteric IPA'})
    ...:     msg = ''
    ...: except Beer.DoesNotExist as e:
    ...:     v1 = None
    ...:     msg = e
    ...:
    ...: # print(v1)
    ...: # print(msg)
    ...:
 
 In [3]: print(v1)
 None
 
 In [4]: print(msg)
 DoesNotExist(DoesNotExist):
 
```




```
 In [2]: # %load 04_multiple_exists.py
    ...: from model_beerdb import *
    ...:
    ...: try:
    ...:     v1 = backend.get(Beer,{'abv' : 5.5})
    ...:     msg = ''
    ...: except Beer.MultipleDocumentsReturned as e:
    ...:     v1 = None
    ...:     msg = e
    ...:
    ...: # print(v1)
    ...: # print(msg)
    ...:
 
 In [3]: print(v1)
 None
 
 In [4]: print(msg)
 MultipleDocumentsReturned(MultipleDocumentsReturned):
 
```

与えられたクエリにマッチするすべてのオブジェクトを取得したい場合は、代わりに `filter()` メソッドを使用することができます。


```
 In [2]: # %load 05_filter.py
    ...: from model_beerdb import *
    ...:
    ...: v1 = backend.filter(Beer, {'abv' : 5.5})
    ...:
    ...: def show(data):
    ...:     for d in data:
    ...:         print(f'{d.name} {d.abv}')
    ...:
    ...: # pirnt(v1)
    ...: # show(v1)
    ...:
 
 In [3]: print(v1)
 <blitzdb.backends.file.queryset.QuerySet object at 0x10459b2e0>
 
 In [4]: show(v1)
 Pale Ale 5.5
 ICHIGO ICHIE 5.5
 
```

 `filter()` メソッドでは、クエリにマッチしたすべてのオブジェクトのキーのリストを含む、クエリセットが返されます。クエリセットはイテレート可能なので、リストと同じように使用できます。

データベースにあるモデルのデータをすべて取得したい場合は、次のように’空の’クエリを与えます。

```
 In [2]: # %load 06_list_all.oy
    ...: from model_beerdb import *
    ...:
    ...: v1 = backend.filter(Beer, {})
    ...:
    ...: def show(data):
    ...:     for d in data:
    ...:         print(f'{d.name} {d.abv}')
    ...:
    ...: # show(v1)
    ...:
 
 In [3]: (v1)
 Pale Ale 5.5
 ICHII SENSHIN 6.5
 ICHIGO ICHIE 5.5
 Pilserl 4.9
 
```

### ドキュメントの更新

データベース上のドキュメントを更新するには、オブジェクトの属性を変更または追加してから、 `save()` メソッドを呼び出します。


```
 In [2]: # %load 07_update.py
    ...: from model_beerdb import *
    ...:
    ...: v1 = backend.get(Beer, {'name': 'Pale Ale'})
    ...: v2 = v1.stock
    ...: v1.stock -= 2
    ...: backend.commit()
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v1.stock)
    ...:
 
 In [3]: print(v1)
 Beer({pk : '43059df084d545939a3a14b4db892861'},lazy = False)
 
 In [4]: print(v2)
 6
 
 In [5]: print(v1.stock)
 4
 
```

ドキュメントを追加する場合も、モデルからオブジェクトを生成して `save()` メソッドを呼び出します。


```
 In [2]: # %load 08_add.py
    ...: from model_beerdb import *
    ...:
    ...: beer = Beer({'name': 'Hysteric IPA', 'abv': 7.0, 'stock': 6})
    ...: brewery = Brewery({'name': 'Y.Market', 'country': 'Japan'})
    ...:
    ...: backend.save(beer)
    ...: backend.save(brewery)
    ...: backend.commit()
    ...:
    ...: v1 = backend.get(Beer,{'name' : 'Hysteric IPA'})
    ...:
    ...: # print(v1)
    ...:
 
 In [3]: print(v1)
 Beer({pk : 'a478b45724bb4f1089baddbde53e48e2'},lazy = False)
 
 In [4]: print(v1.name)
 Hysteric_IPA
 
```


### ドキュメントの削除
データベースからドキュメントを削除するためには、削除したいオブジェクトのインスタンスを指定して、バックエンドの `delete()` メソッドを呼び出します。


```
 In [2]: # %load 09_delete.py
    ...: from model_beerdb import *
    ...: from pprint import pprint
    ...:
    ...: def list_beers():
    ...:     for d in backend.filter(Beer, {}):
    ...:         print(f'{d.name} {d.abv}')
    ...:
    ...: beer = backend.get(Beer, {'name': 'Pale Ale'})
    ...: backend.delete(beer)
    ...: backend.commit()
    ...:
    ...: # pprint(beer)
    ...: # list_beers()
    ...: # backend.save(beer)
    ...: # backend.commit()
    ...: # list_beers()
    ...:
 
 In [3]: pprint(beer)
 Beer({'name': 'Pale Ale', 'abv': 5.5, 'stock': 6, 'pk': 'ca6476fdb6f445f8aba6add6453439e5'})
 
 In [4]: list_beers()
 ICHII SENSHIN 6.5
 ICHIGO ICHIE 5.5
 Pilserl 4.9
 
 In [5]: backend.save(beer)
 Out[5]: Beer({'name': 'Pale Ale', 'abv': 5.5, 'stock': 6, 'pk': 'ca6476fdb6f445f8aba6add6453439e5'})
 
 In [6]: backend.commit()
 
 In [7]: list_beers()
 Pale Ale 5.5
 ICHII SENSHIN 6.5
 ICHIGO ICHIE 5.5
 Pilserl 4.9
    
```

### トランザクション
Blitzdb はトランザクション・データベースで、バックエンドの `commit()` メソッドを呼び出して、新しいドキュメントをディスクに書き込む必要があることには触れました。Blitzdb では次のトランザションに関係するメソッドがあります。

-  `autocommit()` ： `commit()` を自動的に呼び出すかどうかをブール値で与える。デフォルトは `False` 
-  `begine()` ：新しいトランザクションのポイントを指示する
-  `commit()` ：トランザクションで変更された内容をバックエンドへ書き込む
-  `rollback()` ：トランザクションで変更された内容を破棄して `begin()` で取得したポイントに巻き戻す

 `autocommit()` を設定を使えば、 `commit` の呼び出しを気にせずに済むと思うかもしれません。しかし、コミットしたタイミングでディスクへのすべてのインデックスの完全な書き換えが行われるため、書き込み時間に大きなオーバーヘッドが発生することに留意してください。これは、ディスクに格納されているすべてのインデックスの完全な書き換えが発生するからです。

前述のオブジェクトの削除を説明するためのサンプルコードでは、削除したドキュメントを、また `save()` メソッドで追加していました。
トランザクションの `rollback()` で巻き戻してみましょう。


```
 In [2]: # %load 10_transaction.py
    ...: from model_beerdb import *
    ...: from pprint import pprint
    ...:
    ...: def list_beers():
    ...:     for d in backend.filter(Beer, {}):
    ...:         print(f'{d.name} {d.abv}')
    ...:
    ...: trans = backend.begin()
    ...: backend.get(Beer, {'name': 'Pale_Ale'}).delete()
    ...: backend.rollback(trans)
    ...:
    ...: backend.commit()
    ...:
    ...: # list_beers()
    ...:
 
 In [3]: list_beers()
 Pale_Ale 5.5
 ICHII_SENSHIN 6.5
 ICHIGO_ICHIE 5.5
 Pilserl 4.9
 
```


### リレーションシップの定義
データベースは、オブジェクト間の関係を定義できなければ意味がありません。MongoDBのように、Blitzはドキュメントの中に他のドキュメントへの参照を定義することをサポートしています。


```
 In [2]: # %load 09_relation.py
    ...: from model_beerdb import *
    ...: from pprint import pprint
    ...:
    ...: plank = backend.get(Brewery, {'name': 'Plank'})
    ...: pilserl = backend.get(Beer, {'name': 'Pilserl'})
    ...:
    ...: pilserl.brewery = plank
    ...:
    ...: # pprint(pilserl)
    ...: # print(pilserl.brewery.country)
    ...:
 
 In [3]: pprint(pilserl)
 Beer({'name': 'Pilserl', 'abv': 4.9, 'stock': 12, 'pk': '35e61658e10b4f8385e64252db4fa7d5', 'brewery': 'Brewery({...})'})
 
 In [4]: print(pilserl.brewery.country)
 Germany
 
```

BlitzDB は内部的に、ドキュメント内で遭遇した Document インスタンスを、埋め込まれたドキュメントのプライマリキーと、それが格納されているコレクションの名前を含むデータベース参照に変換します。このように、データベースからアクターをリロードすると、埋め込まれたムービーオブジェクトも自動的に（Lazy(ほっといても)）ロードされます。


オブジェクトがデータベースから読み込まれるとき、そのオブジェクトが含む他のオブジェクトへの参照は、自動的に読み込まれます。このことは、プライマリキーとそのオブジェクトが含まれるコレクションの名前だけで初期化されるということです。つまり、その属性は要求があった場合にのみ自動的に読み込まれます。

このようにして、Blitzは本当に必要でない限り、データベースからの複数回の読み込みを避けることができます。

## 高度なクエリ
MongoDB と同様に、Blitz も高度なクエリ演算子をサポートしています。これらの演算子は、クエリの前にドル記号( `$` ) を付けて記述します。

-  `$and` : 2 つ以上の式の AND を実行します。
-  `$or` : 2 つ以上の式に対して OR を実行します。
-  `$gt` : 属性と指定された値の間で  `>` 比較を行います。
-  `$gte` : 属性と指定された値との間で  `>=` の比較を行います。
-  `$alt` : 属性と指定された値の間で  `<` を比較します。
-  `$lte` : 属性と指定された値の間で  `<=` の比較を行う
-  `$all` : 引数リストのすべての値を含むドキュメントを返します。
-  `$in` : 引数リストの少なくとも1つの値に一致するドキュメントを返します。
-  `$ne` : 指定された式に対して等しくない操作を行います。
-  `$not` : 属性と与えられた値の間に不等式があるかどうかをチェックします。
-  `$regex` : パターン・マッチングのための正規表現機能を提供します。
-  `$exists` : すべてのドキュメントにフィールドが存在するかどうかを調べます。


デフォルトでは、クエリで複数の属性を指定した場合、暗黙的に  `$and` クエリが実行され、クエリで指定したすべての属性/値のペアにマッチするドキュメントのみが返されます。この動作は、 `$and` 演算子を使って明示的に指定することもできます。したがって、次の 2 つのクエリは同じものになります。


```
 In [2]: # %load 10_and.py
    ...: from model_beerdb import *
    ...: from pprint import pprint
    ...:
    ...: v1 = backend.filter(Beer, {'name': 'ICHII_SENSHIN', 'abv': 6.5})
    ...: v2 = backend.filter(Beer, {'$and': [{ 'name': 'ICHII_SENSHIN' },
    ...:                                     { 'abv': 6.5 }]})
    ...:
    ...: def show(data):
    ...:     for d in data:
    ...:         pprint(d)
    ...:
    ...: # show(v1)
    ...: # show(v2)
    ...:
 
 In [3]: show(v1)
 Beer({'name': 'ICHII_SENSHIN', 'abv': 6.5, 'stock': 6, 'pk': '5a2a0a56950d4146af7fe7d5580cc96a'})
 
 In [4]: show(v2)
 Beer({'name': 'ICHII_SENSHIN', 'abv': 6.5, 'stock': 6, 'pk': '5a2a0a56950d4146af7fe7d5580cc96a'})
 
```


クエリの中で同じドキュメント属性を複数回参照したい場合は、 `$and` クエリを使用する必要があります。


```
 In [2]: # %load 11_attr_multi_reference.py
    ...: from model_beerdb import *
    ...: from pprint import pprint
    ...:
    ...: v1 = backend.filter(Beer, {'$and': [{ 'abv': { '$gte': 5.5 }},
    ...:                                     { 'abv': { '$lte': 7.0 }}]})
    ...:
    ...: def show(data):
    ...:     for d in data:
    ...:         pprint(d)
    ...:
    ...: # show(v1)
    ...:
 
 In [3]: show(v1)
 Beer({'name': 'ICHIGO_ICHIE', 'abv': 5.5, 'stock': 24, 'pk': '5aba966647004f2f87398e7ca69e4a8f'})
 Beer({'name': 'ICHII_SENSHIN', 'abv': 6.5, 'stock': 6, 'pk': '5a2a0a56950d4146af7fe7d5580cc96a'})
 Beer({'name': 'Hysteric_IPA', 'abv': 7.0, 'stock': 6, 'pk': 'a478b45724bb4f1089baddbde53e48e2'})
 
```

 `$exists` は続くブール値の値によって相反する挙動となります。

フィールドに  `abv` があるドキュメントを取得

```
 query1 = {'abv': {'$exists': True}}
```

フィールドに  `abv` がないドキュメントを取得

```
 query2 = {'abv': {'$exists': False}}
```

次のサンプルで確認してみましょう。


```
 In [2]: # %load 23_exists.py
    ...: from model_beerdb import *
    ...: from pprint import pprint
    ...:
    ...: def show(data):
    ...:     for d in data:
    ...:         pprint(d)
    ...:     else:
    ...:         print('None')
    ...:
    ...: query1 = {'abv': {'$exists': True}}
    ...: query2 = {'abv': {'$exists': False}}
    ...: query3 = {'ibu': {'$exists': False}}
    ...:
    ...: v1 = backend.filter(Beer, query1)
    ...: v2 = backend.filter(Beer, query2)
    ...: v3 = backend.filter(Beer, query3)
    ...:
    ...: # show(v1)
    ...: # show(v2)
    ...: # show(v3)
    ...:
    ...:
 
 In [3]: show(v1)
 Beer({'name': 'Pale_Ale', 'abv': 5.5, 'stock': 6, 'pk': 'ca6476fdb6f445f8aba6add6453439e5'})
 Beer({'name': 'ICHIGO_ICHIE', 'abv': 5.5, 'stock': 24, 'pk': 'bd24f894e823445baab73605c568289e'})
 Beer({'name': 'ICHII_SENSHIN', 'abv': 6.5, 'stock': 6, 'pk': 'd1b696145a7c487fb002f5cbdf12c02c'})
 Beer({'name': 'Pilserl', 'abv': 4.9, 'stock': 12, 'pk': '140beaca28a9445b8df9dd96bbf1caf7'})
 None
 
 In [4]: show(v2)
 None
 
 In [5]: show(v3)
 Beer({'name': 'Pale_Ale', 'abv': 5.5, 'stock': 6, 'pk': 'ca6476fdb6f445f8aba6add6453439e5'})
 Beer({'name': 'ICHII_SENSHIN', 'abv': 6.5, 'stock': 6, 'pk': 'd1b696145a7c487fb002f5cbdf12c02c'})
 Beer({'name': 'ICHIGO_ICHIE', 'abv': 5.5, 'stock': 24, 'pk': 'bd24f894e823445baab73605c568289e'})
 Beer({'name': 'Pilserl', 'abv': 4.9, 'stock': 12, 'pk': '140beaca28a9445b8df9dd96bbf1caf7'})
 None
 
```

 `$in` クエリ演算子では、フィールドの値がリストで与えた値とマッチするドキュメントを取得します。


```
 In [2]: # %load 24_in.py
    ...: from model_beerdb import *
    ...: from pprint import pprint
    ...:
    ...: def show(data):
    ...:     for d in data:
    ...:         pprint(d)
    ...:     else:
    ...:         print('None')
    ...:
    ...:
    ...: query1 = {'name': {'$in': ['Ale']}}
    ...: query2 = {'name': {'$not': {'$in': ['Ale']}}}
    ...:
    ...: v1 = backend.filter(Beer, query1)
    ...: v2 = backend.filter(Beer, query2)
    ...:
    ...: # show(v1)
    ...: # show(v2)
    ...:
 
 In [3]: show(v1)
 None
 
 In [4]: show(v2)
 Beer({'name': 'Pale Ale', 'abv': 5.5, 'stock': 6, 'pk': 'c127f777d13544bdbfd4bb729055711b'})
 Beer({'name': 'ICHII SENSHIN', 'abv': 6.5, 'stock': 6, 'pk': '06a66bf477d7494ba5202e175996e562'})
 Beer({'name': 'ICHIGO ICHIE', 'abv': 5.5, 'stock': 24, 'pk': '0b852f112d9c43e59e9278fca8529755'})
 Beer({'name': 'Pilserl', 'abv': 4.9, 'stock': 12, 'pk': 'c91ddfaf466748fbb74e919b03af16ef'})
 None
 
```

この例のように、フィールドの値の部分文字列とマッチするか評価はされません。つまり、フィールドの値に完全に’合致するかどうかを評価します。
フィールドの値の部分文字列とマッチするか’評価させたい場合は  `$regex` を使用します。


```
 In [2]: # %load 25_regex.py
    ...: from model_beerdb import *
    ...: from pprint import pprint
    ...:
    ...: def show(data):
    ...:     for d in data:
    ...:         pprint(d)
    ...:     else:
    ...:         print('None')
    ...:
    ...:
    ...: query1 = {'name': {'$regex': '.*Ale$'}}
    ...:
    ...: v1 = backend.filter(Beer, query1)
    ...:
    ...: # show(v1)
    ...:
 
 In [3]: show(v1)
 Beer({'name': 'Pale Ale', 'abv': 5.5, 'stock': 6, 'pk': 'c127f777d13544bdbfd4bb729055711b'})
 None
 
```



## クエリ結果の並び替え
クエリの結果はクエリセットオブジェクトとして返されます。このオブジェクトの  `sort()` メソッドを呼び出すと、クエリの結果を並び替えることができます。


```
 In [2]: # %load 12_sort.py
    ...: from model_beerdb import *
    ...: from blitzdb.queryset import QuerySet
    ...: from pprint import pprint
    ...:
    ...: v1 = backend.filter(Beer, {}).sort([("abv", QuerySet.ASCENDING)])
    ...: v2 = backend.filter(Beer, {}).sort([("abv", QuerySet.DESCENDING)])
    ...:
    ...: def show(data):
    ...:     for d in data:
    ...:         pprint(d)
    ...:
    ...: # show(v1)
    ...: # show(v2)
    ...:
 
 In [3]: show(v1)
 Beer({'name': 'Pilserl', 'abv': 4.9, 'stock': 12, 'pk': '35e61658e10b4f8385e64252db4fa7d5'})
 Beer({'name': 'ICHIGO_ICHIE', 'abv': 5.5, 'stock': 24, 'pk': '5aba966647004f2f87398e7ca69e4a8f'})
 Beer({'name': 'ICHII_SENSHIN', 'abv': 6.5, 'stock': 6, 'pk': '5a2a0a56950d4146af7fe7d5580cc96a'})
 Beer({'name': 'Hysteric_IPA', 'abv': 7.0, 'stock': 6, 'pk': 'a478b45724bb4f1089baddbde53e48e2'})
 
 In [4]: show(v2)
 Beer({'name': 'Hysteric_IPA', 'abv': 7.0, 'stock': 6, 'pk': 'a478b45724bb4f1089baddbde53e48e2'})
 Beer({'name': 'ICHII_SENSHIN', 'abv': 6.5, 'stock': 6, 'pk': '5a2a0a56950d4146af7fe7d5580cc96a'})
 Beer({'name': 'ICHIGO_ICHIE', 'abv': 5.5, 'stock': 24, 'pk': '5aba966647004f2f87398e7ca69e4a8f'})
 Beer({'name': 'Pilserl', 'abv': 4.9, 'stock': 12, 'pk': '35e61658e10b4f8385e64252db4fa7d5'})
 
```


## フック(Hook)
Blitzdb では `save()` などの処理の前後に別の処理をさせることができます。

-  `before_save()` ： `save()` が実行される前に呼び出される
-  `before_delete()` ： `delete()` が実行される前に呼び出される
-  `before_update()` ： `update()` が実行される前に呼び出される
-  `after_load()` ：  `load()` が実行された後に呼び出される

 model_demo.py
```
 from blitzdb import Document, FileBackend
 from datetime import datetime
 
 data_dir = './hookdemo'
 backend = FileBackend( data_dir )
 
 class BaseDocument(Document):
 
     def before_save(self):
         self.foo = "before save"
 
     def before_delete(self):
         self.foo = "before delete"
 
     def after_load(self):
         self.bar = "after load"
 
     def before_update(self,set_fields,unset_fields):
         set_fields['updated_at'] = datetime.now()
 
 class MyDoc(BaseDocument):
     pass
 
 if __name__ == '__main__':
     import subprocess
 
     subprocess.call(['rm', '-rf', data_dir])
     
```

### after_load()


```
 In [2]: # %load 31_hook_after_load.py
    ...: from model_demodb import *
    ...:
    ...: doc = MyDoc({'test': 123})
    ...: backend.save(doc)
    ...: backend.commit()
    ...:
    ...: v1 = hasattr(doc, 'bar')
    ...: loaded_doc = backend.get(MyDoc,{'pk' : doc.pk})
    ...: v2 = hasattr(loaded_doc, 'bar')
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(loaded_doc.bar)
    ...:
 
 In [3]: print(v1)
 False
 
 In [4]: print(v2)
 True
 
 In [5]: print(loaded_doc.bar)
 after load
 
```


### before_save()


```
 In [2]: # %load 32_hook_befre_save.py
    ...: from model_demodb import *
    ...:
    ...: doc = MyDoc({'test': 123})
    ...: v1 = hasattr(doc, 'foo')
    ...: backend.save(doc)
    ...: v2 = hasattr(doc, 'foo')
    ...: backend.commit()
    ...:
    ...: loaded_doc = backend.get(MyDoc,{'pk' : doc.pk})
    ...: v3 = hasattr(loaded_doc, 'foo')
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v3)
    ...: # print(doc.foo)
    ...: # print(loaded_doc.foo)
    ...:
 
 In [3]: print(v1)
 False
 
 In [4]: print(v2)
 True
 
 In [5]: print(v3)
 True
 
 In [6]: print(doc.foo)
 before save
 
 In [7]: print(loaded_doc.foo)
 before save
 
```


### before_update()


```
 In [1]: %load 33_hook_befre_update.py
 
 In [2]: # %load 33_hook_befre_update.py
    ...: from model_demodb import *
    ...:
    ...: doc = MyDoc({'test': 123})
    ...: backend.save(doc)
    ...:
    ...: v1 = hasattr(doc, 'foo')
    ...: v2 = hasattr(doc, 'updated_at')
    ...: backend.update(doc,{'foo' : 'I love IPA'})
    ...: backend.commit()
    ...: v3 = doc.foo
    ...: v4 = doc.updated_at
    ...:
    ...:
    ...: # print(v1)
    ...: # ...
    ...: # print(v4)
    ...:
 
 In [3]: print(v1)
 True
 
 In [4]: print(v2)
 False
 
 In [5]: print(v3)
 I love IPA
 
 In [6]: print(v4)
 2021-08-29 07:24:07.278639
 
```

### before_delete()


```
 In [2]: # %load 34_hook_befre_delete.py
    ...: from model_demodb import *
    ...:
    ...: doc = MyDoc({'test': 123})
    ...: doc.pk = 1
    ...: v1 = hasattr(doc, 'foo')
    ...: backend.delete(doc)
    ...: v2 = hasattr(doc, 'foo')
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(doc.foo)
    ...:
 
 In [3]: print(v1)
 False
 
 In [4]: print(v2)
 True
 
 In [5]: print(doc.foo)
 before delete
 
```



## SQLバックエンド

ここで、SQLAlchemy をインストールして、Blitzdb での SQLバックエンドを説明しておきます。

 bash
```
 $ pip install sqlalchemy
 
```

SQLバックエンドでも、これまで説明してきた、基本的な操作やクエリはそのまま使用することができます。
注意するべき点は、FileBackend ではほとんどスキームレスで、ドキュメントオブジェクトにできましたが、SQLBackendではデータに応じたスキームを明示的にモデルクラスに定義する必要があります。

 `model_beerdb.py` を少しだけ修正して、SQLバックエンドを使用するようします。

 modeL-sqldemo.py
```
 from sqlalchemy import create_engine
 from pathlib import Path
 from blitzdb import Document, SqlBackend
 from blitzdb.fields import ( ForeignKeyField,
                              ManyToManyField,
                              CharField,
                              FloatField,
                              IntegerField,
                              BooleanField )
 
 class Brewery(Document):
     name = CharField()
     country = CharField()
 
 class Beer(Document):
     name = CharField()
     abv = FloatField()
     stock = IntegerField()
 
 url = f'sqlite:///{data_dir}/demo.sqlite'
 engine = create_engine(url, echo=False)
 backend = SqlBackend(engine)
 backend.register(Beer)
 backend.register(Brewery)
 backend.init_schema()
 backend.create_schema()
 
 def population_database():
     # Alcohol by Volume (アルコール度数)
     beer_data = [
         { 'name': 'Pale Ale', 'abv': 5.5, 'stock': 6 },
         { 'name': 'ICHII SENSHIN', 'abv': 6.5, 'stock': 6 },
         { 'name': 'ICHIGO ICHIE', 'abv': 5.5, 'stock': 24 },
         { 'name': 'Pilserl', 'abv': 4.9, 'stock': 12 },
     ]
 
     brewery_data = [
         { 'name': 'Minoh', 'country': 'Japan' },
         { 'name': 'Kyoto', 'country': 'Japan' },
         { 'name': 'Plank', 'country': 'Germany' },
     ]
 
     for d in beer_data:
         v = Beer(d)
         v.save(backend)
 
     for d in brewery_data:
         v = Brewery(d)
         v.save(backend)
 
     backend.commit()
 
 if __name__ == '__main__':
     population_database()
```

データベースを初期化しておきます。
 bash
```
 $ python model_sqldemo.py
 
```

Blitzdb3 -> SQLAlchemy -> SQLite3 と経由してデータベースに接続されて、データベースが作成されます。
SQLite3 レベルでデータベースを確認してみあす。

 bash
```
 % sqlite3 sqldemo/demo.sqlite
 SQLite version 3.36.0 2021-06-18 18:36:39
 Enter ".help" for usage hints.
 sqlite> .tables
 beer      brewery   document
 sqlite> SELECT * FROM sqlite_master WHERE type='table' and name='beer';
 table|beer|beer|5|CREATE TABLE beer (
 	data BLOB,
 	name VARCHAR,
 	abv FLOAT,
 	stock INTEGER,
 	pk VARCHAR(32) NOT NULL,
 	PRIMARY KEY (pk)
 )
 sqlite>
 
```

Blitzdbからデータを読み出してみましょう。
次のサンプルコードは、以前に説明した  `02_retreive.py` とインポートするモジュールが’違うだけです。


```
 In [2]: # %load 40_retreive.py
    ...: from model_sqldemo import *
    ...:
    ...: v1 = backend.get(Beer, {'name': 'Pale Ale'})
    ...: v2 = backend.get(Beer, dict(name='Pale Ale'))
    ...:
    ...: # print(v1)
    ...: # print(v1.name)
    ...: # print(v1.abv)
    ...: # print(v2)
    ...: # print(v2.name)
    ...: # print(v2.abv)
    ...:
 
 In [3]: print(v1)
 Beer({pk : '1cb6d0d9d02f45bc9617471c5258c15e'},lazy = False)
 
 In [4]: print(v1.name)
 Pale Ale
 
 In [5]: print(v1.abv)
 5.5
 
 In [6]: print(v2)
 Beer({pk : '1cb6d0d9d02f45bc9617471c5258c15e'},lazy = False)
 
 In [7]: print(v2.name)
 Pale Ale
 
 In [8]: print(v2.abv)
 5.5
 
```

モデルクラスと僅かな修正で、既存のコードがSQLBackendに対応できることを確認できました。

余談ではありますが、Blitzdb と Blitdb3 の違いのひとつが、SQLBackendに 現れます。
Python3.7以降で次のコードを実行すると  `RuntimeError` の例外が発生してしまいます。

```
 In [2]: # %load 40_list_all_ng.py
    ...: from model_sqldemo import *
    ...:
    ...: v1 = backend.filter(Beer, {})
    ...:
    ...: def show(data):
    ...:     for d in data:
    ...:         print(f'{d.name} {d.abv}')
    ...:
    ...: # show(v1)
    ...:
 
 In [3]: show(v1)
 Pilserl 4.9
 ICHIGO ICHIE 5.5
 ICHII SENSHIN 6.5
 Pale Ale 5.5
 ---------------------------------------------------------------------------
 StopIteration                             Traceback (most recent call last)
 ~/anaconda3/envs/class_database/lib/python3.9/site-packages/blitzdb/backends/sql/queryset.py in __iter__(self)
     114             yield obj
 --> 115         raise StopIteration
     116
 
 StopIteration:
 
 The above exception was the direct cause of the following exception:
 
 RuntimeError                              Traceback (most recent call last)
 <ipython-input-3-6ebf82ed8341> in <module>
 ----> 1 show(v1)
 
 <ipython-input-2-e8bcac641822> in show(data)
       5
       6 def show(data):
 ----> 7     for d in data:
       8         print(f'{d.name} {d.abv}')
       9
 
 RuntimeError: generator raised StopIteration
 
```

一見すると何も問題がないように見えますが、Python 3.7 から [PEP-470 ](https://www.python.org/dev/peps/pep-0479) がが全てのコードでデフォルトで有効化されたため、ジェネレータから送出された  `StopIteration` は  `RuntimeError` に変換されるようになりました。
Blitzdb では 2017年から更新されていないため、この Python側の変更に対応しきれていないことが理由です。

Blitdb を使わずに Blitzdb3 を使うと、この問題に対応済みなのでエラーにはなりません。

既存プロジェクトでのなんらかの理由から、Blitdb を使い続ける必要があるのであれば、プログラマ側で次のように対応すれば、この問題を回避することができます。（美しくはないですけれど...)


```
 In [2]: # %load 41_list_all_ok.py
    ...: from model_sqldemo import *
    ...:
    ...: v1 = backend.filter(Beer, {})
    ...:
    ...: def show(data):
    ...:     try:
    ...:         for d in data:
    ...:             print(f'{d.name} {d.abv}')
    ...:     except RuntimeError:
    ...:         pass
    ...:
    ...: # show(v1)
    ...:
 
 In [3]: show(v1)
 Pilserl 4.9
 ICHIGO ICHIE 5.5
 ICHII SENSHIN 6.5
 Pale Ale 5.5
 
```

## 1対多のリレーションシップ
FileBackend でのリレーションシップは、オブジェクトをそのまま属性値とするだけでした。　(サンプルコード `20_relation.py` を参照) 
これに対して、SQLBackend ではモデルクラスのフィールドにリレーションシップを定義する必要があります。このことは、Blitzdb での制約ではなくて、SQLAlchemy側での制約になります。


```
  class Brewery(Document):
      name = CharField()
      country = CharField()
 
 class Beer(Document):
     name = CharField()
     abv = FloatField()
     stock = IntegerField()
     brewery = ForeignKeyField(Brewery)
 
```

この修正を反映したモジュールを使います。
 model_sqldeom2.py
```
 from sqlalchemy import create_engine
 from pathlib import Path
 from blitzdb import Document, SqlBackend
 from blitzdb.fields import ( ForeignKeyField,
                              ManyToManyField,
                              CharField,
                              FloatField,
                              IntegerField,
                              BooleanField )
 
 class Brewery(Document):
     name = CharField()
     country = CharField()
 
 class Beer(Document):
     name = CharField()
     abv = FloatField()
     stock = IntegerField()
     brewery = ForeignKeyField(Brewery)
 
 data_dir = 'sqldemo'
 dir = Path(data_dir)
 dir.mkdir(exist_ok=True)
 
 url = f'sqlite:///{data_dir}/demo.sqlite'
 engine = create_engine(url, echo=False)
 backend = SqlBackend(engine)
 backend.register(Beer)
 backend.register(Brewery)
 backend.init_schema()
 backend.create_schema()
 
 def population_database():
     # Alcohol by Volume (アルコール度数)
     beer_data = [
         { 'name': 'Pale Ale', 'abv': 5.5, 'stock': 6 },
         { 'name': 'ICHII SENSHIN', 'abv': 6.5, 'stock': 6 },
         { 'name': 'ICHIGO ICHIE', 'abv': 5.5, 'stock': 24 },
         { 'name': 'Pilserl', 'abv': 4.9, 'stock': 12 },
     ]
 
     brewery_data = [
         { 'name': 'Minoh', 'country': 'Japan' },
         { 'name': 'Kyoto', 'country': 'Japan' },
         { 'name': 'Plank', 'country': 'Germany' },
     ]
 
     for d in beer_data:
         v = Beer(d)
         v.save(backend)
 
     for d in brewery_data:
         v = Brewery(d)
         v.save(backend)
 
     backend.commit()
 
 if __name__ == '__main__':
     population_database()
     
```



```
 In [2]: # %load 50_one_to_many.py
    ...: from model_sqldemo2 import *
    ...: from pprint import pprint
    ...:
    ...: plank = backend.get(Brewery, {'name': 'Plank'})
    ...: pilserl = backend.get(Beer, {'name': 'Pilserl'})
    ...:
    ...: pilserl.brewery = plank
    ...:
    ...: # pprint(pilserl)
    ...: # print(pilserl.brewery.country)
    ...:
 
 In [3]: print(pilserl)
 Beer({pk : 'ee51ee9a795643f2874b2c3c23587a0c'},lazy = False)
 
 In [4]: pprint(pilserl)
 Beer({'name': 'Pilserl', 'abv': 4.9, 'stock': 12, 'brewery': 'Brewery({...})', 'pk': 'ee51ee9a795643f2874b2c3c23587a0c'})
 
 In [5]: print(pilserl.brewery.country)
 Germany
```


## 多対多のリレーションシップ

SqlBackend を使う場合、多対多のリレーションシップは次のように `ManyToManyField()` を使ってモデルを定義する必要があります。このとき、参照先のモデルクラスがまだ定義されていないこともあります。そのため、参照先のモデルクラスを `related=モ'デルクラス名'` キーワード引数にモデルクラス名を文字列で与えます。

 modeL_sqldemo3.py
```
 rom pathlib import Path
 from blitzdb import Document, SqlBackend
 from blitzdb.fields import ( ForeignKeyField,
                              ManyToManyField,
                              CharField,
                              FloatField,
                              IntegerField,
                              BooleanField )
 
 class Brewery(Document):
     name = CharField()
     country = CharField()
     product = ManyToManyField(related='Beer')
 
 class Beer(Document):
     name = CharField()
     abv = FloatField()
     stock = IntegerField()
     brewery = ManyToManyField(related='Brewery')
 
 data_dir = 'sqldemo'
 dir = Path(data_dir)
 dir.mkdir(exist_ok=True)
 
 url = f'sqlite:///{data_dir}/demo.sqlite'
 engine = create_engine(url, echo=False)
 backend = SqlBackend(engine, ondelete='CASCADE')
 backend.register(Beer)
 backend.register(Brewery)
 backend.init_schema()
 backend.create_schema()
 
 def population_database():
     # Alcohol by Volume (アルコール度数)
     beer_data = [
         { 'name': 'Pale Ale', 'abv': 5.5, 'stock': 6 },
         { 'name': 'ICHII SENSHIN', 'abv': 6.5, 'stock': 6 },
         { 'name': 'ICHIGO ICHIE', 'abv': 5.5, 'stock': 24 },
         { 'name': 'Pilserl', 'abv': 4.9, 'stock': 12 },
     ]
 
     brewery_data = [
         { 'name': 'Minoh', 'country': 'Japan' },
         { 'name': 'Kyoto', 'country': 'Japan' },
         { 'name': 'Plank', 'country': 'Germany' },
     ]
 
     for d in beer_data:
         v = Beer(d)
         v.save(backend)
 
     for d in brewery_data:
         v = Brewery(d)
         v.save(backend)
 
     backend.commit()
 
 if __name__ == '__main__':
     population_database()
     
```

挙動を確認してみましょう。

 pyhton
```
 In [2]: # %load 55_many_to_many.py
    ...: from model_sqldemo3 import *
    ...: from pprint import pprint
    ...:
    ...: plank = backend.get(Brewery, {'name': 'Plank'})
    ...: pilserl = backend.get(Beer, {'name': 'Pilserl'})
    ...:
    ...: pilserl.brewery = plank
    ...: plank.product = pilserl
    ...:
    ...: # pprint(pilserl)
    ...: # pprint(plank)
    ...: # print(pilserl.brewery.country)
    ...: # print(plank.product)
    ...:
 
 In [3]: pprint(pilserl)
 Beer({'name': 'Pilserl', 'abv': 4.9, 'stock': 12, 'pk': '9ebf6b60afee4a2fb676be6f6a256173', 'related_brewery_product': <blitzdb.backends.sql.relations.ManyToManyProxy object at 0x11161eac0>, 'beer_brewery_product': <blitzdb.backends.sql.queryset.QuerySet object at 0x11161e490>, 'brewery': 'Brewery({...})', 'beer_brewery_brewery': <blitzdb.backends.sql.queryset.QuerySet object at 0x11161ed60>})
 
 In [4]: pprint(plank)
 Brewery({'name': 'Plank', 'country': 'Germany', 'pk': '36e3268cb02b4dcd856251a4ebb7b6fa', 'product': 'Beer({...})', 'brewery_beer_product': <blitzdb.backends.sql.queryset.QuerySet object at 0x1115fe1c0>, 'related_beer_brewery': <blitzdb.backends.sql.relations.ManyToManyProxy object at 0x1115fe3a0>, 'brewery_beer_brewery': <blitzdb.backends.sql.queryset.QuerySet object at 0x1115fed30>})
 
 In [5]: print(pilserl.brewery.country)
 Germany
 
 In [6]: print(plank.product)
 Beer({pk : '9ebf6b60afee4a2fb676be6f6a256173'},lazy = False)
 
 In [7]: pprint(plank.product)
 Beer({'name': 'Pilserl', 'abv': 4.9, 'stock': 12, 'pk': '9ebf6b60afee4a2fb676be6f6a256173', 'related_brewery_product': <blitzdb.backends.sql.relations.ManyToManyProxy object at 0x11161eac0>, 'beer_brewery_product': <blitzdb.backends.sql.queryset.QuerySet object at 0x11161e490>, 'brewery': 'Brewery({...})', 'beer_brewery_brewery': <blitzdb.backends.sql.queryset.QuerySet object at 0x11161ed60>})
 
  
```

## SqlBackendでのトランザクション
SqlBackend でのトランザクションは、FileBackend と異なり、自動的にコミットされます。


```
 In [2]: # %load 60_implicit_transaction.py
    ...: from model_sqldemo3 import *
    ...:
    ...: beer = Beer({'name': 'Hysteric IPA', 'abv': 7.0, 'stock': 6})
    ...:
    ...: # 自動的にコミットされる
    ...: backend.save(beer)
    ...: v1 = backend.current_transaction
    ...: v2 = backend._conn
    ...: v3 = backend.get(Beer, {'name': 'Hysteric IPA'})
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v3)
    ...:
 
 In [3]: print(v1)
 None
 
 In [4]: print(v2)
 None
 
 In [5]: print(v3)
 Beer({pk : 'abf7185e1e944dfbbee68c83506596c6'},lazy = False)
 
```

バックエンドの `begin()` メソッドを呼び出すと、明示的にトランザクションが開始します。


```
 In [2]: # %load 61_explicit_transaction.py
    ...: from model_sqldemo3 import *
    ...:
    ...: # 明示的にトランザクションを開始
    ...: transaction = backend.begin()
    ...:
    ...: beer = Beer({'name': 'Hysteric IPA', 'abv': 7.0, 'stock': 6})
    ...: backend.save(beer)
    ...: v1 = backend.current_transaction
    ...: v2 = backend._conn
    ...:
    ...: backend.commit()
    ...: v3 = backend.current_transaction
    ...: v4 = backend._conn
    ...:
    ...: # print(v1)
    ...: # ...
    ...: # print(v4)
    ...:
 
 In [3]: print(v1)
 <sqlalchemy.engine.base.RootTransaction object at 0x10915aa40>
 
 In [4]: print(v2)
 <sqlalchemy.engine.base.Connection object at 0x109228970>
 
 In [5]: print(v3)
 None
 
 In [6]: print(v4)
 None
 
```


## onedelete='CASCADE'

 `model_sqldemo3,py` では、 `SqlBackend()` を呼び出すおときに、引数に　 `ondelete='CASCADE'` を与えていました。
フィールドのタイプに `ForeignKeyField` や  `ManyToManyField` が指定されているとき、参照されている側のレコードが削除されたときは、それを参照しているレコードも一緒に削除したいというときに使用します。

## SqlBackend のTips
SQLAlchemy 経由で SQLite を使えるわけなので、次のようにデータベースと接続するとメモリ上にデータベースを構築することができます。


```
 from sqlalchemy import create_engine
 
 engine = create_engine('sqlite:///:memory:', echo=False)
 backend = SqlBackend(engine)
 
```



## まとめ
Blitzdb は軽量でありながら、リクエスト数が中規模程度のアプリケーションにも対応可能なデーターストアです。ほんな僅かな手間でデータストアとしての機能を果たしてくれます。また、バックエンドを変更することで、SQLAlchmey を経由した多く種類のデータベースシステムや、MongoDB にデータを格納することができます。
シンプルでありながらもクエリ演算子は柔軟に組み合わせて使えるなど利便性は高いと言えるでしょう。

## 参考
- [BlitzDBソースコード ](https://github.com/adewes/blitzdb)
- [BlitzDB3 ソースコード　](https://github.com/abilian/blitzdb3)


