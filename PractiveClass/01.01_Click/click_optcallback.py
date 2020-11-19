#!/usr/bin/env python

import click

def print_version(ctx, param, value):
    click.echo(dir(param))
    click.echo(value)
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version 1.0')
    ctx.exit()

@click.command()
@click.option('--version', is_flag=True, callback=print_version,
              expose_value=False, is_eager=True)

def cmd():
        click.echo('command was done.')

if __name__ == '__main__':
    cmd()

