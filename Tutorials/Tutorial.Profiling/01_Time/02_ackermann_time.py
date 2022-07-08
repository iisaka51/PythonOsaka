import time
import sys
sys.setrecursionlimit(100000)

def ackermann(m, n):
    if m == 0:
        return n + 1
    if n == 0:
        return ackermann(m - 1, 1)
    return ackermann(m - 1, ackermann(m, n - 1))

if __name__ == '__main__':
    t1 = time.time()
    a = ackermann(3, 10)
    calc_time = time.time() - t1
    print(f'{a}: {calc_time:.2f}sec')
