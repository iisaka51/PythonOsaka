#!/usr/bin/env python

import click

@click.command()
@click.argument('srcfile', type=click.File('r'))
def cmd(srcfile):
    lines = srcfile.readlines()
    for line in lines:
        click.echo( line[:-1] )

if __name__ == '__main__':
    cmd()

