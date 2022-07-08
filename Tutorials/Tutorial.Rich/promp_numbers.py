from rich.prompt import IntPrompt

while True:
    number = IntPrompt.ask(
        ":rocket: Enter a number between [b]1[/b] and [b]10[/b]",
        default=5
    )
    if number >= 1 and number <= 10:
        break
    print(":pile_of_poo: [prompt.invalid]Number must be between 1 and 10")

print(f"number={number}")
