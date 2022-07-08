import numpy as np
import pandas as pd
from tabulate import tabulate

df = pd.read_csv('TOYOTA.csv')
print(tabulate(df[:10],df.columns, tablefmt='github', showindex=False))
