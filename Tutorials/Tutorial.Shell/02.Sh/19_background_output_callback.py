from sh import tail
from pathlib import Path

logfile = Path('/tmp/some_logfile.log')
logfile.unlink(missing_ok=True)
logfile.touch(exist_ok=True)

def process_output(line):
    print(line)

p = tail("-f", str(logfile), _out=process_output, _bg=True)
p.wait()
