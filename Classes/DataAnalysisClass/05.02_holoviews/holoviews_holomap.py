import numpy as np
import pandas as pd
import holoviews as hv
import panel as pn
hv.extension('bokeh', logo=False)
import bokeh

hv_plot = hv.HoloMap({i: hv.Curve([1, 2, 3-i], \
               group='Group', label='Label') for i in range(3)},
               'Value')
bokeh_server = pn.Row(hv_plot).show(port=12345)
bokeh_server.stop()
