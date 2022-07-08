タスクランナーInvokeを使ってみよう
=================

### Invoke について
invoke は予め登録しているタスクを実行することができるタスクランナーです。
CLIアプリケーションでのオプション解析、サブコマンドの実行、タスクの編成（前処理/後処理、順次実行)といったことが簡単にできるように設計されています。

### invoke のインストール
invoke は拡張モジュールなのでインストールする必要があります。
 pip
```
 $ pip install invoke
```

### 使用方法
invoke につづけてタスクを与えます。タスクは複数続けることができ、それぞれのタスクはパラメタを複数持つことができます。
invoke を短くした inv も使うことができます。
 zsh
```
 % inv [--core-opts] task1 [--task1-opts] ... taskN [--taskN-opts]
```

invoke は `tasks.py` に記述された関数を `@task` デコレータでタスクとして登録します。
 tasks.py
```
 from invoke import task
 
 @task
 def hello(c):
     """hello world."""
     print("Hello, world!")
```

この関数  `hello()` で定義している引数  `c` は `@task` でデコレートすることで、 `Context` クラスのインスタンスオブジェクトが与えられ、 `c.run()` のようにメソッドを呼び出すことで外部コマンドを実行することができます。
これについては後述していますので、今は難しく考えずに、こういう決まり事という理解でかまいません。

invoke が把握しているタスクは invoke のコアオプションのひとつ( `-l` )で知ることができます。
 zsh
```
 % invoke -l
 Available tasks:
 
   hello   hello world.
```

タスクが記述されたファイル `tasks.py` を、invoke ではコレクションと呼びます。
 `tasks.py` 以外のファイル名にしたいとき、例えば  `mytasks.py` にタスクを記述したいときは次のように実行します。

mytasks.py
```
 from invoke import task
 
 @task
 def greeting(c):
      """hello world."""
      print("Hello, world!")
```

 zsh
```
 % invoke -c mytasks -l
 Available tasks:
 
   greeting   hello world.
 
 % invoke --collection mytasks -l
 Available tasks:
 
   greeting   hello world.
```


### ヘルプメッセージ
特定のタスクのヘルプメッセージを表示するためには、次のようにコマンドを実行します。
 zsh
```
 % invoke --help hello
 Usage: inv[oke] [--core-opts] hello [other tasks here ...]
 
 Docstring:
   hello world.
 
 Options:
   none
 
 % invoke hello --help
 Usage: inv[oke] [--core-opts] hello [other tasks here ...]
 
 Docstring:
   hello world.
 
 Options:
   none
```

オプションｍ `--help` を与えて実行すると、タスクのdocstring と引数/フラグごとのヘルプ出力が表示されます。

### パラメタ
タスク  `hello` は実質的に引数がない（引数が `c` だけしか定義されていない）ため、パラメタを必要としないタスクとなります。
こうしたタスクの呼び出しは、次のように単純にタスク名を与えて実行するだけです。
 zsh
```
 % invoke hello
 Hello, world!
```

次のようにタスクとして登録している関数に引数  `name` があるときは、パラメタを受け取ることができます。

```
 from invoke import task
 
 @task
 def hello(c, name):
     """hello world."""
     print(f"Hello, {name}!")
```

 zsh
```
 % invoke --help hello
 Usage: inv[oke] [--core-opts] hello [--options] [other tasks here ...]
 
 Docstring:
   hello world.
 
 Options:
   -n STRING, --name=STRING
```

パラメタには次のような与え方ができます。
 zsh
```
 % invoke hello --name=Jack
 Hello, Jack!
 % invoke hello --name Jack
 Hello, Jack!
 % invoke hello -n=Jack
 Hello, Jack!
 % invoke hello -n Jack
 Hello, Jack!
 % invoke task2 -nJack
 Hello, Jack!
```


### タイプ
タスクとして登録した関数のデフォルト値を持つ引数は、invoke がタイプヒントを利用して型を変換して与えます。例えば、次のタスクがあるとします。

```
 from invoke import task
 
 @task()
 def task1(c, count=1):
     print(f'Your input number is {count}.　{type(count)}')
 
 @task()
 def task2(c, name=None):
     print(f'Hello {name}.　{type(name)}')
 
 @task()
 def task3(c, flag=False):
     print(f'Flag is {flag}.')
 
 @task()
 def task4(c, flag=True):
      print(f'Flag is {flag}.')
 
 @task()
 def task5(c, q=False, v=False):
      print(f'q: {q} v: {v}.')
```

コマンドラインの文字列から、関数 task1 には `str` 型の"5" ではなく、 `int` 型に変換された 5 が与えられます。
 zsh
```
 % invoke task1 --count=5
 Your input number is 5. <class 'int'>
 % invoke --help task1
 Usage: inv[oke] [--core-opts] task1 [--options] [other tasks here ...]
 
 Docstring:
   none
 
 Options:
   -c INT, --count=INT
```


関数 task2 では、デフォルト値がNoneであり、この場合デフォルト値を与えていないときと同じで、
そのまま  `str` 型の "Jack" が渡されます。

 zsh
```
 % invoke task2 --name=Jack
 Hello Jack. <class 'str'>
 % invoke --help task2
 Usage: inv[oke] [--core-opts] task2 [--options] [other tasks here ...]
 
 Docstring:
   none
 
 Options:
   -n STRING, --name=STRING
```

関数 task3 では、デフォルト値がブール値の `False` になっているため、オプションが与えられたときだけ  `True` となり、打ち消すための `--no-flag` は受け入れません。
 zsh
```
 % invoke task3
 Flag is False.
 
 % invoke task3 --flag
 Flag is True.
 
 % invoke task3 --no-flag
 No idea what '--no-flag' is!
```

 zsh
