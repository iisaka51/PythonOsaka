import numpy as np
import pandas as pd

df0 = pd.read_csv("stockdata.csv")
df1 = pd.read_csv("stockdata.csv", skiprows=[1, 5])
df2 = pd.read_csv("stockdata.csv", skiprows=10)

skip=lambda x: x > 0 and np.random.rand() > 0.1
df3 = pd.read_csv("stockdata.csv", skiprows=skip)
