from rich.console import Console

console = Console()
console.print("Hello", style="red")

console.print("Hello", style="color(1)")

console.print("Hello", style="#ff0000")
console.print("Hello", style="rgb(255,0,0)")
