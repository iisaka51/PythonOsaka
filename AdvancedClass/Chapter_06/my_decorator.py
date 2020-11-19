def my_decorator(func):
    def wrapper():
        print("before the function is called.")
        func()
        print("after the function is called.")
    return wrapper
