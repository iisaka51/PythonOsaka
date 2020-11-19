#!/usr/bin/env python

import click

@click.command()
@click.option('--debug', is_flag=True, help='DEBUG mode')
def cmd(debug):
    click.echo( f'DEBUG mode {debug}')

if __name__ == '__main__':
    cmd()

