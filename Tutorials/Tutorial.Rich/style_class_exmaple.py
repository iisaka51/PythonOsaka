from rich.console import Console
from rich.style import Style

console = Console()
danger_style = Style(color="red", blink=True, bold=True)
console.print("Danger, Will Robinson!", style=danger_style)
