import pandas as pd
from flight_data import flight_data

df = pd.DataFrame(flight_data)

df.loc[:, 'departure'] = pd.to_datetime(df.departure)
df.loc[:, 'arrival'] = pd.to_datetime(df.arrival)
