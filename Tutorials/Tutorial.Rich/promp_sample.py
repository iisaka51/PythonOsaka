from rich.prompt import Prompt
name = Prompt.ask("Enter your name")
print(f'Hello {name}!')

name = Prompt.ask("Enter your name", default="Jack Bauer")
print(f'Hello {name}!')

name = Prompt.ask("What is [i]your[/i] [bold red]name[/]? :smiley: ")
print(f'Hello {name}!')

