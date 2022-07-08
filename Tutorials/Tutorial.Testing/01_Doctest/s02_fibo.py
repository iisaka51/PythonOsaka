def fibo(n):
    """
    >>> fibo(8)
    34
    >>> fibo(9)
    55
    """
    if n == 0 or n == 1:
        return 1
    else:
        return fibo(n-1) + fibo(n-2)

if __name__ == '__main__':
    v = fibo(10)
    print(v)
