from rich.console import Console
from rich.theme import Theme

from rich.console import Console
from rich.theme import Theme
custom_theme = Theme.read(path='style_config.ini')

console = Console(theme=custom_theme)
console.print("This is information", style="info")
console.print("[warning]The pod bay doors are locked[/warning]")
console.print("Something terrible happened!", style="danger")
