import numpy as np

x = np.array([[1,2],[3,4]], dtype=np.float64)
y = np.array([[5,6],[7,8]], dtype=np.float64)

a1 = x + y
a2 = np.add(x, y)

b1 = y - x
b2 = np.subtract(y, x)

c1 = x * y
c2 = np.multiply(x, y)

d1 = x / y
d2 = np.divide(x, y)

e1 = y % x
e2 = np.fmod(y, x)

f1 = y ** x
f2 = np.power(y, x)
