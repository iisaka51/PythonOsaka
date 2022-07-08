import parsl
import os
from parsl.app.app import python_app, bash_app

config = parsl.load()

# delay秒遅延して乱数を生成するアプリ
@python_app
def generate(limit,delay):
    from random import randint
    import time
    time.sleep(delay)
    return randint(1,limit)

# 1〜10の間の乱数を５つ生成する
rand_nums = []
for i in range(5):
    rand_nums.append(generate(10,i))

# アプリの終了を待つ
outputs = [i.result() for i in rand_nums]

# 結果の出力
print(outputs)
