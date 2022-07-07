import pendulum

dt = pendulum.datetime(2020, 2, 2, 2, 2, 2, tz='Asia/Tokyo')
dt_str = 'Sunday 2nd of February 2020 02:02:02 AM'

st1 = dt.strftime('%A %-dnd of %B %Y %I:%M:%S %p')
assert st1 == dt_str

st2 =  dt.format('dddd Do [of] MMMM YYYY HH:mm:ss A')
assert st2 == dt_str
