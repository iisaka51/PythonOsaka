import inspect

filepath = inspect.getfile(lambda: None)
print(filepath)
