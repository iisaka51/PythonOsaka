import pypeln as pl
import time
from random import random

def slow_add1(x):
    time.sleep(random()) # <= 遅い計算処理を想定...
    return x + 1

data = range(10)  # [0, 1, 2, ..., 9]
stage = pl.thread.map(slow_add1, data, workers=3, maxsize=4)

for x in stage:
    print(x)      # e.g. 2, 1, 5, 6, 3, 4, 7, 8, 9, 10
