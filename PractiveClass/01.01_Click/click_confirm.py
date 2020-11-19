#!/usr/bin/env python

import click

@click.command()
@click.confirmation_option(prompt='Are you sure you want to drop the db?')
def cmd():
    click.echo('Dropped all tables!')

if __name__ == '__main__':
    cmd()

