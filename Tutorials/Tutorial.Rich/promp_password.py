from rich.prompt import Prompt

while True:
    password = Prompt.ask(
        "Please enter a password [cyan](must be at least 5 characters)",
        password=True,
    )
    if len(password) >= 5:
        break
    print("[prompt.invalid]password too short")

print(f"password={password!r}")
