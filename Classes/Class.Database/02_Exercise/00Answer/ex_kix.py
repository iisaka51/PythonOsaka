from ex_connect import *

QUERY="SELECT * FROM airports WHERE iata == 'KIX';"

c = conn.cursor()
c.execute(QUERY)
data = c.fetchone()
print(data)
