import parsl
from parsl.app.app import python_app, bash_app
from parsl.configs.local_threads import config

config = parsl.load()

@python_app
def pi(num_points):
    from random import random

    inside = 0
    for i in range(num_points):
        x, y = random(), random()  # ボックスにランダムな点をうつ
        if x**2 + y**2 < 1:        # 円の中にポイントがあるかチェック
            inside += 1

    return (inside*4 / num_points)

# ３つの値の平均値を計算するアプリ
@python_app
def mean(a, b, c):
    return (a + b + c) / 3

# pi の近似値を求める
a, b, c = pi(10**6), pi(10**6), pi(10**6)

# 3つの値の平均を求める
mean_pi  = mean(a, b, c)

# 結果の出力
print(f"a: {a.result():.5f} b: {b.result():.5f} c: {c.result():.5f}")
print(f"Average: {mean_pi.result():.5f}")
