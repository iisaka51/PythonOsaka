def my_divide(a, b):
    try:
        print(a / b)
    except ZeroDivisionError as e:
        print('ZeroDivisionError:', e)
    else:
        print(f'ELSE: {a} and {b}')
    finally:
        print(f'FINISH: {a} and {b}')

my_divide(1,2)
my_divide(1,0)
