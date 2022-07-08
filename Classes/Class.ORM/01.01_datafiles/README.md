datafilesを使ってみよう
=================
## datafiles について

Datafiles ファイルベースのORMで、Pythonデータクラスを双方向のシリアル化ライブラリで、[タイプアノテーション ](https://docs.python.org/ja/3/library/typing.html) を使ってオブジェクトをファイルシステムに同期させます。様々なファイルフォーマットをサポートしており、フォーマットやコメントを可能な限りそのまま保存することができます。オブジェクトの変更は自動的にディスクに保存され、各オブジェクトの復元に必要な最小限のデータのみが含まれます。

次のような適用例が’考えられます。

- ユーザーが編集可能なファイルを適切なPythonタイプに変換する
- プログラムの構成やデータをバージョン管理で保存
- デモやテストのためのデータをロード
- ファイル共有サービスを使ったアプリケーションの状態の同期
- 永続化バックエンドに依存しないデータモデルのプロトタイピング


## インストール
datafiles は拡張モジュールなので次のようにインストールします。

 bash
```
 $ pip install datafiles

```

## datafiles の使い方

### サンプル
datafilesでは次のようなモデルクラスを作ることができます。
このモデルはファイル  `sampledb/KEYの値.yml` に書き出されます。

 sampledb.py
```
 from datafiles import *

 @datafile("sampledb/{self.key}.yml")
 class Sample:
     key: int
     name: str
     value: float = 0.0


 def populate_database():
     d = Sample(1, "Beer")
     d = Sample(2, "Sake")
     d = Sample(3, "Wine")

 if __name__ == '__main__':
     populate_database()

```

モデルクラス Sample は３つのフィールドをもっています。

- key：データを整数で必須
- name: データは文字列で必須
- value：データは浮動小数点で省略可能。デフォルトは 0.0

データベース sampledb を初期化しておきます。

```
 In [1]: !mkdir -p sampledb

 In [2]: %run sampledb.py

 In [3]: !ls sampledb
 1.yml	2.yml	3.yml

 In [4]: !cat sampledb/1.yml
 name: Beer

```

### データの読み出し
データベースから key ファイールドの値を与えて読み出すことができます。


```
 In [2]: # %load 01_retreive.py
    ...: from sampledb import *
    ...:
    ...: sample = Sample(1, Missing)
    ...: v1 = sample.name
    ...: v2 = Sample(10, Missing).name
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(sample)
    ...:

 In [3]: print(v1)
 Beer

 In [4]: print(v2)


 In [5]: print(sample)
 Sample(key=1, name='Beer', value=0.0)

 In [6]: Sample(1)
 ---------------------------------------------------------------------------
 TypeError                                 Traceback (most recent call last)
 <ipython-input-6-f7fc3f19a34f> in <module>
 ----> 1 Sample(1)

 ~/anaconda3/envs/class_database/lib/python3.9/site-packages/datafiles/model.py in modified_init(self, *args, **kwargs)
      80     def modified_init(self, *args, **kwargs):
      81         with hooks.disabled():
 ---> 82             init(self, *args, **kwargs)
      83         Model.__post_init__(self)
      84

 TypeError: __init__() missing 1 required positional argument: 'name'

```

モデルクラスのコンストラクタに与える引数は、位置引数がモデルクラスでのフィールドの定義順に割り当てられます。
ここで、 `Missing` は datafiles で定義されているもので、モデルクラスのフィールドを全て記述することを省略できるようにします。

### タイプチェック
タイプチェックを行うツール mypy を使用している場合は、 `mypy.ini` 設定ファイルでプラグインを有効にしてください。

 mypy.ini
```
 [mypy]
 plugins = datafiles.plugins:mypy

```


## Model API
モデルを作成するには、 `@dataclass` でデコレートしてModelクラスを拡張するか、 `datafile()` デコレーターを使用します。


```
 from dataclasses import dataclass

 @dataclass
 class Item:
     name: str
     count: int
     available: bool

```

ファイルとの同期は、 `@datafile(<pattern>)` デコレーターを追加することで有効になります。


```
 from dataclasses import dataclass
 from datafiles import datafile

 @datafile("items/{self.name}.yml")
 @dataclass
 class Item:
     name: str
     count: int
     available: bool
```

あるいは、 `@dataclass` デコレータを完全に置き換えることもできます。
実際のところ、この方法がもっとも多く使用されます。


```
 from datafiles import datafile

 @datafile("items/{self.name}.yml")
 class Item:
     name: str
     count: int
     available: bool

```

### ファイル名
モデルクラスのインスタンスオブジェクトは、 `@datafile()` に与える引数の文字列 `<pattern>` に従ってディスクに同期されます。


```
 Item("abc")  # <=> items/abc.yml
 Item("def")  # <=> items/def.yml
```

ファイル名は、 `<pattern>` が絶対パスであったり、明示的にカレントディレクトリからの相対パスであったりしない限り、モデルが定義されているファイルへの相対パスとなります。

- 絶対パス:  `/tmp/items/{self.name}.yml`
- モデルファイルからの相対パス:  `items/{self.name}.yml`
- カレントディレクトリからの相対パス:  `./items/{self.name}.yml`

ファイル名のパターンに含まれる属性やデフォルト値を持つ属性は、ディスクからオブジェクトを復元する際にこれらの冗長な値を必要としないため、自動的にシリアライズから除外されます。

## datafile() の引数
 `@datafile()` デコレーターには、次のようなキーワード引数を渡すことができます。

 オプション

| 引数 | タイプ | デフォルト値 | 説明 |
|:--|:--|:--|:--|
| attrs | dict | {}   (注1) | datafile.convertersクラスのシリアル化のための属性のマップ |
| manual | bool | False | オブジェクトやファイルの変更を手動で同期させることができる |
| defaults | bool | False | シリアライズ時にデフォルト値を持つ属性を含める. |
| infer | bool | False | ファイルから新しい属性を自動的に推察する |

注1) デフォルトでは、同期する属性はタイプアノテーションから推測されます。

