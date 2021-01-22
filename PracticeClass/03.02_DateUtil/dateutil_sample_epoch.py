from datetime import *; from dateutil.relativedelta import *

NOW = datetime.now()
TODAY = date.today()

epoch = date(1970,1,1)
diff = relativedelta(TODAY, epoch)

print(f'TODAY: {TODAY}')
print(diff)
