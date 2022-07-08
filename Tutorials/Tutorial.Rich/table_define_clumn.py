from rich.console import Console
from rich.table import Table, Column

table = Table("Released", "Title", "Box Office", title="Star Wars Movies")

console = Console()
console.print(table)

