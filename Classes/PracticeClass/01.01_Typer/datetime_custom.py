from datetime import datetime
import typer

def main(
    launch_date: datetime = typer.Argument(..., formats=["%Y/%m/%d"])
):
    typer.echo(f"Launch will be at: {launch_date}")


if __name__ == "__main__":
    typer.run(main)
