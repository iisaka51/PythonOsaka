import pypeln as pl
import time
from random import random

def slow_add1(x):
    time.sleep(random()) # 遅い処理を想定...
    return x + 1

def main():
    data = range(10) # [0, 1, 2, ..., 9]
    stage = pl.sync.map(slow_add1, data, workers=3, maxsize=4)

    data = list(stage) # e.g. [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(data)

if __name__ == '__main__':
    main()
