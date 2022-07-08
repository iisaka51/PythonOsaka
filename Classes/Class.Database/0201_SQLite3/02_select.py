import sqlite3

conn = sqlite3.connect('example.sqlite')
c = conn.cursor()

symbol='AAPL'
c.execute("SELECT * FROM  stocks WHERE symbol = '%s'" % symbol)
data = c.fetchone()

conn.commit()
conn.close()

# print(data)
