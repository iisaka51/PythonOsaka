from rich.console import Console

console = Console(record=True)
console.print("Hello World!", style="white on blue")
console.save_text(path='output.txt')

console.print("Hello World!", style="white on blue")
console.save_html(path='output.html')
