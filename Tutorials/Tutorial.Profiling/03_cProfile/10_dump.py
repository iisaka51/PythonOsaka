import cProfile
import sys
sys.setrecursionlimit(100000)

def ackermann(m, n):
    if m == 0:
        return n + 1
    if n == 0:
        return ackermann(m - 1, 1)
    return ackermann(m - 1, ackermann(m, n - 1))

if __name__ == '__main__':
    pr = cProfile.Profile()
    pr.enable()
    a = ackermann(3, 10)
    pr.disable()
    pr.dump_stats('ackermann.prof')
    print(a)
