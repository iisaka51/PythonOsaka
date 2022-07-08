データクラスと名前付きタプルとの比較
=================
# はじめに
この資料は、Python のデータクラスと名前付きタプルについて、比較したものです。
# データクラス
Python 3.7 から導入された dataclass は、文字通りデータのためのクラスです。

次のような特徴があり、 データを保持するときに非常に便利なものです。

　　クラスがデータを保持するためのものと明示できる
　　クラスの初期化とバリデーションが簡単
　　クラスを参照したとき保持している値が明示される
　　データへのアクセスが簡単
　　辞書(dict)との相互変換が簡単

# 辞書とはどう違うのか
Python の辞書はキーに対して値を持つことができます。


```
 user = dict(name='Freddie', id=1, email='freddie@example.com')
 >>> user
 {'name': 'Freddie', 'id': 1, 'email': 'freddie@example.com'}
 
```

キーを指定して値を参照する場合は、次のように記述します。


```
 >>> user['name']
 'Freddie'
```

キーはクラス(dict)の属性ではないので、ドット表記で指定することはできません。


```
 >>> user.name
 Traceback (most recent call last):
   File "<stdin>", line 1, in <module>
 AttributeError: 'dict' object has no attribute 'name'
 >>>
```


```
 >>> dir(user)
 ['__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values']
```

# データをクラスで定義する
構成情報などを保持するときなどに、データをクラス変数として定義することがあります。


```
 In [2]: # %load c02_class_variables.py
    ...: class User(object):
    ...:     id: int = 1
    ...:     name: str = 'Freddie'
    ...:     email: str = 'freddie@example.com'
    ...:
    ...: user = User()
    ...: # user.name
    ...: # user
    ...:
 
 In [3]: user.name
 Out[3]: 'Freddie'
 
 In [4]: user
 Out[4]: <__main__.User at 0x7fb3ecd675d0>
 
 In [5]: user.__dict__
 Out[5]: {'id': 1, 'name': 'Freddie', 'email': 'freddie@example.com'}
 
```

変数はクラスの属性となるのでドット表記で値を参照することができるので、データにアクセスしやすくなります。

しかし、静的に定義する場合はよいのですが、動的に変数を設定する場合はそれぞれの変数に個別に設定する必要があります。
また、インスタンスオブジェクトを参照しても単純には内容を知ることができません。
このため通常は、次のように  `__init__` と  `__repr__` を定義する必要がでてきます。


```
 In [2]: # %load c03_class_with_variables.py
    ...: class User(object):
    ...:     def __init__(self,
    ...:         id: int = 0,
    ...:         name: str = '',
    ...:         email: str = '',
    ...:     ):
    ...:         self.id = id
    ...:         self.name = name
    ...:         self.email = email
    ...:
    ...:     def __repr__(self):
    ...:         v = (  'User('
    ...:               f'id={self.id}, '
    ...:               f'name="{self.name}", '
    ...:               f'email="{self.email})"' )
    ...:         return v
    ...:
    ...: user = User(id=1, name='Freddie', email='freddie@example.com')
    ...:
    ...: # user
    ...: # user.name
    ...:
 
 In [3]: user
 Out[3]: User(id=1, name="Freddie", email="freddie@example.com)"
 
 In [4]: user.name
 Out[4]: 'Freddie'
 
 In [5]: user.name = 'Brain'
 
 In [6]:
```

単純にクラスの属性でデータを保持すると、変更できてしまいます。これを定義後は変更できないようにすsるためには、 `@property` を使ってデータごとにアクセスメソッドを定義する必要があります。


