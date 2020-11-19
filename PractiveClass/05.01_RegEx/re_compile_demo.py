import re

text='If you want to using regular expression, you must import the re module'
ptn = re.compile('you')
x = ptn.match(text)

print('match')
if x != None:
    print(f'group: {x.group()}')
    print(f'start: {x.start()}')
    print(f'  end: {x.end()}')
    print(f' span: {x.span()}')

print('search')
x = ptn.search(text)
if x != None:
    print(f'group: {x.group()}')
    print(f'start: {x.start()}')
    print(f'  end: {x.end()}')
    print(f' span: {x.span()}')

print('findall')
print(ptn.findall(text))
