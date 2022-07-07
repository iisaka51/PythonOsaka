from delorean import stops, HOURLY

for stop in stops(freq=HOURLY, count=10):
    print(stop)
