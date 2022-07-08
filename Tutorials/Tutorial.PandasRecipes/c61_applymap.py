import pandas as pd
import numpy as np

df = pd.read_csv('titanic.csv')
df1 = df.applymap(lambda x: 'True' if x == 'female' else 'False')
