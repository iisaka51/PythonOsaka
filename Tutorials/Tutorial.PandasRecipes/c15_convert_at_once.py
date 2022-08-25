import pandas as pd

df = pd.read_csv('stockdata.csv')

df = df.astype(
    {
        "Date": "datetime64[ns]",
        "stock": "category",
        "value": "float",
        "change": "float",
    }
)
