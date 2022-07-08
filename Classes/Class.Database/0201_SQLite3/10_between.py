import sqlite3
from pprint import pprint

conn = sqlite3.connect('example.sqlite')
c = conn.cursor()

c.execute("SELECT * FROM stocks")
v1 = c.fetchall()

c.execute("SELECT * from stocks WHERE price BETWEEN 100 AND 400")
v2 = c.fetchall()

c.execute("SELECT * from stocks WHERE price >= 100 AND price <= 400")
v3 = c.fetchall()

conn.commit()
conn.close()

# pprint(v1)
# pprint(v2)
# pprint(v3)
