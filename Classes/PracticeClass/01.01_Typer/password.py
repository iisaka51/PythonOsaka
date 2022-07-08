import typer

def cmd(password: str = typer.Option(...,
                                     prompt='Password',
                                     hide_input=True,
                                     confirmation_prompt=True)
):
    typer.echo( password )

if __name__ == '__main__':
    typer.run(cmd)
