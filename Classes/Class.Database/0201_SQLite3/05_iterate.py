import sqlite3
from pprint import pprint

conn = sqlite3.connect('example.sqlite')
c = conn.cursor()

def func():
    val = list()
    for row in c.execute("SELECT * FROM stocks"):
        val.append(row)
    return val

v1 = func()

conn.commit()
conn.close()

# pprint(v1)
