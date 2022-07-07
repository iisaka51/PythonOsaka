import pandas as pd
from pandas_profiling import ProfileReport

df = pd.read_csv('titanic.csv')

profile = ProfileReport(df,
                 vars={"num": {"low_categorical_threshold": 0}})
profile.to_file('titanic.html')
