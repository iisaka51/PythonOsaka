import zulu

dt = zulu.parse('2020-05-24T08:20:00.137493+00:00')

dt
# <Zulu [2020-05-24T08:20:00.137493+00:00]>

dt.time_from(dt.end_of_day())
# '16 hours ago'

dt.time_to(dt.end_of_day())
# 'in 16 hours'

dt.time_from(dt.start_of_day())
# 'in 8 hours'

dt.time_to(dt.start_of_day())
# '8 hours ago'

zulu.now()
# <Zulu [2021-09-25T07:12:26.937079+00:00]>

dt.time_from_now()
# '1 year ago'

dt.time_to_now()
# 'in 1 year'
