#!/usr/bin/env python

import time
import click
import click_spinner

@click.command()
def cli():
    spinner = click_spinner.Spinner()
    click.echo('Start:')
    spinner.start()
    time.sleep(20)
    spinner.stop()
    click.echo('End')

if __name__ == '__main__':
    cli()
