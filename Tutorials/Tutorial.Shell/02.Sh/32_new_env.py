import os
import sh

new_env = os.environ.copy()
new_env["USER"] = "Python_Osaka"
new_env["ENVVAR"] = "Python.Osaka"

v1 = sh.envcheck("ENVVAR", _env=new_env)
v2 = sh.envcheck(_env=new_env)

# print(v1)
# print(v2)
