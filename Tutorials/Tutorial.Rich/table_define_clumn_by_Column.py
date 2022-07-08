from rich.console import Console
from rich.table import Table, Column

table = Table("Released", "Title", "Box Office", title="Star Wars Movies")
from rich.table import Column
table = Table(
    "Released",
    "Title",
    Column(header="Box Office", justify="right"),
    title="Star Wars Movies"
)

console = Console()
console.print(table)