```
 In [2]: # %load c04_class_with_property.py
    ...: class User(object):
    ...:     def __init__(self,
    ...:         id: int = 0,
    ...:         name: str = '',
    ...:         email: str = '',
    ...:     ):
    ...:         self.__id = id
    ...:         self.__name = name
    ...:         self.__email = email
    ...:
    ...:     @property
    ...:     def id(self):
    ...:         return self.__id
    ...:
    ...:     @property
    ...:     def name(self):
    ...:         return self.__name
    ...:
    ...:     @property
    ...:     def email(self):
    ...:         return self.__email
    ...:
    ...:     def __repr__(self):
    ...:         v = (  'User('
    ...:               f'id={self.__id}, '
    ...:               f'name="{self.__name}", '
    ...:               f'email="{self.__email})"' )
    ...:         return v
    ...:
    ...: user = User(id=1, name='Freddie', email='freddie@example.com')
    ...:
    ...: # user
    ...: # user.name
    ...: # user.name = 'Brian'
    ...:
 
 In [3]: user
 Out[3]: User(id=1, name="Freddie", email="freddie@example.com)"
 
 In [4]: user.name
 Out[4]: 'Freddie'
 
 In [5]: user.name = 'Brian'
 ---------------------------------------------------------------------------
 AttributeError                            Traceback (most recent call last)
 <ipython-input-5-5e54b473eb2c> in <module>
 ----> 1 user.name = 'Brian'
 
 AttributeError: can't set attribute
 
 In [6]:
 
```

コーディング量としてはかなり増えてしまうことになります。
データクラスを使用するとこうした煩雑な定義を省くことができます。

> **ミュータブル(mutable) と イミュータブル(immutable)**
> プログラミング用語でしばしば使われる言葉で、イミュータブル(immutable) は「不変」を意味する言葉です。
>一度生成したら値を変えることができないオブジェクトに対して使われます。これとは逆に変更可能なオブジェクトはミュータブルであると言われます。


## データクラスの使用方法

標準ライブラリの dataclasses から  `dataclass` をインポートして、クラス定義をデコレートします。


```
 from dataclasses import dataclass
 
 @dataclass
 class User(object):
     name: str = ''
     id: int = 0
     email: str = ''
     
```

python
```
 In [2]: # %load c05_using_dataclas.py
    ...: from dataclasses import dataclass
    ...:
    ...: @dataclass
    ...: class User(object):
    ...:     name: str = ''
    ...:     id: int = 0
    ...:     email: str = ''
    ...:
    ...: user = User(name='Freddie', id=1, email='freddie@example.com')
    ...:
    ...: # user
    ...: # user.name
    ...:
 
 In [3]: user
 Out[3]: User(name='Freddie', id=1, email='freddie@example.com')
 
 In [4]: user.name
 Out[4]: 'Freddie'
 
 In [5]: user.name = 'Brian'
 
 In [6]: user
 Out[6]: User(id=1, name='Brian', email='freddie@example.com')
 
 In [7]:
 
```

データクラスを使用すると、変数はクラスの属性となります。そのためドット表記で値を参照することができます。
ただし、このままではミュータブル（mutable)つまり、値を変更できてしまうことに注意してください、
値を変更できない（イミュータブル(imutable))にしたいときは `@dataclass(frozen=True)` としてデコレートします。


```
 In [2]: # %load c06_using_dataclas_imutable.py
    ...: from dataclasses import dataclass
    ...:
    ...: @dataclass(frozen=True)
    ...: class User(object):
    ...:     id: int = 0
    ...:     name: str = ''
    ...:     email: str = ''
    ...:
    ...: user = User(id=1, name='Freddie', email='freddie@example.com')
    ...:
    ...: # user
    ...: # user.name
    ...:
 
 In [3]: user
 Out[3]: User(id=1, name='Freddie', email='freddie@example.com')
 
 In [4]: user.name
 Out[4]: 'Freddie'
 
 In [5]: user.name = 'Brian'
 ---------------------------------------------------------------------------
 FrozenInstanceError                       Traceback (most recent call last)
 <ipython-input-5-5e54b473eb2c> in <module>
 ----> 1 user.name = 'Brian'
 
 <string> in __setattr__(self, name, value)
 
 FrozenInstanceError: cannot assign to field 'name'
 
 In [6]:
 
```

## 初期化時に値をチェック
dataclass は `__init__` を呼び出したあと、定義されていれば `__post_init__` を呼び出してくれます。フィールド定義で `InitVar` で型アノテーションをした変数が、 `__post_init__` に渡されます。


