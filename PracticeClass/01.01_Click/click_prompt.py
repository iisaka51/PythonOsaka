#!/usr/bin/env python

import click

@click.command()
@click.option('--name', prompt='Your Name')
def cmd(name):
    click.echo( name )

if __name__ == '__main__':
    cmd()

