import time
from contextlib import contextmanager

@contextmanager
def perftest():
    t = time.perf_counter()
    yield None
    perf_time = time.perf_counter() - t
    print(f'Elapsed: {perf_time:.4f}sec')
