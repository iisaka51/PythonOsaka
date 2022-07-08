from ex_connect import *

QUERY_TABLE="SELECT name FROM sqlite_master WHERE type='table';"

c = conn.cursor()
c.execute(QUERY_TABLE)
data = c.fetchall()
print(data)
