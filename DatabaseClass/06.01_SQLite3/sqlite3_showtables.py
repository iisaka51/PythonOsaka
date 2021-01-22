import sqlite3

conn = sqlite3.connect('example.sqlite3')
c = conn.cursor()

c.execute("SELECT name FROM sqlite_master WHERE type='table';")
data = c.fetchall()
print(data)

conn.commit()
conn.close()
