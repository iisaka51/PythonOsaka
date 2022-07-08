import numpy as np
import holoviews as hv

logo = hv.RGB.load_image('./holoviews_logo.png', array=True)
print(f'{type(logo)} with shape {logo.shape}')

rgb_logo = hv.RGB(logo, label='HoloViews Logo')
rgb_logo
