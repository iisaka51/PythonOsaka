イベントスケジューラを使ってみよう
=================
## schedについて
[sched  ](https://docs.python.org/ja/3/library/sched.html#module-sched) モジュールは、特定時刻にタスクを実行する汎用イベントスケジューラを実装します。スケジューラクラスは、現在の時間を知るために time 関数を、一定時間待つために delay 関数を使用します。
schedモジュールを使ってイベントをスケジューリングするには、いくつかの簡単な手順を踏む必要があります。

- schedモジュールの `scheduler()` を使用して、スケジューラインスタンスを作成します。
- スケジューラインスタンスの `enter()` または `enterabs()` メソッドのいずれかを使用してイベントを作成する。
- スケジューラインスタンスの `run()` メソッドを呼び出し、イベントの実行を開始する。

イベントの実行は、スケジューラインスタンスの `run()` メソッドの呼び出し後に開始されることに注意してください。イベントの作成後に `run()` メソッドの呼び出しが遅れたときや、 `run()` を使用してスケジューラを起動した時にイベントの実行時間が既に経過していたときは、イベントの実行も遅れる可能性があります。

イベントは、一定時間後に実行するようにスケジュールできます。遅延させてスケジュールするには、 `sched.enter()` を使用します。 `sched.enter()` は次の引数を受け取ります。

-  `delay` ー 遅延を表す値
-  `priority` ー　優先順位の値
-  `action` 　ー　呼び出す関数
-  `arguments` 　ー　関数の引数のシーケンス（オプション）
-  `kwargs` ー 　関数のキーワード引数を保持する辞書（オプション）

イベントを実行することは、  `action(*argument, **kwargs)` を実行することになります。 `argument` は  `action` のための位置引数を保持するシーケンスを与え、kwargs は  `action` のためのキーワード引数を保持する辞書を与えます。



```
 In [2]: # %load 01_intro.py
    ...: import sched
    ...: import time
    ...:
    ...: scheduler = sched.scheduler(time.time, time.sleep)
    ...: def print_time(arg='default'):
    ...:     print(f'Event: {time.time()} {arg}')
    ...:
    ...: def do_something():
    ...:     print(f'START: {time.time()}')
    ...:     ev1 = scheduler.enter(10, 1, print_time)
    ...:     ev2 = scheduler.enter(5, 2, print_time, argument=('positional',))
    ...:     ev3 = scheduler.enter(5, 1, print_time, kwargs={'arg': 'keyword'})
    ...:     scheduler.run()
    ...:     print(f'END: {time.time()}')
    ...:     return (ev1, ev2, ev3)
    ...:
    ...: ev = do_something()
    ...:
    ...: # print(ev[0])
    ...: # print(ev[1])
    ...: # print(ev[2])
    ...:
 START: 1633066844.615008
 Event: 1633066849.617515 positional
 Event: 1633066849.617617 keyword
 Event: 1633066854.619544 default
 END: 1633066854.619618
 
 In [3]: print(ev[0])
 Event(time=1633066854.6154099, priority=1, action=<function print_time at 0x7fcd453315e0>, argument=(), kwargs={})
 
 In [4]: print(ev[1])
 Event(time=1633066849.615432, priority=2, action=<function print_time at 0x7fcd453315e0>, argument=('positional',), kwargs={})
 
 In [5]: print(ev[2])
 Event(time=1633066849.6154408, priority=1, action=<function print_time at 0x7fcd453315e0>, argument=(), kwargs={'arg': 'keyword'})
 
```


-  `cheduler.enterabs(time, priority, action, argument=(), kwargs={})` 
新しいイベントをスケジュールする

  -  `time` 引数には、コンストラクタに渡された  `timefunc()` 関数の戻り値と互換性のある数値型を指定します。
  - 同じ時間にスケジュールされたイベントは、優先順位の高い順に実行されます。
  - 数字が小さいほど優先順位が高くなります。

イベントの実行とは、 `action(*argument, **kwargs)` を実行することです。
 `argument` は `action` の位置引数を保持するシーケンスです。
 `kwargs` は `action` のキーワード引数を保持する辞書です。

戻り値はイベントで、後でイベントをキャンセルするために使用することができます

-  `scheduler.enter(delay, priority, action, argument=(), kwargs={})` 
delay より多くの時間単位でイベントをスケジュールします。相対時間以外の引数、効果、戻り値はenterabs()のものと同じです。

-  `scheduler.cancel(event)` 
キューからイベントを削除する

-  `scheduler.empty()` 
もしキューが空のときは True を返す

-  `scheduler.run(blocking=True)` 
キューにスケジュールされているイベンtをすべて実行する

-  `scheduler.queue` 
リードオンリーの属性で、実行される順序でイベントが格納されているリスト
各イベントは、  `time` 、  `priority` 、  `action` 、  `argument` 、  `kwargs` の値を持つタプル。

### イベントを重複させる
全てのイベントが処理されるまで run() の呼び出しはブロックされます。それぞれのイベントは同じスレッドで実行されるので、あるイベントがイベント間の遅延時間よりも実行に時間がかかる場合に重複します。このイベントの重複は、それ以降のイベントを延期することで解決されます。イベントがなくなるわけではありませんが、予定した時間よりも遅れてイベントが実行される可能性があります。次の例では、 long_event() は sleep しますが、時間のかかる計算を実行するか、I/O をブロッキングすることで簡単に遅延させられます。


```
 In [2]: # %load 02_long_event.py
    ...: import sched
    ...: import time
    ...:
    ...: scheduler = sched.scheduler(time.time, time.sleep)
    ...:
    ...: def long_event(name):
    ...:     print(f' BEGIN EVENT: {time.time()} {name}')
    ...:     time.sleep(2)
    ...:     print(f'FINISH EVENT: {time.time()} {name}')
    ...:
    ...: print(f'START: {time.time()}')
    ...: ev1 = scheduler.enter(2, 1, long_event, ('first',))
    ...: ev2 = scheduler.enter(3, 1, long_event, ('second',))
    ...: scheduler.run()
    ...: print(f'  END: {time.time()}')
    ...:
 START: 1633066950.749712
  BEGIN EVENT: 1633066952.751495 first
 FINISH EVENT: 1633066954.753462 first
  BEGIN EVENT: 1633066954.7537751 second
 FINISH EVENT: 1633066956.7588632 second
   END: 1633066956.759232
 
```

最初のイベントは2番目のイベントの開始時刻を過ぎるまでかかるため、最初のイベント終了後すぐに2番目のイベントが実行されます。

### イベントの優先度
同じ時間に1つ以上のイベントが予定されている場合、実行する順番を決めるために優先度の値が使用されます。


```
 In [2]: # %load 03_priority.py
    ...: import sched
    ...: import time
    ...:
    ...: scheduler = sched.scheduler(time.time, time.sleep)
    ...:
    ...: def print_event(name):
    ...:     print(f'EVENT: {time.time()} {name}')
    ...:
    ...: now = time.time()
    ...: print(f'START: {now}')
    ...: ev = scheduler.enterabs(now+2, 2, print_event, ('first',))
    ...: ev = scheduler.enterabs(now+2, 1, print_event, ('second',))
    ...: scheduler.run()
    ...: print(f'  END: {time.time()}')
    ...:
 START: 1633067047.576334
 EVENT: 1633067049.5775769 second
 EVENT: 1633067049.5776498 first
   END: 1633067049.577983
 
```


### イベントをキャンセルする
 `enter()` と  `enterabs()` の両方とも、後でキャンセルできるリファレンスを返します。  `run()` はブロックしてしまうので、イベントは違うスレッドからキャンセルさせる必要があります。このサンプルでは、別のスレッドがスケジューラを実行するために開始されて、メイン処理のスレッドがそのイベントをキャンセルするために使用されます。


```
 In [2]: # %load 04_event_cancel.py
    ...: import sched
    ...: import threading
    ...: import time
    ...:
    ...: scheduler = sched.scheduler(time.time, time.sleep)
    ...:
    ...: # スレッドが変更できるグローバル変数をリセット
    ...: counter = 0
    ...:
    ...: def increment_counter(name):
    ...:     global counter
    ...:     print(f'EVENT: {time.time()} {name}')
    ...:     counter += 1
    ...:     print(f'NOW: {counter}')
    ...:
    ...: print(f'START: {time.time()}')
    ...: ev1 = scheduler.enter(2, 1, increment_counter, ('EV1',))
    ...: ev2 = scheduler.enter(3, 1, increment_counter, ('EV2',))
    ...:
    ...: # イベントを実行するスレッドを開始
    ...: t = threading.Thread(target=scheduler.run)
    ...: t.start()
    ...:
    ...: # メインスレッドに戻り、最初のイベントをキャンセルする
    ...: scheduler.cancel(ev1)
    ...:
    ...: # スケジューラのスレッドの実行が終わるまで待つ
    ...: t.join()
    ...:
    ...: print(f'FINAL: {counter}')
    ...:
 START: 1633067320.634683
 EVENT: 1633067323.638434 EV2
 NOW: 1
 FINAL: 1
 
```

2つのイベントが予定されていましたが、最初のイベントはキャンセルされました。2番目のイベントのみ実行されるので、その counter 変数は1回だけインクリメントされます。

 `enterabs()` メソッドを使って、将来のイベントを特定の時間にスケジュールする方法を示します。


```
 In [2]: # %load 05_eventtabs.py
    ...: import sched
    ...: import time
    ...: from datetime import datetime
    ...:
    ...: def time_addition(a,b):
    ...:     print("\nInside Addition : ", datetime.now())
    ...:     print("Time : ", time.monotonic())
    ...:     print("Result : ", a+b)
    ...:
    ...: scheduler = sched.scheduler()
    ...:
    ...: print("Start Time : ", datetime.now(), "\n")
    ...:
    ...: current_time = time.monotonic()
    ...: current_time_plus_5 = current_time + 5
    ...:
    ...: event = scheduler.enterabs(current_time_plus_5, 1,
    ...:                            time_addition, kwargs = {"a":10, "b":20})
    ...:
    ...: print("Current Time  : ", current_time)
    ...:
    ...: print("\nEvent Created : ", event)
    ...: scheduler.run()
    ...:
    ...: print("\nEnd   Time : ", datetime.now())
    ...:
 Start Time :  2021-10-02 08:56:00.819038
 
 Current Time  :  4.304175446
 
 Event Created :  Event(time=9.304175446, priority=1, action=<function time_addition at 0x7f858e8eb670>, argument=(), kwargs={'a': 10, 'b': 20})
 
 Inside Addition :  2021-10-02 08:56:05.819941
 Time :  9.305349228
 Result :  30
 
 End   Time :  2021-10-02 08:56:05.820523
 
```

## schedule を使ってみよう

[schedule ](https://pypi.org/project/schedule/) は人に優しいAPIを持つPythonジョブスケジューリングで、Pythonの関数や他の呼び出し可能なものを、親しみやすい構文で定期的に実行します。次のような特徴があります。

- ジョブスケジューリングのための人間に優しく使いやすいAPIを提供。
- 定期的なジョブのためのインプロセススケジューラで、余分なプロセスが不要。
- 非常に軽量で、外部依存がありません。
- 優れたテストカバレッジ
- Python と 3.6, 3.7, 3.8, 3.9 でテスト済みです。

### schedule が向かないユースケース

scheduleは単純なスケジューリングタスクを実装するためのもので、いくつか向かないユースケースがあります。

- ジョブの永続性（再起動の間、スケジュールを記憶する）
- 正確なタイミング（秒以下の精度での実行）
- 同時実行(複数スレッド)
- ローカライゼーション（タイムゾーン、勤務日、休日）

また、ジョブ機能の実行にかかる時間を考慮しないため、安定した実行スケジュールを保証するためには、長時間実行するジョブをメインスレッド（スケジューラが実行される場所）から別のスレッドに移す必要があります。

### インストール
 bash
```
 $ pip install schedule
```


### schedule の使用方法
schedule の使用方法は、コードをみる方が理解が早いはずなので、ドキュメントからExampleを例示します。

#### 指定した時刻間隔で実行
 `every()` に与えるメソッドに応じた間隔で実行します。


```
 import schedule
 import time
 
 def job():
     print("I'm working...")
 
 # Run job every 3 second/minute/hour/day/week,
 # Starting 3 second/minute/hour/day/week from now
 schedule.every(3).seconds.do(job)
 schedule.every(3).minutes.do(job)
 schedule.every(3).hours.do(job)
 schedule.every(3).days.do(job)
 schedule.every(3).weeks.do(job)
 
 # Run job every minute at the 23rd second
 schedule.every().minute.at(":23").do(job)
 
 # Run job every hour at the 42rd minute
 schedule.every().hour.at(":42").do(job)
 
 # Run jobs every 5th hour, 20 minutes and 30 seconds in.
 # If current time is 02:00, first execution is at 06:20:30
 schedule.every(5).hours.at("20:30").do(job)
 
 # Run job every day at specific HH:MM and next HH:MM:SS
 schedule.every().day.at("10:30").do(job)
 schedule.every().day.at("10:30:42").do(job)
 
 # Run job on a specific day of the week
 schedule.every().monday.do(job)
 schedule.every().wednesday.at("13:15").do(job)
 schedule.every().minute.at(":17").do(job)
 
 while True:
     schedule.run_pending()
     time.sleep(1)
     
```

#### デコレーターによるスケジューリング’
デコレーター `@repeat` を使用してジョブ関数をデコレートすることができます。この場合、 `.do()` の呼び出しは不要です。

 02_using_decorator.py
```
 from schedule import every, repeat, run_pending
 import time
 
 @repeat(every(10).minutes)
 def job():
     print("I am a scheduled job")
 
 while True:
     run_pending()
     time.sleep(1)
     
```

#### ジョブ関数へ引数を渡す
 `.do()` と  `@repeat` はジョブ関数へ引数を渡すことができます。

 03_pass_argument_jon.py
```
 import schedule
 
 def greet(name):
     print('Hello', name)
 
 schedule.every(2).seconds.do(greet, name='Alice')
 schedule.every(4).seconds.do(greet, name='Bob')
 
 from schedule import every, repeat
 
 @repeat(every().second, "World")
 @repeat(every().day, "Mars")
 def hello(planet):
     print("Hello", planet)
     
```

#### ジョブのキャンセル
スケジューラからジョブを削除するには、 `schedule.cancel_job(job)` メソッドを使用します。

 04_cancel_job.py
```
 import schedule
 
 def some_task():
     print('Hello world')
 
 job = schedule.every().day.at('22:30').do(some_task)
 schedule.cancel_job(job)
 
```

#### 1度限りでジョブを実行
ジョブ関数が `schedule.CancelJob` を返すと、スケジューラーからジョブが削除されます。つまり、1度限りで実行されることになります。

 05_run_job_once.py
```
 import schedule
 import time
 
 def job_that_executes_once():
     # Do some work that only needs to happen once...
     return schedule.CancelJob
 
 schedule.every().day.at('22:30').do(job_that_executes_once)
 
 while True:
     schedule.run_pending()
     time.sleep(1)
     
```

#### すべてのジョブを取得
 `schedule.get_jobs()` を呼び出すと、スケジューラからすべてのジョブを取得することができます。

 06_get_all_jobs.py
```
 import schedule
 
 def hello():
     print('Hello world')
 
 schedule.every().second.do(hello)
 
 all_jobs = schedule.get_jobs()
 
```

#### すべてのジョブキャンセル
 `schedule.clear()` を呼び出すと、スケジューラからすべてのジョブを削除することができます。

 07_cancel_all_jobs.py
```
 import schedule
 
 def greet(name):
     print('Hello {}'.format(name))
 
 schedule.every().second.do(greet)
 
 schedule.clear()
 
```

#### 選択したジョブを取得
タグ（一意の識別子となる文字列）を `.tag()` で与えることができます。 `get_jobs()` でタグ与えると、合致するジョブを取得することができます。

 08_get_job_by_filter.py
```
 import schedule
 
 def greet(name):
     print('Hello {}'.format(name))
 
 schedule.every().day.do(greet, 'Andrea').tag('daily-tasks', 'friend')
 schedule.every().hour.do(greet, 'John').tag('hourly-tasks', 'friend')
 schedule.every().hour.do(greet, 'Monica').tag('hourly-tasks', 'customer')
 schedule.every().day.do(greet, 'Derek').tag('daily-tasks', 'guest')
 
 friends = schedule.get_jobs('friend')
 
```

#### 選択したジョブをキャンセル
 `clear()` でタグ与えると、合致するジョブを削除することができます。

 09_canceL_job_by_filer.py
```
 import schedule
 
 def greet(name):
     print('Hello {}'.format(name))
 
 schedule.every().day.do(greet, 'Andrea').tag('daily-tasks', 'friend')
 schedule.every().hour.do(greet, 'John').tag('hourly-tasks', 'friend')
 schedule.every().hour.do(greet, 'Monica').tag('hourly-tasks', 'customer')
 schedule.every().day.do(greet, 'Derek').tag('daily-tasks', 'guest')
 
 schedule.clear('daily-tasks')
 
```

#### ランダムな間隔でジョブを実行
 `every(A).to(B).seconds` は、 `A <= N <= B` となるように、 `N` 秒ごとにジョブ関数を実行します。

 10_ran_job_random_interval.py
```
 def my_job():
     print('Foo')
 
 # Run every 5 to 10 seconds.
 schedule.every(5).to(10).seconds.do(my_job)
 
```

#### 有効期限つきでジョブを実行
 `until()` メソッドは、ジョブの期限を設定することができ、期限を過ぎるとジョブは実行されません。

 11_run_job_until_cerain_time.py
```
 import schedule
 from datetime import datetime, timedelta, time
 
 def job():
     print('Boo')
 
 # run job until a 18:30 today
 schedule.every(1).hours.until("18:30").do(job)
 
 # run job until a 2030-01-01 18:33 today
 schedule.every(1).hours.until("2030-01-01 18:33").do(job)
 
 # Schedule a job to run for the next 8 hours
 schedule.every(1).hours.until(timedelta(hours=8)).do(job)
 
 # Run my_job until today 11:33:42
 schedule.every(1).hours.until(time(11, 33, 42)).do(job)
 
 # run job until a specific datetime
 schedule.every(1).hours.until(datetime(2020, 5, 17, 11, 36, 20)).do(job)
 
```

#### 次のジョブ実行までの秒数を取得
 `schedule.idle_seconds()` を呼び出すと、次のジョブが実行されるまでの秒数を取得します。次のジョブが過去に実行されるようにスケジュールされていた場合、返される値は負数になります。ジョブがスケジュールされていない場合は、 `None` を返します。

 12_time_until_next_exec.py
```
 import schedule
 import time
 
 def job():
     print('Hello')
 
 schedule.every(5).seconds.do(job)
 
 while 1:
     n = schedule.idle_seconds()
     if n is None:
         # no more jobs
         break
     elif n > 0:
         # sleep exactly the right amount of time
         time.sleep(n)
     schedule.run_pending()
     
```

#### すぐにジョブを’実行
 `schedule.run_all()` を呼び出すと、ジョブの実行予定の有無にかかわらず、すべてのジョブを実行することができます。ジョブは終了後、 `run_pending()` を使って実行されたときと同じように再スケジュールされます。


 13_run_job_right_now.py
```
 import schedule
 
 def job_1():
     print('Foo')
 
 def job_2():
     print('Bar')
 
 schedule.every().monday.at("12:40").do(job_1)
 schedule.every().tuesday.at("16:40").do(job_2)
 
 schedule.run_all()
 
 # delay_seconds引数でジョブの実行間隔を何秒か遅らせて実行する
 schedule.run_all(delay_seconds=10)
```

### バックグラウンドでのジョブ実行
schedule 単独ではジョブをバックグラウンドで実行することはできません。バックグランドでジョブを実行したい場合は、自分でスレッドを作成してそこにジョブを移す必要があります。そうすることで、メインスレッドをブロックすることなくジョブを実行することができます。

 20_backgroud.py
```
 import threading
 import time
 import schedule
 
 def run_continuously(interval=1):
     """
     経過時間ごとに保留中のジョブを実行しながら、連続的に実行する。
     戻り値 cease_continuous_run:
         スレッドの連続実行を停止させるために設定できるイベント。
     この関数が失敗したジョブを実行しないことは
      *意図された動作* であることに注意してください。
     例えば、1分毎に実行するジョブを登録して、
     連続実行の間隔を1時間に設定した場合、
     ジョブは各間隔で60回実行されるのではなく、1回だけ実行されます。
     """
     cease_continuous_run = threading.Event()
     class ScheduleThread(threading.Thread):
         @classmethod
         def run(cls):
             while not cease_continuous_run.is_set():
                 schedule.run_pending()
                 time.sleep(interval)
 
     continuous_thread = ScheduleThread()
     continuous_thread.start()
     return cease_continuous_run
 
 def background_job():
     print('Hello from the background thread')
 
 schedule.every().second.do(background_job)
 
 # バックグランドのスレッドを開始
 stop_run_continuously = run_continuously()
 
 # 何かしらの処理
 time.sleep(10)
 
 # バックグランドのスレッドを停止
 stop_run_continuously.set()
 
```


### 並列実行
デフォルトでは、scheduleはすべてのジョブをシリアルに実行します。
次のコードは、10秒ごとに50アイテムを実行しようとしていますが、ログを見ると、10秒スケジュールのすべてのアイテムがシリアルに実行されます。
 21_thread_serial.py
```
 import threading
 import time
 import schedule
 
 def job():
     print("I'm running on thread %s" % threading.current_thread())
 
 def run_threaded(job_func):
     job_thread = threading.Thread(target=job_func)
     job_thread.start()
 
 schedule.every(10).seconds.do(run_threaded, job)
 schedule.every(10).seconds.do(run_threaded, job)
 schedule.every(10).seconds.do(run_threaded, job)
 schedule.every(10).seconds.do(run_threaded, job)
 schedule.every(10).seconds.do(run_threaded, job)
 
 
 while 1:
     schedule.run_pending()
     time.sleep(1)
     
```

各ジョブをそれ自身のスレッドで実行することによって、この制限を回避することができます。
スレッド数をより厳密に制御したい場合は、共有ジョブキューと1つまたは複数のワーカースレッドを使用します。

 22_thread_multi.py
```
 import time
 import threading
 import schedule
 import queue
 
 def job():
     print("I'm working")
 
 
 def worker_main():
     while 1:
         job_func = jobqueue.get()
         job_func()
         jobqueue.task_done()
 
 jobqueue = queue.Queue()
 
 schedule.every(10).seconds.do(jobqueue.put, job)
 schedule.every(10).seconds.do(jobqueue.put, job)
 schedule.every(10).seconds.do(jobqueue.put, job)
 schedule.every(10).seconds.do(jobqueue.put, job)
 schedule.every(10).seconds.do(jobqueue.put, job)
 
 worker_thread = threading.Thread(target=worker_main)
 worker_thread.start()
 
 while 1:
     schedule.run_pending()
     time.sleep(1)
     
```

### 例外処理
schedule は、デフォルトではジョブ実行中に発生した例外をキャッチしません。もし例外を防ぎたいのであれば、ジョブ関数を以下のようなデコレータでラップしてください。

 24_exception_handling.py
```
 import functools
 
 def catch_exceptions(cancel_on_failure=False):
     def catch_exceptions_decorator(job_func):
         @functools.wraps(job_func)
         def wrapper(*args, **kwargs):
             try:
                 return job_func(*args, **kwargs)
             except:
                 import traceback
                 print(traceback.format_exc())
                 if cancel_on_failure:
                     return schedule.CancelJob
         return wrapper
     return catch_exceptions_decorator
 
 @catch_exceptions(cancel_on_failure=True)
 def bad_task():
     return 1 / 0
 
 schedule.every(5).minutes.do(bad_task)
```

他の方法としては、Matt Lewis氏の [safe_schedule.py ](https://gist.github.com/mplewis/8483f1c24f2d6259aef6) の実装例があります。

 safe_schedule.py
```
 mport logging
 from traceback import format_exc
 import datetime
 
 from schedule import Scheduler
 
 logger = logging.getLogger('schedule')
 
 class SafeScheduler(Scheduler):
     """
     失敗したジョブを捕捉し、そのログを記録する Scheduler の実装。
     例外のトレースバックをエラーとし、
     オプションでジョブの再スケジューリングを行います。
     他ののジョブが実行されるかどうか、
     スクリプト全体がクラッシュしないかどうかを、
     気にせずジョブを実行することができます。
     """
     def __init__(self, reschedule_on_failure=True):
         """
         reschedule_on_failure が True の場合は、
         ジョブは正常に終了したかのように、
         次の実行のために再スケジュールされます。
         """
         self.reschedule_on_failure = reschedule_on_failure
         super().__init__()
 
     def _run_job(self, job):
         try:
             super()._run_job(job)
         except Exception:
             logger.error(format_exc())
             job.last_run = datetime.datetime.now()
             job._schedule_next_run()           
```

### ロギング
 `Schedule` は、 `schedule` という名前のPython logger にDEBUGレベルでメッセージを記録します。 `Schedule` からログを受信するには、ロギングレベルをDEBUGに設定します。

 30_logging.py
```
 import schedule
 import logging
 
 logging.basicConfig()
 schedule_logger = logging.getLogger('schedule')
 schedule_logger.setLevel(level=logging.DEBUG)
 
 def job():
     print("Hello, Logs")
 
 schedule.every().second.do(job)
 
 schedule.run_all()
 
 schedule.clear()
 
```

ジョブに再利用可能なロギングを追加する最も簡単な方法は、ロギングを処理するデコレータを実装することです。次のコードでは  `print_elapsed_time` デコレータを追加するものです。

 31_custom_logging.py
```
 import functools
 import time
 import schedule
 
 # このデコレーターを任意のジョブ関数に適用して、
 # 各ジョブの経過時間を記録することができます。
 def print_elapsed_time(func):
     @functools.wraps(func)
     def wrapper(*args, **kwargs):
         start_timestamp = time.time()
         print('LOG: Running job "%s"' % func.__name__)
         result = func(*args, **kwargs)
         print('LOG: Job "%s" completed in %d seconds' % (func.__name__, time.time() - start_timestamp))
         return result
 
     return wrapper
 
 
 @print_elapsed_time
 def job():
     print('Hello, Logs')
     time.sleep(5)
     
```

### 複数のスケジューラ
1つのスケジューラからいくつでもジョブを実行することができます。しかし、大規模なインストールでは、複数のスケジューラを持つことが望ましいかもしれません。schedule は複数のスケジューラを定義することができます。

 40_multi_shceduler.py
```
 import time
 import schedule
 
 def fooJob():
     print("Foo")
 
 def barJob():
     print("Bar")
 
 # 新しいスケジューラーを作成
 scheduler1 = schedule.Scheduler()
 
 # 作成したスケジューラーにジョブを登録
 scheduler1.every().hour.do(fooJob)
 scheduler1.every().hour.do(barJob)
 
 # 2つ目のスケジューラーを作成
 # 必要な数だけ作成することができる
 scheduler2 = schedule.Scheduler()
 scheduler2.every().second.do(fooJob)
 scheduler2.every().second.do(barJob)
 
 while True:
     # run_pending() はすべてのスケジューラで呼び出される必要があります。
     scheduler1.run_pending()
     scheduler2.run_pending()
     time.sleep(1)
 
```


# timeloopを使ってみよう
Timeloopは、一定の間隔を空けて定期的にタスクを実行するためのライブラリです。

各ジョブは独立したスレッドで実行され、サービスの停止時には、現在実行されているすべてのタスクが完了するまで待機します。

## インストール
timeloop は pip で次のようにインストールします。

 zsh
```
 % pip install timeloop
```

## スレッドでジョブを実行する
マルチスレッドでジョブを実行する一般的なコードは次のようになります。


```
 In [2]: # %load 01_threadjob.py
    ...: import threading, time, signal
    ...: from datetime import timedelta
    ...:
    ...: WAIT_TIME_SECONDS = 1
    ...:
    ...: class ProgramKilled(Exception):
    ...:     pass
    ...:
    ...: def foo():
    ...:     print(f'...{time.ctime()}')
    ...:
    ...: def signal_handler(signum, frame):
    ...:     raise ProgramKilled
    ...:
    ...: class Job(threading.Thread):
    ...:     def __init__(self, interval, execute, *args, **kwargs):
    ...:         threading.Thread.__init__(self)
    ...:         self.daemon = False
    ...:         self.stopped = threading.Event()
    ...:         self.interval = interval
    ...:         self.execute = execute
    ...:         self.args = args
    ...:         self.kwargs = kwargs
    ...:
    ...:     def stop(self):
    ...:                 self.stopped.set()
    ...:                 self.join()
    ...:     def run(self):
    ...:             while not self.stopped.wait(self.interval.total_seconds()):
    ...:                 self.execute(*self.args, **self.kwargs)
    ...:
    ...: if __name__ == "__main__":
    ...:     signal.signal(signal.SIGTERM, signal_handler)
    ...:     signal.signal(signal.SIGINT, signal_handler)
    ...:     job = Job(interval=timedelta(seconds=WAIT_TIME_SECONDS), execute=foo
    ...: )
    ...:     job.start()
    ...:
    ...:     while True:
    ...:           try:
    ...:               time.sleep(1)
    ...:           except ProgramKilled:
    ...:               print("Program killed: running cleanup code")
    ...:               job.stop()
    ...:               break
    ...:
 Out[2]: <Handlers.SIG_DFL: 0>
 Out[2]: <function _signal.default_int_handler>
 ...Sat Oct  2 10:19:40 2021
 ...Sat Oct  2 10:19:41 2021
 ...Sat Oct  2 10:19:42 2021
 ...Sat Oct  2 10:19:43 2021
 ...Sat Oct  2 10:19:44 2021
 ...Sat Oct  2 10:19:45 2021
 ...Sat Oct  2 10:19:46 2021
 ...Sat Oct  2 10:19:47 2021
 ...Sat Oct  2 10:19:48 2021
 ^CProgram killed: running cleanup code
 
```

Timeloop を使うとこうしたコードを非常に簡潔に記述できるようになります。]

## Timeloop でジョブの登録
timeloop では、はじめにTimeloopクラスのインスタンスを作成します。この例では、  `tl` です。
ジョブとして登録したい関数に  `@tl.job()` でデコレートします。

 pyton
```
 import time
 
 from timeloop import Timeloop
 from datetime import timedelta
 
 tl = Timeloop()
 
 @tl.job(interval=timedelta(seconds=2))
 def sample_job_every_2s():
     print(f'2s job current time : {time.ctime()}')
 
```

TImeloop クラスは、３つのメソッド、 `job()` 、 `start()` 、 `stop()` を提供しています。
これらのメソッドを見てもシンプルで使いやすいことが理解できるでしょう。


```
 class Timeloop(builtins.object)
  |  Methods defined here:
  |
  |  __init__(self)
  |      Initialize self.  See help(type(self)) for accurate signature.
  |
  |  job(self, interval)
  |
  |  start(self, block=False)
  |
  |  stop(self)
```

## タイムループを別のスレッドで開始する

 `start()` メソッドを呼び出すと、登録されているジョブが開始します。
デフォルトでは、timeloopは別のスレッドで開始されます。
プログラムを終了する前にtl.stopを呼び出すことを忘れないでください。そうしないと、ジョブがうまく終了しません。


```
 In [2]: # %load 01_intro.py
    ...: import time
    ...:
    ...: from timeloop import Timeloop
    ...: from datetime import timedelta
    ...:
    ...: tl = Timeloop()
    ...:
    ...: @tl.job(interval=timedelta(seconds=2))
    ...: def sample_job_every_2s():
    ...:     print(f'2s job current time : {time.ctime()}')
    ...:
    ...: @tl.job(interval=timedelta(seconds=5))
    ...: def sample_job_every_5s():
    ...:     print(f'5s job current time : {time.ctime()}')
    ...:
    ...:
    ...: @tl.job(interval=timedelta(seconds=10))
    ...: def sample_job_every_10s():
    ...:     print(f'10s job current time : {time.ctime()}')
    ...:
    ...: if __name__ == '__main__':
    ...:     tl.start()
    ...:
    ...:     while True:
    ...:         try:
    ...:             time.sleep(1)
    ...:         except KeyboardInterrupt:
    ...:             tl.stop()
    ...:             break
    ...:
 [2021-10-02 09:59:05,859] [timeloop] [INFO] Starting Timeloop..
 [2021-10-02 09:59:05,859] [timeloop] [INFO] Registered job <function sample_job_every_2s at 0x7fe5f1186820>
 [2021-10-02 09:59:05,859] [timeloop] [INFO] Registered job <function sample_job_every_5s at 0x7fe5f1186160>
 [2021-10-02 09:59:05,860] [timeloop] [INFO] Registered job <function sample_job_every_10s at 0x7fe5f1186940>
 [2021-10-02 09:59:05,860] [timeloop] [INFO] Timeloop now started. Jobs will run based on the interval set
 2s job current time : Sat Oct  2 09:59:07 2021
 2s job current time : Sat Oct  2 09:59:09 2021
 5s job current time : Sat Oct  2 09:59:10 2021
 2s job current time : Sat Oct  2 09:59:11 2021
 2s job current time : Sat Oct  2 09:59:13 2021
 10s job current time : Sat Oct  2 09:59:15 2021
 5s job current time : Sat Oct  2 09:59:15 2021
 2s job current time : Sat Oct  2 09:59:15 2021
 2s job current time : Sat Oct  2 09:59:17 2021
 2s job current time : Sat Oct  2 09:59:19 2021
 5s job current time : Sat Oct  2 09:59:20 2021
 2s job current time : Sat Oct  2 09:59:21 2021
 2s job current time : Sat Oct  2 09:59:23 2021
 10s job current time : Sat Oct  2 09:59:25 2021
 5s job current time : Sat Oct  2 09:59:25 2021
 2s job current time : Sat Oct  2 09:59:25 2021
 ^C[2021-10-02 09:59:26,490] [timeloop] [INFO] Stopping job <function sample_job_every_2s at 0x7fe5f1186820>
 [2021-10-02 09:59:26,490] [timeloop] [INFO] Stopping job <function sample_job_every_5s at 0x7fe5f1186160>
 [2021-10-02 09:59:26,490] [timeloop] [INFO] Stopping job <function sample_job_every_10s at 0x7fe5f1186940>
 [2021-10-02 09:59:26,490] [timeloop] [INFO] Timeloop exited.
 
```

## メインスレッドでジョブを実行する
 `start()` メソッドに  `block=True` を与えると、別スレッドを作成せずにジョブを開始します。


```
 In [2]: # %load 03_timeloop_mainthread.py
    ...: import time
    ...: from timeloop import Timeloop
    ...: from datetime import timedelta
    ...:
    ...: tl = Timeloop()
    ...:
    ...: @tl.job(interval=timedelta(seconds=2))
    ...: def sample_job_every_2s():
    ...:     print(f'2s job current time : {time.ctime()}')
    ...:
    ...: @tl.job(interval=timedelta(seconds=5))
    ...: def sample_job_every_5s():
    ...:     print(f'5s job current time : {time.ctime()}')
    ...:
    ...: @tl.job(interval=timedelta(seconds=10))
    ...: def sample_job_every_10s():
    ...:     print(f'10s job current time : {time.ctime()}')
    ...:
    ...: if __name__ == '__main__':
    ...:     tl.start(block=True)
    ...:
 [2021-10-02 10:27:44,761] [timeloop] [INFO] Starting Timeloop..
 [2021-10-02 10:27:44,761] [timeloop] [INFO] Registered job <function sample_job_every_2s at 0x7fb734199040>
 [2021-10-02 10:27:44,762] [timeloop] [INFO] Registered job <function sample_job_every_5s at 0x7fb7341b83a0>
 [2021-10-02 10:27:44,762] [timeloop] [INFO] Registered job <function sample_job_every_10s at 0x7fb7341a6f70>
 [2021-10-02 10:27:44,762] [timeloop] [INFO] Timeloop now started. Jobs will run based on the interval set
 2s job current time : Sat Oct  2 10:27:46 2021
 2s job current time : Sat Oct  2 10:27:48 2021
 5s job current time : Sat Oct  2 10:27:49 2021
 2s job current time : Sat Oct  2 10:27:50 2021
 2s job current time : Sat Oct  2 10:27:52 2021
 10s job current time : Sat Oct  2 10:27:54 2021
 5s job current time : Sat Oct  2 10:27:54 2021
 2s job current time : Sat Oct  2 10:27:54 2021
 ^C[2021-10-02 10:27:55,927] [timeloop] [INFO] Stopping job <function sample_job_every_2s at 0x7fb734199040>
 [2021-10-02 10:27:55,928] [timeloop] [INFO] Stopping job <function sample_job_every_5s at 0x7fb7341b83a0>
 [2021-10-02 10:27:55,928] [timeloop] [INFO] Stopping job <function sample_job_every_10s at 0x7fb7341a6f70>
 [2021-10-02 10:27:55,929] [timeloop] [INFO] Timeloop exited.
 
```


# croniterを使ってみよう

![](https://gyazo.com/5547ad985ab0747986f6939466cb0719.png)

[cronite ](https://github.com/kiorky/croniter) は、cronのような形式でdatetimeオブジェクトの反復処理を行うことができます。

>**cron**
> cron は、Unixで使用されるデーモンサービスで、ジョブ（スクリプト）を自動実行することができます。ログファイルのローテーションや、バックアップなど、定期的に自動実行したいジョブなどに利用されます。

## crontab
cron は [crontab ](https://ja.wikipedia.org/wiki/Crontab) で記述した定義にしたがってでジョブの開始時間を指定することができます。

 zsh
```
 .------------------- minute (0 - 59)
 |   .--------------- hour (0 - 23)
 |   |   .----------- day of month (1 - 31)
 |   |   |   .------- month (1 - 12) or Jan, Feb ... Dec
 |   |   |   |  .---- day of week (0 - 6) or Sun(0 or 7), Mon(1) ... Sat(6)
 V   V   V   V  V
 *   *   *   *  *  実行するコマンド/スクリプト
```

crontab でのジョブの開始時間の指定例

 zsh
```
 0 6 * * * 　　             毎日06:00に実行
 0 6 * * 1                 毎週月曜の 06:00に実行
 0,10 6 * * 1,3,5          毎週月,水,金の 06:00と 06:10に実行
 0-10 6 1 * *              毎月 1日の 06:00から06:10まで 1分毎に実行
 0 0 1,15 * 1              毎月 1日と 15日と 月曜日の 0:00に実行
 0 6 * * 1-5　 　           月曜日から土曜まで 6:00に実行
 0,10,20,30,40,50 * * * *　 10分おきに実行
 */10 * * * * 　　　　　　    10分おきに実行
 * 1 * * *　　　　　　　　     1:00から 1:59まで 1分おきに実行
 0 */1 * * *　　　　   　　　 毎時 0分に 1時間おきに実行
 0 * * * *　　　　　     　　 毎時 0分に 1時間おきに実行
```

このcrontabを確かめるWebサービスもあります。 https://crontab.guru/

## croniter の使用方法
まず、簡単な例を見てみましょう。croniterクラスのインスタンスを生成するときに、crontabを指定します。


```
 In [2]: # %load 01_example.py
    ...: from croniter import croniter
    ...: from datetime import datetime
    ...: import sys
    ...:
    ...: base = datetime(2021, 10, 2, 12, 00)
    ...: cron = croniter('*/2 * * * *', base)  # 2分ごとに実行
    ...:
    ...: print('get_next()...')
    ...: print(cron.get_next(datetime))
    ...: print(cron.get_next(datetime))
    ...: print(cron.get_next(datetime))
    ...:
    ...: print('get_prev()...')
    ...: print(cron.get_prev(datetime))
    ...: print(cron.get_prev(datetime))
    ...: print(cron.get_prev(datetime))
    ...:
 get_next()...
 2021-10-02 12:02:00
 2021-10-02 12:04:00
 2021-10-02 12:06:00
 get_prev()...
 2021-10-02 12:04:00
 2021-10-02 12:02:00
 2021-10-02 12:00:00
 
```


```
 croniter(expr_format, start_time=None, ret_type=<class 'float'>,
          day_or=True, max_years_between_matches=None, is_prev=False, hash_id=None)
```
	

#### 引数
- **expr_format**： crontab の書式でイベント時刻を指定
- **start_time**：開始日時
- **ret_type**

croniterは `start_time` から `cron_format` に沿ってイテレートします。 `day_or` スイッチは、croniterが `day` と `day_of_week` エントリーをどのように扱うかを制御するために使用されます。デフォルトのオプションはcronの動作で、これらの値をORで接続します。 `day_or=False` に設定されていると、値はANDで接続されます。

 `get_next()` と `get_prev()` は、crontab の書式に従って次の値を計算し、 `ret_type` 型のオブジェクトを返します。 `ret_type` は、floatまたはdatetimeオブジェクトです。

 `is_valid()` は与えた crontab の書式が有効かどうかチェックしてブール値を返します。


```
 In [2]: # %load 02_isvalid.py
    ...: from croniter import croniter
    ...:
    ...: v1 = croniter.is_valid('*/2 * * * *')
    ...: v2 = croniter.is_valid('wrang_format * * *')
    ...:
 
 In [3]: v1
 Out[3]: True
 
 In [4]: v2
 Out[4]: False
 
```


## 夏時間(DST)での利用
日本で使用することはあまりないかもしれませんが、crointer は夏時間(DST: Daylight Saving Time)をサポートしています。この場合、プラットフォームがDST をサポートしていることと、タイムゾーンを指定する必要があります。


```
 In [2]: # %load 03_dst_pytz.py
    ...: import pytz
    ...: from croniter import croniter
    ...: from datetime import datetime
    ...:
    ...: tz = pytz.timezone("America/New_York")
    ...: local_date = tz.localize(datetime(2021, 3, 24, 0, 0))
    ...:
    ...: cron = croniter('0 */1 * * *', local_date)
    ...:
    ...: print('get_next()...')
    ...: for i in range(5):
    ...:     print(cron.get_next(datetime))
    ...:
 get_next()...
 2021-03-24 01:00:00-04:00
 2021-03-24 02:00:00-04:00
 2021-03-24 03:00:00-04:00
 2021-03-24 04:00:00-04:00
 2021-03-24 05:00:00-04:00
 
```


```
 In [2]: # %load 04_dst_dateutil.py
    ...: from croniter import croniter
    ...: from datetime import datetime
    ...: import dateutil.tz
    ...:
    ...: tz = dateutil.tz.gettz('Asia/Tokyo')
    ...: local_date = datetime(2021, 3, 14, tzinfo=tz)
    ...: cron = croniter('0 */1 * * *', local_date)
    ...:
    ...: for i in range(5):
    ...:     print(cron.get_next(datetime))
    ...:
 2021-03-14 01:00:00+09:00
 2021-03-14 02:00:00+09:00
 2021-03-14 03:00:00+09:00
 2021-03-14 04:00:00+09:00
 2021-03-14 05:00:00+09:00
 
```

上記の例は実行したマシンでDSTが有効になっていないため、どちらも同じ出力になっています。

 zsh
```
 # timedatectl
       Local time: Sat 2021-10-02 04:32:58 UTC
   Universal time: Sat 2021-10-02 04:32:58 UTC
         RTC time: Sat 2021-10-02 04:32:58
        Time zone: UTC (UTC, +0000)
      NTP enabled: yes
 NTP synchronized: yes
  RTC in local TZ: no
       DST active: n/a
 # timedatectl set-timezone 'America/New_York'
```
　# timedatectl
            - Local time: Sat 2021-10-02 00:36:10 EDT
    - Universal time: Sat 2021-10-02 04:36:10 UTC
                - RTC time: Sat 2021-10-02 04:36:10
              - Time zone: America/New_York (EDT, -0400)
          - NTP enabled: yes
- NTP synchronized: yes
  - RTC in local TZ: no
            - DST active: yes
  - Last DST change: DST began at
                                    - Sun 2021-03-14 01:59:59 EST
                                    - Sun 2021-03-14 03:00:00 EDT
  - Next DST change: DST ends (the clock jumps one hour backwards) at
                                    - Sun 2021-11-07 01:59:59 EDT
                                    - Sun 2021-11-07 01:00:00 EST
　# python 03_dst.py
- get_next()...
- 2021-03-14 01:00:00-05:00
- 2021-03-14 03:00:00-04:00
- 2021-03-14 04:00:00-04:00
- 2021-03-14 05:00:00-04:00
- 2021-03-14 06:00:00-04:00
 
- # python 04_dst_dateutil.py
- 2021-03-14 01:00:00+09:00
- 2021-03-14 02:00:00+09:00
- 2021-03-14 03:00:00+09:00
- 2021-03-14 04:00:00+09:00
- 2021-03-14 05:00:00+09:00

タイムゾーンが `America/New_York' のときは、DSTが始まったときは１時間増えていますが、'Asia/Tokyo'のときは連続した時刻が返されています。

## 複数のcroniter
cronitier は複数回使用することができます。


```
 In [2]: # %load 05_seconds_repeat.py
    ...: from croniter import croniter
    ...: from datetime import datetime
    ...: import dateutil.tz
    ...:
    ...: tz = dateutil.tz.gettz('Asia/Tokyo')
    ...: local_date = datetime(2021, 3, 14, tzinfo=tz)
    ...: cron1 = croniter('* * * * * 1', local_date)
    ...:
    ...: base = datetime(2012, 4, 6, 13, 26, 10)
    ...: cron2 = croniter('* * * * * 15,25', base)
    ...:
    ...: print('1st...')
    ...: for i in range(3):
    ...:     print(cron1.get_next(datetime))
    ...:
    ...: print('2nd...')
    ...: for i in range(3):
    ...:     print(cron2.get_next(datetime))
    ...:
    ...: print('1st again...')
    ...: for i in range(3):
    ...:     print(cron1.get_next(datetime))
    ...:
    ...:
 1st...
 2021-03-14 00:00:01+09:00
 2021-03-14 00:01:01+09:00
 2021-03-14 00:02:01+09:00
 2nd...
 2012-04-06 13:26:15
 2012-04-06 13:26:25
 2012-04-06 13:27:15
 1st again...
 2021-03-14 00:03:01+09:00
 2021-03-14 00:04:01+09:00
 2021-03-14 00:05:01+09:00
```


## 日時がcrontab の書式に合致するかどうかのテスト
 `match()` メソッドを使用すると、日時がcrontab の書式に合致するかテストすることができます。


```
 In [2]: # %load 06_match.py
    ...: from croniter import croniter
    ...: from datetime import datetime
    ...:
    ...: v1 = croniter.match("0 0 * * *", datetime(2019, 1, 14, 0, 0, 0, 0))
    ...: v2 = croniter.match("0 0 * * *", datetime(2019, 1, 14, 0, 2, 0, 0))
    ...:
    ...: dt = datetime(2019, 1, 1, 4, 2, 0, 0)
    ...: # 毎週水曜日 04:02 OR 毎月1日
    ...: v3 = croniter.match("2 4 1 * wed", dt)
    ...:
    ...: # 毎週水曜日 04:02 AND 毎月1日
    ...: v4 = croniter.match("2 4 1 * wed", dt, day_or=False)
    ...:
    ...: assert v1 == True
    ...: assert v2 == False
    ...: assert v3 == True
    ...: assert v4 == False
    ...:
 
 In [3]: !cal 1 2019
     January 2019
 Su Mo Tu We Th Fr Sa
        1  2  3  4  5
  6  7  8  9 10 11 12
 13 14 15 16 17 18 19
 20 21 22 23 24 25 26
 27 28 29 30 31
 
 
```

croniterは次のマッチを見つけようとするときのタイムウィンドウを `max_years_between_matches` 引数で設定できます。、デフォルトは50年です。
ほとんどの場合、このデフォルト値で問題ありません。複数のcron式を評価するアプリケーションや、信頼できないソースやエンドユーザーからのcron式を扱うアプリケーションでは、このパラメータを使用する必要があります。

次の例では、1月1日金曜日の午前4時にマッチします。1月1日が金曜日であることはあまりないので、それぞれの出現には数年の間隔があるかもしれません。制限を15年に設定すると、すべてのマッチが保証されます。


```
 In [2]: # %load 07_max_years_between_matches
    ...: from croniter import croniter
    ...: from datetime import datetime
    ...:
    ...: cron = croniter("0 4 1 1 fri", datetime(2000,1,1),
    ...:                    day_or=False, max_years_between_matches=15)
    ...:
    ...: it = cron.all_next(datetime)
    ...: for i in range(5):
    ...:     print(next(it))
    ...:
 2010-01-01 04:00:00
 2016-01-01 04:00:00
 2021-01-01 04:00:00
 2027-01-01 04:00:00
 2038-01-01 04:00:00
 
```

しかし、今後5年以内の日付にのみ関心がある場合は、上記の例でmax_years_between_matches=5と設定するだけです。これにより、マッチは見つかりませんが、遠い将来の不要なマッチをのためにCPUを浪費することはありません。

## crontab の書式による範囲の反復処理
 `croniter_range()` 関数を使って、範囲内のマッチを見つけます。これは組み込みの `range()` 関数とよく似ていますが、日時を対象としています。step引数にはcronの式を指定します。

2019年の毎月第一土曜日をリストアップ。


```
 In [2]: # %load 08_croniter_range.py
    ...: from croniter import croniter_range
    ...: from datetime import datetime
    ...:
    ...: start_dt = datetime(2019, 1, 1)
    ...: stop_dt = datetime(2019, 12, 31)
    ...: step = "0 0 * * sat#1"
    ...:
    ...: for dt in croniter_range(start_dt, stop_dt, step):
    ...:     print(dt)
    ...:
 2019-01-05 00:00:00
 2019-02-02 00:00:00
 2019-03-02 00:00:00
 2019-04-06 00:00:00
 2019-05-04 00:00:00
 2019-06-01 00:00:00
 2019-07-06 00:00:00
 2019-08-03 00:00:00
 2019-09-07 00:00:00
 2019-10-05 00:00:00
 2019-11-02 00:00:00
 2019-12-07 00:00:00
 
```


## ハッシュ表現
croniterは、 `H` 定義キーワードと必須の  `hash_id` キーワード引数を使ったJenkinsスタイルのハッシュド表現に対応しています。ハッシュ表現は、同じ `hash_id` が与えられていれば一貫性を保ちますが、異なる `hash_id` は互いに全く異なる評価をします。これにより、例えば、異なる名前のジョブを手動で分散させることなく、均等に分散させることができます。


```
 In [2]: # %load 09_hashed_expression.py
    ...: from croniter import croniter
    ...: from datetime import datetime
    ...:
    ...: cronr = croniter("H H * * *", hash_id="hello")
    ...: print(cron.get_next(datetime))
    ...: print(cron.get_next(datetime))
    ...:
    ...: cron = croniter("H H * * *", hash_id="hello")
    ...: print(cron.get_next(datetime))
    ...:
    ...: cron = croniter("H H * * *", hash_id="bonjour")
    ...: print(cron.get_next(datetime))
    ...:
 2021-10-02 11:10:00
 2021-10-03 11:10:00
 2021-10-02 11:10:00
 2021-10-02 20:52:00
 
```

## ランダムな表現
ランダムを表現する `R` 定義キーワードがサポートされており、そのcroniter()インスタンス内でのみ一貫性が保たれます。


```
 In [2]: # %load 10_random_expression.py
    ...: from croniter import croniter
    ...: from datetime import datetime
    ...:
    ...: cron = croniter("R R * * *")
    ...: print(cron.get_next(datetime))
    ...: print(cron.get_next(datetime))
    ...:
    ...: cron = croniter("R R * * *")
    ...: print(cron.get_next(datetime))
    ...:
 2021-10-03 05:04:00
 2021-10-04 05:04:00
 2021-10-03 03:25:00
 
```


## キーワード表現
Vixie cronスタイルの `@` "キーワードに対応しています。 `hash_id` がない場合はVixie cronの定義（正確な時間、分単位）に対応し、 `hash_id` がある場合はJenkinsの定義（期間内のハッシュ化、秒単位）に対応します。

 キーワード表現

| Keyword | hash_id なし | hash_id あり |
|:--|:--|:--|
| @midnight | 0 0 * * * | H H(0-2) * * * H |
| @hourly | 0 * * * * | H * * * * H |
| @daily | 0 0 * * * | H H * * * H |
| @weekly | 0 0 * * 0 | H H * * H H |
| @monthly | 0 0 1 * * | H H H * * H |
| @yearly | 0 0 1 1 * | H H H H * H |
| @annually | 0 0 1 1 * | H H H H * H |

croniter では、Linux の cron で使用される書式に加えて曜日名を指定することは、第2日曜を表現する `sun#2` も使用することができます。


```
 In [2]: # %load 02_format.py
    ...: from croniter import croniter
    ...: from datetime import datetime
    ...: import sys
    ...:
    ...: base = datetime(2021, 10, 2, 12, 00)
    ...:
    ...: print('# 月、金の 04:02')
    ...: cron = croniter('2 4 * * mon,fri', base)
    ...: print(cron.get_next(datetime))
    ...: print(cron.get_next(datetime))
    ...: print(cron.get_next(datetime))
    ...:
    ...: print('# 毎週水曜日と毎月１日の04:02')
    ...: cron = croniter('2 4 1 * wed', base)
    ...: print(cron.get_next(datetime))
    ...: print(cron.get_next(datetime))
    ...: print(cron.get_next(datetime))
    ...:
    ...:
    ...: print('# 毎月1日の水曜日のときの 04:02')
    ...: cron = croniter('2 4 1 * wed', base, day_or=False)
    ...: print(cron.get_next(datetime))
    ...: print(cron.get_next(datetime))
    ...: print(cron.get_next(datetime))
    ...:
    ...: print('# 毎月の第1土曜日と第2日曜日')
    ...: cron = croniter('0 0 * * sat#1,sun#2', base)
    ...: print(cron.get_next(datetime))
    ...: print(cron.get_next(datetime))
    ...: print(cron.get_next(datetime))
    ...:
 # 月、金の 04:02
 2021-10-04 04:02:00
 2021-10-08 04:02:00
 2021-10-11 04:02:00
 # 毎週水曜日と毎月１日の04:02
 2021-10-06 04:02:00
 2021-10-13 04:02:00
 2021-10-20 04:02:00
 # 毎月1日の水曜日のときの 04:02
 2021-12-01 04:02:00
 2022-06-01 04:02:00
 2023-02-01 04:02:00
 # 毎月の第1土曜日と第2日曜日
 2021-10-10 00:00:00
 2021-11-06 00:00:00
 2021-11-14 00:00:00
 
```


croniter 自体はイテレーターを生成するだけなので、実際にジョブを実行させるためには次のようにコードする必要があります。
または、次で説明する aiocron を利用するようにしてください。


```
 # See Also" https://stackoverflow.com/questions/373335/how-do-i-get-a-cron-like-scheduler-in-python
 from croniter import croniter
 from datetime import datetime, timedelta
 
 def roundDownTime(dt=None, dateDelta=timedelta(minutes=1)):
     roundTo = dateDelta.total_seconds()
     if dt == None : dt = datetime.now()
     seconds = (dt - dt.min).seconds
     rounding = (seconds+roundTo/2) // roundTo * roundTo
     return dt + timedelta(0,rounding-seconds,-dt.microsecond)
 
 def getNextCronRunTime(schedule):
     return croniter(schedule, datetime.now()).get_next(datetime)
 
 def sleepTillTopOfNextMinute():
     t = datetime.utcnow()
     sleeptime = 60 - (t.second + t.microsecond/1000000.0)
     time.sleep(sleeptime)
     
 schedule = "*/5 * * * *" # 5分ごとに実行
 
 nextRunTime = getNextCronRunTime(schedule)
 while True:
      roundedDownTime = roundDownTime()
      if (roundedDownTime == nextRunTime):
          # ここじ実行した処理をコード
          nextRunTime = getNextCronRunTime(schedule)
      elif (roundedDownTime > nextRunTime):
          # スケジュール日時に実行できなかったので、再初期化
          nextRunTime = getNextCronRunTime(schedule)
      sleepTillTopOfNextMinute()
 
```


# aiocronを使ってみよう
[aioron ](https://github.com/gawel/aiocron/) は、crontab の書式で指示したタイミングで関数を実行するためのデコレーターを提供します。內部では croniter を利用しています。

## インストール
aiocron は pip コマンドを使って次のよういインストールできます。

 nash
```
 $ pip install aiocron
```

## aiocron をコマンドとして利用する
本来のライブラリとしての利用方法の他に、aiocron はコマンドとしての利用方法も提供されています。
crontab の書式で指定した日時でシェルコマンドを実行することができます。

 bash
```

 Sun Oct  3 08:28:00 JST 2021
 Sun Oct  3 08:30:00 JST 2021
 Sun Oct  3 08:32:00 JST 2021
 
```

 bash
```
  % python -m aiocron --help
 usage: python -m aiocron [-h] [-n N] crontab command [command ...]
 
 positional arguments:
   crontab     quoted crontab. like "* * * * *"
   command     shell command to run
 
 optional arguments:
   -h, --help  show this help message and exit
   -n N        loop N times. 0 for infinite loop
   
```

## aiocron の使用方法
 `crontab()` の引数にcrontab の書式で実行させるタイミングを記述します。
次のコードは２分ごとに時刻を出力するものです。


```
 In [2]: # %load 01_intro.py
    ...: import aiocron
    ...: import asyncio
    ...: from datetime import datetime
    ...:
    ...: @aiocron.crontab('*/2 * * * *')
    ...: async def attime():
    ...:     print(f'{datetime.now()}')
    ...:
    ...: loop = asyncio.get_event_loop()
    ...: try:
    ...:     loop.run_forever()
    ...: except KeyboardInterrupt:
    ...:     loop.close()
    ...:
 2021-10-03 08:35:59.992417
 2021-10-03 08:37:59.989902
 2021-10-03 08:39:59.989782
 ^C
```

オブジェクトの `start()` メソッドを使うこともできます。


```
 In [2]: # %load 02_object.py
    ...: import aiocron
    ...: import asyncio
    ...: from datetime import datetime
    ...:
    ...: @aiocron.crontab('1 9 * * *', start=False)
    ...: async def attime():
    ...:     print(f'{datetime.now()}')
    ...:
    ...: loop = asyncio.get_event_loop()
    ...: try:
    ...:     attime.start()
    ...:     loop.run_forever()
    ...: except KeyboardInterrupt:
    ...:     loop.close()
    ...:
 2021-10-03 09:01:00.002096
 ^C
 
```

作成した関数はattime.funcで引き続き利用可能です。
crontabで与えられたイベント時刻を待つこともできます。この場合、コルーチンは引数を受け取ることができます。


```
 In [2]: # %load 03_corouting.py
    ...: import aiocron
    ...: import asyncio
    ...:
    ...: @aiocron.crontab('0 9,10 * sun,mon', start=False)
    ...: async def attime(i):
    ...:     print('run %i' % i)
    ...:
    ...: async def once():
    ...:     try:
    ...:         res = await attime.next(1)
    ...:     except Exception as e:
    ...:         print('It failed (%r)' % e)
    ...:     else:
    ...:         print(res)
    ...:
    ...: loop = asyncio.get_event_loop()
    ...: try:
    ...:     loop.run_forever()
    ...: except KeyboardInterrupt:
    ...:     loop.close()
    ...:
    
```

最後に、sleepコルーチンとして使うことができます。以下は次のイベント時間まで待ちだけのものです。


```
 await crontab('0 * * * *').next()
```

デコレーターでの記述が気に入らない場合は、自分で呼び出すことができます。


```
 In [2]: # %load 04_crontab.py
    ...: import aiocron
    ...: import asyncio
    ...: from datetime import datetime
    ...:
    ...: async def attime():
    ...:     print(f'{datetime.now()}')
    ...:
    ...: cron = aiocron.crontab('*/2 * * * *', func=attime, start=False)
    ...: loop = asyncio.get_event_loop()
    ...:
    ...: try:
    ...:     cron.start()
    ...:     loop.run_forever()
    ...: except KeyboardInterrupt:
    ...:     loop.close()
    ...:
 2021-10-03 09:30:00.001544
 2021-10-03 09:32:00.001224
 2021-10-03 09:33:59.996777
 ^C
```

## crontab()のAPI

 `crontab(spec, func=None, args=(), start=True, loop=None, tz=None)` 

aiocron は內部で croniter を使用しています。このため、 `crontab()` の loop 以外の引数は croniter に与えるものと同じです。
  - spec には crontab の書式でイベント時刻を指定します。
  - func には関数もしくは実行可能オブジェクトを与えます。
  - tz には タイムゾーンを与えます。
  - loop は asyncio のイベントループを与えます。

## screen によるスケジュール実行
ここまで説明してきたイベントタスク関連のライブラリはデフォルトではバックグランドでサービスする機能を持っていません。FlaskやDjangoなどWebフレームワークと連携させたサービスを開発するなどの方策が’必要になります。
この方法は、"[firefly を使ってWebサービスを実装してみよう]" でも解説しているので参照してみてください。

また、単純なタスクを処理したいのであれば、Linux の [screen ](https://www.gnu.org/software/screen/) コマンドを使うことも方法の1つです。

Ubuntuでのインストール
 bash
```
 $ sudo apt-get update
 $ sudo apt-get install screen
```

RHEL8/Rocky/AlmaLiux でのインストール
 bash
```
 # dnf install epel-release
 # dnf install screen
```

screen を実行して、新しいセッションの起動すると、別のシェルが立ち上がります。

 bash
```
 $ screen
```

 `Ctrl+A d` でデタッチすると screen のセッションを有効にしたまま（プロセスを生かしたまま）抜けることができます。

 bash
```
 iisaka@dev00:~$ screen
 [detached from 2943343.pts-1.dev00]
```

このまま SSH を抜けることができます。
再度ログインしたときは、前回の screen のプロセスIDを  `-r` オプションに与えるとアタッチすることができます。

 bash
```
 $ screen -ls
 There is a screen on:
 	2943343.pts-1.dev00	(03/15/2022 12:19:02 AM)	(Detached)
 1 Socket in /run/screen/S-iisaka.
```

 bash
```
 iisaka@dev00:~$ screen -r 2943343
```

## その他
イベントスケジュールを行う機能を、ライブラリとしてではなくアプリケーションとして探しているのであれば、[Apache AirFlow ](https://airflow.apache.org/) を検討してみてはどうでしょうか？

![](https://gyazo.com/e6b04560581a9cbd33fa40282594c70c.png)

- [Amazon Managed Workflows for Apache Airflow (MWAA) のご紹介 ](https://aws.amazon.com/jp/blogs/news/introducing-amazon-managed-workflows-for-apache-airflow-mwaa/)
  - データ処理パイプラインはそのボリュームを増し、ますます複雑になっていますが、プロセス全体を一連の小さなタスクに分解して簡素化し、これらのタスクの実行をワークフローの一部として調整することができます。その手段として、多くのデベロッパーやデータエンジニアが Apache Airflow を使用しています。Apache Airflow は、コミュニティによって作成され、プログラムによってワークフローを作成、スケジュール、モニタリングするプラットフォームです。Airflow を使用すると、ワークフローをスクリプトとして管理したり、ユーザーインターフェイス (UI) を介してワークフローをモニタリングしたり、強力なプラグインのセットを使用して機能を拡張したりできます。


## 参考
- [sched Python 標準ライブラリ ](https://docs.python.org/ja/3/library/sched.html)
- schedule
  - [PyPI - schedule ](https://pypi.org/project/schedule/)
  - [公式ドキュメント ](https://schedule.readthedocs.io/en/stable/)
- timeloop
  - [PyPI - timeloop ](https://pypi.org/project/timeloop/)
  - [ソースコード ](https://github.com/sankalpjonn/timeloop)
- croniter
  - [PyPI - croniter ](https://pypi.org/project/croniter/)
  - [ソースコード ](https://github.com/kiorky/croniter)
- aiocron
  - [PyPI - aiocron ](https://pypi.org/project/aiocron/)
  - [ソースコード ](https://github.com/gawel/aiocron/)
- screen
  - [ソースコード ](https://www.gnu.org/software/screen/)
  - [SCREEN Quick Reference http://aperiodic.net/screen/quick_reference]
- Apache AirFlow
  - [オフィシャルサイト ](https://airflow.apache.org/)


