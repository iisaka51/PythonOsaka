#!/usr/bin/env python

import click

@click.command()
@click.option('paths', '--path', envvar='PATH', multiple=True, type=click.Path())
def cmd(paths):
    for path in paths:
        click.echo( path )

if __name__ == '__main__':
    cmd()

