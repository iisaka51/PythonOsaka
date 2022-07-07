import pandas as pd
from palmerpenguins import load_penguins

df = load_penguins()

new_df = pd.get_dummies(df,drop_first=True)
