import sh

output = sh.ls("/tmp")
v1 = output.exit_code

# print(v1)
