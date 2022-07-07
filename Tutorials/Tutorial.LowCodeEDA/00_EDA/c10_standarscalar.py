import pandas as pd
from palmerpenguins import load_penguins
from sklearn.preprocessing import StandardScaler

df = load_penguins()

new_df = StandardScaler().fit_transform(df)
