"""
# Create datetime object (not tz naive)

rom snippet import *

# pandas
# df.loc[:, 'departure'] = df.departure.dt.tz_localize('Asia/Tokyo')
# df.loc[:, 'arrival'] = df.arrival.dt.tz_localize('Europe/London')

df.departure[x]k


departure = datetime.datetime.strptime('2021-03-05 10:45', '%Y-%m-%d %H:%M')
departure
datetime.datetime(2021, 3, 5, 10, 45)
# Create datetime object (not tz naive)
arrival = datetime.datetime.strptime('2021-03-06 06:22', '%Y-%m-%d %H:%M')
arrival
datetime.datetime(2021, 3, 6, 6, 22)
# Create delorean object for departure
dpt = Delorean(departure, timezone='Europe/London')
dpt
Delorean(datetime=datetime.datetime(2021, 3, 5, 10, 45), timezone='Europe/London')
# Create delorean object for arrival
arr = Delorean(arrival, timezone='Asia/Kuala_Lumpur')
arr
Delorean(datetime=datetime.datetime(2021, 3, 6, 6, 22), timezone='Asia/Kuala_Lumpur')
# Flight time
flight_time = arr - dpt
flight_time
datetime.timedelta(seconds=41820)
# List properties which aren't "dunders"
[p for p in dir(flight_time) if '__' not in p]
['days',
 'max',
 'microseconds',
 'min',
 'resolution',
 'seconds',
 'total_seconds']
# Same as default representation
flight_time.seconds
41820
# Alternate calculation
flight_time.total_seconds() / 60 / 60
11.616666666666667
"""
