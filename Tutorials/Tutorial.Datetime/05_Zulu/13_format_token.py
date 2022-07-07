import zulu

dt1 = zulu.parse('05/24/20 08:20:00 +0900', '%m/%d/%y %H:%M:%S %z')
dt2 = zulu.parse('05/24/20 08:20:00 +0900', 'MM/dd/YY HH:mm:ss Z')

v1 = dt1.format('%m/%d/%y %H:%M:%S %z')
v2 = dt1.format('MM/dd/YY HH:mm:ss Z')


# dt1           # OUT: <Zulu [2020-05-23T23:20:00+00:00]>
# dt2           # OUT: <Zulu [2020-05-23T23:20:00+00:00]>

# v1            # OUT: '05/23/20 23:20:00 +0000'
# v2            # OUT: '05/23/20 23:20:00 +0000'
