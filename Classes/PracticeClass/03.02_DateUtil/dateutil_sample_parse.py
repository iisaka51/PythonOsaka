import dateutil.parser

print(dateutil.parser.parse('2020/03/04'))
print(dateutil.parser.parse('2020-03-04'))
print(dateutil.parser.parse('2020/Mar/04'))
print(dateutil.parser.parse('2020-March-04'))

print(dateutil.parser.parse('04-Mar-2020'))
print(dateutil.parser.parse('04-March-2020'))
print(dateutil.parser.parse('04-Mar-20'))
print(dateutil.parser.parse('04-March-20'))
