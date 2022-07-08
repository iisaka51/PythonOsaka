import sched
import threading
import time

scheduler = sched.scheduler(time.time, time.sleep)

# スレッドが変更できるグローバル変数をリセット
counter = 0

def increment_counter(name):
    global counter
    print(f'EVENT: {time.time()} {name}')
    counter += 1
    print(f'NOW: {counter}')

print(f'START: {time.time()}')
ev1 = scheduler.enter(2, 1, increment_counter, ('EV1',))
ev2 = scheduler.enter(3, 1, increment_counter, ('EV2',))

# イベントを実行するスレッドを開始
t = threading.Thread(target=scheduler.run)
t.start()

# メインスレッドに戻り、最初のイベントをキャンセルする
scheduler.cancel(ev1)

# スケジューラのスレッドの実行が終わるまで待つ
t.join()

print(f'FINAL: {counter}')
