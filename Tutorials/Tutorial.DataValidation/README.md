Python クラスの属性をバリデーションしてみよう
=================

## はじめに

動的型付けを行う Python では、通常は、型と値のチェックは柔軟に暗黙的にに処理されます。
Python3からtypingモジュールが導入され、型ヒントの実行時サポートが提供されましたが、値の**検証(バリデーション validation)** については、様々な可能性があるため、統一的な方法がありません。
例えば、属性  `num` 　があるとき、数値としての `20` 、 `20.0` 、文字列としての `"20"` 、 `"20.0"` などが候補ですが、どれが有効なのかはプログラムの設計仕様に依存していて、すべてを有効な値とする場合もあります。 

このチュートリアルでは、ユーザアカウント情報を保持するUserクラスを考えてみましょう。

  - クラス　User
  - 属性：　username、email、 age

この場合、入力が有効であることを確保するようにしてみましょう。

  - usernameは20文字以下であること
  - 年齢は正の整数で、負であってはならない。
  - メールアドレスは正しい形式でなればならない

Python ではクラスの属性について、その値を検証する方法には、主に次のようなものがあります。

  - 方法1: 検証関数を作る
  - 方法2: @property を使用する
  - 方法3: ディスクリプタを使用する
  - 方法4: ディスクリプタをデコレータと組み合わせる
  - 方法5: ディスクリプタを抽象基底クラスと組み合わせる
  - 方法6: dataclasses を使用する
  - 方法7: marshmallow を使用する
  - 方法8: Pydanticを使用する
  - 方法9: Cerberus を使用する

順に説明してゆくことにしましょう。

## 方法1: 検証関数を作る

最も単純な方法は、入力項目に対応する **検証関数(Validation Function)** を作成することです。
次のコードは、クラスの属性 `username` 、 `email` 、  `age` について入力値を個別に検証する3つのメソッドを用意しています。属性は順番に検証され、検証に失敗すると  `ValueError` 例外が発行されます。


```
 In [2]: # %load c01_create_validation_func.py
    ...: import re
    ...:
    ...: class User:
    ...:     def __init__(self, id, username, email, age):
    ...:         self.id = id
    ...:         self.username = self.validate_name(username)
    ...:         self.email = self.validate_email(email)
    ...:         self.age = self.validate_age(age)
    ...:
    ...:     def validate_name(self, val):
    ...:         if len(val) > 20:
    ...:             raise ValueError("Userame must be less than 20 characters.")
    ...:         return val
    ...:
    ...:     def validate_email(self, val):
    ...:         regex = "^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$"
    ...:         if not re.match(regex, val):
    ...:             raise ValueError("Invalid email address.")
    ...:         return val
    ...:
    ...:     def validate_age(self, val):
    ...:         if val < 0:
    ...:             raise ValueError("Age must be positive value.")
    ...:         return val
    ...:
    ...:
 
 In [3]:
```


この方法は、単純ですが Pythonらしいコードではありません。 `__init__()` はシンプルであることが望ましいのです。それに、正常な値を使って初期化をしておき、後から属性に無効な値を例外を発生させずに代入できてしまうことも問題です。


```
 In [4]: # %load test_data.py
    ...: users =  [
    ...:     dict( id=1, username="Jack Johnson",
    ...:           email="jackJohnson@gmail.com", age=52),
    ...:     dict( id='2', username="Eddie Jackson",
    ...:           email="edduiejackson@example.com", age='20'),
    ...:     dict( id=3, username="Goichi (iisaka) Yukawa",
    ...:           email="iisaka51@gmail.", age=-20),
    ...: ]
    ...:
    ...:
 
 In [5]: user = User(**users[0])
 
 In [6]: user.age
 Out[6]: 52
 
 In [7]: user.age = 20
 
 In [8]: user.age = -20
 
 In [9]:
```

