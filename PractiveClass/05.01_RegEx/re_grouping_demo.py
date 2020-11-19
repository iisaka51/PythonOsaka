import re

text = "Coronavirus concerns lead to hoarding, panic buying to stock 'panic pantries,'"

searchObj = re.search( r'(?P<virus>corona[^ ]*) .* to (.*?) .*', text, re.M|re.I)

if searchObj:
   print(f'searchObj.group()  : {searchObj.group()}')
   print(f'searchObj.group(virus)  : {searchObj.group("virus")}')
   print(f'searchObj.group(1) : {searchObj.group(1)}')
   print(f'searchObj.group(2) : {searchObj.group(2)}')
else:
   print('Nothing found!!')
