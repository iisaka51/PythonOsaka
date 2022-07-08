import sys
from rich.console import Console

with open('outout.txt', 'w') as fh:
    error_console = Console(file=fh)
    error_console.print("[bold red]This is an error!")
