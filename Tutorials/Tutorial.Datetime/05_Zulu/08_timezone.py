import zulu

dt = zulu.parse('2020-05-24T08:20:00.137493+00:00')

zulu.parse('2020-05-24', default_tz='US/Eastern')
# <Zulu [2020-05-24T04:00:00+00:00]>

zulu.parse('2020-05-24', default_tz='Asia/Tokyo')
# <Zulu [2020-05-23T15:00:00+00:00]>

zulu.parse('2020-05-24', default_tz='local')
# <Zulu [2020-05-23T15:00:00+00:00]>
