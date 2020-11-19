import click
import logging

logger = logging.getLogger(__name__)
# click_log.basic_config(logger)

@click.command()
@click.option('--verbose', default=False, is_flag=True)
# @click_log.simple_verbosity_option(logger)
def cmd(verbose):
    if verbose:
        logger.setLevel(logging.INFO)
        logger.info("Dividing by zero.")
    else:
        logger.setLevel(logging.ERROR)

    try:
        1 / 0
    except:
        logger.error("Failed to divide by zero.")


if __name__ == '__main__':
    cmd()
