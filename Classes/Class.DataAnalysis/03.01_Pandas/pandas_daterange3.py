import pandas as pd

dr_1 = pd.date_range('2020-01-01', periods=3, freq='3D')
dr_2 = pd.date_range('2020-01-01', periods=3, freq='8H')
dr_3 = pd.date_range('2020-01-01', periods=3, freq='4H30min')

print(f"freq='3D':\n {dr_1}")
print(f"freq='8H':\n {dr_2}")
print(f"freq='4H30min':\n {dr_3}")
