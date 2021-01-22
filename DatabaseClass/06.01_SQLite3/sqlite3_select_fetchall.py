import sqlite3

conn = sqlite3.connect('example.sqlite3')
c = conn.cursor()

c.execute("SELECT * from  stocks")
data = c.fetchone()
print(f'1st fetchone(): {data}')
data = c.fetchone()
print(f'2nd fetchone(): {data}')

c.execute("SELECT * from  stocks")
data = c.fetchall()
print(f'fetchall(): {data}')

print('read data as iterator:')
for row in c.execute("SELECT * from  stocks"):
    print(row)

conn.commit()
conn.close()
