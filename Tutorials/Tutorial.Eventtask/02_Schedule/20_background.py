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
