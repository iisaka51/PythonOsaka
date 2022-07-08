import pandas as pd

baseurl = 'https://github.com/pandas-dev/pandas/raw/master/pandas'
url = baseurl + '/tests/data/iris.csv'
df = pd.read_csv(url)
