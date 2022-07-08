import sh
from io import StringIO

buf = StringIO()
sh.date(_out=buf)
v1 = buf.getvalue()

# print(v1)