```
 % invoke task3 --help
 Usage: inv[oke] [--core-opts] task3 [--options] [other tasks here ...]
 
 Docstring:
   none
 
 Options:
   -f, --flag
```

関数 task4 では、デフォルト値がブール値の `True` になっているため、打ち消すための  `--no-flag` を受け入れます。
 zsh
```
 % invoke task4
 Flag is True.
 
 % invoke task4 --flag
 Flag is True.
 
 % invoke task4 --no-flag
 Flag is False.
```

 zsh
```
 % invoke task4 --help
 Usage: inv[oke] [--core-opts] task4 [--options] [other tasks here ...]
 
 Docstring:
   none
 
 Options:
   -f, --[no-]flag
```

関数 task5 では、デフォルト値がブール値の `False` になっている変数  `q` と  `v` があり、フラグオプション `-q` と  `-v` を受け入れます。
 zsh
```
 % invoke --help task5
 Usage: inv[oke] [--core-opts] task5 [--options] [other tasks here ...]
 
 Docstring:
   none
 
 Options:
   -q
   -v
```

このようなショートオプションの場合は、次のようなパラメタの与え方ができます。
 zsh
```
 % invoke task5 -qv
 q: True v: True.
 % invoke task5 -q -v
 q: True v: True.
```

### 複数の値をとるパラメタ
ひとつのパラメタがリストのように複数の値をもたせたいときがあります。
こうしたときは次のように `@task()` に  `iterable=['変数名']` を与えてタスクを登録します。


```
 from invoke import task
 
 @task(iterable=['my_list'])
 def mytask(c, my_list):
     print(my_list)
```

 zsh
```
 % invoke mytask -m=1 -m 2 --my-list 3
 ['1', '2', '3']
```

 zsh
```
 % invoke --help mytask
 Usage: inv[oke] [--core-opts] mytask [--options] [other tasks here ...]
 
 Docstring:
   none
 
 Options:
   -m, --my-list
```

アンダースコア( `_` ) がある変数は、オプション文字としてマイナス記号( `-` ) に置き換えられます。
ただし、 `_mylist` のように先頭のアンダースコアは無視されます。

### 同じオプションが指示された回数を知りたい
オプションを与えた回数に応じてレベルを変えたいなど、与えられたオプションの回数を知りたいときがあります。こうしたときは、次のように `@task()` に  `incrementable=['変数名']` を与えてタスクを登録します。

```
 from invoke import task
 
 @task(incrementable=['verbose'])
 def mytask(c, verbose=0):
     print(verbose)
```

 zsh
```
 % invoke mytask --verbose
 1
 % invoke mytask -v
 1
 % invoke mytask -vvv
 3
```

Pythonでは0は  `False` であり、1（その他のゼロ以外の数値）は  `True` となります。デフォルト値が0に設定されているときは、これはブールフラグのように機能します。
 `incremental` に指定されている変数のデフォルト値に与えた数値は、開始値として機能します。
変数の値が 0 でない限り、Python は常に  `True` として解釈することに留意してください。

既知のバグ：この場合、ヘルプメッセージにはオプションには、数値を与えることができるように表示されますが、実際にはうまく処理してくれません。
 zsh
```
 % invoke --help mytask
 Usage: inv[oke] [--core-opts] mytask [--options] [other tasks here ...]
 
 Docstring:
   none
 
 Options:
   -v INT, --verbose=INT
```

### タスクの編成
これまで説明してきたように、invoke は  `task.py` でデコレータ `@task()` が関数をタスクとして登録します。

次の例をみてみましょう。

```
 from invoke import task
 
 @task()
 def clean(c):
     print("Cleaning")
 
 @task
 def publish(c):
     print("Publishing")
 
 @task()
 def build(c):
     print("Building")
```

 zsh
```
 % invoke -l
 Available tasks:
 
   build
   clean
   publish
```

invoke はタスクとして、 `build` と `clean` 、 `publish` を提供しています。
invoke はコマンドラインに記述した順序で、タスクを実行します。
 zsh
```
 % invoke clean build publish
 Cleaning
 Building
 Publishing
```

単純な場合ではよいのですが、タスク数が多くなった場合では面倒になります。
invoke では、タスクを登録するときにタスクを編成して、前処理/後処理、順次処理などを実行させることができます。
次の例では、関数 `build` には `@task(pre=[clean], post=[publish])` と記述されています。
前処理( `pre=` ) に関数  `clean()` 、後処理( `post=` )に関数 `publish()` を呼び出すように編成しているわけです。

```
 from invoke import task
 
 @task()
 def clean(c):
     print("Cleaning")
 
 @task
 def publish(c):
     print("Publishing")
 
 @task(pre=[clean], post=[publish])
 def build(c):
     print("Building")
```

この場合、タスク `build` を実行するだけで、 `clean` と `publish` のタスクが実行されます。
zsh
```
 % invoke build
 Cleaning
 Building
 Publishing
```

 `pre=` と `post=` にはリストで複数のタスクを指定することができます。

次のように  `@task()` に直接タスクを指定したときは、 `pre=` に記述されたものとして動作します。

```
 from invoke import task
 
 @task
 def clean(c):
     print("Cleaning")
 
 @task
 def distclean(c):
     print("Dist Cleaning")
 
 @task(clean, distclean)
 def build(c):
     print("Building")
```

 zsh
```
 % invoke build
 Cleaning
 Dist Cleaning
 Building
```

タスクは次のように連続して呼び出すこともできます。

```
 from invoke import task
 
 @task
 def clean_obj(c):
     print("Cleaning Object files")
 
 @task
 def clean_tgz(c):
     print("Cleaning .tar.gz files")
 
 @task(clean_obj, clean_tgz)
 def clean(c):
     print("Cleaned everything")
 
 @task
 def makedirs(c):
     print("Making directories")
 
 @task(clean, makedirs)
 def build(c):
     print("Building")
 
 @task(build)
 def deploy(c):
     print("Deploying")
```


 zsh
