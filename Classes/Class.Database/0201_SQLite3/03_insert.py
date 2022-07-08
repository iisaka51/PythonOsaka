import sqlite3

conn = sqlite3.connect('example.sqlite')
c = conn.cursor()
stock_data = [
               ('2020-03-05','BUY','HPE',100,11.99),
               ('2020-03-04','BUY','MSFT',100,161.57)
             ]
c.executemany("insert into stocks values (?,?,?,?,?)", stock_data)
conn.commit()
conn.close()
