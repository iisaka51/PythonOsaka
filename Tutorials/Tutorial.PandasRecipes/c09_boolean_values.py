import pandas as pd

df1 = pd.read_csv("titanic.csv")
df2 = pd.read_csv("titanic.csv",
                   true_values=["female"], false_values=["male"])

# df1['sex'].head()
# df2['sex'].head()