```
 In [2]: # %load c07_dataclass_post_init.py
    ...: from dataclasses import dataclass, InitVar
    ...:
    ...: @dataclass
    ...: class User(object):
    ...:     id: InitVar[int] = 0
    ...:     name: str = ''
    ...:     email: str = ''
    ...:
    ...:     def __post_init__(self, id):
    ...:         if id < 0:
    ...:             raise(ValueError('ID must be positive integer'))
    ...:
    ...: user = User(id=-1, name='Freddie', email='freddie@example.com')
    ...:
 ---------------------------------------------------------------------------
 ValueError                                Traceback (most recent call last)
 <ipython-input-2-cda6568cfc98> in <module>
      12             raise(ValueError('ID must be positive integer'))
      13
 ---> 14 user = User(id=-1, name='Freddie', email='freddie@example.com')
 
 <string> in __init__(self, id, name, email)
 
 <ipython-input-2-cda6568cfc98> in __post_init__(self, id)
      10     def __post_init__(self, id):
      11         if id < 0:
 ---> 12             raise(ValueError('ID must be positive integer'))
      13
      14 user = User(id=-1, name='Freddie', email='freddie@example.com')
 
 ValueError: ID must be positive integer
 
 In [3]:
 
```

## 辞書からデータクラスに変換
これは簡単です。 アンパック演算子( `**` )で辞書の変数を指示するだけです。

python
```
 In [2]: # %load c07_dataclass_from_dict.py
    ...: from dataclasses import dataclass
    ...:
    ...: user_data = {
    ...:     'id': 1,
    ...:     'name': 'Freddie',
    ...:     'email': 'freddie@example.com'
    ...: }
    ...:
    ...: @dataclass
    ...: class User(object):
    ...:     id: int = 0
    ...:     name: str = ''
    ...:     email: str = ''
    ...:
    ...: user = User(**user_data)
    ...:
 
 In [3]: user
 Out[3]: User(id=1, name='Freddie', email='freddie@example.com')
 
 In [4]:
```


## データクラスを辞書に変換

dataclasses モジュールからヘルパー関数  `asdict()` をインポートします。


```
 In [4]: from dataclasses import dataclass, asdict
 
 In [5]: users[0]
 Out[5]: User(id=1, name='Freddie', email='freddie@example.com')
 
 In [6]: asdict(users[0])
 Out[6]: {'id': 1, 'name': 'Freddie', 'email': 'freddie@example.com'}
 
 In [7]:
```


## クラスとデータクラスの違い
クラスとデータクラスにはオブジェクトを比較するときに大きな違いがあります。次のコードを見てみましょう。


```
 In [2]: # %load c09_class_vs_dataclass.py
    ...: from dataclasses import dataclass
    ...:
    ...: class User_C(object):
    ...:     def __init__(self,
    ...:         id: int = 0,
    ...:         name: str = '',
    ...:         email: str = '',
    ...:     ):
    ...:         self.id = id
    ...:         self.name = name
    ...:         self.email = email
    ...:
    ...:     def __repr__(self):
    ...:         v = (  'User('
    ...:               f'id={self.id}, '
    ...:               f'name="{self.name}", '
    ...:               f'email="{self.email})"' )
    ...:         return v
    ...:
    ...:
    ...: @dataclass
    ...: class User_D(object):
    ...:     id: int = 0
    ...:     name: str = ''
    ...:     email: str = ''
    ...:
    ...: v1 = User_C(id=1, name='Freddie', email='freddie@example.com')
    ...: v2 = User_C(id=1, name='Freddie', email='freddie@example.com')
    ...:
    ...: v3 = User_D(id=1, name='Freddie', email='freddie@example.com')
    ...: v4 = User_D(id=1, name='Freddie', email='freddie@example.com')
    ...:
    ...: assert (v1 == v2) == False
    ...: assert (v3 == v4) == True
    ...:
    ...: # v1, v3
    ...:
 
 In [3]:
 
```

 `v1` と  `v2` は  `User_C` クラスのインスタンスオブジェクトで、同じ値で初期化されています。しかし評価すると  `False` になります。これに対して、データクラスでは同じ内容であれば  `True` として評価されます。


# 名前付きタプル

Python には namedtuple というデータ型があります。名前付きタプル(NamedTuple)は、文字通り各要素に名前が付けられたタプルです。
まず、tuple とは何が違うのかを説明してみましょう。

Python の tuple は単純なデータ型で、任意のオブジェクトを含めることができ、グループ化するような場合に使用されます。
同様なものに list 型がありますが、tuple はイミュータブル(imutable) であり、定義後は変更することができません。


