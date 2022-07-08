def func1():
    data = [1.0 / x for x in [3, 2, 1, 0]]
    for x in data:
        print(x)

def func2():
    data = (1.0 / x for x in [3, 2, 1, 0])
    for x in data:
        print(x)

