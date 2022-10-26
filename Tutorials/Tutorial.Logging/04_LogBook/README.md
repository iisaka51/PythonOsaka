logbookを使ってロギングをしてみよう
=================
![](images/logbook_logo.png)


## LogBookについて
Logbookは、Python の標準ライブラリのloggingモジュールの代わりに使用できるログシステムです。シンプルなアプリケーションから複雑なアプリケーションまでをカバーできることを考慮して設計されており、ロギングのコードを書くことを楽にするためのアイデアを取り入れています。

### LogBook の特徴
logbook は次のような特徴を持っています。

- Logbookは、アプリケーションによって拡張可能なロガーをコンセプトにしています。。
- 各ロガーとハンドラ、およびシステムの他の部分は、ログエントリの有用性を向上させる追加情報をログレコードに注入することができます。
- ハンドラは、アプリケーション全体のスタックとスレッド全体のスタックに設定できます。ハンドラを設定すると、既存のハンドラを置き換えることはできませんが、より高い優先度が与えられます。各ハンドラーは、レコードが優先順位の低いハンドラーに伝搬するのを防ぐ機能を持っています。
- Logbook には、すべての情報を便利な方法で標準エラーに吐き出すクイックオプション設定が付属しています (環境変数 LOGBOOK_INSTALL_DEFAULT_HANDLER を設定するなど)。これはWebアプリなどに便利になります。
- すべての組み込みハンドラには、便利なデフォルト設定が適用されており、利用可能なすべての情報を、そのハンドラにとって最も意味のある形式で提供するフォーマッタがあります。例えば、デフォルトの `StreamHandler` は、必要な情報をすべて1行にまとめようとしますが、 `MailHandler` は、きれいにフォーマットされたASCIIテーブルに分割して複数行に渡って表示します。
- Logbookには、ストリーム、任意のファイル、時間とサイズに基づいてローテーションされるファイル、メールを配信するハンドラ、syslogデーモンとNTのログファイルのハンドラが組み込まれています。
- また、特別な　 `FingersCrossedHandler` があり、ハンドラスタックと組み合わせて、すべてのログメッセージを蓄積し、深刻度レベルを超えた場合にそれらを配信する機能を持っています。例えば、ウェブアプリケーションへの特定のリクエストに対するすべてのロギングメッセージを、エラーレコードが表示されるまで保留することができます。その場合、保留されたすべてのレコードをラップしているハンドラにも送信します。このようにして、常に多くのデバッグ記録を記録することができますが、 実際に何か興味のあることを教えてくれる場合にのみ、それらを見ることができます。
- アサーション用のメッセージを記録するハンドラをテスト用に注入することも可能です。
- Logbook は高速で、最新の Python 機能を考慮して設計されています。例えば、ハンドラーのスタックを処理するためにコンテキストマネージャを使用したり、すべてのコアログコールに新しいスタイルの文字列フォーマットを採用しています。
- ZeroMQ、RabbitMQ、Redisなど、重度の分散システムや複数のプロセス間でログメッセージを配信することをサポートしていて、そのための関数を内包しています。
- Logbookシステムは、ログレベルに依存しません。実際、カスタム・ログ・レベルはサポートされていません。代わりに、この目的のためにログ・レコードにタグ付き情報を注入するログ・サブクラスまたはログ・プロセッサを使用することを強くお勧めします。
- PEP 8 のネーミングとコード・スタイルに準拠しています。

### LogBook のアドバンテージ
Python 標準モジュールと比較したときのアドバンテージには次のようなものがあります。

- **軽量**：
適切に設定されていれば、Logbookのロギングコールは非常に軽量で、標準ライブラリのロギングモジュールの同等の設定よりも大きなパフォーマンスの向上をもたらします。
- **追加情報の注入が容易**：
特定のスレッドやアプリケーション全体で発生するすべてのロギングコールに対して、追加情報を注入する機能もサポートしています。例えば、Webアプリケーションでは、リモートアドレス、リクエストURL、HTTPメソッドなどのリクエスト固有の情報を各ログレコードに追加することができます。
- **Unitテストが容易**：
ロギングシステムはステートレスで、非常に簡単にユニットテストすることができます。コンテキストマネージャが使用されている場合、各テストはカスタムログハンドラを簡単にフックすることができます。

