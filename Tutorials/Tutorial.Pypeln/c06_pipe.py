import pypeln as pl
import time
from random import random

def slow_add1(x):
    time.sleep(random()) # <= some slow computation
    return x + 1

def slow_gt3(x):
    time.sleep(random()) # <= some slow computation
    return x > 3


def main():
    data = (
            range(10)
            | pl.thread.map(slow_add1, workers=3, maxsize=4)
            | pl.thread.filter(slow_gt3, workers=2)
            | list
        )
    print(data)

if __name__ == '__main__':
    main()
