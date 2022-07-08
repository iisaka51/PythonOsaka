%matplotlib
import numpy as np
import matplotlib.pyplot as plt

X = range(10)
X = np.sin(X) + 1
plt.plot(X)


from sspipe import p, px
range(10) | np.sin(px)+1 | p(plt.plot)
