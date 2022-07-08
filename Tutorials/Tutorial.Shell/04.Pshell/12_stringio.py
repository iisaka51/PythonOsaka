import pshell as sh
from io import StringIO

outbuf = StringIO()

v1 = sh.call('ls -1 /etc/', stdout=outbuf)
v2 = outbuf.getvalue().splitlines()[:5]

# print(v1)
# print(v2)
