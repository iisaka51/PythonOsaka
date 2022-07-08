import pandas as pd
import pandas_bokeh

baseurl = 'https://github.com/pandas-dev/pandas/raw/master/pandas'
url = baseurl + '/tests/data/iris.csv'
df = pd.read_csv(url)
