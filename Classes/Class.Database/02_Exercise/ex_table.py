from ex_connect import *

QUERY_TABLE="xxxxxxxxxxxxxxxxxx"         # ここを適宜修正してください

c = conn.cursor()
c.execute(QUERY_TABLE)
data = c.fetchall()
print(data)
