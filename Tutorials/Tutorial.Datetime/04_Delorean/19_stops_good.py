from delorean import stops, MONTHLY
from datetime import datetime

d1 = datetime(2021, 5, 24)
d2 = datetime(2022, 5, 24)

for stop in stops(freq=MONTHLY, count=13, timezone="Asia/Tokyo", start=d1):
    print(stop)
