import click
import math
import time
import random

@click.command()
@click.option('--count', default=8000, type=click.IntRange(1, 100000),
              help='The number of items to process.')
def cmd(count):
    """Demonstrates the progress bar."""
    items = range(count)

    def process_slowly(item):
        time.sleep(0.002 * random.random())

    def filter(items):
        for item in items:
            if random.random() > 0.3:
                yield item

    with click.progressbar(items, label='Processing accounts',
                           fill_char=click.style('#', fg='green')) as bar:
        for item in bar:
            process_slowly(item)

    def show_item(item):
        if item is not None:
            return 'Item #%d' % item

    with click.progressbar(filter(items), label='Committing transaction',
                           fill_char=click.style('#', fg='yellow'),
                           item_show_func=show_item) as bar:
        for item in bar:
            process_slowly(item)

    with click.progressbar(length=count, label='Counting',
                           bar_template='%(label)s  %(bar)s | %(info)s',
                           fill_char=click.style('█', fg='cyan'),
                           empty_char=' ') as bar:
        for item in bar:
            process_slowly(item)

    with click.progressbar(length=count, width=0, show_percent=False,
                           show_eta=False,
                           fill_char=click.style('#', fg='magenta')) as bar:
        for item in bar:
            process_slowly(item)

    # 'Non-linear progress bar'
    steps = [math.exp( x * 1. / 20) - 1 for x in range(20)]
    count = int(sum(steps))
    with click.progressbar(length=count, show_percent=False,
                           label='Slowing progress bar',
                           fill_char=click.style('█', fg='green')) as bar:
        for item in steps:
            time.sleep(item)
            bar.update(item)


if __name__ == '__main__':
    cmd()
