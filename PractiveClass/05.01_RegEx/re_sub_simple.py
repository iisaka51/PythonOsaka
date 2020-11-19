import re

demos=[
    ('Delete Pattern abc', 'abc', ''),
    ('Replace pattern abc->def', 'abc', 'def'),
    ('Eliminate duplicate whispaces', r'\s+', ' '),
    ('Replace a string with a part of itself', 'abc(def)ghi', r'\1'),
]

text = 'abcdef abcdefghi ABCDEF     abcdefdeghi'
print(f'TEST string: "{text}\n')
for testcase, pattern, repl in demos:
    result = re.sub( pattern, repl, text)
    print(f'{testcase}: "{result}"')
    newtext, num = re.subn( pattern, repl, text)
    print(f'newtex: {newtext}, number of subs: {num}')
    print()
