import sqlite3

conn = sqlite3.connect('example.sqlite3')
c = conn.cursor()
symbol='AAPL'
c.execute("SELECT * from  stocks where symbol = '%s'" % symbol)
print(c.fetchone())
conn.commit()
conn.close()
