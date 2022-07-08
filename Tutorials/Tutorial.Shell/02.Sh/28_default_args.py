import sh
from io import StringIO

buf = StringIO()

sh.ls("/tmp", _out=buf)
sh.whoami(_out=buf)
sh.ps("auxw", _out=buf)
