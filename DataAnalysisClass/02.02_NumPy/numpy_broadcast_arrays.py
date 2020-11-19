import numpy as np
from pprint import pprint

x = np.array([0, 1, 2])
y = np.array([[10], [20], [30]])
z = 1

a = np.broadcast_arrays(x, y, z)
pprint(a)
