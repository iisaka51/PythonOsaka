import pandas as pd

df = pd.read_csv('titanic.csv')
df1 = df.copy()

# データフレーム全体を変換
df1 = df1.apply(pd.to_numeric, errors="coerce")

df2 = df.copy()
# 指定したカラムを変換
df2.age = pd.to_numeric(df2.age, errors="coerce")

df3 = df.copy()
# 欠損値をゼロ(0)で埋める
df3.age = pd.to_numeric(df3.age, errors="coerce").fillna(0)

# df1
# df2.age
# df3.age
