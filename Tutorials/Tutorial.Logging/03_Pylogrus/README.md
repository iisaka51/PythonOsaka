pylogrusを使ってロギングをしてみよう
=================

## pylogrus について
PyLogrus は Python 用の構造化ロギングライブラリで、 Golang の [Logrusライブラリ ](https://github.com/sirupsen/logrus) にインスパイアされています。PyLogrus はPython 標準ライブラリの logging モジュールを拡張し、ログの記録を色分けしたり、JSON フォーマットの記録を作成するなどの機能を提供しています。

PyLogrus の機能には’、次のようなものがあります。

- コンソールの出力をカラー化する（テキスト形式）
- 色付けをオフにする (テキスト形式)
- ログ・レコードに追加フィールドを加える
- ログレコードに恒久的にフィールドを追加する
- メッセージに恒久的にプレフィックスを追加する
- 新しいコンテクストインスタンスを作成する
- ログレコードを JSON 形式で保存する
- ログレベルの名前を上書きする
- 基本要素の色を上書きする(テキスト形式)
- キーの名前を上書きする(JSON形式)
- レコードに必要なフィールドのみを定義する (JSON形式)
- レコードの時刻をUTC形式で作成する

## インストール
pylogrus は次のように pip でインストールします。

 bash
```
 $ pip install pylogrus
```

## pylogrus の使用方法

## StreamHandler
次のコードは logging でコンソールへログ出力させるためのものです。


```
 In [2]: # %load 01_streaming_logging.py
    ...: import logging
    ...:
    ...: formatter = logging.Formatter(
    ...:     '%(asctime)s:%(lineno)d:%(name)s:%(levelname)s:%(message)s')
    ...:
    ...: logger = logging.getLogger(__name__)
    ...: handler = logging.StreamHandler()
    ...: handler.setFormatter(formatter)
    ...: logger.addHandler(handler)
    ...: logger.setLevel(logging.DEBUG)
    ...: logger.debug('This is simple test.')
    ...:
 2021-09-24 10:27:01,173:12:__main__:DEBUG:This is simple test.
 
```

これを、pylogrus を使うようにするためには、次のようになります。


```
 In [2]: # %load 02_streaming_pylogrus.py
    ...: import logging
    ...: from pylogrus import PyLogrus, TextFormatter           # 追加
    ...:
    ...: formatter = TextFormatter(datefmt='Z', colorize=True)  # 修正
    ...:
    ...: logging.setLoggerClass(PyLogrus)                       # 追加
    ...: logger = logging.getLogger(__name__)
    ...: handler = logging.StreamHandler()
    ...: handler.setFormatter(formatter)
    ...: logger.addHandler(handler)
    ...: logger.setLevel(logging.DEBUG)
    ...: logger.debug('This is simple test.')
    ...:
 [2021-09-24T10:07:07.620Z]    DEBUG This is simple test.
 
```

 `TextFormatter()` のほとんどデフォルトのフォーマットを使用しているので、ログ出力のフォーマットが微妙に異なっています。もちろん明示的に指定することもできます。
 `TextFormatter()` に  `datefmt='Z'` を与えているのは、ログの時刻をUTC時刻にすることの指示です。

> **トリビア**
> 通信で[通話表 ](https://ja.wikipedia.org/wiki/通話表)の文字 Z に使用する語は Zulu であることから「UTC」を「Z時」や “Zulu time” と表すことがある。

 `logging.setLoggerClass(PyLogrus) ` を呼び出すことと、 `TextFormatter()` でフォマットを定義していること以外は、logging と同じですね。


詳しくは後述しますが、 `TextFormatter()` の他にも `JsonFormatter()` を使うことができます。

## FileHandler
ファイルへ出力する場合も確認してみましょう。次のコードは logging でファイルへ出力するためのものです。


```
 In [2]: # %load 03_filehander_logging.py
    ...: import logging
    ...:
    ...: formatter = logging.Formatter(
    ...:     '%(asctime)s:%(lineno)d:%(name)s:%(levelname)s:%(message)s')
    ...:
    ...: logger = logging.getLogger(__name__)
    ...: handler = logging.FileHandler('sample.log')
    ...: handler.setFormatter(formatter)
    ...: logger.addHandler(handler)
    ...: logger.setLevel(logging.DEBUG)
    ...: logger.debug('This is simple test')
    ...:
    ...: # !cat sample.log
    ...:
 
 In [3]: !cat sample.log
 2021-09-24 10:25:21,391:12:__main__:DEBUG:This is simple tes
 
```



```
 In [2]: # %load 04_filehandler_pylogrus.py
    ...: import logging
    ...: from pylogrus import PyLogrus, TextFormatter           # 追加
    ...:
    ...: formatter = TextFormatter(datefmt='Z', colorize=True)  # 修正
    ...:
    ...: logging.setLoggerClass(PyLogrus)                       # 追加
    ...: logger = logging.getLogger(__name__)
    ...: handler = logging.FileHandler('sample.log')
    ...: handler.setFormatter(formatter)
    ...: logger.addHandler(handler)
    ...: logger.setLevel(logging.DEBUG)
    ...: logger.debug('This is simple test')
    ...:
 
 In [3]: !cat sample.log
 2021-09-24 10:25:21,391:12:__main__:DEBUG:This is simple test
 [2021-09-24T10:32:29.651Z]    DEBUG This is simple test
 
```

同じログファイルへ出力したので、logging との結果と混在しています。
コードはStreamHandlerのときと同じで、ほとんど変更がありません。

## ログメッセージのPREFIX

 `withPrefix()` に与えた文字列がログメッセージの前に付加されます。ログを参照するときに便利になります。


```
 In [2]: # %load 05_withprefix.py
    ...: import logging
    ...: from pylogrus import PyLogrus, TextFormatter
    ...:
    ...: formatter = TextFormatter(datefmt='Z', colorize=True)
    ...:
    ...: logging.setLoggerClass(PyLogrus)
    ...: logger = logging.getLogger(__name__)
    ...: handler = logging.StreamHandler()
    ...: handler.setFormatter(formatter)
    ...: logger.addHandler(handler)
    ...: logger.setLevel(logging.DEBUG)
    ...: logger = logger.withPrefix("[DEMO]")
    ...: logger.debug('This is simple test.')
    ...:
 [2021-09-28T10:35:56.318Z]    DEBUG [DEMO] This is simple test.
 
```

## ログにフィールドを追加
 `withFields()` に与えた辞書の情報を使って、ログにフィールドを追加することができます。


```
 n [2]: # %load 06_wthfield.py
    ...: import logging
    ...: from pylogrus import PyLogrus, TextFormatter
    ...:
    ...: formatter = TextFormatter(datefmt='Z', colorize=True)
    ...: err_code = dict(error_code=404)
    ...:
    ...: logging.setLoggerClass(PyLogrus)
    ...: logger = logging.getLogger(__name__)
    ...: handler = logging.StreamHandler()
    ...: handler.setFormatter(formatter)
    ...: logger.addHandler(handler)
    ...: logger.setLevel(logging.DEBUG)
    ...: logger = logger.withFields(err_code)
    ...: logger.debug('This is simple test.')
    ...:
 [2021-09-28T10:43:35.176Z]    DEBUG This is simple test.; error_code=404
 
```

## JSON形式でログを出力

 `TextFormatter()` の代わりに  `JsonFormatter()` を使うとJSON形式で出力されるようになります。


```
 In [2]: # %load 07_json_formatter.py
    ...: import logging
    ...: from pylogrus import PyLogrus, JsonFormatter
    ...:
    ...: enabled_fields = [
    ...:     ('name', 'logger_name'),
    ...:     ('asctime', 'service_timestamp'),
    ...:     ('levelname', 'level'),
    ...:     ('threadName', 'thread_name'),
    ...:     'message',
    ...:     ('exception', 'exception_class'),
    ...:     ('stacktrace', 'stack_trace'),
    ...:     'module',
    ...:     ('funcName', 'function')
    ...: ]
    ...:
    ...: formatter = JsonFormatter(datefmt='Z',
    ...:                 enabled_fields=enabled_fields, indent=2, sort_keys=True)
    ...:
    ...:
    ...: logging.setLoggerClass(PyLogrus)
    ...: logger = logging.getLogger(__name__)
    ...: handler = logging.StreamHandler()
    ...: handler.setFormatter(formatter)
    ...: logger.addHandler(handler)
    ...: logger.setLevel(logging.DEBUG)
    ...: logger.debug('This is simple test.')
    ...:
 {
   "exception_class": null,
   "function": "<module>",
   "level": "DEBUG",
   "logger_name": "__main__",
   "message": "This is simple test.",
   "module": "<ipython-input-2-a50c17352697>",
   "service_timestamp": "2021-09-28T10:48:19.282Z",
   "stack_trace": null,
   "thread_name": "MainThread"
 }
 
```


## まとめ

pylogrus は logging を利用しながら、機能を補完する位置づけで使用することができます。これは、logging を’使用している既存コードへも無理なく適用できることになります。



## 参考
- [pylogrus ソースコード ](https://github.com/vmig/pylogrus)

#ロギング


