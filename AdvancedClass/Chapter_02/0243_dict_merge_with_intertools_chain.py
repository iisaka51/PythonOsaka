from itertools import chain

x = {'a':1, 'b':2}
y = {'c':3, 'd':4}

z = dict(chain(x.items(), y.items()))
print(z)
