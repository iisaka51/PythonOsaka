import arrow

dt1 = arrow.get('\t \n  2022-02-02T22:22:22.222222 \t \n',
                normalize_whitespace=True)
print(dt1)

dt2 = arrow.get('2022-02-02  T \n   22:22:22\t222222',
                'YYYY-MM-DD T HH:mm:ss S',
                normalize_whitespace=True)
print(dt2)
