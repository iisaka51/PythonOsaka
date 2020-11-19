import numpy as np

a = np.array([[1,2,3], [4,5,6], [7,8,9], [10, 11, 12]])
b = np.array([2, 1, 0, 1])
c = np.arange(4)
d = a[c, b]
e = a[c, b] + 10
