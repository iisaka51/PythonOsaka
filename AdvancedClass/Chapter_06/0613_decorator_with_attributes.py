from myDecorators2 import my_decorator

@my_decorator
def say_hello(name):
    print(f"Hello {name}!")


print(say_hello)
print(say_hello.__name__)