```
 % invoke -l
 Available tasks:
 
   build
   clean
   clean-obj
   clean-tgz
   deploy
   makedirs
 
 % invoke deploy
 Cleaning Object files
 Cleaning .tar.gz files
 Cleaned everything
 Making directories
 Building
 Deploying
```

#### 前処理/後処理のタスクにパラメタを与えたい
デフォルトでは前処理/後処理のタスクはパラメタを取ることができませんが、 `call` を使用するとパラメタを与えることができます。

```
 from invoke import task, call
 
 @task
 def clean(c, which=None):
     which = which or 'pyc'
     print(f"Cleaning {which}")
 
 # @task(pre=[call(clean, which='all')])
 @task(call(clean, 'all'))
 def first_build(c):
     print("Fist Building")
 
 @task(post=[call(clean, which='all')])
 def build(c):
     print("Building")
```

前処理のときだけは、単に `@task(call(タスク, 引数))` とすることができます。
 zsh
```
 % invoke -l
 Available tasks:
 
   build
   clean
   first-build
 
 % invoke first-build
 Cleaning all
 Fist Building
 
 % invoke build
 Building
 Cleaning all
```

#### タスクの重複排除
デフォルトでは、事前/事後タスクに含まれているようなタスクは、セッション中に複数回実行されずに、重複排除(Deduplication)されて1回だけ実行されます。

 zsh
```
 
 % invoke build
 Cleaning
 Building
 
 % invoke package
 Cleaning
 Building
 Packaging
 
 % invoke build package
 Cleaning
 Building
 Packaging
```

パラメータを持つタスクが `call()` で呼び出される場合、引数リストに基づいて重複排除されます。
タスクが同じ引数で呼び出される場合は重複排除されますが、引数が異なる呼び出しでは重複排除されません。

重複排除させたくない場合は、invoke に オプション `--no-dedupe` を与えて実行します。
 zsh
```
 % invoke --no-dedupe build package
 Cleaning
 Building
 Cleaning
 Building
 Packaging
```

### 既存コードとの連携

既存コードをタスクとして利用したいときがあり、なるべく変更したくない場合があります。
例えば、次のような、関数 `hell()` を持つモジュール  `hello.py` があるときを考えてみましょう。
hello.py
```
 def hello(name="World"):
   return f"Hello {name}!"
```

このモジュール利用してをCLIアプリケーションとしたい場合は、次のようにラッパー関数を記述すると、既存コードを修正する必要はありません。

tasks.py
```
 from hello import hello
 from invoke import task
 
 @task(name='hello')
 def _hello(c, name):
     """Say hello to someone."""
     print(hello(name))
```

ここでのポイントは、 `@task(name='hello')` でタスク関数  `_hello()` を、タスク名  `hello` としている点です。
これにより既存コードのラッパーした関数を同じ名前のタスクとすることができます。
 zsh
```
 % invoke -l
 Available tasks:
 
   hello    Say Hello to someone.
```

タスクとして hello があることがわかるので、実行してみましょう。

 zsh
```
 % invoke hello
 Hello World!
 
 % invoke hello Jack
 Hello Jack!
```


### プログラムからinvoke を利用する
これまでの例では、 invoke コマンドを利用してコマンドラインからタスクを実行していました。
 `invoke.Program` クラスのインスタンスオブジェクトで `run()` を実行することで、スクリプトがinvoke の機能を持つようになり、毎回 invoke コマンドを実行する必要がなくなります。
まず、プロジェクトディレクトリを作成してみましょう。
 zsh
```
 % mkdir myapp
 % cd myapp
 % mkdir myapp
```

 `app.py` を次のように作成しましょう。
 myapp/app.py
```
 from invoke import Program
 
 __VERSION__='0.1.0'
 app = Program(version=__VERSION__)
 
 if __name__ == '__main__':
     app.run()
```

これで、 `myapp/app.py` が invoke と同じように動作します。
 zsh
```
 % python myapp/app.py --help
 Usage: app.py [--core-opts] task1 [--task1-opts] ... taskN [--taskN-opts]
 
 Core options:
 
   --complete                         Print tab-completion candidates for given
                                      parse remainder.
   --hide=STRING                      Set default value of run()'s 'hide' kwarg.
   --no-dedupe                        Disable task deduplication.
   --print-completion-script=STRING   Print the tab-completion script for your
                                      preferred shell (bash|zsh|fish).
   --prompt-for-sudo-password         Prompt user at start of session for the
                                      sudo.password config value.
   --write-pyc                        Enable creation of .pyc files.
   -c STRING, --collection=STRING     Specify collection name to load.
   -d, --debug                        Enable debug output.
   -D INT, --list-depth=INT           When listing tasks, only show the first
                                      INT levels.
   -e, --echo                         Echo executed commands before running.
   -f STRING, --config=STRING         Runtime configuration file to use.
   -F STRING, --list-format=STRING    Change the display format used when
                                      listing tasks. Should be one of: flat
                                      (default), nested, json.
   -h [STRING], --help[=STRING]       Show core or per-task help and exit.
   -l [STRING], --list[=STRING]       List available tasks, optionally limited
                                      to a namespace.
   -p, --pty                          Use a pty when executing shell commands.
   -r STRING, --search-root=STRING    Change root directory used for finding
                                      task modules.
   -R, --dry                          Echo commands instead of running.
   -T INT, --command-timeout=INT      Specify a global command execution
                                      timeout, in seconds.
   -V, --version                      Show version and exit.
   -w, --warn-only                    Warn, instead of failing, when shell
                                      commands fail.
```

