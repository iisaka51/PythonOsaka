from rich.console import Console
from rich.table import Table, Column
from rich.padding import Padding

table = Table("Released", "Title", "Box Office", title="Star Wars Movies")
world = Padding("Hello", 1, style="red", expand=False)
table.add_row("Hello", world, "Python")

console = Console()
console.print(table)

