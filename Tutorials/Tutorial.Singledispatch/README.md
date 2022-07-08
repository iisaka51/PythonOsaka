singledispatchを使ってみよう
=================
# はじめに
この資料は、Python 3.4 to Python 2.6-3.3で導入された [singledispatch ](https://docs.python.org/ja/3/library/functools.html?highlight=singledispatch#functools.singledispatch) にういて紹介するものです。

# singledispatch について
sindledispatch は、簡単に説明すると関数の引数のタイプによって処理を分岐させることができるデコレーターです。

singledispatch を使うとどれだけ便利になるかを説明するために、はじめに次のような単純に `isinstance()` で型チェックを行うロジックを組み込んだ関数から見てみましょう。


```
 In [2]: # %load c01_simple_dispatch.py
    ...: from typing import Any, List
    ...:
    ...: def func(arg: Any) -> str:
    ...:     if isinstance(arg, int):
    ...:         return 'int'
    ...:     elif isinstance(arg, list):
    ...:         return 'list'
    ...:     else:
    ...:         return 'default'
    ...:
    ...: assert func(1) == 'int'
    ...: assert func([]) == 'list'
    ...: assert func('str') == 'default'
    ...:
 
 In [3]:
```

この `func()` は与えた引数が  `int` のときは、 `"int"` の文字列を、 `list` の時は、 `"list"` の文字列を、それ以外は `"default` の文字列を返します。

Python 3.10 からはパターンマッチ構文が使用できるようになったので、こちらでも記述してみましょう。


```
 In [2]: # %load c02_using_pattern_match.py
    ...: from typing import Any, List
    ...:
    ...: # Python 3.10
    ...:
    ...: def fun(arg: Any) -> str:
    ...:     match arg:
    ...:         case int():
    ...:             return 'int'
    ...:         case list():
    ...:             return 'list'
    ...:         case _:
    ...:             return 'default'
    ...:
    ...: assert fun(1) == 'int'
    ...: assert fun([]) == 'list'
    ...: assert fun('str') == 'default'
    ...:
 
 In [3]:
 
```

こうした、記述がよくない点は、分岐させる型が増えてきたときに可読性が悪くなっていきます。たまたまこのコードは分岐が3つしかなかっただけのことです。また、型を追加することで、関数  `func()` に対して修正がかかるため、都度全ての型をテストをする必要が出てきます。

このコードを singledispatch を使って書き直してみます。

python
```
 In [2]: # %load c03_using_sinpledispatch.py
    ...: from functools import singledispatch
    ...: from typing import Any, List
    ...:
    ...: @singledispatch
    ...: def func(arg: Any) -> str:
    ...:     return 'default'
    ...:
    ...: @func.register(int)
    ...: def func_int(arg: int) -> str:
    ...:         return 'int'
    ...:
    ...: @func.register(list)
    ...: def func_int(arg: List) -> str:
    ...:         return 'list'
    ...:
    ...: assert func(1) == 'int'
    ...: assert func([]) == 'list'
    ...: assert func('str') == 'default'
    ...:
 
 In [3]:
 
```

スッキリとしていませんか？何より関数が独立しているため、型を追加したときも既存のコードへのバグ混入は大幅に低減します。

# 注意点
## Typingの型表記は指定できない

 `resiter()` に与える型として typing モジュールの型表記を指定するとエラーになってしまいます。
 `TypeError: Invalid first argument to ` register()`: typing.List. Use either  `@register(some_class)` or plain  `@register` on an annotated function.`]


## クラスのメソッドにはそのままでは使用できない

python
```
 In [2]: # %load c04_singledispatch_with_class.py
    ...: from functools import singledispatch
    ...: from typing import Any, List
    ...:
    ...: class Patchwork(object):
    ...:
    ...:     def __init__(self, **kwargs):
    ...:         for k, v in kwargs.items():
    ...:             setattr(self, k, v)
    ...:
    ...:     @singledispatch
    ...:     def get(self, arg: Any) -> Any:
    ...:         return getattr(self, arg, None)
    ...:
    ...:     @get.register(list)
    ...:     def _get_list(self, arg: List) -> List:
    ...:         return [self.get(x) for x in arg]
    ...:
    ...: if __name__ == '__main__':
    ...:     pw = Patchwork(a=1, b=2, c=3)
    ...:     print(pw.get('b'))
    ...:     print(pw.get(['a', 'c']))
    ...:
 2
 ---------------------------------------------------------------------------
 TypeError                                 Traceback (most recent call last)
 Input In [2], in <cell line: 19>()
      20 pw = Patchwork(a=1, b=2, c=3)
      21 print(pw.get('b'))
 ---> 22 print(pw.get(['a', 'c']))
 
 File ~/.anyenv/envs/pyenv/versions/miniconda3-4.7.12/envs/scraping/lib/python3.10/functools.py:889, in singledispatch.<locals>.wrapper(*args, **kw)
     885 if not args:
     886     raise TypeError(f'{funcname} requires at least '
     887                     '1 positional argument')
 --> 889 return dispatch(args[0].__class__)(*args, **kw)
 
 Input In [2], in Patchwork.get(self, arg)
      11 @singledispatch
      12 def get(self, arg: Any) -> Any:
 ---> 13     return getattr(self, arg, None)
 
 TypeError: getattr(): attribute name must be string
 
 In [3]:
 
```