#### サブコマンドを登録
次にサブコマンドとしてタスクを登録します。これには invoke コマンドのときと同様に  `tasks.py` に記述するか、後述する `namespace` でタスクを登録します。
 myapp/tasks.py
```
 from invoke import task
 
 @task()
 def hello(c, name="World"):
     print(f'Hello {name}.')
```

デフォルトでは `tasks.py` はコマンドを実行したディレクトリにあるものとして動作します。
 zsh
```
 % cd myapp
 % python app.py -l
 Available tasks:
 
   hello
 
 % python app.py hello
 Hello World.
```


### コマンドのインストール 
ここで、このスクリプトをパッケージとしてインストールしてみましょう。

まず、 `myapp/app.py` のファイル名を変更しましょう。
 zsh
```
 % mv myapp/app.py   myapp/__init__.py
```

次に、 `setup.py` を用意します。
 setup.pu
```
 from setuptools import setup, find_packages
 from myapp import __VERSION__
 
 with open("README.md", "r", encoding="utf-8") as fh:
     long_description = fh.read()
 
 setup(
     name="myapp",
     version=__VERSION__,
     author="Example Author",
     author_email="author@example.com",
     description="A small sample application",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="",
     packages=find_packages(),
     python_requires='>=3.6',
     entry_points={
         "console_scripts": [
             "myapp=myapp:app.run",
         ]
     },
 )
```

この `setup.py` でのポイントは、 `entry_points` の定義です。
この定義により、コンソールスクリプト（つまりコマンド `myapp` ）は、モジュール `myapp` の `app.run()` を実行するということを表していてます。

#### コマンドをインストール
 `setup.py` があるディレクトリで次のコマンドを実行します。
モジュール `myapp` は実行されるpython の  `site-derectory` にコピーされます。
 zsh
```
 % python3 -m pip install  --upgrade .
```

システムへのインストールする権限がない場合は、オプション `--user` を与えると、
ユーザ領域にインストールされます。
- Linux系:  `$HOME/.local/bin` 

モジュール `myapp` を修正することがあれば、再度インストールする必要があります。

修正可能な状態でインストールするときは次のように、オプション `--editable` を与えて実行します。
この場合は、モジュール `myapp` はコピーされずに、このディレクトリの場所を示すファイルがインストールされるため、修正した内容がそのまま利用されるので、都度再インストールする必要がありません。
 zsh
```
 % python -m pip install　--editable .
```

 zsh
```
 % myapp --version
 Myapp 0.1.0
```


### タスクを登録する
ひとつのタスクモジュールを読み込む場合は、基本的なケースでは問題なく機能します。
しかし、タスクをネストされた名前空間のツリーに分割するなどでは、別の方法が必要になります。

 `invoke.Collection` クラスは、タスク（およびその構成）をツリーのような構造に編成するためのAPIを提供します。 コマンドラインから文字列によってタスクが参照される場合、ネストされた名前空間のタスクは、ドット（ `.` )で区切って指示します。(例： `myapp.build` )

名前のない `Collection` の1つには、名前空間(namespace) のルートがあります。 デフォルトでは、 `tasks.py` にあるタスクから生成されます。 `Collection` クラスから独自のインスタンオブジェクト `ns` を作成して、明示的な名前空間を設定します。
これにより、 `tasks.py` のタスクは読み込みこまなくなります。

 myapp/__init__.py
```
 from invoke import Program, Collection, task
 
 __VERSION__='0.1.0'
 
 @task
 def greeting(c, name="World"):
    print(f'Hello {name}')
 
 ns = Collection()
 ns.add_task(greeting)
 
 app = Program(version=__VERSION__, namespace=ns)
 
 if __name__ == '__main__':
     app.run()
```

 zsh
```
 % myapp -l
 Subcommands:
 
   greeting
```

これまでに例示してきたような `tasks.py` がなくてもファイルひとつでタスクを実行することができようになりました。
タスクが多くなってきたり、名前空間がネストするような場合では、ファイルを分割する方が柔軟性が高くなります。
そこで、次のようなファイル構成にしてみます。

 myapp/tasks.py
```
 from invoke import Collection, task
 
 @task
 def greeting_message(c, name="World"):
     print(f'Hello {name}')
 
 ns = Collection()
 ns.add_task(greeting_message, name='greeting')
```
キーワード引数 `name=` および第２引数はタスクの名前を与えます。関数名と同じ場合は省略することができます。

 myapp/__init__.py
```
 from invoke import Program
 from .tasks import ns
 
 __VERSION__='0.1.0'
  app = Program(version=__VERSION__, namespace=ns)
 
 if __name__ == '__main__':
     app.run()
```

この例では、 `tasks.py` のままですが、モジュール名は自由に変更することができます。

### タスクをネストさせる
タスクが多くなってきたりすると、機能ごとにファイルを分割したくなります。
例えば、タスク  `drinks_tasks.py` を作ることを考えてみましょう。
 drinks_tasks.py
```
 from invoke import Collection, task
 
 @task(default=True)
 def beer_lover(c):
   print("I love Beer")
 
 @task
 def wine_lover(c):
   print("I love Wine")
 
 @task
 def sake_lover(c):
   print("I love Sake")
 
 drinks_ns = Collection('drinks')
 drinks_ns.add_task(beer_lover, 'beer')
 drinks_ns.add_task(wine_lover, 'wine')
 drinks_ns.add_task(sake_lover, 'sake')
```

これを前述の myapp に組み込んでみます。

 myapp/__init__.py
```
 from invoke import Program
 from .tasks import ns
 from .drinks_tasks import drinks_ns
  
 __VERSION__='0.1.0'
 
 ns.add_collection(math_ns)
 app = Program(version=__VERSION__, namespace=ns)
 
 if __name__ == '__main__':
     app.run()
```

