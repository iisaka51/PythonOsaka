from skimpy import clean_columns
import pandas as pd

data = {
    'FirstNom': ['Philip', 'Turanga'],
    'lastName': ['Fry', 'Leela'],
    'Tel Phone': ['555-234-5678', '(604) 111-2335'],
 }

df1 = pd.DataFrame(data)
df2 = clean_columns(df1, case='camel', replace={'Nom': 'Name'})
