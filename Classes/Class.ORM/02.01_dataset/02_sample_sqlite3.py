import sqlite3

conn = sqlite3.connect(':memory:')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS users (name, age INTEGER)')
conn.commit()

c.execute('INSERT INTO users values (?, ?) ', ('Jack Bauer', 55))
conn.commit()

c.execute('ALTER TABLE users ADD COLUMN belongs TEXT')
conn.commit()

c.execute('INSERT INTO users values (?, ?, ?) ', ('Jack Bauer', 55, 'CTU'))
conn.commit()

c.execute('SELECT name, age FROM users WHERE name = ?', ('Jack Bauer', ))
row = list(c)[0]
jack = dict(name=row[0], age=row[1])

# print(jack)
