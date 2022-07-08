import numpy as np
import pandas as pd
import holoviews as hv
import panel as pn
hv.extension('bokeh', logo=False)
import bokeh

data = [(i, chr(97+j),  i*j) for i in range(5) for j in range(5) if i!=j]
hv_plot = hv.HeatMap(data).sort()
hv_plot.opts(xticks=None)

bokeh_server = pn.Row(hv_plot).show(port=12345)
bokeh_server.stop()
