from rich.prompt import Confirm

ans = Confirm.ask("Are you sure?")
print(f'Your answer is {ans}!')
