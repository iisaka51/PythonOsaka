import pypeln as pl
import time
from random import random

def slow_gt3(x):
    time.sleep(random()) # 遅い処理を想定...
    return x > 3

def main():
    data = range(10)   # [0, 1, 2, ..., 9]
    stage = pl.task.filter(slow_gt3, data, workers=3, maxsize=4)

    data = pl.task.to_iterable(stage)
    d = list(data)
    print(d)

if __name__ == '__main__':
    main()
