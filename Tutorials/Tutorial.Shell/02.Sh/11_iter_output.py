from sh import tail, touch
from pathlib import Path

logfile = Path('/tmp/some_logfile.log')
logfile.unlink(missing_ok=True)
logfile.touch(exist_ok=True)

for line in tail("-f", str(logfile), _iter=True):
    if "EXIT" in line:
        break
    else:
        print(line)
