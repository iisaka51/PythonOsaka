import zulu

delta = zulu.parse_delta('2h 32m')
# <Delta [2:32:00]>

t1 = delta.format()
assert t1 == '3 hours'

t2 = delta.format(add_direction=True)
assert t2 == 'in 3 hours'

t3 = zulu.parse_delta('-2h 32m').format(add_direction=True)
assert t3 == '3 hours ago'

t4 = delta.format(granularity='day')
assert t4 == '1 day'

t5 = delta.format(locale='de')
assert t5 == '3 Stunden'

t6 = delta.format(locale='fr', add_direction=True)
assert t6 == 'dans 3 heures'

t7 = delta.format(threshold=0)
assert t7 == '0 years'

t8 = delta.format(threshold=0.1)
assert t8 == '0 days'

t9 = delta.format(threshold=0.2)
assert t9 == '3 hours'

t10 = delta.format(threshold=5)
assert t10 == '152 minutes'

t11 = delta.format(threshold=155)
assert t11 == '9120 seconds'

t12 = delta.format(threshold=155, granularity='minute')
assert t12 == '152 minutes'

t13 = delta.format(format='long')
assert t13 == '3 hours'

t14 = delta.format(format='short')
assert t14 == '3 hr'

t15 = delta.format(format='narrow')
assert t15 == '3h'
