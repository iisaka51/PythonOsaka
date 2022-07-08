ZODBを使ってみよう
=================
## ZODBについて
#### ZODB (Zope Object Database) 

- コードとデータベースのシームレスな統合。
- データベースに関連する操作のための別の言語（SQL）は不要。
- データベースマッパー（ORM)は不要。

オブジェクトデータベースという言葉に馴染みがないかもしれませんが、わかりやすい言葉でいうと、「オブジェクト」を格納するデータベースです。リレーショナル・データベースなどのような「レコード」や「テーブル」はありません。 「コレクション」を持っていて、 `pickle` モジュールでのシリアライズ/ディシリアライズのようなアクセス方法を行います。

もっと大まかにいいうと、クラスから生成したインスタンスオブジェクトをそのまま格納でき、取り出したオブジェクトは、そのオブジェクトが持っているメソッドなどにすぐにアクセスできるといったものです。

ZODBは次ののような場合に適しています。

- 開発者がデータベースのコードをたくさん作るよりも、アプリケーションに集中したい場合。
- アプリケーションに複雑な関係やデータ構造が多い場合。
- データの読み取り操作が、書き込み操作よりも比較的大きい場合。

その一方で、ZODBは次のような弱点があります。

- オブジェクト構造がそのまま格納されるためデータ構造を柔軟性に変更できない
- アプリケーションが大量のデータ書き込み操作を必要とする要求使用には適していない
- 格納するデータによってはデータサイズが大きくなることがある
- 起動時にインデックスを読み込むため起動が遅い

データ構造の問題は `pickle` での場合も問題となってしまうものです。
大量のデータ書き込みについては、ZEO という ZODB をサービス化する Python モジュールもあり、不特定多数対しての大量なアクセスを行うようなアプリケーションでないのであれば、あまり問題視するレベルではありません。

## インストール
ZODBをインストールするには、次のコマンドを使用します。

 bash
```
 $ pip install ZODB
```

## ZODBの使い方
データベースとの接続を確立する簡単なサンプルは次のようなものです。


```
 In [2]: # %load 01_connection.py
    ...: import ZODB, ZODB.FileStorage
    ...:
    ...: storage = ZODB.FileStorage.FileStorage('mydata.fs')
    ...: db = ZODB.DB(storage)
    ...: connection = db.open()
    ...: root = connection.root
    ...:
 
 In [3]: !ls mydata*
 mydata.fs	mydata.fs.index	mydata.fs.lock	mydata.fs.tmp
```

ZODBを使うためには「ストレージ 」へ接続して「接続オブジェクト」から「ルートオブジェクト」を作成します。（この例では  `root` ）。

ZODBには次にようになストレージ・バックエンドをサポートしています。
- **FileStorage**
これがデフォルトです。すべてのデータは1つの大きなData.fsファイルに保存され、基本的にトランザクションログです。
- MappingStorage
インメモリデータベースの実装です。
- DemoStorage
読み取り専用のベースデータベースに対する変更を保存するストレージ
- **DirectoryStorage**
オブジェクトリビジョンごとに1つのファイルを保存します。この場合、不完全なシャットダウン時にData.fs.indexを再構築する必要はありません。
- **RelStorage**
リレーショナルデータベースにシリアライズ化して保存します。PostgreSQL、MySQL、Oracleに対応しています。

ZODBデータベースを作成するには、ストレージオブジェクト、データベースオブジェクト、そして最後に接続オブジェクトが必要です。

まず、ストレージオブジェクトを作成します。
前述の例では、 `mydatabse.fs` ファイルを使ってオブジェクト情報を保存するストレージオブジェクトを作成しています。次に、そのストレージオブジェクトからデータベースオブジェクト（ `db` ）を作成します。

次に、 `open()` メソッドを呼び出してデータベースを「オープン」する必要があります。これにより、データベースへの接続オブジェクトが返されます。この接続オブジェクトは、 `root()` メソッドによって、データベースのルートオブジェクトにアクセスすることができるようになります。

ZODBのストレージ・バックエンドは `FileStorage` がデフォルトになるため、次のように簡潔に記述することもできます。


```
 In [2]: # %load 02_connection_short.py
    ...: import ZODB
    ...:
    ...: db = ZODB.DB('mydata.fs')
    ...: connection = db.open()
    ...: root = connection.root
    ...:
    
```

メモリ上にデータベースを格納する場合は、次のようにします。

```
 In [2]: # %load 03_inmemory.py
    ...: import ZODB
    ...:
    ...: db = ZODB.DB(None)
    ...: connection = db.open()
    ...: root = connection.root
    ...:
 
```

接続するデータベースが１つしかない場合は、 `connection()` に直接ファイル名を記述することができます。

```
 In [2]: # %load 04_single_db.py
    ...: import ZODB
    ...:
    ...: connection = ZODB.connection('mydata.fs')
    ...: memory_connection = ZODB.connection(None)
    ...:
 
```

以降なんどもデータベースに接続することになるので、次のようなモジュールを作っておきましょう。
 zodb_mydata.py
```
 import ZODB
 
 connection = ZODB.connection('mydata.fs')
 root = connection.root
```

ルート・オブジェクトは、すべての永続的なオブジェクトを格納する辞書です。例えば、文字列の単純なリストをルート・オブジェクトに格納することができます。


```
 In [2]: # %load 05_store_objectt.py
    ...: from zodb_mydata import *
    ...:
    ...: root.member = ['Freddie', 'Brian', 'John', 'Roger']
    ...:
 
```

ルート・オブジェクトは、すべての永続的なオブジェクトを格納する辞書だと説明しましたが、ルート・オブジェクトのトップにオブジェクトを格納するためにはドット表記を使用します。インデックス表記では次のようなエラーになります。

```
 In [3]: root['member'] = ['Freddie', 'Brian', 'John', 'Roger']
 ---------------------------------------------------------------------------
 TypeError                                 Traceback (most recent call last)
 <ipython-input-3-ff584a2f0242> in <module>
 ----> 1 root['member'] = ['Freddie', 'Brian', 'John', 'Roger']
 
 TypeError: 'RootConvenience' object does not support item assignment
 
```

## トランザクション
ルート・オブジェクトに新しいオブジェクトを追加してデータベースを変更しましたが、この変更はまだ一時的なものです。ZODBはトランザクションもサポートしていて、変更を永続的にするには、現在のトランザクションをコミットする必要があります。
トランザクションは、複数の変更を1つの塊としまとめて操作します。トランザクションのコミットは、これまでにオブジェクトに加えた変更を保存する「チェックポイント」のようなものです。
実際にデータを格納するためには、 `commit()` としから接続オブジェクトを `close()` します。


```
 In [2]: # %load 06_commit.py
    ...: from zodb_mydata import *
    ...: import transaction
    ...:
    ...: root.member = ['Freddie', 'Brian', 'John', 'Roger']
    ...:
    ...: transaction.commit()
    ...: connection.close()
    ...:
    
```

ここで、一旦Python を終了してから、再度データベースに接続してルート・オブジェクトを取得します。

