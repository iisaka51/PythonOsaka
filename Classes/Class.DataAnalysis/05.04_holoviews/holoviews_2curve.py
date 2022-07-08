import numpy as np
import pandas as pd
import holoviews as hv
import panel as pn
hv.extension('bokeh', logo=False)
import bokeh

semilogy = hv.Curve(np.logspace(0, 5),
                    label='Semi-log y axes')
loglog = hv.Curve((np.logspace(0, 5), np.logspace(0, 5)),
                    label='Log-log axes')

hv_plot = semilogy.opts(logy=True) + \
          loglog.opts(logx=True, logy=True, shared_axes=False)

bokeh_server = pn.Row(hv_plot).show(port=12345)
bokeh_server.stop()
