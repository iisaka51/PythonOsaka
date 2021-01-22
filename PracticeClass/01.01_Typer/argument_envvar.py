from pathlib import Path
import typer

                                    # metavar='config_file',
def cmd(name: str = typer.Argument('anonymous',
                                    envvar='USERNAME',
                                    metavar='username',
                                    show_envvar=False),
        config: Path = typer.Option('config.ini',
                                    envvar='CONFIG_FILE')
):
    if config.is_file():
        text = config.read_text()
        typer.echo(f"Config file contents: {text}")
    else:
        typer.echo(f"Config file missing: {config.name}")

    typer.echo(f"Hello: {name}")

if __name__ == '__main__':
    typer.run(cmd)
