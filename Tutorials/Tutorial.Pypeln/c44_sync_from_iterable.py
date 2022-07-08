import pypeln as pl
import time
from random import random

def slow_gt3(x):
    time.sleep(random()) # 遅い処理を想定...
    return x > 3

def main():
    data = range(10)   # [0, 1, 2, ..., 9]
    stage = pl.sync.from_iterable(data)
    stage = pl.sync.filter(slow_gt3, stage, workers=3, maxsize=4)

    data = list(stage) # e.g. [4, 5, 6, 7, 8, 9]
    print(data)

if __name__ == '__main__':
    main()
