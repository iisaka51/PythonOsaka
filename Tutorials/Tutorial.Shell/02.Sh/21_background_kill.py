import sh
from pathlib import Path

logfile = Path('/tmp/some_logfile.log')
logfile.unlink(missing_ok=True)
logfile.touch(exist_ok=True)

def process_output(line, stdin, process):
    print(line)
    if "EXIT" in line:
        process.kill()
        return True

p = sh.tail("-f", str(logfile), _out=process_output, _bg=True)
p.wait()
