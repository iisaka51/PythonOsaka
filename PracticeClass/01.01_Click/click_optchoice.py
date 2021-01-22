#!/usr/bin/env python

import click

@click.command()
@click.option('-H', '--hash-type', type=click.Choice(['md5', 'sha1']))
def cmd(hash_type):
    click.echo( hash_type )

if __name__ == '__main__':
    cmd()

