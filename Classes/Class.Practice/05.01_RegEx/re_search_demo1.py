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
    x = re.search(ptn, text)
    print(f'Pattern: {ptn}')
    if x != None:
        print(f'group: {x.group()}')
        print(f'start: {x.start()}')
        print(f'  end: {x.end()}')
        print(f' span: {x.span()}')