```
 In [2]: # %load c10_tuple_intro.py
    ...: user = (1, 'Freddie', 'freddie@example.com')
    ...:
    ...: # user
    ...: # user[1]
    ...: # user[1] = 'Brian'
    ...:
 
 In [3]: user
 Out[3]: (1, 'Freddie', 'freddie@example.com')
 
 In [4]: user[1]
 Out[4]: 'Freddie'
 
 In [5]: user[1]='Brian'
 ---------------------------------------------------------------------------
 TypeError                                 Traceback (most recent call last)
 <ipython-input-5-f2f345e1249f> in <module>
 ----> 1 user[1]='Brian'
 
 TypeError: 'tuple' object does not support item assignment
 
 In [6]:
```

list と同様に各要素にはインデックスでしかアクセスできません。可読性を高めるために次のようにグローバル変数を定義することもできますが、あまりスマートとは言えません。
それは、tuple の構造と同レベルで、このグローバル変数も保守をしてゆく必要があることと、グローバス変数が何かしらのバグによって、内容が変更される可能性があるためです。


```
 In [2]: # %load c11_tuple_global_variable.py
    ...: USER_ID=0
    ...: USER_NAME=1
    ...: USER_EMAIL=2
    ...:
    ...: user = (1, 'Freddie', 'freddie@example.com')
    ...:
    ...: # user
    ...: # user[USER_NAME]
    ...:
    ...: from enum import Enum
    ...:
    ...: class UserKey(Enum):
    ...:     USER_ID = 0
    ...:     USER_NAME=1
    ...:     USER_EMAIL=2
    ...:
    ...: user[UserKey.USER_NAME.value]
    ...:
 Out[2]: 'Freddie'
 
 In [3]:
 
```


グローバル変数を書き換えられなしようにするために　enum を使って定義する方法もありますが、
構造変化には対応できないことには変わりありません。



## collections.namedtuple を使う方法
名前付きタプル(NamedTuple)には2つの実装があります。はじめに説明する方法は、 collections.namedtuple です。
Python2.6から実装されているため、Pythonバージョンを選ばない方法です。


```
 In [2]: # %load c12_collection_namedtuple.py
    ...: from collections import namedtuple
    ...:
    ...: User = namedtuple("User", "id name email")
    ...:
    ...: user = User(1, "Freddie", "freddie@example.com")
    ...:
    ...: # user
    ...: # user[1]
    ...: # user.name
    ...: # user.name = "Brian"
    ...:
    ...:
 
 In [3]: user
 Out[3]: User(id=1, name='Freddie', email='freddie@example.com')
 
 In [4]: user[1]
 Out[4]: 'Freddie'
 
 In [5]: user.name
 Out[5]: 'Freddie'
 
 In [6]: user.name = 'Brian'
 ---------------------------------------------------------------------------
 AttributeError                            Traceback (most recent call last)
 <ipython-input-6-5e54b473eb2c> in <module>
 ----> 1 user.name = 'Brian'
 
 AttributeError: can't set attribute
 
 In [7]:
 
```

タプルの各要素に付与する名前を空白文字で区切った文字列で与えていますが、次のように名前をリストで渡すこともできます。内部で


```
 User = namedtuple("User", ["id", "name", "email"])
```

名前をドット表記としてアクセスすることができるようになりますが、これまでのようにインデックス指定もできます。
collections.namedtuple は、タプル要素に名前を付けるための1行が増えるだけなので、通常のタプルを簡単に置き換えることができます。


## クラス継承
collections.namedtuple のインスタンスオブジェクトを継承したクラスを作成するこ>とができます。


```
 In [2]: # %load c13_collection_namedtuple_class.py
    ...: from collections import namedtuple
    ...:
    ...: UserMixin = namedtuple("User", "id name email")
    ...: class  User(UserMixin):
    ...:     def get_profile(self):
    ...:         profile = f"{self.name} <{self.email}"
    ...:         return  profile
    ...:
    ...: user = User(1, "Freddie", "freddie@example.com")
    ...:
    ...: # user
    ...: # user.get_profile
    ...:
    ...:
 
 In [3]: user
 Out[3]: User(id=1, name='Freddie', email='freddie@example.com')
 
 In [4]: user.get_profile()
 Out[4]: 'Freddie <freddie@example.com'
 
 In [5]:
 
```

