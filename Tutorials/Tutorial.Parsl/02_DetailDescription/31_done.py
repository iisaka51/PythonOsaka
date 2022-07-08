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

# doubled_x1 の状態をチェックし、
# 結果が利用可能であればTrueを、そうでなければFalseを出力します。
print(f'Task 1: {doubled_x1.done()}')
print(f'Task 2: {doubled_x2.done()}')
answer = doubled_x1.result() + doubled_x2.result()

print(f'Task 1: {doubled_x1.done()}')
print(f'Task 2: {doubled_x2.done()}')
print(answer)