引数の使用例

```
 from datafiles import datafile

 @datafile("items/{self.name}.yml", manual=True, defaults=True)
 class Item:
     name: str
     count: int
     available: bool

 @datafile("config.yml", infer=True)
 class Config:
     default_count: int = 42

```

### メタクラス
また、Metaクラスで  `datafile_<option>` を設定することで、上記の引数をコードで設定することもできます。


```
 from datafiles import datafile, converters

 @datafile("items/{self.name}.yml")
 class Item:
     name: str
     count: int
     available: bool

     class Meta:
         datafile_attrs = {'count': converters.Integer}
         datafile_manual = True
         datafile_defaults = True

```

ここで、 `converters.Integer` はシリアル化されているデータを数値に変換するためのものです。詳しくは後述しています。


### ベースクラス
最後に、データファイルはdatafiles.Modelを明示的に拡張し、Metaクラスにパターンを設定することができます。


```
 from dataclasses import dataclass

 from datafiles import Model, converters

 @dataclass
 class Item(Model):
     name: str
     count: int
     available: bool

     class Meta:
         datafile_pattern = "items/{self.name}.yml"
         datafile_attrs = {'count': converters.Integer}
         datafile_manual = True
         datafile_defaults = True

```

## Manager API
オブジェクト・リレーショナル・マッピング（ORM）のメソッドは、オブジェクト・プロキシを介してすべてのモデル・クラスで利用できます。以下のセクションでは、空のファイルシステムと以下のデータファイル定義のサンプルを想定しています。

 mymodeldb.py
```
 from datafiles import *

 data_dir = './mymodels'
 data_pattern = data_dir + '/{self.my_key}.yml'

 @datafile(data_pattern)
 class MyModel:
      my_key: str
      my_value: int = 0

 if __name__ == '__main__':
     from pathlib import Path

     dir = Path(datadir)
     dir.mkdir(exist_ok=True)

```


### get()
既存のファイルからオブジェクトをインスタンス化します。一致するファイルが存在しない場合や、その他の問題が発生した場合は、適切な例外が発生します。

 pytohn
```
 In [1]: %run mymodeldb.py

 In [2]: %load 10_get.py

 In [3]: # %load 10_get.py
    ...: from mymodeldb import *
    ...:
    ...: v1 = MyModel.objects.get('Beer')
    ...:
 ---------------------------------------------------------------------------
 FileNotFoundError                         Traceback (most recent call last)
 (中略)
 FileNotFoundError: [Errno 2] No such file or directory: '/Users/goichiiisaka/Projects/Python.Osaka/Class.ORM/01.01_datafiles/mymodels/Beer.yml'
```

モデルクラスのインスタンスオブジェクトを作成すると、ファイルに同期されるため `mymodels/Beer.yml' が作成されます。
この後、再度データを `get()` メソッドを呼び出すと、問題なくデータを取得できます。


```
 In [2]: # %load 11_set_and_get.py
    ...: from mymodeldb import *
    ...:
    ...: v1 = MyModel('Beer', 2)
    ...: v2 = MyModel.objects.get('Beer')
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # !cat mymodels/Beer.yml
    ...:

 In [3]: print(v1)
 MyModel(my_key='Beer', my_value=2)

 In [4]: print(v2)
 MyModel(my_key='Beer', my_value=2)

 In [5]: !cat mymodels/Beer.yml
 my_value: 2

```

### get_or_none()
データを格納しているファイルが存在していないとき発生する例外を都度処理するのは面倒なので、 `get_or_none()` を使います。このメソッドは、既存のファイルからオブジェクトをインスタンス化するか、マッチするファイルが存在しない場合は  `None` を返します。


```
 In [2]: # %load 12_get_or_none.py
    ...: from mymodeldb import *
    ...:
    ...: v1 = MyModel.objects.get_or_none('Wine')
    ...: v2 = MyModel('Wine', 3)
    ...: v3 = MyModel.objects.get_or_none('Wine')
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v3)
    ...:

 In [3]: print(v1)
 None

 In [4]: print(v2)
 MyModel(my_key='Wine', my_value=3)

 In [5]: print(v3)
 MyModel(my_key='Wine', my_value=3)

```

### get_or_create()
既存のファイルからオブジェクトをインスタンス化するか、マッチするファイルが存在しない場合はオブジェクトを作成します。


```
 In [2]: # %load 13_get_or_create.py
    ...: from mymodeldb import *
    ...:
    ...: v1 = MyModel.objects.get_or_none('Sake')
    ...: v2 = MyModel.objects.get_or_create('Sake', 3)
    ...: v3 = MyModel.objects.get_or_create('Sake')
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v3)
    ...: # !ls mymodels
    ...: # !cat mymodels/Sake.yml
    ...:

 In [3]: print(v1)
 None

 In [4]: print(v2)
 MyModel(my_key='Sake', my_value=3)

 In [5]: print(v3)
 MyModel(my_key='Sake', my_value=3)

 In [6]: !ls mymodels
 Beer.yml	Sake.yml	Wine.yml

 In [7]: !cat mymodels/Sake.yml
 my_value: 3

```


### all()
 `all()` メソッドは、引数に与えたパターンにマッチするすべてのオブジェクトをイテレートします。引数を省略するとすべてのオブジェクトを返します。また、このとき、キーワード引数　 `_exclude` で除外オブジェクトが￥指定することができます。


```
 In [2]: # %load 14_all.py
    ...: from mymodeldb import *
    ...: from pprint import pprint
    ...:
    ...: v1 = MyModel.objects.all()
    ...: v2 = list(v1)
    ...:
    ...: v3 = MyModel.objects.all(_exclude='Sake')
    ...: v4 = list(v3)
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...: # pprint(v3)
    ...: # pprint(v4)
    ...:

 In [3]: pprint(v1)
 <generator object Manager.all at 0x10ea56c10>

 In [4]: pprint(v2)
 [MyModel(my_key='Beer', my_value=2),
  MyModel(my_key='Sake', my_value=3),
  MyModel(my_key='Wine', my_value=3)]

 In [5]: pprint(v3)
 <generator object Manager.all at 0x10ea56d60>

 In [6]: pprint(v4)
 [MyModel(my_key='Beer', my_value=2), MyModel(my_key='Wine', my_value=3)]

