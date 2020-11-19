#!/usr/bin/env python

import click

@click.command()
@click.option('-P', '--position', nargs=2, help='Geometory: X y')
def cmd(position):
    click.echo( position )

if __name__ == '__main__':
    cmd()

