from ex_connect import *
from pprint import pprint

QUERY_COLUMNS="""SELECT * FROM sqlite_master
                 WHERE type='table' and name='airports'; """

c = conn.cursor()
c.execute(QUERY_COLUMNS)
data = c.fetchall()
pprint(data)
