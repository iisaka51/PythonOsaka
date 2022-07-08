import time
from rich.live import Live
from rich.table import Table

table = Table()
table.add_column("Row ID")
table.add_column("Description")
table.add_column("Level")

# update 4 times a second to feel fluid
with Live(table, refresh_per_second=4) as live:
    for row in range(12):
        live.console.print("Working on row #{row}")
        time.sleep(0.4)
        table.add_row(f"{row}", f"description {row}", "[red]ERROR")

