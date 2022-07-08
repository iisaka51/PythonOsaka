data = [1, 2, 3]

def simpleGenerator():
    yield 1
    yield 2
    yield 3

for value in data:
    print(value)

for value in simpleGenerator():
    print(value)
