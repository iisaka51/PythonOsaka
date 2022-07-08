import os
from bash import bash

new_env = os.environ.copy()
new_env["USER"] = "Python_Osaka"
new_env["ENVVAR"] = "Python.Osaka"

v1 = bash('envcheck ENVVAR', env=new_env)
v2 = bash('envcheck', env=new_env)

# print(v1)
# print(v2)
