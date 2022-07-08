import subprocess
import pshell as sh
import io
import shlex

buf = io.StringIO()

cmd = 'ls /tmp/missing_file'
sh.call(cmd, stderr=buf)

with sh.real_fh(buf) as real_buf:
    subprocess.call(shlex.split(cmd), stderr=real_buf)

