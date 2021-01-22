import logging
from logging.config import fileConfig

fileConfig('logconf.ini')
logger = logging.getLogger()
logger.debug(f'This is simple test')
