import pypeln as pl
import time
from random import random

def slow_add1(x):
    return x + 1

def slow_gt3(x):
    return x > 3

def main():
    data = range(10) # [0, 1, 2, ..., 9]

    stage = pl.sync.map(slow_add1, data, workers=3, maxsize=4)
    stage = pl.sync.filter(slow_gt3, stage, workers=2)

    data = list(stage) # [4, 5, 6, 7, 8, 9, 10]
    print(data)

if __name__ == '__main__':
    main()
