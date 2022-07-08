import typer
from typing import Union

def hello(Union[dict: **kwargs,
               count: int = typer.Option(1, '-C', help='Number of greetings.'),
                name: str = typer.Option(..., prompt='Your Name',
                                    help='The person to greet.'),
               ]
         ):
    """COUNTで与えた回数だけHelloする"""
    print(kwargs)

    for x in range(count):
        typer.echo(f'Hello {name}')

if __name__ == '__main__':
    typer.run(hello)
