import pshell as sh

v1 = sh.check_output('cat sample.txt')
v2 = sh.check_output('cat sample.txt', decode=False)

# print(v1)
# print(v2)
