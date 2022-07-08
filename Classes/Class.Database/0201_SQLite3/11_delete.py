import sqlite3
from pprint import pprint

conn = sqlite3.connect('example.sqlite')
c = conn.cursor()

c.execute("SELECT * FROM  stocks")
v1 = c.fetchall()

c.execute("DELETE FROM  stocks WHERE symbol IN ('HPE', 'MSFT')")
c.execute("SELECT * FROM  stocks")
v2 = c.fetchall()

conn.commit()
conn.close()

# pprint(v1)
# pprint(v2)
# %run 03_insert.py
