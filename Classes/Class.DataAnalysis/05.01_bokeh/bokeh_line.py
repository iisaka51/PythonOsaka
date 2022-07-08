import numpy as np
import pandas as pd
import pandas_bokeh

np.random.seed(42)
df = pd.DataFrame({"Google": np.random.randn(1000)+0.2,
                   "Apple": np.random.randn(1000)+0.17},
                   index=pd.date_range('1/1/2000', periods=1000))
df = df.cumsum()
df = df + 50
df.plot_bokeh(kind="line")
