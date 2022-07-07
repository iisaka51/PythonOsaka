import pendulum

first = pendulum.datetime(2020, 5, 24, 8, 20, 0, 0, tz='Asia/Tokyo')
second = pendulum.datetime(2020, 5, 23, 19, 20, 0, 0, tz='America/New_York')

st1 = first.to_datetime_string()
assert st1 ==  '2020-05-24 08:20:00'
assert first.timezone_name == 'Asia/Tokyo'

st2 = second.to_datetime_string()
assert st2 == '2020-05-23 19:20:00'
assert second.timezone_name == 'America/New_York'

c1 = first == second
assert c1 == True

c2 = first != second
assert c2 == False

c3 = first > second
assert c3 == False

c4 = first >= second
assert c4 == True

c5 = first < second
assert c5 == False

c6 = first <= second
assert c6 == True

first = first.on(2020, 1, 1).at(0, 0, 0)
second = second.on(2020, 1, 1).at(0, 0, 0)

c10 = first == second
assert c10 == False

c11 = first != second
assert c11 == True

c12 = first > second
assert c12 == False

c13 = first >= second
assert c13 == False

c14 = first < second
assert c14 == True

c15 = first <= second
assert c15 == True

# first
# second
