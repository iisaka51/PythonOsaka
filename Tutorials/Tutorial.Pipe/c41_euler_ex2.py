from pipe import where, take_while

def fib(n):
    a, b = 0, 1
    while a <= n:
        yield a
        a, b = b, a + b

euler2 = sum(fib(400_0000) | where(lambda x: x % 2 == 0))

assert euler2 == 4613732
