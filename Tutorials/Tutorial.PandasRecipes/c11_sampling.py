import pandas as pd

df = pd.read_csv('stockdata.csv')
df.sample(3)
df.sample(2)
df.sample(1)
