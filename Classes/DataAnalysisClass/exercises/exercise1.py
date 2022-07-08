import numpy as np
import pandas as pd
import statsmodels.api as sm
import io
import requests

baseurl = 'https://www.analyticsvidhya.com/wp-content/uploads/2016/02/'
url = baseurl + 'AirPassengers.csv'

def read_csv_fromurl(url=url):
    raw_data = requests.get(url).content
    df = pd.read_csv(io.StringIO(raw_data.decode('utf-8')))
    return df

if __name__ == '__main__':
    df = read_csv_fromurl()
    print(df.describe)
