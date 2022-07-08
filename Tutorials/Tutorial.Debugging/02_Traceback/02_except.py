def my_divide(a, b):
    return a / b

if __name__ == '__main__':
    data = [1,0,2,3]
    for n in data:
        try:
            print(my_divide(1,n))
        except ZeroDivisionError:
            print('ZeroDivisonError Occurs')
    print('done.')
