class MyProgError(BaseException):
    pass


def dummyfunc():
    raise MyProgError("Error in dummyfunc()")

try:
    dummyfunc()
except MyProgError as msg:
    print(msg)

