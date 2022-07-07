import pandas as pd
import altair as alt
from palmerpenguins import load_penguins
from snapedautility.plot_histograms import plot_histograms

alt.renderers.enable('altair_viewer') # for IPython
# alt.renderers.enable('notebook')      # for Jupyterlab

df = load_penguins()
chart = plot_histograms(df,
           ["bill_length_mm", "bill_depth_mm", 'species'],
           100, 100)
chart.show()
