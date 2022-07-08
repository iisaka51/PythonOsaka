import parsl
from parsl.app.app import python_app
from htex_config import htex_config as config

parsl.clear()
conf = parsl.load(config)

@python_app
def sleep_double(x):
    import time
    time.sleep(2)
    return x*2

# doubleed_x1 と doubled_x2 は AppFutures であるため、
# 同時に2つのsleep_doubleアプリを起動します。
doubled_x1 = sleep_double(10)
doubled_x2 = sleep_double(5)

# result()メソッドを呼び出すと、
# 対応する各アプリの呼び出しが完了するまでブロックされます。
answer = doubled_x1.result() + doubled_x2.result()
print(answer)
