import pandas as pd
import sqlite3 as sqlite

df = pd.read_csv('data.csv', index_col=0)

conn = sqlite.connect('data.sqlite3')
df.to_sql(name='User', con=conn)
