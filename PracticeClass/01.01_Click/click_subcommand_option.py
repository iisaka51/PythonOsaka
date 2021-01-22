#!/usr/bin/env python

import click

@click.group()
def cli():
    pass

@click.command()
def initdb():
    click.echo('Initialized the database')

@click.command()
@click.option('--force', is_flag=True, default=True, help='drop db anyway')
@click.argument('name')
def dropdb(force, name):
    click.echo(force)
    click.echo('Droped the database:%s' % name)

cli.add_command(initdb)
cli.add_command(dropdb)

if __name__ == "__main__":
    cli()
