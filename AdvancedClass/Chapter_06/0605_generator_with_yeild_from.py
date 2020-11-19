def mygenerator():
    yield from range(5)
    yield from [10,11,12,13]

for d in mygenerator():
    print(d)
