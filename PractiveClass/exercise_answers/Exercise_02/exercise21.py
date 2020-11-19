import datetime

yy, mm, dd = 0, 0, 0
bd = input('Enter your birth date (YYY-MM-DD): ')
try:
    yy, mm, dd = bd.split('-')
except:
    yy, mm, dd = (1962, 1, 13)

yy = int(yy)
mm = int(mm)
dd = int(dd)
birthday = datetime.date(yy, mm, dd)

delta = datetime.date.today() - birthday

print(f"Days of life: {delta.days}")
print(f"Days of Week my birthday: {birthday:%A}")
