from datetime import datetime
import dateutil.parser

dt = datetime(2020, 3, 4, 0, 0)

# assert は与えた式が真のときは何も表示しない

dt1 = dateutil.parser.parse('2020/03/04')
assert dt == dt1

dt2 = dateutil.parser.parse('2020-03-04')
assert dt == dt2

dt3 = dateutil.parser.parse('2020/Mar/04')
assert dt == dt3

dt4 = dateutil.parser.parse('2020-March-04')
assert dt == dt4

dt5 = dateutil.parser.parse('04-Mar-2020')
assert dt == dt5

dt6 = dateutil.parser.parse('04-March-2020')
assert dt == dt6

dt7 = dateutil.parser.parse('04-Mar-20')
assert dt == dt7

dt8 = dateutil.parser.parse('04-March-20')
assert dt == dt8
