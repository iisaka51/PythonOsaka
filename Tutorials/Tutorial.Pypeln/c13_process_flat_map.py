import pypeln as pl
import time
from random import random

def slow_integer_pair(x):
    time.sleep(random()) # 遅い処理を想定...

    if x == 0:
        yield x
    else:
        yield x
        yield -x

def main():
    data = range(10) # [0, 1, 2, ..., 9]
    stage = pl.process.flat_map(
                   slow_integer_pair, data, workers=3, maxsize=4)

    v = list(stage) # e.g. [2, -2, 3, -3, 0, 1, -1, 6, -6, 4, -4, ...]
    print(v)

if __name__ == '__main__':
    main()