```
 In [2]: # %load 07_check_data.py
    ...: from zodb_mydata import *
    ...:
    ...: root.member
    ...:
 Out[2]: ['Freddie', 'Brian', 'John', 'Roger']
 
```

変更した内容を破棄したいときは、 `commit()` の代わりに `abort()` を使います。

```
 In [2]: # %load 08_abort.py
    ...: from zodb_mydata import *
    ...: import transaction
    ...:
    ...: root.member = ['Adam', 'Brian', 'John', 'Roger']
    ...:
    ...: transaction.abort()
    ...: connection.close()
    ...:
    \
```


```
 In [2]: # %load 07_check_data.py
    ...: from zodb_mydata import *
    ...:
    ...: root.member
    ...:
 Out[2]: ['Freddie', 'Brian', 'John', 'Roger']
 
```

リレーショナルデータベースを使っている場合であれば、この例のような単純なPythonのリストを保存するためだけにも、SQL文でクエリを実行しなければなりません。また、読み出すときも、別のSQL文のクエリ実行して、リストオブジェクトに戻すコードが必要になります。ZODBでは、このような作業は一切必要ありません。

## オブジェクトの保存
あるオブジェクトをZODBに格納するにためは、すでにデータベースに存在している他のオブジェクトに、そのオブジェクトを添付するだけです。つまり、ルートオブジェクトはブートストラップの役割を果たします。ルートオブジェクトは、データベースのトップレベルのオブジェクトの名前空間としての役割を果たします。

いま次のような辞書にユーザデータが定義されているとします。
 user_data.py
```
 user_data = [
     { 'name': 'John',
       'birthday': {'year': 1951, 'month': 8, 'day': 19},
       'country-code': 'GB'
     },
     { 'name': 'Freddie',
       'birthday': {'year': 1946, 'month': 9, 'day': 5},
       'country-code': 'GB'
     },
     { 'name': 'Brian',
       'birthday': {'year': 1947, 'month': 7, 'day': 19},
       'country-code': 'GB'
     },
     { 'name': 'Roger',
       'birthday': {'year': 1949, 'month': 7, 'day': 26},
       'country-code': 'GB'
     },
 ]
 
```

これをZODBに格納する場合にルート・オブジェクトに添付すればよいと説明しましたが、次のような記述は自由度がないため避けるべきです。

```
 In [2]: # %load 10.stora_object.py
    ...: from zodb_mydata import *
    ...: from user_data import *
    ...:
    ...: root.devops = user_data
    ...:
    
```

こうしたときは、 `BTree` クラスを使います。格納するオブジェクトが多数になってもルート・オブジェクトが汚れません。

```
 In [2]: # %load 11.stora_object_btree.py
    ...: from zodb_mydata import *
    ...: from BTrees.OOBTree import BTree
    ...: from user_data import *
    ...:
    ...: root.users = BTree()
    ...: root.users['devops'] = user_data
    ...:
    
```

もう一つの方法は、アプリケーション固有のルートを提供するデータベースのルートに永続的なオブジェクトを割り当てることです。

```
 root.app_root = user_app()
 root.task_root = task_app()
 
```

## コンテナと検索
 `BTree` クラスは、ZODBのコアとなるスケーラブルなコンテナとインデックス作成機能を提供します。BTreeにはたくさんの種類があります。が、最も一般的なものは、オブジェクトのキーと値を持つ**OOBTree(Object Oriented Binary Tree )**です。また、整数のキーと値をサポートする特殊なBTreeもあります。整数は、オブジェクトよりも効率的に保存でき、比較も迅速に行えるため、アプリケーションレベルのオブジェクト識別子としてよく使用されます。
BTreeを使用する際には、そのキーが安定した順序であることを確認することが重要になります。

