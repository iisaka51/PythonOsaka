import numpy as np
import pandas as pd
import holoviews as hv
import panel as pn
hv.extension('bokeh', logo=False)
import bokeh
from bokeh.sampledata.stocks import GOOG, AAPL

goog_stock = np.array(GOOG['date'], dtype=np.datetime64)
aapl_stock = np.array(AAPL['date'], dtype=np.datetime64)

goog = hv.Curve((goog_stock, GOOG['adj_close']),
                'Date', 'Stock Index', label='Google')
aapl = hv.Curve((aapl_stock, AAPL['adj_close']),
                'Date', 'Stock Index', label='Apple')

hv_plot = (goog * aapl).opts(width=600, legend_position='top_left')
bokeh_server = pn.Row(hv_plot).show(port=12345)
bokeh_server.stop()
