from estore import *

v1 = select(o for o in Order).order_by(Order.date_shipped)
v2 = select(o for o in Order).order_by(desc(Order.date_shipped))

def func(data):
    for d in data:
        print(f'{d.id} {d.date_shipped} {d.state}')

# print(v1)
# print(v2)
# func(v1)
# func(v2)