```


### filter()
 `filter()` メソッドは、パターンにマッチするすべてのオブジェクトに、必要な属性値を追加してイテレートします。
また、このとき、キーワード引数　 `_exclude` で除外オブジェクトが￥指定することができます。

```
 In [2]: # %load 16_filter.py
    ...: from mymodeldb import *
    ...: from pprint import pprint
    ...:
    ...: v1 = MyModel.objects.filter(my_value=3)
    ...: v2 = list(v1)
    ...:
    ...: v3 = MyModel.objects.filter(my_value=3, _exclude='Sake')
    ...: v4 = list(v3)
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...: # pprint(v3)
    ...: # pprint(v4)
    ...:

 In [3]: pprint(v1)
 <generator object Manager.filter at 0x10a6b0dd0>

 In [4]: pprint(v2)
 [MyModel(my_key='Sake', my_value=3), MyModel(my_key='Wine', my_value=3)]

 In [5]: pprint(v3)
 <generator object Manager.filter at 0x10a6b0f20>

 In [6]: pprint(v4)
 [MyModel(my_key='Wine', my_value=3)]

```


## Mapper API
データファイル・モデルのインスタンスには、ファイルシステムを手動で操作するためのデータファイル・プロキシが追加されています。


```
 In [2]: # %load 20_path.py
    ...: from mymodeldb import *
    ...:
    ...: v1 = MyModel.objects.get('Beer')
    ...: v2 = v1.datafile.path
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v2.parts[-1])
    ...: # print(v2.parent)
    ...:

 In [3]: print(v1)
 MyModel(my_key='Beer', my_value=2)

 In [4]: print(v2)
 /Users/goichiiisaka/Projects/Python.Osaka/Class.ORM/01.01_datafiles/mymodels/Beer.yml

 In [5]: print(type(v2))
 <class 'pathlib.PosixPath'>

 In [6]: print(v2.parts[-1])
 Beer.yml

 In [7]: print(v2.parent)
 /Users/goichiiisaka/Projects/Python.Osaka/Class.ORM/01.01_datafiles/mymodels


```

モデルクラスのインスタンスオブジェクトには 、 `path` 属性がありデータが書き込まれているファイルを保持しています。
これは、Pathlib モジュールの PostixPath クラスのオブジェクトで返されます。

### exists
マップされたファイルが存在するかどうかを判断します。


```
 In [2]: # %load 21_exists.py
    ...: from mymodeldb import *
    ...:
    ...: v1 = MyModel.objects.get('Beer')
    ...: v2 = v1.datafile.exists
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:

 In [3]: print(v1)
 MyModel(my_key='Beer', my_value=2)

 In [4]: print(v2)
 True

```

### save()
オブジェクトをファイルシステムに手動で保存します。


```
 In [2]: # %load 22_save.py
    ...: from mymodeldb import *
    ...:
    ...: v1 = MyModel.objects.get('Beer')
    ...: before_dir = !ls mymodels
    ...: v2 = v1.datafile.path.unlink()
    ...: after_unlink = !ls mymodels
    ...: v3 = v1.datafile.save()
    ...: after_save = !ls mymodels
    ...:
    ...: # print(before_dir)
    ...: # print(after_unlink)
    ...: # print(after_save)
    ...:

 In [3]: print(before_dir)
 ['Beer.yml', 'Sake.yml', 'Wine.yml']

 In [4]: print(after_unlink)
 ['Sake.yml', 'Wine.yml']

 In [5]: print(after_save)
 ['Beer.yml', 'Sake.yml', 'Wine.yml']

```

デフォルトでは、このメソッドは自動的に呼び出されます。この動作を無効にするには、 `datafile()` に `manual=True` を設定してください。

### load()
ファイルシステムからオブジェクトを手動で読み込みます。


```
 In [1]: %load 23_load.py

    ...:
    ...: !mv mymodels/Beer.yml .
    ...: before_load = !ls mymodels
    ...:
    ...: from mymodeldb import *
    ...:
    ...: v1 = MyModel('Beer', 20)
    ...: s1  = f'{v1}'
    ...:
    ...: v2 = MyModel.objects.get('Beer')
    ...: s2  = f'{v2}'
    ...:
    ...: !mv Beer.yml mymodels/Beer.yml
    ...: v3 = v2.datafile.load()
    ...:
    ...: after_load = !ls mymodels
    ...: v4 = MyModel.objects.get('Beer')
    ...:
    ...: # print(v1)
    ...: # print(s1)
    ...: # print(v2)
    ...: # print(s2)
    ...: # print(v3)
    ...: # print(v4)
    ...:

 In [3]: print(v1)
 MyModel(my_key='Beer', my_value=2)

 In [4]: print(s1)
 MyModel(my_key='Beer', my_value=20)

 In [5]: print(v2)
 MyModel(my_key='Beer', my_value=2)

 In [6]: print(s2)
 MyModel(my_key='Beer', my_value=20)

 In [7]: print(v3)
 None

 In [8]: print(v4)
 MyModel(my_key='Beer', my_value=2)

