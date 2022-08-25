import numpy as np
import pandas as pd

df = pd.read_csv('stockdata.csv')

random_col = np.random.randint(10, size=len(df))
df.insert(3, 'random_col', random_col)
