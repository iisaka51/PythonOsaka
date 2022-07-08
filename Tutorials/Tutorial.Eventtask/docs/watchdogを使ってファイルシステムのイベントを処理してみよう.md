watchdogを使ってファイルシステムのイベントを処理してみよう
=================
## はじめに
このチュートリアルでは、Python によるファイルシステムのイベントを監視することを学習します。

## watchdog について
[watchdog](https://github.com/gorakhargosh/watchdog]) は、Python で実装されたライ>ブラリで、ファイルシステムを監視してファイルが更新されたなどのイベントを
トリガーとして処理を行うことができます。

Python標準ライブラリの[select](https://docs.python.org/3.9/library/select.html) や、[Minotaur](https://github.com/giannitedesco/minotaur]) など類似のライブラリはいくつかありますが、これらは Linux に依存した実装方法なのに対して、watchdog は windows, macOS, Linux などのプラットフォームでも動作します。

### インストール
watchdog は pip でインストールすることができます。

```
 $ pip install watchdog
```

### 使用例
座学でwatchdog の API を説明するよりも、まず、実際のコードをお見せして、どのように使うのかを説明することにしましょう。

 import time
 from watchdog.observers import Observer
 from watchdog.events import FileSystemEventHandler

 class MyWatcher:

     def __init__(self, directory=".", handler=FileSystemEventHandler()):
         self.observer = Observer()
         self.handler = handler
         self.directory = directory

     def run(self):
         self.observer.schedule(self.handler, self.directory, recursive=True)
         self.observer.start()
         print(f"MyWatcher Running in {self.directory}")
         try:
             while True:
                 time.sleep(1)
         except:
             self.observer.stop()
         self.observer.join()
         print("\nMyWatcher Terminated\n")


 class MyHandler(FileSystemEventHandler):

     def on_any_event(self, event):
         print(event)   # Your code here

 if __name__=="__main__":
     w = MyWatcher(".", MyHandler())
     w.run()

```

このコードはディレクトリ/フォルダーを監視し、ファイルに変更があったときに何かの処理をするためのスニペットです。

次のような応用例が考えられるでしょう。

- 装着されたUSBメモリに格納されているMP3ファイルを自動再生
- ソースコードの変更を監視して、保存時にWebサイトを再構築する

watchdog では、Watcher と Handler の2つのクラスを定義します。

-         `Watcher`       オブジェクトは指定したディレクトリを監視する
-         `Handler`       オブジェクトは `Watcher`オブジェクトのイベントに応答して何らかの処理を行う

それぞれについて説明してゆきます。

### Watcher クラス

        `Watcher`       クラスの初期化では、監視するディレクトリをイベントを登録しますが、
実際には watchdog の         `Observer`       オブジェクトがほとんどの処理を行っています。

```
 class MyWatcher:

     def __init__(self, directory=".", handler=FileSystemEventHandler()):
             self.observer = Observer()
             self.handler = handler
             self.directory = directory

```

        `run()`       メソッドは、 `Observer`オブジェクト(`self.observer`)の設定を行います。
Observerをスレッドで起動し、プログラムが終了するまでスリープしま、その後にObserverを終了して(Stop/Join)、クリーンアップを行います。

 pytho
```
     def run(self):
         self.observer.schedule(self.handler, self.directory, recursive=True)
         self.observer.start()
         print(f"MyWatcher Running in {self.directory}")
         try:
             while True:
                 time.sleep(1)
         except:
             self.observer.stop()
         self.observer.join()
         print("\nMyWatcher Terminated\n")

```


### Handler クラス
 Handlerクラスにイベントに応答する処理を記述します。先のスニペットでは、       `FileSystemEventHandler`       クラスを派生した  `MyHandler`クラスを定義しています。

```
 class MyHandler(FileSystemEventHandler):

     def on_any_event(self, event):
         print(event) # ここに何かの処理を追加する

```

        `on_any_event()`         は `FileSystemEventHandler` によって定義されたイベントが発生したときに呼び出されるメソッドです。

## Observerクラス
 実際に監視を行うのはObserverオブジェクトです。Observerオブジェクトには、       `scheduler()`       メソッドが提供されていて、
次のような引数を渡すことができます。

        `schedule(self, event_handler, path, recursive=False)`
  -         `event_handler`       ：定義したHandlerクラスのオブジェクト
  -         `path`       ：　監視対象のディレクトリパス
  -         `recursive`       ： `True`を与えるとサブディレクトリも監視する。デフォルトは`False`

Observerオブジェクトには、実行を制御するメソッが提供されています。

  -         `start()`       ：  スレッドを生成してオブジェクトの`run()`メソッドを実行する
  -         `stop()`       ：スレッドを停止するシグナルを送信する
  -         `join()`       ：スレッドの終了を待つ

        `start()`       メソッドは、スレッドオブジェクトごとに一度だけ呼びだす必要があり、同じスレッドオブジェクトで複数回呼び出されると `RuntimeError` を発生させます。
これらの挙動を深く知りたい場合は、「[スレッドベースの並列処理]」を参照してみてください。

## Watcherの起動
 Watcherを起動するためには、定義している       `NyWatcher`       クラスに、監視するディレクトリと `MyHandler`で定義したHandlerを渡してオブジェクトを生成して、`run()`メソッドを呼び出すだけです。

```
 if __name__=="__main__":
     w = MyWatcher(".", MyHandler())
     w.run()

```

## 実行して確認してみよう
次からの例示のためにスニペットの Watcher の定義の         `c002_watcher.py`         として保存しておきます。

 c002_watcher.py
```py
 import time
 from watchdog.observers import Observer
 from watchdog.events import FileSystemEventHandler

 class MyWatcher:

     def __init__(self, directory=".", handler=FileSystemEventHandler()):
         self.observer = Observer()
         self.handler = handler
         self.directory = directory

     def run(self):
         self.observer.schedule(
             self.handler, self.directory, recursive=True)
         self.observer.start()
         print("\nWatcher Running in {}/\n".format(self.directory))
         try:
             while True:
                 time.sleep(1)
         except:
             self.observer.stop()
         self.observer.join()
         print("\nWatcher Terminated\n")

```

## watchdog の API - FileSystemEventHandler
watchdog には非常に多くの機能がありますが、先のスニペットでは         `FileSystemEvent`       クラスを継承したものだけなので、
 ここでは、       `FileSystemEventHandler`         クラスのAPIについて説明することにします。

        `FileSystemEventHandler`         クラスにはイベントに応じて呼び出されるメソッドがあり、対応する event を受け取ります。

-         `on_any_event(self, event)`         - `FileSystemEvent`
-         `on_closed(self, event)`          -  `FileClosedEvent`
-         `on_created(self, event)`          -  `FileCreatedEvent`
-         `on_deleted(self, event)`          - `DirDeletedEvent` もしくは `FileDeletedEvent`
-         `on_modified(self, event)`          - `DirModifiedEvent` もしくは `FileModifiedEvent`
-         `on_moved(self, event)`         - `DirMovedEvent` もしくは `FileMovedEvent`

詳細を知りたいときは、 [watchdog のドキュメント](https://python-watchdog.readthedocs.io/en/stable/]) を参照してください。


## FileSystemEvent オブジェクトのアトリビュート
FileSystemEvent オブジェクトには、つぎのアトリビュートがセットされます。

  -         `event.event_type`
  -         `event.src_path`
  -         `event.is_directory`
  -         `event.is_synthetic`

#### event_type
event_type は次のいずれかのイベントを示す文字列がセットされます。

```
 types = ['created', 'deleted', 'modified', 'moved', 'closed']
```

```
 In [2]: # %load c003_filedeleted.py
    ...: from c002_watcher import MyWatcher, FileSystemEventHandler
    ...:
    ...: class MyHandler(FileSystemEventHandler):
    ...:
    ...:     def on_any_event(self, event):
    ...:         if event.event_type == "deleted":
    ...:             print("file was deleted.")
    ...:
    ...: if __name__=="__main__":
    ...:     w = MyWatcher(".", MyHandler())
    ...:     w.run()
    ...:

 Watcher Running in ./
```

 実行すると、       `”Watcher Running in ./"`          と表示されるので、別ターミナルで次のコマンドを実行してみましょう。

```
 $ touch junk
```

        `MyHandler`       オブジェクトの  `on_any_event()` は呼び出されますが、`event_type` が "deleted" ではないので、何も起きません。

先ほどの別のターミナルで次のコマンドを実行してみます。

```
 $ rm junk
```

すると Watcher から "file deleted" 文字が表示されます。
 今回の場合、       `Ctrl+C`         を押下することで終了させます。

```

  file was deleted.
  ^C
  Watcher Terminated


  In [3]:

```

#### src_path
        `src_path`         はイベントを発生させたファイルまたはディレクトリ/フォルダの絶対パスが文字列で与えられます。
ここでも、別のターミナルから         `touch junk`         と `rm junk` の2つのコマンドを実行してみてください。


```
 In [2]: # %load c004_src_path.py
   ...: from pathlib import Path
   ...: from c002_watcher import MyWatcher, FileSystemEventHandler
   ...:
   ...: class MyHandler(FileSystemEventHandler):
   ...:
   ...:     def on_any_event(self, event):
   ...:         if event.event_type == "deleted":
   ...:             filename = Path(event.src_path).absolute()
   ...:             print(f"{filename} was deleted.")
   ...:
   ...: if __name__=="__main__":
   ...:     w = MyWatcher(".", MyHandler())
   ...:     w.run()
   ...:
 MyWatcher Running in .

 junk was deleted.
 ^C
 Watcher Terminated


 In [3]:
```

期待どおりにイベントをトリガーにして処理がされています。

#### is_directory
        `is_directory`         にはブール値が与えられ、イベントを発生させた対象がファイルのときは`False`、ディレクトリ/フォルダのときは `True` になります。
今回も、別のターミナルから         `touch junk`         と `rm junk` の2つのコマンドを実行してみてください。


 pythokn
```
 In [2]: # %load c005_is_directory.py
    ...: from pathlib import Path
    ...: from c002_watcher import MyWatcher, FileSystemEventHandler
    ...:
    ...: class MyHandler(FileSystemEventHandler):
    ...:
    ...:     def on_any_event(self, event):
    ...:         name = Path(event.src_path).name
    ...:         if event.is_directory:
    ...:             print(f"event occurred in directory: {name}.")
    ...:         else:
    ...:             print(f"event occurred in file: {name}.")
    ...:
    ...: if __name__=="__main__":
    ...:     w = MyWatcher(".", MyHandler())
    ...:     w.run()
    ...:
 MyWatcher Running in .
 event occurred in file: junk.
 event occurred in file: junk.
 event occurred in directory: Tutorial.Filesystem_Events.
 ^C
 MyWatcher Terminated


 In [3]:

```

ファイルに対するイベントは、そのファイルが格納されているディレクトリにも影響を与えることに注意してください。

この例では、ファイル作成したときには、file createdイベントと、directory modifiedイベントが発生することがわかります。’

また、どのイベントが発生するのかを理解していないと重複したイベントを処理してしまうことになるので注意が必要です。
つぎの実行例は、ファイル更新のイベントの処理で、そのファイルに追加するために同じファイル更新のイベントが発生していることを理解しましょう。

```
 In [2]: # %load c006_infinity.py
    ...: from c002_watcher import MyWatcher, FileSystemEventHandler
    ...:
    ...: class MyHandler(FileSystemEventHandler):
    ...:     count = 0
    ...:
    ...:     def on_any_event(self, event):
    ...:         if not event.is_directory:
    ...:             if MyHandler.count <10:
    ...:                 with open(event.src_path, "a") as fp:
    ...:                     fp.write(f"{MyHandler.count} MODIFIED\n")
    ...:                     MyHandler.count += 1
    ...:
    ...: if __name__=="__main__":
    ...:     w = MyWatcher(".", MyHandler())
    ...:     w.run()
    ...:
 MyWatcher Running in .
 ^C
 MyWatcher Terminated


 In [3]:
```

別のターミナルで         `touch junk`         すると、このコードでは何も表示されませんが、`junk` には次のような変更が加えられます。

```
 $ cat junk
 0 MODIFIED
 1 MODIFIED
 2 MODIFIED
 3 MODIFIED
 4 MODIFIED
 5 MODIFIED
 6 MODIFIED
 7 MODIFIED
 8 MODIFIED
 9 MODIFIED
```

#### is_synthetic
is_synthetic  にはブール値がセットされ、合成されたイベントの場合は       `True`       、そうでない場合は `False`になります。
これはOSが実際に発行していないイベントですが、他の実際のイベントから起こったと推定されるイベントです。

# pygtail について

[pygtail https://pypi.org/project/pygtail/] は Debian で使用されている [logcheck](https://logcheck.org/]) コマンドに含まれている logtail2 を Python で実装したものです。ファイルの末尾部分を取得するときに便利ですが、 ローテーションログでのファイルパターンを認識してくれるのが特徴です。

### インストール
pygtail は pip でインストールすることができます。

```
 $ pip install pygtail
```

### 使用例

pygtail は指定したファイルを読み込んで行を返すイテラルオブジェクトを生成する         `Pygtail`       クラスを提供しています。

        `Pygtail`       クラスの使い方はとても簡単で、 `Pygtail`クラスにファイルパスを与えるだけです。


```
 In [2]: # %load c010_pygtail_demo.py
    ...: from pygtail import Pygtail
    ...:
    ...: for line in Pygtail('junk'):
    ...:     sys.stdout.write(line)
    ...:
 0 MODIFIED
 Out[2]: 11
 1 MODIFIED
 Out[2]: 11
 2 MODIFIED
 Out[2]: 11
 3 MODIFIED
 Out[2]: 11
 4 MODIFIED
 Out[2]: 11
 5 MODIFIED
 Out[2]: 11
 6 MODIFIED
 Out[2]: 11
 7 MODIFIED
 Out[2]: 11
 8 MODIFIED
 Out[2]: 11
 9 MODIFIED
 Out[2]: 11

 In [3]: %run c010_pygtail_demo.py

 In [4]: !cat junk.offset
 187563631
 110

 In [5]:
```

実行すると指定したファイルパスに拡張子         `.offset`         がついたファイルが生成されて、最後に読み出した位置を保存しています。つぎに呼ばれたときはこのファイルを参照してこれまでに読み出された部分はスキップして、それ以降の行を返します。

## Pygtailクラス

        `Pygtail`       クラスはイテラルオブジェクトを生成して、呼び出されたときに前回の続きの行を返します。
        `Pygtail`       クラスには次のキーワード引数を渡すことができます。

        `Pygtail(filename, offset_file=None, paranoid=False, copytruncate=True, every_n=0, on_update=False, read_from_end=False, log_patterns=None, full_lines=False)`

  -         `filename`       :  読みだすファイルのパス
  -         `offset_file`       ：　オフセット位置を保存するオフセットファイルのファイルパス。デフォルトは  `{filename}.offset`
  -         `paranoid`       ： `True`を与えると行を読むたびにオフセットファイルを更新する。デフォルトは `False`でファイルの終端に達したときだけ更新する。
  -         `every_n`       ：与えた数値の行を読んだときにオフセットファイルを更新する。デフォルトはゼロ( `0`)で、ファイルの終端に達したときに更新する。
  -         `on_update`       ：オフセットデータが書き込まれたときにこの関数を実行する（デフォルト `False`）
  -         `copytruncate`       ： `True`を与えるとcopytruncate スタイルのログローテーションをサポートする。（デフォルトは`True`)
  -         `log_patterns`       ：一致させるカスタムローテートログパターンのリスト（デフォルトは  `None`）
  -         `full_lines`       ：行末が改行のときのみログを読みだす。（デフォルト `False`）


## cmdkit について
ここまでで、watchdog と pygtail が使えるようになっているので、簡単なコマンドスクリプトを作ってみましょう。

オプション解析のためのツールには、Python 標準ライブラリの argparser や、click や typer などがあります。cmdkit は argparser をラッピングしたモジュールで、オプション解析と構成ファイルの読み書き、および環境変数の読み込みなどができるのでコマンドラインスクリプトを開発が非常に簡単になります。


## ヘルプメッセージ

仕様を考えるためにも、まずヘルプメッセージを考えてみましょう。


```
 logwatcher - Watchdog script for specified directories.


 Usage: logwatcher [OPTIONS] <path>

 Arguments:
     path             The path to Watch directory.

 Options:
     -i, --interval    Watch interval seconds.
     -O, --observate   Observate to watch directory.
     -p, --pattern     Search pattern from logfiles in watch directory.
     -r, --recursive   Whether to recursively for subdirectories.
     -s, --suffix      The suffixes for Watch directory.
     -h, --help        show this message and exit.

```


オプション解析ツールの多くは、ヘルプメッセージを自動生成してくれますが、cmdkit では与えた文字列を単純に表示するだけです。すこしタイプ量は増えるのですが、表示されている内容の細かい調整は簡単で、呼び出す側のコードにドキュメントとしてヘルプメッセージを定義するだけなので、シンプルで理解が用意になります。


 cli_001.py
```py
 from cmdkit.app import Application, exit_status
 from cmdkit.cli import Interface, ArgumentError

 APP_NAME='logwatcher'
 APP_DESCRIPTION=f"""\
 {APP_NAME} - Watchdog script for specified directories.
 """

 APP_USAGE=f"""
 {APP_DESCRIPTION}

 Usage: {APP_NAME} [OPTIONS] <path>
 """

 APP_HELP=f"""
 {APP_USAGE}
 Arguments:
     path             The path to Watch directory.

 Options:
     -i, --interval    Watch interval seconds.
     -O, --observate   Observate to watch directory.
     -p, --pattern     Search pattern from logfiles in watch directory.
     -r, --recursive   Whether to recursively for subdirectories.
     -s, --suffix      The suffixes for Watch directory.
     -h, --help        show this message and exit.
 """

 class MyApp(Application):

     ALLOW_NOARGS: bool = True
     interface = Interface(APP_NAME, APP_USAGE, APP_HELP)

     path: str = ""
     interval: int = 1
     suffix: str = ".txt, .log"
     recursive: bool = False
     observate: bool = True
     pattern: str ="ERROR, FATAL"

     interface.add_argument('path', default=path, type=str)
     interface.add_argument('-i', '--interval', type=int,
                            default=interval )
     interface.add_argument('-r', '--recursive', action='store_true',
                            default=recursive )
     interface.add_argument('-s', '--suffix', type=str,
                            default=suffix )
     interface.add_argument('-w', '--observate', action='store_true',
                            default=observate )
     interface.add_argument('-p', '--pattern', type=str,
                            default=pattern )

     def run(self):
         print(f"path: {self.path}")
         print(f"interval: {self.interval}")
         print(f"suffix: {self.suffix}")
         print(f"recursive: {self.recursive}")
         print(f"observate: {self.observate}")
         print(f"pattern: {self.pattern}")


 if __name__ == '__main__':
     import sys
     MyApp.main(sys.argv[1:])

```

ここで、混乱しやすいことは         `MyApp.main()`         です。`main()`メソッドは cmdkit の `Application` で定義されていて、呼び出すことでオプションとコマンド引数は argparse を使って解析され、それから `MyApp.run()` を呼び出してくれます。

今の段階では、このコードでは         `run()`         にはオプションや引数を表示することしか定義していません。

## デフォルト値を設定できるようにする
 このままでは、オプションのデフォルト値はハードコーディングされてしまっていて柔軟性がありません。そこで、       `config.py`       でデフォルト値を設定し、それを読み込むようにしてみます。

 config.py
```py
 from pathlib import Path
 from dataclasses import dataclass

 workdir = Path.cwd()
 homedir = Path.home()

 @dataclass
 class WatchConfig(object):
     # The directory to Watch.
     WATCH_DIRECTORY: Path = homedir / 'log'

     # Delay time between Watch cycles in seconds.
     WATCH_INTERVAL: int = 1

     # allow to Watch into subdirectories.
     WATCH_RECURSIVELY: bool = False

     # To observate for WATCH_DIRECTORY
     WATCH_DO_OBSERVATE: bool = True

     # The suffix of watch files
     WATCH_FILE_SUFFIXES: str = '.txt, .log, .output'

     # The patterns for observations in watch files
     WATCH_PATTERN: str = "ERROR, FATAL"

```

dataclasses は、データを格納するためのクラスの定義するための様々な機能を含んだ便利なモジュールです。
        `@dataclass`         でデコレートしたクラスはデータを保持するオブジェクトを生成してくれます。

これを使用する場合は次のようになります。

```
 In [2]: # %load config_check.py
    ...: from config import WatchConfig
    ...: from pprint import pprint
    ...:
    ...: conf = WatchConfig()
    ...:
    ...: # pprint(conf)
    ...: # pprint(conf.__dict__)
    ...:

 In [3]: pprint(conf)
 WatchConfig(WATCH_DIRECTORY=PosixPath('/Users/goichiiisaka/log'),
             WATCH_INTERVAL=1,
             WATCH_RECURSIVELY=False,
             WATCH_DO_OBSERVATE=True,
             WATCH_FILE_SUFFIXES='.txt, .log, .output',
             WATCH_PATTERN='ERROR, FATAL')

 In [4]: pprint(conf.__dict__)
 {'WATCH_DIRECTORY': PosixPath('/Users/goichiiisaka/log'),
  'WATCH_DO_OBSERVATE': True,
  'WATCH_FILE_SUFFIXES': '.txt, .log, .output',
  'WATCH_INTERVAL': 1,
  'WATCH_PATTERN': 'ERROR, FATAL',
  'WATCH_RECURSIVELY': False}

 In [5]:
```


ここで定義した         `WatchConfig`       オブジェクトを  cmdkit に読み込ませるためには、`Configuration`クラスを使用します。

```
 In [2]: # %load config_read
    ...: from cmdkit.config import Configuration
    ...: from pprint import pprint
    ...: from config import WatchConfig
    ...:
    ...: from config import basedir, homedir, WatchConfig
    ...:
    ...: conf = Configuration.from_local(
    ...:                  default = WatchConfig().__dict__,
    ...:                  env = False, prefix='',
    ...:                  system = '',
    ...:                  user = str(homedir / '.logwatcher.yml'),
    ...:                  local = str(basedir / 'logwatcher.yml'))
    ...:
    ...: # pprint(conf)
    ...:

 In [3]: pprint(conf)
 Configuration(default=Namespace({'WATCH_DIRECTORY': PosixPath('/Users/goichiiisaka/log'), 'WATCH_INTERVAL': 1, 'WATCH_RECURSIVELY': False, 'WATCH_DO_OBSERVATE': True, 'WATCH_FILE_SUFFIXES': '.txt, .log, .output', 'WATCH_PATTERN': 'ERROR, FATAL'}), system=Namespace({}), user=Namespace({}), local=Namespace({}))

 In [4]:
```

        `Configuration`       クラスを初期化するときに次のキーワード引数を与えることでデフォルト値の設定を柔軟に定義することができます。

-         `default`         - デフォルトの設定値の辞書
-         `system`         - システムレベルの設定ファイル
-         `user`         - ユーザレベルの設定ファイル
-         `local`         - カレントディレクトリにある設定ファイル

 優先度は       `default`       で定義したものもが最も低く、 `system`、`user`、`local`の順に上書きされていきます。

設定ファイルは、TOMI、YAML、JSON で記述することができます。cmdkit の 2.6.1 ではファイルの拡張子で判断しています。
タイプを指定できるようにした修正を[プルリクエスト](https://github.com/glentner/CmdKit/pull/17])して受け入れられたので、次のバージョンではファイル名に制限はなくなるかもしれません。

次のようにカレントディレクトリに         `logwatcher.yaml`         を作成して、もう一度実行してみます。

 logwatcher.yaml
```yaml
 WATCH_DIRECTORY: "/tmp/junk"
```

 pytohn
```
 In [2]: # %load config_read
    ...: from cmdkit.config import Configuration
    ...: from pprint import pprint
    ...: from config import WatchConfig
    ...:
    ...: from config import basedir, homedir, WatchConfig
    ...:
    ...: conf = Configuration.from_local(
    ...:                  default = WatchConfig().__dict__,
    ...:                  env = False, prefix='',
    ...:                  system = '',
    ...:                  user = str(homedir / '.logwatcher.yml'),
    ...:                  local = str(basedir / 'logwatcher.yml'))
    ...:
    ...: # pprint(conf)
    ...:

 In [3]: print(conf.WATCH_DIRECTORY)
 /tmp/junk

 In [4]:
```

 cli_002.py
```py
 from cmdkit.app import Application, exit_status
 from cmdkit.cli import Interface, ArgumentError
 from cmdkit.config import Configuration

 from pathlib import Path
 from config import workdir, homedir, WatchConfig

 myconf = Configuration.from_local(
                  default = WatchConfig().__dict__,
                  env = False, prefix='',
                  user = str(homedir / '.logwatcher.yml'),
                  local = str(workdir / 'logwatcher.yml'))

 APP_NAME='logwatcher'
 APP_DESCRIPTION=f"""\
 {APP_NAME} - Watchdog script for specified files and directories.
 """

 APP_USAGE=f"""
 {APP_DESCRIPTION}

 Usage: {APP_NAME} [OPTIONS] <path>
 """

 APP_HELP=f"""
 {APP_USAGE}
 Arguments:
  path             The path to Watch directory.
                   default is {myconf.WATCH_DIRECTORY}
 Options:
 -i, --interval    Watch interval seconds.
                   default is {myconf.WATCH_INTERVAL}
 -O, --observate   Observate to watch directory.
                   default is {myconf.WATCH_DO_OBSERVATE}
 -p, --pattern     Search pattern from logfiles in watch directory.
                   default is "{myconf.WATCH_PATTERN}"
 -r, --recursive   Whether to recursively for subdirectories.
                   default is {myconf.WATCH_RECURSIVELY}
 -s, --suffix      The suffixes for Watch directory.
                   default is "{myconf.WATCH_FILE_SUFFIXES}"
 -h, --help        show this message and exit.
 """

 class MyApp(Application):

     ALLOW_NOARGS: bool = True
     interface = Interface(APP_NAME, APP_USAGE, APP_HELP)

     path: Path = myconf.WATCH_DIRECTORY
     interval: int = myconf.WATCH_INTERVAL
     suffix: str = myconf.WATCH_FILE_SUFFIXES
     recursive: bool = myconf.WATCH_RECURSIVELY
     observate: bool = myconf.WATCH_DO_OBSERVATE
     pattern: bool = myconf.WATCH_PATTERN
     pattern: bool = myconf.WATCH_PATTERN

     interface.add_argument('path', default=path, type=Path)
     interface.add_argument('-i', '--interval', type=int,
                            default=interval )
     interface.add_argument('-r', '--recursive', action='store_true',
                            default=recursive )
     interface.add_argument('-s', '--suffix', type=str,
                            default=suffix )
     interface.add_argument('-w', '--observate', action='store_true',
                            default=observate )
     interface.add_argument('-p', '--pattern', type=str,
                            default=pattern )

     def run(self):
         print(f"path: {self.path}")
         print(f"interval: {self.interval}")
         print(f"suffix: {self.suffix}")
         print(f"recursive: {self.recursive}")
         print(f"observate: {self.observate}")
         print(f"pattern: {self.pattern}")

 if __name__ == '__main__':
     import sys
     MyApp.main(sys.argv[1:])

```

 今のままでは、       `path`       に与えた対象がファイルであっても受け入れてしまいます。watchdog  と連携させるために、このスクリプトで与えるコマンド引数はディレクトリを与える必要があります。
        `add_argument()`       の  `type`キーワード引数に関数を渡せること利用して、例外を発生させてみます。

 cli_003.py
```py
 from cmdkit.app import Application, exit_status
 from cmdkit.cli import Interface, ArgumentError
 from cmdkit.config import Configuration

 from pathlib import Path
 from config import workdir, homedir, WatchConfig

 myconf = Configuration.from_local(
                  default = WatchConfig().__dict__,
                  env = False, prefix='',
                  user = str(homedir / '.logwatcher.yml'),
                  local = str(workdir / 'logwatcher.yml'))

 # 中略

 def is_dir_path(path):
     if Path(path).is_dir():
         return path
     else:
         raise NotADirectoryError(path)

 class MyApp(Application):

     ALLOW_NOARGS: bool = True
     interface = Interface(APP_NAME, APP_USAGE, APP_HELP)

     path: Path = myconf.WATCH_DIRECTORY
     interval: int = myconf.WATCH_INTERVAL
     suffix: str = myconf.WATCH_FILE_SUFFIXES
     recursive: bool = myconf.WATCH_RECURSIVELY
     observate: bool = myconf.WATCH_DO_OBSERVATE
     pattern: bool = myconf.WATCH_PATTERN

     interface.add_argument('path', default=path, type=is_dir_path)
     interface.add_argument('-i', '--interval', type=int,
                            default=interval )
     interface.add_argument('-r', '--recursive', action='store_true',
                            default=recursive )
     interface.add_argument('-s', '--suffix', type=str,
                            default=suffix )
     interface.add_argument('-w', '--observate', action='store_true',
                            default=observate )
     interface.add_argument('-p', '--pattern', type=str,
                            default=pattern )

     def run(self):
         print(f"path: {self.path}")
         print(f"interval: {self.interval}")
         print(f"suffix: {self.suffix}")
         print(f"recursive: {self.recursive}")
         print(f"observate: {self.observate}")
         print(f"pattern: {self.pattern}")

 if __name__ == '__main__':
     import sys
     try:
         MyApp.main(sys.argv[1:])
     except NotADirectoryError:
         print(APP_USAGE)
         print(f"<path> must be directory.")
         sys.exit(1)

```

```
 $ touch junk
 $ python cli_003.py junk

 logwatcher - Watchdog script for specified files and directories.


 Usage: logwatcher [OPTIONS] <path>

 <path> must be directory.

```

## パターンを検索する
与えたファイルの行をパースして指定したパターンがあるか調べて、ヒットした場合だけ次の文字列を返すようなクラス         `FileChecker`       を作成しましょう。

        `File: {FILENAME}, Found in line {NUMBER}: {LINE}`

ファイルの内容を取得する処理に、pygtail を使うわけです。
行をパースするために、正規表現を処理する標準ライブラリ re を使っています。

 checker.py
```py
 import re
 from pygtail import Pygtail
 from typing import List, Union

 class FileChecker:
     def __init__(self, pattern: List[str]):
         if isinstance(pattern, list):
             self.pattern = pattern
         else:
             self.pattern = [pattern]

     def check_pattern(self, path: str ):
         for num, line in enumerate(Pygtail(path), 1):
             line = line.strip()
             if line:
                 if any(re.findall('|'.join(self.pattern),
                         line, flags=re.IGNORECASE | re.VERBOSE)):
                     msg = (
                          f" File: {path},"
                          f" Found in line {num}: {line}"
                     )
                     yield msg

```

        `watchdog`       で監視するディレクトリで発生するイベントは、ファイルやディレクトリなど対象が複数あるため、初期化時にはパターンを与えて、実際にチェックするときにパスを受け取るようにしています。
この         `FileChecker`       クラスを  `LogHandler`クラスで初期化します。

 core.py
```py
 import time
 from watchdog.observers import Observer
 from watchdog.events import FileSystemEventHandler
 from checker import FileChecker
 from typing import Tuple, List, Optional

 class LogHandler(FileSystemEventHandler):

     def __init__(self,
                  watch_suffixes: Tuple[str] = ('.log'),
                  watch_pattern: List[str] = [],
                  watch_observate: bool = False
         ):
         self.watch_suffixes = watch_suffixes
         self.watch_pattern = watch_pattern
         self.watch_observate = watch_observate
         self.filechecker = FileChecker(self.watch_pattern)

     def on_any_event(self, event):

         if not event.is_directory:
             path = event.src_path
             if hasattr(event, 'dest_path'):
                 path = event.dest_path
             if path.endswith(self.watch_suffixes):
                 basemsg = f" {event.event_type}, File:{path}"
                 for msg in self.filechecker.check_pattern(path=path):
                     print(f"{basemsg} {mg}")
         elif self.watch_observate:
             msg = f" {event.event_type}, Dir:{event.src_path}"
             print(msg)
```

これですべてのパーツがそろったので cmdkit  の　       `run()`         メソッドに記述すれば、コマンドラインスクリプトとして動作できます。

```
     def run(self):
         log_watcher = LogWatcher(
             watch_directory=self.path,
             watch_interval=self.interval,
             watch_recursive=self.recursive,
             watch_do_observate=self.observate,
             watch_suffixes = tuple(self.suffix.replace(' ','').split(",")),
             watch_pattern = list(self.pattern.split(",")),
         )

         log_watcher.run()

```


## まとめ
これまでのハンズオンを通して次のことを理解できたことになります。

- watchdog によるファイルシステムのイベント監視の方法
- pygtail によるファイル内容の末尾部分の取得
- dataclasses によるデータを保持するクラスの作成と利用方法
- cndkit によるコマンドラインスクリプトの作成方法

## 参考資料

- watchdog
  - [PyPi - watchdog](https://pypi.org/project/watchdog/])
  - [ソースコード](https://github.com/gorakhargosh/watchdog])
- pygtail
  - [PyPI - pygtail](https://pypi.org/project/pygtail/])
  - [ソースコード](https://github.com/bgreenlee/pygtail])
- cmdkit
  - [PyPI - cmdkit](https://pypi.org/project/cmdkit/])
  - [ソースコード](https://github.com/glentner/CmdKit])
- Python 公式ドキュメント
  - [dataclasses - データクラス](https://docs.python.org/ja/3.10/library/dataclasses.html#module-dataclasses])
  - [re - 正規表現操作](https://docs.python.org/ja/3.10/library/re.html?highlight=re#module-re])
