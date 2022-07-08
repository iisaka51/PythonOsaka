import sh

v1 = sh.envcheck("ENVVAR", _env={"ENVVAR": "Python.Osaka"})
v2 = sh.envcheck(_env={"ENVVAR": "Python.Osaka"})

# print(v1)
# print(v2)