singledispatchデコレーターは第一引数の型に基づいて登録されたものから呼び出す関数を選択する  `wraper()` を返すようになっています。


```
   def wrapper(*args, **kw):
        return dispatch(args[0].__class__)(*args, **kw)
```

これは、通常の関数では問題ありませんが、クラスのメソッドでは、その最初の引数は常に `self` になるためうまく処理できません。Python 3.8 以降では、この問題に対応した [sinpledispathmethod ](https://docs.python.org/ja/3/library/functools.html#functools.singledispatchmethod) が使用できます。
古いバージョンの Python では、次の  `singledispatchmethod` のようなデコレーターを定義すると、うまく処理することができます。


python
```
 In [2]: # %load c04_singledispatch_with_class.py
    ...: from typing import Any, List
    ...: try:
    ...:     # Python 3.8 or later
    ...:     from functools import singledispatchmethod
    ...: except ImportError:
    ...:     from functools import singledispatch, update_wrapper
    ...:
    ...:     def singledispatchmethod(func):
    ...:         dispatcher = singledispatch(func)
    ...:         def wrapper(*args, **kw):
    ...:             return dispatcher.dispatch(args[1].__class__)(*args, **kw)
    ...:         wrapper.register = dispatcher.register
    ...:         update_wrapper(wrapper, func)
    ...:         return wrapper
    ...:
    ...: class Patchwork(object):
    ...:
    ...:     def __init__(self, **kwargs):
    ...:         for k, v in kwargs.items():
    ...:             setattr(self, k, v)
    ...:
    ...:     @singledispatchmethod
    ...:     def get(self, arg: Any) -> Any:
    ...:         return getattr(self, arg, None)
    ...:
    ...:     @get.register(list)
    ...:     def _get_list(self, arg: List) -> List:
    ...:         return [self.get(x) for x in arg]
    ...:
    ...: if __name__ == '__main__':
    ...:     pw = Patchwork(a=1, b=2, c=3)
    ...:     print(pw.get('b'))
    ...:     print(pw.get(['a', 'c']))
    ...:
 2
 [1, 3]
 
 In [3]:
 
```

# 応用例
[jp_prefecture ](https://github.com/iisaka51/jp_prefecture) では、JIS X 0401-1973 で定義されている都道府県の番号と名前を相互変換するものです。

名前、アフファベット名、コードを相互に変換するために、 singledispatch を使用しています。


```
     @singledispatchmethod
     def code2name(self, arg: Any) -> Optional[str]:
         """ Convert prefecture code to name """
         raise TypeError('Unsupport Type')
 
     @code2name.register(type(None))
     def _code2name_none(self,
             codeL: None,
             ascii: bool=False,
         ):
         """ Convert prefecture code to name """
         return None
 
     @code2name.register(int)
     def _code2name_int(self,
             code: Optional[int]=None,
             ascii: bool=False,
         ) -> Optional[str]:
         """ Convert prefecture code to name """
         try:
             name = [self.__code2name[code],
                     self.__code2alphabet[code]][ascii]
         except KeyError:
             name = None
         return name
 
     @code2name.register(str)
     def _code2name_int(self,
             code: str,
             ascii: bool=False,
         ) -> Optional[str]:
         """ Convert prefecture code to name """
         try:
             name = [self.__code2name[int(code)],
                     self.__code2alphabet[int(code)]][ascii]
         except KeyError:
             name = None
         return name
                          
```

この定義で、 `code` に文字列でも数値でも受け付けるようになります。


```
 In [1]: from jp_prefecture import jp_prefectures as jp
 
 In [2]: jp.code2name(26)
 Out[2]: '京都府'
 
 In [3]: jp.code2name("26")
 Out[3]: '京都府'
 
 In [4]:
```

繰り返しになりますが、singledipatch/singledispatchmethod を使うと、サポートする型を追加したときでも既存コードには修正が入らないことはとても有益な利点です。


