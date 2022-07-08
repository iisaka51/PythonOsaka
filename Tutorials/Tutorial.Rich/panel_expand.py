from rich import print
from rich.panel import Panel

panel = Panel("Hello, [red]World!", expand=False)
print(panel)

panel = Panel.fit("Hello, [red]World!", title="using fit()")
print(panel)