単純にクラスでデータを保持した場合では、属性は変更することができてしまいます。前述したように、クラス定義時に `property` を使って変更できないようにコードすることもできますが、記述量が増えてしまいます。

collections.namedtuple を使うと簡単に、変更できない属性を持たせることができます。
ただし、collections.namedtuple を継承したクラスで変更できない属性を追加することはできません。

collections.namedtuple で階層化を実現するためには、次のようにコードします。


```
 In [2]: # %load c14_collection_namedtuple_add_attr.py
    ...: from collections import namedtuple
    ...:
    ...: UserMixin = namedtuple("UserMixin", "id name email")
    ...: User = namedtuple( 'User', UserMixin._fields + ('grup',))
    ...: user = User(1, 'Freddie', 'freddie@example.com', 'Queeness')
    ...:
    ...: # user
    ...:
 
 In [3]: user
 Out[3]: User(id=1, name='Freddie', email='freddie@example.com', grup='Queeness')
 
 In [4]:
 
```

### デフォルト値
collections.namedtuple にデフォルト値を設定したいときは、次のように定義します。


```
 In [2]: # %load c15_collection_namedtuple_defaults.py
    ...: from collections import namedtuple
    ...:
    ...: User = namedtuple("User", "id name email",
    ...:                   defaults=[1, "", ""] )
    ...:
    ...: # User = namedtuple("User", "id name email")
    ...: # User.__new__.__defaults__ = (1, "", "")
    ...:
    ...: user = User(name="Freddie", email="freddie@example.com")
    ...:
    ...: # user
    ...:
 
 In [3]: user
 Out[3]: User(id=1, name='Freddie', email='freddie@example.com')
 
 In [4]:
 
```

### ヘルパーメソッド
collections.namedtuple は要素の値を変更することができませんが、 `_replace()` メソッドを呼び出すと、指定した要素を変更したコピーを取得することができます。 `_make()` メソッドでは、namedtuple の新しいインスタンスを生成することができます>。


```
 In [2]: # %load c16_collection_namedtuple_helper.py
    ...: from collections import namedtuple
    ...: import json
    ...:
    ...: User = namedtuple("User", "id name email")
    ...:
    ...: user = User(1, "Freddie", "freddie@example.com")
    ...:
    ...: v1 = user
    ...: v2 = user._replace(id=2)
    ...: v3 = user._make([2, 'Brian', 'brian@example.com'])
    ...:
    ...: v4 = user._asdict()
    ...: v5 = json.dumps(v4)
    ...:
 
 In [3]: v1
 Out[3]: User(id=1, name='Freddie', email='freddie@example.com')
 
 In [4]: v2
 Out[4]: User(id=2, name='Freddie', email='freddie@example.com')
 
 In [5]: v3
 Out[5]: User(id=2, name='Brian', email='brian@example.com')
 
 In [6]: v4
 Out[6]: OrderedDict([('id', 1), ('name', 'Freddie'), ('email', 'freddie@example.com')])
 
 In [7]: v5
 Out[7]: '{"id": 1, "name": "Freddie", "email": "freddie@example.com"}'
 
 In [8]:
 
```

# typing.NamedTuple を使用する方法

Pythonでは関数の戻り値をタプルで返すことができます。


```
 In [2]: # %load c20_func_return_tuple.py
    ...: from collections import namedtuple
    ...:
    ...: User = namedtuple("User", "id name email")
    ...:
    ...: def get_user(*args):
    ...:     # ...
    ...:     id = 1
    ...:     name = "Freddie"
    ...:     email = "freddie@exampl.com"
    ...:
    ...:     return id, name, email
    ...:
    ...: v1 = get_user()
    ...:
 
 In [3]: v1
 Out[3]: (1, 'Freddie', 'freddie@exampl.com')
 
 In [4]:
 
```

この場合、タプルの構造が変わったときなどに、修正箇所を見逃しやすくなってしまいます。
明示的に名前付きタプルを返すようにします。


