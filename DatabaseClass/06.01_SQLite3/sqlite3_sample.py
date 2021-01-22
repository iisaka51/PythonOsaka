import sqlite3

conn = sqlite3.connect('sample3.sql3')
c = conn.cursor()
c.execute('create table persons(id integer, name text, birthday)')
