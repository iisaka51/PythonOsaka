from sh2 import mysh, buf
from mysh import ls, whoami

ls("/tmp")
whoami()

v1 = buf.getvalue()

# print(v1)
