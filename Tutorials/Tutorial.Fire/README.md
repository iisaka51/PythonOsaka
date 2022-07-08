オプション解析モジュールFireを使ってみよう
=================
## Python-Fire について
Python-Fire はPythonオブジェクトからコマンドラインインターフェイス(CLI: Command Line Interface)を自動生成するためのライブラリで、次のような特徴があります。

- Python Fireは、PythonでCLIアプリケーションを簡単に作成できます。
  - 既存コードをほんど変更することなくCLIアプリケーションにすることができます。
- Python Fireは、Pythonコードを開発/デバッグための便利なツールです。
- Python Fireは、既存のコードを探索するときに便利なツールです。
- Python Fireは、Pythonの会話形インタフェースREPLを簡単に提供することができます。
  - モジュールと変数などのオブジェクトはすぐに使用できる状態になっています。
  - IPython がインストールされていればREPLとしてIPyhton が起動します。

## Python-Fire のインストール
Python-Fire は拡張モジュールなのでインストールする必要があります。
 pip
```
 $ pip install fire
```

## 使用方法

今、次のような関数があるとします。
hello.py
```
 def hello(name="World"):
   return "Hello %s!" % name
```

この関数をCLIアプリケーションとしたい場合は、単に  `fire.Fire()` で関数を呼び出すだけで、既存コードを修正する必要はありません。

hello_cli.py
```
 from hello import hello
 import fire
 fire.Fire(hello)
```

ヘルプメッセージを表示するためには、 `--help` もしくは  `-h` をオプションで与えます。
 zsh
```
 % python hello_cli.py --help
```

fire は組み込み関数  `help()` のようにヘルプメッセージを表示してくれます。
 zsh
```
 NAME
     hello_cli.py

 SYNOPSIS
     hello_cli.py <flags>

 FLAGS
     --name=NAME

```

 zsh
```
 % python hello_cli.py
 Hello World!

 % python hello_cli.py --name Jack
 Hello Jack!
```

複数のオプションが与えられると最後に指定した値が使用されます。
 zsh
```
 % python hello_cli.py --name Jack --name Eddie
 Hello Eddie!
```

また、Python 実行時に  `-m fire` を与えると、
 `hello.py` をまったく修正しなくてもCLIアプリケーションとして動作させることができます。

 zsh
```
 % python -m fire hello
```

ここで与えている hello は fire が読み込むモジュール名です。つまり、このディレクトリにある hello.py が読み込まれます。

次のようにヘルプメッセージが表示され、関数 `hello()` がサブコマンドとして実行受け付けることがわかります。
zsh
```
 NAME
     hello

 SYNOPSIS
     hello COMMAND

 COMMANDS
     COMMAND is one of the following:

      hello

```

 zsh
```
 % python -m fire hello hello --help
```

 zsh
```
 NAME
     hello hello

 SYNOPSIS
     hello hello <flags>

 FLAGS
     --name=NAME
```

 zsh
```
 % python -m fire hello hello
 Hello World!

 % python -m fire hello hello Jack
 Hello Jack!

 % python -m fire hello hello --name David
 Hello David!
```

## 複数の関数があるときはどうするのか？
次のように複数の関数があるファイルについても、fire は対応できます。
 mymath.py
```
 def add(x, y):
   return x + y

 def multiply(x, y):
   return x * y

 def squre(n):
   return(n**2)

 def cube(n):
   return(n**3)
```

コード修正する場合は、これまでと同様に  `fire.Fire()` を実行するだけです。
 mymath_cli.py
```
 from mymath import *
 import fire
 fire.Fire()
```

ヘルプメッセージを表示してみましょう。
 zsh
```
 % python mymath_cli.py --help
```

ファイルにある関数を読み込んで複数のサブコマンドとして受け付けることがわかります。
 zsh
```
 NAME
     mymath_cli.py

 SYNOPSIS
     mymath_cli.py GROUP | COMMAND

 GROUPS
     GROUP is one of the following:

      fire
        The Python Fire module.

 COMMANDS
     COMMAND is one of the following:

      add

      multiply

      squre

      cube
```