```
 In [2]: # %load c21_func_return_namedtuple.py
    ...: from collections import namedtuple
    ...:
    ...: User = namedtuple("User", "id name email")
    ...:
    ...: def get_user(*args):
    ...:     # ...
    ...:     id = 1
    ...:     name = "Freddie"
    ...:     email = "freddie@exampl.com"
    ...:
    ...:     return User._make([id, name, email])
    ...:
    ...: v1 = get_user()
    ...:
 
 In [3]: v1
 Out[3]: User(id=1, name='Freddie', email='freddie@exampl.com')
 
 In [4]:
 
```

Python 3.6 から導入された、 typing.NamedTuple は型として名前付きタプルを定義した実装です。
デフォルト値の設定も簡単で、クラス継承するときも理解しやすくなり、collections.namedtuple よりもか可読性がよくなります。


```
 In [2]: # %load c22_typing_namedtuple.py
    ...: from typing import NamedTuple
    ...:
    ...: class User(NamedTuple):
    ...:     id: int = 1
    ...:     name: str = ""
    ...:     email: str = ""
    ...:
    ...: def get_user(*args) -> User:
    ...:     # ...
    ...:     id = 1
    ...:     name = "Freddie"
    ...:     email = "freddie@exampl.com"
    ...:
    ...:     return User(id, name, email)
    ...:
    ...: v1 = get_user()
    ...:
 
 In [3]: v1
 Out[3]: User(id=1, name='Freddie', email='freddie@exampl.com')
 
 In [4]: v1.name
 Out[4]: 'Freddie'
 
 In [5]: v1[1]
 Out[5]: 'Freddie'
 
 In [6]: v1.name = 'Brian'
 ---------------------------------------------------------------------------
 AttributeError                            Traceback (most recent call last)
 <ipython-input-6-8f88fed0cadf> in <module>
 ----> 1 v1.name = 'Brian'
 
 AttributeError: can't set attribute
 
 In [7]:
 
```


# メモリ使用量を比較

pympler ライブラリを使用すると使用しているデータのメモリ占有量を知ることができます。
 bash
```
 $ python -m pip install pympler
```


```
 In [2]: # %load c30_comparison_memory.py
    ...: from pympler import asizeof
    ...: from collections import namedtuple
    ...: from typing import NamedTuple
    ...:
    ...: simple_dict = dict(id=1, name='Freddie', part="Vocal",
    ...:                    email='freddie@example.com')
    ...:
    ...: User1 = namedtuple('User1', "id name part email")
    ...: collection_namedtuple  = User1(id=1, name='Freddie', part="Vocal",
    ...:                               email='freddie@example.com')
    ...:
    ...: class User2(NamedTuple):
    ...:     id: int
    ...:     name: str
    ...:     part: str
    ...:     email: str
    ...:
    ...: typing_namedtuple  = User2(id=1, name='Freddie', part="Vocal",
    ...:                           email='freddie@example.com')
    ...:
     ...: @dataclass
    ...: class User3(object):
    ...:     id: int
    ...:     name: str
    ...:     part: str
    ...:     email: str
    ...:
    ...: @dataclass(frozen=True)
    ...: class User4(object):
    ...:     id: int
    ...:     name: str
    ...:     part: str
    ...:     email: str
    ...:
    ...: dataclass_mutable  = User3(id=1, name='Freddie', part="Vocal",
    ...:                             email='freddie@example.com')
    ...: dataclass_immutable  = User4(id=1, name='Freddie', part="Vocal",
    ...:                             email='freddie@example.com')
    ...:
    ...: comparison_data = {
    ...:     'simple_dict': simple_dict,
    ...:     'collection_namedtuple': collection_namedtuple,
    ...:     'typing_namedtuple': typing_namedtuple,
    ...:     'dataclass_mutable': dataclass_mutable,
    ...:     'dataclass_immutable': dataclass_immutable,
    ...: }
    ...:
    ...: for key, val in comparison_data.items():
    ...:     print(f'{key}: {asizeof.asizeof(val)} bytes')
    ...:
 simple_dict: 688 bytes
 collection_namedtuple: 304 bytes
 typing_namedtuple: 304 bytes
 dataclass_mutable: 624 bytes
 dataclass_immutable: 624 bytes
 
 In [4]:
 
```

名前付きタプルは辞書に比べて56%もメモリ消費が少なくてすみことがわかります。最終的なメモリ消費量は、格納する値の数とその型に依存します。値が違えば、結果も違ってこることに留意してください。

