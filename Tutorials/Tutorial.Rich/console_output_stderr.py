import sys
from rich.console import Console
error_console = Console(file=sys.stderr)
error_console.print("[bold red]This is an error!")
