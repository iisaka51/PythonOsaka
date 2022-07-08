from ex_connect import *

QUERY_COLUMNS="xxxxxxxxxxxxxxxxxx"         # ここを適宜修正してください

c.execute(QUERY_COLUMNS)
data = c.fetchall()
print(data)
