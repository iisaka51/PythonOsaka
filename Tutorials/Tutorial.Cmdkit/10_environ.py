import os
from cmdkit.config import Environ

os.environ['MYAPP_A_X'] = '1'
os.environ['MYAPP_A_Y'] = '2'
os.environ['MYAPP_B'] = '3'

# env = Environ(prefix='MYAPP')
env = Environ('MYAPP')
v1 = env.copy()

v2 = env.reduce()

# print(v1)
# print(v2)

