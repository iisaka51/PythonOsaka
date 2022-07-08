class MyDecorator:
    def __init__(self, func):
        print('__init__')
        self.__func = func

    def __call__(self, *args, **kwargs):
        print('__call__')
        result = self.__func(*args, **kwargs)
        return result


@MyDecorator
def my_function(param):
    return f'my_function called with {param}'

print(my_function(10))
print(my_function(20))
