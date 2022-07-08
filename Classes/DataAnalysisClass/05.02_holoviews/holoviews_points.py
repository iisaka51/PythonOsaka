import numpy as np
import pandas as pd
import holoviews as hv
import panel as pn
hv.extension('bokeh', logo=False)

data = np.random.normal(size=[50, 2])
df = pd.DataFrame(data, columns=['col1', 'col2'])

hv_plot = hv.Points(df).opts(width=600, title='Sample Scatter Plot')

bokeh_server = pn.Row(hv_plot).show(port=12345)
bokeh_server.stop()
