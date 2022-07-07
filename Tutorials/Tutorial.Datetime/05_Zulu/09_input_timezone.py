import zulu

zulu.parse('2020-05-24T08:20:00+0900')
# <Zulu [2020-05-23T23:20:00+00:00]>


zulu.parse('2020-05-24T08:20:00+0900', default_tz='Asia/Tokyo')
# <Zulu [2020-05-23T23:20:00+00:00]>
