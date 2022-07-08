import shlex
import subprocess

cmd="sleep 60"
command_bits = shlex.split(cmd)
output=subprocess.Popen(command_bits)

print(command_bits)
