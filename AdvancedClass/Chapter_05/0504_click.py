import click

@click.command()
@click.option('--verbose', '-v', is_flag=True, help='verbose mode')
@click.option('--outfile','-o', help='output file')
@click.option('--pat','-p', type=str, help='search pattern')
@click.option('--overwrite',
    type=click.Choice(['yes', 'no'], case_sensitive=False),
    default='no', help='overwrite if file existing')
@click.argument('filename', type=click.Path(exists=True), nargs=-1)
def cmd(**kwargs):
   print(kwargs)

cmd()
