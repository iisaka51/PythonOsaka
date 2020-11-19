import sqlite3

conn = sqlite3.connect('example.sqlite3')
c = conn.cursor()
c.execute("""CREATE TABLE stocks
            (date text, trans text, symbol text, qty real, price real)""")
c.execute("""INSERT INTO stocks VALUES
             ('2020-03-06','BUY','GOOG',100,1298.41)""")
c.execute("""INSERT INTO stocks VALUES
             ('2020-03-09','BUY','AAPL',100,288.06)""")
conn.commit()
conn.close()
