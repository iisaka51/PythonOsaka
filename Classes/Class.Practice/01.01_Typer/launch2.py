from pathlib import Path
import typer

APP_NAME = "python"

def main():
    app_dir = typer.get_app_dir(APP_NAME)
    typer.echo(app_dir)
    app_dir_path = Path(app_dir)
    typer.echo(app_dir_path)
    typer.launch('launch.py', locate=True)


if __name__ == "__main__":
    typer.run(main)
