import pandas as pd

data = [[11,12,13],
        [21,22,23],
        [31,32,33]]

df = pd.DataFrame(data)
df.to_csv('sample.csv',header=None, index=False)
