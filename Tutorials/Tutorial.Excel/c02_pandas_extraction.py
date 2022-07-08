import pandas as pd

df = pd.read_excel('test.xlsx', index_col=0)

newdf = df[df['Adj Close']<100]

# print(newdf)