# 操作性能の比較
辞書と名前付きタプル、およびデータクラスの操作について性能を比較してみます。


```
 In [2]: # %load c31_comparison_performance.py
    ...: from time import perf_counter
    ...: from dataclasses import dataclass, astuple
    ...: from collections import namedtuple
    ...: from typing import NamedTuple
    ...:
    ...: def average_time(count, data, func):
    ...:     sampling = []
    ...:     for _ in range(count):
    ...:         start = perf_counter()
    ...:         func(data)
    ...:         end = perf_counter()
    ...:         sampling.append(end - start)
    ...:     result = sum(sampling) / count * int(1e8)
    ...:     return result
    ...:
    ...: def perfcheck_dict(dictionary):
    ...:     _ = "name" in dictionary
    ...:     _ = "missing" in dictionary
    ...:     _ = "Freddie" in dictionary.values()
    ...:     _ = "missing" in dictionary.values()
    ...:     _ = dictionary["name"]
    ...:
    ...: def perfcheck_namedtuple(named_tuple):
    ...:     _ = "name" in named_tuple._fields
    ...:     _ = "missing" in named_tuple._fields
    ...:     _ = "Freddie" in named_tuple
    ...:     _ = "missing" in named_tuple
    ...:     _ = named_tuple.name
    ...:
    ...: def perfcheck_dataclass(data_class):
    ...:     _ = "name" in data_class.__dict__
    ...:     _ = "missing" in data_class.__dict__
    ...:     _ = "Freddie" in data_class.__repr__()
    ...:     _ = "missing" in data_class.__repr__()
    ...:     _ = data_class.name
    ...:
    ...: simple_dict = dict(id=1, name='Freddie', part="Vocal",
    ...:                          email='freddie@example.com')
    ...:
    ...: User1 = namedtuple('User1', "id name part email")
    ...: collection_namedtuple  = User1(id=1, name='Freddie', part="Vocal",
    ...:                                email='freddie@example.com')
    ...:
    ...: class User2(NamedTuple):
    ...:     id: int
    ...:     name: str
    ...:     part: str
    ...:     email: str
    ...:
    ...: typing_namedtuple  = User2(id=1, name='Freddie', part="Vocal",
    ...:                            email='freddie@example.com')
    ...:
    ...: @dataclass
    ...: class User3(object):
    ...:     id: int
    ...:     name: str
    ...:     part: str
    ...:     email: str
    ...:
    ...: @dataclass(frozen=True)
    ...: class User4(object):
    ...:     id: int
    ...:     name: str
    ...:     part: str
    ...:     email: str
    ...:
    ...: dataclass_mutable  = User3(id=1, name='Freddie', part="Vocal",
    ...:                             email='freddie@example.com')
    ...: dataclass_immutable  = User4(id=1, name='Freddie', part="Vocal",
    ...:                             email='freddie@example.com')
    ...:
    ...: def main():
    ...:     test_count = 1_000_000
    ...:     time_of_dict = average_time(test_count,
    ...:                          simple_dict, perfcheck_dict)
    ...:     time_of_col_namedtuple = average_time(test_count,
    ...:                          collection_namedtuple, perfcheck_namedtuple)
    ...:     time_of_typing_namedtuple = average_time(test_count,
    ...:                             typing_namedtuple, perfcheck_namedtuple)
    ...:     time_of_dataclass_mutable = average_time(test_count,
    ...:                             dataclass_mutable, perfcheck_dataclass)
    ...:     time_of_dataclass_immutable = average_time(test_count,
    ...:                             dataclass_immutable, perfcheck_dataclass)
    ...:
    ...:     print(f'                dict: {time_of_dict}')
    ...:     print(f'collection_namedtupe: {time_of_col_namedtuple}')
    ...:     print(f'   typing_namedtuple: {time_of_typing_namedtuple}')
    ...:     print(f'   dataclass mutable: {time_of_dataclass_mutable}')
    ...:     print(f' dataclass immutable: {time_of_dataclass_immutable}')
    ...:
    ...:
 
 In [3]: main()
                 dict: 59.221875999941716
 collection_namedtupe: 47.51290830000716
    typing_namedtuple: 48.999928499920394
    dataclass mutable: 321.6785862999634
  dataclass immutable: 396.0550255002401
 
 In [4]:
 
```

