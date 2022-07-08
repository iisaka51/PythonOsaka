def my_divide(a, b):
    return a / b

if __name__ == '__main__':
    import traceback
    data = [1,0,2,3]
    for n in data:
        try:
            print(my_divide(1,n))
        except ZeroDivisionError:
            print(traceback.format_exc())
    print('done.')
