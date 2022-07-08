import pandas as pd

df = pd.read_csv('titanic.csv')

df.loc[df['sex'] == 'female', 'sex_flag'] = 'True'
df.loc[df['sex'] == 'male', 'sex_flag'] = 'False'
