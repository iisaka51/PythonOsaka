from datetime import datetime
import pytz

utc = pytz.utc
now = datetime.now(utc)  # time.time() と等価
epoch = now.timestamp()
print(now)
print(epoch)

tz = pytz.timezone('Asia/Tokyo')
timestamp = datetime.fromtimestamp(epoch, tz)
print(timestamp)
