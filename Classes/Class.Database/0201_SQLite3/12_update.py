import sqlite3
from pprint import pprint

conn = sqlite3.connect('example.sqlite')
c = conn.cursor()

c.execute("SELECT * FROM stocks")
v1 = c.fetchall()
c.execute("UPDATE stocks SET trans = 'SELL' WHERE symbol = 'HPE'")
c.execute("SELECT * FROM stocks")
v2 = c.fetchall()

c.execute("UPDATE stocks SET trans = 'SELL'")
c.execute("SELECT * FROM stocks")
v3 = c.fetchall()

conn.commit()
conn.close()

# pprint(v1)
# pprint(v2)
# pprint(v3)
