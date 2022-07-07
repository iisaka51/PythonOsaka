import pandas as pd
import altair as alt
from snapedautility.detect_outliers import detect_outliers


alt.renderers.enable('altair_viewer') # for IPython
# alt.renderers.enable('notebook')      # for Jupyterlab

s = pd.Series([1,1,2,3,4,5,6,9,10,13,40])
error_data, chart = detect_outliers(s)

chart.show()
