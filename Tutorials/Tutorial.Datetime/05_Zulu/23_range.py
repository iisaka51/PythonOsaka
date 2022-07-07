import zulu

start = zulu.Zulu(2020, 5, 20, 8, 20)
end = zulu.Zulu(2020, 10, 2, 11, 00)

for dt in zulu.range('month', start, end):
    print(dt)