## 特定の関数だけにCLIを追加したい
デフォルトではスクリプトファイルにあるすべての関数をサブコマンドとして扱いますが、 `fire.Fire()` を呼び出すときに辞書で対象関数を指定することができます。

 mymath_cli2.py
```
 from mymath import squre, cube
 import fire
 fire.Fire({
     'Squire': squre,
     'Cube': cube,
 })
```

ヘルプメッセージを表示してみましょう。
 zsh
```
 % python mymath_cli2.py --help
```

 zsh
```
 NAME
     mymath_cli2.py

 SYNOPSIS
     mymath_cli2.py COMMAND

 COMMANDS
     COMMAND is one of the following:

      Squire

      Cube
```
辞書で与えたキーの文字列がサブコマンド名となります。

## クラスを呼び出す
 `fire.Fire()` はクラスもCLIアプリケーションにすることができます。
今、次のようなクラスがあるとします。
 calculator.py
```
 class Calculator(object):
    """A simple calculator class."""

    def double(self, number):
      return 2 * number
```

 `fire.Fire()` の引数にCLIにするクラスを与えます。

 calculator_cli.py
```
 from calculator import Calculator
 import fire
 fire.Fire(Calculator)
```

このクラスの  `double()` メソッドにはデフォルト値が定義されていません。
そのため。コマンド引数を与えずに実行すると、 `--help` オプションが与えられたときと同様にヘルプメッセージを表示します。
 zsh
```
 % python calculator_cli.py
```

 zsh
```
 NAME
     calculator_cli.py - A simple calculator class.

 SYNOPSIS
     calculator_cli.py COMMAND

 DESCRIPTION
     A simple calculator class.

 COMMANDS
     COMMAND is one of the following:

      double
```

 `Calculatror` クラスの `double` メソッドの関数名がサブコマンド名となります。
サブコマンドのヘルプを表示してみましょう。
 zsh
```
 % python calculator_cli.py double --help
```

 zsh
```
 NAME
     calculator_cli.py double

 SYNOPSIS
     calculator_cli.py double NUMBER

 POSITIONAL ARGUMENTS
     NUMBER

 NOTES
     You can also use flags syntax for POSITIONAL ARGUMENTS

```


 zsh
```
 % python calculator_cli.py double 20
 40
 % python calculator_cli.py double --number 20
 40
```

関数よりもクラスを使用する方が柔軟性が高まります。
次の例を見てみましょう。

 calculator_cli2.py
```
 class BrokenCalculator(object):

   def __init__(self, offset=1):
       self._offset = offset

   def add(self, x, y):
     return x + y + self._offset

   def multiply(self, x, y):
     return x * y + self._offset

 if __name__ == '__main__':
   import fire
   fire.Fire(BrokenCalculator)
```

この `BrokenCalculator` はインスタンス生成時に `offset` 引数を取ることができます。
これをオプションとしてコマンドラインから与えることができます。
 zsh
```
 % python example.py add 10 20
 31
 % python example.py multiply 10 20
 201
 % python example.py add 10 20 --offset=0
 30
 % python example.py multiply 10 20 --offset=0
 200
```

## サブコマンドのグループ化

 group.py
```
 class IngestionStage(object):

   def run(self):
     return 'Ingesting! Nom nom nom...'

 class DigestionStage(object):
   def run(self, volume=1):
     return ' '.join(['Burp!'] * volume)

   def status(self):
     return 'Satiated.'

 class Pipeline(object):
   def __init__(self):
     self.ingestion = IngestionStage()
     self.digestion = DigestionStage()

   def run(self):
     value = list()
     result = self.ingestion.run()
     value.append(result)
     result = self.digestion.run()
     value.append(result)
     return value

 if __name__ == '__main__':
   import fire
   fire.Fire(Pipeline)
```

 zsh
```
 % python group.py
```

 zsh
```
 NAME
     group.py

 SYNOPSIS
     group.py GROUP | COMMAND

 GROUPS
     GROUP is one of the following:

      digestion

      ingestion

 COMMANDS
     COMMAND is one of the following:

      run

```

 zsh
```
 % python group.py digestion --help
```

zsh
```
 NAME
     group.py digestion

 SYNOPSIS
     group.py digestion COMMAND

 COMMANDS
     COMMAND is one of the following:

      run

      status
```

 zsh
