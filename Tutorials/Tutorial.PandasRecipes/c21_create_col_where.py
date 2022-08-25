import pandas as pd
import numpy as np

df = pd.read_csv('titanic.csv')

df['sex_flag'] = np.where(df['sex'] == 'female', 'True', 'False')
