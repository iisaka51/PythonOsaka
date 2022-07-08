from university1 import *
import logging

logging.basicConfig(filename='pony.log', level=logging.INFO)

def func(data):
    for d in data:
        print(f'{d.name} {d.gpa}')

with sql_debugging(show_values=True):  # クエリパラメタも出力する
    v1 = select(s for s in Student if s.gpa > 3)
    func(v1)

# !cat pony.log
