import sh

try:
    print(sh.ls("/tmp/python"))
except sh.ErrorReturnCode_1 as err:
    print(f"Error: No such file or directory.")