```

ここで、 `load()` を呼び出す前に取得した  `v1` と `v2` が、 `load()` 後のデータに置き換わっていることに注目してください。
デフォルトでは、このメソッドは自動的に呼び出されます。この動作を無効にするには、 `manual=True` を設定してください。

### modified
ファイルシステムに同期していない変更があるかどうかを判断します。


```
 In [2]: # %load 24_modified.py
    ...: from mymodeldb import *
    ...:
    ...: v1 = MyModel.objects.get('Beer')
    ...: s1 = f'{v1}'
    ...: !echo 'my_value: 6' > mymodels/Beer.yml
    ...:
    ...: v2 = v1.datafile.modified
    ...: v3 = MyModel.objects.get('Beer')
    ...:
    ...: v4 = v3.datafile.modified
    ...:
    ...: # print(v1)
    ...: # print(s1)
    ...: # print(v2)
    ...: # print(v3)
    ...: # print(v4)
    ...:

 In [3]: print(v1)
 MyModel(my_key='Beer', my_value=6)

 In [4]: print(s1)
 MyModel(my_key='Beer', my_value=2)

 In [5]: print(v2)
 True

 In [6]: print(v3)
 MyModel(my_key='Beer', my_value=6)

 In [7]: print(v4)
 False

```

### データを参照する
解析されたモデルの属性に直接アクセスします。


```
 In [2]: # %load 25_data.py
    ...: from mymodeldb import *
    ...:
    ...: v1 = MyModel.objects.get('Beer')
    ...: s1 = f'{v1}'
    ...: v2 = v1.datafile.data
    ...:
    ...: # print(v1)
    ...: # print(s1)
    ...: # print(v2)
    ...:

 In [3]: print(v1)
 MyModel(my_key='Beer', my_value=6)

 In [4]: print(s1)
 MyModel(my_key='Beer', my_value=6)

 In [5]: print(v2)
 ordereddict([('my_value', 6)])

```

## 組み込み型
Python の組み込み型がタイプアノテーションとして使用されると、選択されたファイルフォーマットの対応する型に自動的にマッピングされます。これらの型は、 `Optional` にすると  `None` を値として受け入れます。


```
 from typing import Optional

```

### ブール値(Boolean)

 組み込み型 Boolean

| タイプアノテーション | Python | YAML |
|:--|:--|:--|
| foobar: bool | foobar = True | foobar: true |
| foobar: bool | foobar = False | foobar: false |
| foobar: bool | foobar = None | foobar: false |
| foobar: Optional[bool] | foobar = False | foobar: |

### 整数(Integer)
 組み込み型整数

| タイプアノテーション | Python | YAML |
|:--|:--|:--|
| foobar: int | foobar = 42 | foobar: 42 |
| foobar: int | foobar = 1 | foobar: 1 |
| foobar: int | foobar = None | foobar: 0 |
| foobar: Optional[int] | foobar = None | foobar: |

### 浮動小数点(float)
 組み込み型  浮動小数点

| タイプアノテーション | Python  | YAML |
|:--|:--|:--|
| foobar: float | foobar = 1.23 | foobar: 1.23 |
| foobar: float | foobar = 42 | foobar: 42.0 |
| foobar: float | foobar = None | foobar: 0.0 |
| foobar: Optional[float] | foobar = None | foobar: |

### 文字列(String)
 組み込み型 文字列

| タイプアノテーション | Python  | YAML |
|:--|:--|:--|
| foobar: str | foobar = "Hello, world!" | foobar: Hello, world! |
| foobar: str | foobar = 42 | foobar: '42' |
| foobar: str | foobar = None | foobar: '' |
| foobar: Optional[str] | foobar = None | foobar: |

## コンテナタイプ
オブジェクトのコレクションを定義するために、さまざまなコンテナタイプがサポートされています。

### リスト(list)
Listアノテーションを使用して、他のタイプと同質のコレクションを定義できます。


```
 from typing import List, Optional

```

Python 3.9 から組み込みの `list` がリスト表記( `[...]` )をサポートするようになったため、 `typing.List` は非推奨になりました。


 コンテナタイプ　リスト

| タイプアノテーション | Python | YAML |
|:--|:--|:--|
| foobar: List[int] | foobar = [] | foobar: |
|  |  |   - |
| foobar: List[int] | foobar = [1.23] | foobar: |
|  |  |     - 1.23 |
| foobar: List[int] | foobar = None | foobar: |
|  |  |    - |
| foobar: Optional[List[int]] | foobar = None | foobar: |

### セット(set)
Setアノテーションは、他のタイプのユニークな要素の同種のコレクションを定義するために使用できます。


```
 from typing import Set, Optional

```

 コンテナタイプ 　セット

| タイプアノテーション | Python  | YAML |
|:--|:--|:--|
| foobar: Set[int] | foobar = [] | foobar: |
|  |  |     - |
| foobar: Set[int] | foobar = [1.23] | foobar: |
|  |  |     - 1.23 |
| foobar: Set[int] | foobar = None | foobar: |
|  |  |     - |
| foobar: Optional[Set[int]] | foobar = None | foobar: |

### 辞書(Dictionary)
Dictアノテーションは、複数のタイプの緩やかなマッピングを定義するために使用できます。


```
 from typing import Dict, Optional

```

Python 3.9 から組み込みの `dict` がリスト表記( `[...]` )をサポートするようになったため、 `typing.Dict` は非推奨になりました。

 コンテナタイプ　辞書

| タイプアノテーション | Python  | YAML |
|:--|:--|:--|
| foobar: Dict[str, int] | foobar = {} | foobar: {} |
| foobar: Dict[str, int] | foobar = {'a': 42} | foobar: |
|  |  |     a: 42 |
| foobar: Dict[str, int] | foobar = None | foobar: {} |
| foobar: Optional[Dict[str, int]] | foobar = None | foobar: |

Dictアノテーションでは、スキーマの強制はできません。
これは意外に重要なことで、うまく使えば便利な小技にもなります。

### データクラス(Dataclass)

Python では dataclass はネストさせることができます。

```
 In [2]: # %load 30_nest_dataclass.py
    ...: from dataclasses import dataclass
    ...:
    ...: @dataclass
    ...: class A:
    ...:     a: int
    ...:     b: str
    ...:
    ...: @dataclass
    ...: class B:
    ...:     c: str
    ...:     d: A
    ...:
    ...: data ={'c':'hello', 'd':{'a':4, 'b':'bye'}}
    ...: v1 = B(**data)
    ...:
    ...: data ={'c':'hello', 'd': A(**{'a':4, 'b':'bye'})}
    ...: v2 = B(**data)
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:

 In [3]: print(v1)
 B(c='hello', d={'a': 4, 'b': 'bye'})

 In [4]: print(v2)
 B(c='hello', d=A(a=4, b='bye'))

