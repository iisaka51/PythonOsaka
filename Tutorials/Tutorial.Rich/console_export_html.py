from rich.console import Console

console = Console(record=True)
console.print("Hello World!", style="white on blue")
html1 = console.export_html()
html2 = console.export_html()

print(f'1st: {html1}')
print(f'2nd: {html2}')

console.save_html(path=')
