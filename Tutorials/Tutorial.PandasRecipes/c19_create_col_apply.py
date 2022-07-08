import pandas as pd

df = pd.read_csv('titanic.csv')

is_female = lambda x: 'True' if x == 'female' else 'False'
df['sex_flag'] = df['sex'].apply(is_female)
