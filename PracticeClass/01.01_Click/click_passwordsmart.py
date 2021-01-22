#!/usr/bin/env python

import click

@click.command()
@click.password_option()
def cmd(password):
    click.echo( password )

if __name__ == '__main__':
    cmd()

