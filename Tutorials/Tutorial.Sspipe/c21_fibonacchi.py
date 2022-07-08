from sspipe import p, px

def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

v1 = (fib() | p.where(lambda x: x % 2 == 0)
            | p.take_while(lambda x: x < 4000000)
            | p.add())

v2 = (fib() | p.where(px % 2 == 0)
            | p.take_while(px < 4000000)
            | p.add())
