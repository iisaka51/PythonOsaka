from typing import List
import typer

valid_completion_items = [
    ("Brian", "The guitarist."),
    ("Freddie", "The vocalist."),
    ("John", "The bass guitarist."),
    ("Roger", "The drummer."),
]

def complete_name(ctx: typer.Context, incomplete: str):
    names = ctx.params.get("name") or []
    for name, help_text in valid_completion_items:
        if name.startswith(incomplete) and name not in names:
            yield (name, help_text)

def main(
    name: List[str] = typer.Option(["World"],
                            autocompletion=complete_name,
                            help="The name to say hi to."
    )
):
    for n in name:
        typer.echo(f"Hello {n}")

if __name__ == "__main__":
    typer.run(main)
