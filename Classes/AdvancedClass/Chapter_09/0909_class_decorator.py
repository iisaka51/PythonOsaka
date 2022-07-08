class MyDecorator:
    def my_decorator(self, func):
        def decorator_wrapper(*args, **kwargs):
            print('before the function called')
            func(*args, **kwargs)
            print('after the function called')
        return decorator_wrapper

decorator = MyDecorator()

@decorator.my_decorator
def my_function(param):
    print(f'my_function called with {param}')

my_function(10)
my_function(20)