データクラスの操作が一番性能が悪い結果となっています。これは、データクラスはイテラブルオブジェクトではないため、 `value in object` のような操作を直接できないことにも影響しています。このテストでは `__repr__` を呼び出して一旦文字列変換した結果を参照しています。


## おまけ：データベースから読み出す

 sql
```
 CREATE TABLE IF NOT EXISTS "User" (
 "id" INTEGER,
   "name" TEXT,
   "part" TEXT,
   "email" TEXT
 );
 CREATE INDEX "ix_User_id"ON "User" ("id");
 
 INSERT INTO User(id,name,part,email)
        VALUES (1,"Freddie","Vocal","freddie@example.com");
 INSERT INTO User(id,name,part,email)
        VALUES (2,"Brian","Guitar","brian@example.com");
 INSERT INTO User(id,name,part,email)
        VALUES (3,"John","Base","john@example.com");
 INSERT INTO User(id,name,part,email)
        VALUES (4,"Roger","Drums","rogger@example.com");
 INSERT INTO User(id,name,part,email)
        VALUES (5,"Adam","Vocal","adm@example.com");
 INSERT INTO User(id,name,part,email)
        VALUES (6,"David","Guitar","david@example.com");
 INSERT INTO User(id,name,part,email)
        VALUES (7,"Carlos","Guitar","carlos@example.com");
 INSERT INTO User(id,name,part,email)
        VALUES (8,"Paul","Base","paul@example.com");
 INSERT INTO User(id,name,part,email)
        VALUES (9,"Ian","Drums","ian@example.com");
 INSERT INTO User(id,name,part,email)
        VALUES (10,"nick","Base","nick@example.com");
```

 bash
```
 $ sqlite3 user.db
 SQLite version 3.37.0 2021-12-09 01:34:53
 Enter ".help" for usage hints.
 sqlite> .read data.sql
 sqlite> select * from USER;
 1|Freddie|Vocal|freddie@example.com
 2|Brian|Guitar|brian@example.com
 3|John|Base|john@example.com
 4|Roger|Drums|rogger@example.com
 5|Adam|Vocal|adm@example.com
 6|David|Guitar|david@example.com
 7|Carlos|Guitar|carlos@example.com
 8|Paul|Base|paul@example.com
 9|Ian|Drums|ian@example.com
 10|nick|Base|nick@example.com
 sqlite> ^D
 $ 
```


```
 In [2]: # %load c41_read_data_from_sql.py
    ...: from typing import NamedTuple
    ...: import sqlite3 as sqlite
    ...:
    ...: class User(NamedTuple):
    ...:     id: int
    ...:     name: str
    ...:     part: str
    ...:     email: str
    ...:
    ...: conn = sqlite.connect('user.db')
    ...:
    ...: with conn:
    ...:     cur = conn.cursor()
    ...:     cur.execute('SELECT * FROM User')
    ...:
    ...:     for user in map(User._make, cur.fetchall()):
    ...:         print(user)
    ...:
 Out[2]: <sqlite3.Cursor at 0x7fc0c5450110>
 User(id=1, name='Freddie', part='Vocal', email='freddie@example.com')
 User(id=2, name='Brian', part='Guitar', email='brian@example.com')
 User(id=3, name='John', part='Base', email='john@example.com')
 User(id=4, name='Roger', part='Drums', email='rogger@example.com')
 User(id=5, name='Adam', part='Vocal', email='adm@example.com')
 User(id=6, name='David', part='Guitar', email='david@example.com')
 User(id=7, name='Carlos', part='Guitar', email='carlos@example.com')
 User(id=8, name='Paul', part='Base', email='paul@example.com')
 User(id=9, name='Ian', part='Drums', email='ian@example.com')
 User(id=10, name='nick', part='Base', email='nick@example.com')
 
 In [3]:
 
```

# まとめ
データクラスと名前付きタプルを比較すると、次のことがわかりました。

  - 名前付きタプルはデータクラスと比較してメモリ使用効率が良い
  - データクラスは初期化時の値の検証をする仕組みが提供されている
  - 型アノテーションを行う場合は、 typing.NamedTuple の方が良い

どちらも使用することができるのであれば、typing.NamedTuple の採用を検討してみてください。




