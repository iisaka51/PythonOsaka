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
    print(f'Pattern: {ptn}')
    for match in re.finditer(ptn, text):
        print(f'group: {match.group()}')
        print(f'start: {match.start()}')
        print(f'  end: {match.end()}')
        print(f' span: {match.span()}')
