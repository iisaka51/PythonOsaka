#!/usr/bin/env python

import click

@click.command()
@click.option('--password', prompt='Password',
              hide_input=True, confirmation_prompt=True)
def cmd(password):
    click.echo( password )

if __name__ == '__main__':
    cmd()

