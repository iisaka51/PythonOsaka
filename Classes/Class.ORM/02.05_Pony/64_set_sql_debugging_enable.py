from university1 import *
import logging

logging.basicConfig(filename='pony.log', level=logging.INFO)

def func(data):
    for d in data:
        print(f'{d.name} {d.gpa}')

with sql_debugging:  # デバッグ出力を有効にする
    v1 = select(s for s in Student)
    func(v1)

# !cat pony.log
