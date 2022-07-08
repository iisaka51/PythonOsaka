def my_divide(a, b):
    return a / b

if __name__ == '__main__':
    import sys
    from traceback import TracebackException
    data = [1,0,2,3]
    for n in data:
        try:
            print(my_divide(1,n))
        except ZeroDivisionError:
            exc_type, exc_value, exc_tb = sys.exc_info()
            tb = TracebackException(exc_type, exc_value, exc_tb)
            print(''.join(tb.format_exception_only()))
    print('done.')
