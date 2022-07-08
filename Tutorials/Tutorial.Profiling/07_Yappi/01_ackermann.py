import sys
sys.setrecursionlimit(100000)

def ackermann(m, n):
    if m == 0:
        return n + 1
    if n == 0:
        return ackermann(m - 1, 1)
    return ackermann(m - 1, ackermann(m, n - 1))

if __name__ == '__main__':
    import yappi

    yappi.set_clock_type("cpu")
    yappi.start()
    a = ackermann(2, 30)
    yappi.get_func_stats().print_all()
    print(a)
