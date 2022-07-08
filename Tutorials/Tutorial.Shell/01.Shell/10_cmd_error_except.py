import sys
from shell import shell, CommandError

try:
    shell('ls /tmp/PythonOsaka', die=True)
except CommandError as e:
    print(f'Command Error: {e.stderr}')
    import __main__ as main
    if hasattr(main, '__file__'):   # running script on REPL/IPython
        sys.exit(e.code)
