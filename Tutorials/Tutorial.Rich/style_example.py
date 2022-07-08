from rich.console import Console

console = Console()
console.print("Danger, Will Robinson!",
               style="blink bold red underline on white")

console.print("foo [not bold]bar[/not bold] baz", style="bold")

