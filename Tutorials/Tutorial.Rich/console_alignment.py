from rich.console import Console

console = Console(width=20)

style = "bold white on blue"
console.print("default", style=style)
console.print("left", style=style, justify="left")
console.print("center", style=style, justify="center")
console.print("right", style=style, justify="right")
