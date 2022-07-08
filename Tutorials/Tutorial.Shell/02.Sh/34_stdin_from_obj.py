import sh

stdin = ["sh", "is", "awesome"]
v1 = sh.tr("[:lower:]", "[:upper:]", _in=stdin)

# print(v1)
