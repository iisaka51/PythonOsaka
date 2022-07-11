Pythonでの分岐処理のあれこれ
=================
# 条件式による分岐
プログラミング言語では条件式による分岐処理はなくてはならないもののひとつです。Pythonにも  `if` 文があります。
次のような構文になります。

```
  if 条件式:
      条件式が真のときの処理
```

あるいは


```
 if 条件式:
     条件式が真のときの処理
  else:
      条件式が偽のときの処理
```

もう少し具体的なコードを例示してみましょう。


```
 In [2]: # %load c01_password.py
    ...: import crypt
    ...: import getpass as gw
    ...:
    ...: # To generate, type in a python/IPython shell:
    ...: #  print(crypt.crypt('PASSWORD', 'SALT'))"
    ...: salt='administrator'
    ...: hashed_password='adk6oNRwypFwA'
    ...:
    ...: if hashed_password == crypt.crypt(gw.getpass(), salt):
    ...:     print('Wellcome')
    ...: else:
    ...:     print('Worng password.')
    ...:
 Password:
 Wellcome

 In [3]:
```

ここまでは、何も問題ありませんよね。条件式が複数連続させたいちきは、 `elif` を使います。


```
 if 条件式1:
     条件式1が真のときの処理
  elif 条件式2:
     条件式2が真のときの処理
  # elif ... :
  #    ...
  else:
      すべての条件式が偽のときの処理
```

