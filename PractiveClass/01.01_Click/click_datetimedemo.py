#!/usr/bin/env python

import click
from click_datetime import Datetime
from datetime import datetime

@click.command()
@click.option('--date',
        type=Datetime(format='%Y-%m-%d'), default=datetime.now(),
        help='An example parsing and printing a datetime.')
def cmd(date):
    click.echo('The date : {0}'.format(date))

if __name__ == '__main__':
    cmd()

