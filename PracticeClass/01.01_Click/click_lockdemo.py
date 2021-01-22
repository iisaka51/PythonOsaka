import time
import click
import click_lock

@click.command()
@click_lock.lock
def cmd():
    time.sleep(10)

if __name__ == '__main__':
    cmd()