これも具体的なコードでみてましょう。コンピュータプログラミングで[FizzBuzz問題として知られているものです。
与えられた数値までの中に、3の倍数であれば文字列 Fizz を、5の倍数であれば文字列 Buzz を、両方の公倍数であれば文字列 FizzBuzz を出力して、いずれでもなければ数値を表示するといったもので、プラグラムができるかどうかの判断にも使われたりします。(参考: [Solving FizzBuzz Shows Interviewers Much More Than Your Programming Skills ](https://www.forbes.com/sites/quora/2016/09/12/solving-fizzbuzz-shows-interviewers-much-more-than-your-programming-skills/?sh=3fd722b73b36))


```
 In [2]: # %load c02_fizzbuzz.py
    ...: max = 100
    ...:
    ...: for n in range(1, max):
    ...:     if n % 5 == 0 and n % 3 == 0:
    ...:         print("FizzBuzz")
    ...:     elif n % 3 == 0:
    ...:         print("Fizz")
    ...:     elif n % 5 == 0:
    ...:         print("Buzz")
    ...:     else:
    ...:         print(n)
    ...:
 1
 2
 Fizz
 4
 Buzz
 Fizz
 7
 8
 Fizz
 Buzz
 11
 Fizz
 13
 14
 FizzBuzz
 16
 17
 Fizz
 19
 (以下略）

```

ここで意識しておく必要があることは、’**条件式は記述した順序で評価される**ということです。つまり、上から下、左から右に順に評価されます。小さなことですが、これは意外に重要なことです。例えばほとんど成立しない条件式を先頭におくと、この条件式が毎回無駄に評価されてしまうことになります。


# Pythonの論理演算子
先の例にもあるように、条件式は  `count % 5 == 0` などのように比較演算子を使うことが多いです。 このとき、複数の条件式を論理演算子を使って連続させることもできます。

Python では次の3つの論理演算子があります。

  -  `and` ー　両方が真　 `x < 5 and  x < 10`
  -  `or` 　ー　いずれかが真のときに真   `x < 5 or x < 4`
  -  `not` ー　偽であれば真   `not(x < 5 and x < 10)`


```
 if count % 5 == 0 and count % 3 == 0:
     print("FizzBuzz")
```

論理演算子は**左から右に評価される** ことを意識するようにしてください。上記の例では、はじめに　 `count % 5 == 0` が評価され、その結果が真のときに次の　 `count % 3 == 0` が評価されます。大事なことは、 `and` の場合は、はじめの条件式が偽のときは続く条件式は評価されないということです。そのため、次のように記述することは条件が成立する確率的が高いものを先に書いてしまっているため、良くないということになります。

```
 if count % 3 == 0 and count % 5 == 0:
     print("FizzBuzz")
```



# 真とはなにか？偽とはなにか？
Python では 真値を  `True` , 偽値を  `False` と表現します。これらは、bool型に区分されています。そしてこの bool 型は int 型のサブクラスとして定義されています。


```
 In [1]: issubclass(bool, int)
 Out[1]: True

```

実際のところ  `True` は 1、 `False` は 0 と同じ値となります。そしてint型のサブクラスであることから演算もできてしまいます。

 pytohn
```
 In [1]: True * 2
 Out[1]: 2

 In [2]: False + 1
 Out[2]: 1

```

意図的に bool 型の値に対して四則演算はしないはずですが、これは理解しておく必要のあることです。

比較演算子  `==` はオブジェクトが**同じ値を持つ**ときに真となります。　 `is` はオブジェクトが**同じもの**であるときに真となります。


```
 n [1]: True == 1
 Out[1]: True

 In [2]: False == 0
 Out[2]: True

 In [3]: True is 1
 <>:1: SyntaxWarning: "is" with a literal. Did you mean "=="?
 <ipython-input-3-0acca4945321>:1: SyntaxWarning: "is" with a literal. Did you mean "=="?
   True is 1
 Out[3]: False

 In [4]: False is 0
 <>:1: SyntaxWarning: "is" with a literal. Did you mean "=="?
 <ipython-input-4-62d8d9e7196d>:1: SyntaxWarning: "is" with a literal. Did you mean "=="?
   False is 0
 Out[4]: False

 In [5]:
```

Python での真偽の評価は、**偽でないものは真**という考え方になります。Pythonで偽と評価されるものは、ゼロ( `0` ）、 `False` 、要素のない空のオブジェクト、 `None` があり、それ以外は真として評価されることに注意してください。

そのため、 `if` 文に与える条件式に  `a == True` のように True かどうかを判断させることは良くない場合があります。


## タプルを使った分岐
Python であまり認知されていないもののひとつに機能のひとつに、タプルやリストを使った分岐があります。


```
 (条件式が偽のときの値、条件式が真のときの値)[条件式]
 [条件式が偽のときの値、条件式が真のときの値][条件式]
```

これは、  `True` が1 であり、 `False` が 0 であるために動作するので、タプルだけでなくリストでも可能です。


```
 In [2]: # %load c03_tuple_branches.py
    ...: num = 10
    ...: ans = ('odd', 'even')[num % 2 == 0]
    ...:

 In [3]: ans
 Out[3]: 'even'

 In [4]:

```

次のように記述するとどうなっているか理解しやすいはずです。


```
 In [2]: # %load c04_tuple_branches2.py
    ...: num = 10
    ...: decision_table = ('odd', 'even')
    ...: decision_table[num % 2 == 0]
    ...:
 Out[2]: 'even'

 In [3]:
```


この例では値が  `even` もしくは  `odd` なのでわかりやすいですが、次のように数値だけの場合はどうでしょう。

```
 In [2]: # %load c05_ternay_random.py
    ...: import random
    ...:
    ...: a = random.random()
    ...: b = random.random()
    ...:
    ...: c = (b, a)[a>b]
    ...:

 In [3]: c
 Out[3]: 0.7988492824016477

 In [4]:
```

 `c` の値だけでは、それが `a` と `b` のどちらの値なのか判断できません。例示のためにコードを次のようにしてみます。


```
 In [2]: # %load c06_ternary_notation.py
    ...: import random
    ...:
    ...: a = random.random()
    ...: b = random.random()
    ...:
    ...: c = (f'b:{b}', f'a:{a}')[a>b]
    ...:

 In [3]: c
 Out[3]: 'b:0.8297190471327163'

 In [4]:

```

これで、 `a` か  `b` かどちらの値なのかはっきりしますね。とわいえこの方法での分岐は、Python ではbool値が  `(Ture, False) == (1, 0 )` であることに依存しています。コードの可読性が悪くなり保守しずらいものになることに注意が必要です。「記述できること」よりも「保守しやすいこと」を意識したコードを書くべきでしょう。そこで、タプル’やリストではなく、辞書を使うとPython でもう少し可読性がよくなります。


```
 In [2]: # %load c07_ternery_dict.py
    ...: import random
    ...:
    ...: a = random.random()
    ...: b = random.random()
    ...:
    ...: c = {False: f'b:{b}', True: f'a:{a}'}[a>b]
    ...:

 In [3]: c
 Out[3]: 'b:0.8699309235969509'

 In [4]:

```

意識する必要があることは、タプルやリスト、辞書での三項演算では、条件式により値が選ばれる前に、タプルやリストで定義した値がすべて評価されることです。
どちらかだけを評価させたい場合はラムダ式を使います。


```
 In [2]: # %load c08_ternary_lamba.py
    ...: import random
    ...:
    ...: a = random.random()
    ...: b = random.random()
    ...: c = (lambda: f"a:{a}", lambda: f"b:{b}")[a>b]()
    ...:

 In [3]: c
 Out[3]: 'b:0.6369879852372617'

 In [4]:

```

これらはトリッキーに見えるかもしれませんが、入力と出力を[デシジョンテーブル(Decison Table) ](https://en.wikipedia.org/wiki/Decision_table) で整理することは、コンピュータプラグラミングでは非常によく利用される技法のひとつです。


##  分岐を1行で記述する
Pythonでは通常のif構文に加えて、1行で記述できる構文もあります。Python 2.5 で追加されたもので、**三項演算子（ternary operator)** と呼ばれるものです。


```
 条件式が真のときの値 if 条件式 else 条件式が偽のときの値
```

これは可読性が低くなるのですが、リスト内包表記で条件に応じて処理するようなときによく使用されるものです。

先の FizzBuzz問題を三項演算子を使って記述すると次のようになります。


```
 In [2]: # %load c09_fizzbuzz_complehension.py
    ...: max = 100
    ...: ans = [ 'FizzBuzz' if x % 5 == 0 and x % 3 == 0 else 'Buzz' if x % 5 == 0
    ...:  else 'Fizz' if x % 3 == 0 else x for x in range(max+1)]
    ...:

 In [3]: ans
 Out[3]:
 ['FizzBuzz',
  1,
  2,
  'Fizz',
  4,
  'Buzz',
  'Fizz',
  7,
  8,
  'Fizz',
  'Buzz',
  11,
  'Fizz',
  13,
  14,
  'FizzBuzz',
  16,
  17,
  (攻略）

```

前述しているように、コードを短くすることだけの目的で使用しないでくだい。
考察のために、次のコードをみてみましょう。


```
 In [2]: # %load c10_fizzbuzz_paranoiz.py
    ...: max = 100
    ...: ans = [ 'Fizz'*(n%3==0) + 'Buzz'*(n%5==0) or n for n in range(1, max)]
    ...:

 In [3]: ans
 Out[3]:
 ['FizzBuzz',
  1,
  2,
  'Fizz',
  4,
  'Buzz',
  'Fizz',
  7,
  8,
  'Fizz',
  'Buzz',
  11,
  'Fizz',
  13,
  14,
  'FizzBuzz',
  16,
  17,
  'Fizz',
  19,
  'Buzz',
  'Fizz',
  （以下略）

```

このコードは、 `c09_fizzbuzz_complehension.py` と同じようにリスト内包表記を使っています。一見するとスッキリとしているようですが、これはかなり良くないコードになります。
理由を説明しましょう。まず、 `'Fizz'*(n%3==0) + 'Buzz'*(n%5==0)` はPython ではbool値が  `(Ture, False) == (1, 0 )` であることに加えて、文字列でも四則演算ができることを利用しています。可読性が悪いこともそうですが、なにより’演算回数が多くなることが良くないです。

ちなみに、Python のbool値の特性を利用しない方がもっと短くコードできますが、さらに難読なコードになります。


```
 In [2]: # %load c11_fizzbuzz_minimam.py
    ...: max = 100
    ...: ans = [n%3//2*'Fizz'+n%5//4*"Buzz"or n for n in range(max + 1)]
    ...:

 In [3]: ans[:18]
 Out[3]:
 [0,
  1,
  'Fizz',
  3,
  'Buzz',
  'Fizz',
  6,
  7,
  'Fizz',
  'Buzz',
  10,
  'Fizz',
  12,
  13,
  'FizzBuzz',
  15,
  16,
  'Fizz']

 In [4]:

```


# 条件式だけの分岐処理
論理演算子の評価順序を利用した分岐処理を記述することができます。例えば、次のようなコードは、デフォルト値のセットなどに使用することができます。


```
 TEST=None

 val = TEST or 1
```

 `TEST` の値が偽と評価されるときだけ1が  `val` にセットされます。

三項演算子や論理演算を使った条件分岐は関数で変数の初期化を行うようなときに使うとコードの可読性がよくなります。
例をみてみましょう。次のコードにある  `func1()` と　 `func2()` と  `func3()` を比べてみてください。


```
 In [2]: # %load c12_short_ternary.py
    ...: def func1(real_name, nickname=None):
    ...:     if nickname:
    ...:         name = nickname
    ...:     else:
    ...:         name = real_name
    ...:     return(name)
    ...:
    ...: def func2(real_name, nickname=None):
    ...:     name = nickname if nickname else real_name
    ...:     return(name)
    ...:
    ...: def func3(real_name, nickname=None):
    ...:     name = nickname or real_name
    ...:     return(name)
    ...:
    ...:
    ...: v1 = ( func1('Freddie Bulsara'),
    ...:        func1('Freddie Bulsara', 'Freddie Mercury'))
    ...: v2 = ( func2('Freddie Bulsara'),
    ...:        func2('Freddie Bulsara', 'Freddie Mercury'))
    ...: v3 = ( func3('Freddie Bulsara'),
    ...:        func3('Freddie Bulsara', 'Freddie Mercury'))
    ...:
    ...: assert v1 == v2 and v1 == v3
    ...:

 In [3]:

```


# any() と all() を使った分岐
Pythonの組み込み関数   `any()` と  `all()` を使って条件式をまとめることができます。

  -  `all()` ー すべての要素が `True` であれば `True` を返す
  -  `any()` ー いずれかの要素が `True` であれば `True` を返す

次のコードは、 `all()` で二つの条件式をまとめています。


```
 In [2]: # %load c13_ternary_all_any.py
    ...: import random
    ...:
    ...: a = random.random()
    ...: b = random.random()
    ...:
    ...: decision_table = { False: f'F: {a}, b:{b}', True: f'T: {a}, b:{b}' }
    ...: c = decision_table[ all([a%2==0, b%2==0]) ]
    ...: d = decision_table[ any([a%2==0, b%2==0]) ]
    ...:

 In [3]: c
 Out[3]: 'F: 0.590054415862441, b:0.41650387467125227'

 In [4]: d
 Out[4]: 'F: 0.590054415862441, b:0.41650387467125227'

 In [5]:

```

 `all()` と `any()` を使うと複数の条件式に対しての  `and` や  `or` で記述したものと等価になります。


# パターンマッチによる分岐
Pytohn 3.10 から利用できるようになったパターンマッチを使って分岐を記述してみましょう。


```
 n [2]: # %load c14_pattern_match.py
    ...: max = 100
    ...:
    ...: for n in range(1, max):
    ...:     match n:
    ...:         case n if n % 5 == 0 and n % 3 == 0: print('FizzBuzz')
    ...:         case n if n % 3 == 0: print('Fizz')
    ...:         case n if n % 5 == 0: print('Buzz')
    ...:         case _: print(n)
    ...:
 1
 2
 Fizz
 4
 Buzz
 Fizz
 7
 8
 Fizz
 Buzz
 11
 Fizz
 13
 14
 FizzBuzz
 16
 17
 (以下略）

```

 `match` で評価した値を `case` で受けて分岐させることができます。この例の場合は、 `n` をパターンとして指定しているため、すべてがマッチします。そこで `if` をつけることで条件付きのパターンマッチを行っています。`

この FizzBuzz問題のような単純なケースではパターンマッチを使うメリットはありません。パターンマッチ構文がその真価を発揮する場合は、 `case` をクラスで受けるときです。

## 三項演算子について考察
 `c09_fizzbuzz_complehension.py` のコードの可読性を向上させるためには’、どんな方法があるでしょうか？


```
 In [2]: # %load c09_fizzbuzz_complehension.py
    ...: max = 100
    ...: ans = [ 'FizzBuzz' if x % 5 == 0 and x % 3 == 0 else 'Buzz' if x % 5 == 0
    ...:  else 'Fizz' if x % 3 == 0 else x for x in range(max+1)]
    ...:

 In [3]:
```

無理に1行でコードすることを避けてみましょう。
括弧（ `(...)` で囲んだコードは改行が自由になるので、次のようにしてみます。


```
 In [2]: # %load c15_fizzbuzz_refactor.py
    ...: max = 100
    ...: ans = [ ('FizzBuzz' if x % 5 == 0 and x % 3 == 0 else
    ...:           'Buzz' if x % 5 == 0 else
    ...:           'Fizz' if x % 3 == 0 else x ) for x in range(1,max)]
    ...:

 In [3]:

```

次に、ループと分岐の記述を切り離すことを考えてみましょう。まずは、単純に関数にしてみましょう。


```
 In [2]: # %load c16_fizzbuzz_func.py
    ...: def fizzbuzz(n):
    ...:     data  = ( "FizzBuzz" if n % 5 == 0 and n % 3 == 0 else
    ...:               "Fizz" if n % 3 == 0 else
    ...:               "Buzz" if n % 5 == 0 else n )
    ...:     return data
    ...:
    ...: max = 100
    ...: ans = [ fizzbuzz(n) for n in range(1, max) ]
    ...:

 In [3]:

```

関数の定義が冗長なので、無名関数を使ってみます。


```
 In [2]: # %load c17_fizzbuzz_lambda.py
    ...: fizzbuzz = lambda n: ( "FizzBuzz" if n % 5 == 0 and n % 3 == 0 else
    ...:                        "Fizz" if n % 3 == 0 else
    ...:                        "Buzz" if n % 5 == 0 else n )
    ...:
    ...: max = 100
    ...: ans = [ fizzbuzz(n) for n in range(1, max) ]
    ...:

 In [3]:

```

このコードで注意する必要がある点は、リストを生成していることです。これは、 `max` の値によってはメモリ不足で実行できない状況になることを意識することが重要です。こうした場合、ジェネレータを使用することになります。
リスト内包表記では、 `[...]` を　 `(...)` に変えるだけで、簡単にジェネレータに変更できます。


```
 In [2]: # %load c18_fizzbuzz_generator.py
    ...: fizzbuzz = lambda n: ( "FizzBuzz" if n % 5 == 0 and n % 3 == 0 else
    ...:                        "Fizz" if n % 3 == 0 else
    ...:                        "Buzz" if n % 5 == 0 else n )
    ...:
    ...: max = 100
    ...: ans1 = [ fizzbuzz(n) for n in range(1, max) ]
    ...: ans2 = ( fizzbuzz(n) for n in range(1, max) )
    ...:

 In [3]: type(ans1)
 Out[3]: list

 In [4]: type(ans2)
 Out[4]: generator

 In [5]:

```


ジェネレータは遅延評価されるため、挙動が異なる場合があることに注意してください。例として、次のコードを見てみましょう。


```
 In [2]: # %load c19_generator_lazy.py
    ...: def func1():
    ...:     data = [1.0 / x for x in [3, 2, 1, 0]]
    ...:     for x in data:
    ...:         print(x)
    ...:
    ...: def func2():
    ...:     data = (1.0 / x for x in [3, 2, 1, 0])
    ...:     for x in data:
    ...:         print(x)
    ...:
    ...:

 In [3]: func1()
 ---------------------------------------------------------------------------
 ZeroDivisionError                         Traceback (most recent call last)
 Input In [3], in <cell line: 1>()
 ----> 1 func1()

 Input In [2], in func1()
       2 def func1():
 ----> 3     data = [1.0 / x for x in [3, 2, 1, 0]]
       4     for x in data:
       5         print(x)

 Input In [2], in <listcomp>(.0)
       2 def func1():
 ----> 3     data = [1.0 / x for x in [3, 2, 1, 0]]
       4     for x in data:
       5         print(x)

 ZeroDivisionError: float division by zero

 In [4]: func2()
 0.3333333333333333
 0.5
 1.0
 ---------------------------------------------------------------------------
 ZeroDivisionError                         Traceback (most recent call last)
 Input In [4], in <cell line: 1>()
 ----> 1 func2()

 Input In [2], in func2()
       7 def func2():
       8     data = (1.0 / x for x in [3, 2, 1, 0])
 ----> 9     for x in data:
      10         print(x)

 Input In [2], in <genexpr>(.0)
       7 def func2():
 ----> 8     data = (1.0 / x for x in [3, 2, 1, 0])
       9     for x in data:
      10         print(x)

 ZeroDivisionError: float division by zero

 In [5]:

```

 `func1()` と  `func2()` どちらの関数も  `data` を内部で定義していて、`ゼロでの割り算が含まれています。これは、関数が呼ばれたときに評価実行されます。  `func1()` では `data` をリストで定義しているため、この時点で例外が発生しています。これに対して、 `func2()` では、遅延評価されるため、実際にゼロでの割り算が評価されるまでは、コードが実行するため、ループ処理が実行されています。



# クラスの利用
今回の FizzBuzz問題ではほとんど使い捨ての関数になるため無名関数でも十分ですが、実際のプロジェクトではデータに対してクラスを定義しておく方が保守性と柔軟性が向上することになります。


```
 n [2]: # %load c20_fizzbuzz_class.py
    ...: from typing import Union, Tuple
    ...:
    ...: class FizzBuzz:
    ...:     def __init__(self, n: int):
    ...:         self.n: int = n
    ...:         self._fizzbuzz: Union[str, int] = (
    ...:             "FizzBuzz" if self.n % 5 == 0 and self.n % 3 == 0 else
    ...:             "Fizz" if self.n % 3 == 0 else
    ...:             "Buzz" if self.n % 5 == 0 else self.n )
    ...:
    ...:     @property
    ...:     def fizzbuzz(self) -> Tuple[int, Union[str, int]]:
    ...:         return self.n, self._fizzbuzz
    ...:
    ...: max = 100
    ...: ans = [ FizzBuzz(n) for n in range(1, max)]
    ...:

 In [3]: for n in ans[:18]: print(n.fizzbuzz)
 (1, 1)
 (2, 2)
 (3, 'Fizz')
 (4, 4)
 (5, 'Buzz')
 (6, 'Fizz')
 (7, 7)
 (8, 8)
 (9, 'Fizz')
 (10, 'Buzz')
 (11, 11)
 (12, 'Fizz')
 (13, 13)
 (14, 14)
 (15, 'FizzBuzz')
 (16, 16)
 (17, 17)
 (18, 'Fizz')

 In [4]:

```


## dataclass の利用
Pythonでdataclassses ライブラリを使うとデータをうまく扱えるようになります。処理を分岐させるためにdataclass を使うわけではありませんが、面白いので紹介します。


```
 In [2]: # %load c21_dataclass.py
    ...: from dataclasses import dataclass, field
    ...: from typing import Union
    ...:
    ...: @dataclass
    ...: class Number:
    ...:     n: int
    ...:     fizzbuzz: Union[str, int] = field(init=False)
    ...:
    ...:     def __post_init__(self) -> None:
    ...:         self.fizzbuzz = (
    ...:             "FizzBuzz" if self.n % 5 == 0 and self.n % 3 == 0 else
    ...:             "Fizz" if self.n % 3 == 0 else
    ...:             "Buzz" if self.n % 5 == 0 else self.n )
    ...:
    ...: max = 100
    ...: ans = [ Number(n) for n in range(1, max)]
    ...:
    ...:

 In [3]: ans[:18]
 Out[3]:
 [Number(n=1, fizzbuzz=1),
  Number(n=2, fizzbuzz=2),
  Number(n=3, fizzbuzz='Fizz'),
  Number(n=4, fizzbuzz=4),
  Number(n=5, fizzbuzz='Buzz'),
  Number(n=6, fizzbuzz='Fizz'),
  Number(n=7, fizzbuzz=7),
  Number(n=8, fizzbuzz=8),
  Number(n=9, fizzbuzz='Fizz'),
  Number(n=10, fizzbuzz='Buzz'),
  Number(n=11, fizzbuzz=11),
  Number(n=12, fizzbuzz='Fizz'),
  Number(n=13, fizzbuzz=13),
  Number(n=14, fizzbuzz=14),
  Number(n=15, fizzbuzz='FizzBuzz'),
  Number(n=16, fizzbuzz=16),
  Number(n=17, fizzbuzz=17),
  Number(n=18, fizzbuzz='Fizz')]

 In [4]:

```

注目してほしいのは、結果にオリジナルの数値と変換後の値の両方を保持しているところと、リスト内包表記がスッキリして可読性がよくなっていることです。クラス `Number` を初期化すると  `__post_init__()` が呼び出されてFizzBuzz問題を解いて格納します。


```
 In [4]: for d in ans[:18]: print(d.fizzbuzz)
 1
 2
 Fizz
 4
 Buzz
 Fizz
 7
 8
 Fizz
 Buzz
 11
 Fizz
 13
 14
 FizzBuzz
 16
 17
 Fizz

```

こうして見てくると三項演算子での分岐も便利に使えることがわかりますよね。



