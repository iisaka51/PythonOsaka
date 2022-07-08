import io
import requests
import pandas as pd

baseurl = 'https://www.analyticsvidhya.com/wp-content/uploads/2016/02/'
url = baseurl + 'AirPassengers.csv'

raw_data = requests.get(url).content
df = pd.read_csv(io.StringIO(raw_data.decode('utf-8')))
