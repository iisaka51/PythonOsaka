import sqlite3

conn = sqlite3.connect('example.sqlite')
conn.deleteDatabase('example.sqlite')
conn.close()


