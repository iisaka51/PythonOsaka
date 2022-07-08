import numpy as np
import pandas as pd
import pandas_bokeh

ts = pd.Series(np.random.randn(1000),
               index=pd.date_range('1/1/2000', periods=1000))
df = pd.DataFrame(np.random.randn(1000, 4),
               index=ts.index, columns=list('ABCD'))

df = df.cumsum()
df.plot_bokeh(rangetool=True)
