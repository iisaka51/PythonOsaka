from datetime import timedelta
import zulu

dt = zulu.parse('2020-05-24T08:20:00.137493+00:00')

shifted = dt.subtract(hours=5).add(minutes=10)
# <Zulu [2020-05-24T03:30:00.137493+00:00]>

shifted = dt.subtract(timedelta(hours=5))
# <Zulu [2020-05-24T03:30:00.137493+00:00]>

delta = dt.subtract(shifted)
# <Delta [5:00:00]>

shifted = dt.add(timedelta(minutes=10))
# <Zulu [2020-05-24T03:30:00.137493+00:00]>
