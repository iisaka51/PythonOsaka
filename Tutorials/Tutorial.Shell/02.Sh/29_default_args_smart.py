import sh
from io import StringIO

buf = StringIO()
sh2 = sh(_out=buf)

sh2.ls("/tmp")
sh2.whoami()
sh2.ps("auxw")
