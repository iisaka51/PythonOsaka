import sh

try:
    print(sh.ls("/tmp/python"))
except sh.ErrorReturnCode as err:
    err_msg = err.stderr.decode('utf-8')
    print(f"Error: Exit_Code={err.exit_code}, {err_msg}")
