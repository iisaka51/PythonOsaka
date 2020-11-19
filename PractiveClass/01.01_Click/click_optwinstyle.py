#!/usr/bin/env python

import click

@click.command()
@click.option('/debug;/no-debug')
def cmd(debug):
    click.echo( 'debug=%s' % debug )

if __name__ == '__main__':
    cmd()

