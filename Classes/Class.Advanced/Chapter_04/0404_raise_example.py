def my_divide(a, b):
    try:
        print(a / b)
    except ZeroDivisionError as e:
        raise(ValueError('Zero Division'))

data = [1,0,2,3]
for n in data:
    try:
        my_divide(1,n)
    except ZeroDivisionError:
        print('ZeroDivisonError Occurs')
    except ValueError:
        print('ValueError Occurs')
