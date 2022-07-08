import sys

import numpy as np


def mandelbrot(z: complex, max_iter: int):
    c = z
    for n in range(max_iter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return max_iter

def mandelbrot_set(xmin: float, xmax: float,
                   ymin: float, ymax: float,
                   width: int, height: int,
                   max_iter: int):
    horizon = np.linspace(xmin, xmax, width)
    vertical = np.linspace(ymin, ymax, height)
    return (horizon, vertical,
            [mandelbrot(complex(r, i), max_iter)
                for r in horizon for i in vertical] )

dummy = [
    "manny",
    "mo",
    "jack",
]
