import numpy as np
import pandas as pd
from beautifultable import BeautifulTable

df = pd.read_csv('TOYOTA.csv')
table = BeautifulTable()
table.columns.header = df.header
