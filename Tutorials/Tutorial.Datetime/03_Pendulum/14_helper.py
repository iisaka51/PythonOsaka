import pendulum

dt = pendulum.datetime(2020, 7, 20)
v1 = dt.is_past()
assert v1 == True

v2 = dt.is_leap_year()
assert v2 == True

born = pendulum.datetime(1962, 1, 13)
not_birthday = pendulum.datetime(2020, 10, 2)
birthday = pendulum.datetime(2021, 1, 13)
past_birthday = pendulum.now().subtract(years=50)

v3 = born.is_birthday(not_birthday)
assert v3 == False

v4 = born.is_birthday(birthday)
assert v4 == True

# Compares to now by default
v5 = past_birthday.is_birthday()
assert v5 == True
