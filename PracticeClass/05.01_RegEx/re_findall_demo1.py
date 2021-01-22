import re

text='If you want to using regular expression, you must import the re module'
patterns=[
  'epression',
  'you',
  '^If.*to',
  'module$',

]

print(text)
for ptn in patterns:
    x = re.findall(ptn, text)
    print(f'Pattern: {ptn} {x}')
