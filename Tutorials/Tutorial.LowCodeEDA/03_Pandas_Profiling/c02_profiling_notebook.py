import pandas as pd
from pandas_profiling import ProfileReport

df = pd.read_csv('titanic.csv')


# for Jupyterlab
profile = ProfileReport(df)
profile

