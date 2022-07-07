import pandas as pd
import seaborn as sns

v1 = sns.get_dataset_names()
df = sns.load_dataset('titanic')
df.to_csv('titanic.csv')

# v1
# df
