logzeroを使ってロギングをしてみよう
=================
![](https://gyazo.com/96f0cc7cc9765f6b965338ebdbc0b42c.png)


## logzero について

Python の堅牢で効果的なロギングを行うためのライブラリです。
次のような特徴を持っています。

- コンソールやファイルへの簡単なロギング。
- 完全に設定された Python logger オブジェクトを提供。
- コンソールでのレベルごとの色付けなど、美しいフォーマット。
- JSON ロギングのサポート (統合された python-json-logger を使用)
- coloramaによるWindowsカラー出力のサポート。
- str/bytes エンコーディングの問題に強く、あらゆる種類の文字エンコーディングや特殊文字で動作。
- 複数のロガーが同じログファイルに書き込むことが可能(複数のPythonファイルでも動作)
-  `logzero.logger` によるグローバルなデフォルトロガーと `logzero.setup_logger(...)` によるカスタムロガー。
- すべては1つのファイルに含まれている
- ライセンスはMITライセンス
- Tornadoウェブフレームワークにインスパイアされている
- オープンソースとしてGitHub で公開されている。: https://github.com/metachris/logzero


## インストール

 bash
```
 $ pip install  logzero

```


## logzero の使用方法
logzero の使用は非常に簡単で、 logzzero をインポートして logger を使用するだけで、基本的なロギングは行なえます。



```
 In [2]: # %load 01_intro.py
    ...: from logzero import logger
    ...:
    ...: logger.debug("hello")
    ...: logger.info("info")
    ...: logger.warning("warn")
    ...: logger.error("error")
    ...:
    ...: try:
    ...:     raise Exception("this is a demo exception")
    ...: except Exception as e:
    ...:     logger.exception(e)
    ...:
    ...: # logger.info("test")
    ...:
 [D 210923 14:26:55 <ipython-input-2-b96192c2049f>:4] hello
 [I 210923 14:26:55 <ipython-input-2-b96192c2049f>:5] info
 [W 210923 14:26:55 <ipython-input-2-b96192c2049f>:6] warn
 [E 210923 14:26:55 <ipython-input-2-b96192c2049f>:7] error
 [E 210923 14:26:55 <ipython-input-2-b96192c2049f>:12] this is a demo exception
     Traceback (most recent call last):
       File "<ipython-input-2-b96192c2049f>", line 10, in <module>
         raise Exception("this is a demo exception")
     Exception: this is a demo exception

 In [3]: logger.info("test")
 [I 210924 14:27:04 <ipython-input-3-ef4a2269f512>:1] test

```


## ファイルへロギングを行う

logzero でファイルにロギングを行う場合も、とても簡単です。


```
 In [2]: # %load 02_logging_to_file.py
    ...: import logzero
    ...: from logzero import logger
    ...:
    ...: # non-rotating logfile
    ...: logzero.logfile("/tmp/logfile.log")
    ...:
    ...: # rotating logfile
    ...: logzero.logfile("/tmp/rotating-logfile.log",
    ...:                 maxBytes=1e6, backupCount=3)
    ...:
    ...: # log messages
    ...: logger.info("This message output to the console and the logfile")
    ...:
 [I 210923 14:35:01 <ipython-input-2-3c20ac3d113a>:13] This message output to the console and the logfile

 In [3]: !cat /tmp/logfile.log

 In [4]: !cat /tmp/rotating-logfile.log
 [I 210923 14:35:01 <ipython-input-2-3c20ac3d113a>:13] This message output to the console and the logfile

```

ログ・ファイルでは、最大ファイルサイズ( `maxBytes` )、ローテーション数( `backupCount` )を指示することができます。
この例で、 `/tmp/logfile.log` が空になっています。これはなぜでしょう？
これは、あくまでも例示のためのもので、初回の  `logzero.logfile()` で設定した内容を、２回めの  `logzero.kogfile()` で上書きしているためです。


## JSONフォーマットでロギング
JSONフォーマットでロギングするためにはは、デフォルトのロガーでは  `logzero.json()` を呼び出します。カスタムロガーでは  `setup_logger(json=True)` で有効にすることができます。



```
 In [2]: # %load 03_json_logging.py
    ...: import logzero
    ...: from logzero import logger
    ...:
    ...: logzero.json()
    ...: logger.info("test")
    ...:
    ...: mylogger = logzero.setup_logger(json=True)
    ...: mylogger.info("test again")
    ...:
    ...:
 {"asctime": "2021-09-23 14:48:08,636", "filename": "<ipython-input-2-18f5244aa3dd>", "funcName": "<module>", "levelname": "INFO", "levelno": 20, "lineno": 6, "module": "<ipython-input-2-18f5244aa3dd>", "message": "test", "name": "logzero_default", "pathname": "<ipython-input-2-18f5244aa3dd>", "process": 52320, "processName": "MainProcess", "threadName": "MainThread"}
 {"asctime": "2021-09-23 14:48:08,636", "filename": "<ipython-input-2-18f5244aa3dd>", "funcName": "<module>", "levelname": "INFO", "levelno": 20, "lineno": 9, "module": "<ipython-input-2-18f5244aa3dd>", "message": "test again", "name": "logzero", "pathname": "<ipython-input-2-18f5244aa3dd>", "process": 52320, "processName": "MainProcess", "threadName": "MainThread"}

```


JSONフォーマットで出力されるときは、次のフィールドがあります。

 json
```
 {
     "asctime": "2021-09-23 14:48:08,636",
     "filename": "<ipython-input-2-18f5244aa3dd>",
     "funcName": "<module>",
     "levelname": "INFO",
     "levelno": 20,
     "lineno": 6,
     "module": "<ipython-input-2-18f5244aa3dd>",
     "message": "test",
     "name": "logzero_default",
     "pathname": "<ipython-input-2-18f5244aa3dd>",
     "process": 52320,
     "processName": "MainProcess",
     "threadName": "MainThread"
 }
```

もし、例外を捕獲したのであれば次のように、 `exc_info` のフィールドが追加されます。

 json
```
 {
     "asctime": "2020-10-21 10:43:25,193",
     "filename": "test.py",
     "funcName": "test_this",
     "levelname": "ERROR",
     "levelno": 40,
     "lineno": 17,
     "module": "test",
     "message": "this is a demo exception",
     "name": "logzero",
     "pathname": "_tests/test.py",
     "process": 76192,
     "processName": "MainProcess",
     "threadName": "MainThread",
     "exc_info": "Traceback (most recent call last):\n  File \"_tests/test.py\", line 15, in test_this\n    raise Exception(\"this is a demo exception\")\nException: this is a demo exception"
 }
```


## ログフォーマット
ここでは、ログファイルの使用方法、カスタムフォーマッタ、最小ログレベルの設定などの例を紹介します。

 ログフォーマット

| 出力 | メソッド |
|:--|:--|
| 最小のログレベルを追加 | logzero.loglevel(..) |
| ログファイルにログを追加 | logzero.logfile(..) |
| ログファイルにローテーションを設定 | logzero.logfile(..) |
| ログファイルへのロギングを無効 | logzero.logfile(None) |
| JSONフォーマットでロギング | logzero.json(…) |
| syslog へログを出力 | logzero.syslog(…) |
| カスタムフォーマットを設定 | logzero.formatter(..) |



```
 import logging
 import logzero
 from logzero import logger
 from logging.handlers import SysLogHandler

 # コンソールへログメッセージを出力
 logger.debug("hello")

 # 最小のログレベルに設定
 logzero.loglevel(logzero.INFO)

 # ログファイルを設定(以後のログはこのファイルに書き込まれる)
 logzero.logfile("/tmp/logfile.log")

 # ログファイルを設定(以後のログはこのファイルに書き込まれる)
 # デフォルトの標準エラー出力はしなくなる
 logzero.logfile("/tmp/logfile.log", disableStderrLogger=True)

 # ログ・ファイルごとに異なるログレベルを設定することができる
 logzero.logfile("/tmp/logfile.log", loglevel=logzero.ERROR)

 # ログファイルにローテーションを設定
 logzero.logfile("/tmp/rotating-logfile.log", maxBytes=1000000, backupCount=3)

 # ファイルへのログ出力を無効に設定
 logzero.logfile(None)

 # JSONフォーマットを有効に設定
 logzero.json()

 # JSONフォーマットを無効に設定
 logzero.json(False)

 # logzero のデフォルトの出力先を syslog に設定 syslog facility は 'user'
 logzero.syslog()

 # logzero のデフォルトの出力先を syslog に設定 syslog facility は 'local0'
 logzero.syslog(facility=SysLogHandler.LOG_LOCAL0)

 # カスタムフォーマットを設定
 formatter = logging.Formatter(
     '%(name)s - %(asctime)-15s - %(levelname)s: %(message)s');
 logzero.formatter(formatter)

 # 指定したメッセージをログに出力 (この場合、ログレベルはINFO)
 logger.info("var1: %s, var2: %s", 1, 'Python')

```

## カスタム ロガー
デフォルトのロガーを使用する代わりに、 `logzero.setup_logger(...)` で特定のロガーインスタンスを設定することもできます。


```
 In [2]: # %load 05_custom_logger.py
    ...: import logzero
    ...: from logzero import setup_logger
    ...:
    ...: logger1 = setup_logger(name="mylogger1")
    ...: logger2 = setup_logger(name="mylogger2",
    ...:                        logfile="/tmp/test-logger2.log",
    ...:                        level=logzero.INFO)
    ...: logger3 = setup_logger(name="mylogger3",
    ...:                        logfile="/tmp/test-logger3.log",
    ...:                        level=logzero.INFO, disableStderrLogger=True)
    ...:
    ...: # 何かをロギング
    ...: logger1.info("info for logger 1")
    ...: logger2.info("info for logger 2")
    ...:
    ...: # ファイルのみにログを記録する(stderrへのログはしない)
    ...: logger3.info("info for logger 3")
    ...:
    ...: # カスタムフォーマットにJSONフォーマットを使用
    ...: jsonLogger = setup_logger(name="jsonLogger", json=True)
    ...: jsonLogger.info("info in json")
    ...:
 [I 210925 06:47:23 <ipython-input-2-e119494ae988>:14] info for logger 1
 [I 210925 06:47:23 <ipython-input-2-e119494ae988>:15] info for logger 2
 {"asctime": "2021-09-25 06:47:23,888", "filename": "<ipython-input-2-e119494ae988>", "funcName": "<module>", "levelname": "INFO", "levelno": 20, "lineno": 22, "module": "<ipython-input-2-e119494ae988>", "message": "info in json", "name": "jsonLogger", "pathname": "<ipython-input-2-e119494ae988>", "process": 57896, "processName": "MainProcess", "threadName": "MainThread"}

```


## カスタムハンドラの追加
logzeroはPython の標準ライブラリ logger を使用しているので、SocketHandlerなど多くのPythonロギングハンドラーを追加することができます。

次のコードは、SocketHandlerを追加するものです。


```
 In [2]: # %load 06_add_sockethandler.py
    ...: import logzero
    ...: import logging
    ...: from logging.handlers import SocketHandler, DEFAULT_TCP_LOGGING_PORT
    ...:
    ...: # SocketHandler の設定
    ...: socket_handler = SocketHandler('localhost', DEFAULT_TCP_LOGGING_PORT)
    ...: socket_handler.setLevel(logzero.DEBUG)
    ...: socket_handler.setFormatter(logzero.LogFormatter(color=False))
    ...:
    ...: # logzero のデフォルトロガーに追加
    ...: logzero.logger.addHandler(socket_handler)
    ...:
    ...: logzero.logger.info("this is a test")
    ...:
 [I 210925 07:19:13 <ipython-input-2-0017159e08ca>:14] this is a test

```

機能的な説明は、これだけです。(^o^)v

## まとめ
logzero を利用すると、 Python の標準ライブラリ logging の代わりに使用することができ、より簡単に扱えるようになります。


## 参考
- [logzero ドキュメント ](https://logzero.readthedocs.io/en/latest/)
- [logzero ソースコード  ](https://github.com/metachris/logzero)

