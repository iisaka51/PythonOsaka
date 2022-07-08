import sh
from io import StringIO

buf = StringIO()
mysh = sh(_out=buf)
