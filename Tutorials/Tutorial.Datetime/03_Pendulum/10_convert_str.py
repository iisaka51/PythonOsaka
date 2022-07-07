import pendulum

dt = pendulum.datetime(2020, 2, 2, 2, 2, 2, tz='Asia/Tokyo')

st1 = dt.isoformat()
assert st1 == '2020-02-02T02:02:02+09:00'

st2 = dt.to_date_string()
assert st2 == '2020-02-02'

st3 = dt.to_formatted_date_string()
assert st3 == 'Feb 02, 2020'

st4 = dt.to_time_string()
assert st4 == '02:02:02'

st5 = dt.to_datetime_string()
assert st5 == '2020-02-02 02:02:02'

st6 = dt.to_day_datetime_string()
assert st6 == 'Sun, Feb 2, 2020 2:02 AM'
