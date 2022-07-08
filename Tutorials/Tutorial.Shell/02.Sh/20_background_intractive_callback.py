import sh
from pathlib import Path

logfile = Path('/tmp/some_logfile.log')
logfile.unlink(missing_ok=True)
logfile.touch(exist_ok=True)

def interact(line, stdin):
    if line == "もうは、まだなり。まだは、もうなり。?":
        stdin.put("もうは、まだなり。まだは、もうなり。")

    elif line == "早い利確と、遅い損切り":
        stdin.put("残念な投資行動")
        return True

    else:
        stdin.put("知らない行")
        return True

p = sh.tail('-f', str(logfile), _out=interact, _bg=True)
p.wait()