```

便宜上、 `@datafile` を  `@dataclass` の代わりに使用して、インポート数を少なくすることができます。
datafiles でネストしたクラスを扱うために、次のモジュールを用意しました。

 beerdb.py
```
 from dataclasses import dataclass
 from datafiles import *

 data_dir = './beerdb'
 data_pattern = data_dir + '/{self.brewery}.yml'

 @dataclass
 class Beer:
     name: str
     abv: float   # Alcohol by Volume (アルコール度数)

 @datafile(data_pattern)
 class Drink:
     brewery: str
     data: Beer

 if __name__ == '__main__':
     from pathlib import Path
     from pprint import pprint

     dir = Path(data_dir)
     dir.mkdir(exist_ok=True)

     beers =[
         {'brewery': 'Minoh', 'data': {'name': 'Pale_Ale', 'abv': 5.5} },
         {'brewery': 'Kyoto', 'data': {'name': 'ICHII_SENSHI', 'abv': 6.5} },
         {'brewery': 'Plank', 'data': {'name': 'Pilserl', 'abv': 4.9} },
     ]

     for beer in beers:
         v1 = Drink(**beer)

```


こうしたネストしたデータクラスの値は、デリミタとしてアンダースコア２つ( `__` )を使用してクエリを実行できます。
ビールのデータからアルコール度数が5%以下ののものを取得してみましょう。


```
 In [2]: # %load 31_beers.py
    ...: from beerdb import *
    ...:
    ...: v1 = Drink.objects.filter(data__abv=4.9)
    ...: v2 = list(v1)
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...:

 In [3]: print(v1)
 <generator object Manager.filter at 0x103f8ad60>

 In [4]: print(v2)
 [Drink(brewery='Plank', data=Beer(name='Pilserl', abv=4.9))]

```

ただし、 `filter()` メソッドに指示できるクエリでは、一般的なクエリ演算子ではないことに注意してください。
実際、 `data__abv==4.9` のように条件式として記述するとエラーになります。


```
 In [5]: Drink.objects.filter(data__abv==4.9)
 ---------------------------------------------------------------------------
 NameError                                 Traceback (most recent call last)
 <ipython-input-5-9006ec60babd> in <module>
 ----> 1 Drink.objects.filter(data__abv==4.9)

 NameError: name 'data__abv' is not defined

```



## 拡張型(Extend type)
便利なように、一般的なシナリオを処理するための追加の型が定義されています。

### 数値(Number)
Numberコンバータは、整数または浮動小数点数の値に使用されますが、シリアル化の際にどちらの型にも強制されません。


```
 from typing import Optional
 from datafiles.converters import Number

```

 拡張型　数値

| タイプアノテーション | Python  | YAML |
|:--|:--|:--|
| foobar: Number | foobar = 42 | foobar: 42 |
| foobar: Number | foobar = 1.23 | foobar: 1.23 |
| foobar: Number | foobar = None | foobar: 0.0 |
| foobar: Optional[Number] | foobar = None | foobar: |

### テキスト(Text)
Textコンバータは、テキストの行を含む文字列に使用され、ファイルの複数行に渡って最適な形でシリアル化されます。


```
 from typing import Optional
 from datafiles.converters import Text

```

 拡張型　テキスト

| タイプアノテーション | Python  | YAML |
|:--|:--|:--|
| foobar: Text | foobar = "Hello, world!" | foobar: Hello, world! |
| foobar: Text | foobar = "First\nSecond\n" | foobar: | |
|  |  |     First |
|  |  |     Second |
| foobar: Text | foobar = None | foobar: '' |
| foobar: Optional[Text] | foobar = None | foobar: |

### 列挙型(Enum)
enum.Enumのサブクラスは、タイプアノテーションとしても使用できます。


```
 from enum import Enum

 class Color:
     RED = 1
     GREEN = 2
     BLUE = 3

```

 拡張型　列挙型

| タイプアノテーション | Python  | YAML |
|:--|:--|:--|
| color: Color | color = Color.BLUE | color: 3 |


## カスタムタイプ
カスタムタイプは、アノテーションとして追加のタイプをサポートします。

### 単一継承
カスタムタイプの保存と読み込みは、同梱されているコンバータクラスのいずれかを継承することで可能です。

 単一継承で継承するクラス

| クラス | 説明 |
|:--|:--|
| converters.Converter | すべてのコンバータの基本クラス |
| converters.Boolean | シリアル化の前にboolに変換する |
| converters.Integer | シリアル化の前にintに変換する |
| converters.Float | シリアル化の前にfloatに変換する |
| converters.String | シリアル化の前にstrに変換する |

例えば、浮動小数点数が常に小数点以下2桁に丸められるようにするカスタム・コンバータを説明するために、
次のモジュールを用意しました。

 floatdb.py
```
 from datafiles import *

 data_dir = './datadir'
 data_pattern = data_dir + '/sampledb.yml'

 class RoundedFloat(converters.Float):

     @classmethod
     def to_preserialization_data(cls, python_value, **kwargs):
         number = super().to_preserialization_data(python_value, **kwargs)
         return round(number, 2)

 @datafile(data_pattern)
 class Result:
     total: RoundedFloat = 0.0

 if __name__ == '__main__':
     from pathlib import Path

     dir = Path(data_dir)
     dir.mkdir(exist_ok=True)

