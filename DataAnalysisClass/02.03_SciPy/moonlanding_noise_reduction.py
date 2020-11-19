import numpy as np
from scipy import fftpack
import matplotlib.pyplot as plt

im = plt.imread('./moonlanding.png').astype(float)

im_fft = fftpack.fft2(im)

im_fft2 = im_fft.copy()
r, c = im_fft2.shape

keep_fraction = 0.1
im_fft2[int(r*keep_fraction):int(r*(1-keep_fraction))] = 0
im_fft2[:, int(c*keep_fraction):int(c*(1-keep_fraction))] = 0

im_new = fftpack.ifft2(im_fft2).real
plt.imsave('moonlanding_new.png', im_new)
