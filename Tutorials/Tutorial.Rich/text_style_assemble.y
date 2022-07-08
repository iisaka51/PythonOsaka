from rich.console import Console
from rich.text import Text

console = Console()
text = Text()
text = Text.assemble(("Hello", "bold red"), " World!")
console.print(text)
