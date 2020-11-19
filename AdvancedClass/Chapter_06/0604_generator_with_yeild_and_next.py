def fibonacci(max):
    a, b = 1, 1
    a, b = b, a + b
    while a < max:
        yield a
        a, b = b, a + b

x = fibonacci(30)

print(type(x))
print(x.__next__())
print(x.__next__())
print(x.__next__())
print(next(x))
print(next(x))
print(next(x))

print('Call with for loop')
for i in fibonacci(30):
    print(i)
