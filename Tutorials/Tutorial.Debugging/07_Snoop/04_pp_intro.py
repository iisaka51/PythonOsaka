
def foo(i):
    return i + 333

print('\n単なるデバッグライト')
print(foo(123))

print('\n説明を追加したデバッグライト')
print('foo(123)):', foo(123))

print('\nsnoop.pp によるデバッグライト')
from snoop import pp
pp(foo(123))
