import typer

def abort_cmd():
    raise typer.Abort()

def exit_cmd():
    raise typer.Exit()

action_table = {
    'exit': exit_cmd,
    'abort': abort_cmd,
}

def cmd(action: str = typer.Argument(...)):
    if action in action_table.keys():
        typer.echo(f'ACTION: {subcmd}')
        action_table[subcmd]()
    else:
        typer.echo(f'Unknown ACTION: {subcmd}')

if __name__ == '__main__':
    typer.run(cmd)
