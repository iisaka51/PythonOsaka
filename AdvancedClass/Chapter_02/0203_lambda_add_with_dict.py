data = {'a': 4, 'c':2, 'b': 3, 'd': 1}

result=sorted(data.items())
print(result)

result=sorted(data.items(), key=lambda x: x[1])
print(result)
