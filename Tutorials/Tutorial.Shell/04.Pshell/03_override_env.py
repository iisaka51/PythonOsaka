import os
import pshell as sh

sh.putenv('X', 'foo')
v1 = os.environ['X']

with sh.override_env('X', 'bar'):
    v2 = os.environ['X']

v3 = os.environ['X']

# print(v1)
# print(v2)
# print(v3)
