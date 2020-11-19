import numpy as np
import pandas as pd
import holoviews as hv
import panel as pn
hv.extension('bokeh', logo=False)
import bokeh

groups = [chr(65+g) for g in np.random.randint(0, 3, 200)]
boxes = hv.BoxWhisker((groups,
                       np.random.randint(0, 5, 200),
                       np.random.randn(200)),
                      ['Group', 'Category'], 'Value').sort()

boxes.opts(width=600)

bokeh_server = pn.Row(boxes).show(port=12345)
bokeh_server.stop()
