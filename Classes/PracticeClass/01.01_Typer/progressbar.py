import time
import typer

def do_something(count):
    for num in range(count):
        yield num


def main(count: int = typer.Option(100,
                            '--count', min=10, max=500)
):
    total = 0
    with typer.progressbar(do_something(count),
                           length=count,
                           label="Processing") as progress:
        for value in progress:
            # Fake processing time
            time.sleep(0.01)
            total += 1
    typer.echo(f"Processed {total} things.")

if __name__ == "__main__":
    typer.run(main)
