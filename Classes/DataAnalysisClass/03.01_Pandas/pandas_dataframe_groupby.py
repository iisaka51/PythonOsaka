import numpy as np
import pandas as pd

data = {'Brand': ['A','B','A','C','B','D'],
        'Price': [1000,1200,1000,800,1200,1900],
        'Year': [2020,2017,2020,2018,2017,2016]
        }

df = pd.DataFrame(data, columns= ['Brand', 'Price','Year'])
print (df)
