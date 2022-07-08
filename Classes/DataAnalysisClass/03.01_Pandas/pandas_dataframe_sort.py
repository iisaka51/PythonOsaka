import pandas as pd

data = {'Brand': ['A','B','C','D'],
        'Price': [1000,1200,800,1900],
        'Year': [2020,2017,2018,2016]
        }

df = pd.DataFrame(data, columns= ['Brand', 'Price','Year'])
print (df)
