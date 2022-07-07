from datetime import datetime
import zulu

dt = zulu.parse('2020-05-24T08:20:00.137493+00:00')

t1 = dt.start_of('day')  # OR dt.start_of_day()
# <Zulu [2020-05-24T00:00:00+00:00]>

t2 = dt.end_of('day')  # OR dt.end_of_day()
# <Zulu [2020-05-24T23:59:59.999999+00:00]>

t3 = dt.end_of('year', count=3)  # OR dt.end_of_year()
# <Zulu [2022-12-31T23:59:59.999999+00:00]>
