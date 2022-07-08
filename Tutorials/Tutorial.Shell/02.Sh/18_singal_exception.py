import sh

try:
    p = sh.Sleeper(_bg=True)
    p.kill()
except sh.SignalException_SIGKILL:
    print("killed")
except:
    print("done")

v1 = sh.SignalException_SIGKILL == sh.SignalException_9
print(v1)
