import zulu

dt = zulu.parse('2020-05-24T08:20:00+0900')

dt.format('%Y-%m-%d %H:%M:%S%z')
# '2020-05-23 23:20:00+0000'

dt.format('YYYY-MM-dd HH:mm:ssZ')
# '2020-05-23 23:20:00+0000'

dt.format('%Y-%m-%d %H:%M:%S%z', tz='US/Eastern')
# '2020-05-23 19:20:00-0400'

dt.format('%Y-%m-%d %H:%M:%S%z', tz='local')
# '2020-05-24 08:20:00+0900'

zulu.parse('2020-05-24 08:20:00+0900', '%Y-%m-%d %H:%M:%S%z')
# <Zulu [2020-05-23T23:20:00+00:00]>

