#!/usr/bin/env python

import click

@click.command()
@click.option('-v', '--verbose', count=True, help='Verbosly Mode')
def cmd(verbose):
    click.echo(f'verbose level: {verbose}')

if __name__ == '__main__':
    cmd()

