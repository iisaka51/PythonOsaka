Pythonの関数をタイムアウトさせるときに便利なライブラリ
=================

## タイムアウト
ネットワークプログラミングやWebアプリケーション、GUI/TUIアプリケーションなど、イベント駆動型に分類されるアプリケーションでは、Python の関数を指定した時間を経過するとタイムアウトさせたいときがあります。
そうしたときに使用できる便利なモジュールを紹介します。

いずれも、Python 関数をデコレートして、実行時間の監視したタイムアウト機能を提供します。

- **timeout-decorotor**：マルチスレッド対応
- **timeout-timer**：マルチスレッド対応、コンテキストマネージャとして動作
- **py-timerout**：マルチプロセスベースで実装
- **async-timout**：asyncio互換のタイムアウト・コンテキスト・マネージャ


## timeout-decoratorについて
[timeout-decorator ](https://github.com/pnpnpn/timeout-decorator) は、文字通りデコレートした関数にタイムアウト処理を追加するものです。気の利いた便利なライブラリです。

## インストール
timeout-decorator は pip コマンドでインストールできます。

 bash
```
 $ pip install timeout-decorator
```

## 使用方法
timeout-decorator の使い方は、すごく単純でターゲットの関数に `@timeoout_decorator.timeout()` とアノテーションするだけです。


```
 import time
 import timeout_decorator
 
 @timeout_decorator.timeout(5)
 def mytest():
     print("Start")
     for i in range(1,10):
         time.sleep(1)
         print("{} seconds have passed".format(i))
 
 if __name__ == '__main__':
     mytest()
     
```

タイムアウト時に発生させる別の例外を指定します。


```
 import time
 import timeout_decorator
 
 @timeout_decorator.timeout(5, timeout_exception=StopIteration)
 def mytest():
     print("Start")
     for i in range(1,10):
         time.sleep(1)
         print("{} seconds have passed".format(i))
 
 if __name__ == '__main__':
     mytest()
```

## マルチスレッドでの使用方法
デフォルトでは、timeout-decoratorはシグナルを使って与えられた関数の実行時間を制限します。この方法は、関数がメインスレッドではなく（例えば、ウェブアプリケーションのワーカースレッド）で実行される場合には機能しません。このような場合には、マルチプロセッシングを利用したタイムアウト戦略があります。これを使用するには、 `timeout()` デコレーター関数に  `use_signals=False` を指定します。


```
 import time
 import timeout_decorator
 
 @timeout_decorator.timeout(5, use_signals=False)
 def mytest():
     print "Start"
     for i in range(1,10):
         time.sleep(1)
         print("{} seconds have passed".format(i))
 
 if __name__ == '__main__':
     mytest()
     
```



## timeout-timer
[timeout-timer ](https://github.com/dozysun/timeout-timer) は、関数やステートメントに `timeout()` 関数を追加し、制限時間がなくなった場合に例外を発生させます。コンテキストやデコレータとして動作し、ループの入れ子をサポートし、差分の例外クラスを使用する必要があります。

シグナル・タイムアウト・タイマー(Signal Timeout Timer)とスレッド・タイムアウト・タイマー(Thread Timeout Timer) をサポートしています。シグナル・タイマーはメイン・スレッドでのみ動作し、メイン・スレッドでない場合はスレッド・タイマーを使用します。スレッド・タイマーはタイムアウト秒数よりも長い時間がかかることがありますが、ユーザーの関数がシステムコール（ `time.sleep()` 、 `socket.accept()` など）でビジー状態の場合は、システムコールの終了後に例外が発生します。


## 使用方法


```
 from timeout_timer import timeout, TimeoutInterrupt
 
 class TimeoutInterruptNested(TimeoutInterrupt):
     pass
 
 def test_timeout_nested_loop_both_timeout(timer="thread"):
     cnt = 0
     try:
         with timeout(5, timer=timer):
             try:
                 with timeout(2, timer=timer, exception=TimeoutInterruptNested):
                     sleep(2)
             except TimeoutInterruptNested:
                 cnt += 1
             time.sleep(10)
     except TimeoutInterrupt:
         cnt += 1
     assert cnt == 2
     
```


```
 from timeout_timer import timeout
 
 @timeout(2):
 def f():
     time.sleep(3)
     time.sleep(2)
```



## py-timeout

[py-timeout ](https://github.com/YADRO-KNS/py-timeout) は、Python の関数やメソッドの実行時間でのタイムアウト機能を提供します、純粋な Python のプロセスベースのデコレーターです。シグナルに基づくものではないので、py-timeout はメインスレッドの外でも問題なく動作します。

Python 3.6 以降で動作します。

## インストール
py-timeout は次のようにインストールします。

 bash
```
 $ pip install py-timeout
```

## 使用方法


```
 import timeout
 
 @timeout.timeout(duration=0.5)
 def foo(value: int) -> None:
     ...
 
 ...
 
 @timeout.timeout(duration=0.5)
 def bar(self, value: str) -> str:
     ...
 
 
```

デコレートされた関数またはメソッドは、渡された持続時間値の期待される寿命を持つサブプロセスとして実行されます。


```
 import timeout
 import time
 
 @timeout.timeout(duration=5)
 def foo() -> None:
     while True:
         time.sleep(1)
     
 try:
     foo()
 except timeout.TimeoutException:
     pass
 
```

何らかの理由で実行に時間がかかった場合は、プロセスが終了し、 `TimeoutException` が発生します。


## async-timeout
[async-timeout ](https://github.com/aio-libs/async-timeout) は、asyncio互換のタイムアウト・コンテキスト・マネージャです。
async-timeout コンテキストマネージャは、コードブロックにタイムアウトロジックを適用したい場合や、 `asyncio.wait_for()` が適さない場合に便利です。また、タイムアウトは新しいタスクを作成しないので、 `asyncio.wait_for()` よりもはるかに高速です。


Python 3で動作します。

## インストール
py-timeout は次のようにインストールします。

 bash
```
 $ pip install async-timeout
```

## 使用方法

 `timeout(delay, *, loop=None)` と呼び出すと、 `delay` で指定した時間がすぎるとブロックをキャンセルするコンテキストマネージャーを返します。


```
 async with timeout(1.5):
     await inner()
```

この例の場合、次のように動作します。

-  `inner()` が1.5秒より早く実行された場合、何も起こりません。
- そうでない場合、 `inner()` は  `asyncio.CancelledError` を送って内部的にキャンセルされますが、 `asyncio.TimeoutError` はコンテキストマネージャーのスコープの外で発生します。

 `delay` パラメータに `None` を指定すると、タイムアウト機能をスキップすることができます。

代わりに、 `timeout_at(when)` を使えば、絶対時間でスケジューリングできます。


```
 loop = asyncio.get_event_loop()
 now = loop.time()
 
 async with timeout_at(now + 1.5):
     await inner()
```

これはPOSIX時間ではなく、システムの電源を入れた時間など、定義されていない開始基準の時間であることに注意してください。

コンテキストマネージャには .expired プロパティがあり、コンテキストマネージャでタイムアウトが正確に発生するかどうかを確認できます。


```
 async with timeout(1.5) as cm:
     await inner()
 print(cm.expired)
 
```

このプロパティは、 `inner()` の実行がタイムアウト・コンテキスト・マネージャによってキャンセルされた場合には `True` になります。

 `inner()` の呼び出しが明示的に  `TimeoutError` を発生させた場合、 `cm.expired` は  `False` となります。

スケジュールされた締め切り時間は  `.deadline` プロパティとして利用できます。


```
 async with timeout(1.5) as cm:
     cm.deadline
```

未完了のタイムアウト(Not Finish Yet Timeoout) は、 `shift_by()` や  `shift_to()` メソッドで再スケジューリングできます。


```
 async with timeout(1.5) as cm:
     cm.shift(1)  # add another second on waiting
     cm.update(loop.time() + 5)  # reschedule to now+5 seconds
```




## 参考
- [timeout-decorator ソースコード  ](https://github.com/pnpnpn/timeout-decorator) 
- [timeout-decorator ソースコード  ](https://github.com/pnpnpn/timeout-decorator)
- [py-timeout ソースコード ](https://github.com/YADRO-KNS/py-timeout) 
- [async-timeout ソースコード  ](https://github.com/aio-libs/async-timeout) 