```


これは、次のように使用します。


```
 In [2]: # %load 40_single_inherit.py
    ...: from floatdb import *
    ...:
    ...: v1 = Result(1.2345)
    ...: v2 = !cat datadir/sampledb.yml
    ...:
    ...: v3 = Result()
    ...: v4 = v3.total
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v3)
    ...: # print(v4)
    ...:

 In [3]: print(v1)
 Result(total=1.2345)

 In [4]: print(v2)
 ['total: 1.23']

 In [5]: print(v3)
 Result(total=1.23)

 In [6]: print(v4)
 1.23

```


### 多重継承
既存のクラスを拡張して、そのクラスの機能をインスタンスに継承させることも可能です。例えば、datetimeクラスをベースにして、ISOフォーマットでシリアライズするカスタムコンバータを作成しています。


 datetimedb.py
```
 from datetime import datetime
 from datafiles import converters, datafile

 class MyDateTime(converters.Converter, datetime):

     @classmethod
     def to_preserialization_data(cls, python_value, **kwargs):
         # MyDateTime`をシリアライズ可能な値に変換
         return python_value.isoformat()

     @classmethod
     def to_python_value(cls, deserialized_data, **kwargs):
         # ファイルの値を `MyDateTime` オブジェクトに戻す
         return MyDateTime.fromisoformat(deserialized_data)

     # 追加の処理...


 @datafile("sample.yml")
 class Timestamp:
     my_datetime: MyDateTime = None

```

これは、次のように使用します。


```
 In [2]: # %load 41_datetime.py
    ...: from datetimedb import *
    ...:
    ...: v1 = Timestamp(datetime.now())
    ...: v2 = !cat datadir/timestampdb.yml
    ...: v3 = timestamp = Timestamp()
    ...: v4 = timestamp.my_datetime
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v3)
    ...: # print(v4)
    ...:

 In [3]: print(v1)
 Timestamp(my_datetime=datetime.datetime(2021, 8, 24, 13, 52, 12, 246264))

 In [4]: print(v2)
 ["my_datetime: '2021-08-24T13:45:41.983066'"]

 In [5]: print(v3)
 Timestamp(my_datetime=MyDateTime(2021, 8, 24, 13, 45, 41, 983066))

 In [6]: print(v4)
 2021-08-24 13:45:41.983066

```


### コンバータの登録

次に、自分でクラスを変更する必要がない場合（またはクラスのソースをコントロールできない場合）、任意のクラスのカスタムコンバータを登録することができます。
 isotimedb.py
```
 from datafiles import *
 from datetime import datetime

 data_dir = './datadir'
 data_pattern = data_dir + '/isotimedb.yml'

 class DateTimeConverter(converters.Converter):

     @classmethod
     def to_preserialization_data(cls, python_value, **kwargs):
         # datetimeオブジェクト をシリアライズ可能な値に変換
         return python_value.isoformat()

     @classmethod
     def to_python_value(cls, deserialized_data, **kwargs):
         # ファイルの値をdatetimeオブジェクトに戻す
         return datetime.fromisoformat(deserialized_data)

 converters.register(datetime, DateTimeConverter)

 @datafile(data_pattern)
 class Timestamp:
     my_datetime: datetime = None


 if __name__ == '__main__':
     from pathlib import Path

     dir = Path(data_dir)
     dir.mkdir(exist_ok=True)

```

次のように使用します。


```
 In [2]: # %load 42_regist_converter.py
    ...: from isotimedb import *
    ...:
    ...: v1 = Timestamp(datetime.now())
    ...: v2 = !cat datadir/isotimedb.yml
    ...: v3 = Timestamp()
    ...: v4 = v3.my_datetime
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(v3)
    ...: # print(v4)
    ...:

 In [3]: print(v1)
 Timestamp(my_datetime=datetime.datetime(2021, 8, 24, 14, 23, 53, 987143))

 In [4]: print(v2)
 ["my_datetime: '2021-08-24T14:23:53.987143'"]

 In [5]: print(v3)
 Timestamp(my_datetime=datetime.datetime(2021, 8, 24, 14, 23, 53, 987143))

 In [6]: print(v4)
 2021-08-24 14:23:53.987143

```


## Generic Type
Pythonの一般的な型はサポートされていますが、カスタム型と同様に `to_python_value` と `to_preserialization_data` の実装が必要です。クラスの CONVERTERS 属性には、指定されたジェネリック型に対応する適切なデータファイルコンバータが配置されます。マーシャリングされたデータを変換するためには、これらを使用する必要があります。

#### マーシャリング(marshalling)


```
 from typing import Generic, List, TypeVar
 from datafiles import Missing, converters, datafile
 from datafiles.utils import dedent

 data_dir = './datadir'
 data_pattern = data_dir + '/marshaldb.yml'

 S = TypeVar("S")
 T = TypeVar("T")

 class Pair(Generic[S, T], converters.Converter):
     first: S
     second: T

     def __init__(self, first: S, second: T) -> None:
         self.first = first
         self.second = second

     @classmethod
     def to_python_value(cls, deserialized_data, *, target_object=None):
         paired = zip(cls.CONVERTERS, deserialized_data)
         values = [convert.to_python_value(val) for convert, val in paired]
         return cls(*values)

     @classmethod
     def to_preserialization_data(cls, python_value, *, default_to_skip=None):
         values = [python_value.first, python_value.second]
         paired = zip(cls.CONVERTERS, values)
         return [
             convert.to_preserialization_data(val)
             for convert, val in paired
         ]

 @datafile(data_pattern)
  class Dictish:
      contents: List[Pair[str, converters.Number]]


  if __name__ == '__main__':
      from pathlib import Path
      from pprint import pprint

      dir = Path(data_dir)
      dir.mkdir(exist_ok=True)

