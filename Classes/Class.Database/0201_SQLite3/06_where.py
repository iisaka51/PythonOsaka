import sqlite3
from pprint import pprint

conn = sqlite3.connect('example.sqlite')
c = conn.cursor()

c.execute("SELECT * FROM  stocks")
v1 = c.fetchall()

c.execute("SELECT * FROM  stocks WHERE symbol='AAPL'")
v2 = c.fetchall()

conn.commit()
conn.close()

# pprint(v1)
# pprint(v2)
