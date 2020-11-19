#!/usr/bin/env python

import click

@click.group()
def cli():
    pass

@click.command()
def initdb():
    click.echo('Initialized the database')

@click.command()
def dropdb():
    click.echo('Droped the database')

cli.add_command(initdb)
cli.add_command(dropdb)

if __name__ == "__main__":
    cli()
