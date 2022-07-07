import zulu

dt = zulu.parse('2020-05-24T08:20:00.137493+00:00')

shifted = dt.shift(hours=-5, minutes=10)
# <Zulu [2020-05-24T03:30:00.137493+00:00]>

assert shifted is not dt
# assert は与えた式が真のときは何も表示しない
