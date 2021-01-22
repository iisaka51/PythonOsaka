import click

def validate_rolls(ctx, param, value):
    try:
        rolls, dice = map(int, value.split('d', 2))
        return (dice, rolls)
    except ValueError:
        raise click.BadParameter('rolls need to be in format NdM')

@click.command()
@click.option('--rolls', callback=validate_rolls, default='1d6')
def roll(rolls):
    click.echo(f'Rolling a {rolls[0]}-sided dice {rolls[1]} time(s)')

if __name__ == '__main__':
    roll()
