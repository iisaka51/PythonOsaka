import pandas as pd
import re

df = pd.read_csv('titanic.csv')

regexp = '^Q.*'
v1 = df['embark_town'].str.findall(regexp, flags=re.IGNORECASE)
