import geopandas as gpd
import pandas as pd
import pandas_bokeh

githuburl = 'https://raw.githubusercontent.com/'
baseurl = 'PatrikHlobil/Pandas-Bokeh/master/docs/Testdata/states/'
url = githuburl + baseurl + 'states.geojson'

df_states = gpd.read_file(url)
df_states.plot_bokeh(simplify_shapes=10000)
