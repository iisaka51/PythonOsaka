from ex_connect import *

QUERY_COUNT="SELECT COUNT(name) FROM airports;"

c = conn.cursor()
c.execute(QUERY_COUNT)
count = c.fetchall()[0][0]
print(count)


QUERY="SELECT name FROM airports;"
c.execute(QUERY)
data = list(map(lambda x: x[0], c.fetchall()))
count = len(data)
print(count)
