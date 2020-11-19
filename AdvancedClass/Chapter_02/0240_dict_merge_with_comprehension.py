x = {'a':1, 'b':2}
y = {'c':3, 'd':4}

z = {i:d[i] for d in [x,y] for i in d}
print(z)
