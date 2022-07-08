from rich.console import Console
from rich.text import Text

console = Console()
text = Text()
text.append("Hello", style="bold red")
text.append(" World!")
console.print(text)
