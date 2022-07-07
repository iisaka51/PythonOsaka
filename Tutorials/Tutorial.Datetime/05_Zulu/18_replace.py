import zulu

dt = zulu.parse('2020-05-24T08:20:00.137493+00:00')

replaced = dt.replace(hour=14, minute=43)
# <Zulu [2020-05-24T14:43:18.137493+00:00]>
