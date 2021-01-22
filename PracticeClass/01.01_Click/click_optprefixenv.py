#!/usr/bin/env python

import click

@click.command()
@click.option('--user', envvar='USER')
@click.option('--home', envvar='HOME')
def cmd(user, home):
    click.echo( user )
    click.echo( home )

if __name__ == '__main__':
    cmd(auto_envvar_prefix='DEMO')

