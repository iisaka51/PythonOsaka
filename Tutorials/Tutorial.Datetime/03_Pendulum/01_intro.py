from datetime import datetime
import pendulum

dt = pendulum.datetime(2020,5,24)

# assert は与えた式が真のときは何も表示しない

assert isinstance(dt, datetime)
assert dt.timezone.name == 'UTC'
