from color import *

for fore in FORES:
    for back in BACKS:
        for brightness in BRIGHTNESS:
            cprint("Python", color=back+fore, brightness=brightness, end=' ')
