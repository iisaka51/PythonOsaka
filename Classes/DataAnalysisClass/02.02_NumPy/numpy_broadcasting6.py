import numpy as np

x = np.array([0, 1, 2])
y = np.broadcast_to(x, (4, 3))

print(y)
