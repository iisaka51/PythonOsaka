from ex_connect import *

QUERY_COUNT="xxxxxxxxxxxxxxxxxx"         # ここを適宜修正してください

c.execute(QUERY_COUNT)
data = c.fetchall()
print(data)
