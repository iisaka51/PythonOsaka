import arrow

format = r"ddd[\s+]MMM[\s+]DD[\s+]HH:mm:ss[\s+]YYYY"
dt1 = arrow.get("Sun May 24 08:20:30 2020", format)
print(dt1)

dt2 = arrow.get("Sun \tMay 24   08:20:30     2020", format)
print(dt2)

dt3 = arrow.get("Sun May 24   08:20:30   2020", format)
print(dt3)
