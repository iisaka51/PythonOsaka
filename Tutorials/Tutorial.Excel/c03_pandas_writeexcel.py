import pandas as pd

df = pd.read_excel('test.xlsx', index_col=0)

newdf = df[df['Adj Close']<100]
newdf.to_excel('output.xlsx')

df2 = pd.read_excel('output.xlsx', index_col=0)

# print(newdf)
# print(df2)
