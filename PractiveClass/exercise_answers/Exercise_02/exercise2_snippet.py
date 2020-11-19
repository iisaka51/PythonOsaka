import datetime

yy, mm, dd = 0, 0, 0
bd = input('Enter your birth date (YYY-MM-DD): ')
yy, mm, dd = b.split('-')

yy = int(yy)
mm = int(mm)
dd = int(dd)
birthday = datetime.date(yy, mm, dd)
