import zulu

dt = zulu.parse('2020-05-24T08:20:00.137493+00:00')

copied = dt.copy()
# <Zulu [2020-05-24T08:20:00.137493+00:00]>

assert copied is not dt
assert copied == dt
