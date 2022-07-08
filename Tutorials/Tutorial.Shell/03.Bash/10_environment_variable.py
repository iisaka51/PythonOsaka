from bash import bash

v1 = bash('envcheck ENVVAR', env={"ENVVAR": "Python.Osaka"}).value()
v2 = bash('envcheck', env={"ENVVAR": "Python.Osaka"}).value()

# print(v1)
# print(v2)
