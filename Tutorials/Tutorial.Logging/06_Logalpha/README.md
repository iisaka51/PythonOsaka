logalphaを使ってロギングをしてみよう
=================
## logalpha について
[LogAlpha ](https://logalpha.readthedocs.io/en/latest/) は、シンプルさを重視したPythonでのロギングのための最小限のフレームワークです。LogAlphaはロギングシステムの中核となる機能のみを提供し、煩わしい設定は必要ありません。logalpha はテキストをログに記録することや、ファイルに書き込むことさえ必要としません。

## インストール

logalpha のインストールは pip で行います。

 bash
```
 $ pip install logalpha
 
```


## 基本的な使い方

### 既存設定
LogAlphaは、利用者が独自に設定をカスタマイズすることを期待していますが。使いやすさとデモンストレーションのために、いくつかの典型的な設定が事前に構築されています。

標準的な動作としては、典型的な5つのログレベルと、タイムスタンプ、ホスト名、トピックを含む詳細なメッセージを標準エラーに出力することです。これは、logalpha.contrib.standard　モジュールから利用できます。


```
 from logalpha.contrib.standard import StandardLogger, StandardHandler
 
 handler = StandardHandler()
 StandardLogger.handlers.append(handler)
```

他のモジュールでは、名前付きのトピックでインスタンスを作成します。


```
 log = StandardLogger(__name__)
 
```

ロガー(logger)には、各ロギングレベルのメソッドが自動的に組み込まれます。従来通り、デフォルトのロギングレベルは `WARNING` です。


```
 In [2]: # %load 01_intro.py
    ...: from logalpha.contrib.standard import StandardLogger, StandardHandler
    ...:
    ...: handler = StandardHandler()
    ...: StandardLogger.handlers.append(handler)
    ...:
    ...: log = StandardLogger(__name__)
    ...:
    ...: log.info('message')
    ...: log.warning('message')
    ...:
 2021-09-17 09:28:09.643 GoichiMacBook.local WARNING  [__main__] message
```


## ロガーのカスタマイズ

あらかじめ用意されているものを使うのではなく、独自のロギング動作を定義してみましょう。単純なプログラムであれば、単にOkやErrorのステータスを記録する程度でよいかもしれません。

そのためには、独自のレベルセットを持つロガーを作成する必要があります。そして、メッセージのためのハンドラーを作ります。

 mylogger.py
```
 import sys
 from dataclasses import dataclass
 from typing import List, IO, Callable
 
 from logalpha.color import Color, ANSI_RESET
 from logalpha.level import Level
 from logalpha.message import Message
 from logalpha.handler import StreamHandler
 from logalpha.logger import Logger
 
 
 class OkayLogger(Logger):
     """Logger with Ok/Err levels."""
 
     levels: List[Level] = Level.from_names(['Ok', 'Err'])
     colors: List[Color] = Color.from_names(['green', 'red'])
 
 
 @dataclass
 class OkayHandler(StreamHandler):
     """
     Writes to <stderr> by default.
     Message format includes the colorized level and the text.
     """
 
     level: Level = OkayLogger.levels[0]  # Ok
     resource: IO = sys.stderr
 
     def format(self, message: Message) -> str:
         """Format the message."""
         color = OkayLogger.colors[message.level.value].foreground
         return f'{color}{message.level.name:<3}{ANSI_RESET} {message.content}'
 
```

HandlerとMessageの派生クラスにdataclassデコレーターを含めることを忘れないでください。新しいフィールドを追加していないのであれば、問題なく動作するはずです。

標準のロガーと同じように、ロガーをセットアップします。

 pytohn
```
 In [2]: # %load 02_custom_logger.py
    ...: from mylogger import *
    ...:
    ...: handler = OkayHandler()
    ...: OkayLogger.handlers.append(handler)
    ...:
    ...: log = OkayLogger()
    ...:
    ...: log.ok('operation succeeded')
    ...:
 Ok  operation succeeded
 
```

このロガーを使用しているときに、ログレベルのメソッドが不明であるという警告が IDE から表示される場合があります。これは、このメソッドが動的に生成されるためです。必要であれば、クラスに型のアノテーションを追加して、これを回避することができます。

これらのメソッドの名前は、レベル名を常に小文字で表記したものとなります。


```
 class OkayLogger(Logger):
     """Logger with Ok/Err levels."""
 
     levels: List[Level] = Level.from_names(['Ok', 'Err'])
     colors: List[Color] = Color.from_names(['green', 'red'])
 
     # stubs for instrumented level methods
     ok: Callable[[str], None]
     err: Callable[[str], None]
```


## カスタムメタデータの追加
より詳細なロギング設定のためには、すべてのメッセージに添付したい追加のメタデータを独自に定義する必要があるかもしれません。Messageクラスは、シンプルなデータクラスです。デフォルトでは、レベルとコンテンツのみを含みます。Messageクラスをサブクラス化して属性を追加することで、拡張することができます。



```
 from datetime import datetime
 
 from logalpha.level import Level
 from logalpha.message import Message
 
 
 @dataclass
 class DetailedMessage(Message):
     """A message with additional attributes."""
     level: Level
     content: str
     timestamp: datetime
     topic: str
     host: str
     
```

メッセージの内容を文字列以外のものに定義することができ、ハンドラーはそれに応じてフォーマットや書き込み方法を定義することができます。

繰り返しになりますが、Message自体は単純なデータクラスです。Levelクラスのソッドの1つを呼び出したときにLoggerはメッセージを作成し、それらの属性ごとに定義されたコールバックが必要になります。


```
 from datetime import datetime
 from socket import gethostname
 from typing import Type, Callable, IO
 
 from logalpha.level import Level
 from logalpha.message import Message
 from logalpha.logger import Logger
 
 
 HOST: str = gethostname()
 
 class DetailedLogger(Logger):
     """Logger with detailed messages."""
 
     Message: Type[Message] = DetailedMessage
     topic: str
 
     def __init__(self, topic: str) -> None:
         """Initialize with  `topic` ."""
         super().__init__()
         self.topic = topic
         self.callbacks = {'timestamp': datetime.now,
                           'host': (lambda: HOST),
                           'topic': (lambda: topic)}
                           
```

ここで定義したロガーとMessageは一対一の関係にあります。同じ Message を入力とし、メッセージのフォーマットや書き込み先のリソースの種類が異なる 1 つ以上の Handler クラスを実装する必要があります。



```
 In [2]: # %load 03_detailedlogger.py
    ...: from detailedlogger import *
    ...: from logalpha.contrib.standard import StandardHandler
    ...:
    ...: handler = StandardHandler()
    ...: DetailedLogger.handlers.append(handler)
    ...: log = DetailedLogger('custom log')
    ...:
    ...: log.warning('runtime errors')
    ...:
 2021-09-21 13:08:36.572 GoichiMacBook.local WARNING  [custom log] runtime errors
 
```

## まとめ
logalpha を使うとロギング設定が単純になり、開発効率が向上します。

## 参考
- [logalpha ソースコード ](https://github.com/glentner/logalpha)
- [logalpha ドキュメント ](https://logalpha.readthedocs.io/)

#ロギング


