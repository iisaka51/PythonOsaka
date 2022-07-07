from datetime import datetime
import pytz

jst = pytz.timezone('Asia/Tokyo')
d = datetime.now(pytz.utc)
d = jst.normalize(d.astimezone(jst))

# print(d)
