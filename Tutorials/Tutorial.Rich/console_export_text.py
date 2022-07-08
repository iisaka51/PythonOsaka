from rich.console import Console

console = Console(record=True)
console.print("Hello World!", style="white on blue")
text1 = console.export_text()
text2 = console.export_text()

print(f'1st: {text1}')
print(f'2nd: {text2}')

console.save_text(path='output.txt')
