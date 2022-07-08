import inspect

def my_function():
    filename = inspect.stack()[1][1]
    line = inspect.stack()[1][2]
    method = inspect.stack()[1][3]

    print(f'Method not implemented: {method} at line: {line} of {filename}')

_ = my_function()
