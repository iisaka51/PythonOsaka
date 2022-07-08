import sqlite3
from prettytable import from_db_cursor

connection = sqlite3.connect("CITY.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM CITY")
table = from_db_cursor(cursor)
print(table)
