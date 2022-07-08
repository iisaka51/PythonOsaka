import sh

v1 = sh.cat(_in="test")
v2 = sh.tr("[:lower:]", "[:upper:]", _in="sh is awesome")

# print(v1)
# print(v2)
