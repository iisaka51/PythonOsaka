import pendulum

dt = pendulum.datetime(2020,5,24,8,20,0, tz='Asia/Tokyo')

ct01 = dt.to_atom_string()
assert ct01 == '2020-05-24T08:20:00+09:00'

ct02 = dt.to_cookie_string()
assert ct02 == 'Sunday, 24-May-2020 08:20:00 JST'

ct03 = dt.to_iso8601_string()
assert ct03 == '2020-05-24T08:20:00+09:00'

ct04 = dt.to_rfc822_string()
assert ct04 == 'Sun, 24 May 20 08:20:00 +0900'

ct05 = dt.to_rfc850_string()
assert ct05 == 'Sunday, 24-May-20 08:20:00 JST'

ct06 = dt.to_rfc1036_string()
assert ct06 == 'Sun, 24 May 20 08:20:00 +0900'

ct07 = dt.to_rfc1123_string()
assert ct07 == 'Sun, 24 May 2020 08:20:00 +0900'

ct08 = dt.to_rfc2822_string()
assert ct08 == 'Sun, 24 May 2020 08:20:00 +0900'

ct09 = dt.to_rfc3339_string()
assert ct09 == '2020-05-24T08:20:00+09:00'

ct10 = dt.to_rss_string()
assert ct10 == 'Sun, 24 May 2020 08:20:00 +0900'

ct11 = dt.to_w3c_string()
assert ct11 == '2020-05-24T08:20:00+09:00'
