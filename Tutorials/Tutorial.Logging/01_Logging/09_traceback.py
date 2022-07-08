import logging
from logging.config import fileConfig

fileConfig('logconf.ini')
logger = logging.getLogger()
logger.debug('This is simple test')

try:
    1 / 0
except ZeroDivisionError as msg:
    logger.exception(f'Raise Exception: {msg}')
