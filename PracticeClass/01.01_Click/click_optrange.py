#!/usr/bin/env python

import click

max_cpus=8
@click.command()
@click.option('-N', '--ncpus', type=click.IntRange(1,max_cpus,clamp=True),
              help=f'Set cpu numbers. (1...{max_cpus})')
def cmd(ncpus):
    click.echo( ncpus )

if __name__ == '__main__':
    cmd()