Python の l標準ライブラリ ogging は必要十分な機能を持っています。それでも、パフォーマンスが問題となるようなときがあります。こうしたときに、[LogBook ](https://logbook.readthedocs.io/) を採用する価値は大きいはずです。

## インストール
logbook は拡張モジュールなので次のようにインストールします。

 bash pipの場合
```
 $ pip install logbook

```


## LogBook を logging のバックエンドにする
例えば次のような logging のコードがあるとします。


```
 In [2]: # %load 01_logging_sample.py
    ...: from logging import getLogger
    ...:
    ...: log = getLogger('My Logger')
    ...: log.warning('This is a warning')
    ...:
 This is a warning

```

 `logbook.compat` をインポートして、 `redirect_logging()` 関数を呼び出すと、これ以後の  `logging` の出力は透過的にLogbookにリダイレクトされます。


```
 In [2]: # %load 02_logging_backend.py
    ...: from logbook import warn, StreamHandler
    ...: from logbook.compat import redirect_logging
    ...:
    ...: redirect_logging()
    ...: StreamHandler(sys.stdout).push_application()
    ...: redirect_logging()
    ...:
    ...: from logging import getLogger
    ...:
    ...: log = getLogger('My Logger')
    ...: log.warning('This is a warning')
    ...:
 [2021-09-23 10:26:03.640789] WARNING: My Logger: This is a warning

```

この結果、logging モジュールからみたときには、LogBook の使い方にはほとんど違いはなくなります。
つまり、既存のコードを大きく修正することなく、ロギングを logbook で処理することができるようになるわけです。

## LogBook の使用方法
基本的なAPIは、Python 標準ライブラリのloggingモジュールとよく似ています。

次のコードは単に標準エラー出力にWARNINGレベルのログを出力するものです。


```
 In [2]: # %load 03_logger_logging.py
    ...: import sys
    ...: import logging
    ...:
    ...: ch = logging.StreamHandler(sys.stderr)
    ...: logger = logging.getLogger('logging demo')
    ...: logger.addHandler(ch)
    ...: logger.warning('Hello Python')
    ...:
 Hello Python

```

これを logbook では次のようになります。


```
 In [2]: # %load 04_logger_logbook.py
    ...: import sys
    ...: from logbook import Logger, StreamHandler
    ...:
    ...: StreamHandler(sys.stderr).push_application()
    ...: log = Logger('logbook demo')
    ...: log.warning('Hello Python')
    ...:
 [2021-09-23 04:12:02.048742] WARNING: logbook demo: Hello Python

```

logbook で実装した方がメッセージの出力が詳細になっていますが、これは logging で実装した方がフォーマットを定義していないためです。

ここで、ロガー(Logger)とは、いわゆるRecordDispatcherのことで、一般的にはロギングチャンネルと呼ばれています。チャンネル名は自由につけることができます。この例では  `"logbook demo"` にしています。このように一意の名前を割り当てておくと、必要に応じてフィルタリングできるようになるので便利です。

ログレベルはいくつかあり、ロガーのメソッドとして利用できます。レベルとその意味は次のとおりです。

 ロガーのレベルとメソッド

| ログレベル | メソッド | 説明 |
|:--|:--|:--|
| CRITICALLY | critical() | 終了につながるエラー用 |
| ERROR | error() | 発生したが処理されたエラー用 |
| WARNING | warning() | エラーではない例外的な状況を表します。 |
| NOTICE | notice() | 通常見たいエラー以外のメッセージ |
| INFO | info() | 通常は表示したくないメッセージを表示します。 |
| DEBUG | debug() | デバッグメッセージ用 |

これらの各レベルは、ロガーのメソッドとして呼び出します。例：WARNINGレベルには  `warning()` を呼び出します。
また、ロギングレベル（文字列または整数）を引数にとる `log()` メソッドもあります。

## ハンドラ（Handler)
ロギング・メソッドを呼び出すたびに、ログ・レコードが作成され、それがハンドラーに渡され、ハンドラーはロギング情報をどのように保存または表示するかを決定します。ハンドラには次のものが提供されています。もちろん独自のハンドラーを作成することもできます。

- 任意のストリームにロギングする	 `StreamHandler`
- 標準エラー出力にロギングする	 `StderrHandler`
- ファイルに記録する
 `FileHandler` 、 `MonitoringFileHandler` 、 `RotatingFileHandler` 、 `TimedRotatingFileHandler`
- メールにログを出力する			 `MailHandler` 、 `GMailHandler`
- syslogデーモンにログを出力する	 `SyslogHandler`
- Windows NTのイベントログに記録する		 `NTEventLogHandler`

他にも特別な用途のためのハンドラーもいくつか用意されています。

-  `logbook.FingersCrossedHandler`
メモリにログを記録し、一定のレベルを超えた場合には別のハンドラに情報を委ね、そうでない場合はバッファリングされたレコードをすべて破棄します。
-  `logbook.more.TaggingHandler` タグ付けされたログレコードをディスパッチするための
- ZeroMQへのロギングのための  `logbook.queues.ZeroMQHandler`
-  `logbook.queues.Redis` Redis`へのロギングのためのRedisHandler
-  `logbook.queues.MultiProcessingHandler` 子プロセスから外側のプロセスのハンドラーにロギングします
-  `logbook.queues.ThreadedWrapperHandler` ハンドラの実際の処理をバックグラウンド・スレッドに移し、そのスレッドにレコードを配信するためにキューを使用します
-  `logbook.notifiers.GrowlHandler` と  `logbook.notifiers.LibNotifyHandler` は、OS XのGrowlやlinuxの通知デーモンにロギングするためのものです。
-  `logbook.notifiers.BoxcarHandler` は、boxcarへのロギングします
-  `logbook.more.TwitterHandler` ：twitterへのロギングします
-  `logbook.more.ExternalApplicationHandler` は、OS Xのsayコマンドのような外部アプリケーションにロギングします
-  `logbook.ticketing.TicketingHandler` データベースやその他のデータストアのログレコードからチケットを作成するためのものです。

## ハンドラーの登録
logbook でのハンドラーの登録は、標準ライブラリのlogging とは少し異なる手順になります。ハンドラは、スレッドやプロセス全体、あるいはロガーに対して個別に登録することができます。しかし、よほどのユースケースがない限り、ロガーにハンドラーを追加しないことを強くお勧めします。

エラーをsyslogに流したい場合は、次のようなコードになります。


```
 In [2]: # %load 04_syslog.py
    ...: from logbook import SyslogHandler
    ...: from bash import bash
    ...:
    ...: error_handler = SyslogHandler('logbook example', level='ERROR')
    ...: with error_handler.applicationbound():
    ...:     # 何かの処理が実行されて
    ...:     # エラーは error_handler へロギングされる
    ...:     bash('ls /tmp/missing_file')
    ...:
```

これにより、すべてのエラーは syslog に送られますが、WARNING や低いレベルのログレコードは標準エラー出力に送られます。これは、ハンドラーがデフォルトではイベントを伝搬（バブリング: Bubbling)しないためで、ハンドラーでレコードが処理されても、上位のハンドラーにはバブリングされないことを意味します。syslogに送られたレコードであっても、すべてのレコードを標準エラー出力に表示したい場合は、 `bubble=True` を与えることでバブリングを有効にすることができます。


```
 In [2]: # %load 05_syslog_bubbling.py
    ...: from logbook import SyslogHandler
    ...: from bash import bash
    ...:
    ...: error_handler = SyslogHandler('logbook example',
    ...:                               level='ERROR', bubble=True)
    ...: with error_handler.applicationbound():
    ...:     # 何かの処理が実行されて
    ...:     # エラーは error_handler へロギングされる
    ...:     bash('ls /tmp/missing_file')
    ...:
```

ERRORのみをsyslogに記録し、標準エラー出力には何も表示させないようにしたい場合はどうでしょうか？
その場合は、NullHandlerと組み合わせて使用します。


```
 In [2]: # %load 06_syslog_null.py
    ...: from logbook import SyslogHandler, NullHandler
    ...: from bash import bash
    ...:
    ...: error_handler = SyslogHandler('logbook example', level='ERROR')
    ...: null_handler = NullHandler()
    ...:
    ...: with null_handler.applicationbound():
    ...:     with error_handler.applicationbound():
    ...:         # 何かの処理が実行されて
    ...:         # ERRORは error_handler に送られる
    ...:         # それ以外はすべてnull handlerに吸収されるため、
    ...:         # デフォルトの stderr ハンドラには何も送られない
    ...:         bash('ls /tmp/missing_file')
    ...:
```

## レコード処理
logbook が楽な理由は、ログの記録を自動的に処理する機能にあります。これは、すべての動作について追加情報を記録したい場合に便利です。例えば、Webアプリケーションで現在のリクエストのIPを記録するような使い方があります。また、デーモンプロセスでは、プロセスのユーザーと作業ディレクトリを記録したい場合もあるかもしれません。

コンテキストプロセッサは次の 2 つの方法でに注入することができます。

- ハンドラと同じようにプロセッサをスタックにバインドする
-  `RecordDispatcher.process_record()` メソッドをオーバーライドする

次のコードは、カレントワーキングディレクトリをログレコードに注入する例を示します。


```
 import os
 from logbook import Processor

 def inject_cwd(record):
     record.extra['cwd'] = os.getcwd()

 with my_handler.applicationbound():
     with Processor(inject_cwd).applicationbound():
         # ここでロギングされたものは、
         # ログレコードにカレントワーキングディレクトリが表示されます。
         pass
```


もう一つの方法は、特定のロガーのだけに情報を注入することで、その場合はそのロガーをサブクラス化することができます。


```
 import os

 class MyLogger(logbook.Logger):

     def process_record(self, record):
         logbook.Logger.process_record(self, record)
         record.extra['cwd'] = os.getcwd()
```


## ロギングフォーマットの設定
すべてのハンドラーには便利なデフォルトのログフォーマットがあり、logbookを使用するために変更する必要はありません。しかし、カスタム情報をログレコードに注入し始めると、その情報を見ることができるようにログフォーマットを設定することが意味を持ちます。

フォーマットを設定するには2つの方法があります: フォーマット文字列を変更するか、カスタムフォーマット関数をフックするかです。

logbookに付属している文字列にログを記録するすべてのハンドラは、 デフォルトではStringFormatterを使用します。コンストラクタは logbook.Handler.format_string 属性を設定したフォーマット文字列を受け入れます。この属性をオーバーライドすることができ、その場合には新しい文字列フォーマッタが設定されます。



```
 from logbook import StderrHandler

 handler = StderrHandler()
 handler.format_string = '{record.channel}: {record.message}'
 handler.formatter

```


また、レコードとハンドラを引数として呼び出すカスタムフォーマット関数を設定することもできます。


```
 def my_formatter(record, handler):
      return record.message

 handler.formatter = my_formatter

```

デフォルトの文字列フォーマッタに使用されるフォーマット文字列には、ログレコードそのものであるrecordという変数があります。すべての属性はドット構文を使用して検索でき、余分なdict内の項目はブラケットを使用して検索できます。存在しないextra dictの項目にアクセスする場合は、空の文字列が返されることに注意してください。

ここでは、前のセクションの例から、現在の作業ディレクトリを表示する設定例を示します。


```
 handler = StderrHandler(format_string=
     '{record.channel}: {record.message) [{record.extra[cwd]}]')

```

logbook.moreモジュールには、Jinja2のテンプレートエンジンを使ってログレコードをフォーマットするフォーマッター(JinjaFormatter)があり、特にメールのような複数行のログフォーマットに便利です。


## ディスクトップアプリケーションでの設定

デスクトップアプリケーション（コマンドラインやGUI）では、次のようなコードをよく目にします。


```
 if __name__ == '__main__':
      main()

```

logbook を使用する場合は、ログハンドラーを設定するために with文でラップする必要があります。


```
 from logbook import FileHandler
 log_handler = FileHandler('application.log')

 if __name__ == '__main__':
     with log_handler.applicationbound():
         main()

```

もしくは、ハンドラーを押し込むこともできます。


```
 from logbook import FileHandler
 log_handler = FileHandler('application.log')
 log_handler.push_application()

 if __name__ == '__main__':
     main()

```

ハンドラをスタックから削除したい場合は、ハンドラを逆の順序でポップする必要があることに留意してください。

## Webアプリケーションの設定
Python で書かれた最近の典型的な Web アプリケーションは、コードが実行される可能性のある 2 つの別々のコンテキストを持っています: コードがインポートされたときと、リクエストが処理されたときです。最初のケースは簡単で、すべてをファイルに書き込むグローバルファイルハンドラをプッシュするだけです。

しかし、Logbookはログを改善する能力も与えてくれます。例えば、追加情報を注入するリクエストバウンドロギングに使用されるログハンドラを簡単に作成することができます。

このためには、ロガーのサブクラスを作成するか、ロギングの前に呼び出される関数でハンドラーにバインドすることができます。後者は、別のライブラリで使用されている可能性のある他のロガーインスタンスでもトリガされるという利点があります。

ここでは、WSGIアプリケーションで発生したエラーに対してエラーメールを送信する簡単なWSGIサンプルアプリケーションをご紹介します。


```
 from logbook import MailHandler

 mail_handler = MailHandler('errors@example.com',
                            ['admin@example.com'],
                            format_string=u'''\
 Subject: Application Error at {record.extra[url]}

 Message type:       {record.level_name}
 Location:           {record.filename}:{record.lineno}
 Module:             {record.module}
 Function:           {record.func_name}
 Time:               {record.time:%Y-%m-%d %H:%M:%S}
 Remote IP:          {record.extra[ip]}
 Request:            {record.extra[url]} [{record.extra[method]}]

 Message:

 {record.message}
 ''', bubble=True)

 def application(environ, start_response):
     request = Request(environ)

     def inject_info(record, handler):
         record.extra.update(
             ip=request.remote_addr,
             method=request.method,
             url=request.url
         )

     with mail_handler.threadbound(processor=inject_info):
         # standard WSGI processing happens here.  If an error
         # is logged, a mail will be sent to the admin on
         # example.com
         ...
```

## 深くネストされたロギング設定
深くネストされたロガー セットアップが必要な場合は、それを単純化する NestedSetup クラスを使用できます。これは、例を使って説明するのが一番です。


```
 import os
 from logbook import NestedSetup, NullHandler, FileHandler, \
      MailHandler, Processor

 def inject_information(record):
     record.extra['cwd'] = os.getcwd()

 # より複雑な設定をするために、ネストされたハンドラー設定を使用することができる。
 setup = NestedSetup([
     # セットアップの処理が足りなくなった場合 stderr ハンドラに到達しないようにする。
     NullHandler(),
     # 少なくとも警告であるメッセージをログファイルに書き込む
     FileHandler('application.log', level='WARNING'),
     # エラーはメールで配信され、アプリケーションログにも記録されます。
     # また、アプリケーションログにも記録されます
     MailHandler('servererrors@example.com',
                    ['admin@example.com'],
                    level='ERROR', bubble=True),
     # 追加の情報を記録するために、プロセッサを独自のスタックにプッシュすることもできます。
     # プロセッサとハンドラは別のスタックに置かれるので、
     # プロセッサが一番下に追加されても、一番最初に追加されても問題ありません。
     # フラグについても同じことが言えます。
     Processor(inject_information)
 ])

```

このような複雑な設定が定義されると、入れ子になったハンドラーの設定は、単一のハンドラーであるかのように使用することができます。


```
 with setup.threadbound():
     # ここでは、すべてが上記のルールに基づいて処理されます。

```


## 分散型ロギング設定
複数のプロセスやマシンに分散しているアプリケーションでは、中央のシステムにログを取るのは面倒なことです。LogbookはZeroMQをサポートしています。ZeroMQパブリッシャーとして動作するZeroMQHandlerを設定し、JSONにエンコードされたログレコードを送信することができます。


```
 from logbook.queues import ZeroMQHandler
 handler = ZeroMQHandler('tcp://127.0.0.1:5000')

```

そして、ログ・レコードを受け取り、ZeroMQSubscriberを使って別のログ・ハンドラーに引き渡すことができる別のプロセスが必要なだけです。通常は次のような設定になります。


```
 from logbook.queues import ZeroMQSubscriber

 subscriber = ZeroMQSubscriber('tcp://127.0.0.1:5000')
 with my_handler:
     subscriber.dispatch_forever()

```

 `dispatch_in_background()` を使って、そのループをバックグラウンドのスレッドで実行することもできます。


```
 from logbook.queues import ZeroMQSubscriber

 subscriber = ZeroMQSubscriber('tcp://127.0.0.1:5000')
 subscriber.dispatch_in_background(my_handler)
```

もし、マルチプロセッシング環境でこれを使用したいのであれば、代わりに `MultiProcessingHandler` と `MultiProcessingSubscriber` を使用することができます。これらは、ZeroMQの同等品と同じように動作しますが、 `multiprocessing.Queue.Subscribe` rを介して接続されます。


```
 from multiprocessing import Queue
 from logbook.queues import MultiProcessingHandler, MultiProcessingSubscriber

 queue = Queue(-1)
 handler = MultiProcessingHandler(queue)
 subscriber = MultiProcessingSubscriber(queue)
```

また、 `RedisHandler` を使ってRedisインスタンスにログインすることもできます。そのためには、以下のようにこのハンドラのインスタンスを作成する必要があります。


```
 import logbook
 from logbook.queues import RedisHandler

 handler = RedisHandler()
 l = logbook.Logger()
 with handler:
     l.info('Your log message')

```

デフォルトのパラメータでは、redisのキーの下にredisにメッセージを送信します。

## 単一のロガーをリダイレクト
単一のロガーを別のログファイルに送りたい場合、2つの方法があります。まず、ハンドラーを特定のレコードディスパッチャにアタッチすることができます。つまり、ロガーをインポートして何かをアタッチすればいいわけです。


```
 from yourapplication.yourmodule import logger
 logger.handlers.append(MyHandler(...))
```

レコード ディスパッチャーに直接接続されたハンドラは、スタック ベースのハンドラよりも常に優先されます。バブルフラグは期待通りに動作しますので、ロガーに非バブルハンドラーがあり、それが常にハンドルする場合、他のハンドラーに渡されることはありません。

次に、ロギングチャンネルを見て、特定の種類のロガーだけを受け入れるハンドラを書くことができます。また、フィルター関数でもそれができます。


```
 handler = MyHandler(filter=lambda r, h: r.channel == 'app.database')
```

チャンネルは人間が読める文字列であることを意図しており、必ずしも一意ではないことに留意してください。もし、ロガーを中央で分離しておく必要がある場合は、追加の辞書にさらにメタ情報を導入するとよいでしょう。

ログレコードのディスパッチャを比較することもできます。


```
 from yourapplication.yourmodule import logger
 handler = MyHandler(filter=lambda r, h: r.dispatcher is logger)
```

しかし、これには、ログレコードのディスパッチャエントリが弱い参照であり、予期せずに消えてしまう可能性があり、ログレコードが別のプロセスに送られた場合には存在しないという欠点があります。

例えば、興味のあるロガーが特定のサブシステムで使用されている場合、システムを呼び出す前にスタックを修正することができます。

## logbook のスタック
現在、logbook は内部で3つのスタックを保持しています。

- Handler用のスタック：各ハンドラーはスタックの上から下に向かって処理されます。レコードが処理されたとき、スタック上の次のハンドラーでまだ処理されるべきかどうかは、ハンドラーの `bubble` フラグに依存します。
- Processors用のスタック：ログレコードがハンドラによって処理される前に、スタック内の各プロセッサがレコードに適用されます。
- Flag用のスタック：このスタックは、ログ記録中のエラーがどのように処理されるべきか、スタックフレームのイントロスペクションが使用されるべきか、などの単純なフラグを管理します。

## 一般的なスタック管理
一般的にスタックで管理されるオブジェクトはすべて共通のインターフェース(StackedObject)を持ち、NestedSetupクラスと組み合わせて使用することができます。

一般的にスタックオブジェクトは、コンテキストマネージャー（with文）と一緒に使われます。


```
 with context_object.threadbound():
     # これはこのスレッドだけで管理される
     # ...

 with context_object.applicationbound():
     # これはすべてのアプリケーションで管理される
     # ...
```

また、try/finallyを使用することもできます。


```
 context_object.push_thread()
 try:
     # これはこのスレッドだけで管理される
     # ...
 finally:
     context_object.pop_thread()

 context_object.push_application()
 try:
     # これはすべてのアプリケーションで管理される
     # ...
 finally:
     context_object.pop_application()
```

アプリケーションが終了するまで変更を持続させたい場合を除き、必ずスタックから再びポップすることが非常に重要です。

複数のスタックされたオブジェクトを同時にプッシュ／ポップしたい場合は、NestedSetupを使用することができます。


```
 setup = NestedSetup([stacked_object1, stacked_object2])
 with setup.threadbound():
     # 両方のオブジェクトがスレッドのスタックにバインドされる
     # ...
```

ログブックの関数やメソッドにスタックオブジェクトが渡されることがあります。任意のスタックオブジェクトを渡すことができる場合、これは通常、セットアップと呼ばれます。例えば、ZeroMQSubscriberのようなものにハンドラーやプロセッサーを指定する場合がこれにあたります。

## ハンドラ(Handler)
ハンドラは、スタックするだけでなく、スタック処理がどのように機能するかを指定するため、スタックの機能を最も利用します。各ハンドラーは、レコードを処理するかどうかを決定することができ、次に、チェーンの次のハンドラーがこのレコードを渡すことになっているかどうかを指定するフラグ（バブルフラグ）を持っています。

ハンドラがバブリングしている場合、レコードが適切に処理されていたとしても、次のハンドラにレコードを渡します。もしそうでなければ、さらに下の階層のハンドラーに進めるのをやめます。さらに、いわゆる「ブラックホール」ハンドラ（NullHandler）があり、それに到達するとどんな場合でも処理を停止します。既存のインフラの上にブラックホールハンドラーをプッシュすれば、パフォーマンスに影響を与えることなく、別のハンドラーを構築することができます。

## プロセッサー(Processor)
プロセッサは、ログレコードが処理される際に、追加情報をログレコードに注入することができます。プロセッサーは、少なくとも1つのログハンドラーがレコードの処理に関心を持つと呼び出されます。それ以前は、処理は行われません。

ここでは、カレントワーキングディレクトリをレコードの追加属性に注入するプロセッサの例を示します。


```
 import os

 def inject_cwd(record):
     record.extra['cwd'] = os.getcwd()

 with Processor(inject_cwd):
     # このスレッドのこのブロック内のすべてのロギングコールには、
     # カレントワーキングディレクトリの情報が添付されるようになる
     # ...
```


## フラグ(Flag)
logbook の最後の柱は、Flagスタックです。このスタックは、ログシステムの設定を上書きするために使用できます。現在のところ、これはログ処理中に例外が発生した場合に、logbookの動作を変更するために使用することができます（例えば、ログレコードがファイルシステムに配信されることになっているが、利用可能なスペースが不足している場合など）。さらに、フレームイントロスペクションを無効にするフラグがあり、これは JIT コンパイルされた Python インタプリタでのスピードアップにつながります。

ここでは、エラーレポートを抑制する例を示します。


```
 with Flags(errors='silent'):
     # このブロックではエラーが発生しない
     # ...
```


## パフォーマンスチューニング
アプリケーションやライブラリにロギングコールを増やせば増やすほど、オーバーヘッドが増えてしまいます。この問題を解決するには、いくつかの方法があります。

## デバッグのみのロギング
デバッグログの呼び出しと、デバッグログの呼び出しがあります。デバッグログ呼び出しの中には、本番環境で興味深いものもあれば、ローカルマシンでコードをいじっているときにしか使えないものもあります。ログブックは、内部的には必要最小限のロギングコールを処理するようにしていますが、それでもアクティブなハンドラーがあるかどうかを把握するために、現在のスタックを歩く必要があります。スタック上のハンドラーの数、ハンドラーの種類などに応じて、処理されるものが多くなったり少なくなったりします。

一般的に言って、処理されないロギング・コールは十分に安いので、気にする必要はありません。しかし、ロギングコールだけではなく、記録のために処理しなければならないデータもあるかもしれません。これは、たとえログレコードが廃棄されることになったとしても、常に処理されます。

ここで、Pythonの__debug__機能が役に立ちます。この変数は、Pythonがスクリプトを処理するタイミングで評価される特別なフラグです。これは、コンパイルされたバイトコードにも存在しないように、スクリプトからコードを完全に取り除くことができます（Pythonを-Oスイッチで実行する必要があります）。


```
 if __debug__:
     info = get_wallcalculate_debug_info()
     logger.debug("Call to response() failed.  Reason: {0}", info)

```

## FingersCrossedHandler
デバッグ情報は本当に必要ですか？エラーが発生したときにログファイルだけを見ているという場合は、FingersCrossedHandlerを入れるのも一つの方法です。メモリへのロギングは、ファイルシステムへのロギングよりも常に安上がりです。

>注) Fingers Crossed：直訳は「指を交差させる」ですが、「幸運・成功を祈ってるよ」や「頑張ってね」を意味になります。これは米国の習慣で、「中指と人差し指を交差する」＝「十字架のシンボル」を表すことに由来しています。Logbook での意味では「ただ見ているだけのハンドラー」ということでしょうか。

## スタックを静的に保持
スタックのプッシュやポップを行うと、logbookが使用している内部キャッシュが無効になります。これは実装上の問題ですが、現時点ではこのような仕組みになっています。つまり、プッシュやポップの後の最初のロギングコールは、それ以降のコールよりもパフォーマンスに大きな影響を与えるということです。つまり、ロギングコールごとにスタックからのプッシュやポップを試みるべきではないということです。必要なときだけプッシュやポップを行うようにしてください。(アプリケーション/リクエストの開始/終了)

## イントロスペクションを無効
デフォルトでは、Logbookは、ロギング関数を呼び出した呼び出し元のインタプリタフレームを引き込もうとします。これは、通常、スクリプトの実行を遅くしない高速な操作ですが、ある種のPythonの実装では、JITコンパイラが関数本体に対して行った仮定を無効にすることも意味します。現在、例えば pypy 上で動作するアプリケーションではこのようなケースがあります。pypy上でストックログブックのセットアップを使用している場合、JITは適切に動作しません。

フレームベースの情報(モジュール名、呼び出し関数、ファイル名、ライン番号)を必要としない場合には、 `introspection=False` を与えてこの機能を無効にすることができます。


```
 from logbook import Flags

 with Flags(introspection=False):
     # ここでのすべてのロギングコールはintrospectionを使用しません。
     ...
```


## まとめ

LogBook は次のような目的では選択肢となるでしょう。

　既存コードのロギングではパフォーマンスに問題がでてくる
　既存コードへの変更点を最小限にしたい


## 参考
- [LogBook オフィシャルサイト ](https://logbook.readthedocs.io/)
- [Python公式ドキュメント loggingモジュール ](https://docs.python.org/3.6/library/logging.html#module-logging)
- [Python 公式ドキュメント - logging クックブック ](https://docs.python.org/ja/3/howto/logging-cookbook.html#logging-cookbook)

#ロギング


