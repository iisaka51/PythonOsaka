Pythonのダンダー(Dunder)
=================

### ダンダー(Dunder)
Python には ダンダー(Dunder: Double underscore)と呼ばれる、２つのアンダースコア（ `__` )で始まる関数や属性があります 。これらは状況を把握するときの助けとなるため、コンテキストデバッグやロギングでよく利用されます。

-  `__str__()` ：クラスを読みやすい文字列で返す。 `print()` 、 `str()` 、 `format()` などの組み込み関数から呼ばれるメソッド。クラスに `__str__()` がなければ `__repr__()` を呼び出します。
-  `__repr__()` ：クラスを名各区に定義する文字列を返す。組み込み関数 `repr()` からも呼ばれ、 `__str__()` とよく似ていますが、原則的には、返す文字列を `eval()` で処理するともとのクラスのオブジェクトになるようにします。
-  `__format__()` ：整形された文字列を返す。 `__format__()` には `format` 引数を受け付けるようにし、クラスを整形した文字列で返します。引数を省略すると `__str__()` と返すようにします。
-  `__sq__()` ：演算子　 `==` でクラスを評価したときに呼び出されます。定義しておくとテストのときに便利です。
- __ne__()：演算子  `!=` でクラスを評価したときに呼び出されまっす。定義しておくとテストのときに便利です。
-  `__name__` ：モジュール名、REPLで実行したスクリプトでは `__main__` に設定される
-  `__doc__` ：docstrings と呼ばれるドキュメント。定義されていなければ  `None` になる。
-  `__file__` ：通常はモジュールがファイルから読み込まれた場合は、読み込まれたファイルのパス名が設定される。


 models.py
```
 class User:
     def __init__(self, first_name, last_name):
         self.first_name = first_name
         self.last_name = last_name
 
     def __repr__(self):
         return (f"User(first_name='{self.first_name}',"
                 f"last_name='{self.last_name}')")
 
     def __str__(self):
         return f"User: {self.first_name} {self.last_name}."
 
     def __bytes__(self):
         return bytes(str(self), 'utf-8')
 
     def __format__(self, format=None):
         if format == None:
             return str(self)
         else:
             return f'{format} is {str(self)}'
     def __eq__(self, other):
         if not isinstance(other, User):
             return NotImplemented
         return self.first_name == other.first_name and \
                self.last_name == other.last_name
     def __ne__(self, other):
         if not isinstance(other, User):
             return NotImplemented
         return self.first_name != other.first_name and \
                self.last_name != other.last_name
 
     def debug(self):
         print(f'Filename: {__file__}')
         print(f'FirstName: {self.first_name}')
         print(f'LastName: {self.last_name}')
         
```



```
 In [2]: # %load 01_dunder.py
    ...: from models import User
    ...:
    ...: if __name__ == '__main__':
    ...:     user = User(first_name='David', last_name='Coverdale')
    ...:     print(user)
    ...:     print(user.__format__('this'))
    ...:     user_bytes = user.__bytes__()
    ...:     print(user_bytes)
    ...:     user_repr = repr(user)
    ...:     print(user_repr)
    ...:     user2 = eval(user_repr)
    ...:     assert user == user2
    ...:     user.debug()
    ...:     print(user.debug.__module__)
    ...:
 User: David Coverdale.
 this is User: David Coverdale.
 b'User: David Coverdale.'
 User(first_name='David',last_name='Coverdale')
 Filename: /Users/goichiiisaka/Projects/Python.Osaka/Tutorial.Debuging/02_Dunder/models.py
 FirstName: David
 LastName: Coverdale
 models
 
 In [3]:
 
```

Python のドキュメントには、すべての[ダンダー ](https://docs.python.org/ja/3/reference/datamodel.html)  について説明されています。


