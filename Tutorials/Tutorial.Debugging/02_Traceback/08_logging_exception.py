def my_divide(a, b):
    return a / b

if __name__ == '__main__':
    import traceback
    import logging
    LOG_FILENAME = 'logging_example.log'
    logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

    data = [1,0,2,3]
    for n in data:
        try:
            print(my_divide(1,n))
        except ZeroDivisionError as e:
            logging.error(e, exc_info=True)
    print('done.')
