import typer

def cmd(verbose: int = typer.Option(0, '-v', '--verbose', count=True,
                                    help="Verbosly Mode")):
    typer.echo(f'verbose level: {verbose}')

if __name__ == '__main__':
    typer.run(cmd)
