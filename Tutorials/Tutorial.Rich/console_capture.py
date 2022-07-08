from rich.console import Console

console = Console()
with console.capture() as capture:
    console.print("[bold red]Hello[/] World")
output = capture.get()
print(output)
