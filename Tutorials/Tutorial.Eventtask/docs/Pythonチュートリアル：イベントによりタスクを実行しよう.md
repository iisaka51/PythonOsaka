Pythonチュートリアル：イベントによりタスクを実行しよう
=================

![](https://gyazo.com/d2e4c3c3354e5ee7ff62c27d83fed712.png)


## ファイルやディレクトリを監視してタスクを実行する

ファイルが更新されたタイミングや、ディレクトリにファイルが新規に保存されたタイミングで何かタスクを実行させたいときがあります。最近のOSではシステムレベルでのサポートもあります。

- inotify (Linux)
- epoll (Linux)
- ReadDirectoryChangesW (Windows Win32)
- System.IO.FileSystemWatcher (Windows .NET)
- FSEvents (Mac OS X)
- kqueue (BSD, Mac OS X)

これらのインタフェースをラップするライブラリも多く公開されています。

- epoll (Linix) のインタフェースを利用するもの
  - [select](https://docs.python.org/3.9/library/select.html)：Python 標準ライブラリ

- inotify (Linux) のインタフェースを利用するもの
  - [pyinotify](https://github.com/seb-m/pyinotify)：Linux only
  - [Minotaur](https://github.com/giannitedesco/minotaur)： Linux / Mac 、pyinotify より簡潔に記述できる
  - [butter](https://pypi.org/project/butter/)：Linux only、マウント/アンマウントなどのイベントも監視できる
  - [watchdog](https://github.com/gorakhargosh/watchdog): Watchdog はWindows、Mac（またはLinux）で動作
  - [watchman](https://facebook.github.io/watchman/)：Facebook が開発したファイルシステムを監視するサービスアプリケーション

## pyinotify
パッケージ名からわかるようにLinux の inotify のインタフェースを利用しています。
Linux 以外のプラットフォームでは利用できないことに注意してください。

この資料を作成している時点で、pypi.org では次のパッケージが公開されています。

- [pyinotify 0.9.6](https://pypi.org/project/pyinotify/)
- [rs-pyinotify 0.9.9](https://pypi.org/project/rs-pyinotify/)

rs-pyinotify は、docstrings が変わっているだけで機能は pyinotify と同じものです。

 python
```
 import pyinotify
 import asyncio


 def handle_read_callback(notifier):
     """
     Just stop receiving IO read events after the first
     iteration (unrealistic example).
     """
     print('handle_read callback')
     notifier.loop.stop()


 wm = pyinotify.WatchManager()
 loop = asyncio.get_event_loop()
 notifier = pyinotify.AsyncioNotifier(wm, loop,
                                      callback=handle_read_callback)
 wm.add_watch('/tmp', pyinotify.ALL_EVENTS)
 loop.run_forever()
 notifier.stop()
```

## minotaur
pyinotigy より簡単に利用できます。
ただしLinux の inotify のインタフェースを利用しているため、Linux 以外のプラットフォームでは利用できないことに注意してください。

 python
```
 from minotaur import Inotify

 with Inotify() as n:
         n.add_watch('.', Mask.CREATE | Mask.DELETE | Mask.MOVE)
         for evt in n:
             print(evt)
```

非同期処理を行う場合は、

 python
```
 from minotaur import Inotify

 with Inotify(blocking=False) as n:
         n.add_watch('.', Mask.CREATE | Mask.DELETE | Mask.MOVE)
         async for evt in n:
             print(evt)
```

## watchdog
これまでのものは、Linux に依存した実装になっていますが、watchdog はクロスプラットフォームを意識した実装になっていて、Windows, MacOS, Linux で動作します。

 python
```
 import time
 from watchdog.observers import Observer
 from watchdog.events import FileSystemEventHandler

 class Watcher:

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

 class MyHandler(FileSystemEventHandler):

     def on_any_event(self, event):
         print(event)   # Your code here

 if __name__=="__main__":
     w = Watcher(".", MyHandler())
     w.run()
```

詳細については、「watchdog を使ってファイルシステムのイベントを処理してみよう」にまとめています。

## ファイルの内容を監視しつづけるもの
ログファイルを監視してその出力に"ERROR"の文字列を見つけるとメールを送信するといったような場合があります。こうした機能では Zabbix や Nagios、 Himenos など多くの統合型の監視ツールが存在しています。これらも当然便利ではあるのですが、プライベートプロジェクトや自分の計算ジョブについて監視するためだけに導入するのはオーバーヘッドが大きすぎます。
こうしたユースケースで便利なモジュールが [pygtail https://pypi.org/project/pygtail/] です。

pygtail はもともと debien につくまれている [logcheck https://github.com/SatyenderYadav/Logcheck] に内包されている perl スクリプトの logtail をPythonで実装したもので、コマンドラインツールも利用できます。

 bash
```
 $ pygtail --help
 Usage: pygtail [options] logfile

 Print log file lines that have not been read.

 Options:
   -h, --help            show this help message and exit
   -o OFFSET_FILE, --offset-file=OFFSET_FILE
                         File to which offset data is written (default:
                         <logfile>.offset).
   -p, --paranoid        Update the offset file every time we read a line (as
                         opposed to only when we reach the end of the file).
   -n EVERY_N, --every-n=EVERY_N
                         Update the offset file every n'th time we read a line
                         (as opposed to only when we reach the end of the
                         file).
   --no-copytruncate     Don't support copytruncate-style log rotation.
                         Instead, if the log file shrinks, print a warning.
   --read-from-end       Read log file from the end if offset file is missing.
                         Useful for large files.
   --log-pattern=LOG_PATTERN
                         Custom log rotation glob pattern. Use %s to represent
                         the original filename. You may use this multiple times
                         to provide multiple patterns.
   --full_lines          Only log when line ends in a newline (\n)
   --version             Print version and exit.

```

pygtail ではファイルを監視するための `Pygtail`クラスが提供されます。

 python
```
 from pygtail import Pygtail

 for line in Pygtail("some.log"):
     sys.stdout.write(line)
```

watchdog と連携させた利用例を「watchdogを使ってファイルシステムのイベントを処理してみよう」にまとめています。

## 時間条件によりタスクを実行するもの

- [sched](https://docs.python.org/3/library/sched.html)：汎用イベントスケジューラ、Python 標準ライブラリ
- [schedule](https://pypi.org/project/schedule/): 定期的なジョブのためのインプロセススケジューラで、人に優しいAPIが特徴。
- [timeloop](https://github.com/sankalpjonn/timeloop) 汎用イベントスケジューラ、デコレータで定義するため既存コードへの提供がしやすい
- [croniter](https://github.com/kiorky/croniter)：cron 互換の設定でイベント時刻を取得するもの
- [aiocron](https://github.com/gawel/aiocron/)：cron 互換の設定で処理を実行するもの

これらのライブラリについては、「イベントスケジューラを使ってみよう」にまとめています。

