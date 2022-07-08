import numpy as np

x = np.array([0, 1, 2])
y = np.tile(x, (3, 5))
print(y)

z = np.broadcast_to(x, (3, 5))
print(z)

