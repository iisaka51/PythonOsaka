import glob
import os
import pandas as pd

files = glob.glob("stockdata_*.csv")
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
