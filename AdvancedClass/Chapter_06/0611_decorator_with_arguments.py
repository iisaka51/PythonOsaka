from my_decorators import my_decorator

@my_decorator
def say_hello(name):
    print(f"Hello {name}!")

say_hello('Python')