ZODBはクエリエンジンを提供していません。ZODBのオブジェクトにアクセスする主な方法は、他のオブジェクトをトラバース(traverse)することです。(補足: 属性やアイテムにアクセスしたり、メソッドを呼び出したりすること）
オブジェクトのトラバースは、通常は検索よりもはるかに高速に処理されます。

必要に応じて、BTreeを使ってインデックスを構築し、効率的な検索を行うことができます。もし、あなたのアプリケーションが検索中心であったり、そのようなデータアクセス方法を好むのであれば、ZODBはあなたにとって最適なテクノロジーではないかもしれません。
ZODBをあきらめるまえに、[Newt DB http://www.newtdb.org/en/latest/how-it-works.html]プロジェクトを検証する価値かもしれません。このプロジェクトは、ZODBとPostgreSQLを組み合わせて、インデックス、検索、Python以外のアプリケーションからのアクセスを可能にするものです。

## 変更の検出
ZODBが使いやすい理由の一つは、変更内容を記録しておく必要がないことです。永続的なオブジェクトに変更を加え、トランザクションをコミットするだけですみます。通常は、変更されたものはすべてデータベースに保存されます。

ただし、リストや辞書のようなPythonの単純な変更可能な型に関しては、注意が必要です。
このルールに1つの例外があります。既にデータベースに保存されているリストや辞書を変更しても、その変更は反映されません。

次の例は、リストオブジェクト `data` を root.member にセットしてコミットしています。
この後、data に `Adam` を追加しています。
 `v1` と `v2` にオブジェクトをセットしている段階では何も問題ないように見えます。
しかし、すでにコミットされているためデータベースには追加のデータがあるますが、ZODBはその後  `data` の内容が追加されてもそれを検知することができません。


```
 In [1]: %load 20_dectect_change.py
 
    ...: import transaction
    ...:
    ...:
    ...: root.member = ['Freddie', 'Brian', 'John', 'Roger']
    ...: transaction.commit()
    ...: connection.close()
    ...:
    ...:
    ...: connection = ZODB.connection('mydata.fs')
    ...: root = connection.root
    ...: v1 = root.member
    ...: root.member[0] = 'Adam'
    ...: transaction.commit()
    ...: v2 = root.member
    ...: connection.close()
    ...:
    ...: connection = ZODB.connection('mydata.fs')
    ...: root = connection.root
    ...: v3 = root.member
    ...: connection.close()
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v3)
    ...:
 
 In [3]: print(v1)
 ['Adam', 'Brian', 'John', 'Roger']
 
 In [4]: print(v2)
 ['Adam', 'Brian', 'John', 'Roger']
 
 In [5]: print(v3)
 ['Freddie', 'Brian', 'John', 'Roger']
 
```

この場合は、データベースのオブジェクトに対して直接変更を加えるのではなく、いちど他のオブジェクトにコピーした上で変更し、それをデータベースのオブジェクトにセットして置き換える必要があります。

```
 In [2]: # %load 21_reassigning.py
    ...: from zodb_mydata import *
    ...: import transaction
    ...:
    ...: member = root.member
    ...: member[0] = 'Adam'
    ...: root.member = member
    ...: v1 = member
    ...: transaction.commit()
    ...: connection.close()
    ...:
    ...: connection = ZODB.connection('mydata.fs')
    ...: root = connection.root
    ...: v2 = root.member
    ...: connection.close()
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 ['Adam', 'Brian', 'John', 'Roger']
 
 In [4]: print(v2)
 ['Adam', 'Brian', 'John', 'Roger']
 
```

## Persistent クラス
ZODBに変更を通知する変更可能オブジェクトを作成する最も簡単な方法は、Persistentクラスを作成することです。Persistentクラスを使うと、独自の種類のオブジェクトをデータベースに保存することができます。
Persistentクラスを作成するには、Persistent.Persistentクラスを継承してクラスを作成します。ZODBが行ういくつかの特別な内部処理のため、Persistentをインポートする前に、まずZODBをインポートする必要があります。Persistentモジュールは、ZODBをインポートしたときに実際に作成されます。

まず、次のようなPersistentクラスの派生クラス Member を作成します。
 zodb_members.py
```
 import ZODB
 from persistent import Persistent
 
 class Member(Persistent):
     def setName(self, name):
         self.name = name
     def getName(self)
         return self.name
         
```


```
 In [2]: # %load 22_persistent.py
    ...: from zodb_mydata import *
    ...: from zodb_members import Member
    ...: import transaction
    ...:
    ...: members = []
    ...:
    ...: for name in ['Freddie', 'Brian', 'John', 'Roger']:
    ...:    member = Member()
    ...:    member.setName(name)
    ...:    members.append(member)
    ...:
    ...: root.members=members
    ...: transaction.commit()
    ...:
    ...: vocal = root.members[0]
    ...: vocal.setName('Adam')
    ...: transaction.commit()
    ...: connection.close()
    ...:
    
```

Persistentの派生クラス MemberクラスとしてZODBに登録したデータは、データをコピーしなくても変更（更新、追加、削除）を行うことができるようになります。
変更した場合は `commit()` を忘れないように実行してください。


```
 In [2]: # %load 23_persistent_check.py
    ...: from zodb_mydata import *
    ...:
    ...: v1 = root.members
    ...: v2 = root.members[0].getName()
    ...:
    ...: connection.close()
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:
    ...:
 
 In [3]: print(v1)
 [<zodb_members.Member object at 0x10e2923c0 oid 0xd in <Connection at 10e293400>>, <zodb_members.Member object at 0x10e292430 oid 0xe in <Connection at 10e293400>>, <zodb_members.Member object at 0x10e2924a0 oid 0xf in <Connection at 10e293400>>, <zodb_members.Member object at 0x10e292510 oid 0x10 in <Connection at 10e293400>>]
 
 In [4]: print(v2)
 Adam
 
```

## 変更属性
ZODBがPythonのリストのような通常の変更可能オブジェクト(mutable object)の変更を検出できないことは説明しました。この問題は、永続的なインスタンスを使用する場合にも影響します。これは、Persistentクラスのインスタンスオブジェクトが、通常の変更可能オブジェクトである属性を持つことができるからです。
まず、前述した  `zodb_members.py` を次のように修正しましょう。

 zodb_members_new.py
```
 import ZODB
 from persistent import Persistent
 
 class Member(Persistent):
     def __init__(self):
         self.members = []
     def setName(self, name):
         self.name = name
     def getName(self):
         return self.name
     def add_member(self, name):
         self.members.append(name)
         self._p_changed = 1
         
```

 `add_member()` メソッドを呼び出したとき、ZODBはmutable属性である `self.members` が変更されたことを知ることはできません。前述したように、 `self.members` を変更した後に再割り当てすることで、この問題を回避することができます。しかし、Persistentクラスの派生インスタンスオブジェクトを使用している場合は、別の選択肢があります。インスタンスが変更されたことを、 `_p_changed` 属性を使ってZODBに通知することができます。

このオブジェクトが変更されたことを通知するには、 `_p_changed` 属性を1に設定します。多くの変更を加えた場合でも、ZODBに通知するのは一度だけで構いません。

この `_p_changed` フラグは、P:ersistentクラスの派生クラスを作成するときに守る必要があるルールのひとつです。

## BTree
前述の例で使用した BTressモジュールは、ZODBをインストールすると一緒にインストールされるパッケージのひとつです。
ZODBを使ったプログラミングでは非常に重要な役割を果たします。ZODBではPythonの辞書が必ずしも必要とされるわけではありません。例えば、非常に大きなマッピングを保存したい場合です。ZODBでPython辞書にアクセスすると、辞書全体をアンピックル化してメモリに持ってこなければなりません。仮に10万エントリのユーザーデータベースのような非常に大きなものを保存する場合、そのような大きなオブジェクトではメモリ使用量は大きくなり、アンピックルにも時間がかかります。BTreeはバランスのとれたツリーデータ構造で、マッピングのように動作しますが、キーをいくつかのツリーノードに分散させます。ノードはソートされた状態で保存されています。ノードは、アクセスされたときだけアンピックルされてメモリに取り込まれるので、ツリー全体がメモリを占有する必要はありません。

BTreesパッケージは、関連するデータ構造のコレクションを提供しています。これらのデータ構造には整数に特化したものがあり、高速でメモリ使用量も少なくて済みます。これらのデータ構造を扱うモジュールがあります。モジュール名の最初の2文字は、マッピングのキーと値の型を指定します。 `O` は任意のオブジェクト、 `I` は32ビット符号付き整数、 `F` は32ビット浮動小数点数です。例えば、BTrees.IOBTreeモジュールは、整数のキーと任意のオブジェクトを値とするマッピングを提供しています。

- **OOBTree**
- **OBTree**
- **OIBTree**
- **IIBTree**
- **IFBTree**


各モジュールが提供するデータ構造は次の４つです。

- **BTree**
- **Bucket**
- **TreeSet**
- **Set**

BTree型とBucket型はマッピングで、 `update()` や `keys()` などの通常のマッピングメソッドをすべてサポートしています。TreeSet型とSet型はマッピングに似ていますが、値を持ちません。キーを持たないマッピングに適したメソッド、例えば `keys()` はサポートしますが、 `items()` はサポートしません。バケット型とセット型は、それぞれBTreeとTreeSetsの個々の構成要素です。バケット型やセット型は、要素数が少ないことが確実な場合に使用します。データ構造が大きくなる場合は、BTreeやTreeSetを使うべきです。Pythonのリストのように、BucketやSetは連続した1つのピースで割り当てられ、挿入や削除には既存の要素数に比例した時間がかかります。また、Pythonのリストのように、BucketやSetは1つのオブジェクトであり、全体でピクル化/アンピクル化が行われます。BTreeやTreeSetsは複数レベルのツリー構造で、ワーストケースの時間制限がはるかに改善されています。ツリー構造は複数のオブジェクトから構築され、ZODBは必要に応じて個別にロードすることができます。

BTree および TreeSet型の ` keys()` 、 `values()` 、および  `items() ` メソッドは、すべてのデータを含むリストを実体化しません。その代わり、必要に応じてBTreeからデータを取得する遅延シーケンスを返します。また、「範囲検索」と呼ばれる、返す値の最小値と最大値を指定するオプションの引数もサポートしています。これらの型はすべてソートされた状態で保存されているため、範囲検索は非常に効率的です。

バケット型やセット型の `key()` 、 `values()` 、 `items()` メソッドは、すべてのデータを含むリストを返します。イテレータを返す `iterkeys()` 、 `itervalues()` 、 `iteritems()` メソッドもあります。これらのメソッドは、BTreeとTreeSetオブジェクトにも適用されます。

BTree オブジェクトは、マッピングに期待されるすべてのメソッドをサポートしていますが、キーがソートされていることを利用したいくつかの拡張機能があります。以下の例では、いくつかのメソッドがどのように動作するかを示しています。追加のメソッドとしては、 `minKey() ` と  `maxKey() ` があり、オプションの  `bound` 引数を使ってキーの最小値と最大値を求めることができます。また、  `byValue() ` はおそらく無視すべきでしょう (何をするのかを正確に説明するのは難しく、結果としてほとんど使用されません。) キー、値、アイテムを列挙する様々なメソッドは、最小および最大の `key` 引数（"範囲検索"）や、オプションの `pool` 引数を受け付け、範囲検索が範囲の端点を含むか含まないかを制御します。


```
 In [2]: # %load 30_btrees.py
    ...: from BTrees.OOBTree import OOBTree
    ...:
    ...: t = OOBTree()
    ...: t.update({1: "heart", 2: "diamond", 3: "spade", 4: "club"})
    ...: s = t.keys()
    ...:
    ...: v1 = len(t)
    ...: v2 = t[2]
    ...: v3 = len(s)
    ...: v4 = s[-2]
    ...: v5 = list(s)
    ...: v6 = list(t.values())
    ...: v7 = list(t.values(1, 2))
    ...: v8 = list(t.values(2))
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v3)
    ...: # print(v4)
    ...: # print(v5)
    ...: # print(v6)
    ...: # print(v7)
    ...: # print(v8)
    ...:
 
 In [3]: print(v1)
 4
 
 In [4]: print(v2)
 diamond
 
 In [5]: print(v3)
 4
 
 In [6]: print(v4)
 3
 
 In [7]: print(v5)
 [1, 2, 3, 4]
 
 In [8]: print(v6)
 ['heart', 'diamond', 'spade', 'club']
 
 In [9]: print(v7)
 ['heart', 'diamond']
 
 In [10]: print(v8)
 ['diamond', 'spade', 'club']
 
```



```
 In [2]: # %load 31_btrees_methods.py
    ...: from BTrees.OOBTree import OOBTree
    ...:
    ...: t = OOBTree()
    ...: t.update({1: "red", 2: "green", 3: "blue", 4: "spades"})
    ...:
    ...: v1 = list(t.values(min=1, max=4))
    ...: v2 = list(t.values(min=1, max=4, excludemin=True, excludemax=True))
    ...: v3 = t.minKey()
    ...: v4 = t.minKey(1.5)
    ...: v5 = t.has_key(4)
    ...: v6 = t.has_key(5)
    ...: v7 = 4 in t
    ...: v8 = 5 in t
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v3)
    ...: # print(v4)
    ...: # print(v5, v6)
    ...: # print(v7, v8)
    ...:
 
 In [3]: print(v1)
 ['red', 'green', 'blue', 'spades']
 
 In [4]: print(v2)
 ['green', 'blue']
 
 In [5]: print(v3)
 1
 
 In [6]: print(v4)
 2
 
 In [7]: print(v5, v6)
 True False
 
 In [8]: print(v7, v8)
 True False
 
```


```
 In [1]: %load 32_btrees_iteration.py
    ...: from BTrees.OOBTree import OOBTree
    ...:
    ...: t = OOBTree()
    ...: t.update({1: "red", 2: "green", 3: "blue", 4: "spades"})
    ...:
    ...: v1 = t.keys()
    ...: v2 = t
    ...: v3 = t.iteritems()
    ...:
    ...: def func1():
    ...:     for k in t.keys():
    ...:         print(f'{k} ', end='')
    ...:
    ...: def func2():
    ...:     for k in t:
    ...:         print(f'{k} ', end='')
    ...:
    ...: def func3():
    ...:     for k in t.iteritems():
    ...:         print(f'{k} ', end='')
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v3)
    ...: # func1()
    ...: # func2()
    ...: # func3()
    ...:
 
 In [3]: print(v1)
 <OOBTreeItems object at 0x1080a0a70>
 
 In [4]: print(v2)
 <BTrees.OOBTree.OOBTree object at 0x106ee3640>
 
 In [5]: print(v3)
 <BTrees.OOBTree.OOTreeIterator object at 0x107070f90>
 
 In [6]: func1()
 1 2 3 4
 In [7]: func2()
 1 2 3 4
 In [8]: func3()
 (1, 'red') (2, 'green') (3, 'blue') (4, 'spades')
 
```

## 全体順序付けと永続性
BTreeベースのデータ構造は、いくつかの基本的な点でPythonの `dict` 型とは異なります。最も重要な点の1つは、dictではキーがハッシュコードと等値比較をサポートする必要がありますが、BTreeベースの構造ではハッシュコードを使用せず、キーに全体的な順序付けを必要とします。

#### 全体順序化(Total orderin)

- **再帰性(Reflexive)**： 各 `x` に対して、 `x == x` が真である。
- **三分法(Trichotomy)**： 各 `x` と `y` に対して、 `x < y` 、 `x == y` 、 `x > y` のうち、正確に1つが真である。
- **転移性(Transitivity)**：  `x <= y` かつ  `y <= z` のときは、 `x <= z` も真である。

Pythonに付属するほとんどのオブジェクトのデフォルトの比較関数は、後で説明するいくつかの重要な注意点を除いて、これらのルールを満たしています。複素数は  `==` と  `!=` の比較しかサポートしておらず、それ以外の方法で比較しようとすると例外が発生します。複素数は三分法のルールを満たさず、BTreeベースのデータ構造のキーとして使用してはいけません（ただし、複素数はPythonのdictのキーとして使用することができます。

BTreeベースの構造でキーとして使用しても完全に安全なオブジェクトの例としては、int、long、float、8ビット文字列、Unicode文字列、完全に安全な型のオブジェクトで構成された（おそらく再帰的に）タプルなどがあります。

ここで重要なのは、たとえ2つの型がそれぞれルールを満たしていても、それらの型のオブジェクトを混ぜるとルールを満たさない場合があるということです。例えば、8ビット文字列とUnicode文字列はどちらも全順序を提供しますが、この2つを混ぜると三分法が失われます。例えば、 `'x' < chr(255) and u'x' == 'x'` ですが、 `chr(255)` と `u'x'` を比較しようとすると例外が発生します。このような理由もあって（他にも理由はありますが）、1つのBTreeベースの構造で複数の型を持つキーを使用するのは危険です。そのようなことをしなければ、心配する必要はありません。

もう1つの潜在的な問題は**変異性(mutability)**です。あるキーがBTreeベースの構造に挿入されたとき、そのキーは時間が経っても他のキーとの相対的な順序が変わらないようにしなければなりません。BTreeベースの構造では、キーを挿入する際、他のキーとの相対的な順序を維持しなければなりません。例えば、リストは全体的な順序を提供します。


```
 In [2]: # %load 33_btrees_mutability.py
    ...: from BTrees.OOBTree import OOSet
    ...:
    ...: L1, L2, L3 = [1], [2], [3]
    ...: s = OOSet((L2, L3, L1))
    ...:
    ...: v1 = list(s.keys())
    ...: v2 = s.has_key([3])
    ...: v3 = L2[0] = 5
    ...: v4 = s.has_key([3])
    ...:
    ...: # print(s)
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v3)
    ...: # print(v4)
    ...:
 
 In [3]: print(s)
 OOSet([[1], [5], [3]])
 
 In [4]: print(v1)
 [[1], [5], [3]]
 
 In [5]: print(v2)
 True
 
 In [6]: print(v3)
 5
 
 In [7]: print(v4)
 False
 
```

キールックアップは、キーがソートされたままであることに依存しています（効率的なバイナリサーチの形式が使用されます）。キーL2を挿入した後に変異させることで、OOSetがソートされているという不変性を破壊してしまいます。その結果、このセットに対する将来のすべての操作は予測できなくなってしまいます。

この問題のより微妙な変化は永続性のために発生します。デフォルトでは、Pythonは2つのオブジェクトのメモリアドレスを比較することでいくつかの種類の比較を行います。Python はオブジェクトをメモリ上で移動させないので、これはプログラムの実行期間中、使用可能な全体順序を提供します（オブジェクトのメモリアドレスは変更されません）。しかし、この方法で比較されたオブジェクトが、データベースに格納されているBTreeベースの構造のキーとして使用された場合、オブジェクトが再びデータベースから読み込まれたときに、ほぼ確実に異なるメモリアドレスになってしまいます。BTreeにK1とK2が挿入された時点で、キーK1のメモリアドレスがキーK2のメモリアドレスよりも小さかったとしても、後でデータベースからBTreeを読み込んだときに、K1のアドレスがK2のアドレスよりも小さくなるという保証はありません。その結果、様々な操作が期待通りに動いたり動かなかったりするため、一見ランダムなBTreeになってしまいます。

## イテレーションとミューテーション
Pythonの辞書やリストと同様に、BTreeベースのデータ構造を反復しながら変更することはできません。ただし、反復しながら既存のキーに関連する値を変更することは問題ありません。反復処理中に既存のキーに関連付けられた値を置き換えることは問題ありません。反復処理中にキーを削除したり、新しいキーを追加したりしても、構造体に内部的な損傷を与えることはありませんが、結果は不定で予測できないものになります。BTreeベースの構造体のサイズが反復処理中に変更された場合に `RuntimeError` を発生させようとする試みが実装されていますが、このようなケースのすべてを捉えることはできないため、信頼性が低いことに注意してください。


```
 In [2]: # %load 35_iteration_mutation.py
    ...: from BTrees.IIBTree import *
    ...: s = IISet(range(10))
    ...: v1 = list(s)
    ...:
    ...: def func1():
    ...:     for i in s:
    ...:         print(f'{i} ', end='')
    ...:         s.remove(i)
    ...:
    ...: v2 = list(s)
    ...:
    ...: # print(v1)
    ...: # func1()
    ...: # print(v2)
    ...:
 
 In [3]: print(v1)
 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
 
 In [4]: func1()
 0 2 4 6 8 ---------------------------------------------------------------------------
 RuntimeError                              Traceback (most recent call last)
 <ipython-input-4-d88c41ef3303> in <module>
 ----> 1 func1()
 
 <ipython-input-2-683390a04f0e> in func1()
       5
       6 def func1():
 ----> 7     for i in s:
       8         print(f'{i} ', end='')
       9         s.remove(i)
 
 RuntimeError: the bucket being iterated changed size
 
 In [5]: print(v2)
 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
 
 In [6]: func1()
 1 5 9
 In [7]: func1()
 3 ---------------------------------------------------------------------------
 RuntimeError                              Traceback (most recent call last)
 <ipython-input-7-d88c41ef3303> in <module>
 ----> 1 func1()
 
 <ipython-input-2-683390a04f0e> in func1()
       5
       6 def func1():
 ----> 7     for i in s:
       8         print(f'{i} ', end='')
       9         s.remove(i)
 
 RuntimeError: the bucket being iterated changed size
 
```

Pythonの辞書やリストと同様に、BTreeベースの構造体を反復しながら変更する安全で予測可能な方法は、キーのコピーを反復することです。

```
 In [2]: # %load 36_iteration_safe_mutation.py
    ...: from BTrees.IIBTree import *
    ...: s = IISet(range(10))
    ...:
    ...: def func1():
    ...:     for i in list(s.keys()):
    ...:         print(f'{i} ', end='')
    ...:         s.remove(i)
    ...:
    ...: # s
    ...: # s.keys()
    ...: # func1()
    ...: # s.keys()
    ...: # s
    ...:
 
 In [3]: s
 Out[3]: IISet([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
 
 In [4]: s.keys()
 Out[4]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
 
 In [5]: func1()
 0 1 2 3 4 5 6 7 8 9
 In [6]: s.keys()
 Out[6]: []
 
```

## ZODB ユーティリティー
ZODBには便利なユーティリティー関数が提供されています。

### 64ビット正数と64ビット文字列
ZODBでは64ビットのトランザクションIDを使用していて、通常は文字列として表されますが、整数として操作されることもあります。オブジェクトIDも文字列であり、整数をパックしただけの64ビット文字列が存在するのが一般的です。

関数  `p64` および  `u64` は、整数を文字列としてパックおよびアンパックします。
また、定数  `z64` は、64ビットの文字列としてゼロがパックされています。



```
 In [2]: # %load 40_utils_int_str.py
    ...: import ZODB.utils
    ...:
    ...: v1 = ZODB.utils.p64(12345678901234567890)
    ...: v2 = ZODB.utils.u64(b'\xabT\xa9\x8c\xeb\x1f\n\xd2')
    ...: v3 = ZODB.utils.z64
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v3)
    ...:
 
 In [3]: print(v1)
 b'\xabT\xa9\x8c\xeb\x1f\n\xd2'
 
 In [4]: print(v2)
 12345678901234567890
 
 In [5]: print(v3)
 b'\x00\x00\x00\x00\x00\x00\x00\x00'
 
```

### トランザクションIDの生成
ZODBのストレージでは、トランザクションがコミットされると、トランザクションIDが割り当てられます。これらはUTC時間に基づいていますが、厳密に増加させなければなりません。 `newTid()` 関数はこれをとても簡単に行うことができます。

動作確認を行うために、まず  `time.time()` がいつも同じ値を返すようにハックしたモジュールを用意します。
 fake_time.py
```
 import time
 
 # time.time() が同じ値を返すようにするハック
 old_time = time.time
 def fake_time():
     return 1224825068.12
 
 time.time = fake_time
 
```

これで、新しいタイムスタンプを要求すると、fake_time に基づいたタイムスタンプが得られます。
 `newTid()` は、引数として古い  `tid` が必要になります。トランザクションIDがない場合、 `tid` は `None` を与えます。
この時間は現在の時間に基づいており、タイムスタンプに変換することで確認することができます。


```
 In [2]: # %load 41_newTid_timetamp.py
    ...: import ZODB.utils
    ...: import ZODB.TimeStamp
    ...: from fake_time import *
    ...:
    ...: tid1 = ZODB.utils.newTid(None)
    ...: tid2 = ZODB.utils.newTid(tid1)
    ...:
    ...: v1  = ZODB.TimeStamp.TimeStamp(tid1)
    ...: v2  =  ZODB.utils.u64(tid1), ZODB.utils.u64(tid2)
    ...:
    ...: # print(tid1)
    ...: # print(tid2)
    ...: # print(v1)
    ...: # print(v2)
    ...:
 
 In [3]: print(tid1)
 b'\x03yi\xf7"\xa54\x88'
 
 In [4]: print(tid2)
 b'\x03yi\xf7"\xa54\x89'
 
 In [5]: print(v1)
 2008-10-24 05:11:08.120000
 
 In [6]: print(v2)
 (250347764454864008, 250347764454864009)
 
```

### ロッキングサポート
ZODBでのストレージはスレッドセーフであることが求められます。ロッキングはその自動化に役立ちます。ロッキングは、関数が呼び出されたときにロックを取得し、関数が終了したときにロックを解放するようにします。

はじめに次のようなモジュールを用意します。
 zodb_lock.py
```
 import ZODB.utils
 
 class Lock:
     def acquire(self):
         print('acquire')
     def release(self):
         print('release')
     def __enter__(self):
         return self.acquire()
     def __exit__(self, *ignored):
         return self.release()
         
```


```
 In [2]: # %load 42_locking.py
    ...: from zodb_precondition import *
    ...:
    ...: class C:
    ...:     _lock = Lock()
    ...:     _lock_acquire = _lock.acquire
    ...:     _lock_release = _lock.release
    ...:
    ...:     @ZODB.utils.locked
    ...:     def meth(self, *args, **kw):
    ...:         print('meth %r %r' %(args, kw))
    ...:
    ...: # C().meth(1, 2, a=3)
    ...:
 
 In [3]: C().meth(1, 2, a=3)
 acquire
 meth (1, 2) {'a': 3}
 release
 
```


### 前提条件
しばしば，メソッドの前提条件を指定したくなることがあります．ロッキングでは、オプションでメソッドの前提条件をサポートしています。


```
 In [2]: # %load 43_precondition.py
    ...: from zodb_precondition import *
    ...:
    ...: class C:
    ...:     def __init__(self):
    ...:         self._lock = Lock()
    ...:         self._opened = True
    ...:         self._transaction = None
    ...:
    ...:     def opened(self):
    ...:         print('checking if open')
    ...:         return self._opened
    ...:
    ...:     def not_in_transaction(self):
    ...:         print('checking if in a transaction')
    ...:         return self._transaction is None
    ...:
    ...:     @ZODB.utils.locked(opened, not_in_transaction)
    ...:     def meth(self, *args, **kw):
    ...:         print('meth %r %r' % (args, kw))
    ...:
    ...: c = C()
    ...: # c.meth(1, 2, a=3)
    ...: # c._transaction = 1
    ...: # c.meth(1, 2, a=3)
    ...: # c._opened = False
    ...: # c.meth(1, 2, a=3)
    ...:
 
```


```
 In [3]: c.meth(1, 2, a=3)
 acquire
 checking if open
 checking if in a transaction
 meth (1, 2) {'a': 3}
 release
 

```
 In [4]: c._transaction = 1
 
 In [5]: c.meth(1, 2, a=3)
 acquire
 checking if open
 checking if in a transaction
 release
 ---------------------------------------------------------------------------
 AttributeError                            Traceback (most recent call last)
 <ipython-input-5-dbd9bc3f75ec> in <module>
 ----> 1 c.meth(1, 2, a=3)
 
 ~/anaconda3/envs/class_database/lib/python3.9/site-packages/ZODB/utils.py in __call__(self, *args, **kw)
     284                     raise AssertionError(
     285                         "Failed precondition: ",
 --> 286                         precondition.__doc__.strip())
     287
     288             return func(*args, **kw)
 
 AttributeError: 'NoneType' object has no attribute 'strip'
 
```


```
 In [6]: c._opened = False
 
 In [7]: c.meth(1, 2, a=3)
 acquire
 checking if open
 release
 ---------------------------------------------------------------------------
 AttributeError                            Traceback (most recent call last)
 <ipython-input-7-dbd9bc3f75ec> in <module>
 ----> 1 c.meth(1, 2, a=3)
 
 ~/anaconda3/envs/class_database/lib/python3.9/site-packages/ZODB/utils.py in __call__(self, *args, **kw)
     284                     raise AssertionError(
     285                         "Failed precondition: ",
 --> 286                         precondition.__doc__.strip())
     287
     288             return func(*args, **kw)
 
 AttributeError: 'NoneType' object has no attribute 'strip'
 
```

## メモリ管理
ZODBはオブジェクトのメモリへの入出力を管理します。永続的なオブジェクトごとにメモリへ格納されます。永続化オブジェクトの属性にアクセスすると、必要に応じて自動的にデータベースから読み込まれます。メモリ内のオブジェクト数が多すぎる場合は、もっとも直近に退避されたオブジェクトが削除されます 。メモリ内の最大オブジェクト数と最大バイト数は設定することができます。

```
 from zodb_mydata import *
 
 root.users = BTree()
 root.users['devops'] = user_data
  transaction.commit()
 connection.close()
 
 user_data.append(adam)
 
```


```
 root.users['devops'] = user_data
 transaction.commit()
 
 user_data.append(adam)
 connection.close()
 
```

## ZODB設定ファイルの使用
ZODBは、ZConfig形式で書かれた設定ファイルもサポートしています。設定ファイルを使用することで、設定ロジックをアプリケーションロジックから分離することができます。storagesクラスとDBクラスは、さまざまなキーワード引数をサポートしており、これらのオプションはすべて設定ファイルで指定できます。

この設定ファイルはシンプルです。
 test.conf
```
 <zodb>
   <filestorage>
   path /tmp/test-filestorage.fs
   </filestorage>
 </zodb>
 
```

ZODB.configモジュールは、設定ファイルからデータベースやストレージを開くためのいくつかの機能を備えています。

```
 import ZODB.config
 
 db = ZODB.config.databaseFromURL('/tmp/test.conf')
 conn = db.open()
 
```

ZODB.config は内部で ZConfig を利用しています。


## ZConfig
ZConfigモジュールは、ZODBをインストールすると一緒にインストールされるパッケージのひとつです。
ZConfigは拡張可能な構成ファイルを作成するためのPythonライブラリです。構成ファイルは Apache HTTP Server で使われているような構文で書かれており、 設定メカニズムは XML で書かれたスキーマ仕様を使って設定されます。

ZConfigは、ZopeアプリケーションサーバーやZODBなどのプロジェクトで使用されており、他のプロジェクトでも簡単に使用することができます。ZConfigはPythonの標準ライブラリにのみ依存しています。
構成ファイルの構文について説明することにします。
- **コメント**
シャープ記号(#)で始めた単独の行です。
 config
```
 # This is comment
 
```

- **インクルード**
 `%include` に続けて指定したファイルを構成ファイルとして読み出します。
 config
```
 %include default.conf
 
```

インクルードするリソースは、相対的または絶対的なURLで指定することができます。 `%include` ディレクティブが記述されている構成ファイルに対しての相対的に指定することもできます。

- **値の定義**
値はキーとのペアは次のように表されます。
 config
```
 key value    # still part of the value
 
```

キーには、括弧を除き、非空白文字を含めることができます。値には、キーから行末までのすべての文字が含まれ、周囲の空白文字は取り除かれます。
コメントは単独の行でなければならないので、 `#` 文字は値の一部とすることができます。

セクションには、空のセクションと空でないセクションがあります。空のセクションは、他のセクションの別名として使用することができます。空ではないセクションは、ヘッダーで始まり、後続の行に設定データを含み、ターミネーターで終わります。

空ではないセクションのヘッダーは次のような形式になります（角括弧はオプション部分を示します）。

 config
```
 <section-type [name]>
 
```

section-typeとnameはすべて、キー名と同じ構文上の制約があります。
ターミネーターは次のようになります。
 config
```
 </section-type>
 
```

空ではないセクションの設定データは、1つ以上のキーバリューペアとセクションのシーケンスで構成されています。例えば、以下のようになります。

 config
```
 <my-section>
   key-1 value-1
   key-2 value-2
 
   <another-section>
       key-3 value-3
   </another-section>
 </my-section>
 
```

ここではわかりやすくするためにインデントを使用していますが、構文として必要なわけではありません。
空のセクションのヘッダーは、空でないセクションのヘッダーと似ていますが、ターミネーターはありません。

 config
```
 <section-type [name] />
 
```

- **値の文字列置換**
ZConfig は、単純な文字列置換を使用して値の一部を再利用する限定的な方法を提供します。この機能を使用するには、 `%define` を使用して置換テキストに値を与えて定義し、値からこれらのテキストを参照します。
 config
```
 %define name [value]
 
```

これらの名前のための名前空間は、ZConfig で使用される他の名前空間とは別であり、大文字と小文字は区別されません。これらの名前は、ZConfig で使用される他の名前空間とは異なり、大文字と小文字は区別されます。値を指定する場合は、name と value の間に空白を入れる必要があります。key-value ペアからの値と同様に、value にはどちらの側にも空白が含まれません。

名前は使用する前に定義しなければならず、異なる値で再定義することはできません。設定の一部として解析されるすべてのリソースは、定義された名前のための単一の名前空間を共有します。

構成値から定義された名前を参照するには、ZConfig.substitution モジュールで説明されている構文を使用します。
実際の値の中にドル記号( `$` ) を含む場合は、結果としてひとつのドル記号( `$` )を得るためには、２重に記述する( `$$` )必要があります。

定義済みの名前の値は、構成値と同じ方法で処理され、名前付きの定義への参照を含むことができます。
次の例では、keyの値はvalueと評価されます。
 config
```
 %define name value
 key $name
 
```

- **環境変数からの値の代入**
ZConfig の値は、環境変数から代入することができます。Python の  `os.getenv()` を利用して値を取得します。構文は、ドル記号( `$` )の後にカッコ（ `(...)` を付けたものです。この例では、変数  `key` に  `ENVKEY` という環境変数から割り当てられた値を取得しています。
 config
```
 key $(ENVKEY)
 
```

### コンフィグレーション・スキーマの拡張
コンフィグレーション・スキーマの記述で説明しますが、コンフィグレーションに記述できる内容は、コンポーネントから構築されるスキーマによって制御されます。これらのコンポーネントは、アプリケーションが扱えるオブジェクトの実装セットを拡張するためにも使用できます。構成を記述する際に意味するのは、アプリケーション・オブジェクト・タイプのサードパーティの実装は、その実装に利用可能なZConfigコンポーネントがあれば、構成で使用されているアプリケーション・タイプはどこでも使用できるということです。

構成ファイルでは、 `%import` を使用して、名前付きのコンポーネントを読み込むことができます。
 config
```
 %import Products.Ape
 
```

そのパッケージが提供する ZConfig コンポーネントがロードされ、構成ファイルのロードに使用されるスキーマに組み込まれます。そのパッケージによって提供される ZConfig コンポーネントが読み込まれ、構成ファイルの読み込みに使用されるスキーマに組み込まれます。

スキーマでは、抽象的なセクション・タイプを定義することができます。これらはコンフィギュレーションで直接使用することはできませんが、抽象的なタイプを実装する複数の具体的なセクション・タイプを定義することができます。アプリケーションが抽象型の使用を許可している場合はどこでも、その抽象型を実装した具象型を実際の構成で使用することができます。

 `%import` では、アプリケーションで定義された抽象型を実装する代替の具象セクション・タイプを提供するスキーマ・コンポーネントを読み込むことができます。これにより、アプリケーションで提供されている実装の代わりに、またはそれに加えて、サードパーティによる抽象型の実装を使用することができます。

## ロギング設定の構成ファイル
ロギングをサポートするアプリケーションの例を考えてみましょう。ロギング機構の一般的な動作を設定するためのいくつかのパラメータがあり、 任意の数のログハンドラを指定してログメッセージの処理方法を制御することができます。いくつかのログハンドラーはアプリケーションによって提供されます。以下にロギング設定の例を示します。

 config
```
 <eventlog>
   level verbose
 
   <logfile>
     path /var/log/myapp/events.log
   </logfile>
 </eventlog>
 
```


サードパーティのコンポーネントは、システム管理者のテキストポケットベルやSMS対応の電話に優先度の高いアラートを送信するログハンドラを提供することができます。必要なのは、Pythonでインポートできるように実装をインストールして、設定を変更することだけです。
 config
```
 %import my.pager.loghandler
 
 <eventlog>
   level verbose
 
   <logfile>
     path /var/log/myapp/events.log
   </logfile>
 
   <pager>
     number   1-800-555-1234
     message  Something broke!
   </pager>
 </eventlog>
 
```

## その他のコンポーネント
これまで見てきてわかるように、ZODBはさまざまな機能を単独のモジュールで実装することはしていません。
ZODBをサポートする便利なモジュールや、拡張機能を提供するモジュールがリリースされています。これらのモジュールと連携・協調して開発することができます。

## ZEO
ZEOサーバーを導入するすると、FileStorageへのアクセスを複数のプロセスまたは複数のマシンに拡張することができます。ZEOは、クライアント／サーバー・アーキテクチャを採用していて、サーバープロセスは、1つまたは複数のストレージ（実際には常にFileStorage）を開き、このストレージへのアクセスを提供するネットワークAPIを公開します。クライアントプロセスは、このサーバに接続し、読み書きのリクエストを送信します。サーバーは、クライアントのためにベースとなるストレージへのアクセスを仲介します。

ZEOは、自身の長所と短所に加えて、ベースなるストレージの長所と短所の多くを継承しています。例えば、クライアントに永続的なローカルキャッシュを設定することで、一般的なオブジェクトへのアクセスや、サーバーが利用できない場合には読み取り専用のアクセスも可能にすることができます。しかし、ZEOプロセスはPythonのGILに拘束されているため、スケーラビリティが制限される可能性があります。また、デフォルトではアプリケーションコードをサーバープロセスにロードすることでコンフリクトを解決しますが、クライアントとサーバーのプロセスがすべて互換性のあるコードを実行する必要があるため、デプロイが複雑になる可能性があります。

## NEO
NEOは、複数のコンピュータにデータを分散させ、負荷分散やマルチマスターレプリケーションを行うことができます。また、オフサイトのNEOデータベースへの非同期レプリケーションにも対応しており、ローカルの運用レイテンシーに影響を与えることなく、さらなる災害対策(disaster resistance)が可能になります。

## ZRS
#### ZRS(ZODB replicated storage)
もともとZRSは、Zope社が開発した商用ソフトウェアでしたが、2013年5月よりオープンソースとして公開されました。

### ZRSの特徴
ZRSは次のような特徴を持っています。

- プライマリ→セカンダリのレプリケーションを行う。
- プライマリストレージサーバは読み書き可能なストレージ。
- セカンダリーストレージサーバは読み取り専用のストレージ。
  - ZRSはセカンダリーストレージを読み取り専用のアプリケーションクライアントが使用することでサーバーの負荷を軽減し、スケーラビリティを向上させます。
- 管理者は、プライマリおよびセカンダリのスタンバイサーバを管理・監視し、ミッションクリティカルなデータを2つ以上のデータベースサーバにレプリケーションすることができます。

### ZRSはメンテナンスを簡素化
一度に使用できるプライマリストレージは1台のみです。プライマリストレージが故障あるいは、アップグレード、メンテナンスなどの問題が発生した場合には、セカンダリストレージをプライマリストレージとして設定することができます。アプリケーションはすぐに新しいZRSサーバーに再接続できます。セカンダリストレージはオフラインにすることができ、修理、バックアップ、システムアップグレードすることができます。再度オンラインにした後、セカンダリ・ストレージはプライマリ・ストレージから再びデータ更新がされます。セカンダリーストレージは、定期的なメンテナンスの際にプライマリーストレージに移動させることができるので、より管理しやすくなります。セカンダリーサーバーはいつでもシステムに追加することができます。


## RelStorage
RelStorageはZODBのストレージエンジンで、ZEOやZRSと同じような問題を解決することを目的としているが、トレードオフの異なるアプローチをとっている。RelStorageは、MySQL、PostgreSQL、Oracle、SQLiteなどのリレーショナルデータベースを使用して、オブジェクトの状態データを最終的に保存します。OIDの割り当て、ロック、トランザクション管理、スナップショットの隔離、レプリケーションなどは、外部のデータベースシステムによって実現されます。

### 特徴
- FileStorageおよびZEOのドロップインリプレースメントであり、いくつかの機能が強化されています。
- FileStorageと同様に、Undo、Packing、およびオブジェクト履歴の保存をサポートしています。
- RelStorageは、オブジェクト履歴を保存しないように設定することで、ディスクスペースの使用量を減らし、パフォーマンスを向上させることができます。
- 1台のマシン上の複数のプロセスが、SQLiteを使ってローカルのZODBデータベースを読み書きできるようになりました。
- Blobは、共有ファイルシステム、またはリレーショナル・データベースに保存し、ローカルでのみキャッシュすることができます。
- 同一プロセス内の複数のスレッドは、高性能なメモリ内Pickleキャッシュを共有し、RDBMSへのクエリ数を削減します。これは ZEO に類似しており、ZEO のキャッシュトレースツールがサポートされています。
- インメモリーPickleキャッシュはディスクに保存され、プロセスの起動時に読み込まれます。これにより、RDBMSへの問い合わせが殺到することがなくなり、サイトのウォームアップ時間を劇的に短縮することができます。ZEOとは異なり、このキャッシュはマシン上のすべてのプロセスで自動的に共有されます（個別にクライアント識別子を設定する必要はありません）。
- 大規模なボリュームのあるサイトに最適です。
- 複数のマシン上の複数のPythonプロセスが、同じZODBデータベースを同時に読み書きすることができます。これはZEOに似ていますが、RelStorageはZEOを必要としません。
- ZODB 5のパラレルコミット機能をサポート。データベースライターは、競合する場合にのみお互いをブロックします（ただし、トランザクションIDが割り当てられる2段階のコミットプロトコルの最後にある小さなウィンドウは除きます。
いくつかのテストによると、RelStorageはZEOとFileStorageの標準的な組み合わせよりも並行処理が優れているという。
- FileStorageは、すべてのオブジェクトのインメモリーインデックスのため、データベースが大きくなると起動に時間がかかりますが、RelStorageはデータベースのサイズに関わらず、素早く起動します。
- 複製されたSQLデータベースへのフェイルオーバーが可能。
- PostgreSQLおよびMySQLのgeventとの統合をテスト済み。
- FileStorageをRelStorageに(インクリメンタルに)変換する簡単な方法(zodbconvert)があります。また、RelStorageのインスタンスを別のリレーショナルデータベースに変換することもできます。これは、任意の2つのZODBストレージ実装の間で変換するために使用できる一般的なツールです。
- データベースをパックする簡単な方法(zodbpack)があります。
- zodburi をサポートしています。
- オープンソース(ライセンス：ZPL 2.1)、無料で利用可能.

## zlibstorage
zlibstorageによるデータベースの圧縮

## beforestorage
beforestorageは、変更されている可能性のあるデータベースのポイントインタイムビューを提供します。これは、DemoStorageで使用する本番データベースの変化しないビューを提供するのに役立ちます。


## まとめ
ZODBは非常にシンプルで透過的なPythonのオブジェクトデータベースです。わずか数行のコードでPythonオブジェクトをZODBに格納しすることができ、SQL文でクエリを書く必要もありません。
また、協調して動作する便利なパッケージも多くあるため目的を実現するための開発工数がすくなくなることが見込めます。


## 参考資料
- [ZODB公式ドキュメント ](https://zodb.org/en/latest/)
- [ZEO ソースコード ](https://github.com/zopefoundation/ZEO)
- [ZRS ソースコード ](https://github.com/zopefoundation/zc.zrs)
- [NEO オフィシャルサイト ](https://neo.nexedi.com/)
- [RelStorage 公式ドキュメント ](https://relstorage.readthedocs.io/en/latest/index.html)


previous: [TinyDBを使ってみよう]
next: [SQLite3を使ってみよう]
#Pythonセミナーデータベース編


