#!/usr/bin/env python

import click
from click_shell import shell

@shell(prompt="myapp > ", intro='Starting my app...')
def myapp():
    pass

@myapp.command()
def initdb():
    click.echo('Initialized the database')

@myapp.command()
def dropdb():
    click.echo('Droped the database')

if __name__ == "__main__":
    myapp()
