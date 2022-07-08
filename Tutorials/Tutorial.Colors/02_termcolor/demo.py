from color import *

for fore in FORES:
    for back in BACKS:
        for style in STYLES:
            cprint("Python", color=fore, on_color=back,
                             attrs=[style], end=' ')