## 方法2: @property を使用する
組み込み関数  `property()` を使用します。これは、属性に追加されるデコレーターとして機能します。Pythonの[propertyオブジェクト ](https://docs.python.org/ja/3/library/functions.html#property)は、デコレータとして使用できるメソッド   `getter()` 、 `setter()` 、 `deleter()` があり、 `c` が クラス `C` のインスタンスであるとき、 `c.x` は  `getter()` を呼び出し、 `c.x = value` は  `setter()` を、 `del c.x` は  `deleter()` を呼び出します。


```
 In [2]: # %load c02_using_property.py
    ...: import re
    ...:
    ...: class User:
    ...:     def __init__(self, id, username, email, age):
    ...:         self._id = id
    ...:         self._username = username
    ...:         self._email = email
    ...:         self._age = age
    ...:
    ...:     @property
    ...:     def id(self):
    ...:         return self._id
    ...:
    ...:     @property
    ...:     def username(self):
    ...:         return self._username
    ...:
    ...:     @username.setter
    ...:     def username(self, value):
    ...:         if len(value) > 20:
    ...:             raise ValueError("Userame must be less than 20 characters.")
    ...:         self._name = value
    ...:
    ...:     @property
    ...:     def email(self):
    ...:         return self._email
    ...:
    ...:     @email.setter
    ...:     def email(self, value):
    ...:         regex = "^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$"
    ...:         if not re.match(regex, value):
    ...:             raise ValueError("Invalid email address.")
    ...:         self._email = value
    ...:
    ...:     @property
    ...:     def age(self):
    ...:         return self._age
    ...:
    ...:     @age.setter
    ...:     def age(self, value):
    ...:         if value < 0:
    ...:             raise ValueError("Age musst be postive value.")
    ...:         self._age = value
    ...:
    ...:
 
 In [3]:
```

この方法では、 `id` を除く各属性は2つのメソッドを持っていて、1つは  `@property` で、もう1つは  `setter()` が定義されています。この方法では、 `user.username` のように属性が参照されるたびに、 `@property` を持つメソッドが呼び出されます。初期化時や更新時に属性値が設定されるときは、 `setter()` メソッドが呼び出されます。
方法1のコードと比較すると、検証ロジックは各属性の  `setter()` メソッドで定義するので記述量は増えますが、  `__init__()` はシンプルなります。さらに、この検証は初期化後に各属性が更新されるたびに適用されるようになるため、無効な値を初期化後に設定することはできなくなります。


```
 In [3]: from test_data import users
 
 In [4]: user = User(**users[0])
 
 In [5]: user.age
 Out[5]: 52
 
 In [6]: user.age = 20
 
 In [7]: user.age = -20
 
 ---------------------------------------------------------------------------
 ValueError                                Traceback (most recent call last)
 Input In [7], in <cell line: 1>()
 ----> 1 user.age = -20
 
 Input In [2], in User.age(self, value)
      40 @age.setter
      41 def age(self, value):
      42     if value < 0:
 ---> 43         raise ValueError("Age musst be postive value.")
      44     self._age = value
 
 ValueError: Age musst be postive value.
 
 In [8]:
 
```

属性  `id` は  `setter()` メソッドを持っていないので、初期化後に更新しようとすると、 `AttributeError` の例外が発生します。これは、このid が初期化後に更新できないことを伝える意味に利用することができます。


```
 In [9]: user.id
 Out[9]: 1
 
 In [10]: user.id = 2
 ---------------------------------------------------------------------------
 AttributeError                            Traceback (most recent call last)
 Input In [10], in <cell line: 1>()
 ----> 1 user.id = 2
 
 AttributeError: can't set attribute 'id'
 
 In [11]:
```


## 方法3: ディスクリプタを使用する
Python の [　デスクリプタ(Descriptors) ](https://docs.python.org/ja/3/howto/descriptor.html#descriptor-howto-guide) を利用する方法があります。デスクリプタ は、  `__get__()` ,  `__set__()` ,  `__delete__()` のメソッドが定義されているオブジェクトのことです。これらのメソッドは、属性の取得/設定/削除のデフォルトの動作を変更します。
強力で有益な機能なのですが見落とされがちであったため、Python3.9 で、[属性を検証するためにディスクリプタを使用する例 ](https://docs.python.org/3/howto/descriptor.html#validator-class) がドキュメントに追加されています。

次のコードは、ディスクリプタを使用した例です。すべての属性は、 `__get__()` および  `__set__()` メソッドを持つクラスのディスクリプタとなります。

  -  `self.username=username` のように属性値が設定されると、 `__set__()` が呼び出されます。
  -  `print(self.username)` のように属性を取得する場合は、 `__get__()` が呼び出されます。



```
 In [2]: # %load c03_using_descriptors.py
    ...: import re
    ...:
    ...: class Name:
    ...:     def __get__(self, obj, value=None):
    ...:         return self.value
    ...:
    ...:     def __set__(self, obj, value):
    ...:         if len(value) > 20:
    ...:             raise ValueError("Userame must be less than 20 characters.")
    ...:
    ...:         self.value = value
    ...:
    ...: class Email:
    ...:     def __get__(self, obj, value=None):
    ...:         return self.value
    ...:
    ...:     def __set__(self, obj, value):
    ...:         regex = "^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$"
    ...:         if not re.match(regex, value):
    ...:             raise ValueError("Invalid email address.")
    ...:         self.value = value
    ...:
    ...: class Age:
    ...:     def __get__(self, obj, value=None):
    ...:         return self.value
    ...:
    ...:     def __set__(self, obj, value):
    ...:         if value < 0:
    ...:             raise ValueError("Age must be postive value.")
    ...:         self.value = value
    ...:
    ...: class User:
    ...:
    ...:     name = Name()
    ...:     email = Email()
    ...:     age = Age()
    ...:
    ...:     def __init__(self, id, name, email, age):
    ...:         self.id = id
    ...:         self.name = name
    ...:         self.email = email
    ...:         self.age = age
    ...:
    ...:
 
 In [3]:
 
```

デスクリプタを使う方法は、 `@property` と同等のものになりますが、複数のクラスで記述子を再利用できる場合には、より効果的で利用価値が高くなります。
例えば、従業員情報を保持する Employee のクラスを定義するときなどでは、クラスごとに定型的なコードを作成しなくても、以前のディスクリプタを再利用することができます。



```
 In [2]: # %load c04_reuse_descriptors.py
    ...: from c03_using_descriptors import Name, Email, Age
    ...:
    ...: class Salary:
    ...:     def __get__(self, obj):
    ...:         self.value
    ...:
    ...:     def __set__(self, obj, value):
    ...:         if value < 1000:
    ...:             raise ValueError("Salary must be upper than 1000.")
    ...:         self.value = value
    ...:
    ...: class Employee:
    ...:     name = Name()
    ...:     email = Email()
    ...:     age = Age()
    ...:     salary = Salary()
    ...:
    ...:     def __init__(self, id, name, email, age, salary):
    ...:         self.id = id
    ...:         self.name = name
    ...:         self.email = email
    ...:         self.age = age
    ...:         self.salary = salary
    ...:
    ...: users = [
    ...:     dict(id=1, name="Jack Johnson",
    ...:          email="jackJohnson@example.com",
    ...:          age=40, salary=1000),
    ...:     dict(id=2, name="Eddie Jackson",
    ...:          email="edduiejackson@example.com",
    ...:          age=-20, salary=1000),
    ...:     dict(id=3, name="Goichi longlong name iisaka",
    ...:          email="iisaka51@example.com",
    ...:          age=60, salary=200),
    ...: ]
    ...:
    ...: # person = Employee(**users[0])
    ...: # person = Employee(**users[1])
    ...: # person = Employee(**users[2])
    ...:
 
 In [3]:
 
 In [3]: person = Employee(**users[0])
 
 In [4]: person = Employee(**users[1])
 ---------------------------------------------------------------------------
 ValueError                                Traceback (most recent call last)
 Input In [4], in <cell line: 1>()
 ----> 1 person = Employee(**users[1])
 
 Input In [2], in Employee.__init__(self, id, name, email, age, salary)
      21 self.name = name
      22 self.email = email
 ---> 23 self.age = age
      24 self.salary = salary
 
 File ~/Projects/Python.Osaka/Tutorials/Tutorial.DataValidation/c03_using_descriptors.py:28, in Age.__set__(self, obj, value)
      26 def __set__(self, obj, value):
      27     if value < 0:
 ---> 28         raise ValueError("Age must be postive value.")
      29     self.value = value
 
 ValueError: Age must be postive value.
 
 In [5]:
 
```



## 方法4: ディスクリプタをデコレータと組み合わせる

デコレータとディスクリプタを組み合わせる方法があります。
次に示すように、デスクリプタによって定義された属性の設定/変更/削除のルールは、デコレータにカプセル化されます。


```
 In [2]: # %load c05_using_decrator_with_descriptor.py
    ...: from c03_using_descriptors import Name, Email, Age
    ...:
    ...: def email(attr):
    ...:     def decorator(cls):
    ...:         setattr(cls, attr, Email())
    ...:         return cls
    ...:     return decorator
    ...:
    ...: def age(attr):
    ...:     def decorator(cls):
    ...:         setattr(cls, attr, Age())
    ...:         return cls
    ...:     return decorator
    ...:
    ...: def name(attr):
    ...:     def decorator(cls):
    ...:         setattr(cls, attr, Name())
    ...:         return cls
    ...:     return decorator
    ...:
    ...: @email("email")
    ...: @age("age")
    ...: @name("username")
    ...: class User:
    ...:     def __init__(self, id, username, email, age):
    ...:         self.id = id
    ...:         self.username = username
    ...:         self.email = email
    ...:         self.age = age
    ...:
 
 In [3]:
 
```


これらのデコレータは簡単に拡張することができます。例えば、 `@positive_number(attr1,attr2)` のように複数の属性を扱うような規則を作成することもできます。

ここまでで、組み込み関数を使った4つの方法を説明しました。Python でのデータ検証では組み込み関数だけでの必要十分な機能があるので、ここからは、ライブラリ を使った方法についても説明しましょう。


## 方法5: ディスクリプタを抽象基底クラスと組み合わせる
#### 抽象基底クラス（ABC: Abstract Base Class)


```
 n [2]: # %load c06_using_descriptor_ABCs.py
    ...: from abc import ABC, abstractmethod
    ...: import re
    ...:
    ...: class Validator(ABC):
    ...:
    ...:     def __set_name__(self, owner, name):
    ...:         self.private_name = '_' + name
    ...:
    ...:     def __get__(self, obj, objtype=None):
    ...:         return getattr(obj, self.private_name)
    ...:
    ...:     def __set__(self, obj, value):
    ...:         self.validate(value)
    ...:         setattr(obj, self.private_name, value)
    ...:
    ...:     @abstractmethod
    ...:     def validate(self, value):
    ...:         pass
    ...:
    ...: class Name(Validator):
    ...:     def __init__(self, minsize=8, maxsize=20):
    ...:         self.minsize = minsize
    ...:         self.maxsize = maxsize
    ...:
    ...:     def validate(self, value):
    ...:         if not isinstance(value, str):
    ...:             raise TypeError(f'Expected {value!r} to be an str')
    ...:         if self.minsize is not None and len(value) < self.minsize:
    ...:             raise ValueError(
    ...:                 f'Expected {value!r} to be no smaller than {self.minsize!r}'
    ...:             )
    ...:         if self.maxsize is not None and len(value) > self.maxsize:
    ...:             raise ValueError(
    ...:                 f'Expected {value!r} to be no bigger than {self.maxsize!r}'
    ...:             )
    ...:
    ...: class Email:
    ...:     def validate(self, value):
    ...:         if not isinstance(value, str):
    ...:             raise TypeError(f'Expected {value!r} to be an str')
    ...:         regex = "^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$"
    ...:         if not re.match(regex, value):
    ...:             raise ValueError(f'Expected {value!r} Invalid email address')
    ...:
    ...: class Age(Validator):
    ...:     def validate(self, value):
    ...:         if not isinstance(value, int):
    ...:             raise TypeError(f'Expected {value!r} to be an int')
    ...:         if value < 0:
    ...:             raise ValueError(f'Expected {value!r} to be positive value')
    ...:
    ...:
    ...: class User:
    ...:
    ...:     username = Name(minsize=8, maxsize=20)
    ...:     email = Email()
    ...:     age = Age()
    ...:
    ...:     def __init__(self, id, username, email, age):
    ...:         self.id = id
    ...:         self.username = username
    ...:         self.email = email
    ...:         self.age = age
    ...:
    ...:
 
 In [3]:
 
```

 `Validator` クラスは抽象基底クラス（ABC)を継承したもので、それぞれの属性の記述子を初期化するときに `maxsize` などを指示することができるようになります。単にデスクリプタを使用したときよりもコード量は増えるのですが、コードが読みやすくなります。

## 方法6: dataclasses を使用する

Pythonでデータを保持するクラスを作成する場合、[dataclasses ](https://docs.python.org/ja/3/library/dataclasses.html) モジュールを使うとコードが簡潔に記述することができます。このライブラリは、クラスの  `__init__()` を自動生成するデコレーター `@dataclass` を提供しています。
まずは、 `@dataclass` デコレーター の使い方をみてましょう。


```
 In [2]: # %load c07_using_dataclasses.py
    ...: import re
    ...: from dataclasses import dataclass
    ...: from test_data import users
    ...:
    ...: @dataclass
    ...: class User:
    ...:
    ...:     id: str
    ...:     username: str
    ...:     email: str
    ...:     age: int
    ...:
    ...:
    ...: def parse_user(data):
    ...:     for user in users:
    ...:         user =  User( **user )
    ...:         print(user)
    ...:
    ...: # parse_user(users)
    ...:
 
 In [3]: parse_user(users)
 User(id=1, username='Jack Johnson', email='jackJohnson@gmail.com', age=52)
 User(id='2', username='Eddie Jackson', email='edduiejackson@example.com', age='20')
 User(id=3, username='Goichi (iisaka) Yukawa', email='iisaka51@gmail.', age=-20)
 
 In [4]:
 
```

dataclasses を使用すると、 `__init__()` は自動生成されますが、独自に定義することも出来ます。
この婆は、タイプヒントがあるクラス変数がフィールドと認識される条件になります。オーバーライドした `__init__()` ではフィールドとなる変数をもれなく設定する必要があります。また、個別に追加したクラス変数は、フィールドとして認識されないことに留意してください。


```
 In [2]: # %load c07_using_dataclasses_with_override.py
    ...: import re
    ...: from dataclasses import dataclass
    ...: from test_data import users
    ...:
    ...: @dataclass
    ...: class User:
    ...:
    ...:     id: str
    ...:     username: str
    ...:     email: str
    ...:     age: int
    ...:
    ...:     def __init__(self, id, username, email, age, enable=True):
    ...:         self.id = id
    ...:         self.username = username
    ...:         self.email = email
    ...:         self.age = age
    ...:         self.enable = enable    # フィールドとして扱われない
    ...:
    ...:
    ...: def parse_user(data):
    ...:     for user in users:
    ...:         user =  User( **user )
    ...:         print(user)
    ...:
    ...: # parse_user(users)
    ...:
 
 In [3]: parse_user(users)
 User(id=1, username='Jack Johnson', email='jackJohnson@gmail.com', age=52)
 User(id='2', username='Eddie Jackson', email='edduiejackson@example.com', age='20')
 User(id=3, username='Goichi (iisaka) Yukawa', email='iisaka51@gmail.', age=-20)
 
 In [4]:
 
```

 `@dataclass` でデコレートしたクラスはデータ保持のためのクラスであることが明確になります。また簡単に定義することができるだけでなく、 `__repr__()` が呼ばれると属性の識別子（つまり属性に使用している名前）もされるため、非常に便利です。

ただし、注意する必要があるのは、クラス定義でタイプヒントで型を指定しても実際には与えたデータをそのまま受け入れてしまうことです。この例では、2番目のデータ( `username` が:Eddie) で  `age` に文字列の `"20"` を渡していますが、エラーにはなりません。
こうしたときのために、 `@dataclass` は  `__post_init__()` という特殊メソッドが定義されていると、隠された  `__init__()` から呼び出されるようになっています。 `__post_init__()` は、他のフィールドに基づいてフィールドを初期化したり、検証ルールを定義するために使用できます。


```
 In [2]: # %load c07_using_dataclasses_with_validate.py
    ...: import re
    ...: from dataclasses import dataclass
    ...: from test_data import users
    ...:
    ...: @dataclass
    ...: class User:
    ...:
    ...:     id: str
    ...:     username: str
    ...:     email: str
    ...:     age: int
    ...:
    ...:     def __post_init__(self):
    ...:         if not isinstance(self.age, int):
    ...:             raise TypeError(f'Age must be "int"')
    ...:         if self.age < 0:
    ...:             raise ValueError("Age must be postive value.")
    ...:         regex = "^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$"
    ...:         if not isinstance(self.email, str):
    ...:             raise TypeError(f'Email must be "str"')
    ...:         if not re.match(regex, self.email):
    ...:             raise ValueError("Invalid email address.")
    ...:         if not isinstance(self.username, str):
    ...:             raise TypeError(f'Username must be "str"')
    ...:         if len(self.username) > 20:
    ...:             raise ValueError("Username must be less than 20 characters.")
    ...:
    ...:
    ...: def parse_user(data):
    ...:     for user in users:
    ...:         user =  User( **user )
    ...:         print(user)
    ...:
    ...: # parse_user(users)
    ...:
 
 In [3]: parse_user(users)
 User(id=1, username='Jack Johnson', email='jackJohnson@gmail.com', age=52)
 ---------------------------------------------------------------------------
 TypeError                                 Traceback (most recent call last)
 Input In [3], in <cell line: 1>()
 ----> 1 parse_user(users)
 
 Input In [2], in parse_user(data)
      30 def parse_user(data):
      31     for user in users:
 ---> 32         user =  User( **user )
      33         print(user)
 
 File <string>:7, in __init__(self, id, username, email, age)
 
 Input In [2], in User.__post_init__(self)
      14 def __post_init__(self):
      15     if not isinstance(self.age, int):
 ---> 16         raise TypeError(f'Age must be "int"')
      17     if self.age < 0:
      18         raise ValueError("Age must be postive value.")
 
 TypeError: Age must be "int"
 
 In [4]:
 
```

 `@dataclass ` でクラスをデコレートするこの方法は、方法1と同じ効果を提供します。従来のようにクラスを定義する方法1よりも、とてもシンプルになっています。ただし、デフォルトでは初期化後に無効な値を属性に設定できてしまうことには注意が必要です。


```
 In [11]: user = User(1, "Jack Johnson", "jackJohnson@gmail.com", 40)
 
 In [12]: user.age
 Out[12]: 40
 
 In [13]: user.age = -20
 
 In [14]:
```

 `@dataclass(frozen=True)` とすると、フィールドとして把握されている属性を初期化後に変更すると例外を発生するようになりますが、クラス全体に対しての設定になるため、個別の属性で変更の許可を制御するようなことはできません。


## 方法7: marshmallow を使用する

サードパーティの [Marshmallow ](https://pypi.org/project/marshmallow/) ライブラリは、複雑なデータ型を Python ネイティブのデータ型に変換し、オブジェクトシリアライゼーションを行うためのものです。オブジェクトのシリアライズと検証の方法を理解するために、ユーザーは各属性の検証ルールを定義するスキーマを作成する必要があります。

この marshmallow では  `Length` 、 `Date` 、 `Range` 、 `Email` など、あらかじめ用意されている多くのバリデータを提供しているため、開発者が自分でバリデータを作成する時間を大幅に削減することができるだけでなく、品質の担保への負担も少なくなります。
また、バリデータは独自に作成することも可能です。

これまで紹介してきた方法では、エラーを見つけるとすぐに例外を発行していましたが、Marshmallow の  `ValidationError` は、失敗したバリデーションをすべて含んでます。つまり、開発者は捕獲した例外ですべてのエラーをまとめて処理することができます。


```
 In [2]: # %load c08_using_mashmallow.py
    ...: from marshmallow import Schema, fields, validate, ValidationError
    ...: from dataclasses import dataclass, asdict
    ...: from test_data import users
    ...:
    ...: class UserSchema(Schema):
    ...:     id = fields.Integer(validate=validate.Range(min=1))
    ...:     username = fields.Str(validate=validate.Length(max=20))
    ...:     email = fields.Email()
    ...:     age = fields.Integer(validate=validate.Range(min=1))
    ...:
    ...: @dataclass
    ...: class User:
    ...:     id: int
    ...:     username: str
    ...:     email: str
    ...:     age: int
    ...:
    ...:
    ...: user = User(**users[0])
    ...: data = UserSchema().load(asdict(user))
    ...:
    ...: user.username = "Goichi (iisaka) Yukawa"
    ...: user.age = -20
    ...: try:
    ...:     data = UserSchema().load(asdict(user))
    ...: except ValidationError as e:
    ...:     print(e)
    ...:
 {'age': ['Must be greater than or equal to 1.'], 'username': ['Longer than maximum length 20.']}
 
 In [3]:
```

marshmallow では、定義したスキームにデータを読み込ませたときに検証が行われます。このデータはJSONオブジェクトに変換する必要があることに注意してださい。この例の場合は、 `asdict()` を使っています。

せっかく dataclass を使用しているので、スキーマーとの検証を  `__post_init__()` で定義してみましょう。


```
 In [2]: # %load c08_using_mashmallow_with_dataclasses.py
    ...: from marshmallow import Schema, fields, validate, ValidationError
    ...: from dataclasses import dataclass, asdict
    ...: from test_data import users
    ...:
    ...: class UserSchema(Schema):
    ...:     id = fields.Integer(validate=validate.Range(min=1))
    ...:     username = fields.Str(validate=validate.Length(max=20))
    ...:     email = fields.Email()
    ...:     age = fields.Integer(validate=validate.Range(min=1))
    ...:
    ...: _validator = UserSchema()
    ...: @dataclass
    ...: class User:
    ...:     id: int
    ...:     username: str
    ...:     email: str
    ...:     age: int
    ...:
    ...:     def __post_init__(self):
    ...:         _validator.load(self.__dict__)
    ...:
    ...:
    ...: def parse_user(data):
    ...:     for user in users:
    ...:         try:
    ...:             user =  User( **user )
    ...:             print(f'OK: {user}')
    ...:         except ValidationError as e:
    ...:             print(f'NG: {user}')
    ...:             print(e)
    ...:
    ...: # parse_user(users)
    ...:
 
 In [3]: parse_user(users)
 OK: User(id=1, username='Jack Johnson', email='jackJohnson@gmail.com', age=52)
 OK: User(id='2', username='Eddie Jackson', email='edduiejackson@example.com', age='20')
 NG: {'id': 3, 'username': 'Goichi (iisaka) Yukawa', 'email': 'iisaka51@gmail.', 'age': -20}
 {'email': ['Not a valid email address.'], 'age': ['Must be greater than or equal to 1.'], 'username': ['Longer than maximum length 20.']}
 
 In [4]:
 
```



mashmallow に限った話ではありませんが、Pythonでスキーマを使う場合、データを表すクラスとそのスキーマを表すクラスの両方を持つことになります。これは、重複したコードの同期が取れなくなる可能性がでてきます。
[mashmallow_dataclass https://pypi.org/project/marshmallow-dataclass/]　や [desert ](https://pypi.org/project/desert/) を利用すると、クラス定義からスキーマを生成することができるため、この問題を回避することができます。


```
 n [2]: # %load c08_using_mashmallow_dataclasses.py
    ...: from marshmallow import Schema, validate, ValidationError
    ...: from marshmallow import fields as mfields
    ...: from marshmallow_dataclass import dataclass, class_schema
    ...: from dataclasses import field, asdict
    ...: from marshmallow import Schema
    ...: from typing import ClassVar, Type
    ...: from test_data import users
    ...:
    ...: @dataclass
    ...: class User:
    ...:     id: int = field(metadata = { "validate": validate.Range(min=1) })
    ...:     username: str  = field(metadata = { "validate":  validate.Length(max=20) })
    ...:     email: str  = field(metadata = { "validate":  validate.Email() })
    ...:     age: int  = field(metadata = { "validate": validate.Range(min=1) })
    ...:     Schema: ClassVar[Type[Schema]] = Schema
    ...:
    ...: def parse_user(data):
    ...:     for user in users:
    ...:         user =  User( **user )
    ...:         try:
    ...:             class_schema(User)().load(asdict(user))
    ...:             print(f'OK: {user}')
    ...:         except ValidationError as e:
    ...:             print(f'NG: {user}')
    ...:             print(e)
    ...:
    ...: # parse_user(users)
    ...:
 
 In [3]: parse_user(users)
 OK: User(id=1, username='Jack Johnson', email='jackJohnson@gmail.com', age=52)
 OK: User(id='2', username='Eddie Jackson', email='edduiejackson@example.com', age='20')
 NG: User(id=3, username='Goichi (iisaka) Yukawa', email='iisaka51@gmail.', age=-20)
 {'age': ['Must be greater than or equal to 1.'], 'email': ['Not a valid email address.'], 'username': ['Longer than maximum length 20.']}
 
 In [4]:
 
```



## 方法8: Pydanticを使用する
[Pydantic ](https://pypi.org/project/pydantic/) はMarshmallowと同様にオブジェクトのスキーマやモデルを作成するためのものです。pydantic でも `PositiveInt` や `EmailStr` などの、あらかじめ用意されている多くの検証関数を提供されています。Marshmallow では、検証ルールをスキーマクラスと別に作成することになりますが、pydantic では、クラス定義に統合することができます。



```
 In [2]: # %load c09_using_pydantic.py
    ...: from pydantic import (
    ...:         BaseModel, ValidationError, validator, PositiveInt, EmailStr
    ...:     )
    ...: from test_data import users
    ...:
    ...: class User(BaseModel):
    ...:     id: int
    ...:     username: str
    ...:     email: EmailStr
    ...:     age: PositiveInt
    ...:
    ...:
    ...: def parse_user(data):
    ...:     for user in users:
    ...:         try:
    ...:             user =  User( **user )
    ...:             print(f'OK: {user}')
    ...:         except ValidationError as e:
    ...:             print(f'NG: {user}')
    ...:             print(e)
    ...:
    ...: # parse_user(users)
    ...:
 
 In [3]: parse_user(users)
 OK: id=1 username='Jack Johnson' email='jackJohnson@gmail.com' age=52
 OK: id=2 username='Eddie Jackson' email='edduiejackson@example.com' age=20
 NG: {'id': 3, 'username': 'Goichi (iisaka) Yukawa', 'email': 'iisaka51@gmail.', 'age': -20}
 2 validation errors for User
 email
   value is not a valid email address (type=value_error.email)
 age
   ensure this value is greater than 0 (type=value_error.number.not_gt; limit_value=0)
 
 In [4]:
 
 
```



次コードでは、独自のバリデータを追加するときの例として `User` クラスに `birthday` の属性を追加しています。


```
 In [2]: # %load c09_using_pydantic_with_customvaldate.py
    ...: from datetime import datetime
    ...: from pydantic import (
    ...:         BaseModel, ValidationError, validator, PositiveInt, EmailStr
    ...:     )
    ...: from test_data import users
    ...:
    ...: class User(BaseModel):
    ...:     id: int
    ...:     username: str
    ...:     birthday: str
    ...:     email: EmailStr
    ...:     age: PositiveInt
    ...:
    ...:     @validator('birthday')
    ...:     def valid_date(cls, v):
    ...:         try:
    ...:             datetime.strptime(v, "%Y-%m-%d")
    ...:             return v
    ...:         except ValueError:
    ...:             raise ValueError("date must be in YYYY-MM-DD format.")
    ...:
    ...:
    ...: birthday_list = [
    ...:   { 'birthday': '1994-07-21' },
    ...:   { 'birthday': '1962-01-13' },
    ...:   { 'birthday': '1970-07-22' },
    ...: ]
    ...:
    ...: def parse_user(data):
    ...:     for num, user in enumerate(users):
    ...:         try:
    ...:             # user |= birthday_list[num]       # for Python 3.9 or later
    ...:             user.update(birthday_list[num])
    ...:             user =  User( **user )
    ...:             print(f'OK: {user}')
    ...:         except ValidationError as e:
    ...:             print(f'NG: {user}')
    ...:             print(e)
    ...:
    ...: # parse_user(users)
    ...:
 
 In [3]: parse_user(users)
 OK: id=1 username='Jack Johnson' birthday='1994-07-21' email='jackJohnson@gmail.com' age=52
 OK: id=2 username='Eddie Jackson' birthday='1962-01-13' email='edduiejackson@example.com' age=20
 NG: {'id': 3, 'username': 'Goichi (iisaka) Yukawa', 'email': 'iisaka51@gmail.', 'age': -20, 'birthday': '1970-07-22'}
 2 validation errors for User
 email
   value is not a valid email address (type=value_error.email)
 age
   ensure this value is greater than 0 (type=value_error.number.not_gt; limit_value=0)
 
 In [4]:
 
```


pydantic が便利な機能のひとつに dataclass でタイプヒントで指定した型に変換してくれることがあります。


```
 In [2]: # %load c09_using_pydantic_with_dataclass.py
    ...: from datetime import datetime, date
    ...: from pydantic import (
    ...:         BaseModel, ValidationError, validator, PositiveInt, EmailStr
    ...:     )
    ...: from pydantic.dataclasses import dataclass
    ...: from test_data import users
    ...:
    ...: @dataclass
    ...: class User:
    ...:     id: int
    ...:     username: str
    ...:     birthday: date
    ...:     email: EmailStr
    ...:     age: PositiveInt
    ...:
    ...:
    ...: birthday_list = [
    ...:   { 'birthday': '1994-07-21' },
    ...:   { 'birthday': '1962-01-13' },
    ...:   { 'birthday': '1970-17-22' },
    ...: ]
    ...:
    ...: def parse_user(data):
    ...:     for num, user in enumerate(users):
    ...:         try:
    ...:             # user |= birthday_list[num]       # for Python 3.9 or later
    ...:             user.update(birthday_list[num])
    ...:             user =  User( **user )
    ...:             print(f'OK: {user}')
    ...:         except ValidationError as e:
    ...:             print(f'NG: {user}')
    ...:             print(e)
    ...:
    ...: # parse_user(users)
    ...:
 
 In [3]: parse_user(users)
 OK: User(id=1, username='Jack Johnson', birthday=datetime.date(1994, 7, 21), email='jackJohnson@gmail.com', age=52)
 OK: User(id=2, username='Eddie Jackson', birthday=datetime.date(1962, 1, 13), email='edduiejackson@example.com', age=20)
 NG: {'id': 3, 'username': 'Goichi (iisaka) Yukawa', 'email': 'iisaka51@gmail.', 'age': -20, 'birthday': '1970-17-22'}
 3 validation errors for User
 birthday
   invalid date format (type=value_error.date)
 email
   value is not a valid email address (type=value_error.email)
 age
   ensure this value is greater than 0 (type=value_error.number.not_gt; limit_value=0)
 
 In [4]:
 
```


この例では、2番目のデータ（ `username` がEddie)で `id` と `age` に文字列を与えています。検証としてはエラーになりそうですが、このときデータはdataclassで指定しているタイプヒントにしたがって型変換されます。

pydantic ではスキーマーをJSON形式で出力することができます。


```
 In [10]: print(User.schema_json(indent=2))
 {
   "title": "User",
   "type": "object",
   "properties": {
     "id": {
       "title": "Id",
       "type": "integer"
     },
     "username": {
       "title": "Username",
       "type": "string"
     },
     "birthday": {
       "title": "Birthday",
       "type": "string"
     },
     "email": {
       "title": "Email",
       "type": "string",
       "format": "email"
     },
     "age": {
       "title": "Age",
       "exclusiveMinimum": 0,
       "type": "integer"
     }
   },
   "required": [
     "id",
     "username",
     "birthday",
     "email",
     "age"
   ]
 }
 
 In [11]:
 
```

このスキーマーは [JSON Schema Core https://json-schema.org/latest/json-schema-core.html] や [JSON Schema Validation https://json-schema.org/latest/json-schema-validation.html] 、および [OpenAPI ](https://github.com/OAI/OpenAPI-Specification) に準拠したものになっています。

pydantic では構成ファイルのデータを保持する用途でも使えます。

 c010_config.py
```
 import pydantic
 from typing import Optional, Union, List
 
 class BaseSettings(pydantic.BaseSettings):
     class Config:
         env_prefix = ''
         use_enum_values = True
 
 class MAILSettings(BaseSettings):
     MAIL_SERVER: str = 'smtp.gmail.com'
     MAIL_PORT: int = 587
     MAIL_USE_TLS: bool = True
     MAIL_USE_SSL: bool = False
     MAIL_USERNAME: Optional[str] = None
     MAIL_PASSWORD: Optional[str] = None
     MAIL_DEFAULT_SENDER: Optional[str] = 'YOU_MAIL_ADDRESS_HERE'
     # for debug
     MAIL_DEBUG: bool = False
     MAIL_SUPPRESS_SEND: bool = False
```

このような構成ファイルをアプリケーションで定義しておくと、クラス `MAILSettings` でクラス変数として定義したものがタイプ’ヒントで指示した型に変換されるため、利用がしやすくなります。また、属性値（例： `MAIL_USERNAME` ) と同じ環境変数が定義されていると実行時に読み込んでくれます。
"[設定ファイルを考えてみよう]" にも解説しているので参照してださい。


## 方法9: Cerberus を使用する
Cerberusは、Pythonで実装されたの軽量で拡張性のあるデータ検証ライブラリです。Cerberusは、パワフルでありながらシンプルで軽量なデータ検証機能を提供しています。また、カスタム検証を可能にする拡張性の高い設計になっているため、独自のルールのロジックを実装するコードはほとんど必要ないかもしれません。

まず、cerberus でのスキーマーの定義のしかたをみてみましょう。


```
 In [2]: # %load c11_using_cerberus.py
    ...: from cerberus import Validator, DocumentError
    ...: from datetime import datetime
    ...:
    ...: v = Validator()
    ...: to_date = lambda s: datetime.strptime(s, '%Y-%m-%d')
    ...: v.schema = {
    ...:     'id': {'type': 'integer', 'min': 1 },
    ...:     'username': {
    ...:         'type': 'string',
    ...:         'minlength': 8, 'maxlength': 20 },
    ...:     'email': {
    ...:         'type': 'string',
    ...:         'regex': "^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$" },
    ...:     'birthday': {'type': 'date', 'coerce': to_date },
    ...:     'age': {'type': 'integer', 'min': 0},
    ...:     }
    ...:
    ...:
    ...: user1 =  dict( id=1, username="Jack Johnson",
    ...:               email="jackJohnson@gmail.com",
    ...:               birthday='1970-07-20', age=52  )
    ...: user2 =  dict( id=2, username="Goichi (iisaka) Yukawa",
    ...:                email="iisaka51@gmail.",
    ...:                birthday='1962-01-13', age=-20 )
    ...:
    ...: try:
    ...:     c = (v.validate(user1), v.errors)
    ...:     print(c)
    ...:     c = (v.validate(user2), v.errors)
    ...:     print(c)
    ...: except DocumentError as e:
    ...:     print(e)
    ...:
 (True, {})
 (False, {'age': ['min value is 0'], 'email': ["value does not match regex '^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\\.)+[a-zA-Z]{2,}$'"], 'username': ['max length is 20']})
 
 In [3]:
 
```

 `Validator` クラスのインスタンスオブジェクト `v` にある属性値  `.schema` にスキーマーを登録しまう。検証する場合は、データを辞書で渡すことで、スキーマーでの検証結果が真偽値で返されます。検証エラーがあるときは、 `.errors` に格納されます。
データーがスキーマーにマッピングでない場合には  `DocumentError` が発生します。

cerberus は mashmallows と同じように、定義したスキーマーにマッピングさせて検証を行い、データの保持については別の仕組みに委ねています。そこで、dataclasses と組み合わせてみましょう。


```
 In [2]: # %load c12_using_cerbrus_with_dataclass.py
    ...: from cerberus import Validator, DocumentError
    ...: from datetime import datetime
    ...: from dataclasses import dataclass
    ...: from pydantic import (
    ...:         BaseModel, ValidationError, validator, PositiveInt, EmailStr
    ...:     )
    ...:
    ...: class ValidateError(BaseException):
    ...:     pass
    ...:
    ...: to_date = lambda s: datetime.strptime(s, '%Y-%m-%d')
    ...: schema_user = {
    ...:     'id': {'type': 'integer', 'min': 1 },
    ...:     'username': {
    ...:         'type': 'string',
    ...:         'minlength': 8, 'maxlength': 20 },
    ...:     'email': {
    ...:         'type': 'string',
    ...:         'regex': "^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$" },
    ...:     'birthday': {'type': 'date', 'coerce': to_date },
    ...:     'age': {'type': 'integer', 'min': 0},
    ...:     }
    ...:
    ...: @dataclass
    ...: class User:
    ...:     id: int
    ...:     username: str
    ...:     birthday: str
    ...:     email: str
    ...:     age: int
    ...:
    ...:     def __post_init__(self):
    ...:         if not v.validate(self.__dict__):
    ...:             raise ValidateError(v.errors)
    ...:
    ...: class UserValidator(Validator):
    ...:     def validate_user(self, obj):
    ...:         return self.validate(obj.__dict__)
    ...:
    ...: v = UserValidator(schema_user)
    ...:
    ...:
    ...: users = [
    ...:      User( id=1, username="Jack Johnson",
    ...:                email="jackJohnson@gmail.com",
    ...:                birthday='1970-07-20', age=52  ),
    ...:      User( id=2, username="Goichi Iisaka",
    ...:                email="jackJohnson@gmail.com",
    ...:                birthday='1962-01-13', age=60 ),
    ...: ]
    ...:
    ...: users[1].email = "jackJohnson@gmail."
    ...: users[1].age = -20
    ...:
    ...: for user in users:
    ...:     if v.validate_user(user):
    ...:         print(user)
    ...:     else:
    ...:         print('invalid data')
    ...:         print(v.errors)
    ...:
 User(id=1, username='Jack Johnson', birthday='1970-07-20', email='jackJohnson@gmail.com', age=52)
 invalid data
 {'age': ['min value is 0'], 'email': ["value does not match regex '^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\\.)+[a-zA-Z]{2,}$'"]}
 
 In [3]:
 
```

cerberus では  property のように属性値を変更したタイミングでは検証を行うことができません。しかし、コードはずっと読みやすくなっています。
それとこれは重要なことなのですが、cerberus や mashmallow は与えたデータに対して検証を行うので、property やデスクリプタと違って外部ファイルとして定義されているデータを簡単に検証を行うことができます。


## まとめ
組み込み関数 property や デスクリプタを使用すると、開発者はデータ検証を細かくコントロールすることができますが、バリデータの開発や保守の工数が増えること想定するべきです。
これに対してライブラリを利用してデータ検証を定義すると、開発者は汎用的の定義済みのバリデータを利用できるため、コードを簡潔に記述でき、開発工数を大幅に削減することができるようになりますk。しかし、ライブラリが提供しているバリデータについての知識と、それが要求を満たしているかを検討する必要であります。


## 参考
- Python 公式ドキュメント
  - [propertyオブジェクト ](https://docs.python.org/ja/3/library/functions.html#property)
  - [デスクリプタ(Descriptors) ](https://docs.python.org/ja/3/howto/descriptor.html#descriptor-howto-guide) 
  - [属性を検証するためにディスクリプタを使用する例 ](https://docs.python.org/3/howto/descriptor.html#validator-class) 
  - [dataclasses モジュール ](https://docs.python.org/ja/3/library/dataclasses.html)
  - [PEP 557 - Dataclasses ](https://peps.python.org/pep-0557/)
- marshmallow
  - [PyPI - Marshmallow ](https://pypi.org/project/marshmallow/) 
  - [ソースコード ](https://github.com/marshmallow-code/marshmallow)
  - [公式ドキュメント ](https://marshmallow.readthedocs.io/en/stable/)
- mashmallow-dataclass
  - [PyPI - mashmallow-dataclass ](https://pypi.org/project/marshmallow-dataclass/)
- desert
  - [PyPI - desert ](https://pypi.org/project/desert/)
- pydantic
  - [PyPI - pydantic ](https://pypi.org/project/pydantic/)
  - [ソースコード ](https://github.com/samuelcolvin/pydantic)
  - [公式ドキュメント ](https://pydantic-docs.helpmanual.io/)
- cerberus
  - [PyPI - cerberus ](https://pypi.org/project/Cerberus/)
  - [ソースコード ](https://github.com/pyeve/cerberus)
  - [公式ドキュメント ](https://docs.python-cerberus.org/en/stable/)
- Python.Osaka
  - [設定ファイルを考えてみよう]
  - [データ検証ライブラリCerberusを使ってみよう]


