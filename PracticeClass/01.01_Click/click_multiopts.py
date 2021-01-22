#!/usr/bin/env python

import click

@click.command()
@click.option('-m', '--message', multiple=True)
# @click.option('-m', '--message')
def cmd(message):
    click.echo( message )

if __name__ == '__main__':
    cmd()
