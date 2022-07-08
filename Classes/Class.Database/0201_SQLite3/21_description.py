import sqlite3
from pprint import pprint

conn = sqlite3.connect('example.sqlite')
c = conn.cursor()
print(c.description)

symbol='AAPL'
c.execute("SELECT * from  stocks where symbol = '%s'" % symbol)

for desc in c.description:
    pprint(desc[0])

conn.commit()
conn.close()
