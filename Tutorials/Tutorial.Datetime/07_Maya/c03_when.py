import maya

tests = [
    'last month',
    'Yesterday',
    'yesterday',
    'Tomorrow',
    'tomorrow',
    '昨日',
    '明日',
    '2日前',
    '2日後',
    '4週間後',
    '1ヶ月前',
    '1年後',
    ]

for str_when in tests:
    d = maya.when(str_when)
    print(f'{str_when}: {d}')
