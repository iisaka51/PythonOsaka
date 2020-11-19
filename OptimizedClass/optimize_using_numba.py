from numba import jit

def fib_python(n):
    a, b = 0, 1
    for i in range(n):
        a, b = a + b, a
    return a

@jit
def fib_numba(n):
    a, b = 0, 1
    for i in range(n):
        a, b = a + b, a
    return a
