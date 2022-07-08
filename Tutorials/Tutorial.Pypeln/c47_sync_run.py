import pypeln as pl
import time
from random import random

def get_data():
    return [1, 2, 3, 4, 5, 6, 7]

def slow_add(x):
    time.sleep(random()) # 遅い処理を想定...
    print(x+1)
    return x + 1

def main():
    data = get_data()
    stage = pl.sync.each(slow_add, data, workers=3)
    pl.process.run(stage)

if __name__ == '__main__':
    main()
