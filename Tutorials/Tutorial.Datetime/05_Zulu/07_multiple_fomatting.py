import zulu

zulu.parse('3/2/1992', ['ISO8601', 'MM/dd/YYYY'])
# <Zulu [1992-03-02T00:00:00+00:00]>

try:
    zulu.parse('3/2/1992', 'ISO8601')
except zulu.ParseError as e:
    print(e)

# Value "3/2/1992" does not match any format in
# ["ISO8601" (Unable to parse date string '3/2/1992')]

