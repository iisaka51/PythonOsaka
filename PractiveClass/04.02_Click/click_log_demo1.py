@click.command()
@click.option('--quiet', default=False, is_flag=True)
def cmd(quiet):
    click.echo("Dividing by zero.")

    try:
        1 / 0
    except:
        click.echo("ERROR: Failed to divide by zero.")

if __name__ == '__main__':
    cmd()
