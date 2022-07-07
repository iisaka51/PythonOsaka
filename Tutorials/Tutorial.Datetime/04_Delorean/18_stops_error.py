from delorean import stops, MONTHLY
from datetime import datetime

d1 = datetime(2021, 5, 24)
d2 = datetime(2022, 5, 24)

for stop in stops(freq=MONTHLY, timezone="Asia/Tokyo", stop=d2):
    print(stop)
