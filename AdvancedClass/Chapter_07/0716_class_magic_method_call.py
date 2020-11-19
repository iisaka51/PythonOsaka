class MyClass:
    def __init__(self, arg1, arg2, arg3):
        self.var1 = arg1
        self.var2 = arg2
        self.var3 = arg3

    def __call__(self, *args):
        self.var1, self.var2 = args

obj = MyClass(1, 2, 3)

print(obj.__dict__)
print(id(obj))

print(callable(obj))

obj(20,30)
print(obj.__dict__)
print(id(obj))
