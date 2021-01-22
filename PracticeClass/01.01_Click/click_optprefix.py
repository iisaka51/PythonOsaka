#!/usr/bin/env python

import click

@click.command()
@click.option('+w/-w', default=True)
def cmd(w):
    click.echo( 'writable=%s' % w )

if __name__ == '__main__':
    cmd()

