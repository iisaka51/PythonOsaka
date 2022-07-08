from testdb import *

v1 = table.find(age={'<=': '55'})
v2 = table.find(age={'<': '30'})
v3 = table.find(age={'>': '70'})
v4 = table.find(age={'>=': '71'})
v5 = table.find(age={'=': '0'})
v6 = table.find(age={'!=': '0'})
v7 = table.find(age={'between': [1, 60]})
v8 = table.find(name={'like': '%Wilson'})
v9 = table.find(name={'ilike': '%WILSON'})

def func(data):
    for d in data:
        print(d)

# func(v1)
