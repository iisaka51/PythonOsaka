from rich.console import Console
from time import sleep

console = Console()

with console.status("Do somethings..."):
    sleep(30)
