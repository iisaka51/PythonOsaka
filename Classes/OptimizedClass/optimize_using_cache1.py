def fibo(n):
    if n<2:
        return n
    return fibo(n-1)+fibo(n-2)

from functools import lru_cache as cache
@cache(maxsize=None)
def fibo_cache(n):
    if n<2:
        return n
    return fibo_cache(n-1)+fibo_cache(n-2)