ここでのポイントは名前空間 `drinks_ns` を生成するときコレクション名 `drinks` を明示的に与えていることです。追加する名前空間には名前つけて生成する必要があります。
また、タスク関数の名前は `@task()` だけでなく、 `add_task()` でも与えることができます。
 `@task()` で `default=True` を与えたタスクが、デフォルトになります。

 zsh 
```
 % myapp -l
 Subcommands:
 
   greeting
   drinks.beer (drinks)
   drinks.sake
   drinks.wine
 
 % myapp greeting --help
 Usage: myapp [--core-opts] greeting [--options] [other tasks here ...]
 
 Docstring:
   none
 
 Options:
   -n STRING, --name=STRING
 
 % myapp greeting
 Hello World
 % myapp greeting --name=Jack
 Hello Jack
 % myapp drinks
 I love Beer
 % myapp drinks.wine
 I love Wine
```

### タスクをモジュールとして読み込み
このままでもよいのですが、 `tasks.py` と  `drinks_tasks.py` には、名前空間(namespace)の定義があります。これらのファイルにはタスクに関係するものだけを記述する方がスッキリします。

 myapp/tasks.py
```
 from invoke import task
  
 @task
 def greeting_message(c, name="World"):
     print(f'Hello {name}') 
```

myapp/drinks.py
```
 from invoke import task
 
 @task(default=True)
 def beer_lover(c):
   print("I love Beer")
 
 @task
 def wine_lover(c):
   print("I love Wine")
 
 @task
 def sake_lover(c):
   print("I love Sake")
```

 myapp/__init__py
```
 from invoke import Program, Collection
 import myapp.tasks, myapp.drinks
  
 __VERSION__='0.1.0'
 
 ns = Collection()
 # ns.add_collection(Collection.from_module(tasks))
 ns.add_collection(tasks)
 # ns.add_collection(Collection.from_module(drinks))
 ns.add_collection(drinks)
 app = Program(version=__VERSION__, namespace=ns)
 
 if __name__ == '__main__':
     app.run()
```

 zsh
```
 % myapp -l
 Subcommands:
 
   drinks.beer-lover (drinks)
   drinks.sake-lover
   drinks.wine-lover
   tasks.greeting
   tasks.run
```

この例にあるように、 `add_collection(Collection.from_module(モジュール名))` は、
 `add_collection(モジュール名)` 　とすることができます。

実はもっと簡単にすることもできます。
 myapp/__init__.py
```
 from invoke import Program, Collection
 import myapp.tasks, myapp.drinks
 
 __VERSION__='0.1.0'
 
 ns = Collection(tasks, drinks) 
 app = Program(version=__VERSION__, namespace=ns)
 
 if __name__ == '__main__':
     app.run()
```

### コンテキスト
タスク関数に与える第１引数はコンテキスト( `Context` )オブジェクトがセットされます。

```
 from invoke import task
 
 @task
 def hello(c, name="World"):
     print(f'Hello {name}')
```

コンテキストオブジェクト(この例では `c` )で提供されるAPIメソッドについて説明することにします。
代表的なものについて説明しています。

### run() 
 `c.run()` は、引数に与えた文字列をコマンドラインとして実行します。
-  `hide=stderr` ：標準エラー出力の出力を抑制する
-  `hide=stdout` ：標準出力を出力を抑制する
-  `hide=both` 、 `hide=True` ：標準出力と標準エラー出力の出力を抑制す
-  `warn=True` ：コマンドのエラーを出力する
 `Result` オブジェクトを返します。
-  `ok` : 実行したコマンドが正常に終了していれば  `True` がセットされる
-  `stdout` ：標準出力の内容が格納される
-  `stderr` ：標準エラー出力の内容が格納される


```
 @task()
 def cmd_executor(c, cmd=""):
    result = c.run(cmd, hide=True, warn=True)
    if result.ok:
        print(result.stdout.splitlines()[-1])
    else:
        print(result.stderr.splitlines()[-1])
```



### sudo()
 `c.sudo()` は、引数に与えた文字列をコマンドラインとして、sudo コマンドで管理者権限で実行します。

