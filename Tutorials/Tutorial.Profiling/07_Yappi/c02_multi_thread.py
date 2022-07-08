import yappi
import time
import threading

_NTHREAD = 3

def _work(n):
    time.sleep(n * 0.1)

yappi.start()

threads = []
# スレッドを生成
for i in range(_NTHREAD):
    t = threading.Thread(target=_work, args=(i + 1, ))
    t.start()
    threads.append(t)

# スレッドが終了するのを待つ
for t in threads:
    t.join()

yappi.stop()

# スレッドIDによるスレッド統計情報の取得
threads = yappi.get_thread_stats()
for thread in threads:
    print(
        "Function stats for (%s) (%d)" % (thread.name, thread.id)
    )
    yappi.get_func_stats(ctx_id=thread.id).print_all()
