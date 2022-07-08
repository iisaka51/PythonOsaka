import sys
sys.setrecursionlimit(100000)

def ackermann(m, n):
    if m == 0:
        return n + 1
    if n == 0:
        return ackermann(m - 1, 1)
    return ackermann(m - 1, ackermann(m, n - 1))

if __name__ == '__main__':
    import  timeit
    t = timeit.timeit('ackermann(3, 10)',
                      'from __main__ import ackermann',
                      number=1)
    print(f'Elapsed: {t}sec')
