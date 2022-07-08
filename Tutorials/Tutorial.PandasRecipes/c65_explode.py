import pandas as pd

df = pd.DataFrame({"name": ['A', 'B', 'C'],
                   "day1": [21, 22, 23],
                   'day2':[31, 32, 33],
                   'day3': [41, 42, 43],
                   'day4': [51, 52, [53, 54, 55, 56, 57]],
                   'day5': [61, 61, 62]})

v1 = df.explode('day4').reset_index(drop=True)
