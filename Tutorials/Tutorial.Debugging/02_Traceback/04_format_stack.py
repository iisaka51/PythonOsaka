def my_divide(a, b):
    return a / b

if __name__ == '__main__':
    import traceback
    from pprint import pprint
    data = [1,0,2,3]
    for n in data:
        try:
            print(my_divide(1,n))
        except ZeroDivisionError:
            print('# --- format_stack()')
            pprint(traceback.format_stack())
            print('# --- extract_stack()')
            pprint(traceback.extract_stack())
            print('# --- print_stack()')
            pprint(traceback.print_stack())
    print('done.')
