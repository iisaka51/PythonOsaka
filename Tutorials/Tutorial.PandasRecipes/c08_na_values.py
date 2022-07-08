import pandas as pd
from skimpy import skim

missing_values = ["n/a", "na", " _ _"]
df = pd.read_csv('titanic.csv', na_values=missing_values)
