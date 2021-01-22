#!/usr/bin/env python

import click

@click.command()
@click.argument('srcfile', type=click.Path(exists=True))
def cmd(srcfile):
    print(type(srcfile))
    click.echo( click.format_filename(srcfile) )

if __name__ == '__main__':
    cmd()