```


これは、次のように使用します。


```
 In [2]: # %load 43_marshalling.py
    ...: from marshalldb import *
    ...: from pprint import pprint
    ...:
    ...: v1 = Dictish([Pair("a", 1), Pair("pi", 3.14)])
    ...: v2 = !cat datadir/marshalldb.yml
    ...:
    ...: v3 = list()
    ...: v4 = Dictish(v3)
    ...: v5 = v4.contents
    ...:
    ...: # pprint(v1)
    ...: # pprint(v2)
    ...: # pprint(v3)
    ...: # pprint(v4)
    ...:

 In [3]: pprint(v1)
 Dictish(contents=[<datafiles.converters._bases.GenericStringNumberPair object at 0x11105ca30>, <datafiles.converters._bases.GenericStringNumberPair object at 0x11105cb20>])

 In [4]: pprint(v2)
 ['contents:', '  -   - a', '      - 1', '  -   - pi', '      - 3.14']

 In [5]: pprint(v3)
 [<datafiles.converters._bases.GenericStringNumberPair object at 0x1120bc400>,
  <datafiles.converters._bases.GenericStringNumberPair object at 0x1120bc460>]

 In [6]: pprint(v4)
 Dictish(contents=[<datafiles.converters._bases.GenericStringNumberPair object at 0x1120bc400>, <datafiles.converters._bases.GenericStringNumberPair object at 0x1120bc460>])

 In [7]: !cat datadir/marshalldb.yml
 contents:
   -   - a
       - 1
   -   - pi
       - 3.14
```

## ファイルフォーマット
シリアライズには以下のファイルフォーマットがサポートされています。

### YAML
デフォルトでは、データファイルはYAML言語を使用してシリアル化されます。以下のファイル拡張子のいずれかがこのフォーマットを使用します。
#### 拡張子
-  `.yml`
-  `.yaml`
- (拡張子なし)


```
 In [2]: # %load 50_yaml.py
    ...: from filedb import *
    ...:
    ...: data_pattern = data_dir + '/yamldb.yml'
    ...:
    ...: @datafile(data_pattern, defaults=True)
    ...: class Sample(Base):
    ...:     fmt: str = "YAML Ain't Markup Language"
    ...:
    ...: v1 = Sample(Nested(0), [Nested(1), Nested(2)])
    ...:
    ...: # print(v1)
    ...: # !cat datadir/yamldb.yml
    ...:

 In [3]: print(v1)
 Sample(my_dict=Nested(value=0), my_list=[Nested(value=1), Nested(value=2)], my_bool=True, my_float=1.23, my_int=42, my_str='Hello, world!')

 In [4]: !cat datadir/yamldb.yml
 my_dict:
   value: 0
 my_list:
   - value: 1
   - value: 2
 my_bool: true
 my_float: 1.23
 my_int: 42
 my_str: Hello, world!

```


### JSON
JSON言語にも対応しています。以下のファイル拡張子のいずれかがこのフォーマットを使用します。
#### 拡張子
-  `.json`


```
 In [2]: # %load 51_json.py
    ...: from filedb import *
    ...:
    ...: data_pattern = data_dir + '/jsondb.yml'
    ...:
    ...: @datafile(data_pattern, defaults=True)
    ...: class Sample(Base):
    ...:     fmt: str = "JavaScript Object Notation"
    ...:
    ...: v1 = Sample(Nested(0), [Nested(1), Nested(2)])
    ...:
    ...: # print(v1)
    ...: # !cat datadir/jsondb.yml
    ...:

 In [3]: print(v1)
 Sample(my_dict=Nested(value=0), my_list=[Nested(value=1), Nested(value=2)], my_bool=True, my_float=1.23, my_int=42, my_str='Hello, world!')

 In [4]: !cat datadir/jsondb.yml
 my_dict:
   value: 0
 my_list:
   - value: 1
   - value: 2
 my_bool: true
 my_float: 1.23
 my_int: 42
 my_str: Hello, world!

```



### TOML
TOML言語にも対応しています。以下の拡張子のファイルがこのフォーマットを使用します。
#### 拡張子
-  `.toml`


```
 In [2]: # %load 52_toml.py
    ...: from filedb import *
    ...:
    ...: data_pattern = data_dir + '/tomldb.yml'
    ...:
    ...: @datafile(data_pattern, defaults=True)
    ...: class Sample(Base):
    ...:     fmt: str = "Tom's Obvious Minimal Language"
    ...:
    ...: v1 = Sample(Nested(0), [Nested(1), Nested(2)])
    ...:
    ...: # print(v1)
    ...: # !cat datadir/tomldb.yml
    ...:

 In [3]: print(v1)
 Sample(my_dict=Nested(value=0), my_list=[Nested(value=1), Nested(value=2)], my_bool=True, my_float=1.23, my_int=42, my_str='Hello, world!')

 In [4]: !cat datadir/tomldb.yml
 my_dict:
   value: 0
 my_list:
   - value: 1
   - value: 2
 my_bool: true
 my_float: 1.23
 my_int: 42
 my_str: Hello, world!


```

## カスタムフォーマット
登録制で追加フォーマットに対応しています。

### 既存のマッピング
既存のフォーマッタクラスの1つを新しいファイル拡張子にマッピングします。


```
 from datafile import datafile, formats

 formats.register('.conf', formats.YAML)

 @datafile("my-file-path.conf")
 class MyConfig:
     # ...
```

### 新しいフォーマット
新しいフォーマットをサポートするには、 `datafiles.format.Formatter` ベースクラスを拡張します。


```
 from datafile import datafile, formats


 class MyFormat(formats.Format):

     @classmethod
     def extensions(cls) -> List[str]:
         return ['.my_ext']

     @classmethod
     @abstractmethod
     def deserialize(cls, file_object: IO) -> Dict:
         # ファイルオブジェクト`を読み込んで辞書を返す

     @classmethod
     @abstractmethod
     def serialize(cls, data: Dict) -> str:
         # data`を文字列に変換する


 formats.register('.my_ext', MyFormat)


 @datafile("my-file-path.my_ext")
 class MyConfig:
     # ...
