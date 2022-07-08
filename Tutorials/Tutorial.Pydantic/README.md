pydantic をORMとして使ってみよう
=================
## pydantic について
Pydanticは、pythonの[タイプヒント ](https://docs.python.org/ja/3/library/typing.html)を用いたデータ検証および設定管理を行うためのライブラリです。Pythonでデータがどうあるべきかを定義し、pydanticでそれをチェックします。
pydanticは実行時にタイプヒントの情報をもとにデータを検証して、データが無効な場合はユーザーフレンドリーなエラーを提供します。

次のような長所と短所があります。

- 長所
  - 簡単で素敵な方法で実行時にデータ検証を行うことができる。
  - FastAPIやTyperとのシームレスな統合ができる
  - データとデータスキーマをエクスポートすることをうまく実装できる

- 短所
- 周期的な関係（Cyclic Relation) を定義することができない
- SQLAlchemyのbackref関数をシミュレートする方法がない
- ファイルとの同期はサポートされていない

通常は、pydantoc はシリアル化/非シリアル化のためのライブラリですが、
この pydantic をファイルベースのORMとして利用してみます。

## インストール
 bash
```
 $ pip install pydantic
 
```

pydanticには、必要に応じて以下のオプションの拡張モジュールを利用することができます。

- [email-validator ](https://pypi.org/project/email-validator/)：　電子メールの検証をサポートする
- [typing-extensions ](https://pypi.org/project/typing-extensions/)：　Python 3.8より前のリテラル(Literal)の使用をサポートする
- [python-dotenv ](https://pypi.org/project/python-dotenv/) ：　設定付きdotenvファイルのサポートする

これらのパッケージは必要に応じて、次のようにインストールします。

 bash
```
 $ pip install email-validator
 $ pip install typing_extensions
 $ pip install python-dotenv
```


## モデルクラス
pydanticでオブジェクトを定義するのは、BaseModelを継承した新しいクラスを作るのと同じくらい簡単です。このクラスから新しいオブジェクトを作成すると、pydanticは結果として得られるモデル・インスタンスのフィールドが、モデル上で定義されたフィールド・タイプに適合することを保証します。

pydantic の `BaseModel` クラスを継承して、 `User` モデルクラスを作成します。

 model_user.py
```
 from datetime import datetime
 from typing import List, Optional
 from pydantic import BaseModel
 
 class User(BaseModel):
     id: int
     username : str
     password : str
     confirm_password : str
     email: str
     alias = 'anonymous'
     timestamp: Optional[datetime] = None
     friends: List[int] = []
     
```

ここで、typing モジュールの  `List` と `Optional` をインポートしています。

-  `List` ：リスト型の型ヒントを定義するときに使用
-  `Optional` ：型ヒントに `None` を定義するときに使用　

pydanticでは、組み込みのタイプヒント構文を使って各変数のデータ型を決定します。上記のモデルについて、1つずつ説明してゆきます。

-  `id` ：　IDを表す整数型の変数です。デフォルト値が用意されていないため、このフィールドは必須です。
文字列、バイト、またはフロートは、可能であれば整数に変換されますが、それ以外の場合は例外が発生します。
-  `username` ：ユーザー名を表す文字列変数で、このフィールドは必須です。
-  `password` ：パスワードを表す文字列変数で、このフィールドは必須です。
-  `confirm_password` ：確認用のパスワードを表す文字列変数で、このフィールドは必須です。
このパスワードは後のデータ検証に使用されます。
-  `email` ：メールアドレスを表す文字列変数で、このフィールドは必須です。
-  `alias` ：ユーザ名の別名を表す文字列変数で、このフィールドはオプション(必須ではない)です。
オブジェクト作成時に提供されなければ、 `anonymous` が設定されます。
-  `timestamp` ：日付/時間フィールドで、オプション(必須ではない)です。
pydanticは、unix timestamp のint型か、日付/時間を表す文字列を処理します。
-  `friends` ：整数入力のリスト。



```
 In [2]: # %load 01_create_obj.py
    ...: from model_user import User
    ...:
    ...: data = { 'id': '1001',
    ...:          'username': 'Jack Bauer',
    ...:          'password': 'Password123',
    ...:          'confirm_password': 'Password123',
    ...:          'email': 'jack@ctu.com',
    ...:          'timestamp': '2021-08-24 20:30',
    ...:          'friends': [1, '2', b'3']
    ...:        }
    ...:
    ...: user = User(**data)
    ...:
    ...: # print(user)
    ...:
 
 In [3]: print(user)
 id=1234 username='Jack Bauer' password='Password123' confirm_password='Password123' email='jack@ctu.com' timestamp=datetime.datetime(2021, 8, 24, 20, 30) friends=[1, 2, 3] alias='anonymous'
 
```


モデルクラス  `User` のコンストラクタには文字列で与えていますが、フィールド `id` は自動的に整数に変換されていることに注目してください。同様に、 `friends` フィールドは、バイト( `b'3'` )も自動的に整数( `3` )に変換されています。

### BaseModel
BaseModel を継承したモデルクラスでは、次のメソッドと属性を持つようになります。

-  `dict()` ：モデルのフィールドと値の辞書を返します。
-  `json()` ：JSON 文字列表現のディクショナリーを返します。
-  `copy()` ：モデルのディープコピーを返します。
-  `parse_obj()` ：任意のオブジェクトをモデルにロードするユーティリティーで、オブジェクトが辞書でない場合はエラー処理を行います。
-  `parse_raw()` ：さまざまな形式の文字列を読み込むユーティリティーです。
-  `parse_field()` ：parse_raw()と似ていますが、ファイル用です。
-  `from_orm()` ：任意のクラスからモデルにデータを読み込みます。
-  `schema()` ：モデルを JSON スキーマとして表す辞書を返します。
-  `schema_json()` ：schema() の JSON 文字列表現を返します。
-  `construct()` ：検証を行わずにモデルを作成するためのクラスメソッドです。
-  `__fields_set__` ：モデルのインスタンスが初期化されたときに設定されたフィールドの名前のセット
- _ `_fields__` ：モデルのフィールドの辞書
-  `__config__ ` ：モデルの構成クラス


Userモデルでは `id` をint型で定義していますが、ここに文字列を与えるように変更してみましょう。

 pytohn
```
 In [2]: # %load 02_id_string.py
    ...: from model_user import User
    ...:
    ...: data = { 'id': 'CTU Agent',
    ...:          'username': 'Jack Bauer',
    ...:          'password': 'Password123',
    ...:          'confirm_password': 'Password123',
    ...:          'email': 'jack@ctu.com',
    ...:          'timestamp': '2021-08-24 20:30',
    ...:          'friends': [1, '2', b'3']
    ...:        }
    ...:
    ...: user = User(**data)
    ...:
    ...: # print(user)
    ...:
 ---------------------------------------------------------------------------
 ValidationError                           Traceback (most recent call last)
 <ipython-input-2-5a9b5650ebf2> in <module>
      11        }
      12
 ---> 13 user = User(**data)
      14
      15 # print(user)
 
 ~/anaconda3/envs/class_database/lib/python3.9/site-packages/pydantic/main.cpython-39-darwin.so in pydantic.main.BaseModel.__init__()
 
 ValidationError: 1 validation error for User
 id
   value is not a valid integer (type=type_error.integer)
   
```

インスタンスオブジェクトを作成する段階で、 `ValidationError` の例外が発生しています。


## ValidationError
 `ValidationError` の例外を処理するようにしましょう。


```
 In [2]: # %load 03_try_exept.py
    ...: from model_user import User
    ...: from pydantic import ValidationError
    ...:
    ...: data = { 'id': 'CTU Agent',
    ...:          'username': 'Jack Bauer',
    ...:          'password': 'Password123',
    ...:          'confirm_password': 'Password123',
    ...:          'email': 'jack@ctu.com',
    ...:          'timestamp': '2021-08-24 20:30',
    ...:          'friends': [1, '2', b'3']
    ...:        }
    ...:
    ...: try:
    ...:     user = User(**data)
    ...:     msg = ''
    ...: except ValidationError as e:
    ...:     user = None
    ...:     msg = e.json()
    ...:
    ...: # print(user)
    ...: # print(mg)
    ...:
 
 In [3]: print(user)
 None
 
 In [4]: print(msg)
 [
   {
     "loc": [
       "id"
     ],
     "msg": "value is not a valid integer",
     "type": "type_error.integer"
   }
 ]
 
```

 `ValidationError` の例外が発生した理由がJSON形式で取得しています。

## フィールドタイプ
pydanticは、Pythonの検証一般的な型のほとんどをサポートしています。
その他にtypingやipaddress、enum、decimal、pathlib、uuidなどの標準ライブラリの型も使用することができます。
全リストは以下の通りです。

#### Pythonの一般的なタイプ
- bool
- int
- float
- str
- bytes
- list
- tuple
- dict
- set
- frozenset
- datetime.date
- datetime.time
- datetime.datetime
- datetime.timedelta
- typing.Any
- typing.TypeVar
- typing.Union
- typing.Optional
- typing.List
- typing.Tuple
- typing.Dict
- typing.Set
- typing.FrozenSet
- typing.Sequence
- typing.Iterable
- typing.Type
- typing.Callable
- typing.Pattern
- ipaddress.IPv4Address
- ipaddress.IPv4Interface
- ipaddress.IPv4Network
- ipaddress.IPv6Address
- ipaddress.IPv6Interface
- ipaddress.IPv6Network
- enum.Enum
- enum.IntEnum
- decimal.Decimal
- pathlib.Path
- uuid.UUID
- ByteSize
- HttpUrl
- AnyUrl
- SecretStr
- EmailStr (email-validator のインストールが必要)

前述の User モデルのフィールド定義を少し変えてみましょう。

 modeL_user3.py
```
 from datetime import datetime
 from typing import List, Optional
 from pydantic import (
     BaseModel, EmailStr, SecretStr,
     ValidationError, validator
     )
     
 class User(BaseModel):
     id: int
     username : str
     password: SecretStr
     confirm_password : SecretStr
     email: EmailStr
     alias = 'anonymous'
     comment: str = ''
     timestamp: Optional[datetime] = None
     friends: List[int] = []
 
     @validator('id')
     def id_must_be_4_digits(cls, v):
         if len(str(v)) != 4:
             raise ValueError('must be 4 digits')
         return v
 
     @validator('confirm_password')
     def passwords_match(cls, v, values, **kwargs):
         if 'password' in values and v != values['password']:
             raise ValueError('passwords do not match')
         return v
         
```

このモデルを使ってみましょう。まず、フィールドのタイプとして SecretStr で定義した  `passwod` と  `confirm_password` について注目してください。


```
 In [1]: %load 04_email_step1.py
 
    ...: data = { 'id': '1001',
    ...:          'username': 'Jack Bauer',
    ...:          'password': 'Password123',
    ...:          'confirm_password': 'Password123',
    ...:          'email': 'jack@ctu.com',
    ...:          'timestamp': '2021-08-24 20:30',
    ...:          'friends': [1, '2', b'3']
    ...:        }
    ...:
    ...: def func(user_data):
    ...:     try:
    ...:         user = User(**user_data)
    ...:     except ValidationError as e:
    ...:         user = None
    ...:         print(e)
    ...:     return user
    ...:
    ...: # print(user)
    ...: # print(v1)
    ...: # print(v2)
    ...: # print(type(user.password))
    ...: # user.password = 'python'
    ...: # print(user.password)
    ...: # print(type(user.password))
    ...:
 
 In [3]: print(user)
 id=1001 username='Jack Bauer' password=SecretStr('**********') confirm_password=SecretStr('**********') email='jack@ctu.com' comment='' timestamp=datetime.datetime(2021, 8, 24, 20, 30) friends=[1, 2, 3] alias='anonymous'
 
 In [4]: print(v1)
 **********
 
 In [5]: print(v2)
 True
 
 In [6]: print(type(user.password))
 <class 'pydantic.types.SecretStr'>
 
 In [7]: user.password = 'python'
 
 In [8]: print(user.password)

 
 In [9]: print(type(user.password))
 <class 'str'>
 
```


 `passwod` と  `confirm_password` は表示するとアスタリスク記号( `*` ) になっています。
注意する必要があることは、Python では変数の型は動的にアサインされることです。つまり、モデルクラスのインスタンスオブジェクトを生成するタイミングでは SecretStr として扱われますが、そのあとで文字列をアサインしてしまうと、SecretStr ではなくなるということです。

次に、ユーザのデータでパスワードがミスマッチするようにして、メールアドレスにもただ単に'jack`とだけにして、モデルクラスからオブジェクトを生成してましょう。


```
 In [6]: %load 04_email_step2.py
 
 In [7]: # %load 04_email_step2.py
    ...:
    ...: data['email'] = 'jack'
    ...: data['confirm_password'] = 'password'
    ...: user2 = func(data)
    ...:
    ...: # u = func(data)
    ...: # print(u)
    ...:
 2 validation errors for User
 confirm_password
   passwords do not match (type=value_error)
 email
   value is not a valid email address (type=value_error.email)
 
 
```

SecretStr は表示されるときはアスタリスク記号( `*` )に置き換えられますが、値としてはきちんと評価されているのがわかります。
また、メールアドレスについても使用可能なものかどうかを評価してくれます。


## 制限付きの’タイプを備えたモデル
Pydantic は、コンストレイントタイプ(Constrained Type) を使って、独自の制限を加えることができます。以下の例を見てみましょう。

 model_sample.py
```
 from pydantic import (
     BaseModel,
     NegativeInt,
     PositiveInt,
     conint,
     conlist,
     constr
 )
 
 class SampleModel(BaseModel):
     # 最小の長さは2、最大の長さは10
     short_str: constr(min_length=2, max_length=10)
     # 正規表現
     regex_str: constr(regex=r'^apple (pie|tart|sandwich)$')
     # remove whitespace from string
     strip_str: constr(strip_whitespace=True)
 
     # 値は1000より大きく、かつ1024より小さい
     big_int: conint(gt=1000, lt=1024)
 
     # 値は５の倍数
     mod_int: conint(multiple_of=5)
 
     # 値は正数
     pos_int: PositiveInt
 
     # 値は負数
     neg_int: NegativeInt
 
     # 整数の値を１つから４まで保持するリスト
     short_list: conlist(int, min_items=1, max_items=4)
 
```

## タイプの厳密性を備えたモデル
検証された値が対応するフィールドの型もしくは、その型のサブタイプである場合だけ、検証をパスする厳格な制限を与えたいときは、探している場合は、次の厳格な型(Constrained Type))を使用できます。

- StrictStr
- StrictInt
- StrictFloat
- StrictBool

次の例は、継承したクラスにStrictBoolを強制する適切な方法を示しています。

 model_strict.py
```
 from pydantic import BaseModel, StrictBool
 
 class StrictBoolModel(BaseModel):
     strict_bool: StrictBool
     
```

 `StrictBoolModel` モデルは、入力として `True` か `False` のどちらかしか受け付けないので、文字列の False は、 `ValidationError` が発生します。


```
 In [2]: # %load 05_strict.py
    ...: from model_strict import *
    ...:
    ...: data = [
    ...:     { 'strict_bool': True },
    ...:     { 'strict_bool': False },
    ...:     { 'strict_bool': 'True' },
    ...:     { 'strict_bool': 'False' },
    ...:     { 'strict_bool': 1 },
    ...:     { 'strict_bool': 0 },
    ...:     { 'strict_bool': None },
    ...: ]
    ...:
    ...: def func():
    ...:     for d in data:
    ...:         try:
    ...:             flag = StrictBoolModel(**d)
    ...:         except ValidationError as e:
    ...:             flag = e
    ...:         val = d['strict_bool']
    ...:         print(f'{val}({type(val)}): {flag}')
    ...:
    ...: # func()
    ...:
 
 In [3]: func()
 True(<class 'bool'>): strict_bool=True
 False(<class 'bool'>): strict_bool=False
 True(<class 'str'>): 1 validation error for StrictBoolModel
 strict_bool
   value is not a valid boolean (type=value_error.strictbool)
 False(<class 'str'>): 1 validation error for StrictBoolModel
 strict_bool
   value is not a valid boolean (type=value_error.strictbool)
 1(<class 'int'>): 1 validation error for StrictBoolModel
 strict_bool
   value is not a valid boolean (type=value_error.strictbool)
 0(<class 'int'>): 1 validation error for StrictBoolModel
 strict_bool
   value is not a valid boolean (type=value_error.strictbool)
 None(<class 'NoneType'>): 1 validation error for StrictBoolModel
 strict_bool
   none is not an allowed value (type=type_error.none.not_allowed)
 
```

## バリデータ
pydantic の BaseModel を継承したクラスの中で  `validator` デコレーターを使用して独自のカスタムバリデータを作成することもできます。
次の例では、 `id` フィールドの値が4桁であるかどうか、 `confirm_password` フィールドの値が  `password` フィールドと一致するかどうかを判定しています。

 model_user2.py
```
 from datetime import datetime
 from typing import List, Optional
 from pydantic import BaseModel, ValidationError, validator
 
 class User(BaseModel):
     id: int
     username : str
     password : str
     confirm_password : str
     alias = 'anonymous'
     comment: str = ''
     timestamp: Optional[datetime] = None
     friends: List[int] = []
 
     @validator('id')
     def id_must_be_4_digits(cls, v):
         if len(str(v)) != 4:
             raise ValueError('must be 4 digits')
         return v
 
     @validator('confirm_password')
     def passwords_match(cls, v, values, **kwargs):
         if 'password' in values and v != values['password']:
             raise ValueError('passwords do not match')
         return v
 
```

テストのために次ののデータを用意します。

 test_data.py
```
 data = [
     { 'id': '1000',
       'username': 'Jack Bauer',
       'password': 'Password123',
       'confirm_password': 'Password123',
       'comment': 'TestCase 1: OK'
       'timestamp': '2021-08-24 20:30',
       'friends': [1, '2', b'3']
     },
     { 'id': '1001',
       'username': 'Chloe O'Brian',
       'password': 'Password123',
       'confirm_password': 'Password',
       'comment': 'TestCase 2: Password missmatch'
       'timestamp': '2021-08-24 20:30',
       'friends': [1, '2', b'3']
     },
     { 'id': '10003',
           'username': 'Anthony Tony',
           'password': 'Password123',
           'confirm_password': 'Password123',
           'comment': 'TestCase 3: id length long'
           'timestamp': '2021-08-24 20:30',
           'friends': [1, '2', b'3']
         },
         { 'id': '104',
           'username': 'David Gilmour',
           'password': 'Password123',
           'confirm_password': 'Password123',
           'comment': 'TestCase 4: id length short'
           'timestamp': '2021-08-24 20:30',
           'friends': [1, '2', b'3']
         }
     ]
```



```
 In [2]: # %load 06_custom_validator.py
    ...: from model_user2 import *
    ...: from test_data import test_data
    ...: from pprint import pprint
    ...:
    ...: def func():
    ...:     for d in test_data:
    ...:         try:
    ...:             user = User(**d)
    ...:         except ValidationError as e:
    ...:             user = e
    ...:         print(f'{d["comment"]} - {d["username"]}:')
    ...:         pprint(f'{user}')
    ...:
    ...: # func()
    ...:
 
 In [3]: func()
 TestCase 1: OK - Jack Bauer:
 ("id=1000 username='Jack Bauer' password='Password123' "
  "confirm_password='Password123' comment='TestCase 1: OK' "
  'timestamp=datetime.datetime(2021, 8, 24, 20, 30) friends=[1, 2, 3] '
  "alias='anonymous'")
 TestCase 2: Password missmatch - Chloe O'Brian:
 ('1 validation error for User\n'
  'confirm_password\n'
  '  passwords do not match (type=value_error)')
 TestCase 3: id length long - Anthony Tony:
 '1 validation error for User\nid\n  must be 4 digits (type=value_error)'
 TestCase 4: id length short - David Gilmour:
 '1 validation error for User\nid\n  must be 4 digits (type=value_error)'
 
```





## 参考
- pydantic 
  - [ソースコード　](https://github.com/samuelcolvin/pydantic)
  - [ドキュメント ](https://pydantic-docs.helpmanual.io/)
- [pydantic-factories  ](https://github.com/Goldziher/pydantic-factories)：pydanticベースのモデルやデータクラスのための強力なモックデータ生成機能を提供するもの




