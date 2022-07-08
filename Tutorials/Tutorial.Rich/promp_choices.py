from rich.prompt import Prompt

ans = Prompt.ask("Aur you sure ",
                  choices=["Yes", "No"],
                  default="Yes")
print(f'Your answer is {ans}!')
