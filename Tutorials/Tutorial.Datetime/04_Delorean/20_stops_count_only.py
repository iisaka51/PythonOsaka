from delorean import stops, MONTHLY
from datetime import datetime

for stop in stops(freq=MONTHLY, count=5, timezone="Asia/Tokyo"):
    print(stop)