### prefix()
ネストされたすべての `c.run()` および `c.sudo()` で処理するコマンドの前に、引数で与えたコマンドと `&&` を付けます。
 `&&` の意味は、 `c.prefix()` の引数に与えた文字列をコマンドとして実行して、その結果が正常であるときに(つまり、終了コードがゼロ）のときに、続くコマンドが実行されます。
ほとんどの場合、シェル環境変数をエクスポートまたは変更するものなど、シェルの状態を変更するシェルスクリプトと一緒にこれを使用することをお勧めします。

最も一般的な使用法の1つは、virtualenvwrapperからのworkonコマンドを使用することです。

```
 with c.prefix('workon myvenv'):
     c.run('./manage.py migrate')
```

このコードはシェルのコマンドラインで次のように実行することと同じです。
 bash
```
 $ workon myvenv && ./manage.py migrate
```

また、特定の環境変数を設定してコマンドを実行したいようなときにも使用することができます。
例えば、構成設定ツール Anasible で実行時のカラー表示をさせたくないときは、
次のようにすることができます。

```
 from invoke import task
 
 _cmd_base = "ansible-playbook -i hosts/staging -K "
 
 @task
 def build_openmpi(c):
     with c.prefix('export ANSIBLE_NOCOLOR=1'):
         cmd = _cmd_base + "build_openmpi.yaml"
         c.run(cmd)
```

ただし、このようなタスクが多数あるのであれば、Python 標準ライブラリのsubprocess モジュールを使用する方がスッキリ記述できます。

```
 from invoke import task
 import subprocess
 
 myenv = dict(os.environ, ANSIBLE_NOCOLOR="1")
 @task
 def build_openmpi(c):
     cmd = _cmd_base + "build-openmpi.yml"
     subprocess.call( cmd.split(), env=myenv)
```


### cwd()
 `c.cwd()` は現在のディレクトリを取得します。

### cd()
 `c.cd()` は与えたパスにカレントディレクトリを移動します。
 `c.run()` のコマンドラインとしてcdコマンドを実行することができますが、このセッションが終わると元のディレクトリに戻ってしまいます。


```
 # c.run("cd /var/www && ls") と同じ
 with c.cd('/var/www/html'):
      c.run('ls') 
```

### MockContext
 `MockContext` はテストを行うためのクラスです。 `Context` オブジェクトとそのメソッドは、 `MockContext` クラスのインスタンスオブジェクトを介して提供されます。
これにより、テストを簡単に行うことができます。

たとえば、次のタスクを実行があるとします。

```
 from invoke import task
 
 @task
 def show_platform(c):
     uname = c.run("uname -s").stdout.strip()
     if uname == 'Darwin':
         print("You paid the Apple tax!")
     elif uname == 'Linux':
         print("Year of Linux on the desktop!")
```

このタスクをテストするためのタスクは次のようになります。

```
 import sys
 from spec import trap
 from invoke import MockContext, Result
 from mytasks import show_platform
 
 @trap
 def test_show_platform_on_mac():
     c = MockContext(run=Result("Darwin\n"))
     show_platform(c)
     assert "Apple" in sys.stdout.getvalue()
 
 @trap
 def test_show_platform_on_linux():
     c = MockContext(run=Result("Linux\n"))
     show_platform(c)
     assert "desktop" in sys
```

テストの結果判定に必要なものが標準出力のみという場合では、
 `MockContext` を使用する必要もありません。

 mytasks.py
```
 from invoke import task
 
 @task
 def show_platform(c):
     print(platform_response(c.run("uname -s")))
 
 def platform_response(result):
     uname = result.stdout.strip()
     if uname == 'Darwin':
         return "You paid the Apple tax!"
     elif uname == 'Linux':
         return "Year of Linux on the desktop!"
```


```
 from invoke import Result
 from mytasks import platform_response
 
 def test_platform_response_on_mac():
     assert "Apple" in platform_response(Result("Darwin\n"))
 
 def test_platform_response_on_linux():
     assert "desktop" in platform_response(Result("Linux\n"))
 
```

### タスクに自動応答させる
コマンドを実行するとき、応答を求められる場合があります。
こうしたときは、 `Responder` クラスを使用すると、パターンを監視して、合致する場合には応答を返すことができます。

いま、例示のために次のシェルスクリプトを用意します。
 AreYouReady.sh
```
 #!/bin/bash
 
 echo -n  "Are you ready? [Y/n] " ; read ans
 case ${ans} in
 n|N)    ;;
 y|Y|*)  echo "OK. bye-bye." ;;
 esac
```

これに自動応答させるタスクは次のようになります。


```
 from invoke import task, Responder, CommandTimedOut
 
 @task
 def always_ready(c):
     responder = Responder(
         pattern=r"Are you ready\? \[Y/n\] ",
         response="y\n",
     )
     try:
         c.run("./AreYouReady.sh", watchers=[responder], timeout=5)
     except CommandTimedOut:
         pass
```

### リモートホストでタスクを実行する
invoke はログインしているノードでタスクを実行するものです。場合よっては他ノードで実行させたいときがあります。そうした場合は、関連プロジェクトの Fabric2 を使うと便利です。
Fabric2 は invoke を SSHライブラリを使用するようにラッパーした拡張モジュールです。

Fabric は拡張モジュールなのでインストールする必要があります。
 pip
```
 $ pip install fabric2
```

### Invoke と Fabric2の違い
Invoke と Fabric2 の最大の違いは、対象ホストがリモートかローカルかではなくて、SSHを経由してタスクを実行するかどうでかです。
ローカルノードであってもSSHを経由してタスクを実行することもありえます。
SSHを経由しない場合では、基本的にはタスクのすべての処理を invoke で完結させることができます。
Invoke では `Conetex` tオブジェクトを使用して、 `run()` APIでタスクを実行します。

pyton
```
  from invoke import task
 
  @task
  def do_something(c):
      with c.cd("/path/to/somewhere"):
          c.run("ls")
```

Fabric2 では、多くの場合対象ホストへの接続を行う `Connection` オブジェクトを生成したうえで、 `run()` APIでタスクを実行します。

python
```
  from fabric.connection import Connection
 
  connection = Connection("username@remote_host")
  print(connection.run("ls"))
```

### Fabric2 から Invoke のタスクを利用する
不思議なことにドキュメントには明示されていないのですが、
invoke の `Context` オブジェクトとして `Connetion` オブジェクトを渡すことができます。


```
 from fabric2 import Connection
 from invoke import Collection, task
 
 @task()
 def greeting_message(c, name="World"):
     print(f'Hello {name}')
 
 @task()
 def cmd_executor(c, cmd=""):
     result = c.run(cmd, hide=True, warn=True)
     if result.ok:
         print(result.stdout.splitlines()[-1])
     else:
         print(result.stderr.splitlines()[-1])
 
 @task
 def remote_task(c, cmd=""):
     con = Connection("webapp@web")
     print(cmd_executor(con, cmd))
 
 ns = Collection()
 ns.add_task(greeting_message, name='greeting')
 ns.add_task(cmd_executor, name='run')
 ns.add_task(remote_task, name='remote')
```

### 構成ファイル
Invokeでは、構成ファイル、環境変数、タスク名前空間、およびコマンドラインのオプションを通して Inovkeのコアな動作、およびタスク動作を構成することができます。
構成ファイル読み込みや解析、およびマージした最終結果は、ネストされたPython辞書のように動作する `Config` オブジェクトとして保持されます。 Invokeは、実行時にこのオブジェクトを参照し、 `Context.run()` などのメソッドのデフォルトの動作を決定します。

### 構成の階層構造
構成が読み込まれる順序は次の通りです。

- 構成により制御可能な動作の内部デフォルト値。
- Collection.configureを介してタスクモジュールで定義されたコレクション駆動型構成。 
- サブコレクションの構成は最上位のコレクションにマージされ、最終結果が全体的な構成設定となります。
- ルートコレクションは実行時にロードされるため、このレベルで定義されている場合、ロード処理自体を変更する構成設定は有効になりません。
-  `/etc` 以下のシステムレベルの構成ファイル。（例： `/etc/invoke.yaml` など）
- ユーザーレベルの構成ファイル。（例：`~/.invoke.yaml)
- トップレベルの `tasks.py` の隣にあるプロジェクトレベルの構成ファイル。
たとえば、Invokeの実行で `/home/user/myproject/tasks.py` が読み込まれる場合、プロジェクトレベルの構成ファイルは `/home/user/myproject/invoke.yaml` です。
- 呼び出し元のシェル環境で見つかった環境変数。（例： `INVOKE_*` )
- invコマンド実行時に `-f` で与えた構成ファイル。
(例： `inv -f /path/to/config.yml` )
- invのコマンドラインで与えた特定のコア設定のオプション（例： `-e` )

### デフォルトの構成値
Invoke で使用できる構成値には次のものがあります。
ネストされた設定名はドット構文で参照します。つまり、  `foo.bar` は、Pythonで `{'foo'：{'bar'：<値>}}` となるものを参照します。通常、これらは、アトリビュートとして `Config` オブジェクトと `Context` オブジェクトで読み取りや設定することができます。（例： `ctx.foo.bar` )

 `tasks` 構成ツリーには、タスクの実行に関連する設定が含まれています。

 `tasks.dedupe` は、タスクの重複排除を制御し、デフォルトは `True` です。コマンドラインで  `--no-dedupe` を使用して、実行時に上書きすることもできます。
 `run` 構成ツリーは、 `Runner.run` の動作を制御します。このツリーの各メンバー（ `run.echo` や `run.pty` など）は、同じ名前の `Runner.run` キーワード引数に直接マップされます。

トップレベルの構成設定である `debug` は、デバッグレベルの出力をログに記録するかどうかを制御し、デフォルトは `False` です。
 `debug` は、コマンドライン解析の実行後にデバッグを有効にする `-d` オプションで切り替えることができます。また、環境変数 `INVOKE_DEBUG` で切り替えることもできます。

## 構成ファイル
### 構成ファイルの読み込み
前述の構成ファイルの場所ごとに、 `.yaml` 、 `.json` 、または `.py` で終わるファイルを、この順序で検索し、最初に見つかったファイルを読み込みます。他のファイルを無視されます。

たとえば、 `/etc/invoke.yaml` と `/etc/invoke.json` の両方を含むシステムでは、Invokeを実行すると、YAMLファイルのみが読み込まれることに注意してください。

### 構成ファイルのフォーマット
Invokeでは構成ファイルで任意のネストが可能です。
以下の3つの例はすべて、 `{'debug'：True、 'run'：{'echo'：True}}` と同じです。

 YAML
```
 debug: true
 run:
     echo: true
```

 json
```
 {
     "debug": true,
     "run": {
         "echo": true
     }
 }
```


```
 debug = True
 run = {
     "echo": True
 }
```


### 環境変数で設定
環境変数とは、OSがプロセスを起動する際に、親プロセスから子プロセスへ 引き渡される文字列で設定する変数です。環境変数には、値をネストする簡単な方法がなく、また実行するシェルで呼び出されるすべてのコマンドで共有されるため、少し違った設定方法となります。
環境変数 `FOOBAR` をInvokeに与えたい場合は、最初に構成ファイルまたはタスクコレクションで `foobar` の設定を宣言する必要があることに注意してください。

#### 基本的なルール
invoke のタスク関数に渡したい環境変数は、その変数名の前に  `INVOKE_` つけて定義します。
環境変数名をアンダースコア( `_` )で区切ると、環境変数をネストすることができます。
例えば、Python での辞書型のデータ `{'run: {'echo': True}}` は、
 `INVOKE_RUN_ECHO=1` と定義することができます。

#### 型のキャスト
環境変数は既存の構成値をオーバーライドするためだけに使用することができます。
構成値が文字列またはUnicodeオブジェクトの場合、キャストは行われずに環境変数で設定した値がそのままセットされます。
インタプリタと環境によっては、これは、デフォルトで非Unicode文字列型（例：Python 2のstrなど）に設定された変数の値がUnicode文字列に置き換えられてしまう可能性があります。キャストが行われないことで、非Unicode文字列の値が置き換わることを防ぐための、意図的な仕様です。

構成値が `None` の場合、環境変数からの文字列に置き換えられます。

ブール値は次のように設定されます：
 `0` および空の値や文字列（例： `SETTING =''` 、または `unset SETTING` など）は `False` と評価され、その他の値は `True` と評価されます。

リストとタプルは現在サポートされていないため、例外が発生します。

他のすべてのタイプ（ `in` 、 `long` 、 `float` など）は、入力値のコンストラクターとして使用されます。

たとえば、構成値のデフォルト値が整数1である `foobar` の変数は、 `int()` で設定がされます。つまり、 `FOOBAR=5` は文字列 `5` ではなく、Pythonの `int` 型の5となります。

#### ネストと下線付きの名前
環境変数名は単一の文字列のため、ネストされた構成設定にアクセスできるようにするには、アンダースコア（ `_` )を環境変数名に使用することができます。
前述の　 `INVOKE_RUN_ECHO=1` のような場合です。
ただし、設定名自体にアンダースコアが含まれていると、あいまいさが生じてしまいます。 `INVOKE_FOO_BAR=baz` を考えてみましょう。
これは、 `{'foo':{'bar':'baz'}}` 、 `{'foo_bar':'baz'}` のどちらでしょうか？
構成値はPythonレベルまたは構成ファイルで宣言された設定を変更するためだけに使用できるため、構成の現在の状態を調べて判断してくれます。

それでも、両方の解釈が可能な場合がまだあります。
（例： `{'foo':{'bar':'default'},  'foo_bar': 'otherdefault'}` ）
この場合は、invoke は推測を拒否してエラーが発生します。代わりに、構成レイアウトを変更するか、構成設定に環境変数を使用しないようにしてください。

## コレクションベースの構成
 `Collection` オブジェクトには、 `Collection.configure` を介して設定される場合があり、これは通常、最下位レベルの構成設定となります。
 `Collection` がネストされている場合、構成はデフォルトで下位方向にマージされます。競合が発生すると、呼び出されているタスクに近い内側の名前空間ではなく、ルートに近い外側の名前空間が優先されます。

```
 from invoke import Collection, task
 
 # このタスクとコレクションは、どこかの別のモジュールから簡単に取得でる
 @task
 def mytask(ctx):
     print(ctx['conflicted'])
     
 inner = Collection('inner', mytask)
 inner.configure({'conflicted': 'default value'})
 
 # プロジェクトのルート名前空間
 ns = Collection(inner)
 ns.configure({'conflicted': 'override value'})
```

 `inner.mytask` を呼び出す
  bash
```
 $ inv inner.mytask
 override value
```


## 構成ファイルの例
まず、値をハードコーディングした現実的でないタスクからはじめて、さまざまな構成メカニズムを使用するようにしてゆきましょう。 
例えば、Sphinxドキュメントをビルドするためのタスクモジュールは次のようになるかもしれません。

```
 from invoke import task
 
 @task
 def clean(ctx):
     ctx.run("rm -rf docs/_build")
 
 @task
 def build(ctx):
     ctx.run("sphinx-build docs docs/_build")
```

 `build` タスクでビルド対象を `target` で与えるようにしてみます。

```
 from invoke import task
 
 target = "docs/_build"
 
 @task
 def clean(ctx):
     ctx.run("rm -rf {0}".format(target))
 
 @task
 def build(ctx):
     ctx.run("sphinx-build docs {0}".format(target))
```

これを実行時にパラメタで与えられるようにしてみます。

```
 from invoke import task
 
 default_target = "docs/_build"
 
 @task
 def clean(ctx, target=default_target):
     ctx.run("rm -rf {0}".format(target))
 
 @task
 def build(ctx, target=default_target):
     ctx.run("sphinx-build docs {0}".format(target))
```

このタスクモジュールは対象がひとつだけで機能しますが、再利用をするために、このモジュールを別のデフォルトターゲットで使用できるようにしたい場合は、コンテキストを使用して構成を設定するようにします。

## コンテキストへの切り替え
構成設定とAPIの取得により、ハードコードされたデフォルト値を、ユーザーが自由に再定義できるように簡単に変更することできます。 


```
 from invoke import Collection, task
 
 default_target = "docs/_build"
 
 @task
 def clean(ctx, target=default_target):
     ctx.run("rm -rf {0}".format(target))
 
 @task
 def build(ctx, target=default_target):
     ctx.run("sphinx-build docs {0}".format(target))
 
 ns = Collection(clean, build)
```

次に、デフォルトの `default_target` 値をコレクションのデフォルト構成に移動し、コンテキストを介して参照できます。  `target` のデフォルト値を `None` に変更して、ランタイム値が指定されているかどうかを判断できるようにします。

```
 @task
 def clean(ctx, target=None):
     ctx.run("rm -rf {0}".format(target or ctx.sphinx.target))
 
 @task
 def build(ctx, target=None):
     ctx.run("sphinx-build docs {0}".format(
                                        target or ctx.sphinx.target))
 
 ns = Collection(clean, build)
 ns.configure({'sphinx': {'target': "docs/_build"}})
```


## 構成のオーバーライド
ユーザーがさまざまな方法でデフォルト値をオーバーライドすることができます。
もちろん、最下位レベルのオーバーライドは、配布されたモジュールがインポートされたローカルコレクションツリーを変更するだけです。 例えば、前述のタスクモジュールが `myproject.docs` として配布されている場合、次のように `tasks.py` を定義できます。


```
 from invoke import Collection, task
 from myproject import docs
 
 @task
 def mylocaltask(ctx):
     # 何かを行うローカルタスク
     pass
 
 # ローカルのルート名前空間にdocsを追加し、さらに独自のタスクを追加
 ns = Collection(mylocaltask, docs)
```

こうしておくと、最後に次の行を追加するだけです。

```
 ns.configure({'sphinx': {'target': "built_docs"}}) 
```

これで、 `default_target` が `docs/_build` ではなく `built_docs` にデフォルト設定されている `docs` サブ名前空間ができます。

Python で名前空間を設定するより、構成ファイルで行いたい場合は、上記の追加した行の代わりに、 `tasks.py` と同じディレクトリに `invoke.yaml` という名前のあるファイルを配置するだけです。
 invoke.yaml
```
 sphinx:
     target: built_docs
```


## 参考
- [invoke オフィシャルサイト http://www.pyinvoke.org/]
- [fabric オフィシャルサイト http://www.fabfile.org/]
- [Python Packaging User Guide ](https://packaging.python.org/)

#タスクランナー


