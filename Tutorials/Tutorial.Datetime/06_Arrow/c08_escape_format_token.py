import arrow

fmt = "YYYY-MM-DD h[時] m[分]"
dt = arrow.get("2018-03-09 8時 40分", fmt)
dt.format(fmt)

fmt = "YYYY-MM-DD hh:mm [Good Morning.]"
dt = arrow.get("2018-03-09 08:40 Good Morning.", fmt)
dt.format(fmt)
