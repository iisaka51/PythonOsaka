from snippet import *

df.loc[:, 'departure'] = df.departure.dt.tz_localize('Asia/Tokyo')
df.loc[:, 'arrival'] = df.arrival.dt.tz_localize('Europe/London')

df.dtypes

df.loc[:, 'actual_duration'] = df.arrival.dt.tz_convert('Asia/Tokyo') - df.departure

df
