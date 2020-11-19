import pandas as pd

data = pd.read_csv('sample.csv', header=None)
print(data)
print(data.max())