```
 % python group.py ingestion --help
```

 zsh
```
 NAME
     group.py ingestion

 SYNOPSIS
     group.py ingestion COMMAND

 COMMANDS
     COMMAND is one of the following:

      run
```

 zsh
```
 % python group.py run
 Ingesting! Nom nom nom...
 Burp!

 % python group.py ingestion run
 Ingesting! Nom nom nom...

 % python group.py digestion run
 Burp!

 % python group.py digestion status
 Satiated.
```

> 公式ドキュメントについて補足：
> 公式ドキュメントでは  `Pipeline` は  `IngestionStage` と  `DigestionStage` クラスの  `run()` メソッドを呼び出すだけ と表記されています。
> しかし、これではその結果を表示することができません。
>  fire は戻り値を表示するため、値をreturn するか、
> 明示的に `print()` する必要があります。

## プロパティーにアクセスする
これまで見てきたサンプルプログラムでは、何かの関数を実行しています。
次のコードは、単にプロパティにアクセスするだけの例です。

[airports ](https://github.com/trendct-data/airports.py) はアメリカの空港コードを保持するモジュールです。

 access_cli.py
```
 from airports import airports

 class Airport(object):
   def __init__(self, code):
     self.code = code
     self.name = dict(airports).get(self.code)
     self.city = self.name.split(',')[0] if self.name else None

 if __name__ == '__main__':
   import fire
   fire.Fire(Airport)
```

 zsh
```
 % python access_cli.py --help
```

 zsh
```
 NAME
     access_cli.py

 SYNOPSIS
     access_cli.py --code=CODE

 ARGUMENTS
     CODE
```


 zsh
```
 % python access_cli.py --code=JSK
```

 zsh
```
 NAME
     access_cli.py --code=JFK

 SYNOPSIS
     access_cli.py --code=JFK VALUE

 VALUES
     VALUE is one of the following:

      city

      code

      name
```

ヘルプメッセージにあるようにプロパティーを与えるとその値が帰ってくるようになります。

 zsh
```
 % python access_cli.py --code=JFK city
 New York-New Jersey-Long Island

 % python access_cli.py --code=JFK name
 New York-New Jersey-Long Island, NY-NJ-PA - John F. Kennedy International (JFK)
```

 `fire.Fire()` は呼び出した結果に対して、引数で与えられたオブジェクトが実行できるメソッドを実行することができます。

 zsh
```
 % python access_cli.py --code=SFO name upper
 SAN FRANCISCO-OAKLAND-FREEMONT, CA - SAN FRANCISCO INTERNATIONAL (SFO)
```

これは airports モジュールにある airports は  `str` 型のリストなので、 `str` 型には  `upper` メソッドが使えるからです。
どのようなメソッドがあるかは `--help` をオプションを与えると詳細を知ることができますが、簡単には  `help` としても推察することができます。（エラーになることを利用しています）
 zsh
```
 % python access_cli.py --code=SFO name help
 ERROR: Could not consume arg: help
 Usage: access_cli.py --code=SFO name <command>
   available commands:    capitalize | casefold | center | count | encode |
                          endswith | expandtabs | find | format | format_map |
                          index | isalnum | isalpha | isascii | isdecimal |
                          isdigit | isidentifier | islower | isnumeric |
                          isprintable | isspace | istitle | isupper | join |
                          ljust | lower | lstrip | maketrans | partition |
                          replace | rfind | rindex | rjust | rpartition |
                          rsplit | rstrip | split | splitlines | startswith |
                          strip | swapcase | title | translate | upper | zfill

 For detailed information on this command, run:
   access_cli.py --code=SFO name --help
```

このため、関数を数珠つなぎで呼ばれるように設定したい場合は、メソッドが自分自身を返すクラスを用意するだけです。

 chain_cli.py
```
 class BinaryCanvas(object):
   """A canvas with which to make binary art, one bit at a time."""

   def __init__(self, size=10):
     self.pixels = [[0] * size for _ in range(size)]
     self._size = size
     self._row = 0  # The row of the cursor.
     self._col = 0  # The column of the cursor.

   def __str__(self):
     return '\n'.join(' '.join(str(pixel) for pixel in row) for row in self.pixels)

   def show(self):
     print(self)
     return self

   def move(self, row, col):
     self._row = row % self._size
     self._col = col % self._size
     return self
   def on(self):
     return self.set(1)

   def off(self):
     return self.set(0)

   def set(self, value):
     self.pixels[self._row][self._col] = value
     return self

 if __name__ == '__main__':
   import fire
   fire.Fire(BinaryCanvas)
```

zsh
```
 % python chain.py move 3 3 on move 3 6 on move 6 3 on move 6 6 on move 7 4 on move 7 5 on
 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0
 0 0 0 1 0 0 1 0 0 0
 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0
 0 0 0 1 0 0 1 0 0 0
 0 0 0 0 1 1 0 0 0 0
 0 0 0 0 0 0 0 0 0 0
 0 0 0 0 0 0 0 0 0 0
```

この例  `BinaryCanvas` の例では、0/1 の文字で構成されるキャンバスが表示されています。
これは、 `__str__` メソッドの定義に従っています。
 `__str__` メソッドが最終コンポーネントに存在する場合、オブジェクトはシリアル化されて表示されます。 `__str__` メソッドがない場合は、代わりにオブジェクトのヘルプ画面が表示されます。

## 変数にアクセスする
プロパティーにアクセスするだけでその値を返すようなCLIアプリケーションが記述できるわけですので、次のように変数にアクセスしても同様にことができます。

 greeting.py
```
 english = 'Hello World'
 spanish = 'Hola Mundo'

 import fire
 fire.Fire()
```

ヘルプメッセージを見てみましょう。
 zsh
```
 % python greeting.py --help
```

 zsh
```
 NAME
     greeting.py

 SYNOPSIS
     greeting.py GROUP | VALUE

 GROUPS
     GROUP is one of the following:

      fire
        The Python Fire module.

 VALUES
     VALUE is one of the following:

      english

      spanish
```

 zsh
```
 % python greeting.py english
 Hello World

 % python greeting.py spanish
 Hola Mundo
```


## 可変引数をとる関数
次のような可変引数をとるような関数の場合でも、fire はうまく処理してくれます。

 nargs_cli.py
```
 def order_by_length(*items):
   """Orders items by length, breaking ties alphabetically."""
   sorted_items = sorted(items, key=lambda item: (len(str(item)), str(item)))
   return ' '.join(sorted_items)

 if __name__ == '__main__':
   import fire
   fire.Fire(order_by_length)
```

 zsh
```
 % python nargs_cli.py --help
```

 zsh
```
 NAME
     nargs_cli.py - Orders items by length, breaking ties alphabetically.

 SYNOPSIS
     nargs_cli.py [ITEMS]...

 DESCRIPTION
     Orders items by length, breaking ties alphabetically.

 POSITIONAL ARGUMENTS
     ITEMS
```

 zsh
```
 % python nargs_cli.py Beer Wine Sake
 Beer Sake Wine
```

fire に与えたオブジェクトが持つメソッドはすべて呼び出せることは説明しましたが、この場合はコマンド引数とサブコマンド（メソッド）の区別をつけられません。こうしたときは、マイナス記号1つ( `-` ) でコマンドライン引数とサブコマンドを区切ります。


 zsh
```
 % python nargs_cli.py Beer Wine Sake - upper
 BEER SAKE WINE
```

区切り文字を変えたい場合、fire は  `--separator` オプションで与えます。
 zsh
```
 % python nargs_cli.py Beer Wine Sake @ upper -- --separator=@
 BEER SAKE WINE
```

この `--separator` のように、fire 自身が解釈するオプションがいくつかあります。コマンドラインでCLIアプリケーションのオプションや引数と区別するために、マイナス記号２つ( `--` ) で区切ると、それ以後は fire が解釈するオプションとなります。

## パラメタの型
typer はコマンドラインに与えられた型を推定することができます。

 check_type.py
```
 import fire
 fire.Fire(lambda obj: type(obj).__name__)
```

 zsh
```
 % python check_type.py 10
 int
 % python check_type.py 10.0
 float
 % python check_type.py hello
 str
 % python check_type.py '(1,2)'
 tuple
 % python check_type.py [1,2]
 list
 % python check_type.py True
 bool
 % python check_type.py {name:David}
 dict
```


### パラメタに文字列を使用するときの注意
コマンドラインをはじめにシェルがパースするために、
シングルクォートとダブルクォートを２重にする必要があります。

 zsh
```
 % python check_type.py 10
 int
 % python check_type.py "10"
 int
 % python check_type.py '"10"'
 str
 % python check_type.py "'10'"
 str
 % python check_type.py \"10\"
 str
```

### パラメタに辞書型のデータを使用するときの注意
パラメタに辞書を使用する場合はシェルを意識する必要があります。
 zsh
```
 % python check_type.py '{"name": "David Bieber"}'
 dict
 % python check_type.py {"name":'"David Bieber"'}
 dict
 % python check_type.py {"name":"David Bieber"}
 str
 % python check_type.py {"name": "David Bieber"}
 <error> # 複数のパラメタだとシェルが解釈してしまう
```

### パラメタにbool型のデータを使う
これまでの例で、パラメタにbool型を使うことができることは説明しました。
bool型では、その指示の方法には次のように複数の方法があります。

 zsh
```
 % python check_type.py --obj=True
 bool
 % python check_type.py --obj=False
 bool
 % python check_type.py --obj
 bool
 % python check_type.py --noobj
 bool
```


## 会話形モード:REPL
スクリプトを呼び出すとき  `--  --interactive` を与えると、
IPython のように会話形のRPELが起動します。
Fireは与えられたコンテキストで使用されているすべてのモジュールと変数を含むを、すぐに使用できるようになっているため、デバッグなどで便利です。

 zsh
```
 % python calculator_cli.py -- --interactive
 Fire is starting a Python REPL with the following objects:
 Modules: fire
 Objects: Calculator, calculator.py, component, result, trace


 Type 'copyright', 'credits' or 'license' for more information
 IPython 7.19.0 -- An enhanced Interactive Python. Type '?' for help.

 In [1]:
```


## プログラムをトレースする
Python プログラムがどうのように挙動しているか把握できるとデバッグが楽になります。こうしたときのために fire には  `--trace` オプションがあります。
前述の  `chain.py` をトレースしてみましょう。

 zsh
```
 % python chain.py move 3 3 on move 3 6 on move 6 3 on move 6 6 on move 7 4 on move 7 5 on -- --trace
```

次のような出力を生成します。
 zsh
```
 Fire trace:
 1. Initial component
 2. Instantiated class "BinaryCanvas" (chain.py:1)
 3. Accessed property "move" (chain.py:17)
 4. Called routine "move" (chain.py:17)
 5. Accessed property "on" (chain.py:22)
 6. Called routine "on" (chain.py:22)
 7. Accessed property "move" (chain.py:17)
 8. Called routine "move" (chain.py:17)
 9. Accessed property "on" (chain.py:22)
 10. Called routine "on" (chain.py:22)
 11. Accessed property "move" (chain.py:17)
 12. Called routine "move" (chain.py:17)
 13. Accessed property "on" (chain.py:22)
 14. Called routine "on" (chain.py:22)
 15. Accessed property "move" (chain.py:17)
 16. Called routine "move" (chain.py:17)
 17. Accessed property "on" (chain.py:22)
 18. Called routine "on" (chain.py:22)
 19. Accessed property "move" (chain.py:17)
 20. Called routine "move" (chain.py:17)
 21. Accessed property "on" (chain.py:22)
 22. Called routine "on" (chain.py:22)
 23. Accessed property "move" (chain.py:17)
 24. Called routine "move" (chain.py:17)
 25. Accessed property "on" (chain.py:22)
```

## 入力補完スクリプトの生成
fire に  `--completion` を与えると、Bashの入力補完スクリプトを生成します。
入力補完スクリプトをホームディレクトリに保存するには、次のようにします。

 bash
```
```
　$ python chain.py -- --completion > $HOME/._chain.py

このあと、このファイルを読み込んでおきます。
 bash
```
 $ source $HOME/._chain.py
```

ただし、対応しているシェルは Bash と Fish だけです。

参考:
- [Python-Fire オフィシャルサイト ](https://github.com/google/python-fire)