```

## ユーティリティー関数
以下の関数は、高レベルの機能を提供します。

### auto()
任意のファイルが与えられると、このライブラリはそのファイルの構造を、そのファイルに同期したPythonオブジェクトにマッピングすることを試みます。例えば、sample.ymlという名前のYAMLファイルに以下の内容が書かれているとします。

 sample.yml
```
 names:
   - Alice
   - Bob
 numbers:
   - 1
   - 2
```

次のようにして読み込むことができます。


```
 In [2]: # %load 60_utils_auto.py
    ...: !cat datadir/sample.yml
    ...:
    ...: from datafiles import auto
    ...:
    ...: sample = auto('datadir/sample.yml')
    ...: v1 = sample.names
    ...:
    ...: sample.numbers.append(3)
    ...:
    ...:
    ...: # print(v1)
    ...: # !cat datadir/sample.yml
    ...:
 names:
   - Alice
   - Bob
 numbers:
   - 1
   - 2

 In [3]: print(v1)
 ['Alice', 'Bob']

 In [4]: !cat datadir/sample.yml
 names:
   - Alice
   - Bob
 numbers:
   - 1
   - 2
   - 3

```


## 設定(Setting)
前述の動作を一時的に変更したいクライアントのために、モジュールレベルでいくつかの設定を制御することができます。すべての値のデフォルトはTrueです。

### HIDDEN_TRACEBACK
パッチを当てたメソッドで例外が発生した場合、pytest ではデフォルトでこのトレースバックが隠されます。複雑な問題をデバッグするためにこの情報が必要な場合は、次のように有効にします。


```
 import datafiles

 datafiles.settings.HIDDEN_TRACEBACK = False

```

### HOOKS_ENABLED
データファイルを使用しているクライアントのユニットテストを実行する場合、パフォーマンス向上を目的にディスクへのファイルの書き込みを避けるときなどでは、モデルの自動ロード/セーブを無効にすると便利です。


```
 mport datafiles

 def pytest_runtest_setup(item):
     """ユニットテスト中にファイルストレージを無効にする"""
     datafiles.settings.HOOKS_ENABLED = False

```


### MINIMAL_DIFFS
リストをシリアライズする際、datafilesは意図的に空のリストの意味的な表現から逸脱し、バージョンコントロールでYAMLファイルを保存するというユースケースに最適化します。

アイテムの任意の空リストを以下のように格納することで

 YAML
```
 items:
   -

```

アイテムの追加や削除は、常に1行の変更になります。一方、アイテムにアイテムを追加する場合は []にアイテムを追加すると、よりノイズの多いdiffが生成され、ファイルを手で編集するためにYAMLの仕様に関する知識が必要になります。

この動作を無効にするには


```
 import datafiles

 datafiles.settings.MINIMAL_DIFFS = False

```

### WRITE_DELAY
一部のファイルシステムでは、ファイルを書き込んだ直後に読み込んだ場合、ファイルの修正時刻（st_mtime）が変化しないことがあります。このため、急速に変化するファイルを使用する場合、断続的な問題が発生する可能性があります。

この問題を解決するために、データファイルがファイルシステムに書き込まれた後に、短い遅延時間を挿入することができます。


```
 import datafiles

 datafiles.settings.WRITE_DELAY = 0.01  # 秒数

```


## Dataclass_type_validator によるデータの検証
datafiles ではタイプヒントを利用してデータをオブジェうとにマッピングしているだけなので、データの検証(Validation)については不十分です。
この機能不足を補うために dataclass_type_validator を使ってみましょう。

まず、次のようにインストールします。

 bash
```
 $ pip install dataclass_type_validator
```

次のようなモデルのモジュールを作成します。
 userdb.py
```
 from datafiles import *
 from typing import List
 from dataclass_type_validator import (
     dataclass_type_validator, TypeValidationError
     )

 @datafile("userdb/{self.id}.yml")
 class User:

     id: int
     name: str
     friend_ids: List[int]

     def __post_init__(self):
         dataclass_type_validator(self)

```

ここでのポイントは、 `__post_init__()` メソッドを記述することです。

このモデルでオブジェクトを生成するとき、意図的にモデルで定義した型と異なるデータを与えてみます。


```
 In [2]: # %load 70_validator.py
    ...: from userdb import *
    ...:
    ...: v1 = User(id=10, name='John Smith', friend_ids=[1, 2])
    ...:
    ...: try:
    ...:     v2 = User(id='a', name=['John', 'Smith'], friend_ids=['a'])
    ...:     msg = ''
    ...: except TypeValidationError as e:
    ...:     v2 = None
    ...:     msg = e
    ...:
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(msg)
    ...:

 In [3]: print(v1)
 User(id=10, name='John Smith', friend_ids=[1, 2])

 In [4]: print(v2)
 None

 In [5]: print(msg)
 userdb.User (errors = {'id': "must be an instance of <class 'int'>, but received <class 'str'>", 'name': "must be an instance of <class 'str'>, but received <class 'list'>", 'friend_ids': 'must be an instance of typing.List[int], but there are some errors: ["must be an instance of <class \'int\'>, but received <class \'str\'>"]'})

```

きちんとデータの検証が行われて、 `TypeValidationError` 例外が発生しています。


## まとめ
ファイルベースのORMはJSONや、YAML, TOMLをサポートしていてファイルフォーマットを抽象化することができます。
また、ファイル入出力をプログラマが考慮しなくてもよいため、効率よくコードを開発することができます。



## 参考
- [datafiles ソースコード ](https://github.com/jacebrowning/datafiles)
- [dataclass-type-validator ソースコード  ](https://github.com/levii/dataclass-type-validator)　
