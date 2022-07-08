def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("before the function is called.")
        func(*args, **kwargs)
        print("after the function is called.")
    return wrapper
