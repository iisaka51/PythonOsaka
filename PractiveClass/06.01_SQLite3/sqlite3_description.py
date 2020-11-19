import sqlite3

conn = sqlite3.connect('example.sqlite3')
c = conn.cursor()
print(c.description)

symbol='AAPL'
c.execute("SELECT * from  stocks where symbol = '%s'" % symbol)
for desc in c.description:
    print(desc[0])

conn.commit()
conn.close()
