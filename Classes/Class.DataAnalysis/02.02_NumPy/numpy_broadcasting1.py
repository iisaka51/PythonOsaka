import numpy as np

x = np.array([[1,2,3], [4,5,6], [7,8,9], [10, 11, 12]])
y = np.empty_like(x)
v1 = np.array([1, 2, 3])

for i in range(4):
    y[i, :] = x[i, :] + v1

print(y)
