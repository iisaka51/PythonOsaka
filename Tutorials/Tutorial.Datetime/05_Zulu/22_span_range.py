import zulu

start = zulu.Zulu(2020, 5, 20, 8, 20)
end = zulu.Zulu(2020, 10, 2, 11, 00)

for span in zulu.span_range('month', start, end):
    print(span)
