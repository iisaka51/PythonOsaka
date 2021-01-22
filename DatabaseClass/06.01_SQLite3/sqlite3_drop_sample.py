import sqlite3

conn = sqlite3.connect('example.sqlite3')
c = conn.cursor()
conn.deleteDatabase('example.sqlite3')
conn.close()


