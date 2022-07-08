import pandas as pd

df = pd.read_csv('titanic.csv')

fare_orig = df['fare']
top_10 = fare_orig.value_counts().nlargest(10).index
fare_new = fare_orig.where(fare_orig.isin(top_10), other="Other")
v1 = fare_new.value_counts()
