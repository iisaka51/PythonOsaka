import pypeln as pl
import asyncio
from random import random

async def slow_add1(x):
    await asyncio.sleep(random()) # <= some slow computation
    return x + 1

async def slow_gt3(x):
    await asyncio.sleep(random()) # <= some slow computation
    return x > 3


async def main():
    data = range(10) # [0, 1, 2, ..., 9]

    stage = pl.task.map(slow_add1, data, workers=3, maxsize=4)
    stage = pl.task.filter(slow_gt3, stage, workers=2)

    data = await stage # e.g. [5, 6, 9, 4, 8, 10, 7]
    print(data)


if __name__ == '__main__':
    asyncio.run(main())
