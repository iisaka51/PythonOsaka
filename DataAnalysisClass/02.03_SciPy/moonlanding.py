import numpy as np
import matplotlib.pyplot as plt

im = plt.imread('./moonlanding.png').astype(float)

plt.figure()
plt.imshow(im, plt.cm.gray)
plt.title('Original image')
