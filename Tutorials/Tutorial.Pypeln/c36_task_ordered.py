import pypeln as pl
import random
import time

def slow_squared(x):
    time.sleep(random.random())

    return x ** 2

def main():
    stage = range(5)
    stage = pl.task.map(slow_squared, stage, workers = 2)
    stage = pl.task.ordered(stage)

    print(list(stage)) # [0, 1, 4, 9, 16]

if __name__ == '__main__':
    main()
