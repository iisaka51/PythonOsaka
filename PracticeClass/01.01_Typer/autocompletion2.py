import typer

valid_completion_items = [
    ("Brian", "The guitarist."),
    ("Freddie", "The vocalist."),
    ("John", "The bass guitarist."),
    ("Roger", "The drummer."),
]

def complete_name(incomplete: str):
    for name, help_text in valid_completion_items:
        if name.startswith(incomplete):
            yield (name, help_text)


def main(
    name: str = typer.Option("World",
                      autocompletion=complete_name,
                      help="The name to say hi to."
    )
):
    typer.echo(f"Hello {name}")

if __name__ == "__main__":
    typer.run(main)
