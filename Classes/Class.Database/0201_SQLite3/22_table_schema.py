import sqlite3
from pprint import pprint

conn = sqlite3.connect('example.sqlite')
c = conn.cursor()

c.execute("SELECT * FROM sqlite_master WHERE type='table' and name='stocks';")
data = c.fetchall()
pprint(data)

conn.commit()
conn.close()

